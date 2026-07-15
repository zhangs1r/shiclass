window.SHICLASS_DATA = {
  featuredCollectionId: "seminar-series",
  groups: [
    {
      id: "seminars",
      kind: "研讨会",
      title: "施老师大课堂 · 研讨会系列",
      emoji: "🎓",
      description: "施凌老师研讨会系列课程，涵盖 Kalman Filter 理论、演讲技巧、学术规范等内容。按时间顺序排列，从入门到深入。",
      meta: ["KF 系列", "演讲技巧", "学术规范"]
    }
  ],
  collections: [
    {
      id: "yang-xicheng",
      groupId: "seminars",
      kind: "特邀分享",
      title: "图像算法在安防行业的应用",
      subtitle: "杨熙丞 · 特邀分享",
      description: "特邀杨熙丞分享图像算法在安防行业中的实际应用案例与技术经验。",
      quickOpen: "lessons/0000-图像算法安防应用.html",
      meta: ["1 节课", "~30 分钟", "安防 / 图像算法"]
    },
    {
      id: "series-1-2",
      groupId: "seminars",
      kind: "研讨会系列",
      title: "系列 1-2：研究共同体与学术规范",
      subtitle: "研讨会系列 1-2",
      description: "第 0001-0002 课。研究共同体的构建方法、组内学术规范与职业习惯。",
      quickOpen: "lessons/0001-研究共同体方向地图.html",
      meta: ["2 节课", "~90 分钟", "学术规范"]
    },
    {
      id: "series-3-speech",
      groupId: "seminars",
      kind: "研讨会系列",
      title: "系列 3：演讲技巧与学术表达",
      subtitle: "研讨会系列 3",
      description: "第 0003 课。如何做好学术演讲？从结构设计到表达技巧。",
      quickOpen: "lessons/0003-演讲技巧学术表达.html",
      meta: ["1 节课", "~45 分钟", "演讲技巧"]
    },
    {
      id: "kf-series-4-5",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L1-L2：矩阵基础与状态空间",
      subtitle: "Kalman Filter 入门系列 (L1-L2)",
      description: "第 0004-0005 课（KF L1-L2），已拆分为 4 节。矩阵特征值、SVD、正定性、矩阵求逆引理、状态空间模型与协方差传播，打下 KF 数学基础。",
      quickOpen: "lessons/0004-KF-L1-矩阵特征值.html",
      meta: ["4 节", "~3 小时", "矩阵理论 / 状态空间"]
    },
    {
      id: "kf-series-l5",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L5：贝叶斯估计与 Bayes Rule",
      subtitle: "Kalman Filter 贝叶斯基础 (L5)",
      description: "新增第 KF L5 课。贝叶斯估计入门——Bayes Rule、先验/似然/后验、Romeo & Juliet 经典例子。填补 L4（可观性）到 L6（MAP/MMSE）之间的理论桥梁。",
      quickOpen: "lessons/KF-L5-贝叶斯估计与BayesRule.html",
      meta: ["1 课", "~60 分钟", "贝叶斯估计"]
    },
    {
      id: "kf-series-6-7",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L3-L4：系统理论与能控可观",
      subtitle: "Kalman Filter 系统基础 (L3-L4)",
      description: "第 0006-0007 课（KF L3-L4）。二次型优化、系统稳定性、能控性、最小能量控制、PBH、可观性。",
      quickOpen: "lessons/0006-KF-L3-二次型优化.html",
      meta: ["2 节", "~3 小时", "系统理论 / 能控性"]
    },
    {
      id: "kf-series-9-11",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L6-L9：估计理论与最小二乘",
      subtitle: "Kalman Filter 进阶系列 (L6-L9)",
      description: "第 0008-0011 课。MAP、MMSE、最大似然、最小二乘与内积空间。",
      quickOpen: "lessons/0008-KF-L6-MAP-MMSE.html",
      meta: ["4 节课", "~4 小时", "估计理论 / 最小二乘"]
    },
    {
      id: "kf-series-10-13",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L10-L13：投影定理与递归估计",
      subtitle: "Kalman Filter 核心系列 (L10-L13)",
      description: "第 0012-0015 课。投影定理、LMMSE、正交原理、Gram-Schmidt、新息过程、递归估计。",
      quickOpen: "lessons/0012-KF-L10-投影定理.html",
      meta: ["4 节课", "~4 小时", "投影定理 / 递归估计"]
    },
    {
      id: "kf-series-14",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L14：Kalman Filter 模型与测量更新",
      subtitle: "Kalman Filter 正式推导 (2 节)",
      description: "第 0016 课（双节）。系统模型、基本假设、估计符号体系、新息、Kalman Gain、测量更新。",
      quickOpen: "lessons/0016-KF-L14-KalmanFilter-1.html",
      meta: ["2 节", "~90 分钟", "Kalman Filter / 测量更新"]
    },
    {
      id: "kf-series-15",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L15：新息过程、Kalman 增益与后验协方差",
      subtitle: "Kalman Filter 测量更新推导 (2 节)",
      description: "第 0017-0018 课。新息定义与正交性证明、新息协方差、Kalman 增益、后验协方差更新公式的几何推导。",
      quickOpen: "lessons/0017-KF-L15-新息过程.html",
      meta: ["2 节", "~60 分钟", "新息过程 / Kalman 增益"]
    },
    {
      id: "kf-series-16",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L16：时间更新、固定增益与传感器融合",
      subtitle: "Kalman Filter 时间更新与融合 (2 节)",
      description: "第 0019-0020 课。时间更新投影法证明、协方差收敛性、固定增益估计器、信息形式 KF 与即插即用融合。",
      quickOpen: "lessons/0019-KF-L16-时间更新.html",
      meta: ["2 节", "~60 分钟", "时间更新 / 传感器融合"]
    },
    {
      id: "kf-series-17",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L17：MMSE 等价性与增益优化三种方法",
      subtitle: "Kalman Filter 概率法与优化法 (2 节)",
      description: "第 0021-0022 课。条件高斯定理、MMSE=LMMSE 证明、控制输入与分离原理、优化法与 Completion of Squares、三种方法对比。",
      quickOpen: "lessons/0021-KF-L17-条件高斯与MMSE.html",
      meta: ["2 节", "~60 分钟", "MMSE / 增益优化"]
    },
    {
      id: "special-bit",
      groupId: "seminars",
      kind: "特邀分享",
      title: "北理工分享：生成式模型驱动具身智能",
      subtitle: "许佳玉 · 特邀分享",
      description: "第 0023 课。北京理工大学许佳玉特邀分享——DDPM、Flow Matching、MinFlow 与 IMF 在机器人动作生成中的演进。基于 SRT 如实记录。",
      quickOpen: "lessons/0023-北理工-扩散模型基础.html",
      meta: ["1 节课", "~30 分钟", "具身智能 / 生成式"]
    },
    {
      id: "special-e2map",
      groupId: "seminars",
      kind: "组内分享",
      title: "E2Map：经验-情绪地图与自反式导航",
      subtitle: "张健强 · 组内分享（2 节）",
      description: "第 0025-0026 课。E2Map——导航地图进化、三层架构、经验场与情绪场公式、自反式导航代价函数与实验。",
      quickOpen: "lessons/0025-E2Map-架构与经验场.html",
      meta: ["2 节课", "~60 分钟", "情绪地图 / 导航"]
    },
    {
      id: "kf-series-18",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L18：动态规划入门与 Bellman 方程",
      subtitle: "Kalman Filter 延伸系列 (2 节)",
      description: "第 0027-0028 课。动态规划（DP）入门——离散时间动态系统、7-11 库存控制例子、策略与 Bellman 方程推导。",
      quickOpen: "lessons/0027-KF-L18-动态规划基础.html",
      meta: ["2 节课", "~60 分钟", "动态规划 / Bellman"]
    },
    {
      id: "kf-series-19",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L19：最优性原理、DP 算法与维度灾难",
      subtitle: "Kalman Filter 延伸系列 (2 节)",
      description: "第 0029-0030 课。动态规划理论深化——Bellman 最优性原理形式化证明、海盗分钻石经典案例（向后归纳）、DP 算法反向递推、维度灾难与应对。",
      quickOpen: "lessons/0029-KF-L19-最优性原理.html",
      meta: ["2 节课", "~60 分钟", "最优性原理 / 维度灾难"]
    }
  ],
    lessons: [
    {
      id: "0000-图像算法安防应用",
      collectionId: "yang-xicheng",
      path: "lessons/0000-图像算法安防应用.html",
      title: "杨熙丞：图像算法在安防行业的应用",
      subtitle: "荧光抓拍、车窗增强、算法部署全流程与校招建议",
      duration: "30 min",
      tags: ["图像算法", "安防"]
    },
    {
      id: "0001-研究共同体方向地图",
      collectionId: "series-1-2",
      path: "lessons/0001-研究共同体方向地图.html",
      title: "研究共同体与方向地图",
      subtitle: "从海关检测到SLAM——统一的状态估计主线",
      duration: "30 min",
      tags: ["学术规范"]
    },
    {
      id: "0002-学术规范职业习惯",
      collectionId: "series-1-2",
      path: "lessons/0002-学术规范职业习惯.html",
      title: "组规、学术规范与职业习惯",
      subtitle: "学术诚信、投稿规范、守时与邮件礼仪",
      duration: "30 min",
      tags: ["学术规范"]
    },
    {
      id: "0003-演讲技巧学术表达",
      collectionId: "series-3-speech",
      path: "lessons/0003-演讲技巧学术表达.html",
      title: "演讲技巧与学术表达",
      subtitle: "Verbal/Vocal/Visual三要素与演讲结构设计",
      duration: "30 min",
      tags: ["演讲技巧"]
    },
    {
      id: "0004-KF-L1-矩阵特征值",
      collectionId: "kf-series-4-5",
      path: "lessons/0004-KF-L1-矩阵特征值.html",
      title: "KF L1：矩阵特征值、SVD与正定性",
      subtitle: "特征值几何意义、SVD分解、正定矩阵判据与Cholesky",
      duration: "45 min",
      tags: ["线性代数", "KF基础"]
    },
    {
      id: "0005a-KF-L2-矩阵求逆引理",
      collectionId: "kf-series-4-5",
      path: "lessons/0005a-KF-L2-矩阵求逆引理.html",
      title: "KF L2(上)：矩阵求逆引理",
      subtitle: "MIL标准形式、三步推导、几何直觉与KF用途预告",
      duration: "30 min",
      tags: ["线性代数", "KF基础"]
    },
    {
      id: "0005b-KF-L2-状态空间协方差",
      collectionId: "kf-series-4-5",
      path: "lessons/0005b-KF-L2-状态空间协方差.html",
      title: "KF L2(下)：状态空间与协方差",
      subtitle: "2D车辆建模、协方差矩阵、线性变换传播",
      duration: "30 min",
      tags: ["线性代数", "KF基础"]
    },
    {
      id: "0006-KF-L3-二次型优化",
      collectionId: "kf-series-6-7",
      path: "lessons/0006-KF-L3-二次型优化.html",
      title: "KF L3：二次型优化、稳定性与能控性",
      subtitle: "二次型优化、特征值稳定性、能控性矩阵",
      duration: "45 min",
      tags: ["KF基础", "能控性"]
    },
    {
      id: "0007-KF-L4-最小能量控制",
      collectionId: "kf-series-6-7",
      path: "lessons/0007-KF-L4-最小能量控制.html",
      title: "KF L4：最小能量控制、PBH与可观性",
      subtitle: "最小能量控制、PBH判据、系统可观性",
      duration: "45 min",
      tags: ["控制理论", "可观性"]
    },
    {
      id: "KF-L5-贝叶斯估计",
      collectionId: "kf-series-l5",
      path: "lessons/KF-L5-贝叶斯估计与BayesRule.html",
      title: "KF L5：贝叶斯估计与 Bayes Rule",
      subtitle: "先验/似然/后验、Bayes Rule、Romeo & Juliet经典例子",
      duration: "45 min",
      tags: ["估计理论"]
    },
    {
      id: "0008-KF-L6-MAP-MMSE",
      collectionId: "kf-series-9-11",
      path: "lessons/0008-KF-L6-MAP-MMSE.html",
      title: "KF L6：MAP、MMSE与假设检验",
      subtitle: "后验→点估计、MAP、MMSE、假设检验",
      duration: "45 min",
      tags: ["估计理论"]
    },
    {
      id: "0009-KF-L7-非贝叶斯估计",
      collectionId: "kf-series-9-11",
      path: "lessons/0009-KF-L7-非贝叶斯估计.html",
      title: "KF L7：非贝叶斯估计与最大似然",
      subtitle: "非贝叶斯框架、ML估计、MAP vs ML",
      duration: "45 min",
      tags: ["估计理论"]
    },
    {
      id: "0010-KF-L8-最小二乘正规方程",
      collectionId: "kf-series-9-11",
      path: "lessons/0010-KF-L8-最小二乘正规方程.html",
      title: "KF L8：最小二乘与正规方程",
      subtitle: "硬币ML、列空间、正规方程推导",
      duration: "45 min",
      tags: ["最小二乘"]
    },
    {
      id: "0011-KF-L9-最小二乘几何",
      collectionId: "kf-series-9-11",
      path: "lessons/0011-KF-L9-最小二乘几何.html",
      title: "KF L9：最小二乘几何与内积空间",
      subtitle: "正规方程投影解释、内积空间概念",
      duration: "45 min",
      tags: ["最小二乘"]
    },
    {
      id: "0012-KF-L10-投影定理",
      collectionId: "kf-series-9-11",
      path: "lessons/0012-KF-L10-投影定理.html",
      title: "KF L10：投影定理与随机最小二乘",
      subtitle: "投影定理证明、正交性、从MMSE到LMMSE",
      duration: "45 min",
      tags: ["投影定理"]
    },
    {
      id: "0013-KF-L11-LMMSE正交原理",
      collectionId: "kf-series-9-11",
      path: "lessons/0013-KF-L11-LMMSE正交原理.html",
      title: "KF L11：LMMSE与正交原理",
      subtitle: "线性估计器、正规方程、正交原理",
      duration: "45 min",
      tags: ["LMMSE"]
    },
    {
      id: "0014-KF-L12-LMMSE例子",
      collectionId: "kf-series-9-11",
      path: "lessons/0014-KF-L12-LMMSE例子.html",
      title: "KF L12：LMMSE例子与Gram-Schmidt",
      subtitle: "LMMSE典型例子、Gram-Schmidt正交化",
      duration: "45 min",
      tags: ["LMMSE"]
    },
    {
      id: "0015-KF-L13-递归估计",
      collectionId: "kf-series-9-11",
      path: "lessons/0015-KF-L13-递归估计.html",
      title: "KF L13：递归估计与新息过程",
      subtitle: "计算瓶颈、新息过程、递归估计形式",
      duration: "45 min",
      tags: ["递归估计"]
    },
    {
      id: "0016-KF-L14-KalmanFilter-1",
      collectionId: "kf-series-14",
      path: "lessons/0016-KF-L14-KalmanFilter-1.html",
      title: "KF L14(1/2)：系统模型与假设体系",
      subtitle: "KF系统模型、基本假设与符号体系",
      duration: "45 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0016-KF-L14-KalmanFilter-2",
      collectionId: "kf-series-14",
      path: "lessons/0016-KF-L14-KalmanFilter-2.html",
      title: "KF L14(2/2)：新息与Kalman增益推导",
      subtitle: "新息、Kalman Gain、状态/协方差更新",
      duration: "45 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0017-KF-L15-新息过程",
      collectionId: "kf-series-15",
      path: "lessons/0017-KF-L15-新息过程.html",
      title: "KF L15(1/2)：新息过程与正交性",
      subtitle: "新息定义、正交性证明、新息协方差",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0018-KF-L15-后验协方差更新",
      collectionId: "kf-series-15",
      path: "lessons/0018-KF-L15-后验协方差更新.html",
      title: "KF L15(2/2)：后验协方差完整推导",
      subtitle: "五个测量更新等式逐条几何证明",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0019-KF-L16-时间更新",
      collectionId: "kf-series-16",
      path: "lessons/0019-KF-L16-时间更新.html",
      title: "KF L16(1/2)：时间更新与收敛性",
      subtitle: "Time Update投影法证明、协方差收敛性",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0020-KF-L16-固定增益与传感器融合",
      collectionId: "kf-series-16",
      path: "lessons/0020-KF-L16-固定增益与传感器融合.html",
      title: "KF L16(2/2)：固定增益与传感器融合",
      subtitle: "固定增益估计器、信息形式KF、即插即用",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0021-KF-L17-条件高斯与MMSE",
      collectionId: "kf-series-17",
      path: "lessons/0021-KF-L17-条件高斯与MMSE.html",
      title: "KF L17(1/2)：条件高斯与MMSE",
      subtitle: "条件高斯定理、MMSE=LMMSE、分离原理",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0022-KF-L17-增益优化方法",
      collectionId: "kf-series-17",
      path: "lessons/0022-KF-L17-增益优化方法.html",
      title: "KF L17(2/2)：增益优化三种方法对比",
      subtitle: "Completion of Squares、三视角对比",
      duration: "30 min",
      tags: ["Kalman Filter"]
    },
    {
      id: "0023-北理工-扩散模型基础",
      collectionId: "special-bit",
      path: "lessons/0023-北理工-扩散模型基础.html",
      title: "北理工：生成式模型驱动具身智能",
      subtitle: "许佳玉 · BC局限性、DDPM、Flow Matching、MinFlow与IMF",
      duration: "30 min",
      tags: ["生成式", "具身智能"]
    },
    {
      id: "0025-E2Map-架构与经验场",
      collectionId: "special-e2map",
      path: "lessons/0025-E2Map-架构与经验场.html",
      title: "E2Map(1/2)：架构与经验场",
      subtitle: "导航地图进化、三层架构、经验场数学模型",
      duration: "30 min",
      tags: ["情绪地图"]
    },
    {
      id: "0026-E2Map-情绪场与自反导航",
      collectionId: "special-e2map",
      path: "lessons/0026-E2Map-情绪场与自反导航.html",
      title: "E2Map(2/2)：情绪场与自反导航",
      subtitle: "情绪场构建、代价函数、实验分析",
      duration: "30 min",
      tags: ["情绪地图"]
    },
    {
      id: "0027-KF-L18-动态规划基础",
      collectionId: "kf-series-18",
      path: "lessons/0027-KF-L18-动态规划基础.html",
      title: "KF L18(1/2)：动态规划基础",
      subtitle: "DP三要素、7-11库存控制、开环vs闭环",
      duration: "30 min",
      tags: ["动态规划"]
    },
    {
      id: "0028-KF-L18-Bellman方程",
      collectionId: "kf-series-18",
      path: "lessons/0028-KF-L18-Bellman方程.html",
      title: "KF L18(2/2)：Bellman方程",
      subtitle: "策略形式化、最优性原理、DP求解流程",
      duration: "30 min",
      tags: ["动态规划"]
    },
    {
      id: "0029-KF-L19-最优性原理",
      collectionId: "kf-series-19",
      path: "lessons/0029-KF-L19-最优性原理.html",
      title: "KF L19(1/2)：最优性原理与海盗分钻石",
      subtitle: "最优性原理表述、向后归纳、海盗分钻石经典案例",
      duration: "30 min",
      tags: ["动态规划", "博弈论"]
    },
    {
      id: "0030-KF-L19-DP算法",
      collectionId: "kf-series-19",
      path: "lessons/0030-KF-L19-DP算法.html",
      title: "KF L19(2/2)：DP算法与维度灾难",
      subtitle: "DP算法递推、最优策略提取、维度灾难与应对",
      duration: "30 min",
      tags: ["动态规划", "DP算法"]
    },
  ]
};
