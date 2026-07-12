# 课程内容准确性审查报告

## 审查范围
- 0003-演讲技巧学术表达.html
- 0017-KF-L15-新息过程.html / 0018-KF-L15-后验协方差更新.html
- 0019-KF-L16-时间更新.html / 0020-KF-L16-固定增益与传感器融合.html
- 0021-KF-L17-条件高斯与MMSE.html / 0022-KF-L17-增益优化方法.html
- 0027-KF-L18-动态规划基础.html / 0028-KF-L18-Bellman方程.html
- KF-L5-贝叶斯估计与BayesRule.html

---

## 1. 0003 - 演讲技巧与学术表达

**评分: ✅ 无误**

对照板书 (`20251115_施凌_研讨会系列3_演讲技巧 md文档/document.md`)，HTML 内容准确涵盖了：
- Verbal/Vocal/Visual 三要素及细则
- 三段式演讲结构（Tell them → Say it → Tell them）
- 幻灯片设计原则
- Q&A 应答技巧
- 李开复 10 句箴言（与板书一一对应）
- 参考改写例句准确

板书中的 "Overcoming Language Barrier" 和 "Hiding Nervousness" 章节是授课现场的延伸，HTML 中未单独成节，但其核心内容已融入其他章节的讲解中，不算遗漏。无数学公式错误风险。

---

## 2. 0017 - KF-L15: 新息过程

**评分: ✅ 无误**

对照板书 (`20260517_施凌_研讨会系列18_KF_L15 md文档/document.md`)，验证了以下关键公式：

### 公式 ①: 新息定义
$$e_k = y_k - C \hat x_{k|k-1}$$ ✅

### 公式 ②: 新息协方差
$$R_{e,k} = C P_{k|k-1} C' + R$$ ✅

### 空间包含关系
- $\mathcal{L}_k \subset \text{span}\{x_0, w_0, \dots, w_{k-1}; v_0, \dots, v_k\}$ ✅
- $\mathcal{L}_{k-1} \subset \text{span}\{x_0, w_0, \dots, w_{k-2}; v_0, \dots, v_{k-1}\}$ ✅
- $v_k \perp \mathcal{L}_{k-1}$ ✅

### Gram-Schmidt 正交化与新息的对应关系
板书通过投影法推导 e_k，HTML 的推导（第 148-205 行）与板书完全一致。无错误。

---

## 3. 0018 - KF-L15: 后验协方差更新

**评分: ✅ 无误**

对照同一份板书，验证了以下关键公式：

### 公式 ③-④: 状态更新与 Kalman 增益
$$\hat x_{k|k} = \hat x_{k|k-1} + K_k e_k, \quad K_k = P_{k|k-1} C' R_{e,k}^{-1}$$ ✅

### 公式 ⑤: 后验协方差
$$P_{k|k} = P_{k|k-1} - P_{k|k-1} C' R_{e,k}^{-1} C P_{k|k-1}$$ ✅

### 交叉协方差
$$\langle x_k, e_k \rangle = P_{k|k-1} C'$$ ✅

### 紧凑形式
$$P_{k|k} = (I - K_k C) P_{k|k-1}$$ ✅
$$P_{k|k}^{-1} = P_{k|k-1}^{-1} + C' R^{-1} C$$ ✅（矩阵求逆引理）

第 248-288 行的完整推导与板书一致，Completion of Squares 验证正确。

---

## 4. 0019 - KF-L16: 时间更新

**评分: ✅ 无误**

对照板书 (`20260523_施凌_研讨会系列19_KF_L16 md文档/document.md`)，验证：

### 公式 ⑥-⑦: 时间更新
$$\hat x_{k+1|k} = A \hat x_{k|k}$$ ✅
$$P_{k+1|k} = A P_{k|k} A' + Q$$ ✅

### 收敛条件
- $(A, C)$ 可观 ✅
- $(A, \sqrt{Q})$ 能控 ✅
板书明确写明 "Yes when (A, C) is observable & (A, sqrt(Q)) is controllable" ✅

### 固定增益估计器
板书提到 $P_{k|k} \to \bar P \Rightarrow k_k \to k^*$，HTML 第 302-308 行展示了收敛后的 LTI 形式，正确。 ✅

