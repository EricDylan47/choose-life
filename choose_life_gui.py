#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
✞ CHOOSE LIFE = CHOOSE YOUR MISERY ✞
人生选择模拟器 —— 终极混沌版
================================================================================
# 清醒度？只是你骗自己还能撑下去的幻觉
# 信誉？你就是个骗子，别装了
# 戒断？你的身体早就不属于你了
================================================================================
"""

import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time
import threading
import subprocess
import os
import sys

# ═══════════════════════════════════════════════════════════════════════════
# 音乐播放
# ═══════════════════════════════════════════════════════════════════════════
class MusicPlayer:
    def __init__(self):
        self.playing = False
        self.process = None

    def play(self, music_file=None):
        if self.playing:
            return
        if music_file and os.path.exists(music_file):
            try:
                self.process = subprocess.Popen(
                    ["afplay", "-v", "0.3", music_file],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
                self.playing = True
            except:
                pass

    def stop(self):
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self.playing = False

music_player = MusicPlayer()

# ═══════════════════════════════════════════════════════════════════════════
# 颜色定义
# ═══════════════════════════════════════════════════════════════════════════
RED = '#FF4444'
DARK_RED = '#8B0000'
GRAY = '#808080'
DARK_GRAY = '#404040'
BLACK = '#0D0D0D'
BG_DARK = '#1A1A1A'
YELLOW = '#FFA500'  # 亮橙色，更醒目
GREEN = '#00FF00'
PURPLE = '#9900FF'

# ═══════════════════════════════════════════════════════════════════════════
# 动作库
# ═══════════════════════════════════════════════════════════════════════════
ALL_ACTIONS = [
    ("灌下那瓶掺水威士忌", "drink_shit_whisky"),
    ("试图看懂那本编程书", "learn_code"),
    ("把假Heroin扔进马桶", "throw_away_heroin"),
    ("给Mark打电话要钱", "call_mark"),
    ("躺平，在黑暗中等待", "lie_down"),
    ("出门，去酒吧买醉", "go_to_bar"),
    ("尝试联系Renton", "contact_renton"),
    ("去ATM机查余额", "check_bank"),
    ("给父母打电话", "call_parents"),
    ("出门找工作", "find_job"),
    ("清理房间", "clean_room"),
    ("听天由命", "accept_fate"),
    ("偷Spud的皮鞋去当铺", "steal_spud_shoes"),
    ("给Diane发短信", "text_diane"),
    ("去网吧上网", "go_internet_cafe"),
    ("在墙上涂鸦", "graffiti_wall"),
    ("偷听邻居吵架", "eavesdrop_neighbor"),
    ("尝试戒毒", "try_quit_drugs"),
    ("去教堂祈祷", "pray_at_church"),
    ("看A片自慰", "watch_porn"),
    ("给Sick Boy打电话", "call_sick_boy"),
    ("去海边发呆", "stare_at_sea"),
    ("垃圾桶里翻东西吃", "dumpster_dive"),
    ("假装去上班", "fake_go_work"),
    ("写遗书", "write_suicide_note"),
    ("打自杀热线", "call_hotline"),
    ("跟踪陌生人", "stalk_stranger"),
    ("赊账喝酒", "drink_on_credit"),
    ("尝试黑掉银行", "hack_bank"),
    ("去图书馆", "go_library"),
    ("和猫玩", "play_with_cat"),
    ("在雨中漫步", "walk_in_rain"),
    # 新增可互动动作
    ("和Begbie赌博", "begbie_gamble"),
    ("在酒吧拼酒", "drinking_contest"),
    ("偷酒吧的酒", "steal_bar_liquor"),
    ("和Spud玩纸牌", "spud_cards"),
    ("去当铺典当", "pawnshop"),
]

# ═══════════════════════════════════════════════════════════════════════════
# 选择结果 - 极乐迪斯科风格的文学描写
# ═══════════════════════════════════════════════════════════════════════════
CHOICE_RESULTS = {
    "drink_shit_whisky": [
        ("你灌下那瓶掺水的威士忌。灼烧感从喉咙一路延伸到胃部，像是把一把钝刀吞了下去...", "清醒度-25", "money", -5),
        ("威士忌寡淡如水，你的身体在抗议这份欺骗...", "清醒度-20", "money", -3),
        ("劣质酒精让你天旋地转，胃里翻江倒海...", "清醒度-30", "money", -8),
    ],
    "learn_code": [
        ("代码在你眼前变成天书，那些字符像是远古的楔形文字...", "清醒度-5", "money", 0),
        ("编程书纸张发黄，盗版印刷的错误让你更加困惑...", "清醒度-10", "money", 0),
        ("你盯着屏幕看了十分钟，然后意识渐渐模糊...", "清醒度+5", "money", 0),
    ],
    "throw_away_heroin": [
        ("Spud看到你扔掉东西，眼神里闪过一丝困惑...", "戒断值-15", "信誉", -10),
        ("房东经过时皱起眉头，空气里弥漫着可疑的气息...", "戒断值+5", "money", -15),
        ("Mark注意到了你的举动，狐疑地看了你一眼...", "戒断值+10", "信誉", -20),
    ],
    "call_mark": [
        ("电话响了几声，然后转入忙音...", "信誉-10", "money", 0),
        ("Mark接了电话，听起来心情不错: '等着，我给你转点...' - £30到账", "信誉+10", "money", 30),
        ("Mark最近发了笔横财: '拿着，算我借你的.' - £50静静到账", "信誉+15", "money", 50),
    ],
    "lie_down": [
        ("你躺回床上，天花板上的霉斑像幅抽象画...", "清醒度-10", "money", 0),
        ("敲门声传来，是房东在提醒你该缴租了...", "清醒度+5", "money", -5),
        ("黎明的光线透过脏窗帘，你又熬过了一夜...", "清醒度-5", "money", 0),
    ],
    "go_to_bar": [
        ("酒精模糊了你的视线，世界在旋转...", "清醒度-35", "money", -20),
        ("Begbie在吧台发酒疯，你明智地躲开了...", "清醒度-20", "money", -10),
        ("你发现口袋被割开了，钱包不翼而飞...", "清醒度-15", "money", -30),
    ],
    "contact_renton": [
        ("电话那头只有忙音，像是某种永恒的沉默...", "清醒度-10", "money", 0),
        ("Renton早已不在这个城市，他去了伦敦寻找新生活...", "清醒度-15", "money", 0),
        ("你被拉入了黑名单，也许这就是结局...", "清醒度-20", "money", 0),
    ],
    "check_bank": [
        ("你的账户似乎被冻结了，机器拒绝读取...", "清醒度-10", "money", 0),
        ("余额显示: £0.37 . 这就是你全部的积蓄...", "清醒度-15", "money", 0),
        ("你发现一笔未知的转账记录，金额去向不明...", "清醒度-5", "money", -20),
    ],
    "call_parents": [
        ("电话那头传来母亲的哭声，你喉咙发紧...", "信誉+5", "money", 0),
        ("父亲叹了口气，把电话挂了...", "信誉-10", "money", 0),
        ("你听到父亲苍老的声音，眼眶有些湿润...", "信誉+10", "money", 0),
        ("母亲心软了: '儿子，拿去买点吃的.' - £40静静到账", "信誉+15", "money", 40),
    ],
    "find_job": [
        ("工作人员抬头看你，眼神里写着'又一个失败者'...", "清醒度-10", "money", 0),
        ("招聘启事贴满墙壁，但没有一个空位...", "清醒度-15", "money", 0),
        ("你投出的简历石沉大海...", "清醒度-20", "money", 0),
        ("劳工市场的人对你点头: '这里有个日结工作，£50一天.'", "清醒度+10", "money", 50),
    ],
    "clean_room": [
        ("你在床底发现一只死老鼠，臭味让你干呕...", "清醒度-10", "money", 0),
        ("打扫累了，你直接躺在地上睡着了...", "清醒度+5", "money", 0),
        ("你发现墙上有个可疑的小孔——是摄像头...", "清醒度-20", "money", 0),
        ("清理抽屉时，你找到以前藏的私房钱£30...", "清醒度+5", "money", 30),
    ],
    "accept_fate": [
        ("放弃抵抗的那一刻，你感到一种病态的平静...", "清醒度-30", "money", -10),
        ("接受现实没那么难，反正人生本来就是如此...", "清醒度-20", "money", -15),
        ("你像具行尸走肉，在房间里游荡...", "清醒度-25", "money", -5),
    ],
    "steal_spud_shoes": [
        ("皮鞋尺码太小，根本穿不下...", "清醒度-5", "money", 10),
        ("当铺老板看出这是偷来的东西，拒绝交易...", "信誉-20", "money", 0),
        ("老板只是耸耸肩，给了你£15...", "信誉+5", "money", 20),
        ("这双皮鞋居然是真皮的! 当了£40!", "信誉+10", "money", 40),
    ],
    "text_diane": [
        ("Diane很快回复了: '别再联系我了.' 然后拉黑...", "信誉+5", "money", 0),
        ("消息显示已读，但没有回复...", "信誉-10", "money", 0),
        ("Diane回了: '你需要帮助.' 然后转了£20...", "信誉+10", "money", 20),
    ],
    "go_internet_cafe": [
        ("网吧电脑太卡，你盯着加载界面发呆...", "清醒度-5", "money", -5),
        ("你在论坛发的帖子被网友嘲笑...", "信誉-15", "money", 0),
        ("你在网上接了个翻译私活£30，虽少但够买几瓶酒...", "清醒度-10", "money", 30),
    ],
    "graffiti_wall": [
        ("你在巷子里画下自己的愤怒，但技法太稚嫩...", "清醒度-5", "money", 0),
        ("巡警的手电筒照过来，你拔腿就跑...", "清醒度-15", "money", -10),
        ("一个街头艺术经纪人看中了你的涂鸦: '这个我要了.' - £40", "清醒度+10", "money", 40),
    ],
    "eavesdrop_neighbor": [
        ("邻居发现了你贴在门上的耳朵...", "清醒度-10", "money", 0),
        ("你听到他们在议论你的不堪...", "清醒度-20", "money", 0),
    ],
    "try_quit_drugs": [
        ("戒断反应如潮水般涌来，你全身颤抖...", "戒断值-20", "清醒度+15", 0),
        ("你坚持了不到三分钟，意志力全线崩溃...", "戒断值-10", "清醒度+10", 0),
    ],
    "pray_at_church": [
        ("你跪在教堂长椅上，但神没有回应...", "清醒度+5", "money", 0),
        ("管理员走过来: '这里不允许流浪汉进入.'", "清醒度-10", "money", 0),
    ],
    "watch_porn": [
        ("电脑在这关键时刻卡住了...", "清醒度-5", "money", 0),
        ("看完之后，只有更深的空虚...", "清醒度-15", "money", 0),
    ],
    "call_sick_boy": [
        ("Sick Boy接了: '新货到了，要来点吗?' - 你花了£10买了包假货...", "戒断值+15", "money", -10),
        ("Sick Boy: '帮我送趟货，给你£40.' 你接下了这危险的差事...", "戒断值+10", "信誉", -15),
        ("Sick Boy介绍了个来钱的活: '跟单，£40.' 顺利完成!", "戒断值+5", "money", 40),
    ],
    "stare_at_sea": [
        ("海鸥在你头顶盘旋，像是在嘲笑你的落魄...", "清醒度+5", "money", 0),
        ("看着海浪，你第一次认真考虑跳下去...", "清醒度-10", "money", 0),
    ],
    "dumpster_dive": [
        ("你在垃圾桶里翻出半个发霉的苹果，至少饿不死...", "清醒度-10", "money", 5),
        ("你居然捡到£15! 可能是谁掉的...", "清醒度+5", "money", 15),
        ("隔壁酒吧的保安发现你在翻垃圾，把你赶走了...", "清醒度-20", "money", 0),
    ],
    "fake_go_work": [
        ("你在地铁站站了一整天，装作赶路的样子...", "清醒度-10", "money", 0),
        ("邻居揭穿了你的谎言，你在假装上班...", "信誉-20", "money", 0),
    ],
    "write_suicide_note": [
        ("你写了几行字，但风吹走了纸...", "清醒度+5", "money", 0),
        ("写着写着，你突然不想死了...", "清醒度-15", "money", 0),
    ],
    "call_hotline": [
        ("自杀热线一直占线...", "清醒度-10", "money", 0),
        ("终于有人接了，但只是例行公事地问了几句...", "清醒度-15", "money", 0),
    ],
    "stalk_stranger": [
        ("那个陌生人突然回头，你慌忙躲进巷子...", "清醒度-20", "money", -5),
        ("你跟丢了目标，在陌生的街道上迷失...", "清醒度-10", "money", 0),
    ],
    "drink_on_credit": [
        ("酒保让你赊账，但你已经欠了£50...", "清醒度-20", "money", -50),
        ("你被扣下来刷杯子抵债...", "清醒度-15", "money", -30),
    ],
    "hack_bank": [
        ("你对着电脑发楞，根本不知道自己在做什么...", "清醒度-5", "money", 0),
        ("屏幕上弹出一个警告: '检测到非法入侵.' 你慌忙关机...", "清醒度-15", "money", 0),
    ],
    "go_library": [
        ("图书馆今天不开门...", "清醒度-5", "money", 0),
        ("管理员看你太落魄，把你赶了出来...", "清醒度-10", "money", 0),
    ],
    "play_with_cat": [
        ("一只流浪猫抓了你一下，然后跑开了...", "清醒度-10", "money", 0),
        ("猫躺在你腿上，发出呼噜声。这是今天唯一的温暖...", "清醒度+5", "money", 0),
    ],
    "walk_in_rain": [
        ("雨水浸透了你的衣服，但你毫不在意...", "清醒度-10", "money", 0),
        ("路人用奇怪的眼光看你，你像是个彻头彻尾的笑话...", "清醒度-15", "money", 0),
    ],
    # 新增可互动动作的结果
    "begbie_gamble": [
        ("Begbie诱惑你玩骰子...", "清醒度-5", "money", 0),  # 将触发小游戏
    ],
    "drinking_contest": [
        ("酒吧里有人发起拼酒挑战...", "清醒度-5", "money", 0),  # 将触发小游戏
    ],
    "steal_bar_liquor": [
        ("你盯上了吧台后面的酒...", "清醒度-5", "money", 0),  # 将触发小游戏
    ],
    "spud_cards": [
        ("Spud提议玩纸牌...", "清醒度-5", "money", 0),  # 将触发小游戏
    ],
    "pawnshop": [
        ("你走进当铺...", "清醒度-5", "money", 0),  # 将触发小游戏
    ],
}

# ═══════════════════════════════════════════════════════════════════════════
# 随机事件库 - 极乐迪斯科风格的文学描写
# ═══════════════════════════════════════════════════════════════════════════
BASIC_EVENTS = [
    ("烟抽完了，你只能坐在黑暗中数天花板上的裂缝...", "清醒度-5"),
    ("威士忌被猫打翻了，那畜生居高临下地看着你...", "清醒度-5"),
    ("你在地上居然捡到£10! 可能是谁不小心掉的...", "清醒度+10", "money", 10),
    ("房东在砸门，房租已经欠了四个月了...", "清醒度-10", "money", -5),
    ("邻居又在放吵死人的techno，墙壁都在震动...", "清醒度-5"),
    ("手机欠费了，反正也没人会打给你...", "清醒度-5"),
    ("冰箱里只有一盒过期的牛奶...", "清醒度-10"),
    ("电源线接触不良，电脑时开时关...", "清醒度-5"),
    ("窗外在下雨，雨水顺着玻璃流下，像是你的人生...", "清醒度-5"),
    ("耳机线缠在一起了，像是你的思绪...", "清醒度-5"),
    ("彩票居然中了£20! 你怀疑是不是在做梦...", "清醒度+15", "money", 20),
    ("便利店店员多找了你£15...", "清醒度+5", "money", 15),
    ("门缝底下塞进来一张水电费账单...", "清醒度-10"),
    ("一只蟑螂从你面前大摇大摆地爬过，像是这里的主人...", "清醒度-5"),
    ("你想上厕所，却发现马桶堵了...", "清醒度-10"),
]

HEAVY_EVENTS = [
    ("警察查房了，哪怕你什么都没做，敲门声还是让你心跳加速...", "清醒度-20", "money", -10),
    ("Sick Boy骗你去借高利贷，你知道自己别无选择...", "清醒度-25", "money", -30),
    ("母亲在电话里哭: '你怎么变成这样了...' 你沉默不语...", "清醒度-30", "信誉", -15),
    ("Mark带人来要债了，你躲在天花板的夹层里不敢出声...", "清醒度-20", "money", -20),
    ("Spud把你仅剩的钱换成了一包假货，你欲哭无泪...", "清醒度-15", "money", -15),
    ("你的银行账户被冻结了，所有积蓄化为乌有...", "清醒度-20", "money", -50),
    ("Begbie在酒吧里发酒疯，砸烂了半个酒吧...", "清醒度-25", "money", -10),
    ("你走在街上被人打了闷棍，醒来时已经在巷子里...", "清醒度-30", "money", -30),
    ("房东带人来收房，你被赶出了门...", "清醒度-30", "money", -20),
    ("你试图联系Renton，但他早已音讯全无...", "清醒度-20"),
    ("你喝多了吐了一地，臭味让你自己都恶心...", "清醒度-25"),
    ("有人举报你纵火，虽然你什么都没做...", "清醒度-25", "money", -15),
    ("你的电脑中毒了，所有照片和文件都化为乌有...", "清醒度-20"),
    ("你在酒吧看到Diane挽着另一个男人的手...", "清醒度-25"),
    ("你的债主找上门来，你从窗户逃走了...", "清醒度-30", "money", -25),
]

# ═══════════════════════════════════════════════════════════════════════════
# 玩家类
# ═══════════════════════════════════════════════════════════════════════════
class HumanTrash:
    def __init__(self):
        self.cash = 50
        self.sober = 60
        self.reputation = 40
        self.withdrawal = 20
        self.anxiety = 90
        self.despair = 50
        self.day = 1
        self.round = 0
        self.hour = 12
        self.rent_due = 6
        self.choices_log = []
        self.history = []


class ChooseLifeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CHOOSE LIFE - 人生选择模拟器")
        self.root.geometry("1100x1000")
        self.root.configure(bg=BG_DARK)
        self.root.bind('<Key>', self.handle_keypress)

        self.player = HumanTrash()
        self.displayed_actions = []
        self.timer_running = False
        self.time_left = 25
        self.timer_id = None
        self.debuff_active = False
        self.game_over = False
        self.rent_amount = 40

        self.create_widgets()
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
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "bgm.wav"),
        ]
        for music_path in possible_paths:
            if os.path.exists(music_path):
                music_player.play(music_path)
                break

    def create_widgets(self):
        title = tk.Label(self.root, text="✞ CHOOSE LIFE = CHOOSE MISERY ✞",
                         font=("Courier", 16, "bold"), fg=RED, bg=BG_DARK)
        title.pack(pady=8)

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

        status_frame = tk.Frame(self.root, bg=BG_DARK, bd=1, relief="solid")
        status_frame.pack(pady=5, padx=20, fill="x")

        # 现金
        cash_frame = tk.Frame(status_frame, bg=BG_DARK)
        cash_frame.pack(fill="x", pady=2)
        tk.Label(cash_frame, text="💰 现金 £", fg=GREEN, bg=BG_DARK, width=10, anchor="w").pack(side="left")
        self.cash_var = tk.IntVar()
        self.cash_var.set(50)
        self.cash_scale = tk.Scale(cash_frame, from_=0, to=200, orient="horizontal",
                                   variable=self.cash_var, bg=BG_DARK, fg=GREEN,
                                   highlightthickness=0, length=250, showvalue=0)
        self.cash_scale.pack(side="left")
        self.cash_value_label = tk.Label(cash_frame, text="£50", fg="#00FF00", bg="#333333", bd=2, relief="solid",
                                         width=8, anchor="w", font=("Courier", 12, "bold"))
        self.cash_value_label.pack(side="left", padx=5)

        # 清醒度
        sober_frame = tk.Frame(status_frame, bg=BG_DARK)
        sober_frame.pack(fill="x", pady=2)
        tk.Label(sober_frame, text="🧠 清醒度", fg=GREEN, bg=BG_DARK, width=10, anchor="w").pack(side="left")
        self.sober_var = tk.IntVar()
        self.sober_var.set(60)
        self.sober_scale = tk.Scale(sober_frame, from_=0, to=100, orient="horizontal",
                                    variable=self.sober_var, bg=BG_DARK, fg=GREEN,
                                    highlightthickness=0, length=250, showvalue=0)
        self.sober_scale.pack(side="left")
        self.sober_value_label = tk.Label(sober_frame, text="60", fg="#00FF00", bg="#333333", bd=2, relief="solid",
                                          width=8, anchor="w", font=("Courier", 12, "bold"))
        self.sober_value_label.pack(side="left", padx=5)

        # 信誉
        rep_frame = tk.Frame(status_frame, bg=BG_DARK)
        rep_frame.pack(fill="x", pady=2)
        tk.Label(rep_frame, text="👥 信誉", fg=YELLOW, bg=BG_DARK, width=10, anchor="w").pack(side="left")
        self.rep_var = tk.IntVar()
        self.rep_var.set(40)
        self.rep_scale = tk.Scale(rep_frame, from_=0, to=100, orient="horizontal",
                                   variable=self.rep_var, bg=BG_DARK, fg=YELLOW,
                                   highlightthickness=0, length=250, showvalue=0)
        self.rep_scale.pack(side="left")
        self.rep_value_label = tk.Label(rep_frame, text="40", fg="#FFFF00", bg="#333333", bd=2, relief="solid",
                                         width=8, anchor="w", font=("Courier", 12, "bold"))
        self.rep_value_label.pack(side="left", padx=5)

        # 戒断值
        wd_frame = tk.Frame(status_frame, bg=BG_DARK)
        wd_frame.pack(fill="x", pady=2)
        tk.Label(wd_frame, text="💉 戒断值", fg=PURPLE, bg=BG_DARK, width=10, anchor="w").pack(side="left")
        self.wd_var = tk.IntVar()
        self.wd_var.set(20)
        self.wd_scale = tk.Scale(wd_frame, from_=0, to=100, orient="horizontal",
                                  variable=self.wd_var, bg=BG_DARK, fg=PURPLE,
                                  highlightthickness=0, length=250, showvalue=0)
        self.wd_scale.pack(side="left")
        self.wd_value_label = tk.Label(wd_frame, text="20", fg="#CC66FF", bg="#333333", bd=2, relief="solid",
                                        width=8, anchor="w", font=("Courier", 12, "bold"))
        self.wd_value_label.pack(side="left", padx=5)

        # 焦虑和绝望
        anx_frame = tk.Frame(status_frame, bg=BG_DARK)
        anx_frame.pack(fill="x", pady=2)
        tk.Label(anx_frame, text="😰 焦虑", fg=RED, bg=BG_DARK, width=10, anchor="w").pack(side="left")
        self.anxiety_var = tk.IntVar()
        self.anxiety_var.set(90)
        self.anxiety_scale = tk.Scale(anx_frame, from_=0, to=100, orient="horizontal",
                                      variable=self.anxiety_var, bg=BG_DARK, fg=RED,
                                      highlightthickness=0, length=150, showvalue=0)
        self.anxiety_scale.pack(side="left")
        self.anxiety_value_label = tk.Label(anx_frame, text="90", fg="#FF6666", bg="#333333", bd=2, relief="solid",
                                             width=5, anchor="w", font=("Courier", 12, "bold"))
        self.anxiety_value_label.pack(side="left", padx=5)

        tk.Label(anx_frame, text="💀 绝望", fg=RED, bg=BG_DARK, width=8, anchor="w").pack(side="left", padx=(10,0))
        self.despair_var = tk.IntVar()
        self.despair_var.set(50)
        self.despair_scale = tk.Scale(anx_frame, from_=0, to=100, orient="horizontal",
                                      variable=self.despair_var, bg=BG_DARK, fg=RED,
                                      highlightthickness=0, length=150, showvalue=0)
        self.despair_scale.pack(side="left")
        self.despair_value_label = tk.Label(anx_frame, text="50", fg="#FF6666", bg="#333333", bd=2, relief="solid",
                                             width=5, anchor="w", font=("Courier", 12, "bold"))
        self.despair_value_label.pack(side="left", padx=5)

        # 场景描述
        self.scene_label = tk.Label(self.root, text="", font=("Courier", 11),
                                    fg=GRAY, bg=BG_DARK, wraplength=850, justify="left")
        self.scene_label.pack(pady=5)

        self.hint_label = tk.Label(self.root, text="按 1-6 选择 | 25秒倒计时",
                                   font=("Courier", 10, "italic"), fg=DARK_GRAY, bg=BG_DARK)
        self.hint_label.pack()

        self.options_frame = tk.Frame(self.root, bg=BG_DARK)
        self.options_frame.pack(pady=10)

        self.option_buttons = []
        for i in range(6):
            btn = tk.Button(self.options_frame, text=f"[{i+1}] ",
                           font=("Courier", 11), fg="#FFA500", bg="#1A1A1A",
                           width=50, height=1, anchor="w",
                           command=lambda idx=i: self.make_choice(idx))
            btn.pack(pady=2)
            self.option_buttons.append(btn)

        self.result_label = tk.Label(self.root, text="",
                                     fg="#FFA500", bg=BG_DARK, wraplength=1000,
                                     justify="left", height=12)
        self.result_label.pack(pady=5, fill="both", padx=20, expand=True)

        self.event_label = tk.Label(self.root, text="",
                                    fg="#FFA500", bg=BG_DARK, wraplength=1000,
                                    justify="left", height=8)
        self.event_label.pack(pady=5, fill="both", padx=20, expand=True)

        control_frame = tk.Frame(self.root, bg=BG_DARK)
        control_frame.pack(pady=10)

        self.music_btn = tk.Button(control_frame, text="🎵 音乐: 开",
                                   font=("Courier", 10), fg=GREEN, bg=DARK_GRAY,
                                   command=self.toggle_music, width=15)
        self.music_btn.pack(side="left", padx=5)
        self.music_on = True

        self.continue_btn = tk.Button(control_frame, text="继续 >>",
                                       font=("Courier", 12, "bold"), fg=RED, bg=DARK_RED,
                                       command=self.next_round, state="disabled", width=20, height=2)
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
        if event.char in '123456' and not self.game_over:
            try:
                idx = int(event.char) - 1
                if self.option_buttons[idx]['state'] == 'normal':
                    self.cancel_timer()
                    self.make_choice(idx)
            except (ValueError, IndexError):
                pass

    def start_timer(self):
        self.timer_running = True
        self.time_left = 25
        self.update_timer()

    def update_timer(self):
        if not self.timer_running:
            return
        if self.time_left > 0:
            self.timer_label.configure(text=f"⏰ {self.time_left}s")
            self.time_left -= 1
            self.timer_id = self.root.after(1000, self.update_timer)
        else:
            self.timer_label.configure(text="超时!")
            # 随机选择一个有效选项
            idx = random.randint(0, len(self.displayed_actions) - 1) if self.displayed_actions else 0
            self.make_choice(idx)

    def cancel_timer(self):
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None

    def start_new_round(self):
        self.player.round += 1
        self.player.hour += 4
        if self.player.hour >= 24:
            self.player.hour -= 24
            self.player.day += 1

        self.time_label.configure(text=f"第{self.player.day}天 {self.player.hour}:00")
        self.rent_label.configure(text=f"房租: £{self.rent_amount} | {self.player.rent_due}轮后到期")

        self.result_label.configure(text="")
        self.event_label.configure(text="")

        time_of_day = "早上" if 6 <= self.player.hour < 12 else "下午" if 12 <= self.player.hour < 18 else "晚上"
        scenes = [
            f"【{time_of_day}】你躺在格拉斯哥贫民区的出租屋里，四周墙壁渗着霉味...\n那些霉斑像是你腐烂人生的几何图案。",
            f"【{time_of_day}】你站在浴室镜子前，镜子里的人像具腐烂的尸体。\n你不确定——究竟是你的灵魂先死了，还是你的身体先烂了。",
            f"【{time_of_day}】厨房堆着发霉餐具，你的胃在抽搐。\n饥饿和空虚，哪个更难熬？",
        ]
        self.scene_label.configure(text=random.choice(scenes))

        if self.player.withdrawal >= 80:
            self.trigger_withdrawal_event()
            return

        self.check_debuffs()
        self.check_rent()
        self.setup_options()
        self.start_timer()

    def setup_options(self):
        available_actions = [a for a in ALL_ACTIONS if a[1] not in self.player.history[-3:]]
        self.displayed_actions = random.sample(available_actions, min(6, len(available_actions)))

        for i, btn in enumerate(self.option_buttons):
            if i < len(self.displayed_actions):
                btn.configure(text=f"[{i+1}] {self.displayed_actions[i][0]}",
                             state="normal")
            else:
                btn.configure(text="", state="disabled")

    def trigger_withdrawal_event(self):
        self.cancel_timer()
        self.event_label.configure(text="⚠️ 戒断反应发作！你必须抵抗！⚠️")
        result = simpledialog.askstring("戒断发作!", "快速输入 【FUCK】 来抵抗!\n5秒倒计时...", parent=self.root)
        if result and result.upper() == "FUCK":
            self.result_label.configure(text="✓ 你抵抗成功了！戒断值-20，清醒度+15")
            self.player.withdrawal -= 20
            self.player.sober = min(100, self.player.sober + 15)
        else:
            self.result_label.configure(text="✗ 你抵抗失败了！清醒度直接归0！")
            self.player.sober = 0
            self.player.withdrawal += 10
        self.update_status()
        self.continue_btn.configure(state="normal")

    def check_debuffs(self):
        if self.player.sober < 20 and not self.debuff_active:
            self.debuff_active = True
            self.event_label.configure(text=self.event_label.cget("text") + "\n⚠️ 清醒度太低！你手抖看不清选项！")
        elif self.player.sober >= 20 and self.debuff_active:
            self.debuff_active = False

    def check_rent(self):
        self.player.rent_due -= 1
        if self.player.rent_due <= 0:
            if self.player.cash >= 40:
                self.player.cash -= 40
                self.player.rent_due = 6
                self.event_label.configure(text="✓ 你交了房租£40，还剩£" + str(self.player.cash))
            else:
                self.show_ending("landlord")
                return
        if self.player.cash < 0:
            self.show_ending("debt")

    def update_status(self):
        self.cash_var.set(max(0, self.player.cash))
        self.sober_var.set(max(0, self.player.sober))
        self.rep_var.set(max(0, self.player.reputation))
        self.wd_var.set(max(0, self.player.withdrawal))
        self.anxiety_var.set(max(0, min(100, self.player.anxiety)))
        self.despair_var.set(max(0, min(100, self.player.despair)))

        self.cash_value_label.configure(text=f"£{self.player.cash}")
        self.sober_value_label.configure(text=str(self.player.sober))
        self.rep_value_label.configure(text=str(self.player.reputation))
        self.wd_value_label.configure(text=str(self.player.withdrawal))
        self.anxiety_value_label.configure(text=str(self.player.anxiety))
        self.despair_value_label.configure(text=str(self.player.despair))

    def make_choice(self, idx):
        if idx >= len(self.displayed_actions):
            return
        self.cancel_timer()
        for btn in self.option_buttons:
            btn.configure(state="disabled")

        action_name, action_id = self.displayed_actions[idx]
        self.player.choices_log.append(action_name)
        self.player.history.append(action_id)

        # 特殊互动
        if action_id == "call_parents":
            self.handle_call_parents()
            return
        if action_id == "text_diane":
            self.handle_text_diane()
            return
        if action_id == "call_sick_boy":
            self.handle_call_sick_boy()
            return
        if action_id == "call_mark":
            self.handle_call_mark()
            return
        if action_id == "contact_renton":
            self.handle_contact_renton()
            return
        if action_id == "dumpster_dive":
            self.handle_dumpster_dive()
            return
        if action_id == "find_job":
            self.handle_find_job()
            return
        if action_id == "begbie_gamble":
            self.handle_begbie_gamble()
            return
        if action_id == "drinking_contest":
            self.handle_drinking_contest()
            return
        if action_id == "steal_bar_liquor":
            self.handle_steal_bar_liquor()
            return
        if action_id == "spud_cards":
            self.handle_spud_cards()
            return
        if action_id == "pawnshop":
            self.handle_pawnshop()
            return

        results = CHOICE_RESULTS.get(action_id, [("你做了点什么...", "清醒度-5", "money", 0)])
        result_text, stat1, stat2, val = random.choice(results)

        # 记录变化前的现金
        old_cash = self.player.cash

        self.result_label.configure(text=f"► 你选择了：{action_name}\n{result_text}")
        self.apply_effect(stat1, val)
        if stat2:
            self.apply_effect(stat2, val)

        # 计算金钱变化
        money_change = self.player.cash - old_cash
        if money_change != 0:
            change_text = f"💰 现金: {'+' if money_change > 0 else ''}{money_change} (现在: £{self.player.cash})"
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{change_text}")

        self.trigger_events()
        self.update_status()

        if self.player.reputation < 20:
            self.event_label.configure(text=self.event_label.cget("text") + "\n⚠️ 信誉太低！所有朋友都背叛了你！")

        if self.player.sober <= 0:
            self.show_ending("sober")
            return
        if self.player.cash < 0:
            self.show_ending("debt")
            return

        self.continue_btn.configure(state="normal")

    def apply_effect(self, stat, val):
        if stat == "money":
            self.player.cash = max(0, self.player.cash + val)
        elif stat == "清醒度":
            self.player.sober = max(0, min(100, self.player.sober + val))
        elif stat == "信誉":
            self.player.reputation = max(0, min(100, self.player.reputation + val))
        elif stat == "戒断值":
            self.player.withdrawal = max(0, min(100, self.player.withdrawal + val))
        elif stat == "焦虑":
            self.player.anxiety = max(0, min(100, self.player.anxiety + val))
        elif stat == "绝望":
            self.player.despair = max(0, min(100, self.player.despair + val))

    def trigger_events(self):
        if random.random() < 0.4:
            if random.random() < 0.8:
                event = random.choice(BASIC_EVENTS)
            else:
                event = random.choice(HEAVY_EVENTS)
                self.apply_effect("清醒度", -15)
                self.apply_effect("绝望", 10)
            event_text = event[0]
            self.event_label.configure(text=self.event_label.cget("text") + f"\n✞ {event_text} ✞")
            if len(event) >= 4:
                self.apply_effect(event[2], event[3])

    # ═══════════════════════════════════════════════════════════════════════════
    # 特殊互动处理器
    # ═══════════════════════════════════════════════════════════════════════════
    def handle_call_parents(self):
        choice = simpledialog.askstring("给父母打电话",
            "你对着电话说:\n1. 爸妈，我错了，我想回家\n2. 能打点钱给我吗?\n3. 没什么事，就是想听听你们声音\n输入 1, 2 或 3:",
            parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：给父母打电话\n\n电话那头沉默了很久...\n\n母亲的声音有些哽咽: '儿子，你终于想通了...'\n\n她给你转了£50，让 你回家。")
            self.player.cash += 50
            self.player.reputation += 20
            self.player.despair -= 20
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：给父母打电话\n\n父亲在电话那头咆哮:\n'你还有脸跟我们要钱?!'\n\n他把电话挂了。")
            self.player.reputation -= 15
            self.player.despair += 10
        elif choice == "3":
            self.result_label.configure(text="► 你选择了：给父母打电话\n\n母亲哽咽着说:\n'儿子，妈想你了...'\n\n她悄悄给你转了£30。")
            self.player.cash += 30
            self.player.reputation += 10
            self.player.despair -= 10
        else:
            self.result_label.configure(text="► 你选择了：给父母打电话\n\n你犹豫了一下，还是把电话挂了。")

        self.finish_turn()

    def handle_text_diane(self):
        choice = simpledialog.askstring("给Diane发短信",
            "你编写着短信:\n1. Diane，我 想你了...\n2. 最近怎么样? 有空出来喝一杯?\n3. 对不起，之前是我不对...\n输入 1, 2 或 3:",
            parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：给Diane发短信\n\nDiane很快回复:\n'你在开什么玩笑? 我们已经结束了。'\n\n她把你拉黑了。")
            self.player.reputation -= 20
            self.player.despair += 15
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：给Diane发短信\n\nDiane过了很久回复:\n'我现在很忙。'\n\n你知道她只是不想见你。")
            self.player.despair += 5
        elif choice == "3":
            self.result_label.configure(text="► 你选择了：给Diane发短信\n\nDiane回了:\n'我考虑考虑...'\n\n第二天她给你转了£20。")
            self.player.cash += 20
            self.player.reputation += 10
        else:
            self.result_label.configure(text="► 你选择了：给Diane发短信\n\n你最终还是没有发送。")

        self.finish_turn()

    def handle_call_sick_boy(self):
        choice = simpledialog.askstring("给Sick Boy打电话",
            "Sick Boy接起电话:\n'哟，找我啥事?'\n1. 有好货吗?\n2. 有什么来钱的活吗?\n3. 没什么，挂了啊\n输入 1, 2 或 3:",
            parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：给Sick Boy打电话\n\nSick Boy说: '有啊，最新的货，£30'\n\n你买了一包...结果发现是面粉。")
            self.player.cash -= 30
            self.player.withdrawal += 20
            self.player.despair += 10
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：给Sick Boy打电话\n\nSick Boy淫笑:\n'有个好活，帮我送点货，给你 £50'")
            if random.random() < 0.6:
                self.result_label.configure(text=self.result_label.cget("text") + "\n\n你成功完成了送货!\nSick Boy给了你 £50!")
                self.player.cash += 50
                self.player.reputation += 15
            else:
                self.result_label.configure(text=self.result_label.cget("text") + "\n\n警察! 你拔腿就跑!\n好不容 易逃脱，但钱没拿到。")
                self.player.despair += 10
        else:
            self.result_label.configure(text="► 你选择了：给Sick Boy打电话\n\nSick Boy骂了一句就挂了。")

        self.finish_turn()

    def handle_call_mark(self):
        choice = simpledialog.askstring("给Mark打电话",
            "Mark接起电话:\n'干啥?'\n1. Mark，借我点钱...\n2. 我想见见你...\n3. 打错了\n输入 1, 2 或 3:",
            parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：给Mark打电话\n\nMark沉默了一下:\n'...等着，我给你转点'\n\n他给你转了£20")
            self.player.cash += 20
            self.player.reputation += 5
        elif choice == "2":
            if random.random() < 0.5:
                self.result_label.configure(text="► 你选择了：给Mark打电话\n\nMark说在老地方酒吧等你\n\n你去了，他请你喝了一杯。")
                self.player.sober -= 15
            else:
                self.result_label.configure(text="► 你选择了：给Mark打电话\n\nMark说他很忙...\n\n你知道他在躲你。")
        else:
            self.result_label.configure(text="► 你选择了：给Mark打电话\n\n你快速挂断了电话。\n\n手在颤抖。")

        self.finish_turn()

    def handle_contact_renton(self):
        choice = simpledialog.askstring("联系Renton",
            "你知道Renton在伦敦...\n1. 给他写信\n2. 打电话给他\n3. 算了吧\n输入 1, 2 或 3:",
            parent=self.root)

        if choice == "1":
            self.result_label.configure(text="► 你选择了：联系Renton\n\n你写了一封很长的信...\n\n一周后你收到了回信:\n'Renton... 我现在不太好... £30 是我最后的帮助了...'")
            self.player.cash += 30
            self.player.despair -= 15
        elif choice == "2":
            self.result_label.configure(text="► 你选择了：联系Renton\n\n电话通了...\n\n'Renton?'\n\n然后是一阵忙音。\n\n他可能已经换号了。")
            self.player.despair += 10
        else:
            self.result_label.configure(text="► 你选择了：联系Renton\n\n你放弃了。\n\n也许他早就把你忘了。")
            self.player.despair += 5

        self.finish_turn()

    def handle_dumpster_dive(self):
        self.result_label.configure(text="► 你选择了：翻垃圾桶\n\n快速点击按钮10次来翻找!")

        dialog = tk.Toplevel(self.root)
        dialog.title("翻垃圾桶")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_DARK)

        clicks = [0]
        max_clicks = 10

        def on_click():
            clicks[0] += 1
            btn.configure(text=f"已点击: {clicks[0]}/{max_clicks}")
            if clicks[0] >= max_clicks:
                dialog.after(100, dialog.destroy)

        tk.Label(dialog, text="快速点击按钮10次!", fg=YELLOW, bg=BG_DARK,
                 font=("Courier", 14)).pack(pady=20)

        btn = tk.Button(dialog, text="点击翻找!", fg=GREEN, bg=DARK_GRAY,
                       font=("Courier", 20), width=15, height=3, command=on_click)
        btn.pack(pady=20)

        dialog.wait_window()

        treasures = [
            ("半块发霉的面包", 5, -5),
            ("一包过期的薯片", 2, -2),
            ("£15现金!", 15, 0),
            ("空的啤酒罐", 1, 0),
            ("居然捡到£30!", 30, 0),
            ("一条发臭的鱼", -5, -10),
        ]

        if clicks[0] >= 8:
            item = treasures[4]
        elif clicks[0] >= 5:
            item = treasures[2]
        else:
            item = treasures[0]

        self.result_label.configure(text=self.result_label.cget("text") +
            f"\n\n你找到了: {item[0]}!\n现金: £{item[1]}, 清醒度: {item[2]}")
        self.player.cash = max(0, self.player.cash + item[1])
        self.player.sober = max(0, min(100, self.player.sober + item[2]))
        self.finish_turn()

    def handle_find_job(self):
        self.result_label.configure(text="► 你选择了：找工作\n\n需要进行面试!")

        choice = simpledialog.askstring("面试",
            "面试官问: 你为什么想来这里工作?\n1. 因为我需要钱\n2. 我热爱工作\n3. 没为什么\n输入 1, 2 或 3:",
            parent=self.root)

        score = 0
        if choice == "1":
            score += 2
            score_text = "面试官点了点头"
        elif choice == "2":
            score += 1
            score_text = "面试官茫然看着你"
        else:
            score_text = "面试官皱起眉头"

        choice2 = simpledialog.askstring("面试",
            "面试官问: 你的最长工作时间 是?\n1. 一天\n2. 一星期\n3. 我很勤奋\n输入 1, 2 或 3:",
            parent=self.root)

        if choice2 == "1":
            score += 2
        elif choice2 == "2":
            score += 1

        if score >= 3:
            self.result_label.configure(text=self.result_label.cget("text") +
                f"\n\n{score_text}\n\n恭喜! 你被录取了!\n日薪£50!")
            self.player.cash += 50
            self.player.sober += 10
        elif score >= 1:
            self.result_label.configure(text=self.result_label.cget("text") +
                f"\n\n{score_text}\n\n面试官说会考虑...\n\n三天后你收到通知，被录用! 日薪£25")
            self.player.cash += 25
        else:
            self.result_label.configure(text=self.result_label.cget("text") +
                f"\n\n{score_text}\n\n面试官摆 了摆手:\n'你可以走了。'")

        self.finish_turn()

    # ═══════════════════════════════════════════════════════════════════════════
    # 新增互动小游戏
    # ═══════════════════════════════════════════════════════════════════════════
    def handle_begbie_gamble(self):
        """Begbie的骰子赌博游戏"""
        self.result_label.configure(text="► 你选择了：和Begbie赌博\n\nBegbie拿出三颗骰子:\n'赌大小，£20一次。'\n\n在三颗骰子上点击选择你的猜测方向!")

        dialog = tk.Toplevel(self.root)
        dialog.title("Begbie的赌博")
        dialog.geometry("400x250")
        dialog.configure(bg=BG_DARK)

        result_label = tk.Label(dialog, text="点击下方按钮选择:", fg="#FFA500", bg=BG_DARK,
                               font=("Courier", 14)).pack(pady=20)

        bet_amount = 20
        result_text = ""

        def bet_big():
            nonlocal result_text
            dice = [random.randint(1, 6) for _ in range(3)]
            total = sum(dice)
            win = total >= 11  # 大: 11-18
            result_text = f"骰子: {dice} = {total}\n"
            if win:
                result_text += f"你赢了! 获得 £{bet_amount}!"
                self.player.cash += bet_amount
            else:
                result_text += f"你输了! 失去 £{bet_amount}!"
                self.player.cash -= bet_amount
            dialog.destroy()

        def bet_small():
            nonlocal result_text
            dice = [random.randint(1, 6) for _ in range(3)]
            total = sum(dice)
            win = total <= 10  # 小: 3-10
            result_text = f"骰子: {dice} = {total}\n"
            if win:
                result_text += f"你赢了! 获得 £{bet_amount}!"
                self.player.cash += bet_amount
            else:
                result_text += f"你输了! 失去 £{bet_amount}!"
                self.player.cash -= bet_amount
            dialog.destroy()

        btn_frame = tk.Frame(dialog, bg=BG_DARK)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🔴 押 大 (11-18)", fg=RED, bg=DARK_GRAY,
                  font=("Courier", 14), width=15, command=bet_big).pack(pady=5)
        tk.Button(btn_frame, text="🔵 押 小 (3-10)", fg="#4169E1", bg=DARK_GRAY,
                  font=("Courier", 14), width=15, command=bet_small).pack(pady=5)

        dialog.wait_window()

        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
        self.finish_turn()

    def handle_drinking_contest(self):
        """酒吧拼酒小游戏"""
        self.result_label.configure(text="► 你选择了：在酒吧拼酒\n\n酒保说:\n'谁能在10秒内喝完5杯龙舌兰,奖金£30!'\n\n快速点击按钮完成挑战!")

        dialog = tk.Toplevel(self.root)
        dialog.title("拼酒挑战")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_DARK)

        clicks = [0]
        max_clicks = 5
        start_time = time.time()
        success = [False]

        def on_click():
            clicks[0] += 1
            btn.configure(text=f"已喝: {clicks[0]}/{max_clicks} 杯")
            if clicks[0] >= max_clicks:
                elapsed = time.time() - start_time
                if elapsed <= 10:
                    success[0] = True
                dialog.destroy()

        tk.Label(dialog, text="10秒内喝完5杯!", fg="#FFA500", bg=BG_DARK,
                 font=("Courier", 14)).pack(pady=20)

        btn = tk.Button(dialog, text="开始喝酒!", fg=GREEN, bg=DARK_GRAY,
                       font=("Courier", 20), width=15, height=2, command=on_click)
        btn.pack(pady=20)

        dialog.wait_window()

        if success[0]:
            result_text = f"✓ 你在{time.time()-start_time:.1f}秒内喝完了!\n获得 £30!"
            self.player.cash += 30
            self.player.sober -= 20
        else:
            result_text = "✗ 你喝得太慢了...\n没有得到奖金"
            self.player.sober -= 10

        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
        self.finish_turn()

    def handle_steal_bar_liquor(self):
        """偷酒小游戏 - 时机游戏"""
        self.result_label.configure(text="► 你选择了：偷酒吧的酒\n\n你趁酒保转身时下手...\n\n注意! 等到绿色时点击才能成功!")

        dialog = tk.Toplevel(self.root)
        dialog.title("偷酒")
        dialog.geometry("400x250")
        dialog.configure(bg=BG_DARK)

        # 游戏状态
        colors = ["#FF0000", "#FF6600", "#FFFF00", "#00FF00", "#00FF00", "#FF0000"]
        color_names = ["太早!", "太早!", "准备...", "抢!", "成功!", "太晚!"]
        current_idx = [0]
        game_running = [True]
        result_text = ""

        def change_color():
            if not game_running[0]:
                return
            current_idx[0] = (current_idx[0] + 1) % len(colors)
            indicator.configure(bg=colors[current_idx[0]], text=color_names[current_idx[0]])
            if current_idx[0] < 4:
                dialog.after(500 + random.randint(200, 800), change_color)
            else:
                game_running[0] = False

        def try_steal():
            if not game_running[0]:
                return
            game_running[0] = False
            nonlocal result_text
            if current_idx[0] in [3, 4]:  # 绿色
                result_text = "✓ 你成功偷到一瓶好酒!\n当掉获得 £25"
                self.player.cash += 25
            else:
                result_text = "✗ 被发现了! 你拔腿就跑,\n什么都没拿到"
                self.player.sober -= 10
            dialog.destroy()

        indicator = tk.Label(dialog, text="等待...", fg=BLACK, bg="#FF0000",
                           font=("Courier", 24, "bold"), width=10, height=3)
        indicator.pack(pady=20)

        tk.Button(dialog, text="动手!", fg=RED, bg=DARK_GRAY,
                  font=("Courier", 16), width=15, height=2, command=try_steal).pack(pady=20)

        dialog.after(1000 + random.randint(500, 2000), change_color)
        dialog.wait_window()

        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
        self.finish_turn()

    def handle_spud_cards(self):
        """和Spud玩纸牌"""
        self.result_label.configure(text="► 你选择了：和Spud玩纸牌\n\nSpud洗着牌:\n'21点, £15一次. 超过21点算爆.'\n\n输入你的选择: 要牌(Y)或停止(N)\n(输入 y 或 n, 会进行3次选择)")

        choice = simpledialog.askstring("21点",
            "你的初始两张牌:\nJ和5 = 15点\n\n要牌(y)或停止(n)?",
            parent=self.root)

        player_total = 15
        result_text = ""

        if choice and choice.lower() == 'y':
            card = random.randint(2, 11)
            player_total += card
            if player_total > 21:
                result_text = f"你抽到了{card}, 总共{player_total}点 - 爆了!\n你输了£15"
                self.player.cash -= 15
            else:
                # 第二次选择
                choice2 = simpledialog.askstring("21点",
                    f"你现在{player_total}点\n要牌(y)或停止(n)?",
                    parent=self.root)
                if choice2 and choice2.lower() == 'y':
                    card2 = random.randint(2, 11)
                    player_total += card2
                    if player_total > 21:
                        result_text = f"你抽到了{card2}, 总共{player_total}点 - 爆了!\n你输了£15"
                        self.player.cash -= 15
                    else:
                        result_text = f"你停牌, {player_total}点.\n"
                else:
                    result_text = f"你停牌, {player_total}点.\n"
        else:
            result_text = f"你停牌, {player_total}点.\n"

        # Spud的牌
        spud_total = random.randint(15, 21)
        result_text += f"Spud: {spud_total}点\n"

        if player_total <= 21:
            if player_total > spud_total:
                result_text += "✓ 你赢了! 获得 £15!"
                self.player.cash += 15
            elif player_total == spud_total:
                result_text += "平局! 钱退给你."
            else:
                result_text += "✗ 你输了."
                self.player.cash -= 15
        else:
            result_text += "✗ 你已经爆了."

        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
        self.finish_turn()

    def handle_pawnshop(self):
        """当铺讨价还价"""
        self.result_label.configure(text="► 你选择了：去当铺\n\n当铺老板抬头看你:\n'有什么要当的?'")

        choice = simpledialog.askstring("当铺",
            "你有什么可以当的?\n1. 旧手表 (值£20)\n2. 收音机 (值£15)\n3. 相机 (值£30)\n4. 什么都不当\n输入 1, 2, 3 或 4:",
            parent=self.root)

        result_text = ""

        if choice == "1":
            result_text = "你拿出旧手表...\n老板看了看: '£8, 要当就当.'\n\n你与他讨价还价..."
            offer = 8
        elif choice == "2":
            result_text = "你拿出收音机...\n老板按下开关: '坏的. £5, 爱当不当.'\n\n你与他讨价还价..."
            offer = 5
        elif choice == "3":
            result_text = "你拿出相机...\n老板检查了一下: '镜头花了. £15.'\n\n你与他讨价还价..."
            offer = 15
        else:
            result_text = "你看了一圈, 什么都没当."
            self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
            self.finish_turn()
            return

        # 讨价还价小游戏
        counter = simpledialog.askstring("讨价还价",
            f"老板开价£{offer}, 你想加多少?\n(输入数字, 如 5 表示要加£5)\n或者直接回车接受:",
            parent=self.root)

        if counter:
            try:
                add = int(counter)
                final_offer = offer + add
                if final_offer <= offer * 1.5:  # 最高加50%
                    result_text += f"\n老板摇头: '不行, {final_offer}太多了.'"
                    result_text += f"\n最终以 £{offer} 当掉."
                    self.player.cash += offer
                else:
                    result_text += f"\n老板叹气: '行行行, 你的了. £{final_offer}'"
                    self.player.cash += final_offer
            except:
                result_text += f"\n你接受了 £{offer}."
                self.player.cash += offer
        else:
            result_text += f"\n你接受了 £{offer}."
            self.player.cash += offer

        self.result_label.configure(text=self.result_label.cget("text") + f"\n\n{result_text}")
        self.finish_turn()

    def finish_turn(self):
        self.trigger_events()
        self.update_status()

        # 在结果中显示当前现金
        self.result_label.configure(text=self.result_label.cget("text") +
            f"\n\n💰 当前现金: £{self.player.cash}")

        if self.player.reputation < 20:
            self.event_label.configure(text=self.event_label.cget("text") + "\n⚠️ 信誉太低！所有朋友都背叛了你！")

        if self.player.sober <= 0:
            self.show_ending("sober")
            return
        if self.player.cash < 0:
            self.show_ending("debt")
            return

        self.continue_btn.configure(state="normal")

    def next_round(self):
        self.player.withdrawal = min(100, self.player.withdrawal + 5)
        self.player.sober = min(100, self.player.sober + 5)
        self.continue_btn.configure(state="disabled")
        self.start_new_round()

    def show_ending(self, reason):
        self.game_over = True
        self.cancel_timer()

        endings = {
            "normal": ("混沌烂局", "你选了那么久，最后还是回到这间出租屋...\n\n钱花光了，朋友背叛了，清醒度归零了。\n\n你终于明白了：\n\n人生就是TM一坨屎——\n而你只是屎上那只蠕动的蛆。"),
            "landlord": ("被赶出门", "房东把你赶出来了！\n\n你连房租都交不起，还谈什么人生？\n\n滚出去喝西北风吧！\n\n——不过想想，你本来就 在喝西北风。"),
            "debt": ("债务爆炸", "你欠了一屁股债！\n\n追债的天天上门，你还能躲去哪？"),
            "sober": ("清醒度归零", "你终于彻底麻木了...\n\n清醒度归零，你活着跟死了有什么区别？\n\n没有。\n\n真的没有。"),
        }

        title, text = endings.get(reason, endings["normal"])
        self.save_record(title)

        reply = messagebox.askretrycancel(
            f"✞ {title} ✞",
            f"{text}\n\n存活: {self.player.day}天 {self.player.round}轮\n\n再来一局？"
        )

        if reply:
            self.player = HumanTrash()
            self.game_over = False
            self.debuff_active = False
            self.start_new_round()
        else:
            self.root.quit()

    def save_record(self, ending_type):
        try:
            with open("人生烂账.txt", "w", encoding="utf-8") as f:
                f.write("=" * 50 + "\n")
                f.write("人生烂账 —— 你的失败全记录\n")
                f.write("=" * 50 + "\n\n")
                f.write(f"结局: {ending_type}\n")
                f.write(f"存活: {self.player.day}天 {self.player.round}轮\n")
                f.write(f"现金: £{self.player.cash}\n")
                f.write(f"清醒度: {self.player.sober}\n")
                f.write(f"信誉: {self.player.reputation}\n")
                f.write(f"戒断值: {self.player.withdrawal}\n\n")
                f.write("-" * 50 + "\n")
                f.write("你的选择:\n")
                for i, c in enumerate(self.player.choices_log, 1):
                    f.write(f"  {i}. {c}\n")
                f.write("\n这就是你的人生——烂，且无解\n")
        except:
            pass


def main():
    root = tk.Tk()
    app = ChooseLifeGame(root)
    root.mainloop()


if __name__ == "__main__":
    main()
