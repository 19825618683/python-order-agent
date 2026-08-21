# Python 订单 Agent

这是 Python AI Agent 主线项目。

## 运行准备

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

在 `.env` 中填写 `DEEPSEEK_API_KEY`，不要把 `.env` 提交到 Git。

运行：

```bash
python agent.py
```

当前 Agent 流程：

```text
用户问题 → DeepSeek 判断需要的工具 → Python 执行订单工具 → 工具结果交回模型 → 模型生成回答
```
