import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excel_file = pd.ExcelFile('GSE-Results-2025-0209-16-53.xlsx')

sheet_names = excel_file.sheet_names

df = excel_file.parse(sheet_names[0])

gses = df.iloc[:, 2].tolist()

print(gses)
print(str(len(gses)))

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

avg_gse = np.mean(gses)
variance_gse = np.var(gses)

print(f"GSE的均值是: {avg_gse}")
print(f"GSE的方差是: {variance_gse}")

ax = sns.violinplot(y=gses, width=0.55)
for violin in ax.collections:
    violin.set_facecolor('#C4DFFF')

plt.title('Participant GSE Distribution')
plt.ylabel('GSE')

plt.savefig('GSE_violin_plot.png', dpi=300, bbox_inches='tight')

plt.show()
