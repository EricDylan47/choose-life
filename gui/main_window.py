# -*- coding: utf-8 -*-
"""
Main window/GUI module
"""
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import os
import sys
from datetime import datetime

# Import from other modules
from config import (
    RED, DARK_RED, GRAY, DARK_GRAY, BLACK,
    BG_DARK, BG_MEDIUM, BG_LIGHT,
    YELLOW, ORANGE, GREEN, PURPLE, CYAN, PINK,
    COLORS_EX, TITLE_ART
)
from models.player import Player, HumanTrash
from models.npc import NPC_DEFINITIONS
from models.quest import QuestManager
from data.actions import ALL_ACTIONS
from game.save_system import save_game, load_game, get_save_info
from game.mini_games import MiniGames
from game.game_engine import GameEngine
from audio.music import music_player


class ChooseLifeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CHOOSE LIFE - 人生选择模拟器 v3.0")
        self.root.geometry("1400x1000")
        self.root.configure(bg=BG_DARK)
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', self.handle_keypress)
        self.root.bind('<space>', lambda e: self.next_round() if self.continue_btn['state'] == 'normal' and not self.game_over else None)
        self.root.bind('<Button-1>', self.on_click)
        self.root.focus_force()

        self.player = Player()
        self.player.root = root  # 给player添加root引用以便对话框使用
        self.player.quest_manager = QuestManager(self.player)
        self.game_engine = GameEngine(self.player)
        self.displayed_actions = []
        self.timer_running = False
        self.time_left = 25
        self.timer_id = None
        self.debuff_active = False
        self.game_over = False
        self.rent_amount = 40
        self.last_event_round = 0  # 事件冷却追踪
        self.music_on = True

        self.create_menu()
        self.create_widgets()
        # 初始化时先激活可用的任务
        self.player.quest_manager.check_new_quests()
        self._update_quest_display()
        self.start_new_round()
        self.play_background_music()

    def play_background_music(self):
        if getattr(sys, 'frozen', False):
            app_dir = os.path.dirname(sys.executable)
            resource_dir = os.path.join(app_dir, "Contents", "Resources")
        else:
            resource_dir = os.path.dirname(os.path.abspath(__file__))

        possible_paths = [
            os.path.join(resource_dir, "bgm.wav"),
            os.path.join(resource_dir, "bgm.mp3"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "bgm.wav"),
            "/Users/baizhenting/Desktop/vscodework/choose life/bgm.wav",
        ]
        for music_path in possible_paths:
            if os.path.exists(music_path):
                music_player.play(music_path)
                break

    def create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        # 游戏菜单
        game_menu = tk.Menu(menubar, tearoff=0, bg=BG_MEDIUM, fg='white')
        menubar.add_cascade(label="游戏", menu=game_menu, font=("Courier", 10))
        game_menu.add_command(label="新游戏", command=self.confirm_new_game, font=("Courier", 10))
        game_menu.add_separator()
        game_menu.add_command(label="保存游戏 (1)", command=lambda: self.quick_save(1), font=("Courier", 10))
        game_menu.add_command(label="保存游戏 (2)", command=lambda: self.quick_save(2), font=("Courier", 10))
        game_menu.add_command(label="保存游戏 (3)", command=lambda: self.quick_save(3), font=("Courier", 10))
        game_menu.add_separator()
        game_menu.add_command(label="读取存档 (1)", command=lambda: self.quick_load(1), font=("Courier", 10))
        game_menu.add_command(label="读取存档 (2)", command=lambda: self.quick_load(2), font=("Courier", 10))
        game_menu.add_command(label="读取存档 (3)", command=lambda: self.quick_load(3), font=("Courier", 10))
        game_menu.add_separator()
        game_menu.add_command(label="退出", command=self.confirm_quit, font=("Courier", 10))

        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0, bg=BG_MEDIUM, fg='white')
        menubar.add_cascade(label="帮助", menu=help_menu, font=("Courier", 10))
        help_menu.add_command(label="游戏说明", command=self.show_help, font=("Courier", 10))
        help_menu.add_command(label="快捷键", command=self.show_shortcuts, font=("Courier", 10))

    def quick_save(self, slot):
        """快速保存"""
        from config import SAVE_FORMAT_VERSION
        game_data = {
            'version': SAVE_FORMAT_VERSION,
            'player': self.player.to_dict(),
            'rent_amount': self.rent_amount,
            'game_over': self.game_over,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ending': '游戏中' if not self.game_over else '未知',
            'quest_manager': self.player.quest_manager.to_dict() if self.player.quest_manager else {},
        }
        if save_game(game_data, slot):
            messagebox.showinfo("保存成功", f"游戏已保存到存档槽 {slot}")

    def quick_load(self, slot):
        """快速加载"""
        data = load_game(slot)
        if data:
            self.player = Player.from_dict(data.get('player', {}))
            self.player.root = self.root
            self.player.quest_manager = QuestManager.from_dict(
                data.get('quest_manager', {}), self.player
            )
            self.game_engine = GameEngine(self.player)
            self.rent_amount = data.get('rent_amount', 40)
            self.game_over = data.get('game_over', False)
            self.refresh_display()
            self.setup_options()
            messagebox.showinfo("加载成功", f"已从存档槽 {slot} 加载游戏")
        else:
            messagebox.showwarning("加载失败", f"存档槽 {slot} 为空")

    def confirm_new_game(self):
        """确认新游戏"""
        if messagebox.askyesno("新游戏", "当前进度将会丢失，确定要开始新游戏吗？"):
            self.restart_game()

    def confirm_quit(self):
        """确认退出"""
        if messagebox.askyesno("退出", "确定要退出游戏吗？"):
            self.root.quit()

    def show_help(self):
        """显示帮助"""
        help_text = """【CHOOSE LIFE 游戏说明】

目标：在这个世界活下去，或者毁灭。

属性说明：
- 💰 现金：没有钱你什么都做不了
- 🧠 清醒度：归零你就完了
- 👥 信誉：太低没人帮你
- 💉 戒断值：太高会出问题
- 😰 焦虑：越高越容易出错
- 💔 绝望：高了可能会自杀

游戏规则：
- 每轮选择1-6号选项
- 时间有限，快做决定！
- 6轮后房租到期
- 没钱交租就会被赶出去

按键：
- 1-6：选择选项
- 回车/空格：继续
- ESC：查看状态"""

        help_win = tk.Toplevel(self.root)
        help_win.title("游戏说明")
        help_win.geometry("500x500")
        help_win.configure(bg=BG_DARK)

        text = tk.Text(help_win, bg=BG_MEDIUM, fg='white', font=("Courier", 11),
                      wrap="word", padx=20, pady=20)
        text.pack(fill="both", expand=True)
        text.insert("1.0", help_text)
        text.config(state="disabled")

        tk.Button(help_win, text="关闭", command=help_win.destroy,
                 bg=BG_LIGHT, fg="white", font=("Courier", 12)).pack(pady=10)

    def show_shortcuts(self):
        """显示快捷键"""
        shortcuts = """【快捷键】

1-6     选择对应选项
Enter   继续下一轮
Space   继续下一轮
F1      游戏说明
F2      存档槽1
F3      读档槽1
"""
        messagebox.showinfo("快捷键", shortcuts)

    def restart_game(self):
        """重新开始游戏"""
        self.player = Player()
        self.player.root = self.root
        self.player.quest_manager = QuestManager(self.player)
        self.game_engine = GameEngine(self.player)
        self.displayed_actions = []
        self.timer_running = False
        self.time_left = 25
        self.timer_id = None
        self.debuff_active = False
        self.game_over = False
        self.rent_amount = 40
        self.last_event_round = 0

        self.create_widgets()
        # 重新开始时也初始化任务
        self.player.quest_manager.check_new_quests()
        self._update_quest_display()
        self.start_new_round()

    def refresh_display(self):
        """刷新显示所有属性"""
        # 财务
        self.cash_var.set(max(0, self.player.cash))
        self.bank_var.set(max(0, self.player.bank_balance))
        self.debt_var.set(max(0, self.player.debt))

        # 身体
        self.sober_var.set(max(0, min(100, self.player.sober)))
        self.health_var.set(max(0, min(100, self.player.health)))
        self.wd_var.set(max(0, min(100, self.player.withdrawal)))

        # 精神
        self.anxiety_var.set(max(0, min(100, self.player.anxiety)))
        self.despair_var.set(max(0, min(100, self.player.despair)))
        self.hope_var.set(max(0, min(100, self.player.hope)))

        # 社交
        self.rep_var.set(max(0, min(100, self.player.reputation)))
        self.social_var.set(max(0, min(20, self.player.social_connections)))

        # 更新数值标签
        self.cash_value_label.configure(text=f"£{self.player.cash}")
        self.bank_value_label.configure(text=f"£{self.player.bank_balance}")
        self.debt_value_label.configure(text=f"£{self.player.debt}")
        self.sober_value_label.configure(text=str(self.player.sober))
        self.health_value_label.configure(text=str(self.player.health))
        self.wd_value_label.configure(text=str(self.player.withdrawal))
        self.anxiety_value_label.configure(text=str(self.player.anxiety))
        self.despair_value_label.configure(text=str(self.player.despair))
        self.hope_value_label.configure(text=str(self.player.hope))
        self.rep_value_label.configure(text=str(self.player.reputation))
        self.social_value_label.configure(text=str(self.player.social_connections))

        # 更新进度条
        self._update_bar(self.cash_bar, self.player.cash, 200, COLORS_EX['cash'])
        self._update_bar(self.bank_bar, self.player.bank_balance, 1000, COLORS_EX['bank_balance'])
        self._update_bar(self.debt_bar, self.player.debt, 500, COLORS_EX['debt'])
        self._update_bar(self.sober_bar, self.player.sober, 100, COLORS_EX['sober'])
        self._update_bar(self.health_bar, self.player.health, 100, COLORS_EX['health'])
        self._update_bar(self.wd_bar, self.player.withdrawal, 100, COLORS_EX['withdrawal'])
        self._update_bar(self.anxiety_bar, self.player.anxiety, 100, COLORS_EX['anxiety'])
        self._update_bar(self.despair_bar, self.player.despair, 100, COLORS_EX['despair'])
        self._update_bar(self.hope_bar, self.player.hope, 100, COLORS_EX['hope'])
        self._update_bar(self.rep_bar, self.player.reputation, 100, COLORS_EX['reputation'])
        self._update_bar(self.social_bar, self.player.social_connections, 20, COLORS_EX['social_connections'])

        # 更新NPC关系显示
        self._update_npc_display()

        # 更新任务显示
        self._update_quest_display()

        self.time_label.configure(text=f"第{self.player.day}天 {self.player.hour}:00")
        self.rent_label.configure(text=f"房租: £{self.rent_amount} | {self.player.rent_due}轮后到期")

    def _update_bar(self, bar, value, max_val, color):
        """更新进度条"""
        progress = max(0, min(1, value / max_val))
        bar.configure(bg=color)
        bar.place_configure(relwidth=progress)

    def _update_npc_display(self):
        """更新NPC关系显示"""
        lines = []
        for npc_id, rel in self.player.relationships.items():
            npc_def = NPC_DEFINITIONS.get(npc_id, {})
            name = npc_def.get('name', npc_id)
            state_icon = {'enemy': '😠', 'stranger': '❓', 'acquaintance': '🤝', 'friend': '😊', 'close_friend': '💕'}.get(rel.state, '❓')
            lines.append(f"{state_icon}{name}: {rel.state} (好感{rel.affinity})")
        self.npc_label.configure(text="\n".join(lines) if lines else "无")

    def _update_quest_display(self):
        """更新任务显示"""
        if not self.player.quest_manager:
            self.quest_label.configure(text="无进行中的任务")
            return

        active = self.player.quest_manager.active_quests
        completed = self.player.quest_manager.completed_quests
        lines = []

        # 显示进行中的任务
        if active:
            for qid in active[:3]:  # 最多显示3个
                quest = self.player.quest_manager.all_quests.get(qid)
                if quest:
                    lines.append(f"📋{quest.title}")
                    for obj in quest.objectives:
                        prog = obj.get('current', 0)
                        tgt = obj.get('target', 1)
                        lines.append(f"   ▸ {obj.get('description', '')} ({prog}/{tgt})")
        else:
            lines.append("无进行中的任务")

        # 显示最近完成的任务
        if completed:
            recent = completed[-2:]  # 最近2个
            for qid in recent:
                quest = self.player.quest_manager.all_quests.get(qid)
                if quest:
                    lines.append(f"✅{quest.title}")

        self.quest_label.configure(text="\n".join(lines))

    def create_widgets(self):
        """创建所有GUI部件"""
        # 先清除现有部件
        for widget in self.root.winfo_children():
            if widget != self.root.config('menu')[-1]:  # 保留菜单
                widget.destroy()

        # 标题
        title_frame = tk.Frame(self.root, bg=BG_DARK)
        title_frame.pack(pady=5)

        title = tk.Label(title_frame, text="✞ CHOOSE LIFE = CHOOSE MISERY ✞",
                         font=("Courier New", 18, "bold"), fg=RED, bg=BG_DARK)
        title.pack()

        subtitle = tk.Label(title_frame, text="在黑暗中做出选择，要么堕落，要么毁灭",
                           font=("Courier", 10, "italic"), fg=GRAY, bg=BG_DARK)
        subtitle.pack()

        # 顶部信息栏
        top_frame = tk.Frame(self.root, bg=BG_DARK)
        top_frame.pack(fill="x", padx=20)

        self.time_label = tk.Label(top_frame, text="第1天 12:00",
                                  font=("Courier", 12), fg=YELLOW, bg=BG_DARK)
        self.time_label.pack(side="left")

        self.rent_label = tk.Label(top_frame, text=f"房租: £{self.rent_amount} | 6轮后到期",
                                  font=("Courier", 12, "bold"), fg=RED, bg=BG_DARK)
        self.rent_label.pack(side="right")

        self.timer_label = tk.Label(top_frame, text="",
                                    font=("Courier", 14, "bold"), fg=PURPLE, bg=BG_DARK)
        self.timer_label.pack(side="right", padx=20)

        # 主内容区域 - 使用左右分栏
        main_frame = tk.Frame(self.root, bg=BG_DARK)
        main_frame.pack(fill="both", expand=True, padx=20)

        # 左侧：状态面板
        left_frame = tk.Frame(main_frame, bg=BG_DARK)
        left_frame.pack(side="left", fill="y", padx=(0, 10))

        # 属性面板
        status_frame = tk.Frame(left_frame, bg=BG_DARK, bd=1, relief="solid")
        status_frame.pack(pady=5, fill="x")

        stats_container = tk.Frame(status_frame, bg=BG_LIGHT, bd=0, relief="flat")
        stats_container.pack(fill="x", padx=5, pady=5)

        # 创建自定义进度条样式
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

        # ===== 财务维度 =====
        tk.Label(stats_container, text="【财务】", fg=YELLOW, bg=BG_LIGHT,
                font=("Courier New", 10, "bold")).pack(fill="x", pady=(5, 2))

        self.cash_var = tk.IntVar()
        self.cash_var.set(50)
        self.cash_var, self.cash_bar, self.cash_value_label = create_stat_bar(
            stats_container, "现金", "💰", COLORS_EX['cash'], self.cash_var, 200)

        self.bank_var = tk.IntVar()
        self.bank_var.set(0)
        self.bank_var, self.bank_bar, self.bank_value_label = create_stat_bar(
            stats_container, "银行存款", "🏦", COLORS_EX['bank_balance'], self.bank_var, 1000)

        self.debt_var = tk.IntVar()
        self.debt_var.set(0)
        self.debt_var, self.debt_bar, self.debt_value_label = create_stat_bar(
            stats_container, "债务", "⚠️", COLORS_EX['debt'], self.debt_var, 500)

        # ===== 身体健康维度 =====
        tk.Label(stats_container, text="【身体】", fg=ORANGE, bg=BG_LIGHT,
                font=("Courier New", 10, "bold")).pack(fill="x", pady=(5, 2))

        self.sober_var = tk.IntVar()
        self.sober_var.set(60)
        self.sober_var, self.sober_bar, self.sober_value_label = create_stat_bar(
            stats_container, "清醒度", "🧠", COLORS_EX['sober'], self.sober_var, 100)

        self.health_var = tk.IntVar()
        self.health_var.set(80)
        self.health_var, self.health_bar, self.health_value_label = create_stat_bar(
            stats_container, "健康", "❤️", COLORS_EX['health'], self.health_var, 100)

        self.wd_var = tk.IntVar()
        self.wd_var.set(20)
        self.wd_var, self.wd_bar, self.wd_value_label = create_stat_bar(
            stats_container, "戒断值", "💉", COLORS_EX['withdrawal'], self.wd_var, 100)

        # ===== 精神健康维度 =====
        tk.Label(stats_container, text="【精神】", fg=CYAN, bg=BG_LIGHT,
                font=("Courier New", 10, "bold")).pack(fill="x", pady=(5, 2))

        self.anxiety_var = tk.IntVar()
        self.anxiety_var.set(90)
        self.anxiety_var, self.anxiety_bar, self.anxiety_value_label = create_stat_bar(
            stats_container, "焦虑", "😰", COLORS_EX['anxiety'], self.anxiety_var, 100)

        self.despair_var = tk.IntVar()
        self.despair_var.set(50)
        self.despair_var, self.despair_bar, self.despair_value_label = create_stat_bar(
            stats_container, "绝望", "💀", COLORS_EX['despair'], self.despair_var, 100)

        self.hope_var = tk.IntVar()
        self.hope_var.set(30)
        self.hope_var, self.hope_bar, self.hope_value_label = create_stat_bar(
            stats_container, "希望", "✨", COLORS_EX['hope'], self.hope_var, 100)

        # ===== 社交维度 =====
        tk.Label(stats_container, text="【社交】", fg=GREEN, bg=BG_LIGHT,
                font=("Courier New", 10, "bold")).pack(fill="x", pady=(5, 2))

        self.rep_var = tk.IntVar()
        self.rep_var.set(40)
        self.rep_var, self.rep_bar, self.rep_value_label = create_stat_bar(
            stats_container, "信誉", "👥", COLORS_EX['reputation'], self.rep_var, 100)

        self.social_var = tk.IntVar()
        self.social_var.set(2)
        self.social_var, self.social_bar, self.social_value_label = create_stat_bar(
            stats_container, "社交", "🤝", COLORS_EX['social_connections'], self.social_var, 20)

        # NPC关系面板
        npc_frame = tk.Frame(left_frame, bg=BG_DARK, bd=1, relief="solid")
        npc_frame.pack(pady=5, fill="x")
        tk.Label(npc_frame, text="【人物关系】", fg=PURPLE, bg=BG_DARK,
                font=("Courier New", 10, "bold")).pack(pady=2)

        self.npc_label = tk.Label(npc_frame, text="", fg=GRAY, bg=BG_DARK,
                font=("Courier", 9), justify="left", anchor="nw")
        self.npc_label.pack(padx=5, pady=2)

        # 任务面板
        quest_frame = tk.Frame(left_frame, bg=BG_DARK, bd=1, relief="solid")
        quest_frame.pack(pady=5, fill="x")
        tk.Label(quest_frame, text="【当前任务】", fg=YELLOW, bg=BG_DARK,
                font=("Courier New", 10, "bold")).pack(pady=2)

        self.quest_label = tk.Label(quest_frame, text="无进行中的任务",
                fg=GRAY, bg=BG_DARK, font=("Courier", 9), justify="left", anchor="nw")
        self.quest_label.pack(padx=5, pady=2)

        # 右侧：游戏内容
        right_frame = tk.Frame(main_frame, bg=BG_DARK)
        right_frame.pack(side="right", fill="both", expand=True)

        # 场景描述
        self.scene_label = tk.Label(right_frame, text="", font=("Courier", 11),
                                    fg=GRAY, bg=BG_DARK, wraplength=700, justify="left")
        self.scene_label.pack(pady=5)

        self.hint_label = tk.Label(right_frame, text="按 1-6 选择 | 25秒倒计时",
                                   font=("Courier", 10, "italic"), fg=DARK_GRAY, bg=BG_DARK)
        self.hint_label.pack()

        self.options_frame = tk.Frame(right_frame, bg=BG_DARK)
        self.options_frame.pack(pady=5)

        self.option_buttons = []
        for i in range(6):
            btn = tk.Button(self.options_frame, text=f"[{i+1}] ",
                           font=("Courier", 10), fg="#FFA500", bg="#1A1A1A",
                           width=35, height=1, anchor="w",
                           command=lambda idx=i: self.make_choice(idx))
            btn.pack(pady=1, fill="x")
            self.option_buttons.append(btn)

        # 结果文本区域
        self.result_label = tk.Label(right_frame, text="",
                                     fg="#FFA500", bg=BG_DARK,
                                     font=("Courier", 11), justify="left", anchor="nw")
        self.result_label.pack(pady=5, fill="both", padx=10, expand=True)

        # 事件文本区域
        self.event_label = tk.Label(right_frame, text="",
                                    fg="#FFA500", bg=BG_DARK,
                                    font=("Courier", 10), justify="left", anchor="nw")
        self.event_label.pack(pady=5, fill="both", padx=10, expand=True)

        control_frame = tk.Frame(right_frame, bg=BG_DARK)
        control_frame.pack(pady=10)

        self.music_btn = tk.Button(control_frame, text="🎵 音乐: 开",
                                   font=("Courier", 10), fg=GREEN, bg=DARK_GRAY,
                                   command=self.toggle_music, width=15)
        self.music_btn.pack(side="left", padx=5)

        self.continue_btn = tk.Button(control_frame, text="【点击继续】",
                                       font=("Courier", 14, "bold"), fg="white", bg="#8B0000",
                                       command=self.next_round, state="disabled", width=25, height=2)
        self.continue_btn.pack(side="left", padx=5)

    def toggle_music(self):
        if self.music_on:
            music_player.stop()
            self.music_btn.configure(text="🎵 音乐: 关", fg=GRAY)
            self.music_on = False
        else:
            self.play_background_music()
            self.music_btn.configure(text="🎵 音乐: 开", fg=GREEN)
            self.music_on = True

    def handle_keypress(self, event):
        # 按1-6选择选项
        if event.char in '123456' and not self.game_over:
            try:
                idx = int(event.char) - 1
                if self.option_buttons[idx]['state'] == 'normal':
                    self.cancel_timer()
                    self.make_choice(idx)
            except (ValueError, IndexError):
                pass
        # 按回车或空格继续下一轮
        elif event.keysym == 'Return' or event.keysym == 'Space' or event.char in ['\r', '\n', ' ']:
            if self.continue_btn['state'] == 'normal' and not self.game_over:
                self.next_round()

    def on_click(self, event):
        """确保点击时窗口获得焦点"""
        self.root.focus_force()

    def start_timer(self):
        self.timer_running = True
        self.time_left = 25
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        self.timer_label.configure(text=f"⏱ {self.time_left}s")
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="时间到!")
            # 超时自动选择第一个
            self.make_choice(0)

    def cancel_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def setup_options(self):
        """设置本轮选项"""
        self.displayed_actions = random.sample(ALL_ACTIONS, 6)
        for i, (name, action_id) in enumerate(self.displayed_actions):
            self.option_buttons[i].configure(text=f"[{i+1}] {name}", state="normal")

    def start_new_round(self):
        """开始新一轮"""
        self.player.round += 1
        self.player.hour = 12 + (self.player.round % 6) * 2
        if self.player.round % 6 == 0:
            self.player.day += 1
            self.player.rent_due -= 1

        # 触发事件
        event_text = self.game_engine.trigger_events()
        if event_text:
            self.event_label.configure(text=event_text)

        # 检查新任务
        if self.player.quest_manager:
            self.player.quest_manager.check_new_quests()
            self._update_quest_display()

        self.result_label.configure(text="")
        self.event_label.configure(text="")
        self.scene_label.configure(text="在昏暗的出租屋里，你睁开眼睛...\n又是新的一天。")
        self.setup_options()
        self.start_timer()
        self.refresh_display()

    def make_choice(self, idx):
        """处理选择"""
        if idx >= len(self.displayed_actions):
            return

        action_name, action_id = self.displayed_actions[idx]
        self.cancel_timer()

        # 记录选择
        self.player.choices_log.append(action_name)

        # 处理特殊NPC互动
        is_dialog_action = action_id in ('call_mark', 'call_parents', 'text_diane',
                                          'contact_renton', 'call_sick_boy', 'support_group')
        if is_dialog_action:
            if action_id == 'call_mark':
                self.handle_call_mark()
            elif action_id == 'call_parents':
                self.handle_call_parents()
            elif action_id == 'text_diane':
                self.handle_text_diane()
            elif action_id == 'contact_renton':
                self.handle_contact_renton()
            elif action_id == 'call_sick_boy':
                self.handle_call_sick_boy()
            elif action_id == 'support_group':
                self.handle_support_group()
        # 处理小游戏
        elif action_id == 'begbie_gamble':
            self.handle_begbie_gamble()
        elif action_id == 'drinking_contest':
            self.handle_drinking_contest()
        elif action_id == 'steal_bar_liquor':
            self.handle_steal_bar_liquor()
        elif action_id == 'spud_cards':
            self.handle_spud_cards()
        elif action_id == 'pawnshop':
            self.handle_pawnshop()
        elif action_id == 'dumpster_dive':
            self.handle_dumpster_dive()
        elif action_id == 'find_job':
            self.handle_find_job()
        else:
            # 普通动作
            self.handle_normal_action(action_id, action_name)

        # 禁用所有按钮
        for btn in self.option_buttons:
            btn.configure(state="disabled")

        # 对话框操作后，确保事件处理完全恢复
        if is_dialog_action:
            self.root.update()
            self.root.update_idletasks()

        self.finish_turn()

    def handle_normal_action(self, action_id, action_name):
        """处理普通动作"""
        narrative, effect_texts = self.game_engine.apply_choice_result(action_id)
        if narrative:
            self.result_label.configure(text=f"► {action_name}\n\n{narrative}")
        else:
            self.result_label.configure(text=f"► {action_name}\n\n你做了这个选择...")

        # 更新任务进度
        if self.player.quest_manager:
            if action_id == 'support_group':
                self.player.quest_manager.update_quest_progress(action_id='support_group')

    def handle_support_group(self):
        """处理参加互助会"""
        self.result_label.configure(text="► 你选择了：参加互助会\n\n你坐在戒毒互助会的圈子里，听着别人的故事...")

        outcomes = [
            ("一个老者分享了他如何战胜毒瘾的故事，给了你希望...", 20, 10, -20),
            ("你听到的全是比你更惨的故事，反而觉得自己还有救...", 15, 5, -10),
            ("有人认出你是那个'瘾君子'，投来鄙夷的目光...", -10, -15, 5),
        ]
        outcome = random.choice(outcomes)
        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{outcome[0]}")
        self.player.apply_effect('sober', outcome[1])
        self.player.apply_effect('reputation', outcome[2])
        self.player.apply_effect('withdrawal', outcome[3])

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(action_id='support_group')

    def handle_call_mark(self):
        """处理给Mark打电话"""
        choice = simpledialog.askstring("Mark", "Mark接了电话:\n'哟，怎么想起给我打电话了？'\n\n1. 问他最近怎么样\n2. 跟他套近乎\n3. 直接挂断", parent=self.root)

        mark_rel = self.player.relationships.get('mark')

        if choice == "1":
            self.result_label.configure(text="► 你选择了：嘘寒问暖\n\nMark: '最近手头紧，三天后还我£100.'")
            if mark_rel:
                mark_rel.affinity += 5
                update_relationship_state(mark_rel)
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：套近乎\n\nMark: '少来这套，有屁快放。'")
            if mark_rel:
                mark_rel.affinity -= 5
                update_relationship_state(mark_rel)
        else:
            self.result_label.configure(text="► 你选择了：挂断\n\n你挂断了电话，心里一阵发慌...")

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='mark')

    def handle_call_parents(self):
        """处理给父母打电话"""
        choice = simpledialog.askstring("父母",
            "电话接通了...\n\n1. 嘘寒问暖\n2. 委婉地要钱\n3. 告诉他们你想回家\n4. 挂断", parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：嘘寒问暖\n\n母亲的声音有些颤抖：\n'儿子，我们都很担心你...'")
            self.player.apply_effect('reputation', 5)
            self.player.apply_effect('hope', 5)
            self.player.story_flags['called_parents_home'] = True
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：要钱\n\n父亲沉默了很久，然后叹了口气：\n'我下午转账给你...'")
            self.player.apply_effect('cash', 40)
            self.player.apply_effect('reputation', -5)
            self.player.story_flags['asked_parents_for_money'] = True
        elif choice == "3":
            self.result_label.configure(text="► 你选择了：告诉他们想回家\n\n母亲哭了出来：\n'太好了太好了...你爸虽然嘴上不说，但天天念叨你...'")
            self.player.apply_effect('hope', 15)
            self.player.apply_effect('despair', -10)
            self.player.story_flags['reconnected_with_mother'] = True
        else:
            self.result_label.configure(text="► 你选择了：挂断\n\n你按下挂断键，泪水在眼眶里打转...")

    def handle_text_diane(self):
        """处理给Diane发短信"""
        choice = simpledialog.askstring("Diane",
            "你编辑着给Diane的消息...\n\n1. 发一句'最近还好吗'\n2. 发一句'我想你'\n3. 算了，不发了", parent=self.root)

        diane_rel = self.player.relationships.get('diane')

        if choice == "1":
            self.result_label.configure(text="► 你选择了：问好\n\nDiane很快回复了:\n'挺好的，你呢？'")
            if diane_rel:
                diane_rel.affinity += 10
                update_relationship_state(diane_rel)
            self.player.apply_effect('hope', 5)
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：表白\n\n消息显示已读...\n\n很久之后，Diane回复:\n'我们已经结束了.'")
            if diane_rel:
                diane_rel.affinity -= 10
                update_relationship_state(diane_rel)
            self.player.apply_effect('despair', 10)
        else:
            self.result_label.configure(text="► 你选择了：放弃\n\n你删掉了打好的字，心里空落落的...")

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='diane')

    def handle_contact_renton(self):
        """处理联系Renton"""
        choice = simpledialog.askstring("Renton",
            "你拨通了Renton的号码...\n\n1. 求他回来\n2. 问他在伦敦怎么样\n3. 什么都不说", parent=self.root)

        renton_rel = self.player.relationships.get('renton')

        if choice == "1":
            self.result_label.configure(text="► 你选择了：求他回来\n\n电话那头沉默了很久...\n\n'我会回来的。但你要答应我，好好活着。'")
            if renton_rel:
                renton_rel.affinity += 15
                update_relationship_state(renton_rel)
            self.player.apply_effect('hope', 20)
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：问近况\n\n'伦敦很好，一切都重新开始。'\n\n'Renton，我...'")
            if renton_rel:
                renton_rel.affinity -= 5
                update_relationship_state(renton_rel)
        else:
            self.result_label.configure(text="► 你选择了：什么都不说\n\n电话那头只有你的呼吸声...\n\n然后Renton先挂断了。")
            if renton_rel:
                renton_rel.affinity -= 5
                update_relationship_state(renton_rel)

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='renton')

    def handle_call_sick_boy(self):
        """处理给Sick Boy打电话"""
        choice = simpledialog.askstring("Sick Boy",
            "Sick Boy接了电话：\n'Shit happens. 什么事？'\n\n1. 问有没有新货\n2. 问他最近在干嘛\n3. 问能不能帮忙", parent=self.root)

        sick_boy_rel = self.player.relationships.get('sick_boy')

        if choice == "1":
            self.result_label.configure(text="► 你选择了：问新货\n\n'新货到了，要来点吗？£40一包'")
            self.player.apply_effect('cash', -40)
            self.player.apply_effect('withdrawal', -30)
            if sick_boy_rel:
                sick_boy_rel.affinity += 5
                update_relationship_state(sick_boy_rel)
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：闲聊\n\n'我？我在写诗。在这座腐烂的城市里，只有艺术是永恒的。'")
            self.player.apply_effect('sober', 5)
            if sick_boy_rel:
                sick_boy_rel.affinity += 10
                update_relationship_state(sick_boy_rel)
        else:
            self.result_label.configure(text="► 你选择了：求助\n\n'我？帮你？你拿什么还？'")
            if sick_boy_rel:
                sick_boy_rel.affinity -= 5
                update_relationship_state(sick_boy_rel)
            self.player.apply_effect('despair', 5)

    # 小游戏处理器
    def handle_begbie_gamble(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_begbie_gamble(self.root, self.player, callback)

    def handle_drinking_contest(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_drinking_contest(self.root, self.player, callback)

    def handle_steal_bar_liquor(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_steal_bar_liquor(self.root, self.player, callback)

    def handle_spud_cards(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_spud_cards(self.root, self.player, callback)

    def handle_pawnshop(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_pawnshop(self.root, self.player, callback)

    def handle_dumpster_dive(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_dumpster_dive(self.root, self.player, callback)

    def handle_find_job(self):
        def callback(result):
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result}")
        MiniGames.handle_find_job(self.root, self.player, callback)

    def finish_turn(self):
        """回合结束处理"""
        self.game_engine.last_event_round = self.player.round

        # 检查任务失败
        if self.player.quest_manager:
            self.player.quest_manager.check_failures()
            self._update_quest_display()

        self.update_status()

        # 在结果中显示当前现金
        self.result_label.configure(text=self.result_label.cget("text") +
            f"\n\n💰 当前现金: £{self.player.cash}")

        if self.player.reputation < 20:
            self.event_label.configure(text=self.event_label.cget("text") + "\n⚠️ 信誉太低！所有朋友都背叛了你！")

        # 检查结局
        ending = self.game_engine.check_endings()
        if ending:
            self.show_ending(ending)
            return

        self.continue_btn.configure(state="normal")
        self.root.update_idletasks()

    def update_status(self):
        """更新状态显示"""
        # 触发事件
        event_text = self.game_engine.trigger_events()
        if event_text:
            current_text = self.event_label.cget("text")
            self.event_label.configure(text=current_text + "\n\n" + event_text if current_text else event_text)

        self.refresh_display()

    def next_round(self):
        self.player.withdrawal = min(100, self.player.withdrawal + 5)
        self.player.sober = min(100, self.player.sober + 5)
        self.continue_btn.configure(state="disabled")
        self.start_new_round()

    def show_ending(self, reason):
        """显示结局"""
        self.game_over = True
        self.cancel_timer()

        title, text = self.game_engine.get_ending(reason)
        self.game_engine.save_record(title)

        reply = messagebox.askretrycancel(
            f"✞ {title} ✞",
            f"{text}\n\n存活: {self.player.day}天 {self.player.round}轮\n\n再来一局？"
        )

        if reply:
            self.player = Player()
            self.player.root = self.root
            self.player.quest_manager = QuestManager(self.player)
            self.game_engine = GameEngine(self.player)
            self.game_over = False
            self.debuff_active = False
            self.start_new_round()
        else:
            self.root.quit()
