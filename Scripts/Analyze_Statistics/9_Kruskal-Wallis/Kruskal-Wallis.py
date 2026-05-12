import csv
from scipy import stats
import scikit_posthocs as sp

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

stat, p = stats.kruskal(*data_list)
print(f"Kruskal-Wallis检验结果：\nH统计量={stat:.3f}, p值={p:.4f}")

if p < 0.05:
    print("\n显著性差异存在，进行Dunn检验：")
    dunn_result = sp.posthoc_dunn(data_list, p_adjust='bonferroni')

    groups = [f"Group{i + 1}" for i in range(len(data_list))]

    print("\nDunn检验结果矩阵：")
    print("\t" + "\t".join(groups))
    for i in range(len(dunn_result)):
        row = dunn_result.iloc[i].values
        print(f"{groups[i]}\t" + "\t".join(f"{x:.4f}" for x in row))

    with open('Dunn_Test_Results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([''] + groups)
        for i in range(len(dunn_result)):
            row = dunn_result.iloc[i].tolist()
            writer.writerow([groups[i]] + row)

else:
    print("\n未达到显著性水平，无需进行后续检验")
