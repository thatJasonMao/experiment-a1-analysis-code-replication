import csv
from scipy import stats
from itertools import combinations

paths = ["Data_1.csv", "Data_2.csv", "Data_3.csv"]

data_list = []

for path in paths:
    current_data = []
    with open(path, mode='r', newline='', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                current_data.append(float(row[0]))
    data_list.append(current_data)

f_stat, p_value = stats.f_oneway(*data_list)
print(f"单因素方差分析结果: F={f_stat:.4f}, p={p_value:.4e}")

if p_value < 0.05:
    print("\n结果显著，进行Bonferroni校正...")

    comparisons = list(combinations(range(len(data_list)), 2))

    alpha = 0.05 / len(comparisons)
    n_groups = len(data_list)
    result_matrix = [['—' for _ in range(n_groups)] for _ in range(n_groups)]

    for i, j in comparisons:
        t_stat, p = stats.ttest_ind(data_list[i], data_list[j])
        significance = '显著' if p < alpha else '不显著'
        result_matrix[i][j] = f"{p:.4e}-{significance}"
        print(f"组{i + 1} vs 组{j + 1}: p={p:.4e} (校正后α={alpha:.4e}) -> {'显著' if p < alpha else '不显著'}")

    print("\n多重比较结果矩阵:")
    header = ["组别"] + [f"组{i+1}" for i in range(n_groups)]
    print("\t".join(header))
    for idx, row in enumerate(result_matrix):
        print(f"组{idx+1}\t" + "\t".join(row))

    with open("多重比较结果.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        for idx, row in enumerate(result_matrix):
            writer.writerow([f"组{idx+1}"] + row)

else:
    print("\n结果不显著，无需事后检验")
