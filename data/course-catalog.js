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
      id: "kf-series-4-8",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L1-L5：矩阵基础与贝叶斯估计",
      subtitle: "Kalman Filter 入门系列 (L1-L5)",
      description: "第 0004-0005 课（已发布）。从矩阵特征值、SVD 到状态空间与协方差，打下 KF 理论基础。",
      quickOpen: "lessons/0004-KF-L1-矩阵特征值.html",
      meta: ["5 节课", "~6 小时", "矩阵理论 / 贝叶斯"]
    },
    {
      id: "kf-series-9-11",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L6-L9：估计理论与最小二乘",
      subtitle: "Kalman Filter 进阶系列 (L6-L9)",
      description: "第 0006-0011 课。MAP、MMSE、最大似然、最小二乘与内积空间。",
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
      id: "special-bit",
      groupId: "seminars",
      kind: "特邀分享",
      title: "北理工分享：生成式模型驱动具身智能",
      subtitle: "特邀分享",
      description: "第 0020 课。北京理工大学特邀分享——生成式模型如何驱动具身动作生成。",
      quickOpen: "lessons/0020-北理工-生成式具身智能.html",
      meta: ["1 节课", "~40 分钟", "具身智能 / 生成式"]
    },
    {
      id: "special-e2map",
      groupId: "seminars",
      kind: "组内分享",
      title: "E2Map：经验-情绪地图与自反式导航",
      subtitle: "张健强 · 组内分享",
      description: "第 0021 课。E2Map——让机器人拥有记忆和情感的建图范式。",
      quickOpen: "lessons/0021-E2Map-经验情绪地图.html",
      meta: ["1 节课", "~35 分钟", "情绪地图 / 导航"]
    },
    {
      id: "kf-series-18",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L18：动态规划入门与库存控制",
      subtitle: "Kalman Filter 延伸系列 (L18)",
      description: "第 0022 课。动态规划（DP）入门——离散时间动态系统、累加代价函数、7-11 库存控制例子、开环 vs 闭环策略。",
      quickOpen: "lessons/0022-KF-L18-动态规划入门.html",
      meta: ["1 节课", "~45 分钟", "动态规划 / 库存控制"]
    },
    {
      id: "kf-series-15-17",
      groupId: "seminars",
      kind: "KF 系列",
      title: "KF L15-L17：测量更新证明、概率方法与增益优化",
      subtitle: "Kalman Filter 深入系列 (L15-L17)",
      description: "第 0017-0019 课。新息与后验协方差证明、时间更新与固定增益、MMSE 等价性与优化方法。",
      quickOpen: "lessons/0017-KF-L15-新息测量更新.html",
      meta: ["3 节课", "~3 小时", "测量更新 / 优化"]
    }
  ],
  lessons: [
    {
      id: "0000-图像算法安防应用",
      collectionId: "yang-xicheng",
      title: "图像算法在安防行业的应用",
      subtitle: "人脸识别、目标检测与工程落地",
      path: "lessons/0000-图像算法安防应用.html",
      duration: "30 min",
      meta: ["杨熙丞", "特邀分享"]
    },
    {
      id: "0001-研究共同体方向地图",
      collectionId: "series-1-2",
      title: "研究共同体与方向地图",
      subtitle: "看懂不同研究方向之间的联系",
      path: "lessons/0001-研究共同体方向地图.html",
      duration: "45 min",
      meta: ["研讨会系列1", "研究导论"]
    },
    {
      id: "0002-学术规范职业习惯",
      collectionId: "series-1-2",
      title: "组规、学术规范与职业习惯",
      subtitle: "学术诚信、守时、邮件礼仪与 AI 工具使用",
      path: "lessons/0002-学术规范职业习惯.html",
      duration: "45 min",
      meta: ["研讨会系列2", "学术规范"]
    },
    {
      id: "0003-演讲技巧学术表达",
      collectionId: "series-3-speech",
      title: "演讲技巧与学术表达",
      subtitle: "从结构设计到 Q&A 处理",
      path: "lessons/0003-演讲技巧学术表达.html",
      duration: "45 min",
      meta: ["研讨会系列3", "演讲技巧"]
    },
    {
      id: "0004-KF-L1-矩阵特征值",
      collectionId: "kf-series-4-8",
      title: "KF L1：矩阵特征值、SVD 与正定性",
      subtitle: "Kalman Filter 的线性代数基础",
      path: "lessons/0004-KF-L1-矩阵特征值.html",
      duration: "60 min",
      meta: ["KF L1", "线性代数"]
    },
    {
      id: "0005-KF-L2-矩阵求逆状态空间",
      collectionId: "kf-series-4-8",
      title: "KF L2：矩阵求逆引理、状态空间与协方差",
      subtitle: "状态空间模型与协方差传播",
      path: "lessons/0005-KF-L2-矩阵求逆状态空间.html",
      duration: "60 min",
      meta: ["KF L2", "状态空间"]
    },
    {
      id: "0012-KF-L10-投影定理",
      collectionId: "kf-series-10-13",
      title: "KF L10：投影定理与随机最小二乘",
      subtitle: "从内积空间投影到 MMSE 与 LMMSE",
      path: "lessons/0012-KF-L10-投影定理.html",
      duration: "45 min",
      meta: ["KF L10", "投影定理"]
    },
    {
      id: "0013-KF-L11-LMMSE正交原理",
      collectionId: "kf-series-10-13",
      title: "KF L11：线性最小均方估计与正交原理",
      subtitle: "LMMSE 正规方程与正交原理",
      path: "lessons/0013-KF-L11-LMMSE正交原理.html",
      duration: "45 min",
      meta: ["KF L11", "LMMSE"]
    },
    {
      id: "0014-KF-L12-LMMSE例子",
      collectionId: "kf-series-10-13",
      title: "KF L12：LMMSE 例子、Gram-Schmidt 与三类估计问题",
      subtitle: "LMMSE 应用、Gram-Schmidt、Smoothing/Filtering/Prediction",
      path: "lessons/0014-KF-L12-LMMSE例子.html",
      duration: "60 min",
      meta: ["KF L12", "Gram-Schmidt"]
    },
    {
      id: "0015-KF-L13-递归估计",
      collectionId: "kf-series-10-13",
      title: "KF L13：递归估计与新息过程",
      subtitle: "新息过程如何让递归计算成为可能",
      path: "lessons/0015-KF-L13-递归估计.html",
      duration: "45 min",
      meta: ["KF L13", "新息过程"]
    },
    {
      id: "0016-KF-L14-KalmanFilter-1",
      collectionId: "kf-series-14",
      title: "KF L14：Kalman Filter 模型、假设与符号体系 (1/2)",
      subtitle: "系统模型、基本假设、估计记号、递归结构",
      path: "lessons/0016-KF-L14-KalmanFilter-1.html",
      duration: "45 min",
      meta: ["KF L14", "模型假设"]
    },
    {
      id: "0016-KF-L14-KalmanFilter-2",
      collectionId: "kf-series-14",
      title: "KF L14：Kalman Filter 测量更新详解 (2/2)",
      subtitle: "新息、Kalman Gain、误差协方差更新、完整 KF 算法",
      path: "lessons/0016-KF-L14-KalmanFilter-2.html",
      duration: "45 min",
      meta: ["KF L14", "测量更新"]
    },
    {
      id: "0017-KF-L15-新息测量更新",
      collectionId: "kf-series-15-17",
      title: "KF L15：从新息到后验协方差的完整测量更新推导",
      subtitle: "五个核心等式的几何证明",
      path: "lessons/0017-KF-L15-新息测量更新.html",
      duration: "45 min",
      meta: ["KF L15", "测量更新"]
    },
    {
      id: "0018-KF-L16-时间更新增益",
      collectionId: "kf-series-15-17",
      title: "KF L16：时间更新、固定增益与传感器融合",
      subtitle: "Time Update 证明、P_k 收敛性与多传感器融合",
      path: "lessons/0018-KF-L16-时间更新增益.html",
      duration: "45 min",
      meta: ["KF L16", "时间更新"]
    },
    {
      id: "0019-KF-L17-MMSE增益优化",
      collectionId: "kf-series-15-17",
      title: "KF L17：线性高斯下 MMSE 等价与 Kalman 增益优化",
      subtitle: "概率法推导 + 优化法求解 K_k",
      path: "lessons/0019-KF-L17-MMSE增益优化.html",
      duration: "45 min",
      meta: ["KF L17", "MMSE"]
    },
    {
      id: "0020-北理工-生成式具身智能",
      collectionId: "special-bit",
      title: "北理工分享：生成式模型驱动具身动作生成",
      subtitle: "DDPM、Flow Matching、MinFlow 在机器人模仿学习中的应用",
      path: "lessons/0020-北理工-生成式具身智能.html",
      duration: "40 min",
      meta: ["北理工", "生成式模型"]
    },
    {
      id: "0021-E2Map-经验情绪地图",
      collectionId: "special-e2map",
      title: "E2Map：经验-情绪地图与自反式导航",
      subtitle: "让机器人拥有记忆和情感的建图范式",
      path: "lessons/0021-E2Map-经验情绪地图.html",
      duration: "35 min",
      meta: ["张健强", "情绪地图"]
    },
    {
      id: "0022-KF-L18-动态规划入门",
      collectionId: "kf-series-18",
      title: "KF L18：动态规划入门与库存控制例子",
      subtitle: "DP 基础、7-11 库存控制、开环 vs 闭环策略",
      path: "lessons/0022-KF-L18-动态规划入门.html",
      duration: "45 min",
      meta: ["KF L18", "动态规划"]
    }
  ]
};
