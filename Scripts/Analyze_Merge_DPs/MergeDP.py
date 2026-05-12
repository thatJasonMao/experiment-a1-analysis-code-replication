import os
import csv
import matplotlib.pyplot as plt
import numpy as np

def bayesian_dp1():
    return get_grand_parent_folder() + os.sep + "Analyze_Bayesian_DP1" + os.sep + "Single_Item_Results" + os.sep + "Fixed_Effects_Summary.csv"

def bayesian_dp2():
    return get_grand_parent_folder() + os.sep + "Analyze_Bayesian_DP2" + os.sep + "Single_Item_Results" + os.sep + "Fixed_Effects_Summary.csv"

def bayesian_dp3():
    return get_grand_parent_folder() + os.sep + "Analyze_Bayesian_DP3" + os.sep + "Single_Item_Results" + os.sep + "Fixed_Effects_Summary.csv"

def logit_dp1():
    return get_grand_parent_folder() + os.sep + "Analyze_MultiEffectLogit_DP1" + os.sep + "Results" + os.sep + "fixed_effects_V5_NC.csv"

def logit_dp2():
    return get_grand_parent_folder() + os.sep + "Analyze_MultiEffectLogit_DP2" + os.sep + "Results" + os.sep + "fixed_effects_V5_1_DP2_NC.csv"

def logit_dp3():
    return get_grand_parent_folder() + os.sep + "Analyze_MultiEffectLogit_DP3" + os.sep + "Results" + os.sep + "fixed_effects_V5_DP3_NC.csv"

def get_grand_parent_folder():
    current_script_path = os.path.abspath(__file__)
    current_folder = os.path.dirname(current_script_path)
    parent_folder = os.path.dirname(current_folder)
    return parent_folder

def draw_bayesian():
    dp1_data = []
    dp2_data = []
    dp3_data = []

    with open(bayesian_dp1(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[3]), float(row[4])]
                dp1_data.append((str_key, value))
    for key, value in dp1_data:
        print(f"VarName:{key} Effect: {value}")

    with open(bayesian_dp2(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[3]), float(row[4])]
                dp2_data.append((str_key, value))
    for key, value in dp2_data:
        print(f"VarName:{key} Effect: {value}")

    with open(bayesian_dp3(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[3]), float(row[4])]
                dp3_data.append((str_key, value))
    for key, value in dp3_data:
        print(f"VarName:{key} Effect: {value}")

    all_dps = {
        "DP1": {k: v for k, v in dp1_data},
        "DP2": {k: v for k, v in dp2_data},
        "DP3": {k: v for k, v in dp3_data}
    }

    all_vars = sorted(
        set(list(all_dps["DP1"].keys()) + list(all_dps["DP2"].keys()) + list(all_dps["DP3"].keys())),
        key=lambda x: (modify_var_names(x) == 'Intercept', modify_var_names(x))

    )

    effect_matrix = []
    significance_matrix = []

    for var in all_vars:
        row = []
        sig_row = []
        for dp in ["DP1", "DP2", "DP3"]:
            ci = all_dps[dp].get(var, [0, 0])
            mean_effect = (ci[0] + ci[1]) / 2
            is_significant = (ci[0] * ci[1]) > 0

            row.append(mean_effect)
            sig_row.append(is_significant)
        effect_matrix.append(row)
        significance_matrix.append(sig_row)

    plt.figure(figsize=(24, 15))
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.size'] = 22

    background = np.ones_like(effect_matrix) * 0.8
    plt.imshow(background, cmap='Greys', aspect='auto',
               extent=[-0.5, len(all_dps) - 0.5, -0.5, len(all_vars) - 0.5])

    max_effect = np.max(effect_matrix)
    min_effect = np.min(effect_matrix)

    masked_effects = np.ma.masked_where(~np.array(significance_matrix), effect_matrix)
    heatmap = plt.imshow(masked_effects, cmap='coolwarm', aspect='auto',
                         vmin=min_effect, vmax=max_effect)

    cbar = plt.colorbar(heatmap)
    cbar.set_label('Effect Size', rotation=270, labelpad=20)

    plt.xticks(np.arange(len(all_dps)), ["Decision Point 1", "Decision Point 2", "Decision Point 3"], rotation=0)
    plt.yticks(np.arange(len(all_vars)), [modify_var_names(var) for var in all_vars])

    plt.title("Fixed Effects Summary (Bayesian Causal Inference)",
             fontsize=26, pad=20)

    for i in range(len(all_vars)):
        for j in range(len(all_dps)):
            ci = all_dps[["DP1", "DP2", "DP3"][j]].get(all_vars[i], [0, 0])
            text = f"({ci[0]:.4f}, {ci[1]:.4f})"
            plt.text(j, i, text,
                     ha='center',
                     va='center',
                     color='black',
                     fontsize=20,
                     bbox=dict(
                         facecolor='white',
                         edgecolor='black',
                         boxstyle='round,pad=0.2',
                         alpha=0.8
                     ))

    plt.tight_layout()
    plt.savefig("bayesian_effects_heatmap.png", dpi=600)

    plt.close()

