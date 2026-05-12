import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

fig_name = "Number of Gaze on Leader"

def draw_group(group_name):
    data_a1 = pd.read_csv(f'{group_name}_A1.csv')
    data_a2 = pd.read_csv(f'{group_name}_A2.csv')
    data_b1 = pd.read_csv(f'{group_name}_B1.csv')
    data_b2 = pd.read_csv(f'{group_name}_B2.csv')
    data_b3 = pd.read_csv(f'{group_name}_B3.csv')
    data_b4 = pd.read_csv(f'{group_name}_B4.csv')
    data_b5 = pd.read_csv(f'{group_name}_B5.csv')

    file_names = [f'{group_name}_A1', f'{group_name}_A2', f'{group_name}_B1', f'{group_name}_B2', f'{group_name}_B3', f'{group_name}_B4', f'{group_name}_B5']
    column_names = [name[-2:] for name in file_names]

    data_a1_dist = data_a1.iloc[:, 1].rename(column_names[0])
    data_a2_dist = data_a2.iloc[:, 1].rename(column_names[1])
    data_b1_dist = data_b1.iloc[:, 1].rename(column_names[2])
    data_b2_dist = data_b2.iloc[:, 1].rename(column_names[3])
    data_b3_dist = data_b3.iloc[:, 1].rename(column_names[4])
    data_b4_dist = data_b4.iloc[:, 1].rename(column_names[5])
    data_b5_dist = data_b5.iloc[:, 1].rename(column_names[6])

    combined_data = pd.concat([data_a1_dist, data_a2_dist, data_b1_dist, data_b2_dist, data_b3_dist, data_b4_dist, data_b5_dist], axis=1)

    correlation_matrix = combined_data.corr(method='spearman')

    print('相关性矩阵：')
    print(correlation_matrix)

    plt.rcParams['figure.dpi'] = 300

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    plt.figure(figsize=(10, 8))
    sns.heatmap(correlation_matrix, annot=True, cmap='plasma', vmin=-1, vmax=1)
    plt.title(f'Correlation of {fig_name} Between Levels Group:{group_name}')

    script_path = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(script_path, f'{fig_name} Correlation Heatmap Group-{group_name}.png')

    plt.savefig(save_path, bbox_inches='tight')

    # plt.show()

if __name__ == "__main__":
    draw_group("Security")
    draw_group("Passenger")
    draw_group("Robot")
