import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Age.xlsx'
df = pd.read_excel(file_path)

gender_column = df.iloc[:, 3]

gender_distribution = gender_column.value_counts()

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

colors = ['#C4DFFF', '#FAE2D3']

patches, texts, autotexts = plt.pie(gender_distribution, labels=gender_distribution.index, autopct='%1.1f%%',
                                    colors=colors,
                                    wedgeprops={'linewidth': 1, 'edgecolor': 'black'})

for text in texts:
    text.set_fontsize(10)
    text.set_position((0.5 * text.get_position()[0], 0.5 * text.get_position()[1]))

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_position((0.5 * autotext.get_position()[0], 0.5 * autotext.get_position()[1]))

plt.title('Participant Gender Distribution')

plt.axis('equal')

plt.savefig('gender_distribution_pie_chart.png', dpi=300, bbox_inches='tight')

plt.show()
