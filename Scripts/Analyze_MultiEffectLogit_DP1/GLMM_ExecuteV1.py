import pandas as pd
from sklearn.preprocessing import StandardScaler
from pymer4.models import Lmer

df = pd.read_excel("Final_Data_Chain.xlsx", sheet_name="Data_Chain_Trim")

df = df.rename(columns={'3D': 'ThreeD'})

scaler = StandardScaler()
cont_vars = ['Age', 'GSE', 'ITS']
df[['Age_scaled', 'GSE_scaled', 'ITS_scaled']] = scaler.fit_transform(df[cont_vars])

df['FollowRate'] = df['FollowRate'].astype('category')

discrete_vars = ['Gender', 'Familiarity', 'FollowTendency', 'SelfDecideTendency',
                 'ThreeD', 'XR', 'MetroFrequency', 'LeaderType']
for col in discrete_vars:
    df[col] = df[col].astype('category')

formula = """
DP1_Result ~ 
Age_scaled + 
GSE_scaled + 
ITS_scaled + 
C(Gender) + 
C(Familiarity) + 
C(FollowTendency) + 
C(SelfDecideTendency) + 
C(ThreeD) + 
C(XR) + 
C(MetroFrequency) + 
C(FollowRate) + 
C(LeaderType) + 
(1|SubjectName)
"""

model = Lmer(formula, data=df, family='binomial')
model.fit(summarize=False)

print(model.summary())

print("\n显著性摘要：")
print(model.coefs[['Estimate', 'SE', 'P-val']].sort_values('P-val'))
