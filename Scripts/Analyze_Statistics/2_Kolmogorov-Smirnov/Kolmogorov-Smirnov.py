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
                        print(f"数据格式错误 @文件 {path} 行 {reader.line_num}: {e}")

    except FileNotFoundError:
        print(f"文件 {path} 未找到，跳过处理")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', 0, '文件未找到'])
        continue
    except Exception as e:
        print(f"处理 {path} 时发生错误: {e}")
        remark = f"文件读取错误: {e}"

    sample_size = len(current_data)
    if sample_size <= 5000:
        print(f"文件 {path} 样本量 {sample_size} 没有达到推荐范围(5000以上)")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', sample_size, f"{remark}无效样本量"])
        continue

    if len(set(current_data)) == 1:

        print(f"文件 {path} 所有数据值相同（值={current_data[0]}），无法进行K-S检验")
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
        print(f"文件 {path} 检验时发生错误: {e}")
        with open('Results.csv', 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([path, 'N/A', 'N/A', 'N/A', sample_size, f"{remark}检验错误"])
        continue

    print(f"\n文件 {path} 的K-S检验结果:")
    print(f"统计量 D = {statistic:.4f}")
    print(f"p值 = {p_value:.4f}")
    print("数据服从正态分布" if is_normal else "数据不服从正态分布")
    print("-" * 50)
