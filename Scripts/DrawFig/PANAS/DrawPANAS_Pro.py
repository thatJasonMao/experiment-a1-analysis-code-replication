import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

try:
    before_data = pd.read_excel('Before.xlsx')
    after_data = pd.read_excel('After.xlsx')
except FileNotFoundError:
    print("File not found / 文件未找到，请确保 'Before.xlsx' 和 'After.xlsx' 在脚本同一目录下。")
else:
    PANAS_Before = before_data.iloc[:, 3].astype(float)
    PANAS_After = after_data.iloc[:, 3].astype(float)

    mean_before = np.mean(PANAS_Before)
    var_before = np.var(PANAS_Before)
    mean_after = np.mean(PANAS_After)
    var_after = np.var(PANAS_After)

    print(f"PANAS_Before mean / PANAS_Before 均值: {mean_before}, variance / 方差: {var_before}")
    print(f"PANAS_After mean / PANAS_After 均值: {mean_after}, variance / 方差: {var_after}")

    plt.rcParams['figure.dpi'] = 300

    plt.rcParams.update({'font.size': 15})

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    violin1 = sns.violinplot(data=PANAS_Before, ax=axes[0])
    for violin in violin1.collections:
        violin.set_edgecolor('black')
        violin.set_facecolor('#C4DFFF')
    axes[0].set_title('Pre-NA Distribution')
    axes[0].set_ylabel('NA Value')

    violin2 = sns.violinplot(data=PANAS_After, ax=axes[1])
    for violin in violin2.collections:
        violin.set_edgecolor('black')
        violin.set_facecolor('#FAE2D3')
    axes[1].set_title('Post-NA Distribution')
    axes[1].set_ylabel('NA Value')

    plt.tight_layout()

    fig.set_size_inches(4000 / 300, 2000 / 300)
    plt.savefig('PANAS_distribution.png', dpi=300)
