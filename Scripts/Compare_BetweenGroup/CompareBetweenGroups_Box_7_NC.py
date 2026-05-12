import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import csv
import numpy as np
from scipy import stats
from itertools import combinations

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

target_dirs = {
    "MLE":                         os.path.join(PROJECT_ROOT, "Scripts", "Analyze_EyeGaze_Index", "LyapunovData"),
    "Scan Speed":                  os.path.join(PROJECT_ROOT, "Scripts", "Analyze_EyeGaze_Index", "GazeRouteSpeed"),
    "Scan Distance":               os.path.join(PROJECT_ROOT, "Scripts", "Analyze_EyeGaze_Index", "GazeRouteDistance"),
    "Gaze Depth":                  os.path.join(PROJECT_ROOT, "GroupData_Gaze_Obj_Distance"),
    "Evac. Speed":                 os.path.join(PROJECT_ROOT, "GroupData_Avg_Speed"),
    "Evac. Acc.":                  os.path.join(PROJECT_ROOT, "GroupData_Avg_Acc_XZ"),
    "Gazes on Leader":             os.path.join(PROJECT_ROOT, "GroupData_Gaze_On_Leader_Time"),
    "Evac. Distance":              os.path.join(PROJECT_ROOT, "GroupData_Total_Move_Distance"),
    "Evac. Time":                  os.path.join(PROJECT_ROOT, "GroupData_Total_Travel_Time"),
}

decimal_place_map = {
    "MLE": 3,
    "Scan Distance": 1,
}

leaders = ['Passenger', 'Security', 'Robot']
scenarios = ['A1', 'A2', 'B1', 'B2', 'B3', 'B4', 'B5']

sub_folder_path = os.path.join(SCRIPT_DIR, "Results_NC_Final")
os.makedirs(sub_folder_path, exist_ok=True)

alpha = 1.0
box_width = 0.6

colors = sns.color_palette("coolwarm", n_colors=3)

positions = {
    'A1': (0, 0),
    'A2': (0, 1),
    'B1': (1, 0),
    'B2': (1, 1),
    'B3': (1, 2),
    'B4': (2, 0),
    'B5': (2, 1)
}

shift_scenarios = ['A1', 'A2', 'B4', 'B5']

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

for compare_id, source_dir in target_dirs.items():
    if not os.path.isdir(source_dir):
        print(f"[SKIP] Source directory not found: {source_dir}")
        continue

    all_data = []
    missing_files = False

    for leader in leaders:
        for scenario in scenarios:
            file_path = os.path.join(source_dir, f'{leader}_{scenario}.csv')
            if not os.path.isfile(file_path):
                print(f"  [WARN] File not found: {file_path}")
                missing_files = True
                continue
            df = pd.read_csv(file_path)
            for col in df.columns[1:]:
                temp_df = pd.DataFrame({
                    'subject': df.iloc[:, 0].tolist(),
                    'value': df[col].tolist(),
                    'leader': leader,
                    'scenario': scenario
                })
                all_data.append(temp_df)

    if not all_data:
        print(f"[SKIP] No data loaded for: {compare_id}")
        continue

    all_data = pd.concat(all_data, ignore_index=True)

    min_value = all_data['value'].min()
    max_value = all_data['value'].max()
    y_range = max_value - min_value

    plt.rcParams['figure.dpi'] = 800
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.size'] = 16

    fig, axes = plt.subplots(
        nrows=3, ncols=3, figsize=(9.5, 14),
        gridspec_kw={'height_ratios': [1.8, 1.8, 1.8], 'hspace': 0.35, 'wspace': 0.3}
    )

    axes[0, 2].axis('off')
    axes[2, 2].axis('off')

    dx = 1080 / (fig.dpi * fig.get_figwidth())

    for scenario in shift_scenarios:
        row, col = positions[scenario]
        ax = axes[row, col]
        pos = ax.get_position()
        ax.set_position([pos.x0 + dx, pos.y0, pos.width, pos.height])

    axes[0, 2].axis('off')
    axes[2, 2].axis('off')

    for scenario in scenarios:
        subset = all_data[all_data['scenario'] == scenario]
        row, col = positions[scenario]
        ax = axes[row, col]

        if scenario == 'A1' or scenario == 'A2':
            combined_data = subset['value']
            mean = combined_data.mean()

            boxplot = ax.boxplot(
                combined_data, patch_artist=True, widths=box_width,
                tick_labels=['All Participant Groups']
            )
            for patch in boxplot['boxes']:
                patch.set_facecolor(colors[0])
                patch.set_alpha(alpha)
            ax.set_title(f'{scenario}: {compare_id}', fontsize=18)
            ax.tick_params(axis='x', labelsize=14)
            ax.tick_params(axis='y', labelsize=12.8)

            ax.text(
                1, mean, f'{mean:.{decimal_place_map.get(compare_id, 2)}f}',
                ha='center', va='center',
                bbox=dict(
                    facecolor='white', edgecolor='black',
                    boxstyle='round,pad=0.05', alpha=0.65, pad=0.2
                ),
                fontsize=15
            )
            ax.set_ylim(min_value, max_value)
        else:
            data_to_plot = []
            means = []
            for leader in leaders:
                leader_data = subset[subset['leader'] == leader]['value'].dropna().tolist()
                data_to_plot.append(leader_data)
                means.append(np.mean(leader_data) if leader_data else float('nan'))

            boxplot = ax.boxplot(
                data_to_plot, tick_labels=leaders, patch_artist=True, widths=box_width
            )
            for patch, color in zip(boxplot['boxes'], colors):
                patch.set_facecolor(color)
                patch.set_alpha(alpha)

            ax.set_title(f'{scenario}: {compare_id}', fontsize=18)
            ax.tick_params(axis='x', labelsize=11)
            ax.tick_params(axis='y', labelsize=12.8)

            for j, mean in enumerate(means, start=1):
                if not np.isnan(mean):
                    ax.text(
                        j, mean, f'{mean:.{decimal_place_map.get(compare_id, 2)}f}',
                        ha='center', va='center',
                        bbox=dict(
                            facecolor='white', edgecolor='black',
                            boxstyle='round,pad=0.05', alpha=0.65, pad=0.2
                        ),
                        fontsize=15
                    )

            ax.set_ylim(min_value, max_value)

            valid_groups = [g for g in data_to_plot if len(g) >= 2]
            if len(valid_groups) >= 2:
                try:
                    add_significance_brackets(
                        ax, data_to_plot,
                        group_positions=[1, 2, 3],
                        y_max=max_value,
                        y_range=y_range
                    )
                except Exception as e:
                    print(f"  [WARN] Significance test failed for {scenario} ({compare_id}): {e}")

    output_path = os.path.join(sub_folder_path, f'{compare_id}_box_plots_nc.png')
    plt.savefig(output_path, bbox_inches='tight', dpi=800)
    plt.close()
    print(f"[DONE] {compare_id} -> {output_path}")

print("All metrics processed.")
