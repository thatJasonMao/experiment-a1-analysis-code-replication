import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sympy.physics.control.control_plots import matplotlib

# Security/Robot/Passenger
group_name = "Security"

key_word = "Gaze Distance"

files = [f'{group_name}_A1.csv', f'{group_name}_A2.csv', f'{group_name}_B1.csv',
         f'{group_name}_B2.csv', f'{group_name}_B3.csv', f'{group_name}_B4.csv', f'{group_name}_B5.csv']

dfs = []
for file in files:
    df = pd.read_csv(file)
    scenario = file.split('/')[-1].split('.')[0]
    df['Scenario'] = scenario
    dfs.append(df)

combined_df = pd.concat(dfs, ignore_index=True)

melted_df = pd.melt(combined_df, id_vars=['Scenario'], var_name='Subject', value_name='Distance')
melted_df = melted_df[melted_df['Subject'] != 'Scenario']
melted_df['Distance'] = pd.to_numeric(melted_df['Distance'], errors='coerce')

plt.rcParams['figure.dpi'] = 600
plt.rcParams['font.sans-serif'] = ['Times New Roman']

plt.rcParams.update({'font.size': 15})

plt.figure(figsize=(15, 10))

ax = sns.boxplot(x='Scenario', y='Distance', data=melted_df, palette='pastel')

boxes = [artist for artist in ax.get_children() if isinstance(artist, matplotlib.patches.PathPatch)]
box_centers = []

for box in boxes:
    verts = box.get_path().vertices
    y_center = (verts[:,1].min() + verts[:,1].max()) / 2
    box_centers.append(y_center)

means = melted_df.groupby('Scenario')['Distance'].mean()

for i, (mean, center) in enumerate(zip(means, box_centers)):
    plt.text(i, center, f'Mean: {mean:.2f}',
             horizontalalignment='center',
             verticalalignment='center',

             fontsize=15,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round'))

plt.title(f'{key_word} at Each Level')
plt.xlabel('Level')
plt.ylabel(f'{key_word}(m)')

plt.savefig(f'{key_word}_{group_name}_Box_Plot.png', dpi=600, bbox_inches='tight')
