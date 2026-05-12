import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

file_path = 'SSQ-Results-2025-0209-14-54.xlsx'
df = pd.read_excel(file_path)

ssq_value = df.iloc[:, 2]
n_scale = df.iloc[:, 3]
o_scale = df.iloc[:, 4]
d_scale = df.iloc[:, 5]

def print_vio(data_container, name):
    plt.rcParams['figure.dpi'] = 300
    plt.figure(figsize=(2000 / 300, 2000 / 300))

    avg = np.mean(data_container)
    variance = np.var(data_container)

    print(f"Mean of {name} / {name}的均值是: {avg}")
    print(f"Variance of {name} / {name}的方差是: {variance}")

    ax = sns.violinplot(y=data_container, width=0.55)
    for violin in ax.collections:
        violin.set_facecolor('#C4DFFF')

    plt.title(f'Participant {name} Distribution')
    plt.ylabel('Value')

    plt.savefig(f'{name}_violin_plot.png', dpi=300, bbox_inches='tight')

    # plt.show()

print_vio(ssq_value, "SSQ Value")
print_vio(n_scale,"N_Scale")
print_vio(o_scale,"O_Scale")
print_vio(d_scale, "D_Scale")
