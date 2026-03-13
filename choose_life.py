#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
✞ CHOOSE LIFE = CHOOSE Fucking MISERY ✞
人生选择模拟器 —— 致郁混沌版
================================================================================

# 你以为选代码就能翻盘？就像Renton戒毒一千次——
# 最后还是爬回马桶边，这就是人生。

# 本程序拒绝任何"积极向上"的可能。
# 人生本就是烂局，选择只是换种烂法。
# 这不是游戏，是TM现实。
"""

import random
import time
import os
import sys

# ═══════════════════════════════════════════════════════════════════════════
# 【初始化设置】—— 你的人生，从一坨屎开始
# ═══════════════════════════════════════════════════════════════════════════

# 颜色代码 —— 红色代表血，灰色代表灰烬，黑色代表虚无
RED = '\033[91m'
DARK_RED = '\033[31m'
GRAY = '\033[90m'
DARK_GRAY = '\033[38;5;240m'
BLACK = '\033[30m'
BG_RED = '\033[41m'
BG_BLACK = '\033[40m'
BG_DARK = '\033[48;5;234m'
RESET = '\033[0m'
BOLD = '\033[1m'
BLINK = '\033[5m'
DIM = '\033[2m'
UNDERLINE = '\033[4m'

# ═══════════════════════════════════════════════════════════════════════════
# 【UI绘制函数】—— 终端里的暗黑美学
# ═══════════════════════════════════════════════════════════════════════════

def clear_screen():
    """清屏 —— 像你TM的人生一样干净"""
    os.system('cls' if os.name == 'nt' else 'clear')


def print_box(text, width=60, style="double"):
    """
    打印带边框的文字框
    """
    if style == "double":
        tl, tr, bl, br, h, v = "╔", "╗", "╚", "╝", "═", "║"
    elif style == "single":
        tl, tr, bl, br, h, v = "┌", "┐", "└", "┘", "─", "│"
    elif style == "heavy":
        tl, tr, bl, br, h, v = "█", "█", "█", "█", "█", "█"
    else:
        tl, tr, bl, br, h, v = "+", "+", "+", "+", "-", "|"

    lines = text.split('\n')
    print(f"{DARK_RED}{tl}{h * width}{tr}{RESET}")
    for line in lines:
        padding = width - len(line)
        left_pad = padding // 2
        right_pad = padding - left_pad
        print(f"{DARK_RED}{v}{RESET}{GRAY}{' ' * left_pad}{line}{' ' * right_pad}{RESET}{DARK_RED}{v}{RESET}")
    print(f"{DARK_RED}{bl}{h * width}{br}{RESET}")


def print_divider(char="─", length=60, color=DARK_RED):
    """打印分隔线"""
    print(f"{color}{char * length}{RESET}")


def print_header(text, underline=True):
    """打印标题"""
    print(f"\n{DARK_RED}{BOLD}╔{'═' * 58}╗{RESET}")
    print(f"{DARK_RED}{BOLD}║{RESET}{GRAY}{text:^58}{RESET}{DARK_RED}{BOLD}║{RESET}")
    print(f"{DARK_RED}{BOLD}╚{'═' * 58}╝{RESET}")
    if underline:
        print_divider()


def print_menu_item(num, text, desc=""):
    """打印菜单选项"""
    print(f"  {DARK_RED}{BOLD}[{num}]{RESET} {GRAY}{text}{RESET}")
    if desc:
        print(f"      {DARK_GRAY}{desc}{RESET}")


def loading_bar(progress, total, bar_length=30):
    """打印加载条"""
    percent = progress / total
    filled = int(bar_length * percent)
    bar = "█" * filled + "░" * (bar_length - filled)
    return f"[{RED}{bar}{RESET}] {int(percent * 100)}%"


def flicker_text(text, times=3):
    """文字闪烁效果"""
    for _ in range(times):
        print(f"{RED}{BOLD}{text}{RESET}", end='\r')
        time.sleep(0.1)
        print(f"{' ' * len(text)}", end='\r')
        time.sleep(0.1)
    print(f"{RED}{BOLD}{text}{RESET}")


def typewriter_text(text, delay=0.03, color=GRAY):
    """打字机效果"""
    for char in text:
        sys.stdout.write(f"{color}{char}{RESET}")
        sys.stdout.flush()
        time.sleep(delay)
    print()


def print_ascii_art(art):
    """打印ASCII艺术"""
    print(f"{RED}{BOLD}{art}{RESET}")


# ASCII艺术库
TITLE_ART = r"""
 ██████╗██╗   ██╗██████╗ ███████╗██████╗     ███████╗ █████╗ ██████╗ ██╗
██╔════╝╚██╗ ██╔╝██╔══██╗██╔════╝██╔══██╗    ██╔════╝██╔══██╗██╔══██╗██║
██║      ╚████╔╝ ██████╔╝█████╗  ██████╔╝    █████╗  ███████║██████╔╝██║
██║       ╚██╔╝  ██╔══██╗██╔══╝  ██╔══██╗    ██╔══╝  ██╔══██║██╔══██╗╚═╝
╚██████╗   ██║   ██████╔╝███████╗██║  ██║    ██║     ██║  ██║██║  ██║██╗
 ╚═════╝   ╚═╝   ╚═════╝ ╚══════╝╚═╝  ╚═╝    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝
"""

SUBTITLE_ART = r"""
    ╔═══════════════════════════════════════════════════════════════╗
    ║     C H O O S E   L I F E   =   C H O O S E   M I S E R Y   ║
    ╚═══════════════════════════════════════════════════════════════╝
"""

ENDING_ART = r"""
    ██████╗ ███████╗ █████╗ ██████╗     ███████╗██╗ ██████╗ ███╗   ██╗ █████╗ ██╗
    ██╔══██╗██╔════╝██╔══██╗██╔══██╗    ██╔════╝██║██╔════╝ ████╗  ██║██╔══██╗██║
    ██║  ██║█████╗  ███████║██║  ██║    ███████╗██║██║  ███╗██╔██╗ ██║███████║██║
    ██║  ██║██╔══╝  ██╔══██║██║  ██║    ╚════██║██║██║   ██║██║╚██╗██║██╔══██║╚═╝
    ██████╔╝███████╗██║  ██║██████╔╝    ███████║██║╚██████╔╝██║ ╚████║██║  ██║██╗
    ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═════╝     ╚══════╝╚═╝ ╚═════╝ ╚═╝  ╚═══╝╚═╝  ╚═╝
