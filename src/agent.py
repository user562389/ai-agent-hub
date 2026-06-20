"""
AI Agent 核心逻辑 — 对话 + 工具调用
"""
from openai import OpenAI
from . import config
from .tools import TOOL_DEFINITIONS, call_tool
import json


client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)


def chat_with_ai(message: str, history: list, use_tools: bool = True) -> str:
    """
    发送消息给 AI，自动决定是否调用工具

    参数:
        message: 用户消息
        history: 历史对话 [(user_msg, ai_msg), ...]
        use_tools: 是否启用工具调用
    """
    messages = [{"role": "system", "content": config.SYSTEM_PROMPT}]

    # 加载历史对话
    for user_msg, ai_msg in history:
        messages.append({"role": "user", "content": user_msg})
        messages.append({"role": "assistant", "content": ai_msg})

    messages.append({"role": "user", "content": message})

    # 第1步：调用 API，传入工具定义
    response = client.chat.completions.create(
        model=config.MODEL,
        messages=messages,
        tools=TOOL_DEFINITIONS if use_tools else None,
        tool_choice="auto" if use_tools else None,
    )

    reply = response.choices[0].message

    # 第2步：如果 AI 想调用工具
    if reply.tool_calls:
        # ★ 先把 AI 的回复（含 tool_calls）加入消息列表 — 只需要加一次！
        messages.append(reply)

        # 依次执行每个工具调用
        for tool_call in reply.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            # 执行工具
            result = call_tool(func_name, func_args)

            # 把工具结果送回 AI
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        # 第3步：AI 基于工具结果给出最终回答
        final = client.chat.completions.create(
            model=config.MODEL,
            messages=messages,
        )
        return final.choices[0].message.content
    else:
        # AI 直接回答了（不需要工具）
        return reply.content
