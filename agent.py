import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from order_tools import get_order_summary, get_order_by_id
TOOL_HANDLERS = {
    "get_order_summary": get_order_summary,
    "get_order_by_id": get_order_by_id,
}

load_dotenv()

api_key = os.getenv("DEEPSEEK_API_KEY")
if not api_key:
    raise RuntimeError("未找到 DEEPSEEK_API_KEY。请在 .env 文件中配置，且不要提交该文件。")

client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com",
)

SYSTEM_PROMPT = "你是订单助手。只要用户询问订单统计，必须调用工具，不能编造数据。“不少于”“不小于”和“>=”都表示金额大于或等于门槛；例如“金额不小于200元”必须调用 get_order_summary，并传入 minimum_amount=200。"

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_order_summary",
            "description": "统计金额不少于指定门槛的订单。",
            "parameters": {
                "type": "object",
                "properties": {
                    "minimum_amount": {
                        "type": "number",
                        "description": "订单金额门槛。",
                    }
                },
                "required": ["minimum_amount"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_order_by_id",
            "description": "根据订单编号查询单笔订单。",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "订单编号。",
                    }
                },
                "required": ["order_id"],
            },
        },
    },
]


def ask_agent(user_question: str) -> str:
    """处理一个订单问题，并返回模型的最终回答。"""
    response = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_question},
        ],
        tools=TOOLS,
    )

    assistant_message = response.choices[0].message
    if not assistant_message.tool_calls:
        return assistant_message.content or "暂时没有得到回答。"

    print("模型选择的工具：", assistant_message.tool_calls[0].function.name)
    print("模型提供的参数：", assistant_message.tool_calls[0].function.arguments)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_question},
        assistant_message.model_dump(exclude_none=True),
    ]

    for tool_call in assistant_message.tool_calls:
        arguments = json.loads(tool_call.function.arguments)
        tool_handler = TOOL_HANDLERS.get(tool_call.function.name)
        if tool_handler is None:
            raise ValueError(f"未知工具：{tool_call.function.name}")

        tool_result = tool_handler(**arguments)
        messages.append(
            {
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": json.dumps(tool_result, ensure_ascii=False),
            }
        )

    final_response = client.chat.completions.create(
        model=os.getenv("DEEPSEEK_MODEL", "deepseek-v4-flash"),
        messages=messages,
        tools=[],
    )
    return final_response.choices[0].message.content or "暂时没有得到回答。"


if __name__ == "__main__":
    user_question = input("请输入订单问题：")
    print(ask_agent(user_question))
