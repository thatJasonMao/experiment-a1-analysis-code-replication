import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np

compare_id = "Total Eye Scanning Length"

value_name = "Length (m)"

leaders = ['Passenger', 'Robot', 'Security']
scenarios = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']

all_data = []

alpha = 1.0

for leader in leaders:
    for scenario in scenarios:
        file_path = f'{leader}_{scenario}.csv'
        df = pd.read_csv(file_path)

        for col in df.columns[1:]:
            temp_df = pd.DataFrame({
                'subject': df.iloc[:, 0].tolist(),
                'value': df[col].tolist(),
                'leader': leader,
                'scenario': scenario
            })
            all_data.append(temp_df)

all_data = pd.concat(all_data, ignore_index=True)

plt.rcParams['figure.dpi'] = 800
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 16

fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(20, 14), gridspec_kw={'height_ratios': [1.8, 1.8, 1.8], 'hspace': 0.35, 'wspace': 0.3})

positions = {
    'A1': (0, 0),
    'A2': (0, 1),
    'B1': (1, 0),
    'B2': (1, 1),
    'B3': (1, 2),
    'B4': (2, 0),
    'B5': (2, 1)
}

axes[0, 2].axis('off')
axes[2, 2].axis('off')

dx = 2250 / (fig.dpi * fig.get_figwidth())

shift_scenarios = ['A1', 'A2', 'B4', 'B5']

for scenario in shift_scenarios:
    row, col = positions[scenario]
    ax = axes[row, col]
    pos = ax.get_position()
    ax.set_position([pos.x0 + dx, pos.y0, pos.width, pos.height])

axes[0, 2].axis('off')
axes[2, 2].axis('off')

min_value = all_data['value'].min()
max_value = all_data['value'].max()

colors = sns.color_palette("vlag", n_colors=3)

box_width = 0.6

for scenario in scenarios:
    subset = all_data[all_data['scenario'] == scenario]
    row, col = positions[scenario]
    ax = axes[row, col]

    if scenario == 'A1' or scenario == 'A2':
        combined_data = subset['value']
        mean = combined_data.mean()
        with open(f'{scenario}_mean.csv', 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerow(['All Participant Groups', mean])

        boxplot = ax.boxplot(combined_data, patch_artist=True, widths=box_width, labels=['All Participant Groups'])
        for patch in boxplot['boxes']:
            patch.set_facecolor(colors[0])
            patch.set_alpha(alpha)
        ax.set_title(f'Scenario:{scenario} {compare_id}')
        ax.set_ylabel(value_name)
        ax.text(1, mean, f'{mean:.2f}', ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'), fontsize=12)

    else:
        data_to_plot = [subset[subset['leader'] == leader]['value'] for leader in leaders]
        means = [np.mean(group) for group in data_to_plot]
        with open(f'{scenario}_mean.csv', 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerows(zip(leaders, means))

        boxplot = ax.boxplot(data_to_plot, labels=leaders, patch_artist=True, widths=box_width)
        for patch, color in zip(boxplot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(alpha)
        ax.set_title(f'Scenario:{scenario} {compare_id}')
        ax.set_ylabel(value_name)
        ax.tick_params(axis='x')

        means = subset.groupby('leader')['value'].mean()
        for j, mean in enumerate(means, start=1):
            ax.text(j, mean, f'{mean:.2f}', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'), fontsize=12)

    ax.set_ylim(min_value, max_value)

plt.savefig(f'{compare_id}_box_plots.png', bbox_inches='tight', dpi=800)

plt.close()
