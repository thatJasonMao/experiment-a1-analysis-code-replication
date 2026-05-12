import pandas as pd
from sklearn.preprocessing import StandardScaler
from pymer4.models import Lmer
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_excel("Final_Data_Chain.xlsx", sheet_name="Data_Chain_Trim")

df = df.rename(columns={'3D': 'ThreeD'})

scaler = StandardScaler()
cont_vars = ['Familiarity', 'FollowTendency', 'SelfDecideTendency', 'FollowRate']
df[[col + '_scaled' for col in cont_vars]] = scaler.fit_transform(df[cont_vars])

categorical_vars = ['Gender', 'LeaderType', 'MetroFrequency']
for col in categorical_vars:
    df[col] = df[col].astype('category')

formula = """
DP1_Result ~ 
""" + " + ".join([col + '_scaled' for col in cont_vars]) + " + " + \
          " + ".join(['C(' + col + ')' for col in categorical_vars]) + " + (1|SubjectName)"

model = Lmer(formula, data=df, family='binomial')
model.fit(summarize=False)

print(model.summary())

print("\n显著性摘要：")
print(model.coefs[['Estimate', 'SE', 'P-val']].sort_values('P-val'))

model.coefs['lower'] = model.coefs['Estimate'] - 1.96 * model.coefs['SE']
model.coefs['upper'] = model.coefs['Estimate'] + 1.96 * model.coefs['SE']

model.coefs['OR'] = np.exp(model.coefs['Estimate'])
model.coefs['OR_lower'] = np.exp(model.coefs['lower'])
model.coefs['OR_upper'] = np.exp(model.coefs['upper'])

plt.figure(figsize=(10, 6))
sns.pointplot(x='OR', y='index', data=model.coefs.reset_index(), join=False, color='blue')
plt.hlines(y=model.coefs.reset_index()['index'], xmin=model.coefs['OR_lower'], xmax=model.coefs['OR_upper'], color='blue')
plt.axvline(1, linestyle='--', color='red')
plt.xscale('log')

plt.xlabel('Odds Ratio (log scale)')
plt.ylabel('Predictors')
plt.title('Forest Plot of Odds Ratios')
plt.show()
