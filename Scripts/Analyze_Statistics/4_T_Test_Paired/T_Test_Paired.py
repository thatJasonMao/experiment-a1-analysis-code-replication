import csv
import numpy as np
from scipy import stats

data_path_A = "Data_1.csv"
data_path_B = "Data_2.csv"

list_A = []
list_B = []

with open(data_path_A, mode='r', newline='', encoding='utf-8', errors='ignore') as file_A:
    reader_A = csv.reader(file_A)
    for row in reader_A:
        if row:
            list_A.append(float(row[0]))

with open(data_path_B, mode='r', newline='', encoding='utf-8', errors='ignore') as file_B:
    reader_B = csv.reader(file_B)
    for row in reader_B:
        if row:
            list_B.append(float(row[0]))

print(f"List A Length: {str(len(list_A))} Content:", list_A)
print(f"List B Length: {str(len(list_B))} Content:", list_B)

t_stat, p_value = stats.ttest_rel(list_A, list_B)
print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:
    diff = [a - b for a, b in zip(list_A, list_B)]

    n = len(diff)
    if n < 5000:
        stat, p_norm = stats.shapiro(diff)
        test_name = "Shapiro-Wilk"
    else:
        stat, p_norm = stats.kstest(diff, 'norm', args=(np.mean(diff), np.std(diff, ddof=1)))
        test_name = "Kolmogorov-Smirnov"

    print(f"\n差值正态性检验 ({test_name}):")
    print(f"统计量: {stat:.4f}, P值: {p_norm:.4f}")

    mean_diff = np.mean(diff)
    pooled_std = np.std(diff, ddof=1)
    cohens_d = mean_diff / pooled_std

    ci_low, ci_high = stats.t.interval(
        0.95,
        df=n - 1,
        loc=mean_diff,
        scale=stats.sem(diff)
    )

    print("\n效应量分析:")
    print(f"Cohen's d: {cohens_d:.4f}")
    print(f"95% 置信区间: [{ci_low:.4f}, {ci_high:.4f}]")
