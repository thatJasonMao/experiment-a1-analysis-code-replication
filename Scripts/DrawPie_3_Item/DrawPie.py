import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

target_level = "B5"

passenger_df = pd.read_csv(f'Passenger_{target_level}.csv')
robot_df = pd.read_csv(f'Robot_{target_level}.csv')
security_df = pd.read_csv(f'Security_{target_level}.csv')

passenger_destinations = passenger_df.iloc[:, 1]
robot_destinations = robot_df.iloc[:, 1]
security_destinations = security_df.iloc[:, 1]

passenger_counts = passenger_destinations.value_counts()
robot_counts = robot_destinations.value_counts()
security_counts = security_destinations.value_counts()

desired_order = ['AR', 'AL', 'BR', 'BL', 'CR', 'CL', 'DR', 'DL']

passenger_counts = passenger_counts.reindex(desired_order, fill_value=0)
robot_counts = robot_counts.reindex(desired_order, fill_value=0)
security_counts = security_counts.reindex(desired_order, fill_value=0)

def create_export_df(counts, group_name):
    total = counts.sum()
    return pd.DataFrame({
        'Destination': counts.index,
        'Count': counts,
        'Percentage': (counts / total * 100).round(1) if total != 0 else 0,
        'Group': group_name
    })

export_df = pd.concat([
    create_export_df(passenger_counts, 'Passenger'),
    create_export_df(robot_counts, 'Robot'),
    create_export_df(security_counts, 'Security')
])
export_df.to_csv(f'sum_{target_level}.csv', index=False)

passenger_counts = passenger_counts[passenger_counts > 0]
robot_counts = robot_counts[robot_counts > 0]
security_counts = security_counts[security_counts > 0]

plt.rcParams.update({'font.size': 25})

plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.sans-serif'] = ['Arial']

fig, axes = plt.subplots(1, 3, figsize=(12, 5))
plt.subplots_adjust(wspace=0.2, hspace=0.3)

pastel_colors = sns.color_palette("vlag", len(desired_order))

BOX_FONT_SIZE = 20

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

def plot_pie(ax, counts, title, radius=0.8):
    colors = [pastel_colors[desired_order.index(label)] for label in counts.index]

    wedges, _ = ax.pie(
        counts,
        labels=None,
        autopct=None,

        colors=colors,
        pctdistance=1.5,
        labeldistance=1.4,
        radius=radius
    )

    annotate_max_slice(ax, counts, wedges, radius=radius, r_frac=0.55)
    ax.set_title(title, y=0.85)

plot_pie(axes[0], passenger_counts, f'{target_level} Group: Passenger', radius=0.8)
plot_pie(axes[1], robot_counts, f'{target_level} Group: Robot', radius=0.8)
plot_pie(axes[2], security_counts, f'{target_level} Group: Security', radius=0.8)

plt.tight_layout()
plt.savefig(f'destination_distribution_{target_level}.png', dpi=600, transparent=True)
plt.close()
