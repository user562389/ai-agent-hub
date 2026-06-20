"""
工具定义 — AI Agent 可以调用的外部工具
"""
import math
import json


def calculator(expression: str) -> str:
    """
    计算数学表达式（安全版）
    例: "2 + 3 * 4" → "14"
    """
    # 只允许数字和运算符，防止恶意代码
    allowed = set("0123456789+-*/.()% ")
    for ch in expression:
        if ch not in allowed:
            return f"错误：表达式包含不允许的字符 '{ch}'"
    try:
        result = eval(expression, {"__builtins__": {}}, {"math": math})
        return f"{result}"
    except Exception as e:
        return f"计算错误：{e}"


def get_current_time() -> str:
    """获取当前日期和时间"""
    from datetime import datetime
    now = datetime.now()
    return now.strftime("%Y年%m月%d日 %H:%M")


def get_weather(city: str) -> str:
    """
    查询城市天气（演示版 — 返回模拟数据）
    实际项目可以对接真实天气API
    """
    # 模拟数据，展示功能
    weather_data = {
        "北京": "晴，25°C，空气质量良好",
        "上海": "多云，28°C，湿度较大",
        "广州": "雷阵雨，32°C",
        "深圳": "阵雨，30°C",
        "杭州": "阴，26°C",
        "成都": "多云，29°C",
    }
    return weather_data.get(city, f"暂时没有 {city} 的天气数据")


# ============================================================
# 工具注册表 — 告诉AI有哪些工具可用
# ============================================================
TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "计算数学表达式，支持加减乘除和括号",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "数学表达式，如 '2 + 3 * 4'",
                    }
                },
                "required": ["expression"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_current_time",
            "description": "获取当前的日期和时间",
            "parameters": {
                "type": "object",
                "properties": {},
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "查询指定城市的天气情况",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "城市名称，如'北京'",
                    }
                },
                "required": ["city"],
            },
        },
    },
]

# 名字 → 实际函数的映射
TOOL_FUNCTIONS = {
    "calculator": calculator,
    "get_current_time": get_current_time,
    "get_weather": get_weather,
}


def call_tool(name: str, args: dict) -> str:
    """根据工具名和参数，调用对应的函数"""
    func = TOOL_FUNCTIONS.get(name)
    if not func:
        return f"错误：未知工具 '{name}'"
    try:
        return func(**args)
    except Exception as e:
        return f"工具执行错误：{e}"
