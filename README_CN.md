# VR 疏散实验数据分析系统 框架文档

## 一、总体介绍

本项目为虚拟现实疏散实验的数据分析代码仓库，围绕“领导者在场对人员疏散决策与行为的影响”这一核心研究问题，对多受试者、多关卡、多组别的眼动追踪、运动轨迹以及问卷量表数据进行系统性的提取、清洗、统计建模与可视化。

实验数据采集于长春、深圳、成都三地，受试者按照领导者类型分为 Passenger（乘客）、Robot（机器人）、Security（安保）三组，覆盖 A1 至 B5 共 7 个实验关卡。

**数据与隐私说明**：
- 本仓库仅包含数据分析代码，不包含任何实验原始数据或中间结果数据。
- 所有涉及受试者隐私的数据（主要指受试者姓名）均已经过 MD5 哈希脱敏处理，仓库中不包含任何可识别的个人身份信息。

分析流程的核心模块包括：

- **数据聚合与清洗**：将单关卡多源数据（Log、EyeGaze、NPC、Subject）按时间戳对齐，生成统一的 GroupData 文件，并构建全局受试者索引。
- **指标提取**：从 GroupData 中提取运动学指标（速度、加速度、移动距离、疏散耗时）、眼动指标（注视目标分类、注视点坐标、注视路径距离与速度、Lyapunov 指数）以及跟随行为指标（跟随比例、跟随关系）。
- **量表计分**：对 GSE（自我效能感）、ITS（人际信任）、SSQ（仿真不适）、PANAS（正负情绪）等标准化心理学量表进行计分与汇总。
- **统计检验**：涵盖 Shapiro-Wilk、Kolmogorov-Smirnov、独立样本及配对 t 检验、Mann-Whitney U、Wilcoxon 符号秩检验、单因素及重复测量 ANOVA、Kruskal-Wallis 检验、Friedman 检验等十种方法。
- **高级建模**：基于 PyMC 的贝叶斯层次 Logistic 回归模型（V1 至 V8 迭代），以及基于 pymer4（R lme4 接口）的混合效应 Logit 模型（V1 至 V5 迭代），用于分析决策点跟随行为的影响因素。
- **眼动模式分析**：对注视点进行 DBSCAN 聚类（2D/3D），按场景（Hall、Platform、Aisle）和注视目标（All、Environment、Leader、NPC）细分，生成 KDE 热力图与拓扑图。
- **组间/组内比较与可视化**：箱型图、小提琴图、Spearman 相关性热力图、DTW 轨迹相似度分析、极坐标注视热力图、饼图等多种可视化。

---

## 二、快速开始

### 2.1 环境要求

- Python 3.9 或更高版本
- R 4.0 或更高版本（pymer4 依赖 R 语言环境）

### 2.2 安装依赖

本项目未提供 `requirements.txt` 文件，请根据实际使用的脚本逐一安装所需依赖包。核心依赖如下：

```bash
pip install pandas numpy matplotlib seaborn scipy scikit-learn
pip install pymc arviz fastdtw openpyxl tqdm psutil
pip install pymer4
```

### 2.3 数据准备

本仓库不包含实验数据。如需复现分析流程，请将实验数据按以下目录结构放置：

- `受试者采集数据_长春/`：长春站受试者数据（每受试者一个子目录）
- `受试者采集数据_深圳/`：深圳站受试者数据（每受试者一个子目录）
- `受试者采集数据_成都/`：成都站受试者数据（每受试者一个子目录）
- `问卷数据/`：各类问卷原始 Excel 文件

### 2.4 运行流程

分析流程按以下顺序执行：

1. `Build_Global_Reference.py`：构建全局受试者索引
2. `GroupData.py`：聚合每位受试者每个关卡的多源数据
3. 各类量表计分脚本（`GSE_Calculation.py`、`ITS_Calculation.py` 等）
4. 各类指标提取脚本（`ExtractAvgSpeed.py`、`Extract_Full_Gaze_Info_*.py` 等）
5. 统计检验脚本（`Analyze_Statistics/` 下各子目录）
6. 高级建模脚本（`Analyze_Bayesian_DP*/`、`Analyze_MultiEffectLogit_DP*/`）
7. 可视化脚本（`DrawFig/`、`DrawGaze*/`、`Compare*/` 等）

---

## 三、主要依赖包

