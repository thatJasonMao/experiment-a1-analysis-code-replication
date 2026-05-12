import pandas as pd
import pymc as pm
import itertools
import time
import numpy as np
from sklearn.preprocessing import StandardScaler
import arviz as az
import matplotlib.pyplot as plt
from tqdm import tqdm
import gc
import os
import psutil

CONFIG = {
    'sampling': {
        'draws': 2000,
        'tune': 1000,
        'chains': 4,
        'cores': 16,

        'target_accept': 0.9,
        'progressbar': False
    },
    'memory': {
        'cache_size': 50,

        'plot_dpi': 300

    }
}

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)

if __name__ == "__main__":
    ensure_directory("Results")
    print("初始化高性能计算环境...")

    data = pd.read_csv("Data_Chain_Trim.csv")
    data['DP1_Result'] = data['DP1_Result'].map({'Yes': 1, 'No': 0})

    categorical_cols = ['Gender', '3D', 'XR', 'MetroFrequency', 'LeaderType']
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

    continuous_vars = ['GSE', 'ITS', 'Age', 'FollowRate',
                       'Familiarity', 'FollowTendency', 'SelfDecideTendency', 'Level']
    scaler = StandardScaler()
    data[continuous_vars] = scaler.fit_transform(data[continuous_vars])

    dummy_prefixes = ['Gender_', '3D_', 'XR_', 'MetroFrequency_', 'LeaderType_']
    dummy_cols = [col for col in data.columns if any(col.startswith(p) for p in dummy_prefixes)]
    fixed_effect_cols = continuous_vars + dummy_cols

    subject_code = data['SubjectName'].astype('category').cat.codes.values
    n_subjects = data['SubjectName'].nunique()
    interaction_terms = [(v1, v2, f"{v1}_x_{v2}")
                         for v1, v2 in itertools.combinations(fixed_effect_cols, 2)]

    pbar = tqdm(interaction_terms, desc="贝叶斯交互分析", dynamic_ncols=True)
    for var1, var2, interaction_term in pbar:
        cycle_start = time.time()
        interaction_data = data[var1] * data[var2]

        with pm.Model() as model:
            mu_a = pm.Normal('mu_a', 0, 1)
            sigma_a = pm.HalfNormal('sigma_a', 1)

            subj_intercept = pm.Normal('subj_intercept', mu_a, sigma_a, shape=n_subjects)

            beta_main = {col: pm.Normal(f'beta_{col}', 0, 1) for col in fixed_effect_cols}
            beta_int = pm.Normal(f'beta_{interaction_term}', 0, 1)

            mu = (
                    subj_intercept[subject_code] +
                    sum(beta_main[col] * data[col] for col in fixed_effect_cols) +
                    beta_int * interaction_data
            )
            theta = pm.Deterministic('theta', pm.math.sigmoid(mu))

            pm.Bernoulli('y', theta, observed=data['DP1_Result'])

            trace = pm.sample(**CONFIG['sampling'])

        elapsed_time = time.time() - cycle_start
        with open(f"Results/interaction_{interaction_term}.txt", 'w') as f:
            f.write(f"=== 交互项分析报告 {interaction_term} ===\n")
            f.write(f"分析耗时: {elapsed_time:.1f}s\n\n")

            int_summary = pm.summary(trace, var_names=[f'beta_{interaction_term}'], hdi_prob=0.89)
            f.write("交互项系数:\n" + int_summary.to_string() + "\n\n")

            main_summary = pm.summary(trace, var_names=[f'beta_{var1}', f'beta_{var2}'], hdi_prob=0.89)
            f.write("主效应系数:\n" + main_summary.to_string() + "\n\n")

            full_summary = pm.summary(trace, hdi_prob=0.89)
            f.write("完整模型参数:\n" + full_summary.to_string())

        plt.figure(figsize=(12, 6))
        az.plot_posterior(trace, var_names=[
            f'beta_{interaction_term}',
            f'beta_{var1}',
            f'beta_{var2}'
        ], hdi_prob=0.89)
        plt.suptitle(f'Posterior: {interaction_term}')
        plt.savefig(f"Results/posterior_{interaction_term}.png",
                    dpi=CONFIG['memory']['plot_dpi'], bbox_inches='tight')
        plt.close()

        plt.figure(figsize=(10, 8))
        theta_samples = trace.posterior['theta'].values
        mean_pred = theta_samples.mean(axis=(0, 1))
        scatter = plt.scatter(data[var1], data[var2], c=mean_pred,
                              cmap='viridis', alpha=0.7, s=50)
        plt.colorbar(scatter, label='Possibility')
        plt.xlabel(var1, fontsize=12)
        plt.ylabel(var2, fontsize=12)
        plt.title(f'Prediction: {interaction_term}', pad=20)
        plt.savefig(f"Results/prediction_{interaction_term}.png",
                    dpi=CONFIG['memory']['plot_dpi'], bbox_inches='tight')
        plt.close()
        # endregion

        '''
        if len(mem_cache) >= CONFIG['memory']['cache_size']:
            del mem_cache[0]
            gc.collect()
        mem_cache.append((trace, interaction_term))
        '''

        mem_usage = psutil.Process().memory_info().rss // 1024 ** 2
        pbar.set_postfix_str(f"内存: {mem_usage}MB | 最新项: {interaction_term[:15]}")
        print("\n分析完成！结果已保存至Results目录。")
