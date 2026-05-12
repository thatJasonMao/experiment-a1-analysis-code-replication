import pandas as pd
import matplotlib.pyplot as plt

def autopct_format(values):
    def my_format(pct):
        return f'{pct:.1f}%'

    return my_format

file_path = 'Location.xlsx'
df = pd.read_excel(file_path)

location_column = df.iloc[:, 4]

location_counts = location_column.value_counts()

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

colors = ['#C4DFFF', '#FAE2D3', '#FFF5D3']

patches, texts, autotexts = plt.pie(
    location_counts,
    labels=location_counts.index,
    autopct=autopct_format(location_counts),
    colors=colors,
    wedgeprops={'linewidth': 1, 'edgecolor': 'black'}
)

for text in texts:
    text.set_fontsize(10)
    text.set_position((0.5 * text.get_position()[0], 0.5 * text.get_position()[1]))

for autotext in autotexts:
    autotext.set_fontsize(10)
    autotext.set_position((0.5 * autotext.get_position()[0], 0.5 * autotext.get_position()[1]))

plt.title('Participant Location Distribution')

plt.savefig('location_plot.png', dpi=300, bbox_inches='tight')

plt.show()
