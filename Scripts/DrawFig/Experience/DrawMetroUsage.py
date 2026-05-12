import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

plt.rcParams.update({'font.size': 15})

file_path = 'Experience.xlsx'
df = pd.read_excel(file_path)

column_7 = df.iloc[:, 6]

dict_usage = {
    6: "Multiple times a day",
    5: "Once a day",
    4: "Several times a week, but not every day",
    3: "Once a week",
    2: "Every two to four weeks",
    1: "Once a month/Occasionally",
    0: "Never used"
}

list_usage = []

for usage_id in column_7.keys():
    str_usage = dict_usage[column_7[usage_id]]
    list_usage.append(str_usage)

usage_counts = pd.Series(list_usage).value_counts()

usage_percentages = usage_counts / usage_counts.sum()

plt.figure(figsize=(2000 / 300, 2000 / 300), dpi=300)

colors = sns.color_palette('pastel', len(usage_percentages))

plt.pie(usage_percentages, labels=usage_percentages.index, autopct='%1.1f%%', colors=colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1})

plt.axis('equal')

plt.title('Participant Urban Rail Transit Usage Distribution', y=1.1)

plt.savefig('metro_usage_pie_chart.png', bbox_inches='tight')

# plt.show()
