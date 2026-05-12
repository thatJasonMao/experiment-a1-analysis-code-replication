import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

target_level = "A2"

passenger_df = pd.read_csv(f'Passenger_{target_level}.csv')
robot_df = pd.read_csv(f'Robot_{target_level}.csv')
security_df = pd.read_csv(f'Security_{target_level}.csv')

passenger_destinations = passenger_df.iloc[:, 1]
robot_destinations = robot_df.iloc[:, 1]
security_destinations = security_df.iloc[:, 1]

all_destinations = pd.concat([passenger_destinations, robot_destinations, security_destinations])

all_counts = all_destinations.value_counts()

desired_order = ['AR', 'AL', 'BR', 'BL', 'CR', 'CL', 'DR', 'DL']

all_counts = all_counts.reindex(desired_order, fill_value=0)

total = all_counts.sum()
proportions = all_counts / total if total != 0 else all_counts * 0
result_df = pd.DataFrame({
    'Destination': all_counts.index,
    'Count': all_counts,
    'Proportion': proportions
})
result_df.to_csv(f'sum_{target_level}.csv', index=False)

all_counts = all_counts[all_counts > 0]

plt.rcParams.update({'font.size': 35})

plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.sans-serif'] = ['Arial']

fig, ax = plt.subplots(figsize=(8, 8))

pastel_colors = sns.color_palette("vlag", len(desired_order))

for dest, color in zip(desired_order, pastel_colors):
    r, g, b = [int(x * 255) for x in color]
    hex_color = f"#{r:02x}{g:02x}{b:02x}"
    print(f"{dest}: {hex_color}")

BOX_FONT_SIZE = 30

def annotate_max_slice(ax, counts, wedges, radius=0.8, r_frac=0.55):
    if len(counts) == 0:
        return
    total = counts.sum()
    if total == 0:
        return

    max_idx = int(np.argmax(counts.values))
    w = wedges[max_idx]
    pct = counts.values[max_idx] / total * 100.0

    theta = (w.theta1 + w.theta2) / 2.0
    theta_rad = np.deg2rad(theta)

    r = radius * r_frac
    x = r * np.cos(theta_rad)
    y = r * np.sin(theta_rad)

    ax.text(
        x, y, f"{pct:.2f}%",
        ha="center", va="center",
        fontsize=BOX_FONT_SIZE, color="black",
        bbox=dict(
            boxstyle="round,pad=0.25",
            facecolor="white",
            edgecolor="black",
            linewidth=1,
            alpha=0.95
        )
    )

colors_for_counts = [pastel_colors[desired_order.index(label)] for label in all_counts.index]

wedges, _ = ax.pie(
    all_counts,
    labels=None,
    autopct=None,
    colors=colors_for_counts,
    pctdistance=1.5,
    labeldistance=1.4,
    radius=0.8
)

annotate_max_slice(ax, all_counts, wedges, radius=0.8, r_frac=0.55)

ax.set_title(f'{target_level} Group: Total', y=0.85)

plt.tight_layout()
plt.savefig(f'merge_destination_distribution_{target_level}.png', bbox_inches='tight', dpi=600, transparent=True)
plt.close()
