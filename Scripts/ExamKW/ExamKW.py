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

if len(csv_files) == 2:
    data0 = []
    data1 = []

    file0 = csv_files[0]
    file1 = csv_files[1]

    with open(file0, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data = float(row[1])
            data0.append(data)

    with open(file1, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            data = float(row[1])
            data1.append(data)

    statistic, p_value = stats.kruskal(data0, data1)

    alpha = 0.05
    if p_value < alpha:
        print("拒绝原假设，两组数据分布存在显著差异。")
    else:
        print("不能拒绝原假设，两组数据分布无显著差异。")
