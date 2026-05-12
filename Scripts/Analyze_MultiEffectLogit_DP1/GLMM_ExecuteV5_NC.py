import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc
from pymer4.models import Lmer

current_version = "V5_NC"

df = pd.read_excel("Final_Data_Chain.xlsx", sheet_name="Data_Chain_Trim")

df = df.rename(columns={'3D': 'ThreeD'})

scaler = StandardScaler()
cont_vars = ['GSE', 'ITS', 'Age', 'Familiarity', 'FollowTendency', 'SelfDecideTendency', 'FollowRate', 'Level']
df[[col + '_scaled' for col in cont_vars]] = scaler.fit_transform(df[cont_vars])

categorical_vars = ['Gender', 'ThreeD', 'XR', 'LeaderType', 'MetroFrequency']
for col in categorical_vars:
    df[col] = df[col].astype('category')

formula = """
DP1_Result ~ 
""" + " + ".join([col + '_scaled' for col in cont_vars]) + " + " + \
          " + ".join(['C(' + col + ')' for col in categorical_vars]) + " + (1|SubjectName)"

model = Lmer(formula, data=df, family='binomial')
model.fit(summarize=False)

fixed_effects = model.coefs.reset_index().rename(columns={'index': 'Variable'})
fixed_effects['CI_lower'] = fixed_effects['Estimate'] - 1.645 * fixed_effects['SE']
fixed_effects['CI_upper'] = fixed_effects['Estimate'] + 1.645 * fixed_effects['SE']

fixed_effects = fixed_effects[fixed_effects['SE'] <= 10]
fixed_effects = fixed_effects.sort_values('Estimate')

fixed_effects.to_csv(f'Results/fixed_effects_{current_version}.csv',
                    index=False,
                    encoding='utf-8-sig')

linear_pred = model.predict(
    df,
    use_rfx=True,
    skip_data_checks=True,
    verify_predictions=False
)

linear_pred = np.asarray(linear_pred)

pred_probs = 1 / (1 + np.exp(-linear_pred))

plt.figure(figsize=(20, 6.5))
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 20

norm = plt.Normalize(vmin=fixed_effects['Estimate'].min(), vmax=fixed_effects['Estimate'].max())
colors = plt.cm.plasma(norm(fixed_effects['Estimate']))

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

plt.axvline(0, color='silver', linestyle='--', linewidth=2.5)

sig_color = 'crimson'
nonsig_color = 'slategrey'

for i, row in fixed_effects.iterrows():
    ecolor = sig_color if row.get('P-val', 1) < 0.1 else nonsig_color
    plt.errorbar(
        row['Estimate'], row['Variable'],
        xerr=[[row['Estimate'] - row['CI_lower']], [row['CI_upper'] - row['Estimate']]],
        fmt='o', color='black', ecolor=ecolor, capsize=5,
        elinewidth=2.5, mew=2.5, markersize=5
    )

plt.xlabel('Coefficient Estimate (90% CI)')
plt.xlim(-12, 8)

plt.tight_layout()
plt.savefig(f'Results/fixed_effects_coefficients_{current_version}.png', dpi=600, bbox_inches='tight')
plt.close()

fpr, tpr, _ = roc_curve(df['DP1_Result'], pred_probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(12, 12))
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['font.size'] = 55

plt.plot([0, 1], [0, 1], color='navy', lw=6, linestyle='--')
plt.plot(fpr, tpr, color='darkorange', lw=6, label=f'(AUC = {roc_auc:.3f}')
plt.title('Logistic ROC', fontsize=75)

plt.legend(loc="lower right", fontsize=60)

plt.tick_params(axis='both', labelsize=75)

plt.savefig(f'Results/NC_roc_curve_{current_version}.png', dpi=600, bbox_inches='tight', transparent=True)
plt.close()

plt.rcParams['font.size'] = 20
plt.figure(figsize=(10, 6))
for outcome in [0, 1]:
    plt.hist(pred_probs[df['DP1_Result'] == outcome],
             bins=30, alpha=0.5,
             label=f'Actual Outcome = {outcome}')
plt.xlabel('Predicted Probability')
plt.ylabel('Frequency')
plt.title('Predicted Probability Distribution by Actual Outcome')
plt.legend()
plt.savefig(f'Results/predicted_prob_distribution_{current_version}.png', dpi=300, bbox_inches='tight')
plt.close()

residuals = df['DP1_Result'] - pred_probs
plt.figure(figsize=(10, 6))
plt.scatter(pred_probs, residuals, alpha=0.5)
plt.axhline(0, color='r', linestyle='--')
plt.xlabel('Predicted Probability')
plt.ylabel('Residuals')
plt.title('Residuals vs. Predicted Values')
plt.savefig(f'Results/residuals_plot_{current_version}.png', dpi=300, bbox_inches='tight')
plt.close()

try:
    re_var = model.ranef_var
    plt.figure(figsize=(8, 4))
    re_var.plot(kind='barh')
    plt.xlabel('Variance')
    plt.title('Random Effects Variance Components')
    plt.savefig(f'Results/random_effects_variance_{current_version}.png', dpi=300, bbox_inches='tight')
    plt.close()
except AttributeError:
    print("Warning: Could not extract random effects variance automatically")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

pd.set_option('display.expand_frame_repr', False)

print(model.summary())
print("\n显著性摘要：")
print(model.coefs[['Estimate', 'SE', 'P-val']].sort_values('P-val'))
