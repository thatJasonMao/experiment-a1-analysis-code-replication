import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

excel_file = pd.ExcelFile('TLX.xlsx')

sheet_names = excel_file.sheet_names

df = excel_file.parse(sheet_names[0])

tlxs = df.iloc[:, 10].tolist()

print(tlxs)
print(str(len(tlxs)))

plt.rcParams['figure.dpi'] = 300
plt.figure(figsize=(2000 / 300, 2000 / 300))

avg = np.mean(tlxs)
variance = np.var(tlxs)

print(f"均值是: {avg}")
print(f"方差是: {variance}")

ax = sns.violinplot(y=tlxs, width=0.55)
for violin in ax.collections:
    violin.set_facecolor('#C4DFFF')

plt.title('Participant NASA-TLX Distribution')
plt.ylabel('NASA-TLX Value')

plt.savefig('TLX_violin_plot.png', dpi=300, bbox_inches='tight')

# plt.show()