| 依赖包 | 版本要求 | 用途说明 |
|--------|----------|----------|
| pandas | - | 数据框操作与 CSV 读写 |
| numpy | - | 数值计算与数组操作 |
| matplotlib | - | 图表绘制基础库 |
| seaborn | - | 统计图表（箱型图、小提琴图、热力图） |
| scipy | - | 统计检验（Shapiro-Wilk、K-S、t 检验等） |
| scikit-learn | - | 数据标准化、DBSCAN 聚类、模型评估指标 |
| pymc | - | 贝叶斯层次 Logistic 回归建模 |
| arviz | - | 贝叶斯模型后验分析与可视化 |
| pymer4 | - | 混合效应 Logistic 回归（R lme4 的 Python 接口） |
| fastdtw | - | 动态时间规整计算（轨迹相似度度量） |
| openpyxl | - | Excel 文件读写 |
| tqdm | - | 进度条显示 |
| psutil | - | 系统资源监控 |

---

## 四、开发里程碑

[需要提供 Git 提交记录以生成里程碑]

---

## 五、模块与脚本详细说明

### 5.1 数据聚合模块

#### GroupData.py

- **功能描述**：将每位受试者每个关卡的多源 CSV 数据（Log_Info、EyeGaze_Simulation_Info、NPC_Simulation_Info、Subject_Simulation_Info）按时间戳对齐，合并为统一的 GroupData CSV 文件。
- **核心逻辑**：
  - 扫描受试者目录下 A1 至 B5 共 7 个关卡文件夹，每个文件夹包含 4 类 CSV 源文件。
  - 以 Log_Info 中的 "Unfreeze Subject Agent Move" 和 "Subject Agent Has Arrive" 事件确定有效时间窗口。
  - 按统一时间采样点对齐并合并多源数据，每个受试者生成一个独立文件，命名为 `<受试者名>_<关卡>.csv`。
- **依赖**：`openpyxl`、`tqdm`

#### Build_Global_Reference.py

- **功能描述**：通过扫描长春、深圳与成都三地的受试者数据目录，建立受试者昵称到数据文件夹路径的映射，并导出为全局索引表。
- **核心逻辑**：
  - 从基本情况问卷中读取所有受试者的飞书昵称与真实姓名。
  - 遍历 `受试者采集数据_长春`、`受试者采集数据_深圳` 和 `受试者采集数据_成都` 目录树，利用昵称模糊匹配受试者文件夹。
  - 输出 `Subject_Data_Global_Reference.xlsx` 供后续脚本统一引用。
- **依赖**：`openpyxl`

### 5.2 量表计分模块

| 脚本 | 量表名称 | 计分方式 |
|------|----------|----------|
| `GSE_Calculation.py` | 自我效能感 (GSE) | 10 项加总分 |
| `ITS_Calculation.py` | 人际信任 (ITS) | 25 项加总分 |
| `SimulationSickness_Calculation.py` | 仿真不适 (SSQ) | N/O/D 三因子加权 + 总分 |
| `Pre_PANAS_Calculation.py` | 实验前正负情绪 (PANAS) | PA 与 NA 分别加总 |
| `After_PANAS_Calculation.py` | 实验后正负情绪 (PANAS) | PA 与 NA 分别加总 |
| `BaseInfo_Calculation.py` | 受试者基本信息 | 姓名、性别、年龄等字段提取 |

所有计分脚本采用统一的四步模式：定位问卷文件 (`find_file`)、读取原始数据 (`read`)、按量表标准计分 (`calculate`)、输出 Excel 结果 (`output`)。依赖均为 `openpyxl`。

### 5.3 数据预处理模块

| 脚本 | 功能描述 |
|------|----------|
| `GroupData_DivideByLeaderArriveTime.py` | 以领导者到达终点的时间戳为边界，截取受试者在对应时间窗口内的运动数据 |
| `GroupData_DivideBySubjectArriveTime_Start_To_DP_2.py` | 以受试者到达决策点 2 的时刻为边界切分数据 |
| `GroupData_DivideBySubjectArriveTime_DP_2_To_DP_3.py` | 截取受试者从决策点 2 到决策点 3 之间的运动数据 |
| `TrimGroupData.py` | 对聚合后的 GroupData 进行进一步裁剪或过滤 |

### 5.4 指标提取模块

#### 运动学指标

