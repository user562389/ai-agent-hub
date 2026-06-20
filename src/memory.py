"""
记忆管理模块 — 让AI记住你的每一次对话
"""
import json
import os
from datetime import datetime

# 对话记录存储在项目根目录的 memory/ 文件夹
MEMORY_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "memory")


def _ensure_dir():
    """确保存储目录存在"""
    os.makedirs(MEMORY_DIR, exist_ok=True)


def list_all():
    """获取所有历史对话列表（按更新时间倒序）"""
    _ensure_dir()
    conversations = []
    for fname in os.listdir(MEMORY_DIR):
        if not fname.endswith(".json"):
            continue
        path = os.path.join(MEMORY_DIR, fname)
        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            conversations.append({
                "id": fname[:-5],  # 去掉 .json
                "title": data.get("title", "新对话"),
                "time": data.get("updated_at", ""),
                "count": data.get("count", 0),
            })
        except (json.JSONDecodeError, FileNotFoundError):
            continue

    # 按时间倒序（最新的在最前面）
    conversations.sort(key=lambda x: x["time"], reverse=True)
    return conversations


def load(convo_id):
    """加载指定对话的聊天记录"""
    path = os.path.join(MEMORY_DIR, f"{convo_id}.json")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data.get("history", [])


def save(convo_id, history):
    """保存聊天记录到文件"""
    _ensure_dir()

    # 从第一条用户消息提取标题
    title = "新对话"
    for user_msg, _ in history:
        if user_msg:
            title = (user_msg[:28] + "…") if len(user_msg) > 28 else user_msg
            break

    data = {
        "title": title,
        "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "count": len(history),
        "history": history,
    }

    path = os.path.join(MEMORY_DIR, f"{convo_id}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def delete(convo_id):
    """删除指定对话"""
    path = os.path.join(MEMORY_DIR, f"{convo_id}.json")
    if os.path.exists(path):
        os.remove(path)


def generate_id():
    """生成唯一对话ID（精确到秒）"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")
