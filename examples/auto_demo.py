"""
自动演示脚本 — 展示 AI Agent 的 Function Calling 能力
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from openai import OpenAI
from tools import TOOL_DEFINITIONS, call_tool
import json
import time
import config

client = OpenAI(
    api_key=config.API_KEY,
    base_url=config.BASE_URL
)

SYSTEM_PROMPT = "你是一个智能助手，可以使用工具来回答问题。"


def run_agent(user_message: str):
    """运行 AI Agent 并打印完整过程"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_message},
    ]

    print(f"\n{'='*55}")
    print(f"👤 用户: {user_message}")
    print(f"{'='*55}")

    start = time.time()

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages,
        tools=TOOL_DEFINITIONS,
        tool_choice="auto",
    )

    reply = response.choices[0].message

    if reply.tool_calls:
        # ★ 先把 AI 回复（含 tool_calls）加入消息列表 — 只需要加一次！
        messages.append(reply)

        # 依次执行每个工具
        for tool_call in reply.tool_calls:
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)
            print(f"   🤖 AI 决定调用 → [{func_name}({func_args})]")

            result = call_tool(func_name, func_args)
            print(f"   🔧 工具返回 → {result}")

            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result,
            })

        final = client.chat.completions.create(
            model="deepseek-chat",
            messages=messages,
        )
        final_answer = final.choices[0].message.content
    else:
        final_answer = reply.content

    elapsed = time.time() - start
    print(f"🤖 AI 回答（{elapsed:.1f}s）: {final_answer}")


# ============================================================
# 测试用例
# ============================================================
test_questions = [
    "今天是几号？",                                # → 调 get_current_time
    "北京今天天气怎么样？",                        # → 调 get_weather
    "帮我算一下 258 × 37 等于多少？",             # → 调 calculator
    "Hello! 介绍一下你自己。",                     # → 不调工具，直接回答
    "上海天气怎么样？明天是几号？帮我算 1024÷8",  # → 连续调多个工具！
]

if __name__ == "__main__":
    print("🌟 AI Agent Function Calling 自动演示")
    print(f"共 {len(test_questions)} 个测试\n")

    for i, q in enumerate(test_questions, 1):
        run_agent(q)
        if i < len(test_questions):
            print("\n⏳ 等待2秒再试下一个...\n")
            time.sleep(2)

    print(f"\n{'='*55}")
    print("✅ 演示完成！")
    print("看到了吗？AI 遇到需要工具的问题时，会：")
    print("  1. 识别出需要用什么工具")
    print("  2. 调用工具获取结果")
    print("  3. 基于工具结果生成精准回答")
