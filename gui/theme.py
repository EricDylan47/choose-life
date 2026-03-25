# -*- coding: utf-8 -*-
"""
GUI theme module
Contains UI constants and theme functions
"""
from config import (
    RED, DARK_RED, GRAY, DARK_GRAY, BLACK,
    BG_DARK, BG_MEDIUM, BG_LIGHT,
    YELLOW, ORANGE, GREEN, PURPLE, CYAN, PINK,
    COLORS_EX
)

__all__ = [
    'RED', 'DARK_RED', 'GRAY', 'DARK_GRAY', 'BLACK',
    'BG_DARK', 'BG_MEDIUM', 'BG_LIGHT',
    'YELLOW', 'ORANGE', 'GREEN', 'PURPLE', 'CYAN', 'PINK',
    'COLORS_EX', 'create_stat_bar_style'
]


def create_stat_bar_style():
    """返回创建自定义进度条样式的函数"""
    return """
    def create_stat_bar(parent, label, icon, color, var, max_val=100):
        frame = tk.Frame(parent, bg=BG_LIGHT)
        frame.pack(fill="x", pady=2)

        tk.Label(frame, text=f"{icon}{label}", fg=color, bg=BG_LIGHT,
                width=10, anchor="w", font=("Courier New", 9, "bold")).pack(side="left")

        bar_bg = tk.Frame(frame, bg="#1a1a1a", height=12)
        bar_bg.pack(side="left", fill="x", expand=True, padx=5)
        bar_bg.pack_propagate(False)

        var.set(min(max_val, max(0, var.get())))
        progress = max(0, min(1, var.get() / max_val))
        bar_fill = tk.Frame(bar_bg, bg=color, height=10)
        bar_fill.place(relx=0, rely=0.5, relwidth=progress, anchor="w")
        bar_fill.pack_propagate(False)

        value_label = tk.Label(frame, text=str(var.get()), fg=color, bg=BG_LIGHT,
                              width=5, font=("Courier New", 9, "bold"))
        value_label.pack(side="right")

        return var, bar_fill, value_label
    """
