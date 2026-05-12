import csv
from scipy import stats

paths = ["Data_1.csv", "Data_2.csv", "Data_3.csv"]

with open('Results.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(['文件名', '统计量D', 'p值', '是否正态', '样本量', '备注'])

for path in paths:
    current_data = []
    remark = ''
    try:
        with open(path, mode='r', newline='', encoding='utf-8', errors='ignore') as f:
            reader = csv.reader(f)
            for row in reader:
                if row:
                    try:
                        current_data.append(float(row[0]))
                    except (ValueError, IndexError) as e:
                        remark += f"数据格式错误行{reader.line_num}; "
                        print(f"Data format error / 数据格式错误 @file {path} line {reader.line_num}: {e}")

    except FileNotFoundError:
        print(f"File not found, skipping / 文件 {path} 未找到，跳过处理")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', 0, '文件未找到'])
        continue
    except Exception as e:
        print(f"Error processing file / 处理 {path} 时发生错误: {e}")
        remark = f"文件读取错误: {e}"

    sample_size = len(current_data)
    if sample_size <= 5000:
        print(f"Sample size {sample_size} below recommended range (5000+) for file / 文件 {path} 样本量 {sample_size} 没有达到推荐范围(5000以上)")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', sample_size, f"{remark}无效样本量"])
        continue

    if len(set(current_data)) == 1:

        print(f"All data values identical for file / 文件 {path} 所有数据值相同（值={current_data[0]}）, K-S test not applicable")
        continue
        
    try:
        sample_mean = sum(current_data) / len(current_data)
        sample_std = (sum([(x - sample_mean) ** 2 for x in current_data]) / (len(current_data) - 1)) ** 0.5

        statistic, p_value = stats.kstest(current_data, 'norm', args=(sample_mean, sample_std))

        is_normal = p_value > 0.05

        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([
                path,
                f"{statistic:.4f}",
                f"{p_value:.4f}",
                "是" if is_normal else "否",
                sample_size,
                remark
            ])

    except Exception as e:
        print(f"Error during K-S test for file / 文件 {path} 检验时发生错误: {e}")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', sample_size, f"{remark}检验错误"])
        continue

    print(f"
K-S test results for file / 文件 {path} 的K-S检验结果:")
    print(f"Statistic D / 统计量 D = {statistic:.4f}")
    print(f"p-value / p值 = {p_value:.4f}")
    print("Data follows normal distribution / 数据服从正态分布" if is_normal else "Data does not follow normal distribution / 数据不服从正态分布")
    print("-" * 50)
