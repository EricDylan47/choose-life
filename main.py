#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CHOOSE LIFE - 人生选择模拟器
入口点
"""
import tkinter as tk
from gui.main_window import ChooseLifeGame


def main():
    root = tk.Tk()
    app = ChooseLifeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
