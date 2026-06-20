"""
配置管理 — AI Agent Hub
"""
"""
配置管理 — AI Agent Hub
"""
import os

# DeepSeek API 配置（优先读环境变量，没有就用 .env 文件）
# 使用方式：在项目根目录创建 .env 文件，写入：
#   DEEPSEEK_API_KEY=你新创建的key
API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
BASE_URL = "https://api.deepseek.com"
MODEL = "deepseek-chat"

# 系统提示词
SYSTEM_PROMPT = "你是一个专业、高效的AI助手。回答简洁清晰，有逻辑，不啰嗦。"

# 应用配置
APP_TITLE = "AI 智能助手"
PRIMARY_COLOR = "#007aff"
