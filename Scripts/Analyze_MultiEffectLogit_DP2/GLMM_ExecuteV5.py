import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import roc_curve, auc
from pymer4.models import Lmer

current_version = "V5_DP2"

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

# ======================
# ======================

linear_pred = model.predict(
    df,
    use_rfx=True,
    skip_data_checks=True,
    verify_predictions=False
)

linear_pred = np.asarray(linear_pred)

pred_probs = 1 / (1 + np.exp(-linear_pred))

plt.figure(figsize=(10, 8))
fixed_effects = model.coefs.reset_index().rename(columns={'index': 'Variable'})
fixed_effects['CI_lower'] = fixed_effects['Estimate'] - 1.96 * fixed_effects['SE']
fixed_effects['CI_upper'] = fixed_effects['Estimate'] + 1.96 * fixed_effects['SE']
fixed_effects = fixed_effects.sort_values('Estimate')

plt.errorbar(fixed_effects['Estimate'], fixed_effects['Variable'],
             xerr=[fixed_effects['Estimate'] - fixed_effects['CI_lower'],
                   fixed_effects['CI_upper'] - fixed_effects['Estimate']],
             fmt='o', color='black', ecolor='gray', capsize=5)
plt.axvline(0, color='r', linestyle='--')
plt.xlabel('Coefficient Estimate (95% CI)')
plt.title('Fixed Effects with Confidence Intervals')
plt.tight_layout()
plt.savefig(f'Results/fixed_effects_coefficients_{current_version}.png', dpi=300, bbox_inches='tight')
plt.close()

fpr, tpr, _ = roc_curve(df['DP1_Result'], pred_probs)
roc_auc = auc(fpr, tpr)

plt.figure(figsize=(8, 6))
plt.plot(fpr, tpr, color='darkorange', lw=2,
         label=f'ROC Curve (AUC = {roc_auc:.2f})')
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.savefig(f'Results/roc_curve_{current_version}.png', dpi=300, bbox_inches='tight')
plt.close()

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

print(model.summary())
print("\n显著性摘要：")
print(model.coefs[['Estimate', 'SE', 'P-val']].sort_values('P-val'))