| 脚本 | 提取指标 | 计算方法 |
|------|----------|----------|
| `ExtractAvgSpeed.py` | 平均绝对速度 | 逐帧读取 AbsVelo 列，按关卡聚合求均值 |
| `ExtractAvgAcc.py` | 平均加速度 | 读取三轴加速度分量，计算矢量加速度均值 |
| `ExtractMoveDistance.py` | 移动路径总长度 | 逐帧累加相邻帧之间的欧氏距离 |
| `ExtractTravelTime.py` | 疏散耗时 | 首帧与末帧时间戳差值 |
| `Full_Speed.py` | 全量速度序列 | 提取所有受试者所有关卡的速度时间序列 |
| `Full_Acc.py` | 全量加速度序列 | 提取所有受试者所有关卡的加速度时间序列 |

#### 眼动指标

| 脚本 | 提取指标 |
|------|----------|
| `Extract_Full_Gaze_Info_On_All.py` | 全目标注视帧（不筛选目标类型） |
| `Extract_Full_Gaze_Info_On_Leader.py` | 领导者注视帧 |
| `Extract_Full_Gaze_Info_On_NPC.py` | NPC 注视帧 |
| `Extract_Full_Gaze_Info_On_Env.py` | 环境注视帧 |
| `Extract_Full_Gaze_Info_On_Leader_Advanced.py` | 领导者注视帧（含注视时长、连续帧数等高级特征） |
| `ExtractGazePoint.py` | 注视点世界坐标 |
| `Eye_Gaze_On_Leader.py` | 对领导者的注视方向向量 |
| `Eye_Gaze_On_NPC.py` | 对 NPC 的注视方向向量 |
| `Eye_Gaze_On_Env.py` | 对环境的注视方向向量 |

#### 跟随行为指标

| 脚本 | 提取指标 |
|------|----------|
| `Followship_Calculation.py` | 逐帧计算受试者与领导者之间的欧氏距离，按阈值判定跟随状态，统计各关卡跟随时间比例 |
| `ExtractGazeLeaderTimes.py` | 注视领导者次数 |

### 5.5 统计检验模块

位于 `Scripts/Analyze_Statistics/` 目录下，按检验方法组织为 10 个子目录：

| 序号 | 目录 | 检验方法 | 适用场景 |
|------|------|----------|----------|
| 1 | `1_Shapiro-Wilk/` | Shapiro-Wilk 检验 | 正态性检验 |
| 2 | `2_Kolmogorov-Smirnov/` | Kolmogorov-Smirnov 检验 | 正态性检验 |
| 3 | `3_T_Test_Independent/` | 独立样本 t 检验 | 两组独立样本均值比较 |
| 4 | `4_T_Test_Paired/` | 配对样本 t 检验 | 两组配对样本均值比较 |
| 5 | `5_Mann_Whitney/` | Mann-Whitney U 检验 | 两组独立样本的非参数检验 |
| 6 | `6_Wilcoxon/` | Wilcoxon 符号秩检验 | 两组配对样本的非参数检验 |
| 7 | `7_One_Way_ANOVA/` | 单因素方差分析 | 多组独立样本均值比较 |
| 8 | `8_Repeat_ANOVA/` | 重复测量方差分析 | 多组重复测量数据均值比较 |
| 9 | `9_Kruskal-Wallis/` | Kruskal-Wallis 检验 | 多组独立样本的非参数检验 |
| 10 | `10_Friedman/` | Friedman 检验 | 多组配对样本的非参数检验 |

### 5.6 高级建模模块

#### 贝叶斯层次 Logistic 回归 (PyMC)

位于 `Scripts/Analyze_Bayesian_DP1/`、`Analyze_Bayesian_DP2/`、`Analyze_Bayesian_DP3/` 分别对应三个决策点。

- **功能描述**：使用 PyMC 构建贝叶斯层次 Logistic 回归模型，分析各决策点处受试者跟随决策的影响因素。模型包含固定效应（如性别、年龄、GSE、ITS 等）与随机效应（受试者个体差异）。
- **版本迭代**：V1 至 V8 逐步演进，V5 起分化为按决策点独立的版本（DP1/DP2/DP3），V7 引入更精细的先验设定与采样参数，V8 增加 ROC、Precision-Recall 曲线及校准曲线等模型评估指标。
- **依赖**：`pymc`、`arviz`、`scikit-learn`、`matplotlib`

#### 混合效应 Logit 模型 (pymer4)

位于 `Scripts/Analyze_MultiEffectLogit_DP1/`、`Analyze_MultiEffectLogit_DP2/`、`Analyze_MultiEffectLogit_DP3/`。

