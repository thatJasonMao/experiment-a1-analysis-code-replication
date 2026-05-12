import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excel_file = pd.ExcelFile('PQ.xlsx')

sheet_names = excel_file.sheet_names

df = excel_file.parse(sheet_names[0])

pqs = df.iloc[:, 20].tolist()

print(pqs)
print(str(len(pqs)))

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

avg = np.mean(pqs)
variance = np.var(pqs)

print(f"均值是: {avg}")
print(f"方差是: {variance}")

ax = sns.violinplot(y=pqs, width=0.55)
for violin in ax.collections:
    violin.set_facecolor('#C4DFFF')

plt.title('Participant IPQ Distribution')
plt.ylabel('IPQ Value')

plt.savefig('IPQ_violin_plot.png', dpi=300, bbox_inches='tight')

# plt.show()
