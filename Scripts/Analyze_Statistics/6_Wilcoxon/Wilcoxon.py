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

if len(list_A) != len(list_B):
    print("错误：两组数据长度不一致，无法进行配对样本检验")

else:
    result = stats.wilcoxon(list_A, list_B)
    print("\n威尔科克森符号秩检验结果:")
    print(f"统计量: {result.statistic:.4f}")
    print(f"P值: {result.pvalue:.4f}")
