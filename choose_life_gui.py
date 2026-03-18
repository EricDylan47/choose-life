#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
✞ CHOOSE LIFE = CHOOSE YOUR MISERY ✞
人生选择模拟器 —— 终极混沌版 v2.0
================================================================================
# 清醒度？只是你骗自己还能撑下去的幻觉
# 信誉？你就是个骗子，别装了
# 戒断？你的身体早就不属于你了
================================================================================
"""

import tkinter as tk
from tkinter import messagebox, simpledialog, ttk
import random
import time
import threading
import subprocess
import os
import sys
import json
from datetime import datetime

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
# 颜色定义 - 增强版配色方案
# ═══════════════════════════════════════════════════════════════════════════
RED = '#FF4444'
DARK_RED = '#8B0000'
GRAY = '#808080'
DARK_GRAY = '#404040'
BLACK = '#0D0D0D'
BG_DARK = '#121212'
BG_MEDIUM = '#1E1E1E'
BG_LIGHT = '#2D2D2D'
YELLOW = '#FFD700'
ORANGE = '#FFA500'
GREEN = '#00FF7F'
PURPLE = '#9B59B6'
CYAN = '#00CED1'
PINK = '#FF69B4'

# 状态条颜色
COLORS = {
    'cash': '#2ECC71',      # 绿色 - 现金
    'sober': '#3498DB',     # 蓝色 - 清醒度
    'reputation': '#F39C12', # 橙色 - 信誉
    'withdrawal': '#9B59B6', # 紫色 - 戒断值
    'anxiety': '#E74C3C',   # 红色 - 焦虑
    'despair': '#1ABC9C',   # 青色 - 绝望
}

# ═══════════════════════════════════════════════════════════════════════════
# ASCII 艺术
# ═══════════════════════════════════════════════════════════════════════════
ASCII_ART = r"""
    ___    __    ___  _       __   _  _  ____     ____  ___  __  __  ____
   / __)  /  \  / __)( )     (  ) ( )( )(  _ \   (  _ \(  _)(  )(  )(  _ \
  ( ( _  (  O )( (__ | |____  )(__  __  (  ) )   )___/ ) _)  )(__  (  ) )
   \__)  \__/  \___)(______)(______)(_)(__\_)  (__)  (__)   (____)(__\_)
"""

TITLE_ART = """
████████╗ ██████╗  ██████╗ ██╗    ██╗███╗   ██╗
╚══██╔══╝██╔═══██╗██╔══██╗██║    ██║████╗  ██║
   ██║   ██║   ██║██████╔╝██║ █╗ ██║██╔██╗ ██║
   ██║   ██║   ██║██╔══██╗██║███╗██║██║╚██╗██║
   ██║   ╚██████╔╝██║  ██║╚███╔███╔╝██║ ╚████║
   ╚═╝    ╚═════╝ ╚═╝  ╚═╝ ╚══╝╚══╝ ╚═╝  ╚═══╝
   ██████╗ ███████╗████████╗██████╗  ██████╗
   ██╔══██╗██╔════╝╚══██╔══╝██╔══██╗██╔═══██╗
   ██████╔╝█████╗     ██║   ██████╔╝██║   ██║
   ██╔══██╗██╔══╝     ██║   ██╔══██╗██║   ██║
   ██║  ██║███████╗   ██║   ██║  ██║╚██████╔╝
   ╚═╝  ╚═╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝
