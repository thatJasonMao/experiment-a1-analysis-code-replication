import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

if __name__ == "__main__":
    data = pd.read_csv("Data_Chain_Trim.csv")

    data['DP1_Result'] = data['DP1_Result'].map({'Yes': 1, 'No': 0})
    data['Gender'] = data['Gender'].astype('category').cat.codes
    data['3D'] = data['3D'].map({'Yes': 1, 'No': 0})
    data['XR'] = data['XR'].map({'Yes': 1, 'No': 0})
    data['MetroFrequency'] = data['MetroFrequency'].astype('category').cat.codes

    leader_dummies = pd.get_dummies(data['LeaderType'], prefix='Leader', drop_first=True)
    data = pd.concat([data, leader_dummies], axis=1)

    scene_order = {'B1': 1, 'B2': 2, 'B3': 3, 'B4': 4, 'B5': 5}
    data['Level'] = data['Level'].map(scene_order)

    continuous_vars = ['GSE', 'ITS', 'Age', 'FollowRate',
                       'Familiarity', 'FollowTendency', 'SelfDecideTendency']
    scaler = StandardScaler()
    data[continuous_vars] = scaler.fit_transform(data[continuous_vars])

    with pm.Model() as model:
        mu_a = pm.Normal('mu_a', mu=0, sigma=1)
        sigma_a = pm.HalfNormal('sigma_a', 1)

        subj_intercept = pm.Normal('subj_intercept', mu=mu_a, sigma=sigma_a,
                                   shape=len(data['SubjectName'].unique()))

        beta_GSE = pm.Normal('beta_GSE', mu=0, sigma=1)
        beta_ITS = pm.Normal('beta_ITS', mu=0, sigma=1)
        beta_Age = pm.Normal('beta_Age', mu=0, sigma=1)
        beta_FollowRate = pm.Normal('beta_FollowRate', mu=0, sigma=1)
        beta_Familiarity = pm.Normal('beta_Familiarity', mu=0, sigma=1)
        beta_FollowTendency = pm.Normal('beta_FollowTendency', mu=0, sigma=1)
        beta_SelfDecideTendency = pm.Normal('beta_SelfDecideTendency', mu=0, sigma=1)

        beta_Gender = pm.Normal('beta_Gender', mu=0, sigma=1)
        beta_3D = pm.Normal('beta_3D', mu=0, sigma=1)
        beta_XR = pm.Normal('beta_XR', mu=0, sigma=1)
        beta_MetroFrequency = pm.Normal('beta_MetroFrequency', mu=0, sigma=1)

        beta_Leader1 = pm.Normal('beta_Leader1', mu=0, sigma=1)

        beta_Leader2 = pm.Normal('beta_Leader2', mu=0, sigma=1)

        beta_level = pm.Normal('beta_level', mu=0, sigma=1)

        mu = (
                subj_intercept[data['SubjectName'].astype('category').cat.codes.values] +
                beta_GSE * data['GSE'] +
                beta_ITS * data['ITS'] +
                beta_Age * data['Age'] +
                beta_FollowRate * data['FollowRate'] +
                beta_Familiarity * data['Familiarity'] +
                beta_FollowTendency * data['FollowTendency'] +
                beta_SelfDecideTendency * data['SelfDecideTendency'] +
                beta_Gender * data['Gender'] +
                beta_3D * data['3D'] +
                beta_XR * data['XR'] +
                beta_MetroFrequency * data['MetroFrequency'] +
                beta_Leader1 * data['Leader_Robot'] +

                beta_Leader2 * data['Leader_Security'] +
                beta_level * data['Level']
        )

        theta = pm.Deterministic('theta', pm.math.sigmoid(mu))

        y = pm.Bernoulli('y', p=theta, observed=data['DP1_Result'])

        trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.9)

    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']

    var_names = ['beta_GSE', 'beta_ITS', 'beta_Age', 'beta_FollowRate',
                 'beta_Familiarity', 'beta_FollowTendency', 'beta_SelfDecideTendency',
                 'beta_Gender', 'beta_3D', 'beta_XR', 'beta_MetroFrequency',
                 'beta_Leader1', 'beta_Leader2', 'beta_level']
    az.plot_trace(trace, var_names=var_names)
    plt.show()

    summary = az.summary(trace, var_names=var_names, hdi_prob=0.89)
    print("参数后验分布总结：")
    print(summary)

    continuous_var_names = ['beta_GSE', 'beta_ITS', 'beta_Age', 'beta_FollowRate',
                            'beta_Familiarity', 'beta_FollowTendency', 'beta_SelfDecideTendency',
                            'beta_Leader1', 'beta_Leader2']
    az.plot_forest(trace, var_names=continuous_var_names, combined=True, hdi_prob=0.89)
    plt.title('连续变量及引导者类型效应大小')
    plt.show()

    var_names_for_posterior = var_names[:-1]

    pm.plot_posterior(trace, var_names=var_names_for_posterior,
                      textsize=12, hdi_prob=0.89)
    plt.show()
