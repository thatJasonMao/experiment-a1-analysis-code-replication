import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams['figure.dpi'] = 300
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

width = 2000 / 300
height = 2000 / 300
plt.figure(figsize=(width, height), dpi=300)

file_paths = [
    'Security_A2.csv',
    'Security_B1.csv',
    'Security_B2.csv',
    'Security_B3.csv',
    'Security_B4.csv',
    'Security_B5.csv'
]
scenarios = ['A2', 'B1', 'B2', 'B3', 'B4', 'B5']
dp_labels = ['DP1', 'DP2', 'DP3']
follow_ratios = []
follow_counts = []

for file_path in file_paths:
    df = pd.read_csv(file_path, header=None)
    scene_ratios = []
    scene_counts = []
    for col in range(2, 5):
        follow_count = (df.iloc[:, col] == 'Follow').sum()
        ratio = follow_count / len(df) * 100
        scene_ratios.append(ratio)
        scene_counts.append(follow_count)
    follow_ratios.append(scene_ratios)
    follow_counts.append(scene_counts)

follow_ratios = np.array(follow_ratios).T
follow_counts = np.array(follow_counts).T

num_scenarios = len(scenarios)
num_dps = len(dp_labels)
bar_width = 0.8 / num_dps
bar_positions = np.arange(num_scenarios)

fig, ax = plt.subplots(figsize=(10, 8))

for i in range(num_dps):
    bars = ax.barh(bar_positions - bar_width * (num_dps - 1) / 2 + i * bar_width, follow_ratios[i],
                   height=bar_width, label=dp_labels[i])
    for bar, ratio, count in zip(bars, follow_ratios[i], follow_counts[i]):
        ax.text(bar.get_width(), bar.get_y() + bar.get_height() / 2,
                f'{ratio:.2f}% ({count})', ha='left', va='center', fontsize=8)

ax.set_title('不同场景中受试者在DP1、DP2、DP3的跟随比例（Security引导）')
ax.set_xlabel('跟随比例（%）')
ax.set_ylabel('场景')
ax.set_yticks(bar_positions)
ax.set_yticklabels(scenarios)
ax.invert_yaxis()
ax.legend(loc='upper right')

plt.tight_layout()

plt.savefig('destination_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