"""

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
    # 新增剧情分支
    ("去诊所看医生", "see_doctor"),
    ("在公园遇到流浪歌手", "meet_busker"),
    ("接神秘电话", "mysterious_call"),
    ("参加互助会", "support_group"),
    ("偷看Diane的社交账号", "stalk_diane_social"),
    ("尝试向Sick Boy进货", "buy_from_sick_boy"),
    ("在医院急诊室", "emergency_room"),
    ("遇到传教士", "meet_preacher"),
    ("在码头吹风", "pier_contemplation"),
    ("偷流浪猫的猫粮", "steal_cat_food"),
    ("和毒贩做交易", "dealer_transaction"),
    ("参加地下拳击", "underground_boxing"),
    ("在图书馆撩志愿者", "library_romance"),
    ("接私活当打手", "hitman_job"),
    ("在教堂偷奉献箱", "steal_offering"),
    ("遇到旧相识", "meet_old_friend"),
    ("尝试网络诈骗", "online_scam"),
    # === 新增深度剧情分支 ===
    ("去心理咨询", "therapy_session"),
    ("参加瑜伽课程", "yoga_class"),
    ("写日记记录生活", "journal_writing"),
    ("深夜电台倾诉", "radio_confession"),
    ("在雨中漫步", "rain_walk"),
    ("去动物园看动物", "zoo_visit"),
    ("尝试冥想", "meditation"),
    ("给未来的自己写信", "future_letter"),
    ("在酒吧当临时工", "bar_temp"),
    ("参加诗歌朗诵会", "poetry_club"),
    ("学习烹饪", "cooking_class"),
    ("去旧书店淘宝", "used_bookstore"),
    ("志愿者活动", "volunteer_work"),
    ("观看日出", "watch_sunrise"),
    ("制定人生计划", "life_plan"),
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
    # 新增剧情分支的结果
    "see_doctor": [
        ("医生给你做了检查，摇头叹气...", "清醒度+20", "money", -10),
        ("护士帮你量了血压，说你活不久了...", "清醒度+10", "money", -5),
        ("医生开了点药，免费的...", "清醒度+15", "money", 0),
    ],
    "meet_busker": [
        ("流浪歌手给你唱了一首伤感的歌，你听入了迷...", "清醒度+10", "money", 0),
        ("你给了歌手£5，他教你弹吉他...", "清醒度+15", "money", -5),
        ("歌手看你可怜，给你£5...", "清醒度+5", "money", 5),
    ],
    "mysterious_call": [
        ("电话那头传来熟悉的声音: '我知道你的秘密...' - 你吓出一身冷汗", "焦虑+20", "money", 0),
        ("一个陌生女人哭着说打错了...", "清醒度-5", "money", 0),
        ("沉默...然后挂断了。你彻夜难眠...", "焦虑+15", "清醒度-10", 0),
    ],
    "support_group": [
        ("你参加了戒毒互助会，大家分享着自己的故事...", "清醒度+20", "信誉+10", 0),
        ("你听到别人的悲惨故事，觉得自己还算幸运...", "清醒度+15", "绝望-10", 0),
        ("有人对你指指点点，你愤怒离场...", "清醒度-10", "信誉-15", 0),
    ],
    "stalk_diane_social": [
        ("Diane有了新男友，看起来很幸福...", "绝望+25", "清醒度-15", 0),
        ("Diane发了很多emo动态，你们曾经那么美好...", "绝望+15", "焦虑+10", 0),
        ("她的生活跟你完全无关了...", "清醒度-5", "绝望+10", 0),
    ],
    "buy_from_sick_boy": [
        ("Sick Boy给你介绍了'好货'...", "戒断值-30", "money", -40),
        ("你买了假货，被坑了£30...", "戒断值+10", "money", -30),
        ("Sick Boy说最近缺货，让你等几天...", "戒断值+15", "money", 0),
    ],
    "emergency_room": [
        ("急诊室医生救了你一命...", "清醒度+30", "money", -50),
        ("护士帮你包扎了伤口...", "清醒度+10", "money", -20),
        ("你只是喝多了，被赶了出来...", "清醒度-15", "money", -5),
    ],
    "meet_preacher": [
        ("传教士试图拯救你的灵魂...", "清醒度+10", "money", -5),
        ("你把传教士骂走了...", "清醒度-10", "信誉-5", 0),
        ("传教士给了你一点钱买吃的...", "清醒度+5", "money", 10),
    ],
    "pier_contemplation": [
        ("海风吹拂，你想起曾经美好的日子...", "清醒度+15", "绝望-10", 0),
        ("你看到一艘船驶过，梦想着离开这里...", "清醒度+10", "焦虑+5", 0),
        ("一个老头给你讲了他的人生故事...", "清醒度+5", "绝望-5", 0),
    ],
    "steal_cat_food": [
        ("你偷了流浪猫的猫粮，至少能充饥...", "清醒度+5", "money", 0),
        ("猫抓了你一下，你感染了...", "清醒度-10", "money", -10),
        ("猫粮难吃得要命，但你别无选择...", "清醒度+5", "绝望+5", 0),
    ],
    "dealer_transaction": [
        ("你和毒贩交易，被警察看到了!", "戒断值-25", "money", -50),
        ("毒贩看你可怜，赊了你一点...", "戒断值-20", "money", -10),
        ("交易顺利，你拿到了货...", "戒断值-30", "money", -35),
    ],
    "underground_boxing": [
        ("你被打得鼻青脸肿，但赢了£50!", "清醒度-20", "money", 50),
        ("你被打趴下了，医药费花了£30...", "清醒度-25", "money", -30),
        ("你打赢了对手，赢得了尊重!", "清醒度-15", "money", 80, "信誉", 15),
    ],
    "library_romance": [
        ("你和志愿者聊了起来，感觉还不错...", "清醒度+15", "绝望-10", 0),
        ("她对你没兴趣，礼貌地走开了...", "清醒度-5", "绝望+5", 0),
        ("你们交换了联系方式...", "清醒度+10", "焦虑-5", 0),
    ],
    "hitman_job": [
        ("你接了私活，成功完成了任务，得到£100!", "money", 100, "信誉", 20),
        ("任务失败，你被打了一顿...", "清醒度-30", "money", -20),
        ("你临阵退缩了，太危险了...", "信誉-10", "money", 0),
    ],
    "steal_offering": [
        ("你偷了奉献箱里的钱£20...", "money", 20, "信誉", -25),
        ("被抓住了! 神父报警了...", "money", 0, "信誉", -40),
        ("你良心不安，把钱放了回去...", "信誉+5", "清醒度+10", 0),
    ],
    "meet_old_friend": [
        ("你遇到了的老同学，他现在混得很好...", "绝望+20", "清醒度-10", 0),
        ("老朋友请了你一顿饭，聊了很多...", "清醒度+10", "money", 15),
        ("他答应帮你找工作...", "清醒度+15", "信誉+10", 0),
    ],
    "online_scam": [
        ("你骗到了£30! 但良心不安...", "money", 30, "焦虑+15", 0),
        ("你被对方反套路了亏了£20...", "money", -20, "焦虑+10", 0),
        ("你成功骗了一笔大的£100!", "money", 100, "信誉", -20),
    ],
    # === 新增深度剧情 ===
    "therapy_session": [
        ("心理咨询师认真倾听你的故事，你第一次感到被理解...", "清醒度+25", "焦虑-15"),
        ("医生给你开了安眠药，免费的...", "清醒度+15", "money", -5),
        ("你觉得这些都是bullshit，甩门而去...", "清醒度-5", "信誉-10"),
    ],
    "yoga_class": [
        ("跟着老师做瑜伽，身体渐渐放松，脑子也不那么乱了...", "清醒度+20", "焦虑-10"),
        ("你笨手笨脚地被别人嘲笑，但感觉还不错...", "清醒度+10", "money", -15),
        ("课后的冥想让你找到了片刻宁静...", "清醒度+15", "绝望-5"),
    ],
    "journal_writing": [
        ("你把所有的痛苦都写了下来，笔尖触及灵魂深处...", "清醒度+15", "焦虑-10"),
        ("写完后你把这些文字都烧掉了，像是在告别过去...", "清醒度+10", "绝望-5"),
        ("你的字迹越来越潦草，像是内心的混乱...", "清醒度-5", "焦虑+5"),
    ],
    "radio_confession": [
        ("深夜电台DJ认真听了你的故事，给你点了一首歌...", "清醒度+15", "焦虑-10"),
        ("主持人说'我们会为你祈祷'，你挂断了电话...", "清醒度+5", "money", 0),
        ("热线一直占线，你对着忙音说了半小时...", "清醒度+10", "money", 0),
    ],
    "rain_walk": [
        ("雨水打在脸上，你想起童年时的无忧时光...", "清醒度+15", "绝望-10"),
        ("你淋感冒了，但脑子反而清醒了一些...", "清醒度+10", "money", -5),
        ("路人都用奇怪的眼神看你，你成了这座城市的笑话...", "清醒度-5", "焦虑+10"),
    ],
    "zoo_visit": [
        ("看到笼子里的狮子，你觉得自己跟它没什么区别...", "清醒度+5", "绝望+5"),
        ("海狮的表演让你笑了出来，这是今天的第一个笑容...", "清醒度+15", "money", -10),
        ("动物园的孩子们很开心，你想起了曾经的单纯...", "清醒度+10", "绝望-5"),
    ],
    "meditation": [
        ("闭眼深呼吸，脑子里的噪音渐渐消失...", "清醒度+20", "焦虑-15"),
        ("你睡着了，醒来时脖子都僵了...", "清醒度+5", "money", 0),
        ("各种念头纷至沓来，根本无法静心...", "清醒度-5", "焦虑+5"),
    ],
    "future_letter": [
        ("你给五年后的自己写了封信，充满了希望...", "清醒度+15", "绝望-10", 0),
        ("你不知道该写什么，未来对你来说是一片空白...", "清醒度-5", "绝望+5", 0),
        ("你把自己骂了一通，这封信读起来像遗书...", "清醒度-10", "绝望+10", 0),
    ],
    "bar_temp": [
        ("你洗了一晚上的杯子，赚了£30...", "money", 30, "清醒度-10"),
        ("酒吧老板看你可怜，多给了你£10小费...", "money", 40, "信誉+5"),
        ("你偷看了老板的抽屉，里面有£100...", "money", 100, "信誉-20"),
    ],
    "poetry_club": [
        ("你朗诵了一首自己写的诗，虽然很烂但大家鼓掌了...", "清醒度+15", "信誉+10"),
        ("其他人都是文学青年，你感觉自己格格不入...", "清醒度-5", "绝望+5", 0),
        ("你听到一个女孩的诗，听入了迷...", "清醒度+10", "焦虑-5", 0),
    ],
    "cooking_class": [
        ("你学会了做一道简单的菜，成就感油然而生...", "清醒度+15", "money", -20),
        ("做饭的时候你切到了手，鲜血直流...", "清醒度-10", "money", -10),
        ("你给自己做了一顿饭，虽然很难吃但至少是热的...", "清醒度+10", "money", -5),
    ],
    "used_bookstore": [
        ("你在旧书堆里找到一本绝版书，卖了£50...", "money", 50, "清醒度+10", 0),
        ("你翻看一本日记本，发现了一个陌生人的一生...", "清醒度+10", "绝望+5", 0),
        ("老板看你可怜，送了你几本旧书...", "清醒度+5", "money", 5),
    ],
    "volunteer_work": [
        ("你帮老人打扫房间，他们谢谢你...", "清醒度+15", "信誉+15", 0),
        ("你累了一天但很开心，感觉自己还有用...", "清醒度+20", "绝望-10", 0),
        ("组织者说你的精神状态不适合当志愿者...", "清醒度-5", "信誉-10", 0),
    ],
    "watch_sunrise": [
        ("太阳从地平线升起，新的一天开始了...", "清醒度+20", "绝望-10", 0),
        ("你看着太阳，思考为什么自己还活着...", "清醒度+10", "焦虑+5", 0),
        ("太冷了，你冻得发抖，但还是看完了...", "清醒度+15", "money", 0),
    ],
    "life_plan": [
        ("你列了满满一张计划表，感觉人生有了方向...", "清醒度+15", "绝望-15", 0),
        ("写完后你把纸撕了，计划永远是计划...", "清醒度-5", "绝望+10", 0),
        ("你决定从今天开始改变，哪怕一点点...", "清醒度+10", "信誉+5", 0),
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
    # 新增事件
    ("一个推销员敲门，向你推销根本不存在的保健品...", "清醒度-5", "money", -5),
    ("电视里在播戒毒公益广告，你换了个频道...", "清醒度-10"),
    ("邮箱里有一封给你的信，是法院的传票...", "清醒度-15", "焦虑+10"),
    ("你在垃圾堆里翻到一台还能用的旧手机!", "清醒度+5", "money", 0),
    ("房东说要涨房租了...", "清醒度-10", "money", -10),
    ("一只鸽子飞到窗台上盯着你...", "清醒度-5"),
    ("你听到隔壁传来欢笑声，那是你曾经的生活...", "清醒度-10"),
    ("止痛药过期了，你犹豫了一下还是吃了...", "清醒度-15"),
    ("有人在你门口放了一束花，不知道是谁...", "清醒度+10"),
    ("手机收到一条诈骗短信说你中奖了...", "清醒度-5"),
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
    # 新增重型事件
    ("你在医院醒来，完全不记得发生了什么...", "清醒度-30", "money", -40),
    ("高利贷找上门来，你的一条腿可能保不住了...", "清醒度-35", "money", -60),
    ("你唯一的朋友Spud死了， overdose...", "清醒度-40", "绝望+20", 0),
    ("你在警局过夜，被当成嫌疑人审讯了12小时...", "清醒度-25", "信誉-15", 0),
    ("你发现自己染上了HIV...", "清醒度-40", "绝望+30", 0),
    ("你的房子着火了，所有东西都烧光了...", "清醒度-35", "money", -80),
    ("你被绑架了，醒来时在一个废弃仓库里...", "清醒度-40", "money", -30),
    ("你在网吧晕倒，被送到医院急救...", "清醒度-30", "money", -50),
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

    def to_dict(self):
        """转换为字典用于存档"""
        return {
            'cash': self.cash,
            'sober': self.sober,
            'reputation': self.reputation,
            'withdrawal': self.withdrawal,
            'anxiety': self.anxiety,
            'despair': self.despair,
            'day': self.day,
            'round': self.round,
            'hour': self.hour,
            'rent_due': self.rent_due,
            'choices_log': self.choices_log,
            'history': self.history,
        }

    @classmethod
    def from_dict(cls, data):
        """从字典恢复"""
        player = cls()
        player.cash = data.get('cash', 50)
        player.sober = data.get('sober', 60)
        player.reputation = data.get('reputation', 40)
        player.withdrawal = data.get('withdrawal', 20)
        player.anxiety = data.get('anxiety', 90)
        player.despair = data.get('despair', 50)
        player.day = data.get('day', 1)
        player.round = data.get('round', 0)
        player.hour = data.get('hour', 12)
        player.rent_due = data.get('rent_due', 6)
        player.choices_log = data.get('choices_log', [])
        player.history = data.get('history', [])
        return player


class ChooseLifeGame:
    def __init__(self, root):
        self.root = root
        self.root.title("CHOOSE LIFE - 人生选择模拟器 v2.0")
        self.root.geometry("1300x950")
        self.root.configure(bg=BG_DARK)
        self.root.bind('<Key>', self.handle_keypress)
        self.root.bind('<Return>', self.handle_keypress)
        self.root.bind('<space>', lambda e: self.next_round() if self.continue_btn['state'] == 'normal' and not self.game_over else None)
        self.root.bind('<Button-1>', self.on_click)
        self.root.focus_force()

        self.player = HumanTrash()
        self.displayed_actions = []
        self.timer_running = False
        self.time_left = 25
        self.timer_id = None
        self.debuff_active = False
        self.game_over = False
        self.rent_amount = 40

        self.create_menu()
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
        game_data = {
            'player': self.player.to_dict(),
            'rent_amount': self.rent_amount,
            'game_over': self.game_over,
            'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'ending': '游戏中' if not self.game_over else '未知'
        }
        if save_game(game_data, slot):
            messagebox.showinfo("保存成功", f"游戏已保存到存档槽 {slot}")

    def quick_load(self, slot):
        """快速加载"""
        data = load_game(slot)
        if data:
            self.player = HumanTrash.from_dict(data.get('player', {}))
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

    def refresh_display(self):
        """刷新显示"""
        self.cash_var.set(max(0, self.player.cash))
        self.sober_var.set(max(0, min(100, self.player.sober)))
        self.rep_var.set(max(0, min(100, self.player.reputation)))
        self.wd_var.set(max(0, min(100, self.player.withdrawal)))
        self.anxiety_var.set(max(0, min(100, self.player.anxiety)))
        self.despair_var.set(max(0, min(100, self.player.despair)))

        self.cash_value_label.configure(text=f"£{self.player.cash}")
        self.sober_value_label.configure(text=str(self.player.sober))
        self.rep_value_label.configure(text=str(self.player.reputation))
        self.wd_value_label.configure(text=str(self.player.withdrawal))
        self.anxiety_value_label.configure(text=str(self.player.anxiety))
        self.despair_value_label.configure(text=str(self.player.despair))

        self.time_label.configure(text=f"第{self.player.day}天 {self.player.hour}:00")
        self.rent_label.configure(text=f"房租: £{self.rent_amount} | {self.player.rent_due}轮后到期")

    def create_widgets(self):
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

        # 属性面板 - 使用更美观的进度条样式
        stats_container = tk.Frame(status_frame, bg=BG_LIGHT, bd=0, relief="flat")
        stats_container.pack(fill="x", padx=5, pady=5)

        # 创建自定义进度条样式
        def create_stat_bar(parent, label, icon, color, var, max_val=100):
            frame = tk.Frame(parent, bg=BG_LIGHT)
            frame.pack(fill="x", pady=3)

            # 标签
            tk.Label(frame, text=f"{icon} {label}", fg=color, bg=BG_LIGHT,
                    width=10, anchor="w", font=("Courier New", 10, "bold")).pack(side="left")

            # 进度条背景
            bar_bg = tk.Frame(frame, bg="#1a1a1a", height=16)
            bar_bg.pack(side="left", fill="x", expand=True, padx=5)
            bar_bg.pack_propagate(False)

            # 进度条前景
            var.set(min(max_val, var.get()))
            progress = var.get() / max_val
            bar_fill = tk.Frame(bar_bg, bg=color, height=14)
            bar_fill.place(relx=0, rely=0.5, relwidth=progress, anchor="w")
            bar_fill.pack_propagate(False)

            # 数值显示
            value_label = tk.Label(frame, text=str(var.get()), fg=color, bg=BG_LIGHT,
                                  width=6, font=("Courier New", 10, "bold"))
            value_label.pack(side="right")

            return var, bar_fill, value_label

        # 现金
        self.cash_var = tk.IntVar()
        self.cash_var.set(50)
        self.cash_var, self.cash_bar, self.cash_value_label = create_stat_bar(
            stats_container, "现金", "💰", COLORS['cash'], self.cash_var, 200)

        # 清醒度
        self.sober_var = tk.IntVar()
        self.sober_var.set(60)
        self.sober_var, self.sober_bar, self.sober_value_label = create_stat_bar(
            stats_container, "清醒度", "🧠", COLORS['sober'], self.sober_var, 100)

        # 信誉
        self.rep_var = tk.IntVar()
        self.rep_var.set(40)
        self.rep_var, self.rep_bar, self.rep_value_label = create_stat_bar(
            stats_container, "信誉", "👥", COLORS['reputation'], self.rep_var, 100)

        # 戒断值
        self.wd_var = tk.IntVar()
        self.wd_var.set(20)
        self.wd_var, self.wd_bar, self.wd_value_label = create_stat_bar(
            stats_container, "戒断值", "💉", COLORS['withdrawal'], self.wd_var, 100)

        # 焦虑
        self.anxiety_var = tk.IntVar()
        self.anxiety_var.set(90)
        self.anxiety_var, self.anxiety_bar, self.anxiety_value_label = create_stat_bar(
            stats_container, "焦虑", "😰", COLORS['anxiety'], self.anxiety_var, 100)

        # 绝望
        self.despair_var = tk.IntVar()
        self.despair_var.set(50)
        self.despair_var, self.despair_bar, self.despair_value_label = create_stat_bar(
            stats_container, "绝望", "💀", COLORS['despair'], self.despair_var, 100)

        # 场景描述
        self.scene_label = tk.Label(self.root, text="", font=("Courier", 11),
                                    fg=GRAY, bg=BG_DARK, wraplength=850, justify="left")
        self.scene_label.pack(pady=5)

        self.hint_label = tk.Label(self.root, text="按 1-6 选择 | 25秒倒计时",
                                   font=("Courier", 10, "italic"), fg=DARK_GRAY, bg=BG_DARK)
        self.hint_label.pack()

        self.options_frame = tk.Frame(self.root, bg=BG_DARK)
        self.options_frame.pack(pady=5)

        self.option_buttons = []
        for i in range(6):
            btn = tk.Button(self.options_frame, text=f"[{i+1}] ",
                           font=("Courier", 10), fg="#FFA500", bg="#1A1A1A",
                           width=35, height=1, anchor="w",
                           command=lambda idx=i: self.make_choice(idx))
            btn.pack(pady=1, fill="x")
            self.option_buttons.append(btn)

        # 结果文本区域 - 不自动换行，水平滚动
        self.result_label = tk.Label(self.root, text="",
                                     fg="#FFA500", bg=BG_DARK,
                                     font=("Courier", 11), justify="left", anchor="nw")
        self.result_label.pack(pady=5, fill="both", padx=10, expand=True)

        # 事件文本区域
        self.event_label = tk.Label(self.root, text="",
                                    fg="#FFA500", bg=BG_DARK,
                                    font=("Courier", 10), justify="left", anchor="nw")
        self.event_label.pack(pady=5, fill="both", padx=10, expand=True)

        control_frame = tk.Frame(self.root, bg=BG_DARK)
        control_frame.pack(pady=10)

        self.music_btn = tk.Button(control_frame, text="🎵 音乐: 开",
                                   font=("Courier", 10), fg=GREEN, bg=DARK_GRAY,
                                   command=self.toggle_music, width=15)
        self.music_btn.pack(side="left", padx=5)
        self.music_on = True

        self.continue_btn = tk.Button(control_frame, text="【按回车继续】",
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
        self.root.focus_force()

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
        # 更新变量值
        self.cash_var.set(max(0, self.player.cash))
        self.sober_var.set(max(0, min(100, self.player.sober)))
        self.rep_var.set(max(0, min(100, self.player.reputation)))
        self.wd_var.set(max(0, min(100, self.player.withdrawal)))
        self.anxiety_var.set(max(0, min(100, self.player.anxiety)))
        self.despair_var.set(max(0, min(100, self.player.despair)))

        # 更新数值标签
        self.cash_value_label.configure(text=f"£{self.player.cash}")
        self.sober_value_label.configure(text=str(self.player.sober))
        self.rep_value_label.configure(text=str(self.player.reputation))
        self.wd_value_label.configure(text=str(self.player.withdrawal))
        self.anxiety_value_label.configure(text=str(self.player.anxiety))
        self.despair_value_label.configure(text=str(self.player.despair))

        # 更新进度条颜色和宽度
        def update_bar(bar, value, max_val, color):
            progress = max(0, min(1, value / max_val))
            bar.configure(bg=color)
            bar.place_configure(relwidth=progress)

        update_bar(self.cash_bar, self.player.cash, 200, COLORS['cash'])
        update_bar(self.sober_bar, self.player.sober, 100, COLORS['sober'])
        update_bar(self.rep_bar, self.player.reputation, 100, COLORS['reputation'])
        update_bar(self.wd_bar, self.player.withdrawal, 100, COLORS['withdrawal'])
        update_bar(self.anxiety_bar, self.player.anxiety, 100, COLORS['anxiety'])
        update_bar(self.despair_bar, self.player.despair, 100, COLORS['despair'])

    def make_choice(self, idx):
        try:
            if idx >= len(self.displayed_actions):
                return
            self.cancel_timer()
            for btn in self.option_buttons:
                btn.configure(state="disabled")
            self.root.update_idletasks()

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
            result = random.choice(results)

            # 解析结果元组 - 支持不同格式
            # 格式1: (desc, stat1_with_val, stat2_with_val, val2)
            #   例如: ("描述", "清醒度-15", "money", -5) -> 清醒度-15, money-5
            # 格式2: (desc, stat1, val1, stat2, val2)
            #   例如: ("描述", "money", 100, "信誉", 20) -> money+100, 信誉+20
            result_text = result[0]

            # 记录变化前的现金
            old_cash = self.player.cash

            # 立即显示结果
            self.result_label.configure(text=f"► 你选择了：{action_name}\n\n{result_text}")
            self.root.update_idletasks()

            if len(result) == 4:
                # 格式1: result[1]="清醒度-15", result[2]="money", result[3]=-5
                stat1 = result[1]
                stat2 = result[2]
                val2 = result[3]

                # 解析stat1
                if stat1 and isinstance(stat1, str):
                    parsed = self.parse_stat_change(stat1)
                    if parsed:
                        self.apply_effect(parsed[0], parsed[1])

                # 解析stat2
                if stat2 and isinstance(stat2, str):
                    parsed = self.parse_stat_change(stat2)
                    if parsed:
                        self.apply_effect(parsed[0], parsed[1])
                    elif val2 is not None:
                        try:
                            self.apply_effect(stat2, int(val2))
                        except (ValueError, TypeError):
                            pass

            elif len(result) >= 5:
                # 格式2: result[1]="money", result[2]=100, result[3]="信誉", result[4]=20
                stat1 = result[1]
                val1 = result[2]
                stat2 = result[3] if len(result) > 3 else None
                val2 = result[4] if len(result) > 4 else None

                # 应用stat1
                if stat1 and isinstance(stat1, str):
                    parsed = self.parse_stat_change(stat1)
                    if parsed:
                        self.apply_effect(parsed[0], parsed[1])
                    elif val1 is not None:
                        try:
                            self.apply_effect(stat1, int(val1))
                        except (ValueError, TypeError):
                            pass

                # 应用stat2
                if stat2 and isinstance(stat2, str) and val2 is not None:
                    parsed = self.parse_stat_change(stat2)
                    if parsed:
                        self.apply_effect(parsed[0], parsed[1])
                    else:
                        try:
                            self.apply_effect(stat2, int(val2))
                        except (ValueError, TypeError):
                            pass
            else:
                # 默认效果
                self.apply_effect("清醒度", -5)

            # 计算金钱变化
            money_change = self.player.cash - old_cash
            if money_change != 0:
                change_text = f"\n\n💰 现金: {'+' if money_change > 0 else ''}{money_change} (现在: £{self.player.cash})"
                self.result_label.configure(text=self.result_label.cget("text") + change_text)

            self.root.update_idletasks()
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
            self.root.update_idletasks()
            self.root.focus_force()
        except Exception as e:
            print(f"Error in make_choice: {e}")
            import traceback
            traceback.print_exc()
            self.result_label.configure(text=f"发生错误: {e}")
            self.continue_btn.configure(state="normal")

    def parse_stat_change(self, stat_str):
        """解析形如 '清醒度-15' 或 'money+20' 的字符串"""
        if not stat_str or not isinstance(stat_str, str):
            return None
        # 找到 +/- 的位置
        for i, char in enumerate(stat_str):
            if char in '+-':
                stat_name = stat_str[:i]
                try:
                    val = int(stat_str[i:])
                    return (stat_name, val)
                except ValueError:
                    return None
        return None

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

        # 新增结局触发条件
        # 戒断值过高可能导致过量
        if self.player.withdrawal >= 95 and random.random() < 0.3:
            self.show_ending("overdose")
            return

        # 没钱+低清醒度可能入狱
        if self.player.cash < 10 and self.player.sober < 20 and random.random() < 0.2:
            self.show_ending("arrest")
            return

        # 长时间存活可能触发神秘结局
        if self.player.day > 20 and self.player.round > 50 and random.random() < 0.1:
            self.show_ending("mysterious")
            return

        # 高绝望值可能触发特殊结局
        if self.player.despair >= 95:
            if random.random() < 0.3:
                self.show_ending("overdose")
                return

        # 正面结局触发条件
        # 高清醒度+高信誉+有钱 = 人生赢家
        if self.player.sober >= 80 and self.player.reputation >= 70 and self.player.cash >= 200:
            if random.random() < 0.15:
                self.show_ending("success")
                return

        # 戒掉毒瘾 = 救赎
        if self.player.withdrawal == 0 and self.player.sober >= 60 and self.player.day > 10:
            if random.random() < 0.1:
                self.show_ending("redemption")
                return

        self.continue_btn.configure(state="normal")
        self.root.update_idletasks()  # 强制刷新界面

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
            # 新增结局
            "hiv": ("绝望深渊", "你收到了HIV检测结果——阳性。\n\n这个世界在你眼前崩塌。\n\n也许这就是你最后一次放纵的代价。"),
            "arrest": ("锒铛入狱", "警车带走了你。\n\n在监狱里，你终于有了栖身之地。\n\n只是这代价太大了。"),
            "overdose": ("过量身亡", "你的人生在那一刻停止了。\n\n也许在某个瞬间，你曾经想要改变。\n\n但现在一切都晚了。"),
            "redemption": ("自我救赎", "你终于戒掉了毒瘾！\n\n虽然人生已经一团糟，但你决定重新开始。\n\n这是你应得的——一个新的开始。"),
            "success": ("人生赢家", "你他妈的居然成功了！\n\n找到工作，戒掉毒瘾，还清债务。\n\n在这个操蛋的世界里，你赢了。"),
            "mysterious": ("神秘消失", "你消失了。\n\n没有人知道你去了哪里。\n\n也许这是最好的结局。"),
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