"""

SKULL_ART = r"""
              .-.
             (o o)
             | O |
              \ /
           .-'. '-'.-'
          /  /| |\
         /  / | | \
        /  /  | |  \
       /  /   | |   \
      /  /    | |    \
     /  /     | |     \
    (__/      | |      \
              | |
             /   \
            |     |
            |     |
            |     |
           _|     |_
          |___   ___|
              | |
              | |
              | |
             _| |_
            |___|___|
"""

# 随机种子 —— 就像你的出生，本质上是TM随机的悲剧
random.seed(time.time())


# ═══════════════════════════════════════════════════════════════════════════
# 【全局变量】—— 你个烂人的人生状态
# ═══════════════════════════════════════════════════════════════════════════

class HumanTrash:
    """
    # 你是垃圾，你的人生也是垃圾
    # 属性只会变差，不会变好
    # 相信我，这真的是"最好的情况"
    """

    def __init__(self):
        # 初始属性 —— 都是屎，就别挑了
        self.anxiety = 90          # 焦虑值：90/100，高得一批
        self.alive_value = 10      # 活着值：10/100低得可怜，但TM死不了
        self.despair = 50          # 绝望值：50/100，降低初始值，避免第一轮就绝望
        self.money = 20            # 兜里剩20镑，偷来的，迟早要还
        self.debuffs = []          # 你的debuff，比你的优点还多
        self.choices_log = []      # 你的选择记录 —— 记录你TM多傻
        self.events_log = []       # 随机事件记录 —— 记录生活TM多狗血
        self.round = 0             # 你已经浪费了多少轮
        self.despair_cooldown = 0  # 绝望模式冷却轮数

    def drag_you_to_hell(self):
        """更新你的糟糕状态 —— 让你更惨，是我的荣幸"""
        # 活着值≤0时强制继续，只会触发"濒死但死不了"
        if self.alive_value <= 0:
            self.alive_value = 1
            self.despair = min(100, self.despair + 5)
            print(f"\n{RED}{BOLD}✞ 你想死？但你TM连死的力气都没有 ✞{RESET}")
            print(f"{GRAY}...你的身体在抽搐，意识在消散，但TM就是断不了气{RESET}")

        # 绝望值≥100时，所有选项变成"无意义的烂选项"
        if self.despair >= 100:
            self.despair = 100
            print(f"\n{DARK_RED}{BOLD}✞ 绝望已经TM吞没了你 ✞{RESET}")
            print(f"{GRAY}一切都没意义了...你只能机械地选择，然后等待更糟的结果{RESET}")


# ═══════════════════════════════════════════════════════════════════════════
# 【随机事件库】—— 生活TM从不让你好过
# ═══════════════════════════════════════════════════════════════════════════

# 基础随机事件 —— 日常狗血
BASIC_EVENTS = [
    "烟抽完了，你只能坐在黑暗中数天花板上的裂缝",
    "威士忌被猫打翻了 —— 那畜生居高临下地看着你，眼神里写着蔑视",
    "编程书被风吹到地上，撕烂的那页正好是你唯一看懂的部分",
    "房东在砸门，房租欠了四个月了，每一声都是对你的审判",
    "邻居又在放吵死人的 techno，节奏像你TM混乱的脑神经",
    "手机欠费了，反正也没人会打给你",
    "冰箱里只有过期的牛奶和一块发霉到认不出原形的面包",
    "电源线接触不良，笔记本就是块昂贵的砖头",
    "窗外在下雨，雨滴砸在玻璃上的声音像你TM逐渐腐烂的心跳",
    "耳机线缠在一起了，就像你TM一团浆糊的人生",
    "你TM想洗个热水澡，水管爆了，热水器的尸体躺在地上",
    "门缝底下塞进来一张水电费账单，你TM看都不敢看",
    "窗户关不紧，凌晨三点冷风吹进来，你TM裹紧被子继续受",
    "一只蟑螂从你面前大摇大摆地爬过，你TM连打的力气都没有",
    "你TM想上厕所，马桶堵了，那种绝望已经超越语言",
]

# 重度随机事件 —— 让你怀疑人生
HEAVY_EVENTS = [
    "警察查房了 —— 哪怕你TM什么都没做，那种被盯上的感觉挥之不去",
    "Sick Boy骗你去借高利贷，你TM居然信了，那畜生的眼睛里写着『交易』",
    "父母打电话骂你没出息，你TM连话都说不出来，听筒里的沉默比骂声更刺耳",
    "Mark带人来要债了，手里转着那把弹簧刀，笑得让你TM脊背发凉",
    "Spud把你仅剩的钱换成了一包假货，还TM一脸无辜",
    "你的银行账户被冻结了，TM的，为什么你永远最后一个知道",
    "妓女在楼下拉客，吵了你TM一整晚，你TM在脑海里演完了整部三级片",
    "你TM喝多了吐了一地，现在还在恶心，胃酸灼烧着你的食管",
    "有人举报你纵火，虽然你TM什么都没做，但警察的眼神已经给你定了罪",
    "你的电脑中毒了，所有代码都没了 —— 活TM该，谁让你TM不自量力",
    "Diane打电话来哭诉她TM的悲惨人生，你TM听着听着就睡着了",
    "Begbie在酒吧里发疯，拿酒瓶砸人，你TM差一点就成了下一个目标",
    "你TM走在街上被人打了闷棍，醒来时钱包没了，牙齿也TM松了一颗",
    "房东带人来收房，你TM跪下来求他，他TM只是冷笑",
    "你TM试图联系Renton，但他TM早已消失得无影无踪，就像你TM从未存在过",
]

# 电影暗黑桥段彩蛋 —— 随机触发
MOVIE_QUOTES = [
    ("Renton", "I'm a junky. I'm worse than a junky. I'm a liar."),
    ("Renton", "Choose life. Choose a job. Choose a career. Choose a family... Choose a fucking big television."),
    ("Mark", "The little things become the big things. You miss them, you become nothing."),
    ("Sick Boy", "We're bastards. And you can't kid yourself. You're just as bad as any of us."),
    ("Diane", "You think we're bad? You should see the state of the toilets!"),
    ("Renton", "I don't think there's anything worse than being third generation unemployed."),
    ("Begbie", "You f***ing retards! I'm gonnae kill the ba***rd!"),
    ("Spud", "I've got the gear. I've got the gear. I've got the gear."),
    ("Renton", "There were new dreams. And better dreams."),
    ("Renton", "It had to be the two of you. The two of you, forever."),
]


# ═══════════════════════════════════════════════════════════════════════════
# 【工具函数】—— 输出要够TM混乱
# ═══════════════════════════════════════════════════════════════════════════

def chaotic_print(text, delay=0.03):
    """
    混沌输出函数 —— 文字应该像你TM的人生一样混乱
    """
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        if random.random() < 0.1:  # 10%概率随机抖动
            sys.stdout.write(random.choice([' ', '\t', '\n']))
            sys.stdout.flush()
        time.sleep(delay)
    print()


def broken_text(text):
    """
    破碎字幕式输出 —— 就像你TM的精神状态
    """
    result = ""
    for char in text:
        if random.random() < 0.05:  # 5%概率插入乱码
            result += random.choice(['█', '▓', '░', '■', '□', '▪'])
        result += char
    return result


def screen_flicker():
    """
    屏幕闪烁效果 —— 让你TM的眼皮跳一跳
    """
    for _ in range(random.randint(2, 5)):
        sys.stdout.write(random.choice([RED, GRAY, DARK_GRAY, RESET]))
        sys.stdout.flush()
        time.sleep(random.uniform(0.01, 0.05))


def print_title():
    """
    打印标题 —— 用血和灰烬写的
    """
    clear_screen()
    print(f"\n")
    print_ascii_art(TITLE_ART)
    print(f"\n")
    print(f"{DARK_RED}{BOLD}                       ═══ 1996 · GLASGOW ═══{RESET}")
    print(f"\n")
    print(f"  {GRAY}墙上全是霉斑，空气中TM都是烂酒味{RESET}")
    print(f"  {GRAY}你在破床垫上醒来，宿醉+戒断反应双重折磨...{RESET}")
    print(f"\n")
    print_divider("─", 65, DARK_RED)


def print_status(player):
    """
    打印你的悲惨状态 —— 欣赏你自己的狼狈
    """
    # 绘制状态条
    def draw_bar(value, max_val=100):
        length = 20
        filled = int((value / max_val) * length)
        bar = "█" * filled + "░" * (length - filled)
        return bar

    print(f"\n")
    print(f"  {DARK_RED}╔{'═' * 48}╗{RESET}")
    print(f"  {DARK_RED}║{RESET}  {BOLD}{DARK_RED}◈ 你TM的人生状态 ◈{RESET}" + " " * 26 + f"{DARK_RED}║{RESET}")
    print(f"  {DARK_RED}╠{'═' * 48}╣{RESET}")

    # 焦虑值
    anxiety_color = RED if player.anxiety > 70 else GRAY
    print(f"  {DARK_RED}║{RESET}  焦虑值   [{anxiety_color}{draw_bar(player.anxiety)}{RESET}] {player.anxiety:>3}/100   {DARK_RED}║{RESET}")

    # 活着值
    alive_color = RED if player.alive_value < 30 else GRAY
    alive_icon = "✕" if player.alive_value < 30 else "♥"
    print(f"  {DARK_RED}║{RESET}  活着值   [{alive_color}{draw_bar(player.alive_value)}{RESET}] {player.alive_value:>3}/100 {alive_icon}  {DARK_RED}║{RESET}")

    # 绝望值
    despair_color = RED if player.despair > 80 else GRAY
    print(f"  {DARK_RED}║{RESET}  绝望值   [{despair_color}{draw_bar(player.despair)}{RESET}] {player.despair:>3}/100   ☠  {DARK_RED}║{RESET}")

    # 金钱
    print(f"  {DARK_RED}║{RESET}  金钱     £{player.money:<6} {'(偷来的)' if player.money <= 20 else '':<20} {DARK_RED}║{RESET}")

    print(f"  {DARK_RED}╠{'═' * 48}╣{RESET}")

    # DEBUFF显示
    if player.debuffs:
        debuff_text = " | ".join(player.debuffs[:3])
        if len(player.debuffs) > 3:
            debuff_text += f" ...(+{len(player.debuffs)-3})"
        print(f"  {DARK_RED}║{RESET}  DEBUFF: {RED}{debuff_text:<40} {DARK_RED}║{RESET}")
    else:
        print(f"  {DARK_RED}║{RESET}  {DARK_GRAY}暂无DEBUFF（但TM不会持续太久）{' ' * 13} {DARK_RED}║{RESET}")

    print(f"  {DARK_RED}╚{'═' * 48}╝{RESET}")
    print(f"\n")


# ═══════════════════════════════════════════════════════════════════════════
# 【开局设置】—— 你的悲剧从现在开始
# ═══════════════════════════════════════════════════════════════════════════

def apply_initial_debuff(player):
    """
    随机开局debuff —— 生活TM从不让你好过
    """
    INITIAL_DEBUFFS = [
        ("手抖得写不了代码", "你TM的手抖得跟帕金森似的，键盘都按不准，每一个字符都是煎熬"),
        ("宿醉看不清选项", "你TM醉得眼睛都睁不开，选项在视线里扭曲成奇怪的形状"),
        ("Mark提前找上门", "操，Mark带着两个马仔已经在砸你的门了，拳头的闷响像催命的鼓点"),
        ("停电了电脑开不了", "他妈的停电了，你TM的笔记本就是块昂贵的废铁，屏幕黑得像你的未来"),
        ("房东堵在门口", "房东在门口骂骂咧咧你要房租，但你TM哪有钱，连呼吸都是浪费"),
        ("威士忌被偷了", "你TM仅剩的那瓶威士忌不见了，肯定是被Spud那狗日的偷走了"),
        ("头痛欲裂", "你的头像是被十吨重的卡车反复碾压，太阳穴突突地跳"),
        ("门锁坏了", "你TM的门锁彻底罢工了，任何人都能随时闯进来，包括讨债的，包括警察"),
    ]

    # 随机选择1-2个debuff
    num_debuffs = random.randint(1, 2)
    for _ in range(num_debuffs):
        debuff, desc = random.choice(INITIAL_DEBUFFS)
        if debuff not in player.debuffs:
            player.debuffs.append(debuff)

            print(f"\n  {RED}╔{'═' * 50}╗{RESET}")
            print(f"  {RED}║{RESET}  {BOLD}{RED}◈ 随机DEBUFF触发 ◈{RESET}")
            print(f"  {RED}╚{'═' * 50}╝{RESET}")
            print(f"  {RED}✞ {debuff} ✞{RESET}")
            print(f"  {GRAY}{desc}{RESET}")
            print()

            # 应用debuff效果（减少绝望增加）
            if "手抖" in debuff:
                player.anxiety += 10
            elif "宿醉" in debuff:
                player.alive_value -= 5
            elif "Mark" in debuff:
                player.money = max(0, player.money - 10)
            elif "停电" in debuff:
                player.despair += 5
            elif "房东" in debuff:
                player.despair += 8
            elif "威士忌" in debuff:
                player.despair += 6
            elif "头痛" in debuff:
                player.anxiety += 8
                player.alive_value -= 3
            elif "门锁" in debuff:
                player.anxiety += 12


def describe_scene(player):
    """
    描述当前场景 —— 你TM在垃圾堆里
    返回显示的物品列表，供选择使用
    """
    # 根据回合数改变场景描述
    scene_descriptions = [
        ("破出租屋", "你躺在格拉斯哥贫民区的出租屋里，四周墙壁渗着霉味，地板上散落着酒瓶和烟头..."),
        ("浴室", "你站在浴室的镜子前，镜子里的人看起来像一具还没完全腐烂的尸体..."),
        ("厨房", "厨房里堆着发霉的餐具和过期的食物，你TM的胃在抽搐，但不是因为饥饿..."),
        ("窗边", "你站在窗边，看着外面灰蒙蒙的天，雨滴在玻璃上划出泪痕般的轨迹..."),
        ("床上", "你蜷缩在那张弹簧都TM戳出来的床垫上，被子散发着霉味，但你TM已经习惯了..."),
        ("门口", "你站在门口，犹豫着要不要出去，外面的世界TM的一样烂..."),
        ("桌前", "你坐在那张摇摇晃晃的桌子前，桌上摊着你TM根本看不懂的编程书..."),
    ]

    scene_name, scene_desc = random.choice(scene_descriptions)

    print(f"\n")
    print(f"  {DARK_RED}╔{'═' * 52}╗{RESET}")
    print(f"  {DARK_RED}║{RESET}  {BOLD}{DARK_RED}◈ 场景：{scene_name} ◈{RESET}" + " " * (30 - len(scene_name)) + f"{DARK_RED}║{RESET}")
    print(f"  {DARK_RED}╚{'═' * 52}╝{RESET}")
    print(f"  {GRAY}{scene_desc}{RESET}")
    print(f"\n")

    # 动作库 - 32个动作（扩充到30+）
    all_actions = [
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
        # 新增20个动作
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
        ("假装上班", "fake_go_work"),
        ("写遗书", "write_suicide_note"),
        ("拨打自杀热线", "call_hotline"),
        ("跟踪陌生人", "stalk_stranger"),
        ("在pub赊账", "drink_on_credit"),
        ("尝试黑进银行系统", "hack_bank"),
        ("去图书馆看书", "go_library"),
        ("逗那只流浪猫", "play_with_cat"),
        ("在雨中漫步", "walk_in_rain"),
    ]

    # 物品库 - 与动作一一对应（32个）
    items = [
        ("掺了水的威士忌", "喝起来像TM掺了水的谎言之酒"),
        ("封面破损的编程书", "你TM根本看不懂，那些字母认识你你不认识它们"),
        ("标着「Heroin」的面粉", "可能TM被Spud换成真的了，也可能没有"),
        ("Mark的催债纸条", "里面TM藏着刀片，就像你的处境一样危险"),
        ("这张破床垫", "弹簧戳出来的地方像你TM千疮百孔的人生"),
        ("酒吧的名片", "上面印着那个可以让你TM买醉的地方"),
        ("Renton的照片", "那个去了伦敦的叛徒，你现在TM只想骂他"),
        ("银行的账单", "上面那串数字让你TM想死"),
        ("父母的电话号码", "你TM没脸打，但也TM忘不掉"),
        ("招聘的广告", "你TM曾经相信能找到出路"),
        ("床底下的脏衣服", "你TM已经一个月没洗了"),
        ("天花板的裂缝", "你TM盯着它看了一整晚"),
        # 新增物品
        ("Spud的旧皮鞋", "尺码小了，但TM能当点钱"),
        ("Diane的电话号码", "她TM可能早就换号了"),
        ("网吧会员卡", "里面还TM剩£3"),
        ("喷漆罐", "你TM想写点什么，但TM什么都不会写"),
        ("邻居家的门缝", "里面TM传来争吵声"),
        ("戒毒中心的宣传册", "你TM看过就扔了"),
        ("教堂的传单", "神TM会救你？"),
        ("旧杂志里的裸女", "分辨率TM低得可怜"),
        ("Sick Boy的名片", "背面TM写着各种生意"),
        ("海边的明信片", "你TM从来没用过"),
        ("垃圾桶里的半块披萨", "上面TM爬满了蛆"),
        ("假工作证", "你TM连面试都没去过"),
        ("皱巴巴的信纸", "你TM写了一半就撕了"),
        ("小纸条上的热线电话", "你TM打过，但TM占线"),
        ("那个戴帽子的行人", "你TM跟了他三条街"),
        ("酒保的脸", "他TM已经TM记住你了"),
        ("银行的登录页面", "你TM知道密码是TM什么吗"),
        ("过期杂志", "你TM打发时间的东西"),
        ("那只脏兮兮的流浪猫", "它TM抓了你一下"),
        ("窗外的雨", "你TM想让它TM停下来"),
    ]

    # 每轮显示6个随机物品（从32个中选）
    num_items = 6
    displayed_indices = random.sample(range(32), num_items)

    print(f"  {RED}▶ 你看到/想到：{RESET}")
    print(f"  {DARK_GRAY}{'─' * 50}{RESET}")

    for i, idx in enumerate(displayed_indices, 1):
        item, desc = items[idx]
        action_name, action_id = all_actions[idx]
        print(f"  {DARK_RED}│{RESET}  {DARK_RED}[{i}]{RESET} {GRAY}{item:<18}{RESET}")
        print(f"  {DARK_RED}│{RESET}      {DARK_GRAY}{desc}{RESET}")

    print(f"  {DARK_GRAY}{'─' * 50}{RESET}")

    # 返回显示的选项数量和对应的动作ID列表
    displayed_actions = [all_actions[idx] for idx in displayed_indices]

    # 选项说明
    print(f"\n  {GRAY}你的选择（1-{num_items}）：{RESET}")
    print(f"\n")

    return num_items, displayed_actions


# ═══════════════════════════════════════════════════════════════════════════
# 【选择系统】—— 你TM选什么都一样烂
# ═══════════════════════════════════════════════════════════════════════════

def get_choice(prompt, num_options, player):
    """
    获取选择 —— 附带"随机输入惩罚"
    """
    # 减少绝望模式冷却
    if player.despair_cooldown > 0:
        player.despair_cooldown -= 1

    # 绝望值≥100且冷却结束后，强制使用"无所谓"选项
    if player.despair >= 100 and player.despair_cooldown == 0:
        print(f"\n  {RED}╔{'═' * 50}╗{RESET}")
        print(f"  {RED}║{RESET}  {BOLD}{RED}你已经TM绝望到没感觉了...{RESET}")
        print(f"  {RED}║{RESET}  {GRAY}所有选项对你来说都TM一样了...{RESET}")
        print(f"  {RED}╚{'═' * 50}╝{RESET}")
        # 设置冷却，让玩家只能选1持续3轮
        player.despair_cooldown = 3
        return 1  # 强制返回第一个选项

    while True:
        choice = input(f"\n  {RED}▶ {RESET}{prompt}{RESET}")

        # 先检查是否是有效输入（非数字的情况）
        try:
            choice_int = int(choice)
        except ValueError:
            # 输入不是数字时，才触发惩罚
            if random.random() < 0.3:  # 只有30%概率真的惩罚
                screen_flicker()
                print(f"\n  {RED}╔{'═' * 50}╗{RESET}")
                print(f"  {RED}║{RESET}  {BOLD}{RED}✞ 输入无效，重选！{RESET}")
                print(f"  {RED}║{RESET}  {GRAY}连选个烂选项都做不好，你还能做什么？{RESET}")
                print(f"  {RED}╚{'═' * 50}╝{RESET}")
                time.sleep(0.5)
            else:
                print(f"\n  {RED}▶ 请输入数字，你是TM文盲吗？{RESET}")
            continue

        # 数字在有效范围内时，直接返回
        if 1 <= choice_int <= num_options:
            return choice_int
        else:
            # 超出范围
            if random.random() < 0.3:
                screen_flicker()
                print(f"\n  {RED}╔{'═' * 50}╗{RESET}")
                print(f"  {RED}║{RESET}  {BOLD}{RED}✞ 有效选项：1-{num_options}{RESET}")
                print(f"  {RED}║{RESET}  {GRAY}你TM瞎啊？{RESET}")
                print(f"  {RED}╚{'═' * 50}╝{RESET}")
            else:
                print(f"\n  {RED}▶ 有效选项：1-{num_options}{RESET}")


def execute_choice_v2(choice_num, displayed_actions, player):
    """
    执行选择V2 —— 基于显示的选项列表
    """
    # 如果绝望值≥100，返回一个"无意义选择"
    if player.despair >= 100:
        return execute_despair_choice(choice_num, player)

    # 获取玩家选择的动作
    if choice_num < 1 or choice_num > len(displayed_actions):
        return None

    choice_name, choice_id = displayed_actions[choice_num - 1]
    player.choices_log.append(choice_name)

    # 正常选择后重置绝望冷却
    player.despair_cooldown = 0

    print(f"\n  {RED}► 你选择了：{choice_name}{RESET}")

    # 给玩家时间看到自己的选择
    time.sleep(1.0)

    # 实际执行随机负面结果
    result = random.choice(CHOICE_RESULTS[choice_id])
    print(f"\n  {DARK_RED}▶ {result}{RESET}")

    # 从结果中提取属性变化
    process_result(result, player)

    # 随机触发电影彩蛋
    if random.random() < 0.12:
        trigger_movie_quote()

    return result


def execute_despair_choice(choice_num, player):
    """
    绝望模式下的选择 —— 你TM选什么都没区别
    """
    print(f"\n{RED}► 你机械地执行了某个动作...{RESET}")
    print(f"{GRAY}但你TM甚至不确定自己在做什么...{RESET}")

    # 随机触发一个更糟糕的事件
    event = random.choice(HEAVY_EVENTS)
    player.events_log.append(event)
    print(f"\n{DARK_RED}✞ {event} ✞{RESET}")

    # 绝望加深（减少增加量）
    player.despair = min(100, player.despair + 5)
    player.alive_value = max(0, player.alive_value - 3)

    return event


# 选择结果映射 —— 所有结果都是TM烂的，扩展到32个选项
CHOICE_RESULTS = {
    "drink_shit_whisky": [
        "威士忌是假的，你TM喝到胃出血，蜷缩在地板上抽搐",
        "掺水太多，你TM喝完更渴了，渴得你TM想喝自己的尿",
        "你TM喝多了，吐了一地，污渍渗进地板缝里永远洗不掉",
        "酒里好像有什么脏东西，你TM拉肚子拉到虚脱，马桶TM在嘲笑你",
        "味道太TM难喝了，你TM后悔为什么要喝，但已经来不及了",
        "你TM喝太快了，呛得眼泪鼻涕一起流，样子TM比垃圾还狼狈",
        "喝完后你TM开始哭，哭着哭着就睡着了，醒来更TM绝望",
    ],
    "learn_code": [
        "代码被病毒清空了，你TM白写一晚上，每个字母都是讽刺",
        "编程书TM是盗版的，字都看不清，看清了也TM看不懂",
        "你TM看了一会儿就睡着了，醒来发现书被蟑螂啃了",
        "编译器报错了，你TM改了一百遍还是错，错的不是你TM是人生",
        "邻居吵得你TM根本没办法集中，墙薄得像TM不存在",
        "你TM终于看懂了一行代码，然后发现这行代码TM一点用没有",
        "你TM在键盘上睡着了口水流了一键盘，笔记本TM彻底报废",
        "你TM写了三个小时的代码，保存的时候TM蓝屏了",
    ],
    "throw_away_heroin": [
        "SpudTM以为你藏了真的，连夜跑来抢你的钱，你TM被打得鼻青脸肿",
        "房东TM看到了，扣你房租，理由是污染环境",
        "你TM刚扔完就后悔了，跑回去找，发现TM被猫翻出来了",
        "MarkTM看到了，以为你背叛了他，要在群里处理你",
        "你TM扔的是面粉，但TM怀疑自己扔错了，每分每秒都在怀疑",
        "你TM把面粉倒进马桶，马桶TM堵了，屎水倒流",
        "你TM刚扔完就下雨了，雨水把面粉冲得到处都是，TM像在演恐怖片",
    ],
    "call_mark": [
        "MarkTM没给你钱，但塞给你一包真Heroin，你TM知道这是陷阱",
        "MarkTM给你钱，但TM是假的，你TM看不出来，被警察抓了",
        "MarkTM骂了你一顿，把你电话挂了，说你TM不配做他兄弟",
        "MarkTM要你来他那儿，你TM不敢去，但也TM不敢不去",
        "MarkTM说最近风声紧，让你TM小心点，然后TM挂了电话",
        "MarkTM接了，但只要你TM去帮他送货，否则一分钱没有",
        "MarkTM的电话TM打不通，你TM听着忙音，感觉自己TM被世界遗弃了",
    ],
    "lie_down": [
        "你想TM躺平，但连死的力气都没有，身体TM像灌了铅",
        "你TM躺了一会儿，更TM累了，累得每个细胞都在哀号",
        "房东TM来砸门了，你TM只能装死，假装这TM不是你的房子",
        "天TM亮了，你TM还得继续受罪，阳光TM像针一样扎进来",
        "你TM睡着了，做了个TM更烂的梦，梦里你TM在爬一座永远爬不到顶的山",
        "你TM躺着躺着就开始哭，哭着哭着就开始笑，笑自己TM为什么还活着",
        "你TM想睡，但头痛得睡不着，闭上眼睛全是走马灯TM一样的过去",
    ],
    "go_to_bar": [
        "你TM去了酒吧，喝得烂醉如泥，醒来钱包TM空了，人TM躺在巷子里",
        "在酒吧遇到Begbie，他TM非要比划两下，你TM挂了彩",
        "你TM喝多了跟人打架，打架TM没输，但被一群人追着打",
        "酒吧里的妓女对你TM抛媚眼，你TM没钱，只能看着她走向别人",
        "你TM在酒吧听到有人讨论Renton，说他TM去了伦敦，过得TM比你好",
        "你TM喝到一半发现钱包被偷了，只能TM刷盘子抵酒钱",
        "你TM想借酒消愁，结果TM越喝越愁，愁得想把自己TM淹死在酒瓶里",
    ],
    "contact_renton": [
        "Renton的电话TM打不通，你TM听到的是您拨打的用户TM已注销",
        "Renton接了，但他TM只是说我很忙，然后TM挂了",
        "Renton说他在伦敦过得很好，你TM突然觉得自己TM更烂了",
        "你TM发了条消息，消息显示已读，但TM永远没有回复",
        "Renton让你TM去伦敦找他，你TM买得起车票吗？你TM买不起",
        "你TM发现Renton的社交账号把你TM拉黑了",
        "Renton说他在戒毒，你TM突然意识到自己TM还TM在烂泥里",
    ],
    "check_bank": [
        "你的账户TM被冻结了，原因TM未知，你TM看着屏幕发呆",
        "余额显示0.37，你TM想哭，但TM哭不出来",
        "你TM查到有一笔未知转账，TM是你TM之前欠的网贷在利滚利",
        "ATM机TM吞了你的卡，你TM站在机器前，感觉TM被世界抛弃",
        "你TM查到上个月有一笔消费，你TM根本不记得花在哪了",
        "你TM想查明细，但机器显示服务暂时不可用，就像TM你的人生",
        "你TM查到只剩5.32，够买几瓶啤酒，然后TM继续烂",
    ],
    "call_parents": [
        "你TM拨通电话，你TM妈接的，还没开口你TM就先哭了",
        "你TM爸妈把电话挂了，说TM不想再听到你的消息",
        "你TM听到你TM爸的声音，他TM苍老了很多，你TM更TM内疚了",
        "你TM爸妈说他们TM也不容易，让你TM别再打电话来了",
        "你TM想借钱，但你TM妈说家里TM也没余粮了",
        "你TM听到你TM妈在哭，你TM突然挂掉电话，TM不敢再听下去",
        "你TM爸妈让你TM回家，但你TM知道自己TM已经没脸回去了",
    ],
    "find_job": [
        "你TM去了职业中心，那TM的工作人员看你TM像看垃圾",
        "你TM看到一则招聘启示，打电话过去人家TM说已经招满了",
        "你TM填了一堆表格，然后TM石沉大海，连TM回音都没有",
        "你TM去面试，面试官问你TM有什么经验，你TM答不上来",
        "你TM找到一份体力活，但TM当天就被炒了，因为你TM太TM虚弱",
        "你TM想创业，但TM连启动资金都没有，梦想TM就是TM笑话",
        "你TM被告知你TM的技能不符合市场需求，就像你TM这个人不符合人的定义",
    ],
    "clean_room": [
        "你TM开始收拾房间，然后TM发现床底下有一只死老鼠",
        "你TM打扫到一半就累了，躺在脏衣服堆里睡着了",
        "你TM扔掉了很多东西，但TM发现真正该扔的是自己",
        "你TM擦窗户的时候TM看到窗外的海鸥，它们TM看起来比你TM自由",
        "你TM整理书架的时候TM看到那本编程书，TM又陷入了自我怀疑",
        "你TM收拾完了，但TM只是把垃圾从地上移到垃圾桶，TM本质没有变",
        "你TM打扫的时候TM发现房东藏在房间里的摄像头",
    ],
    "accept_fate": [
        "你TM放弃了抵抗，躺在地上看着天花板，TM天花板好像在嘲笑你",
        "你TM接受了这一切，然后TM发现接受比抵抗TM更TM痛苦",
        "你TM不想再挣扎了，但TM身体TM还是TM在呼吸，就像TM在讽刺",
        "你TM闭上眼睛，等待什么TM发生，然后TM什么TM都没发生",
        "你TM觉得自己TM像一具行尸走肉，TM没有灵魂，没有希望",
        "你TM站在原地不动，时间TM在流逝，但你TM感觉TM自己在倒退",
        "你TM接受了，但TM接受本身就是TM一种TM绝望的选择",
    ],
    # 新增20个动作的结果
    "steal_spud_shoes": [
        "皮鞋尺码太小，你TM根本穿不上，只能TM扔了",
        "当铺老板TM看出是偷的，只给你TM£2",
        "SpudTM发现了，跟你TM大打一架",
        "皮鞋TM太臭了，你TM熏得头晕",
        "你TM成功当了£5，但TM转眼就买酒花了",
    ],
    "text_diane": [
        "DianeTM回了，说TM她TM已经搬家了",
        "你TM发了几十条消息，她TM一条都没回",
        "DianeTM把你TM拉黑了，你TM看得到红色的感叹号",
        "她TM回了一句滚，你TM突然TM觉得TM更TM孤独",
        "DianeTM问你TM借钱，你TM哪TM有",
    ],
    "go_internet_cafe": [
        "网吧TM太卡了，你TM连网页都打不开",
        "你TM看到自己TM的帖子被骂翻了",
        "旁边的人TM在看小电影，你TMTM不好意思",
        "网管TM轰你TM走，说你TM太TM臭了",
        "你TM打了一晚上游戏，钱TM花TM光TM了",
    ],
    "graffiti_wall": [
        "你TM写的字TM太TM丑了，连自己TM都不认识",
        "警察TM来了，你TM跑TM得TM太快TM扭TM到TM脚",
        "你TM刚写完，TM就被TM其他TM小TM子TM涂掉了",
        "你TM想表达TM什么，但TM最终TM只是TM画了TM个TM屎",
        "路人TM笑你TM的TM作品，TM你TM想TM钻TM地TM缝",
    ],
    "eavesdrop_neighbor": [
        "邻居TM发现TM你TM了，TM拿TM拖把TM打TM你TM",
        "你TM听到TM他们TM在TM骂你TM，TM你TM更TM抑郁TM了",
        "他们TM吵TM完TM了，TM你TM还TM站TM在TM那TM儿TM",
        "隔壁TM在TM做TM爱，TM你TMTM听TM得TMTM更TMTM难受TM",
        "你TM听到TM自己TM的TM名TM字TM，TM原TM来TM他TM们TM在TM说TM你TM的TM坏TM话TM",
    ],
    "try_quit_drugs": [
        "戒断TM反应TM让TM你TM生不如死，TM你TM又TM去TM找TMMarkTM",
        "你TM坚持TM了TM3TM分TM钟，TM然后TM决TM定TM放TM弃TM",
        "SickBoyTM笑TM你TM天真，TM说TM你TM连TM毒TM都TM戒TM不TM掉TM",
        "你TM去TM戒TM毒TM中心，TM但TM他TM们TM要TM收TM钱TM",
        "你TM以TM为TM自TM己TM能TM戒TM掉，TM结TM果TM更TM想TM了TM",
    ],
    "pray_at_church": [
        "神TM没TM回TM应TM你TM，TM只TM有TM空TM荡TM荡TM的TM回TM声TM",
        "牧TM师TM看TM你TM像TM看TM垃圾，TM把TM你TM赶TM出TM来TM",
        "你TM祈TM祷，TM但TM只TM是TM想TM睡TM觉TM",
        "旁TM边TM的TM人TM在TM笑TM你TM，TM你TM感TM觉TM更TM绝TM望TM",
        "你TM突TM然TM发TM现，TM自TM己TM根TM本TM不TM相TM信TM神TM",
    ],
    "watch_porn": [
        "电脑TM死TM机TM了，TM你TM什TM么TM都TM没TM看TM成TM",
        "看TM完TM更TM空TM虚，TM你TM感TM觉TM自TM己TM更TM可TM悲TM",
        "弹TM出TM广TM告，TM你TM又TM被TM骗TM了TM£50TM",
        "邻TM居TM听TM到TM声TM音，TM来TM敲TM你TM的TM门TM",
        "你TM发TM现TM自TM己TM连TM这TM点TM快TM乐TM都TM找TM不TM到TM",
    ],
    "call_sick_boy": [
        "SickBoyTM要TM你TM去TM帮TM他TM做事，TM你TM不TM敢TM不TM去TM",
        "他TM说TM他TM在TM做TM生TM意，TM问TM你TM要TM不TM要TM入TM伙TM",
        "SickBoyTM把TM你TM的TM电TM话TM挂TM了，TM说TM你TM太TM废TM了TM",
        "他TM叫TM你TM去TM酒TM吧，TM说TM有TM好TM东TM西TM",
        "SickBoyTM说TM他TM在TM伦TM敦，TM叫TM你TM去TM找TM他TM",
    ],
    "stare_at_sea": [
        "海TM鸥TM在TM吃TM东TM西，TM你TM觉TM得TM自TM己TM连TM鸟TM不TM如TM",
        "海TM风TM吹TM得TM你TM发TM抖，TM你TM感TM觉TM更TM冷TM了TM",
        "涨TM潮TM了，TM你TM不TM想TM回TM去，TM但TM也TM没TM地TM方TM去TM",
        "有TM人TM叫TM你TM，TM你TM回TM头TM看，TM只TM是TM卖TM东TM西TM的TM",
        "你TM突TM然TM想TM跳TM下TM去，TM但TM最TM后TM还TM是TM不TM敢TM",
    ],
    "dumpster_dive": [
        "你TM找TM到TM一TM个TM半TM烂TM的TM苹TM果，TM吃TM完TM拉TM肚TM子TM",
        "有TM人TM打TM你，TM说TM你TM是TM垃TM圾TM",
        "你TM找TM到TM一TM件TM衣TM服，TM但TM太TM大TM了TM",
        "翻TM到TM£5TM，TM但TM被TM老TM板TM发TM现TM抢TM走TM了TM",
        "你TM找TM到TM一TM本TM好TM书，TM但TM被TM雨TM淋TM湿TM了TM",
    ],
    "fake_go_work": [
        "你TM在TM公TM司TM门TM口TM站TM了TM一TM天，TM但TM没TM人TM发TM现TM",
        "同TM事TM看TM出TM你TM是TM假TM的，TM在TM背TM后TM笑TM你TM",
        "老TM板TM叫TM你TM滚，TM你TM不TM好TM意TM思TM再TM去TM",
        "你TM站TM了TM一TM天TM太TM累TM了，TM回TM去TM直TM接TM睡TM着TM",
        "邻TM居TM问TM你TM去TM哪TM儿TM了，TM你TM不TM好TM意TM思TM说TM",
    ],
    "write_suicide_note": [
        "你TM写TM了TM半TM天，TM纸TM被TM风TM吹TM走TM了TM",
        "你TM突TM然TM不TM想TM死TM了，TM但TM也TM不TM想TM活TM着TM",
        "写TM完TM了，TM你TM感TM觉TM更TM绝TM望TM了TM",
        "纸TM上TM只TM写TM了TM几TM个TM字，TM你TM不TM知TM道TM写TM什TM么TM",
        "你TM把TM纸TM撕TM了，TM决TM定TM再TM撑TM一TM天TM",
    ],
    "call_hotline": [
        "占TM线，TM你TM等TM了TM半TM小TM时TM",
        "对TM方TM问TM你TM有TM什TM么TM能TM帮TM的，TM你TM说TM不TM出TM话TM来TM",
        "他TM说TM要TM不TM然TM你TM试TM试TM，TM直TM接TM挂TM了TM",
        "你TM听TM了TM半TM天TM心TM灵TM鸡TM汤，TM更TM绝TM望TM了TM",
        "热TM线TM永TM远TM在TM等TM待TM中，TM就像TM你TM的TM人TM生TM",
    ],
    "stalk_stranger": [
        "那TM人TM发TM现TM你TM了，TM把TM你TM打TM了TM一TM顿TM",
        "你TM跟TM到TM一TM半TM迷TM路TM了TM，TM回TM不TM去TM",
        "他TM进TM了TM银TM行，TM你TM不TM敢TM进TM去TM",
        "她TM回TM头TM看TM你TM笑TM了TM一TM下，TM你TM突TM然TM觉TM得TM更TM孤TM独TM",
        "你TM跟TM了TM三TM条TM街，TM最TM后TM放TM弃TM了TM",
    ],
    "drink_on_credit": [
        "酒TM保TM说TM这TM次TM算TM了，TM但TM他TM的TM眼TM神TM很TM不TM屑TM",
        "你TM欠TM了TM£50，TM下TM次TM去TM被TM扣TM下TM",
        "其TM他TM客TM人TM笑TM你TM，TM说TM你TM是TM垃TM圾TM",
        "最TM后TM还TM是TMMarkTM来TM给TM你TM付TM的TM钱TM",
        "你TM喝TM完TM跑TM路，TM被TM追TM了TM半TM条TM街TM",
    ],
    "hack_bank": [
        "你TM根TM本TM不TM懂TM编TM程，TM什TM么TM都TM黑TM不TM进TM去TM",
        "屏TM幕TM弹TM出TM警TM告，TM你TM赶TM紧TM关TM掉TM",
        "你TM试TM了TM半TM天，TM账TM户TM被TM冻TM结TM了TM",
        "突TM然TM弹TM出TM警TM告，TM你TM的TM电TM脑TM被TM黑TM了TM",
        "你TM发TM现TM自TM己TM根TM本TM没TM那TM个TM本TM事TM",
    ],
    "go_library": [
        "图TM书TM馆TM关TM门TM了，TM你TM白TM跑TM一TM趟TM",
        "管TM理TM员TM把TM你TM赶TM出TM来，TM说TM你TM太TM脏TM",
        "你TM找TM到TM一TM本TM好TM书，TM但TM根TM本TM看TM不TM进TM去TM",
        "旁TM边TM的TM学TM生TM在TM笑TM你TM，TM说TM你TM是TM社TM会TM残TM渣TM",
        "你TM看TM了TM半TM天TM书，TM发TM现TM自TM己TM还TM是TM一TM无TM是TM处TM",
    ],
    "play_with_cat": [
        "那TM只TM猫TM抓TM了TM你TM一TM下，TM你TM感TM觉TM更TM疼TM了TM",
        "猫TM走TM了，TM留TM下TM你TM一TM个TM人TM",
        "它TM在TM你TM脚TM边TM蹭TM，TM然TM后TM跑TM了TM",
        "你TM逗TM了TM半TM天TM，TM猫TM根TM本TM不TM理TM你TM",
        "猫TM叫TM了TM几TM声，TM像TM在TM笑TM你TM",
    ],
    "walk_in_rain": [
        "雨TM越TM下TM越TM大，TM你TM全TM身TM都TM湿TM透TM了TM",
        "你TM走TM了TM半TM天，TM发TM现TM自TM己TM根TM本TM没TM地TM方TM去TM",
        "有TM人TM打TM伞TM经TM过，TM看TM你TM像TM看TM怪TM物TM",
        "雷TM声TM吓TM了TM你TM一TM跳，TM你TM觉TM得TM更TM可TM怜TM了TM",
        "你TM走TM到TM底TM，TM发TM现TM只TM是TM浪TM费TM时TM间TM",
    ],
}


def process_result(result, player):
    """
    处理选择结果 —— 让你的属性TM变得更烂
    """
    # 随机扣属性，全部TM是负的（减少绝望增加速度，允许偶尔降低）
    alive_change = random.randint(-12, -2)
    anxiety_change = random.randint(-5, 12)
    # 30%概率绝望减少，让你TM偶尔喘口气
    if random.random() < 0.3:
        despair_change = random.randint(-8, -1)
    else:
        despair_change = random.randint(-2, 6)

    player.alive_value = max(0, min(100, player.alive_value + alive_change))
    player.anxiety = max(0, min(100, player.anxiety + anxiety_change))
    player.despair = max(0, min(100, player.despair + despair_change))

    # 金钱变化（基本上都是TM减少）
    if random.random() < 0.6:
        money_change = random.randint(-15, -1)
        player.money = max(0, player.money + money_change)
        print(f"{GRAY}金钱变化：£{money_change}{RESET}")

    print(f"{GRAY}活着值 {alive_change:+d} | 焦虑值 {anxiety_change:+d} | 绝望值 {despair_change:+d}{RESET}")


def trigger_random_events(player):
    """
    触发随机事件 —— 1-2个随机负面事件（减少数量以便阅读）
    """
    # 减少事件数量，避免信息过载
    num_events = random.randint(1, 2)

    print(f"\n  {RED}╔{'═' * 50}╗{RESET}")
    print(f"  {RED}║{RESET}  {BOLD}{RED}◈ 随机事件触发 ◈{RESET}")
    print(f"  {RED}╚{'═' * 50}╝{RESET}")

    for i in range(num_events):
        # 增加延迟让玩家阅读
        time.sleep(1.0)

        # 80%概率触发基础事件，20%触发重度事件（减少重度事件频率）
        if random.random() < 0.8:
            event = random.choice(BASIC_EVENTS)
            # 基础事件有20%概率稍微减少绝望（让你TM偶尔喘口气）
            if random.random() < 0.2:
                player.despair = max(0, player.despair - 3)
        else:
            event = random.choice(HEAVY_EVENTS)
            # 重度事件额外扣属性（减少绝望增加）
            player.alive_value = max(0, player.alive_value - 5)
            player.despair = min(100, player.despair + 5)

        player.events_log.append(event)

        # 破碎字幕效果
        print(f"  {RED}{broken_text(f'✞ {event} ✞')}{RESET}")

    print()
    # 等待玩家确认后再继续
    input(f"\n  {GRAY}▶ 按回车继续...{RESET}")


def trigger_movie_quote():
    """
    随机触发电影暗黑桥段 —— 让你TM更抑郁
    """
    char, quote = random.choice(MOVIE_QUOTES)

    print(f"\n{BG_BLACK}{GRAY}")
    print(f"╔═══════════════════════════════════════════════╗")
    print(f"║  【电影桥段】                                  ║")
    print(f"║  {char.upper():^40} ║")
    print(f"║  「{quote}」  ║")
    print(f"╚═══════════════════════════════════════════════╝")
    print(f"{RESET}")


# ═══════════════════════════════════════════════════════════════════════════
# 【结局系统】—— 无论如何都是TM烂
# ═══════════════════════════════════════════════════════════════════════════

def determine_ending(player):
    """
    决定你的结局 —— 100%烂结局，无一例外
    """
    rand = random.random()

    if rand < 0.7:
        return "chaos_ending", ENDING_TEXTS["chaos"]
    elif rand < 0.9:
        return "destruction_ending", ENDING_TEXTS["destruction"]
    else:
        return "void_ending", ENDING_TEXTS["void"]


def print_ending(ending_type, ending_text):
    """
    打印结局 —— 让你TM认清现实
    """
    clear_screen()
    print(f"\n")

    # 打印结局艺术字
    print_ascii_art(ENDING_ART)
    print(f"\n")

    # 结局类型显示
    ending_titles = {
        "chaos_ending": "混沌烂局",
        "destruction_ending": "自我毁灭",
        "void_ending": "虚无烂局"
    }
    title = ending_titles.get(ending_type, ending_type)

    print(f"  {RED}╔{'═' * 54}╗{RESET}")
    print(f"  {RED}║{RESET}    {BOLD}{DARK_RED}◈ {title} ◈{RESET}" + " " * (30 - len(title)) + f"{RED}║{RESET}")
    print(f"  {RED}╚{'═' * 54}╝{RESET}")
    print(f"\n")

    # 打字机效果输出结局
    for line in ending_text.split('\n'):
        typewriter_text(f"  {GRAY}{line}{RESET}", delay=0.015)
        time.sleep(0.1)

    print(f"\n")
    print_divider("─", 60, RED)
    print(f"\n")

    # 最终评论 - 逐字显示
    for line in FINAL_COMMENT.split('\n'):
        for char in line:
            sys.stdout.write(f"{RED}{BOLD}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(0.02)
        print()

    print(f"\n")
    # 打印骷髅
    print_ascii_art(SKULL_ART)
    print(f"\n")


ENDING_TEXTS = {
    "chaos": """你选了所有"看似正常"的选项，却还是回到这间出租屋。

编程没学会，那本编程书早就被你TM撕了擦屁股。
钱被骗光，从Mark到Sick Boy，从Spud到你自己，每个人都在骗你。
威士忌掺了水，就像你的人生——连假货都TM是假的。

你站在格拉斯哥阴雨中，看着那些行色匆匆的"正常"人——
他们步履坚定，目光向前，仿佛知道目的地在哪。
他们TM也有房贷，也有烦恼，也TM一样的烂。
只是他们TM会装，装了一辈子，装到死。

你TM终于明白了：
不是你不努力，是努力TM本身就是笑话。
不是你不走运，是运气TM根本不存在。
你只是在这TM无尽的混沌中漂浮，
等待某天彻底沉底，连气泡都不留下。""",

    "destruction": """你选了所有"放纵"的选项，最后躺在医院。

戒断反应让你吐到虚脱，胆汁都TM吐出来了，
你TM看着天花板，想起那些年在马桶边抽搐的日子。
医生说"再作就死"，你TM突然笑了——

你以为你还有选择吗？
你以为你TM有的选吗？

从你TM生下来的那一刻，从你TM被丢进这TM垃圾堆一样的人生开始，
结局就TM已经写好了。

你TM只是个废物。
这不是悲剧，这是TM日常。
每天TM醒来，每天TM死去，每天TM重复。
出院后还是会一样——
一样的烂，一样的绝望，一样的无路可走。

Begbie说得对：
"你TM就是TM一坨屎，永远TM是。" """,

    "void": """你选了半天，发现所有选择都TM没用。

房租还是欠着，房东TM在砸门，你TM假装不在家。
朋友还是骗你，MarkTM在利用你，Sick BoyTM在嘲笑你，SpudTM在偷你的东西。
代码还是写不出来，那些字母TM认识你你不认识它们。

人生就是一场没得选的烂戏，
你TM只是个演员，演着别人写好的剧本。
观众TM早就离场了，评论家TM早就走人了，
只剩你TM还在舞台上，假装着有台词，假装着有观众。

你TM突然意识到：
根本没有"选择"这回事。
你TM以为你在选，其实只是TM在等——等命运TM来决定怎么TM弄死你。

这不是虚无，这是TM绝望。
这不是悲剧，这是TM现实。
现实TM就是这样：没有救赎，没有希望，没有意义。

然后呢？
然后TM继续活着，像TM一具行尸走肉，
然后TM继续等死，像TM所有人一样。"""
}

FINAL_COMMENT = """Choose Life？

别自欺欺人了。

生活从来没有给你选择。
它TM只是让你TM以为你有选择——
然后看着你TM挣扎，看着你TM绝望，看着你TM腐烂。

你TM烂在格拉斯哥的出租屋里，
烂在无尽的混沌里，
烂在每一个TM以为会有转机的清晨。

这就是人生：
TM没有意义，
TM没有出口，
TM没有救赎。

唯一TM确定的，
是TM死亡——
而你TM甚至TM没有TM勇气TM去TM拥抱TM它。"""


# ═══════════════════════════════════════════════════════════════════════════
# 【人生烂账】—— 记录你TM有多烂
# ═══════════════════════════════════════════════════════════════════════════

def save_life_record(player):
    """
    强制生成"人生烂账.txt" —— 记录你TM的所有烂选择
    """
    filename = "人生烂账.txt"

    with open(filename, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("人生烂账 —— 你的失败全记录\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"存活轮数：{player.round} 轮\n")
        f.write(f"最终状态：焦虑{player.anxiety}/100 | 活着{player.alive_value}/100 | 绝望{player.despair}/100\n")
        f.write(f"剩余金钱：£{player.money}\n\n")

        f.write("-" * 60 + "\n")
        f.write("你的选择（全是TM没用的）：\n")
        f.write("-" * 60 + "\n")
        for i, choice in enumerate(player.choices_log, 1):
            f.write(f"  {i}. {choice}\n")

        f.write("\n")
        f.write("-" * 60 + "\n")
        f.write("随机事件（生活TM对你的暴打）：\n")
        f.write("-" * 60 + "\n")
        for i, event in enumerate(player.events_log, 1):
            f.write(f"  {i}. {event}\n")

        f.write("\n")
        f.write("=" * 60 + "\n")
        f.write("这就是你的人生——烂，且无解\n")
        f.write("=" * 60 + "\n")

    print(f"\n{GRAY}▓ 人生烂账已保存至：{filename}{RESET}")


# ═══════════════════════════════════════════════════════════════════════════
# 【主循环】—— 你的TM人生还在继续
# ═══════════════════════════════════════════════════════════════════════════

def game_loop():
    """
    主游戏循环 —— 你TM逃不掉的
    """
    print_title()

    # 创建玩家
    player = HumanTrash()

    # 应用初始debuff
    apply_initial_debuff(player)

    print(f"\n{RED}{BOLD}准备好了吗？你TM根本没得选{RESET}")
    input(f"\n{GRAY}按回车键开始你的烂人生...{RESET}")

    # 游戏主循环
    while True:
        player.round += 1

        print(f"\n")
        print(f"  {DARK_RED}╔{'═' * 54}╗{RESET}")
        print(f"  {DARK_RED}║{RESET}  {BOLD}{RED}◈ 第 {player.round:>2} 轮 ◈{RESET}" + " " * 28 + f"{DARK_RED}║{RESET}")
        print(f"  {DARK_RED}╚{'═' * 54}╝{RESET}")

        # 打印状态
        print_status(player)

        # 描述场景，获取显示的选项数量和对应的动作
        num_options, displayed_actions = describe_scene(player)

        # 获取选择
        choice = get_choice(
            f"{RED}► 选择你的动作 (1-{num_options}): {RESET}",
            num_options,
            player
        )

        # 执行选择（附带随机反转）
        execute_choice_v2(choice, displayed_actions, player)

        # 触发随机事件
        trigger_random_events(player)

        # 更新状态
        player.drag_you_to_hell()

        # 检查是否结束（纯粹随机，15-25轮后大概率结束）
        if player.round >= random.randint(15, 25):  # 15-25轮随机结束
            # 但也有小概率提前结束（遭遇重大打击）
            if random.random() < 0.1:
                print(f"\n{RED}{BOLD}✞ 命运给了你最后一击 ✞{RESET}")
                print(f"{GRAY}你TM终于撑不住了...{RESET}")
                break
            break

        # 让玩家按回车继续，给时间阅读
        input(f"\n  {GRAY}▶ 按回车继续下一轮...{RESET}")

    # 结算结局
    ending_type, ending_text = determine_ending(player)
    print_ending(ending_type, ending_text)

    # 保存烂账
    save_life_record(player)

    # 强制循环
    ask_replay()


def ask_replay():
    """
    强制循环 —— 你TM以为能退出？
    """
    print(f"\n{RED}{BOLD}再来一局？（Y/N）{RESET}")

    while True:
        response = input(f"{GRAY}> {RESET}").strip().upper()

        if response == 'Y':
            print(f"\n{DARK_RED}{BOLD}很好，你TM就喜欢受虐{RESET}")
            time.sleep(1)
            game_loop()
            return
        elif response == 'N':
            # 强制继续！哈哈！
            print(f"\n{RED}{BOLD}✞ 你以为能退出？人生可不会让你选 ✞{RESET}")
            print(f"{GRAY}...你TM还是得继续{RESET}")
            time.sleep(1.5)
            game_loop()
            return
        else:
            print(f"{RED}输入Y或N，你TM文盲吗？{RESET}")


# ═══════════════════════════════════════════════════════════════════════════
# 【程序入口】—— 你的TM人生开始了
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # 欢迎来到TM现实
    clear_screen()
    print(f"\n")

    # 打印标题艺术字
    print_ascii_art(TITLE_ART)
    print(f"\n")

    # 副标题
    print(f"  {DARK_RED}╔{'═' * 56}╗{RESET}")
    print(f"  {DARK_RED}║{RESET}    {GRAY}C H O O S E   L I F E   =   C H O O S E   M I S E R Y{RESET}    {DARK_RED}║{RESET}")
    print(f"  {DARK_RED}╚{'═' * 56}╝{RESET}")

    print(f"\n")
    print(f"  {DARK_GRAY}┌{'─' * 56}┐{RESET}")
    print(f"  {DARK_GRAY}│{RESET}  {GRAY}「人生本就是烂局，选择只是换种烂法」{GRAY:^20}  {DARK_GRAY}│{RESET}")
    print(f"  {DARK_GRAY}│{RESET}                                                         {DARK_GRAY}│{RESET}")
    print(f"  {DARK_GRAY}│{RESET}    {RED}这里没有救赎，没有希望，没有好结局{RESET}       {DARK_GRAY}│{RESET}")
    print(f"  {DARK_GRAY}│{RESET}           {GRAY}你TM准备好了吗？{RESET}                      {DARK_GRAY}│{RESET}")
    print(f"  {DARK_GRAY}└{'─' * 56}┘{RESET}")

    print(f"\n\n")
    print(f"  {DARK_RED}【操作说明】{RESET}")
    print(f"  {GRAY}输入数字选择选项，按回车确认{RESET}")
    print(f"  {GRAY}注意：你TM的每个选择都会让你TM更烂{RESET}")
    print(f"\n")

    print_divider("─", 60, DARK_RED)
    print(f"\n")

    input(f"  {GRAY}▶ 按回车键开始你的烂人生...{RESET}")

    # 开始游戏
    game_loop()


# ═══════════════════════════════════════════════════════════════════════════
# 【开发者诅咒】
# ═══════════════════════════════════════════════════════════════════════════
#
# 如果你觉得这个程序烂，那恭喜你——
# 你TM终于看懂了人生。
#
# "Choose life" is a lie.
# Life chooses you, and it chooses suffering.
# That's it. That's the truth.
#
# ───────────────────────────────────────────────────────────────────────────
# ✞ R.I.P. 1996-2026. All of us. ✞
# ═══════════════════════════════════════════════════════════════════════════
