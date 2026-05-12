import csv
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

statistic, p_value = stats.mannwhitneyu(list_A, list_B, alternative='two-sided')

print("\nMann-Whitney U Test Results:")
print(f"U statistic: {statistic:.4f}")
print(f"P-value: {p_value:.6f}")

alpha = 0.05
if p_value < alpha:
    print("Reject null hypothesis: Significant difference between groups")
else:
    print("Fail to reject null hypothesis: No significant difference")