- **功能描述**：使用 pymer4（基于 R 的 lme4 包）构建广义线性混合模型（GLMM），以 Logit 连接函数分析各决策点的跟随行为。与贝叶斯模型形成方法学互补，提供频率学派的建模视角。
- **版本迭代**：V1 至 V5 逐步演进，V5 分化为按决策点独立版本，V5_NC 为无协变量对照组。
- **依赖**：`pymer4`（需要 R 环境）、`pandas`

#### 决策点合并分析

位于 `Scripts/Analyze_Merge_DPs/`。

- **功能描述**：`MergeDP.py` 将三个决策点的固定效应结果合并，进行跨决策点的对比可视化（如森林图样式展示各预测变量的效应量及可信区间）。

### 5.7 眼动模式分析模块

#### DBSCAN 聚类分析

按场景和注视目标分为四个子目录：

| 目录 | 覆盖场景 | 输出类型 |
|------|----------|----------|
| `Analyze_EyeGazePattern/` | 通用（不区分场景） | 2D 等高线 / 3D 散点 |
| `Analyze_EyeGazePattern_Hall/` | Hall（走廊） | 2D 等高线 / 3D 散点 |
| `Analyze_EyeGazePattern_Plat/` | Platform（站台） | 2D 等高线 / 3D 散点 |
| `Analyze_EyeGazePattern_Aisle/` | Aisle（通道） | 2D 等高线 / 3D 散点 |

每个子目录包含 8 个脚本，按注视目标（OnAll / OnEnv / OnLeader / OnNPC）和维度（2D / 3D）排列组合。脚本统一流程为：

1. 按分组（Security / Passenger / Robot）加载注视点坐标
2. 使用 DBSCAN 算法（ε=0.097, min_samples=10）进行密度聚类
3. 通过 KDE（高斯核密度估计）生成注视热力图
4. 绘制 2D 等高线图或 3D 散点图，并叠加场景截图作为背景

#### 注视拓扑图

位于 `Analyze_EyeGazePattern/` 子目录中：

| 脚本 | 功能描述 |
|------|----------|
| `On_All_Topo.py` | 全目标注视点拓扑分布图 |
| `On_Env_Topo.py` | 环境注视点拓扑分布图 |
| `On_Leader_Topo.py` | 领导者注视点拓扑分布图 |
| `On_NPC_Topo.py` | NPC 注视点拓扑分布图 |

#### 注视指标分析

位于 `Scripts/Analyze_EyeGaze_Index/`：

| 脚本 | 功能描述 |
|------|----------|
| `ExtractGazeRouteDistance.py` / `GazeRouteDistance.py` | 提取并计算注视路径的总长度 |
| `ExtractGazeRouteSpeed.py` / `GazeRouteSpeed.py` | 提取并计算注视移动的平均速度 |
| `ExtractLyapunov.py` / `Lyapunov_Rosenstein.py` / `Lyapunov_Wolf.py` | 计算注视时间序列的 Lyapunov 指数，评估注视模式的混沌特性 |
| `RelativePosDataConfirm.py` | 验证注视点的相对位置数据一致性 |

#### 注视对象可视化

| 目录 | 功能描述 |
|------|----------|
| `Analyze_EyeGazeOnLeader/` | 绘制领导者注视点云胶囊图与点云分布图 |
| `Analyze_EyeGazeOnNPC/` | 绘制 NPC 注视点云分布图 |

### 5.8 组间与组内比较模块

#### 组间比较

位于 `Scripts/Compare_BetweenGroup/`，对以下指标进行 Security/Passenger/Robot 三组间的统计比较与可视化：

- 疏散加速度、疏散路径长度、疏散速度、疏散时间
- 注视深度、注视扫描长度、注视扫描速度
- 最大 Lyapunov 指数、注视领导者次数
- DTW 轨迹相似度

每种指标均提供箱型图（`CompareBetweenGroups_Box_6.py` / `_Box_7.py`，对应 6 项与 7 项指标）和小提琴图（`CompareBetweenGroups_Vio.py`）、无协变量版本（`_NC.py`）以及数据重命名脚本（`Rename.py`）。

#### 组内比较

位于 `Scripts/Compare_InsideGroup/`，通过 Spearman 相关性分析和箱型图/小提琴图展示组内个体差异。

#### 决策点比较

