# Active Memory（主动记忆）技术拆解

## 问题

把整段对话历史塞进 prompt 会随会话变长而爆炸。个人智能体需要**跨会话**记住用户的关键上下文
（事实、偏好、决定），并在**每个回合主动**只取与当前查询相关的那部分。

## 拆成四个可复用组件

1. **编码（Encoder）**：文本 → 向量。参考实现用 `md5(text)` 前 8 字节做种子驱动 `random.Random`
   生成单位伪随机向量——零依赖且可复现。生产直接换真实句向量模型。

2. **打分（Scorer）**，加权和而非单一余弦：

        score = w_rel·relevance + w_rec·recency + w_imp·importance + w_freq·freq
        relevance = (cosine(q_emb, m_emb) + 1) / 2
        recency   = exp(-age / half_life)
        freq      = log(1 + access_count) / (log(1 + access_count) + 1)

   权重默认 `0.5 / 0.2 / 0.2 / 0.1`，全部可在 config 里调。

3. **检索（Retriever）**：按 score 排序取 top-k，并在 token 预算内累计。**检索即复用**——被取中的
   记忆 `access_count += 1`，下一轮频次权重上升，形成「越常用越靠前」的正反馈。

4. **巩固（Consolidator）**：当 episodic 缓冲超过阈值，把最旧的一半蒸馏成 compact 的 semantic
   事实，控制长期上下文增长。

## 可复用要点

- 别把「全量历史」当记忆，**按相关度做 top-k 检索**才是主动记忆的核心。
- 打分要**多信号**：纯余弦相似度在语义接近时会召回一堆噪声。
- 用**确定性种子**做参考嵌入，保证基准可复现、可回归。
