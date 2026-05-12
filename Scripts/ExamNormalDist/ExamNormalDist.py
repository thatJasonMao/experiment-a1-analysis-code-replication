import csv
import os
import numpy as np
import scipy.stats as stats

current_folder = os.getcwd()

csv_files = []

for root, dirs, files in os.walk(current_folder):
    for file in files:
        if file.endswith('.csv'):
            csv_files.append(os.path.join(root, file))

for file in csv_files:
    with open(file, 'r', newline='', encoding='utf-8') as csvfile:
        datas = []
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data = float(row[1])
            datas.append(data)
    statistic, p_value = stats.shapiro(datas)
    if p_value > 0.05:
        print(os.path.basename(file) + " conforms to normal distribution / 中的数据符合正态分布")
    if p_value < 0.05:
        print(os.path.basename(file) + " does not conform to normal distribution / 中的数据不符合正态分布")
