# VR Evacuation Experiment Data Analysis System — Framework Documentation

## 1. Overview

This repository contains the data analysis codebase for a virtual reality evacuation experiment, centered on the core research question of how leader presence influences evacuation decision-making and behavior. It provides systematic extraction, cleaning, statistical modeling, and visualization of eye-tracking, movement trajectory, and questionnaire data collected from multiple participants across multiple levels and experimental groups.

Experiments were conducted at three sites — Changchun, Shenzhen, and Chengdu. Participants were assigned to one of three groups based on leader type: Passenger, Robot, and Security, covering 7 levels from A1 through B5.

**Data and Privacy Notice**:
- This repository contains analysis code only. No experimental raw data or intermediate result data is included.
- All privacy-sensitive data (specifically, participant names) has been anonymized via MD5 hashing. No personally identifiable information is present in this repository.

The analysis pipeline consists of the following core modules:

- **Data Aggregation & Cleaning**: Time-align multi-source per-level data (Log, EyeGaze, NPC, Subject) into unified GroupData files, and build a global participant index.
- **Metric Extraction**: Extract kinematic metrics (speed, acceleration, travel distance, evacuation time), eye-tracking metrics (gaze target classification, gaze point coordinates, gaze path distance & velocity, Lyapunov exponents), and following-behavior metrics (follow ratio, follow relationship).
- **Questionnaire Scoring**: Score and aggregate standardized psychological scales including GSE (General Self-Efficacy), ITS (Interpersonal Trust Scale), SSQ (Simulator Sickness Questionnaire), and PANAS (Positive and Negative Affect Schedule).
- **Statistical Testing**: Covers 10 methods — Shapiro-Wilk, Kolmogorov-Smirnov, independent/paired t-test, Mann-Whitney U, Wilcoxon signed-rank, one-way/repeated-measures ANOVA, Kruskal-Wallis, and Friedman tests.
- **Advanced Modeling**: Bayesian hierarchical logistic regression via PyMC (V1 through V8 iterations), and mixed-effects logit models via pymer4 (R lme4 interface, V1 through V5 iterations), for analyzing factors influencing following behavior at decision points.
- **Eye-Gaze Pattern Analysis**: DBSCAN clustering of gaze points (2D/3D), subdivided by scene (Hall, Platform, Aisle) and gaze target (All, Environment, Leader, NPC), generating KDE heatmaps and topology maps.
- **Between-Group / Within-Group Comparison & Visualization**: Box plots, violin plots, Spearman correlation heatmaps, DTW trajectory similarity analysis, polar gaze heatmaps, pie charts, and more.

---

## 2. Quick Start

### 2.1 Environment Requirements

- Python 3.9 or later
- R 4.0 or later (required by pymer4 for mixed-effects modeling)

### 2.2 Installing Dependencies

