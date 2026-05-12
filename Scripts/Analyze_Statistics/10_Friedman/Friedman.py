import csv
from scipy import stats
import scikit_posthocs as sp
from scipy.stats import friedmanchisquare
import numpy as np

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

data_array = np.array(data_list)

statistic, p_value = friedmanchisquare(*data_array)

print(f"Friedman检验统计量: {statistic}")
print(f"p值: {p_value}")
