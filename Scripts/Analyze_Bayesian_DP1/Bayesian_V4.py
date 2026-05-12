import pandas as pd
import pymc as pm
import itertools
import time
from sklearn.preprocessing import StandardScaler
import arviz as az
import matplotlib.pyplot as plt

if __name__ == "__main__":
    data = pd.read_csv("Data_Chain_Trim.csv")

    data['DP1_Result'] = data['DP1_Result'].map({'Yes': 1, 'No': 0})

    categorical_cols = ['Gender', '3D', 'XR', 'MetroFrequency', 'LeaderType']
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)

    continuous_vars = ['GSE', 'ITS', 'Age', 'FollowRate',
                       'Familiarity', 'FollowTendency', 'SelfDecideTendency']
    scaler = StandardScaler()
    data[continuous_vars] = scaler.fit_transform(data[continuous_vars])

    dummy_cols = [col for col in data.columns
                  if col.startswith('Gender_')
                  or col.startswith('3D_')
                  or col.startswith('XR_')
                  or col.startswith('MetroFrequency_')
                  or col.startswith('LeaderType_')]
    fixed_effect_cols = continuous_vars + dummy_cols

    all_pairs = list(itertools.combinations(fixed_effect_cols, 2))
    print(f"要计算的自变量组合数量{len(all_pairs)}")

    for var1, var2 in all_pairs:
        print(f"Processing interaction: {var1} * {var2}")
        start_time = time.time()
        interaction_term = f"{var1}_x_{var2}"

        with pm.Model() as interaction_model:
            mu_a = pm.Normal('mu_a', mu=0, sigma=1)
            sigma_a = pm.HalfNormal('sigma_a', 1)

            subject_code = data['SubjectName'].astype('category').cat.codes.values
            n_subjects = len(data['SubjectName'].unique())
            subj_intercept = pm.Normal('subj_intercept', mu=mu_a, sigma=sigma_a,
                                       shape=n_subjects)

            beta = {col: pm.Normal(f'beta_{col}', mu=0, sigma=1)
                    for col in fixed_effect_cols}

            beta_interaction = pm.Normal(f'beta_{interaction_term}', mu=0, sigma=1)

            mu = subj_intercept[subject_code]
            for col in fixed_effect_cols:
                mu += beta[col] * data[col]
            mu += beta_interaction * (data[var1] * data[var2])

            theta = pm.Deterministic('theta', pm.math.sigmoid(mu))

            y = pm.Bernoulli('y', p=theta, observed=data['DP1_Result'])

            trace = pm.sample(2000, tune=1000, chains=4, target_accept=0.9)

        elapsed_time = time.time() - start_time

        filename = f"Results/interaction_{interaction_term}.txt"
        with open(filename, 'w') as f:
            f.write(f"Interaction Term: {interaction_term}\n\n")

            with pd.option_context('display.max_columns', None,
                                   'display.max_colwidth', 20,
                                   'display.width', 1000):
                interaction_summary = pm.summary(trace, var_names=[f'beta_{interaction_term}'])
                f.write("Interaction Coefficient Summary:\n")
                f.write(interaction_summary.to_string())
                f.write("\n\n")

                f.write("Main Effect Coefficients Summary:\n")
                main_effect_summary = pm.summary(trace, var_names=[f'beta_{var1}', f'beta_{var2}'])
                f.write(main_effect_summary.to_string())
                f.write("\n\n")

                f.write("Full Model Summary:\n")
                f.write(pm.summary(trace).to_string())
                f.write(f"\n\nTime elapsed: {elapsed_time:.2f} seconds")

        plt.figure()
        az.plot_posterior(trace, var_names=[f'beta_{interaction_term}', f'beta_{var1}', f'beta_{var2}'])
        plt.savefig(f"Results/posterior_{interaction_term}.png")
        plt.close()

        plt.figure()
        theta_samples = trace.posterior['theta'].values

        mean_pred = theta_samples.mean(axis=(0, 1))

        plt.scatter(data[var1], data[var2], c=mean_pred, cmap='viridis', alpha=0.6)
        plt.colorbar(label='Predicted Probability')
        plt.xlabel(var1)
        plt.ylabel(var2)
        plt.title(f'Predicted Probability of {interaction_term}')
        plt.savefig(f"Results/prediction_{interaction_term}.png")
        plt.close()

        del interaction_model
        del trace