| 脚本 | 功能描述 |
|------|----------|
| `CompareDPInsideGroup.py` | 组内各决策点跟随比例的比较 |
| `CompareDPBetweenGroup.py` | 组间各决策点跟随比例的比较 |

### 5.9 轨迹分析模块

#### DTW 轨迹相似度

| 脚本 | 功能描述 |
|------|----------|
| `BaseDTW.py` | 使用 fastdtw 算法计算两两受试者之间的轨迹 DTW 距离 |
| `DrawTrajDTW/ExtractDTW.py` | 提取并组织 DTW 距离矩阵 |
| `DrawTrajDTW/DrawTrajDTW.py` | 绘制 DTW 轨迹对齐线图 |
| `DrawTrajDTW/DrawDTW_MergeBox.py` | 绘制多条件合并的 DTW 距离箱型图 |

#### 场景间路径比较

位于 `Scripts/ComparePathBetweenScene/`，比较 Hall 与 Platform 场景间的疏散路径差异，提供单场景与合并分析（`_Merge`、`_Merge_All`）。

#### 场景间速度比较

位于 `Scripts/ComparePlaneVelocity/`，按 Hall 与 Platform 场景比较受试者的平面移动速度。

### 5.10 可视化模块

#### 问卷数据可视化

位于 `Scripts/DrawFig/`，各子目录分别对应一种问卷量表：

| 目录 | 量表 | 图表类型 |
|------|------|----------|
| `Age/` | 年龄分布 | 直方图/箱型图 |
| `Experience/` | 游戏/VR/地铁使用经验 | 柱状图/箱型图 |
| `Gender/` | 性别分布 | 柱状图 |
| `GSE/` | 自我效能感 | 箱型图 |
| `ITS/` | 人际信任 | 箱型图 |
| `Location/` | 采集地点分布 | 柱状图 |
| `PANAS/` | 正负情绪 | 箱型图 |
| `PQ/` | 存在感问卷 | 箱型图 |
| `Preference/` | 偏好问卷 | 箱型图 |
| `SSQ/` | 仿真不适 | 箱型图 |
| `TLX/` | 任务负荷 | 箱型图 |

#### 极坐标注视图

| 目录 | 功能描述 |
|------|----------|
| `DrawGazeOnAllPolar_HeatMap/` | 全目标 AOI 极坐标热力图 |
| `DrawGazeOnAllPolar_Points/` | 全目标 AOI 极坐标散点图 |
| `DrawGazeOnEnvPolar_HeatMap/` | 环境 AOI 极坐标热力图 |
| `DrawGazeOnLeaderPolar_HeatMap/` | 领导者 AOI 极坐标热力图 |
| `DrawGazeOnLeaderPolar_Points/` | 领导者 AOI 极坐标散点图 |
| `DrawGazeOnLeaderPolar_Single/` | 单受试者领导者极坐标图 |
| `DrawGazeOnNPCPolar_HeatMap/` | NPC AOI 极坐标热力图 |

#### 其他可视化

| 目录/脚本 | 功能描述 |
|------|----------|
| `DrawSpearman/` | Spearman 相关性矩阵热力图（6 项与 7 项指标版本） |
| `DrawPie_3_Item/` | 三组受试者终点选择分布饼图及合并饼图 |
| `Draw_Subject_Trajectory_Single_Level.py` | 单关卡受试者轨迹绘制 |

### 5.11 辅助模块

| 脚本 | 功能描述 |
|------|----------|
| `ExamNormalDist.py` | 对各指标进行正态分布检验 |
| `ExamKW.py` | 对各指标进行 Kruskal-Wallis 检验 |
| `Calculate_Total_Time.py` / `Total_Time_Calculation.py` / `Total_Time_Interval.py` | 疏散总时间计算与区间统计 |
| `CompareAcc.py` / `CompareAvgSpeed.py` / `CompareDP.py` / `CompareGazeDistance.py` / `CompareGazeLeaderTimes.py` / `CompareMoveDistance.py` / `CompareTotalTravelTime.py` | 各指标的比较分析脚本 |
| `Delete_Target_Script.py` | 批量删除辅助工具 |
| `Record_Data_Modify.py` | 实验记录数据修正 |
| `Subject_Destination.py` / `Subject_Leader.py` | 受试者终点选择与领导者分析 |
| `GroupData.py`（受试者目录下） | 每位受试者数据目录下均有一份独立的 GroupData.py，功能与 Scripts 目录下的主版本相同 |