---

## 5. 0020 - KF-L16: 固定增益与传感器融合

**评分: ✅ 无误**

对照同一份板书，验证：

### 固定增益估计器
$$\hat x_{k+1|k} = A \hat x_{k|k-1} + K^* [y_k - C \hat x_{k|k-1}]$$ ✅

### 代数 Riccati 方程 (ARE)
$$\bar P = A \bar P A' - A \bar P C' [C \bar P C' + R]^{-1} C \bar P A' + Q$$ ✅

### 信息形式的 KF
$$\Omega_{k|k} = \Omega_{k|k-1} + C' R^{-1} C$$ ✅
$$\xi_{k|k} = \xi_{k|k-1} + C' R^{-1} y_k$$ ✅

### 传感器融合（即插即用）
板书写明 "plug & play"，HTML 的多传感器累加公式正确：
$$\Omega_{k|k} = \Omega_{k|k-1} + \sum_i C_i' R_i^{-1} C_i$$ ✅
$$\xi_{k|k} = \xi_{k|k-1} + \sum_i C_i' R_i^{-1} y_k^i$$ ✅

板书末尾的 MMSE vs LMMSE 预览已在 HTML 第 6 节（"从几何到概率的过渡"）中正确承接。

---

## 6. 0021 - KF-L17: 条件高斯与 MMSE

**评分: ✅ 无误**

对照板书 (`20260530_施凌_研讨会系列20_KF_L17 md文档/document.md`)，验证：

### 条件高斯定理
$$\mu_{x|y=y} = \bar x + \Sigma_{xy} \Sigma_y^{-1} (y - \bar y)$$ ✅
$$\Sigma_{x|y=y} = \Sigma_x - \Sigma_{xy} \Sigma_y^{-1} \Sigma_{yx}$$ ✅

### 系统模型（含控制输入）
$$x_{k+1} = A x_k + B u_k + w_k$$ ✅
$$y_k = C x_k + v_k$$ ✅

### 符号体系
- $\hat x_{k|k} = E[x_k | Y_k, U_{k-1}]$ ✅
- $\hat x_{k|k-1} = E[x_k | Y_{k-1}, U_{k-1}]$ ✅

### 概率法时间更新
$$\hat x_{k|k-1} = A \hat x_{k-1|k-1} + B u_{k-1}$$ ✅
$$P_{k|k-1} = A P_{k-1|k-1} A' + Q$$ ✅

### MMSE = LMMSE 等价性证明
板书明确写出 "MMSE = LMMSE for linear Gaussian systems" ✅
HTML 第 6 节的证明思路正确。

---

## 7. 0022 - KF-L17: 增益优化方法

**评分: ✅ 无误**

对照同一份板书，验证：

### 优化问题设定
$$\hat X_k = A \hat X_{k-1} + K_k (y_k - C A \hat X_{k-1}), \quad \hat X_0 = 0$$ ✅

### 误差协方差二次型表达
板书留作练习（"take home exercise: 把 P_k 表示成 K_k 的函数"），HTML 完整推导：
$$P_{k+1}(K) = (I - K C) P_{k+1|k} (I - K C)' + K R K'$$ ✅

### Completion of Squares
HTML 第 200-228 行的配方法推导正确。最优增益：
$$K_{k+1}^* = P_{k+1|k} C' [C P_{k+1|k} C' + R]^{-1}$$ ✅

---

## 8. 0027 - KF-L18: 动态规划基础

**评分: ✅ 无误**

对照板书 (`20260627_施凌_研讨会系列23_KF_L18/document.md`)，验证：

### 基本问题 (P1) 的两个要素
① 离散时间动态系统: $x_{k+1} = f_k(x_k, u_k, w_k)$ ✅
② 累加代价函数: $J = \mathbb{E}\{g_N(x_N) + \sum_{k=0}^{N-1} g_k(x_k, u_k, w_k)\}$ ✅

### 7-11 便利店库存控制
$$x_{k+1} = x_k + u_k - w_k$$ ✅
$$J = \mathbb{E}\{R(x_N) + \sum [r(x_k) + cu_k - \beta w_k]\}$$ ✅

