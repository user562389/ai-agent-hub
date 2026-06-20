"""
Function Calling 演示 — AI 如何调用工具
单独跑这个文件，看 AI Agent 的工作流程
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from openai import OpenAI
from tools import TOOL_DEFINITIONS, call_tool
import json
import config

client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

SYSTEM_PROMPT = "你是一个智能助手，可以使用工具来回答问题。"


def run_agent(user_message: str) -> str:
    """运行 AI Agent — 自动决定是否调用工具"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    print(f"\n{'='*50}")
    print(f"👤 用户: {user_message}")
    print(f"{'='*50}")

    # 第1步：调用 API，告诉 AI 有哪些工具可用
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOL_DEFINITIONS,  # ← ★ 这就是 Function Calling 的关键！
        tool_choice="auto",       # ← AI 自己决定要不要用工具
    )

    reply = response.choices[0].message

    # 第2步：如果 AI 想调用工具
    if reply.tool_calls:
        # ★ 先把 AI 回复（含 tool_calls）加入消息列表 — 只需要加一次！
        messages.append(reply)

        for tool_call in reply.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"\n🤖 AI 决定调用工具: [{func_name}]")
            print(f"   参数: {func_args}")

            # 第3步：执行工具
            result = call_tool(func_name, func_args)
            print(f"🔧 工具返回: {result}")

            # 把工具结果送回给 AI，让它生成最终回答
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        # 第5步：AI 基于工具结果给出最终回答
        final = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        final_answer = final.choices[0].message.content
    else:
        # AI 直接回答了（不需要工具）
        final_answer = reply.content

    print(f"\n🤖 AI: {final_answer}")
    return final_answer


# ============================================================
# 运 行
# ============================================================
if __name__ == "__main__":
    print("🧪 AI Agent Function Calling 演示")
    print("输入你的问题（输入 'q' 退出）\n")

    while True:
        user_input = input("👤 > ")
        if user_input.lower() in ("q", "quit", "exit"):
            break
        if not user_input.strip():
            continue
        run_agent(user_input)
