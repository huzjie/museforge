# 训练信号设计

mock 后端只有一个旋钮 `skill ∈ [0,1]`，训练只是单调抬升它：

    score_memory  = (skill - 0.5) * 2 * is_correct + noise   (noise ∈ [0,1))
    try_subgoal   = skill >= threshold                         (threshold ∈ [0,1))
    persist       = skill >= threshold

## 为什么单调趋 1，而不是「对+1 错-1」

若用「对 +1 / 错 -1」的对称信号，skill 低（正确率 <50%）时期望漂移为负，skill 会被压到 0。
**恒正 delta** 保证 skill 单调爬向 1.0，记忆召回率与目标完成率随之单调上升，基准曲线干净可回归。

## 信号/噪声配比（boost 在 skill=0.5 时应为 0）

`score_memory` 用 `(skill-0.5)·2 · is_correct + noise`，noise 必须 ∈ `[0,1)`：
- skill=0.5 时 boost=0，纯随机 → recall@1 ≈ 1/n_candidates；
- skill=1.0 时 boost=1，正确项 ∈ [1,2]、错误项 ∈ [0,1]，恒胜出 → recall@1 = 1。

若误用 `skill·is_correct + noise`（skill=0.5 时 boost 恒为 0.5），正确项就 ∈ [0.5,1.5]，
recall@1 直接 ~0.6，曲线起点过高、区分度差。**关键：boost 在 skill=0.5 时应恰为 0。**
