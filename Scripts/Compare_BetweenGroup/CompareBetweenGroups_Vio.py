import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

compare_id = "Number of Gaze on Leader"

value_name = "Number of Gaze on Leader"

leaders = ['Passenger', 'Robot', 'Security']
scenarios = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']

all_data = []

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

fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(18, 12))

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

min_value = all_data['value'].min()
max_value = all_data['value'].max()

colors = ['#C4DFFF', '#FAE2D3', '#FFF5D3']

for scenario in scenarios:
    subset = all_data[all_data['scenario'] == scenario]
    row, col = positions[scenario]
    ax = axes[row, col]

    if scenario in ['A1', 'A2']:
        combined_data = subset['value']
        violin = sns.violinplot(y=combined_data, ax=ax, color=colors[0])
        ax.set_title(f'Level:{scenario} {compare_id}')
        ax.set_xlabel('Total Participant Group')
        ax.set_ylabel(value_name)
        mean = combined_data.mean()
        ax.text(0, mean, f'{mean:.2f}', ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
    else:
        violin = sns.violinplot(x='leader', y='value', data=subset, ax=ax, hue='leader', palette=colors, legend=False)
        ax.set_title(f'Level:{scenario} {compare_id}')
        ax.set_xlabel('Leader Type')
        ax.set_ylabel(value_name)
        ax.tick_params(axis='x', rotation=45)

        means = subset.groupby('leader')['value'].mean()
        for j, mean in enumerate(means):
            ax.text(j, mean, f'{mean:.2f}', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

    ax.set_ylim(min_value, max_value)

plt.tight_layout()

plt.savefig(f'{compare_id}_violin_plots.png', bbox_inches='tight', dpi=600)

plt.close()
