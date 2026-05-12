import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

file_path = 'Preference.xlsx'
df = pd.read_excel(file_path)

familiarity = df.iloc[:, 4]
tendency_follow = df.iloc[:, 5]
tendency_decide = df.iloc[:, 6]

data_containers = [familiarity, tendency_follow, tendency_decide]
container_names = ['Spatial Familiarity', 'Follow Tendency', 'Self-determine Tendency']

for data, name in zip(data_containers, container_names):
    data = data - 0.5

    plt.figure(figsize=(2000 / 300, 2000 / 300), dpi=300)

    n, bins, patches = plt.hist(data, bins=[i + 0.5 for i in range(0, 11)], edgecolor='black', linewidth=1,
                                color='#C4DFFF')

    plt.xlabel('Score')
    plt.xticks(rotation=45)
    plt.ylabel('Number of Participants')
    plt.title(f'Participant {name} Distribution')

    max_y = int(max(n))
    y_ticks = range(0, max_y + 1, 5)
    plt.yticks(y_ticks)

    x_ticks = range(1, 11)
    plt.xticks(x_ticks)

    plt.savefig(f'{name}_histogram.png', bbox_inches='tight')

    plt.close()
