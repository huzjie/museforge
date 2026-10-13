# 专注度打分提示词

评估智能体当前推进状态，输出 JSON：
{"progress": 0-1, "is_stuck": true/false, "should_escalate": true/false, "reason": "一句话"}

目标：{goal}
已完成：{completed}/{total}
最近失败：{recent_failures}
