import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

files = ['Security_A1.csv', 'Security_A2.csv', 'Security_B1.csv',
         'Security_B2.csv', 'Security_B3.csv', 'Security_B4.csv', 'Security_B5.csv']

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

plt.figure(figsize=(20, 10))

ax = sns.violinplot(x='Scenario', y='Distance', data=melted_df)

means = melted_df.groupby('Scenario')['Distance'].mean()
y_max = melted_df['Distance'].max()
offset = y_max * 0.05

for i, mean in enumerate(means):
    y_pos = mean + offset
    plt.text(i, y_pos, f'Mean: {mean:.2f}',
             horizontalalignment='center', verticalalignment='bottom', fontsize=10,
             bbox=dict(facecolor='white', alpha=0.7, edgecolor='black', boxstyle='round'))

plt.title('各场景下受试者疏散时间')
plt.xlabel('场景')
plt.ylabel('疏散时间')

plt.savefig('violin_plot.png', dpi=600, bbox_inches='tight')

# plt.show()