This project does not include a `requirements.txt` file. Install the necessary dependencies based on the scripts you intend to run. Core dependencies:

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
pip install pymc arviz fastdtw openpyxl tqdm psutil
pip install pymer4
```

### 2.3 Data Preparation

This repository does not contain experimental data. To reproduce the analysis pipeline, organize your data according to the following directory structure:

- `受试者采集数据_长春/`: Changchun site participant data (one subdirectory per participant)
- `受试者采集数据_深圳/`: Shenzhen site participant data (one subdirectory per participant)
- `受试者采集数据_成都/`: Chengdu site participant data (one subdirectory per participant)
- `问卷数据/`: Raw questionnaire Excel files

### 2.4 Analysis Pipeline

Execute scripts in the following order:

1. `Build_Global_Reference.py`: Build the global participant index
2. `GroupData.py`: Aggregate multi-source data per participant per level
3. Questionnaire scoring scripts (`GSE_Calculation.py`, `ITS_Calculation.py`, etc.)
4. Metric extraction scripts (`ExtractAvgSpeed.py`, `Extract_Full_Gaze_Info_*.py`, etc.)
5. Statistical testing scripts (subdirectories under `Analyze_Statistics/`)
6. Advanced modeling scripts (`Analyze_Bayesian_DP*/`, `Analyze_MultiEffectLogit_DP*/`)
7. Visualization scripts (`DrawFig/`, `DrawGaze*/`, `Compare*/`, etc.)

---

## 3. Core Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| pandas | - | DataFrame operations and CSV I/O |
| numpy | - | Numerical computing and array operations |
| matplotlib | - | Base plotting library |
| seaborn | - | Statistical plots (box plots, violin plots, heatmaps) |
| scipy | - | Statistical tests (Shapiro-Wilk, K-S, t-test, etc.) |
| scikit-learn | - | Data standardization, DBSCAN clustering, model evaluation metrics |
| pymc | - | Bayesian hierarchical logistic regression modeling |
| arviz | - | Bayesian model posterior analysis and visualization |
| pymer4 | - | Mixed-effects logistic regression (Python interface for R lme4) |
| fastdtw | - | Dynamic Time Warping computation (trajectory similarity) |
| openpyxl | - | Excel file I/O |
| tqdm | - | Progress bar display |
| psutil | - | System resource monitoring |

---

## 4. Development Milestones

| Stage | Milestone | Key Deliverables |
|-------|-----------|-----------------|
| **M1** | Data Aggregation & Global Index | Multi-source data time-aligned into GroupData files; `Subject_Data_Global_Reference.xlsx` global participant index built |
| **M2** | Questionnaire Scoring & Preprocessing | Standardized scoring for GSE / ITS / SSQ / PANAS; time-window splitting by decision points (DP1/DP2/DP3) |
| **M3** | Kinematic & Eye-Tracking Metrics | Speed, acceleration, travel distance, evacuation time, gaze target classification, Lyapunov exponents, gaze path distance/velocity, follow ratios |
| **M4** | Statistical Testing | Normality tests (Shapiro-Wilk, K-S); parametric/non-parametric between-group comparisons (t-test, Mann-Whitney, ANOVA, Kruskal-Wallis, Friedman) |
| **M5** | Bayesian Hierarchical Logistic Regression | PyMC modeling (V1→V8) with fixed/random effects, ROC/PR calibration curves; independent modeling per decision point |
| **M6** | Mixed-Effects Logit Models | pymer4 / R-lme4 GLMM (V1→V5) for frequentist cross-validation; independent modeling per decision point |
| **M7** | Eye-Gaze Pattern Clustering | DBSCAN 2D/3D clustering × 4 scenes × 4 gaze targets; KDE heatmaps, topology maps, polar visualization |
| **M8** | Between/Within-Group Comparisons | Box/violin plots, Spearman correlation heatmaps, DTW trajectory similarity, follow-ratio comparison across decision points |
| **M9** | Final Figures & Publication Graphics | Questionnaire distributions, polar gaze heatmaps, trajectory plots, pie charts, posterior forest plots — all ≥300 DPI publication-ready output |

---

## 5. Module & Script Details

### 5.1 Data Aggregation Module

#### GroupData.py

- **Purpose**: Align multi-source CSV data (Log_Info, EyeGaze_Simulation_Info, NPC_Simulation_Info, Subject_Simulation_Info) by timestamp for each participant and level, and merge into a unified GroupData CSV file.
- **Core Logic**:
  - Scan 7 level folders (A1 through B5) under each participant directory; each folder contains 4 types of source CSV files.
  - Determine the valid time window using the "Unfreeze Subject Agent Move" and "Subject Agent Has Arrive" events from Log_Info.
  - Align and merge multi-source data at uniform time sampling points. Output one file per participant, named `<ParticipantName>_<Level>.csv`.
- **Dependencies**: `openpyxl`, `tqdm`

#### Build_Global_Reference.py

- **Purpose**: Scan participant data directories at Changchun, Shenzhen, and Chengdu sites, build a mapping from participant nicknames to data folder paths, and export it as a global index table.
- **Core Logic**:
  - Read all participant Feishu nicknames and real names from the basic information questionnaire.
  - Traverse the `受试者采集数据_长春`, `受试者采集数据_深圳`, and `受试者采集数据_成都` directory trees, fuzzy-match participant folders using nicknames.
  - Output `Subject_Data_Global_Reference.xlsx` for unified reference by downstream scripts.
- **Dependencies**: `openpyxl`

### 5.2 Questionnaire Scoring Module

| Script | Scale | Scoring Method |
|--------|-------|----------------|
| `GSE_Calculation.py` | General Self-Efficacy (GSE) | Sum of 10 items |
| `ITS_Calculation.py` | Interpersonal Trust Scale (ITS) | Sum of 25 items |
| `SimulationSickness_Calculation.py` | Simulator Sickness (SSQ) | N/O/D three-factor weighted + total |
| `Pre_PANAS_Calculation.py` | Pre-experiment PANAS | PA and NA summed separately |
| `After_PANAS_Calculation.py` | Post-experiment PANAS | PA and NA summed separately |
| `BaseInfo_Calculation.py` | Participant Basic Information | Name, gender, age, etc. extraction |

All scoring scripts follow a uniform four-step pattern: locate the questionnaire file (`find_file`), read raw data (`read`), score according to scale standards (`calculate`), and output Excel results (`output`). All depend on `openpyxl`.

### 5.3 Data Preprocessing Module

| Script | Purpose |
|--------|---------|
| `GroupData_DivideByLeaderArriveTime.py` | Segment subject movement data using the leader's arrival time at the destination as boundary |
| `GroupData_DivideBySubjectArriveTime_Start_To_DP_2.py` | Segment data using the subject's arrival time at Decision Point 2 as boundary |
| `GroupData_DivideBySubjectArriveTime_DP_2_To_DP_3.py` | Extract movement data between Decision Point 2 and Decision Point 3 |
| `TrimGroupData.py` | Further trimming or filtering of aggregated GroupData |

### 5.4 Metric Extraction Module

#### Kinematic Metrics

| Script | Extracted Metric | Calculation Method |
|--------|-----------------|-------------------|
| `ExtractAvgSpeed.py` | Mean absolute speed | Read AbsVelo column per frame, aggregate mean by level |
| `ExtractAvgAcc.py` | Mean acceleration | Read three-axis acceleration components, compute vector mean |
| `ExtractMoveDistance.py` | Total travel path length | Accumulate Euclidean distance between consecutive frames |
| `ExtractTravelTime.py` | Evacuation time | Timestamp difference between first and last frame |
| `Full_Speed.py` | Full velocity time series | Extract velocity sequences for all participants across all levels |
| `Full_Acc.py` | Full acceleration time series | Extract acceleration sequences for all participants across all levels |

#### Eye-Tracking Metrics

| Script | Extracted Metric |
|--------|-----------------|
| `Extract_Full_Gaze_Info_On_All.py` | All-target gaze frames (no target filtering) |
| `Extract_Full_Gaze_Info_On_Leader.py` | Leader gaze frames |
| `Extract_Full_Gaze_Info_On_NPC.py` | NPC gaze frames |
| `Extract_Full_Gaze_Info_On_Env.py` | Environment gaze frames |
| `Extract_Full_Gaze_Info_On_Leader_Advanced.py` | Leader gaze frames (with advanced features: duration, consecutive frame count) |
| `ExtractGazePoint.py` | Gaze point world coordinates |
| `Eye_Gaze_On_Leader.py` | Gaze direction vector toward Leader |
| `Eye_Gaze_On_NPC.py` | Gaze direction vector toward NPC |
| `Eye_Gaze_On_Env.py` | Gaze direction vector toward Environment |

#### Following Behavior Metrics

| Script | Extracted Metric |
|--------|-----------------|
| `Followship_Calculation.py` | Per-frame subject-leader Euclidean distance; follow status determined by threshold; follow-time ratio per level |
| `ExtractGazeLeaderTimes.py` | Number of times the participant gazed at the leader |

### 5.5 Statistical Testing Module

Located under `Scripts/Analyze_Statistics/`, organized into 10 subdirectories by test method:

| No. | Directory | Test Method | Application |
|-----|-----------|-------------|-------------|
| 1 | `1_Shapiro-Wilk/` | Shapiro-Wilk test | Normality testing |
| 2 | `2_Kolmogorov-Smirnov/` | Kolmogorov-Smirnov test | Normality testing |
| 3 | `3_T_Test_Independent/` | Independent samples t-test | Comparing means of two independent groups |
| 4 | `4_T_Test_Paired/` | Paired samples t-test | Comparing means of two paired groups |
| 5 | `5_Mann_Whitney/` | Mann-Whitney U test | Non-parametric test for two independent groups |
| 6 | `6_Wilcoxon/` | Wilcoxon signed-rank test | Non-parametric test for two paired groups |
| 7 | `7_One_Way_ANOVA/` | One-way ANOVA | Comparing means of multiple independent groups |
| 8 | `8_Repeat_ANOVA/` | Repeated measures ANOVA | Comparing means for repeated measures data |
| 9 | `9_Kruskal-Wallis/` | Kruskal-Wallis test | Non-parametric test for multiple independent groups |
| 10 | `10_Friedman/` | Friedman test | Non-parametric test for multiple paired groups |

### 5.6 Advanced Modeling Module

#### Bayesian Hierarchical Logistic Regression (PyMC)

Located in `Scripts/Analyze_Bayesian_DP1/`, `Analyze_Bayesian_DP2/`, `Analyze_Bayesian_DP3/` for the three decision points respectively.

- **Purpose**: Build Bayesian hierarchical logistic regression models using PyMC to analyze factors influencing following decisions at each decision point. Models include fixed effects (e.g., gender, age, GSE, ITS) and random effects (individual participant differences).
- **Version Iteration**: V1 through V8 progressive refinement; from V5 onward, models are split by decision point (DP1/DP2/DP3); V7 introduces more refined prior specifications and sampling parameters; V8 adds model evaluation metrics including ROC curves, precision-recall curves, and calibration curves.
- **Dependencies**: `pymc`, `arviz`, `scikit-learn`, `matplotlib`

#### Mixed-Effects Logit Model (pymer4)

Located in `Scripts/Analyze_MultiEffectLogit_DP1/`, `Analyze_MultiEffectLogit_DP2/`, `Analyze_MultiEffectLogit_DP3/`.

- **Purpose**: Use pymer4 (based on R's lme4 package) to build Generalized Linear Mixed Models (GLMM) with logit link function, analyzing following behavior at each decision point from a frequentist perspective, complementing the Bayesian approach methodologically.
- **Version Iteration**: V1 through V5 progressive refinement; V5 split into per-decision-point versions; V5_NC serves as the no-covariate control version.
- **Dependencies**: `pymer4` (requires R environment), `pandas`

#### Cross-Decision-Point Analysis

Located in `Scripts/Analyze_Merge_DPs/`.

- **Purpose**: `MergeDP.py` combines fixed-effect results from all three decision points for cross-decision-point comparative visualization (e.g., forest-plot style display of effect sizes and credible/confidence intervals for each predictor).

### 5.7 Eye-Gaze Pattern Analysis Module

#### DBSCAN Clustering Analysis

Organized into four subdirectories by scene and gaze target:

| Directory | Scene Coverage | Output Type |
|-----------|---------------|-------------|
| `Analyze_EyeGazePattern/` | General (scene-independent) | 2D contour / 3D scatter |
| `Analyze_EyeGazePattern_Hall/` | Hall corridor | 2D contour / 3D scatter |
| `Analyze_EyeGazePattern_Plat/` | Platform | 2D contour / 3D scatter |
| `Analyze_EyeGazePattern_Aisle/` | Aisle | 2D contour / 3D scatter |

Each subdirectory contains 8 scripts, arranged by gaze target (OnAll / OnEnv / OnLeader / OnNPC) and dimensionality (2D / 3D). The unified workflow is:

1. Load gaze point coordinates by group (Security / Passenger / Robot)
2. Apply DBSCAN clustering (ε=0.097, min_samples=10) for density-based clustering
3. Generate gaze heatmaps via KDE (Gaussian kernel density estimation)
4. Produce 2D contour plots or 3D scatter plots, overlaid on scene screenshots as background

#### Gaze Topology Maps

Located under `Analyze_EyeGazePattern/`:

| Script | Purpose |
|--------|---------|
| `On_All_Topo.py` | All-target gaze point topology distribution map |
| `On_Env_Topo.py` | Environment gaze point topology distribution map |
| `On_Leader_Topo.py` | Leader gaze point topology distribution map |
| `On_NPC_Topo.py` | NPC gaze point topology distribution map |

#### Gaze Metric Analysis

Located in `Scripts/Analyze_EyeGaze_Index/`:

| Script | Purpose |
|--------|---------|
| `ExtractGazeRouteDistance.py` / `GazeRouteDistance.py` | Extract and compute total gaze path length |
| `ExtractGazeRouteSpeed.py` / `GazeRouteSpeed.py` | Extract and compute mean gaze movement speed |
| `ExtractLyapunov.py` / `Lyapunov_Rosenstein.py` / `Lyapunov_Wolf.py` | Compute Lyapunov exponents of gaze time series, assessing chaotic properties of gaze patterns |
| `RelativePosDataConfirm.py` | Validate relative position data consistency of gaze points |

#### Gaze Target Visualization

| Directory | Purpose |
|-----------|---------|
| `Analyze_EyeGazeOnLeader/` | Leader gaze point cloud capsule and scatter plots |
| `Analyze_EyeGazeOnNPC/` | NPC gaze point cloud scatter plots |

### 5.8 Between-Group & Within-Group Comparison Module

#### Between-Group Comparison

Located in `Scripts/Compare_BetweenGroup/`, performing statistical comparison and visualization across Security/Passenger/Robot groups for the following metrics:

- Evacuation acceleration, evacuation path length, evacuation speed, evacuation time
- Gaze depth, gaze scanning length, gaze scanning velocity
- Maximum Lyapunov exponent, number of gazes on leader
- DTW trajectory similarity

Each metric includes box plots (`CompareBetweenGroups_Box_6.py` / `_Box_7.py`, for 6 and 7 metrics respectively), violin plots (`CompareBetweenGroups_Vio.py`), no-covariate versions (`_NC.py`), and data renaming scripts (`Rename.py`).

#### Within-Group Comparison

Located in `Scripts/Compare_InsideGroup/`, displaying within-group individual differences via Spearman correlation analysis, box plots, and violin plots.

#### Decision Point Comparison

| Script | Purpose |
|--------|---------|
| `CompareDPInsideGroup.py` | Within-group comparison of follow ratios across decision points |
| `CompareDPBetweenGroup.py` | Between-group comparison of follow ratios across decision points |

### 5.9 Trajectory Analysis Module

#### DTW Trajectory Similarity

| Script | Purpose |
|--------|---------|
| `BaseDTW.py` | Compute pairwise DTW distances between participant trajectories using the fastdtw algorithm |
| `DrawTrajDTW/ExtractDTW.py` | Extract and organize the DTW distance matrix |
| `DrawTrajDTW/DrawTrajDTW.py` | Plot DTW trajectory alignment line plots |
| `DrawTrajDTW/DrawDTW_MergeBox.py` | Plot multi-condition merged DTW distance box plots |

#### Cross-Scene Path Comparison

Located in `Scripts/ComparePathBetweenScene/`, comparing evacuation path differences between Hall and Platform scenes, with single-scene and merged analysis versions (`_Merge`, `_Merge_All`).

#### Cross-Scene Velocity Comparison

Located in `Scripts/ComparePlaneVelocity/`, comparing planar movement velocities across Hall and Platform scenes.

### 5.10 Visualization Module

#### Questionnaire Data Visualization

Located in `Scripts/DrawFig/`, each subdirectory corresponds to one questionnaire scale:

| Directory | Scale | Chart Type |
|-----------|-------|------------|
| `Age/` | Age distribution | Histogram / box plot |
| `Experience/` | Gaming/VR/metro usage experience | Bar chart / box plot |
| `Gender/` | Gender distribution | Bar chart |
| `GSE/` | General Self-Efficacy | Box plot |
| `ITS/` | Interpersonal Trust | Box plot |
| `Location/` | Data collection site distribution | Bar chart |
| `PANAS/` | Positive and Negative Affect | Box plot |
| `PQ/` | Presence Questionnaire | Box plot |
| `Preference/` | Preference questionnaire | Box plot |
| `SSQ/` | Simulator Sickness | Box plot |
| `TLX/` | Task Load Index | Box plot |

#### Polar Gaze Plots

| Directory | Purpose |
|-----------|---------|
| `DrawGazeOnAllPolar_HeatMap/` | All-target AOI polar heatmap |
| `DrawGazeOnAllPolar_Points/` | All-target AOI polar scatter plot |
| `DrawGazeOnEnvPolar_HeatMap/` | Environment AOI polar heatmap |
| `DrawGazeOnLeaderPolar_HeatMap/` | Leader AOI polar heatmap |
| `DrawGazeOnLeaderPolar_Points/` | Leader AOI polar scatter plot |
| `DrawGazeOnLeaderPolar_Single/` | Single-participant leader polar plot |
| `DrawGazeOnNPCPolar_HeatMap/` | NPC AOI polar heatmap |

#### Other Visualizations

| Directory / Script | Purpose |
|--------------------|---------|
| `DrawSpearman/` | Spearman correlation matrix heatmaps (6-metric and 7-metric versions) |
| `DrawPie_3_Item/` | Three-group destination choice distribution pie charts and merged pie chart |
| `Draw_Subject_Trajectory_Single_Level.py` | Single-level participant trajectory plotting |

### 5.11 Auxiliary Module

| Script | Purpose |
|--------|---------|
| `ExamNormalDist.py` | Normality distribution testing for metrics |
| `ExamKW.py` | Kruskal-Wallis testing for metrics |
| `Calculate_Total_Time.py` / `Total_Time_Calculation.py` / `Total_Time_Interval.py` | Total evacuation time calculation and interval statistics |
| `CompareAcc.py` / `CompareAvgSpeed.py` / `CompareDP.py` / `CompareGazeDistance.py` / `CompareGazeLeaderTimes.py` / `CompareMoveDistance.py` / `CompareTotalTravelTime.py` | Comparative analysis scripts for various metrics |
| `Delete_Target_Script.py` | Batch deletion utility |
| `Record_Data_Modify.py` | Experimental recording data correction |
| `Subject_Destination.py` / `Subject_Leader.py` | Participant destination choice and leader analysis |
| `GroupData.py` (under each participant directory) | An independent copy of GroupData.py resides under each participant's data directory, functionally identical to the main version under Scripts/ |
