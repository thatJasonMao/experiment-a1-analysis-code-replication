import os.path
import pandas as pd
import numpy as np
import pymc as pm
import arviz as az
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc, precision_recall_curve, confusion_matrix, ConfusionMatrixDisplay
from sklearn.calibration import calibration_curve

sub_folder = "Single_Item_Results"

if __name__ == "__main__":

    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)

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

        with model:
            post_pred = pm.sample_posterior_predictive(trace, var_names=['y'])

        y_prob = post_pred.posterior_predictive['y'].mean(axis=(0, 1))

        y_true = data['DP1_Result'].values

        fpr, tpr, _ = roc_curve(y_true, y_prob)
        roc_auc = auc(fpr, tpr)

        plt.rcParams['font.sans-serif'] = ['Arial']
        plt.rcParams['font.size'] = 55

        plt.figure(figsize=(12, 12))
        plt.plot([0, 1], [0, 1], color='navy', lw=6, linestyle='--')
        plt.plot(fpr, tpr, color='darkorange', lw=6, label=f'AUC = {roc_auc:.3f}')
        # plt.xlabel('False Positive Rate', fontsize=50)
        # plt.ylabel('True Positive Rate', fontsize=50)
        plt.title('Bayesian ROC', fontsize=75)
        plt.legend(loc="lower right", fontsize=60)
        plt.tick_params(axis='both', labelsize=75)
        plt.savefig(f'{sub_folder}/NC_ROC_Curve.png', dpi=600, bbox_inches='tight', transparent=True)
        plt.close()

        precision, recall, _ = precision_recall_curve(y_true, y_prob)
        pr_auc = auc(recall, precision)

        plt.figure(figsize=(8, 6))
        plt.plot(recall, precision, color='blue', lw=2,
                label=f'PR曲线 (AUC = {pr_auc:.2f})')

        plt.xlabel('召回率', fontsize=12)
        plt.ylabel('精确率', fontsize=12)
        plt.title('精确率-召回率曲线', fontsize=14)
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.legend(loc='upper right')

        plt.savefig(f'{sub_folder}/PR_Curve.png', dpi=300, bbox_inches='tight')
        plt.close()

        prob_true, prob_pred = calibration_curve(y_true, y_prob, n_bins=10)

        plt.figure(figsize=(8, 6))
        plt.plot(prob_pred, prob_true, 's-', label='模型')
        plt.plot([0, 1], [0, 1], '--', color='gray', label='理想校准')
        plt.xlabel('预测概率', fontsize=12)
        plt.ylabel('实际比例', fontsize=12)
        plt.title('校准曲线', fontsize=14)
        plt.legend()
        plt.savefig(f'{sub_folder}/Calibration_Curve.png', dpi=300, bbox_inches='tight')
        plt.close()

    var_names = [f'beta_{col}' for col in fixed_effect_cols]
    az.plot_trace(trace, var_names=var_names)
    # plt.show()
    plt.savefig(f'{sub_folder}/Trace_Plot.png')

    summary = az.summary(trace, var_names=var_names, hdi_prob=0.89)
    print("参数后验分布总结：")
    print(summary)

    summary.to_csv(f'{sub_folder}/Fixed_Effects_Summary.csv',
                  index=True,
                  float_format='%.4f',
                  encoding='utf-8-sig')

    plt.figure(figsize=(20, 6.5))
    plt.rcParams['font.family'] = 'Arial'
    plt.rcParams['font.size'] = 20

    summary_df = az.summary(trace, var_names=var_names, hdi_prob=0.89)

    fixed_effects = summary_df.reset_index()[['index', 'mean', 'sd', 'hdi_5.5%', 'hdi_94.5%']]
    fixed_effects.columns = ['Variable', 'Estimate', 'SE', 'CI_lower', 'CI_upper']

    fixed_effects = fixed_effects.sort_values('Estimate')

    norm = plt.Normalize(vmin=fixed_effects['Estimate'].min(), vmax=fixed_effects['Estimate'].max())
    colors = plt.cm.plasma(norm(fixed_effects['Estimate']))

    plt.axvline(0, color='silver', linestyle='--', linewidth=2.5)

    for i, row in fixed_effects.iterrows():
        plt.hlines(y=row['Variable'],
                   xmin=row['CI_lower'],
                   xmax=row['CI_upper'],
                   colors='gray',
                   alpha=0.6,
                   linewidth=2.5)

    plt.scatter(fixed_effects['Estimate'], fixed_effects['Variable'],
                c=colors,
                s=150,
                edgecolor='black',
                linewidth=1.5,
                zorder=3)

    sm = plt.cm.ScalarMappable(cmap='plasma', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=plt.gca(), aspect=40, pad=0.03)
    cbar.set_label('Effect Size', rotation=270, labelpad=25)

    sig_color = 'crimson'
    nonsig_color = 'slategrey'
    for i, row in fixed_effects.iterrows():
        ecolor = sig_color if (row['CI_lower'] > 0) or (row['CI_upper'] < 0) else nonsig_color
        plt.errorbar(row['Estimate'], row['Variable'],
                     xerr=[[row['Estimate'] - row['CI_lower']], [row['CI_upper'] - row['Estimate']]],
                     fmt='o', color='black', ecolor=ecolor, capsize=5,
                     elinewidth=2.5, mew=2.5, markersize=5)

    plt.xlabel('Coefficient Estimate (89% CI)')

    plt.xlim(-3, 3)

    for spine in plt.gca().spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('black')
        spine.set_linewidth(0.8)

    plt.tight_layout()
    plt.savefig(f'{sub_folder}/Effect_Plot_Modified.png',
                dpi=600,
                bbox_inches='tight',
                facecolor='white')
    plt.close()

    for var in var_names:
        plt.figure()
        pm.plot_posterior(trace, var_names=[var],

                         textsize=12, hdi_prob=0.89)
        plt.savefig(f'{sub_folder}/{var}_Posterior.png',

                   dpi=300,
                   bbox_inches='tight')
        plt.close()

    var_names = [f'beta_{col}' for col in fixed_effect_cols]
    plt.figure(figsize=(8, 12))

    axes = az.plot_trace(trace,
                         var_names=var_names,
                         compact=False,
                         )

    for ax_row in axes:
        trace_ax = ax_row[1]
        trace_ax.set_xlim(0, 2000)
        trace_ax.set_xticks([0, 500, 1000, 1500, 2000])

    plt.tight_layout()
    plt.savefig(f'{sub_folder}/Trace_Plot.png', dpi=300)
