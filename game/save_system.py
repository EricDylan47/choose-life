# -*- coding: utf-8 -*-
"""
Save system module
"""
import os
import json

# ═══════════════════════════════════════════════════════════════════════════
# 存档管理
# ═══════════════════════════════════════════════════════════════════════════
SAVE_DIR = os.path.expanduser("~/Documents/ChooseLife")
os.makedirs(SAVE_DIR, exist_ok=True)


def get_save_path(slot):
    return os.path.join(SAVE_DIR, f"save_{slot}.json")


def save_game(player_data, slot=1):
    """保存游戏进度"""
    save_path = get_save_path(slot)
    try:
        with open(save_path, 'w', encoding='utf-8') as f:
            json.dump(player_data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存失败: {e}")
        return False


def load_game(slot):
    """加载游戏进度"""
    save_path = get_save_path(slot)
    try:
        if os.path.exists(save_path):
            with open(save_path, 'r', encoding='utf-8') as f:
                return json.load(f)
    except Exception as e:
        print(f"加载失败: {e}")
    return None


def get_save_info(slot):
    """获取存档信息"""
    save_path = get_save_path(slot)
    try:
        if os.path.exists(save_path):
            with open(save_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return f"第{data.get('day', 0)}天 - {data.get('ending', '未完成')}"
    except:
        pass
    return "空存档"
