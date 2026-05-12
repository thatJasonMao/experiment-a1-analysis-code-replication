import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    data = pd.read_csv("Data_Chain_Trim.csv")

    data['DP1_Result'] = data['DP1_Result'].map({'Yes': 1, 'No': 0})

    categorical_cols = ['Gender', '3D', 'XR', 'MetroFrequency', 'LeaderType']
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

    continuous_vars = ['GSE', 'ITS', 'Age', 'FollowRate',
                       'Familiarity', 'FollowTendency', 'SelfDecideTendency', 'Level']
    scaler = StandardScaler()
    data[continuous_vars] = scaler.fit_transform(data[continuous_vars])

    dummy_cols = [col for col in data.columns
                  if col.startswith('Gender_')
                  or col.startswith('3D_')
                  or col.startswith('XR_')
                  or col.startswith('MetroFrequency_')
                  or col.startswith('LeaderType_')]
    fixed_effect_cols = continuous_vars + dummy_cols

    with pm.Model() as model:
        mu_a = pm.Normal('mu_a', mu=0, sigma=1)
        sigma_a = pm.HalfNormal('sigma_a', 1)

        subject_code = data['SubjectName'].astype('category').cat.codes.values
        subj_intercept = pm.Normal('subj_intercept', mu=mu_a, sigma=sigma_a,
                                   shape=len(data['SubjectName'].unique()))

        beta = {}
        for col in fixed_effect_cols:
            beta[col] = pm.Normal(f'beta_{col}', mu=0, sigma=1)

        mu = subj_intercept[subject_code]
        for col in fixed_effect_cols:
            mu += beta[col] * data[col]

        theta = pm.Deterministic('theta', pm.math.sigmoid(mu))

        y = pm.Bernoulli('y', p=theta, observed=data['DP1_Result'])

        trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.9)

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    var_names = [f'beta_{col}' for col in fixed_effect_cols]
    az.plot_trace(trace, var_names=var_names)
    plt.show()

    summary = az.summary(trace, var_names=var_names, hdi_prob=0.89)
    print("参数后验分布总结：")
    print(summary)

    az.plot_forest(trace, var_names=var_names, combined=True, hdi_prob=0.89)
    plt.title('变量效应大小')
    plt.show()

    pm.plot_posterior(trace, var_names=var_names,
                      textsize=12, hdi_prob=0.89)
    plt.show()
