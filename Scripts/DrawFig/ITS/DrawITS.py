import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excel_file = pd.ExcelFile('ITS-Results-2025-0210-10-29.xlsx')

sheet_names = excel_file.sheet_names

df = excel_file.parse(sheet_names[0])

itss = df.iloc[:, 2].tolist()

print(itss)
print(str(len(itss)))

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

avg_its = np.mean(itss)
variance_its = np.var(itss)

print(f"ITS的均值是: {avg_its}")
print(f"ITS的方差是: {variance_its}")

ax = sns.violinplot(y=itss, width=0.55)
for violin in ax.collections:
    violin.set_facecolor('#C4DFFF')

plt.title('Participant ITS Distribution')
plt.ylabel('ITS')

plt.savefig('ITS_violin_plot.png', dpi=300, bbox_inches='tight')

plt.show()
