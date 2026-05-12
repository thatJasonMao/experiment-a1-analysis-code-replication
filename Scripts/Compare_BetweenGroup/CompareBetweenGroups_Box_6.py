import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv

compare_id = "DTW between Trajectories"

value_name = "Value"

leaders = ['Passenger', 'Robot', 'Security']
scenarios = ['A2', 'B1', 'B2', 'B3', 'B4', 'B5']

all_data = []

alpha = 1.0

box_width = 0.6

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

plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.sans-serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 16

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(20, 14),
                        gridspec_kw={'hspace': 0.35, 'wspace': 0.3})

positions = {
    'A2': (0, 0),
    'B1': (0, 1),
    'B2': (1, 0),
    'B3': (1, 1),
    'B4': (2, 0),
    'B5': (2, 1)
}

# axes[0, 2].axis('off')
# axes[2, 2].axis('off')

min_value = all_data['value'].min()
max_value = all_data['value'].max()

colors = sns.color_palette("vlag", n_colors=3)

for scenario in scenarios:
    subset = all_data[all_data['scenario'] == scenario]
    row, col = positions[scenario]
    ax = axes[row, col]

    if scenario in ['A1', 'A2']:
        combined_data = subset['value']
        boxplot = ax.boxplot(combined_data, patch_artist=True, widths=box_width,
                           labels=['All Participant Groups'])

        mean = combined_data.mean()
        with open(f'{scenario}_mean.csv', 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerow(['All Participant Groups', mean])
        for patch in boxplot['boxes']:
            patch.set_facecolor(colors[0])
            patch.set_alpha(alpha)
        ax.set_title(f'Scenario:{scenario} {compare_id}')
        ax.set_ylabel(value_name)
        mean = combined_data.mean()
        ax.text(1, mean, f'{mean:.2f}', ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

    else:
        data_to_plot = [subset[subset['leader'] == leader]['value'] for leader in leaders]
        boxplot = ax.boxplot(data_to_plot, labels=leaders, patch_artist=True, widths=box_width)

        means = subset.groupby('leader')['value'].mean()
        with open(f'{scenario}_mean.csv', 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerows(zip(leaders, means))
        for patch, color in zip(boxplot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(alpha)
        ax.set_title(f'Scenario:{scenario} {compare_id}')
        ax.tick_params(axis='x')
        ax.set_ylabel(value_name)

        means = subset.groupby('leader')['value'].mean()
        for j, mean in enumerate(means, start=1):
            ax.text(j, mean, f'{mean:.2f}', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

    ax.set_ylim(min_value, max_value)

# plt.tight_layout()

plt.savefig(f'{compare_id}_box_plots.png', bbox_inches='tight', dpi=600)

plt.close()
