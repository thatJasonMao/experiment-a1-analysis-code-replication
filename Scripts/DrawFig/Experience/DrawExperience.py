import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 15})

file_path = 'Experience.xlsx'
df = pd.read_excel(file_path)

column_5 = df.iloc[:, 4]
column_6 = df.iloc[:, 5]

fig, axes = plt.subplots(1, 2, figsize=(12, 6))

colors = ['#C4DFFF', '#FAE2D3']

column_5_counts = column_5.value_counts()
patches_5, texts_5, autotexts_5 = axes[0].pie(
    column_5_counts,
    labels=column_5_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
)
axes[0].axis('equal')
axes[0].set_title('Participant Experience: 3D Games')

for text in texts_5:
    text.set_fontsize(10)
    text.set_position((0.5 * text.get_position()[0], 0.5 * text.get_position()[1]))

for autotext in autotexts_5:
    autotext.set_fontsize(10)
    autotext.set_position((0.5 * autotext.get_position()[0], 0.5 * autotext.get_position()[1]))

column_6_counts = column_6.value_counts()
patches_6, texts_6, autotexts_6 = axes[1].pie(
    column_6_counts,
    labels=column_6_counts.index,
    autopct='%1.1f%%',
    startangle=90,
    colors=colors,
    wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
)
axes[1].axis('equal')
axes[1].set_title('Participant Experience: XR')

for text in texts_6:
    text.set_fontsize(10)
    text.set_position((0.5 * text.get_position()[0], 0.5 * text.get_position()[1]))

for autotext in autotexts_6:
    autotext.set_fontsize(10)
    autotext.set_position((0.5 * autotext.get_position()[0], 0.5 * autotext.get_position()[1]))

plt.tight_layout()

plt.savefig('Combined_PieCharts.png', dpi=300, bbox_inches='tight')
plt.show()
plt.close()
