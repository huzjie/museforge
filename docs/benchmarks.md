# 基准

## 记忆基准（memory_bench）

对 50 个确定性 query、每个 10 个候选（恰 1 个正确），用后端 `rank_memories` 排序，报：

- `recall@1`：正确候选排第 1 的比例
- `recall@5`：正确候选进前 5 的比例
- `MRR`：平均倒数排名

skill 0.5 → 1.0 时三项单调上升（recall@1 由 ~0.1 到 1.0）。

## 专注基准（focus_bench）

对 30 个确定性目标、每个 6 个子目标、预算 30 次尝试，报：

- `goal_completion_rate`：完整完成的目标比例
- `avg_progress`：平均进度
- `give_up_rate` / `persistence`：中途放弃比例 / 坚持度

skill 0.5 → 1.0 时完成率与坚持度单调上升。

## 复现

    python -m museforge.cli bench
