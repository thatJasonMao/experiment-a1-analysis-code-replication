import os
import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from itertools import combinations

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

compare_id = "DTW between scenarios and groups"
value_name = "DTW Value"

output_dir = os.path.join(SCRIPT_DIR, "DTW")
os.makedirs(output_dir, exist_ok=True)

leaders = ['Passenger', 'Robot', 'Security']
scenarios = ['A2', 'B1', 'B2', 'B3', 'B4', 'B5']
alpha = 1.0
box_width = 0.6

dtw_path = os.path.join(PROJECT_ROOT, "Results", "TrajDTW.csv")
sl_path = os.path.join(PROJECT_ROOT, "Results", "Subject_Leader.csv")

dtw_data = {}
with open(dtw_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        level_name = row[0].replace('.csv', '')
        subject = level_name.split('_')[0]
        level = level_name.split('_')[1]
        value = float(row[1])
        dtw_data[(subject, level)] = value

sl_data = {}
with open(sl_path, 'r', encoding='utf-8') as f:
    reader = csv.reader(f)
    headers = next(reader)
    for row in reader:
        if len(row) > 1:
            name = row[0]
            sl_data[name] = {}
            for i in range(1, len(headers)):
                sl_data[name][headers[i]] = row[i]

def get_leader(name, level):
    if name not in sl_data:
        return None
    val = sl_data[name].get(level, '')
    if 'Passenger' in val:
        return 'Passenger'
    if 'Security' in val:
        return 'Security'
    if 'Robot' in val:
        return 'Robot'
    return None

all_data = []

for scenario in scenarios:
    for (subject, level), value in dtw_data.items():
        if level != scenario:
            continue
        leader = get_leader(subject, scenario)
        if leader is None and scenario == 'A2':
            leader = 'All'
        if leader is None:
            continue
        all_data.append(pd.DataFrame({
            'subject': [subject],
            'value': [value],
            'leader': [leader],
            'scenario': [scenario]
        }))

all_data = pd.concat(all_data, ignore_index=True)

min_value = all_data['value'].min()
max_value = all_data['value'].max()
y_range = max_value - min_value

def p_to_stars(p):
    if p < 0.001:
        return '***'
    elif p < 0.01:
        return '**'
    elif p < 0.05:
        return '*'
    else:
        return 'ns'

def add_significance_brackets(ax, data_groups, group_positions, y_max, y_range):
    n = len(data_groups)
    pairs = list(combinations(range(n), 2))

    if n < 2:
        return

    sig_pairs = []
    for i, j in pairs:
        g1 = [x for x in data_groups[i] if not np.isnan(x)]
        g2 = [x for x in data_groups[j] if not np.isnan(x)]
        if len(g1) < 2 or len(g2) < 2:
            continue
        _, p_val = stats.mannwhitneyu(g1, g2, alternative='two-sided')
        sig_pairs.append((i, j, p_val))

    bracket_step = y_range * 0.10
    bracket_height = y_range * 0.025
    tip_height = y_range * 0.018

    current_top = y_max + y_range * 0.05

    for idx, (i, j, p_val) in enumerate(sig_pairs):
        stars = p_to_stars(p_val)
        x1 = group_positions[i]
        x2 = group_positions[j]
        y = current_top + idx * bracket_step

        ax.plot([x1, x1, x2, x2],
                [y - tip_height, y, y, y - tip_height],
                color='black', linewidth=0.9)

        label = f'{stars}  p={p_val:.3f}' if stars != 'ns' else f'p={p_val:.3f}'
        ax.text((x1 + x2) / 2, y + bracket_height * 0.3, label,
                ha='center', va='bottom', fontsize=9.5, color='black')

    new_ylim_top = current_top + len(sig_pairs) * bracket_step + bracket_step
    ax.set_ylim(ax.get_ylim()[0], new_ylim_top)

plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.sans-serif'] = ['Arial']
plt.rcParams['font.size'] = 18

fig, axes = plt.subplots(nrows=3, ncols=2, figsize=(16, 11),
                        gridspec_kw={'hspace': 0.35, 'wspace': 0.3})
fig.suptitle(compare_id, fontsize=22, fontweight='bold', y=0.94)

positions = {
    'A2': (0, 0),
    'B1': (0, 1),
    'B2': (1, 0),
    'B3': (1, 1),
    'B4': (2, 0),
    'B5': (2, 1)
}

colors = sns.color_palette("coolwarm", n_colors=3)

for scenario in scenarios:
    subset = all_data[all_data['scenario'] == scenario]
    row, col = positions[scenario]
    ax = axes[row, col]

    if scenario == 'A2':
        combined_data = subset['value']
        boxplot = ax.boxplot(combined_data, patch_artist=True, widths=box_width,
                           tick_labels=['All Participant Groups'])
        mean = combined_data.mean()
        with open(os.path.join(output_dir, f'{scenario}_mean.csv'), 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerow(['All Participant Groups', mean])
        for patch in boxplot['boxes']:
            patch.set_facecolor(colors[0])
            patch.set_alpha(alpha)
        ax.set_title(f'scenario: {scenario}')
        ax.set_ylabel(value_name)
        ax.text(1, mean, f'{mean:.2f}', ha='center', va='center',
                bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))
        ax.set_ylim(min_value, max_value)
    else:
        data_to_plot = [subset[subset['leader'] == leader]['value'].dropna().tolist() for leader in leaders]
        boxplot = ax.boxplot(data_to_plot, tick_labels=leaders, patch_artist=True, widths=box_width)
        means = subset.groupby('leader')['value'].mean()
        with open(os.path.join(output_dir, f'{scenario}_mean.csv'), 'w', newline='', encoding='utf-8') as mean_file:
            mean_writer = csv.writer(mean_file)
            mean_writer.writerow(['Group', 'Mean'])
            mean_writer.writerows(zip(leaders, [means.get(l, 0) for l in leaders]))
        for patch, color in zip(boxplot['boxes'], colors):
            patch.set_facecolor(color)
            patch.set_alpha(alpha)
        ax.set_title(f'scenario: {scenario}')
        ax.tick_params(axis='x')
        ax.set_ylabel(value_name)
        for j, leader in enumerate(leaders, start=1):
            mean = means.get(leader, 0)
            ax.text(j, mean, f'{mean:.2f}', ha='center', va='center',
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round'))

        ax.set_ylim(min_value, max_value)

        try:
            add_significance_brackets(
                ax, data_to_plot,
                group_positions=[1, 2, 3],
                y_max=max_value,
                y_range=y_range
            )
        except Exception as e:
            print(f"  [WARN] Significance test failed for {scenario}: {e}")

plt.savefig(os.path.join(output_dir, f'{compare_id}_box_plots.png'), bbox_inches='tight', dpi=600)
plt.close()
print(f"[DONE] {compare_id}")
