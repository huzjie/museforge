# Active Focus（主动专注）技术拆解

## 问题

衡量智能体能否围绕一个困难目标持续推进、遇到卡点尝试替代路径、适应新信息，而不是轻易放弃。

## 四步循环

1. **分解（Planner）**：把目标拆成有序子目标。参考实现按目标文本 md5 确定性拆出 3..max 个子目标
   （用固定动词表），保证同一目标两次拆解一致、可测试。

2. **追踪（Tracker）**：`progress = 已完成子目标 / 总子目标`。

3. **障碍检测（DifficultyDetector）**：连续 `staleness_threshold` 次尝试无进展且有过失败 → 判定
   `is_stuck`；`difficulty = failures / attempts`（0..1）。

4. **探索（Explorer）**：卡住时给出 `max_alternatives` 条确定性替代路径 + 一次「重述目标」。

## 专注度标量

    focus = 0.5·progress + 0.3·persistence + 0.2·adaptivity
    persistence = 1 - difficulty
    adaptivity = 卡住时是否尝试过替代路径（完成即 1）

## 可复用要点

- 把「坚持/放弃」变成**可测的布尔决策**（`persist_after_failure`），而不是模糊的意志力描述。
- 卡点检测用**「连续无进展」计数**，比单次失败更鲁棒（一次失败可能是正常噪声）。
- 替代路径要**确定性可生成**，才能在基准里复现、在真实系统里审计。
