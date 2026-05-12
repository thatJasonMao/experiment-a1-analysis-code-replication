import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def calculate_follow_ratio(file_path):
    df = pd.read_csv(file_path, header=None)
    follow_count = (df.iloc[:, 4] == 'Follow').sum()
    total_count = len(df)
    follow_ratio = follow_count / total_count * 100
    return follow_ratio, follow_count

leaders = ['Passenger', 'Robot', 'Security']
scenarios = ['A2', 'B1', 'B2', 'B3', 'B4', 'B5']

follow_ratios = {leader: {} for leader in leaders}
follow_counts = {leader: {} for leader in leaders}

for leader in leaders:
    for scenario in scenarios:
        file_path = f'{leader}_{scenario}.csv'
        ratio, count = calculate_follow_ratio(file_path)
        follow_ratios[leader][scenario] = ratio
        follow_counts[leader][scenario] = count

ratios_df = pd.DataFrame(follow_ratios)
counts_df = pd.DataFrame(follow_counts)

ratios_df = ratios_df.reindex(index=ratios_df.index[::-1])
counts_df = counts_df.reindex(index=counts_df.index[::-1])

width = 2000 / 300
height = 2000 / 300
plt.figure(figsize=(width, height), dpi=300)

ratios_df.plot(kind='barh', stacked=False)

plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['figure.dpi'] = 300

default_font_size = plt.rcParams['font.size']
new_font_size = default_font_size * 0.5
plt.rcParams.update({'font.size': new_font_size})

plt.title('各场景中受试者在 DP3 的跟随比例')
plt.xlabel('跟随比例(%)')
plt.ylabel('场景')

plt.xticks(rotation=0)
plt.gca().xaxis.set_major_formatter(FuncFormatter(lambda x, _: f'{x:.2f}%'))

for i, col in enumerate(ratios_df.columns):
    for j, (ratio, count) in enumerate(zip(ratios_df[col], counts_df[col])):
        plt.text(ratio, j - 0.1 + i * 0.2, f'{ratio:.2f}% ({count})', color='black', va='center', fontsize=new_font_size)

legend = plt.legend(title='领导者', loc='upper right')
for text in legend.get_texts():
    text.set_fontsize(new_font_size)
legend.get_title().set_fontsize(new_font_size)

plt.tight_layout()

plt.savefig('destination_distribution.png', dpi=300, bbox_inches='tight')
plt.close()
