import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excel_file = pd.ExcelFile('Age.xlsx')

sheet_names = excel_file.sheet_names

df = excel_file.parse(sheet_names[0])

ages = df.iloc[:, 4].tolist()

print(ages)
print(str(len(ages)))

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

mean_age = np.mean(ages)
variance_age = np.var(ages)

print(f"年龄的均值是: {mean_age}")
print(f"年龄的方差是: {variance_age}")

ax = sns.violinplot(y=ages, width=0.55)
for violin in ax.collections:
    violin.set_facecolor('#C4DFFF')

plt.title('Participant Age Distribution')
plt.ylabel('Age')

plt.savefig('age_violin_plot.png', dpi=300, bbox_inches='tight')

plt.show()
