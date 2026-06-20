"""
AI Agent Hub — 多功能 AI 智能助手
带 Function Calling + 长记忆系统的 Gradio 网页界面
"""
import sys
import os

# 确保能导入 src 模块
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import gradio as gr
from agent import chat_with_ai
import memory

# ============================================================
#  样 式（苹果风蓝色气泡）
# ============================================================
CSS = """
footer {display:none !important}
.gradio-container {max-width: 100% !important; min-height: 100vh !important; margin: 0 !important; padding: 0 !important; background: #f5f5f7 !important;}

/* 气泡消息通用 */
.message {
    padding: 16px 22px !important;
    font-size: 17px !important;
    line-height: 1.7 !important;
    border-radius: 20px !important;
    margin: 6px 0 !important;
    max-width: 80% !important;
    word-wrap: break-word !important;
}
/* 用户气泡 — 右对齐，苹果蓝 */
.message.user {
    background: #007aff !important;
    color: white !important;
    margin-left: auto !important;
    border-bottom-right-radius: 4px !important;
}
/* AI 气泡 — 左对齐，白色 */
.message.bot {
    background: #ffffff !important;
    color: #1d1d1f !important;
    border: 1px solid #e8e8ed !important;
    border-bottom-left-radius: 4px !important;
}

/* 输入框 — 大圆角 */
textarea, input[type="text"], input[type="search"], select {
    background: #ffffff !important;
    border: 1px solid #e8e8ed !important;
    border-radius: 28px !important;
    padding: 14px 22px !important;
    font-size: 17px !important;
    outline: none !important;
    box-shadow: none !important;
}
textarea:focus, input:focus {
    border-color: #007aff !important;
    box-shadow: 0 0 0 3px rgba(0,122,255,0.15) !important;
}

/* 按钮 */
button {
    border-radius: 28px !important;
    font-weight: 500 !important;
    border: none !important;
    padding: 10px 24px !important;
    font-size: 15px !important;
    transition: all 0.2s !important;
}
button:hover { opacity: 0.85 !important; }
button.primary { background: #007aff !important; color: white !important; }
"""

# ============================================================
#  页 面 事 件 处 理
# ============================================================
def build_conversation_choices():
    """生成下拉框选项"""
    convos = memory.list_all()
    return [(f"{c['title']}  ({c['time']})", c["id"]) for c in convos]


def on_send(message, chatbot_value, convo_id):
    """发送消息 → 调用AI（带工具！）→ 保存记忆"""
    if not message.strip():
        return "", chatbot_value, convo_id, gr.Dropdown()

    # ★ 调用 AI Agent（自动决定是否使用工具）
    bot_reply = chat_with_ai(message, chatbot_value, use_tools=True)

    # 更新对话历史
    chatbot_value.append((message, bot_reply))

    # 保存到文件（长记忆！）
    memory.save(convo_id, chatbot_value)

    # 刷新下拉列表
    choices = build_conversation_choices()
    return "", chatbot_value, convo_id, gr.Dropdown(choices=choices, value=convo_id, label="📋 历史对话")


def on_new():
    """新建对话"""
    new_id = memory.generate_id()
    memory.save(new_id, [])
    choices = build_conversation_choices()
    return [], new_id, gr.Dropdown(choices=choices, value=new_id, label="📋 历史对话")


def on_switch(convo_id):
    """切换历史对话"""
    if not convo_id:
        return gr.Chatbot()
    history = memory.load(convo_id)
    return history


def on_page_load():
    """页面加载时打开最近的对话"""
    convos = memory.list_all()
    if convos:
        latest = convos[0]
        history = memory.load(latest["id"])
        choices = build_conversation_choices()
        return history, latest["id"], gr.Dropdown(choices=choices, value=latest["id"], label="📋 历史对话")
    else:
        new_id = memory.generate_id()
        memory.save(new_id, [])
        choices = build_conversation_choices()
        return [], new_id, gr.Dropdown(choices=choices, value=new_id, label="📋 历史对话")


# ============================================================
#  Gradio 界 面
# ============================================================
with gr.Blocks(css=CSS, title="AI Agent Hub") as demo:
    # ---- 状态 ----
    convo_id = gr.State()

    # ---- 顶部标题 ----
    gr.HTML("""
    <div style="text-align:center; padding:20px 0 8px 0; background:#f5f5f7;">
        <h1 style="font-size:26px; font-weight:600; color:#1d1d1f; margin:0;">
            🤖 AI Agent Hub
        </h1>
        <p style="font-size:14px; color:#86868b; margin:4px 0 0 0;">
            多功能 AI 智能助手 · 支持工具调用 · 对话自动保存
        </p>
        <div style="margin-top:6px;">
            <span style="font-size:12px; background:#e8f0fe; color:#007aff; padding:3px 12px; border-radius:12px;">
                🔧 计算器 · 天气查询 · 时间日期
            </span>
        </div>
    </div>
    """)

    # ---- 控制栏 ----
    with gr.Row(equal_height=True):
        convo_selector = gr.Dropdown(
            choices=build_conversation_choices(),
            label="📋 历史对话",
            interactive=True,
            scale=4,
            min_width=200,
        )
        new_btn = gr.Button("✏️ 新对话", scale=1, min_width=100, variant="secondary")

    # ---- 聊天区域 ----
    chatbot = gr.Chatbot(
        label="",
        height=520,
        bubble_full_width=False,
    )

    # ---- 工具状态提示 ----
    gr.HTML("""
    <div style="text-align:center; font-size:13px; color:#86868b; padding:2px 0;">
        💡 试试问：<b>"今天几号"</b> · <b>"北京天气"</b> · <b>"258×37等于多少"</b>
    </div>
    """)

    # ---- 输入区域 ----
    msg = gr.Textbox(
        placeholder="输入消息，按 Enter 发送...",
        label="",
        container=False,
        show_label=False,
    )

    # ---- 事件绑定 ----
    msg.submit(
        fn=on_send,
        inputs=[msg, chatbot, convo_id],
        outputs=[msg, chatbot, convo_id, convo_selector],
    )

    new_btn.click(
        fn=on_new,
        outputs=[chatbot, convo_id, convo_selector],
    )

    convo_selector.select(
        fn=on_switch,
        inputs=[convo_selector],
        outputs=[chatbot],
    )

    # ---- 页面加载时恢复最近对话 ----
    demo.load(
        fn=on_page_load,
        outputs=[chatbot, convo_id, convo_selector],
    )

# ============================================================
#  启 动
# ============================================================
if __name__ == "__main__":
    print("🚀 AI Agent Hub 启动中...")
    print("   🌐 浏览器打开后试试问：")
    print("      - '今天几号？'        → 调用时间工具")
    print("      - '北京天气怎么样？'  → 调用天气工具")
    print("      - '258 × 37 = ?'     → 调用计算器工具")
    print("      - '上海天气和今天是几号？' → 连续调用多个工具！")
    demo.launch()