### 开环 vs 闭环控制
板书对比了离线策略（open-loop）和在线策略（$u_k = \mu_k(x_k)$），HTML 第 227-261 行描述准确 ✅

---

## 9. 0028 - KF-L18: Bellman 方程

**评分: ✅ 无误**

对照同一份板书（该板书仅覆盖到策略定义 $\pi = \{\mu_0, \dots, \mu_{N-1}\}$），验证：

注意：板书仅 61 行，内容覆盖到策略定义。Bellman 方程、最优性原理、DP 求解流程等是板书的自然延伸和详细展开。以下数学内容经独立验证正确：

### 策略定义
$$\pi = \{\mu_0, \mu_1, \dots, \mu_{N-1}\}$$ ✅

### Bellman 最优性原理
表述正确："An optimal policy has the property that whatever the initial state and initial decision are, the remaining decisions must constitute an optimal policy..." ✅

### Bellman 方程
$$V_k(x_k) = \min_{u_k} \mathbb{E}_{w_k}[g_k(x_k, u_k, w_k) + V_{k+1}(f_k(x_k, u_k, w_k))]$$ ✅
$$V_N(x_N) = g_N(x_N)$$ ✅

### DP 求解流程
初始化 → 反向递推 → 提取策略 → 正向执行 ✅

### 维度灾难讨论
准确描述了状态空间指数增长问题及其常用应对方法 ✅

---

## 10. KF-L5 - 贝叶斯估计与 Bayes Rule

**评分: ✅ 无误**

对照板书 (`20251227_施凌_研讨会系列8_KF_L5 md文档/document.md`)，验证：

### Bayesian vs Non-Bayesian
两种框架的对比（θ 为随机变量 vs 固定常数）与板书一致 ✅

### 房间温度例子
$$Y = \theta + v, \quad v \sim N(0, 1)$$ ✅

### Bayes Rule 四种形式
- 离散 θ + 离散 X ✅
- 离散 θ + 连续 X ✅
- 连续 θ + 离散 X ✅
- 连续 θ + 连续 X ✅

### 抽奖号码例子
6 位中奖号码（000000-999999），逐位缩小候选空间 ✅

### Romeo & Juliet 例题
$$f(\theta) = 1, \quad 0 \le \theta \le 1$$ ✅
$$f(x|\theta) = 1/\theta, \quad 0 \le x \le \theta$$ ✅
$$f(\theta|x) = \frac{1}{\theta |\log x|}, \quad x \le \theta \le 1$$ ✅
数学推导验证：分母 $\int_x^1 1/\theta' d\theta' = \ln(1) - \ln(x) = |\ln x|$ ✅

极值情况 $x=1 \Rightarrow \theta=1$ ✅

---

# 总结

| 课程 | 评分 | 备注 |
|------|------|------|
| 0003 - 演讲技巧与学术表达 | ✅ 无误 | 通识课，无数学公式 |
| 0017 - KF-L15: 新息过程 | ✅ 无误 | ①②公式推导正确 |
| 0018 - KF-L15: 后验协方差更新 | ✅ 无误 | ③④⑤公式推导正确 |
| 0019 - KF-L16: 时间更新 | ✅ 无误 | ⑥⑦公式 + 收敛性正确 |
| 0020 - KF-L16: 固定增益与传感器融合 | ✅ 无误 | ARE、信息形式、融合正确 |
| 0021 - KF-L17: 条件高斯与 MMSE | ✅ 无误 | 条件高斯 + MMSE=LMMSE 正确 |
| 0022 - KF-L17: 增益优化方法 | ✅ 无误 | Completion of Squares 推导正确 |
| 0027 - KF-L18: 动态规划基础 | ✅ 无误 | DP 三要素 + 7-11 例子正确 |
| 0028 - KF-L18: Bellman 方程 | ✅ 无误 | Bellman 方程正确（独立验证） |
| KF-L5 - 贝叶斯估计与 Bayes Rule | ✅ 无误 | Bayes Rule 四种形式 + Romeo&Juliet 推导正确 |

**全部 10 门课程审查通过，未发现内容错误或公式错误。**
