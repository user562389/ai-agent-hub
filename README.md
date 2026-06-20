# AI Agent Hub 🤖

多功能 AI 智能助手系统 — 集成对话、工具调用（Function Calling）、长记忆存储的 AI Agent 项目。

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| 💬 智能对话 | 基于 DeepSeek 大模型 API 的多轮对话 |
| 🔧 Function Calling | AI 自动调用计算器、天气查询、时间查询等外部工具 |
| 🧠 长记忆系统 | 对话历史自动保存到本地，刷新页面可恢复 |
| 🎨 精美界面 | 苹果风格蓝色气泡聊天 UI，全屏大字体 |

## 🛠 技术栈

- **Python 3** — 核心语言
- **Gradio** — Web 界面框架
- **OpenAI SDK** — 大模型 API 调用
- **DeepSeek API** — 语言模型
- **JSON** — 本地数据持久化

## 📁 项目结构

```
ai-agent-hub/
├── src/
│   ├── app.py          # Gradio Web 界面（主入口）
│   ├── agent.py        # AI Agent 核心逻辑
│   ├── tools.py        # 工具定义（计算器、天气、时间）
│   └── memory.py       # 对话记忆管理模块
├── examples/
│   ├── function_calling_demo.py  # Function Calling 交互演示
│   └── auto_demo.py              # Function Calling 自动演示
├── memory/             # 对话历史存储目录
├── README.md           # 项目说明（本文件）
└── requirements.txt    # Python 依赖
```

## 🚀 快速开始

### 1️⃣ 安装依赖

```bash
pip install -r requirements.txt
```

### 2️⃣ 配置 API Key

编辑 `src/config.py`，填入你的 DeepSeek API Key：

```python
API_KEY = "your-api-key-here"
```

> 💡 在 [DeepSeek 官网](https://platform.deepseek.com) 注册获取 API Key

### 3️⃣ 启动应用

```bash
cd src
python app.py
```

浏览器会自动打开 `http://localhost:7860`

### 4️⃣ 运行 Function Calling 演示

```bash
cd examples
python function_calling_demo.py    # 交互模式
# 或
python auto_demo.py                # 自动演示
```

## 🤖 Function Calling 演示效果

AI 能自动识别何时调用工具：

```
👤 用户: 北京今天天气怎么样？
🤖 AI 决定调用 → [get_weather({'city': '北京'})]
🔧 工具返回 → 晴，25°C，空气质量良好
🤖 AI: 北京今天天气晴朗，气温25°C，空气质量良好！

👤 用户: 帮我算一下 258 × 37 等于多少？
🤖 AI 决定调用 → [calculator({'expression': '258 * 37'})]
🔧 工具返回 → 9546
🤖 AI: 258 × 37 = 9546
```

## 🧠 长记忆系统

- 所有对话自动保存为 JSON 文件
- 页面刷新后自动恢复最近对话
- 支持切换历史对话
- 自动从首条消息提取对话标题

## 📌 路线图

- [x] 基础对话功能
- [x] Function Calling 工具调用
- [x] 对话历史持久化
- [ ] RAG 知识库（开发中）
- [ ] 网页搜索工具
- [ ] LangChain 集成

## 📬 联系我

李玉峰 — 求职 AI Agent / 大模型应用开发

- 📧 邮箱: 1773963074@qq.com
- 💻 GitHub: [github.com/user562389/ai-agent-hub](https://github.com/user562389/ai-agent-hub)
