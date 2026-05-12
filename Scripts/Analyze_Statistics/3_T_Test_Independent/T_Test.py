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

t_stat, p_value = stats.ttest_ind(list_A, list_B, equal_var=False)
print("T-statistic:", t_stat)
print("P-value:", p_value)

if p_value < 0.05:

    mean_A, mean_B = np.mean(list_A), np.mean(list_B)
    std_A, std_B = np.std(list_A, ddof=1), np.std(list_B, ddof=1)
    n_A, n_B = len(list_A), len(list_B)

    pooled_std = np.sqrt(((n_A - 1) * std_A ** 2 + (n_B - 1) * std_B ** 2) / (n_A + n_B - 2))
    cohen_d = (mean_A - mean_B) / pooled_std

    mean_diff = mean_A - mean_B
    se = np.sqrt(std_A ** 2 / n_A + std_B ** 2 / n_B)
    dof = (std_A ** 2 / n_A + std_B ** 2 / n_B) ** 2 / (
                (std_A ** 4) / (n_A ** 2 * (n_A - 1)) + (std_B ** 4) / (n_B ** 2 * (n_B - 1)))
    ci_low, ci_high = stats.t.interval(0.95, dof, loc=mean_diff, scale=se)

    print(f"\n显著性结果:")
    print(f"Cohen's d = {cohen_d:.4f}")
    print(f"95% CI: [{ci_low:.4f}, {ci_high:.4f}]")