def draw_logit():
    dp1_data = []
    dp2_data = []
    dp3_data = []

    with open(logit_dp1(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[14]), float(row[15])]
                dp1_data.append((str_key, value))
    for key, value in dp1_data:
        print(f"VarName:{key} Effect: {value}")

    with open(logit_dp2(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[14]), float(row[15])]
                dp2_data.append((str_key, value))
    for key, value in dp2_data:
        print(f"VarName:{key} Effect: {value}")

    with open(logit_dp3(), 'r', newline='', encoding='utf-8', errors='ignore') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            if len(row) > 1:
                str_key = row[0]
                value = [float(row[14]), float(row[15])]
                dp3_data.append((str_key, value))
    for key, value in dp3_data:
        print(f"VarName:{key} Effect: {value}")

    all_dps = {
        "DP1": {k: v for k, v in dp1_data},
        "DP2": {k: v for k, v in dp2_data},
        "DP3": {k: v for k, v in dp3_data}
    }

    all_vars = sorted(
        set(list(all_dps["DP1"].keys()) + list(all_dps["DP2"].keys()) + list(all_dps["DP3"].keys())),
        key=lambda x: (
            modify_var_names(x.replace("ThreeD", "3D")) == 'Intercept',

            modify_var_names(x.replace("ThreeD", "3D"))

        )
    )

    effect_matrix = []
    significance_matrix = []

    for var in all_vars:
        row = []
        sig_row = []
        for dp in ["DP1", "DP2", "DP3"]:
            ci = all_dps[dp].get(var, [0, 0])
            mean_effect = (ci[0] + ci[1]) / 2
            is_significant = (ci[0] * ci[1]) > 0

            row.append(mean_effect)
            sig_row.append(is_significant)
        effect_matrix.append(row)
        significance_matrix.append(sig_row)

    plt.figure(figsize=(24, 15))
    plt.rcParams['font.sans-serif'] = ['Arial']
    plt.rcParams['font.size'] = 22

    background = np.ones_like(effect_matrix) * 0.8

    plt.imshow(background, cmap='Greys', aspect='auto',
               extent=[-0.5, len(all_dps) - 0.5, -0.5, len(all_vars) - 0.5])

    max_effect = np.max(effect_matrix)
    min_effect = np.min(effect_matrix)

    masked_effects = np.ma.masked_where(~np.array(significance_matrix), effect_matrix)
    heatmap = plt.imshow(masked_effects, cmap='coolwarm', aspect='auto',
                    vmin=min_effect, vmax=max_effect)

    cbar = plt.colorbar(heatmap)
    cbar.set_label('Effect Size', rotation=270, labelpad=20)

    plt.xticks(np.arange(len(all_dps)), ["Decision Point 1", "Decision Point 2", "Decision Point 3"], rotation=0)
    plt.yticks(np.arange(len(all_vars)), [modify_var_names(var) for var in all_vars])

    plt.title("Fixed Effects Summary (Mixed-Effects Logistic Regression)",
             fontsize=26, pad=20)

    for i in range(len(all_vars)):
        for j in range(len(all_dps)):
            ci = all_dps[["DP1", "DP2", "DP3"][j]].get(all_vars[i], [0, 0])
            text = f"({ci[0]:.4f}, {ci[1]:.4f})"
            plt.text(j, i, text,
                     ha='center',
                     va='center',
                     color='black',

                     fontsize=20,
                     bbox=dict(

                         facecolor='white',
                         edgecolor='black',
                         boxstyle='round,pad=0.2',

                         alpha=0.8
                     ))

    plt.tight_layout()
    plt.savefig("logit_effects_heatmap.png", dpi=600)
    plt.close()

def modify_var_names(raw_name):
    new_name = raw_name

    if "beta_" in raw_name:
        new_name = raw_name.replace("beta_", "")
    if "_scaled" in raw_name:
        new_name = raw_name.replace("_scaled", "")
    if "(Intercept)" in raw_name:
        new_name = raw_name.replace("(Intercept)", "Intercept")
    if "C(" in raw_name:
        new_name = raw_name.replace("C(", "")
        new_name = new_name.replace(")", "_")
    if "ThreeD" in raw_name:
        new_name = raw_name.replace("C(ThreeD)", "3D_")
    if "FollowRate" in raw_name:
        new_name = new_name.replace("FollowRate", "FollowProportion")
    if "Level" in raw_name:
        new_name = new_name.replace("Level", "ScenarioSequence")
    if "Familiarity" in raw_name:
        new_name = new_name.replace("Familiarity", "Familiarity*")
    if "FollowTendency" in raw_name:
        new_name = new_name.replace("FollowTendency", "FollowTendency*")
    if "SelfDecideTendency" in raw_name:
        new_name = new_name.replace("SelfDecideTendency", "SelfDecideTendency*")
    
    return new_name

if __name__ == "__main__":
    draw_bayesian()
    draw_logit()
