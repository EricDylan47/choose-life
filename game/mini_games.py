# -*- coding: utf-8 -*-
"""
Mini-games module
Contains all mini-game implementations
"""
import random
import time


class MiniGames:
    """Handler class for all mini-games"""

    @staticmethod
    def handle_begbie_gamble(root, player, result_callback):
        """Begbie的骰子赌博游戏"""
        import tkinter as tk
        from config import BG_DARK, DARK_GRAY, RED

        result_label_text = ["Begbie拿出三颗骰子:\n'赌大小，£20一次。'\n\n在三颗骰子上点击选择你的猜测方向!"]

        dialog = tk.Toplevel(root)
        dialog.title("Begbie的赌博")
        dialog.geometry("400x250")
        dialog.configure(bg=BG_DARK)

        result_text = [""]

        def bet_big():
            result_text[0] = ""
            dice = [random.randint(1, 6) for _ in range(3)]
            total = sum(dice)
            win = total >= 11  # 大: 11-18
            result_text[0] = f"骰子: {dice} = {total}\n"
            if win:
                result_text[0] += f"你赢了! 获得 £20!"
                player.cash += 20
            else:
                result_text[0] += f"你输了! 失去 £20!"
                player.cash -= 20
            dialog.destroy()

        def bet_small():
            result_text[0] = ""
            dice = [random.randint(1, 6) for _ in range(3)]
            total = sum(dice)
            win = total <= 10  # 小: 3-10
            result_text[0] = f"骰子: {dice} = {total}\n"
            if win:
                result_text[0] += f"你赢了! 获得 £20!"
                player.cash += 20
            else:
                result_text[0] += f"你输了! 失去 £20!"
                player.cash -= 20
            dialog.destroy()

        tk.Label(dialog, text="点击下方按钮选择:", fg="#FFA500", bg=BG_DARK,
                font=("Courier", 14)).pack(pady=20)

        btn_frame = tk.Frame(dialog, bg=BG_DARK)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="🔴 押 大 (11-18)", fg=RED, bg=DARK_GRAY,
                font=("Courier", 14), width=15, command=bet_big).pack(pady=5)
        tk.Button(btn_frame, text="🔵 押 小 (3-10)", fg="#4169E1", bg=DARK_GRAY,
                font=("Courier", 14), width=15, command=bet_small).pack(pady=5)

        dialog.wait_window()
        result_callback(result_text[0])

    @staticmethod
    def handle_drinking_contest(root, player, result_callback):
        """酒吧拼酒小游戏"""
        import tkinter as tk
        from config import BG_DARK, DARK_GRAY, GREEN

        dialog = tk.Toplevel(root)
        dialog.title("拼酒挑战")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_DARK)

        clicks = [0]
        max_clicks = 5
        start_time = [time.time()]
        success = [False]
        result_text = [""]

        def on_click():
            clicks[0] += 1
            btn.configure(text=f"已喝: {clicks[0]}/{max_clicks} 杯")
            if clicks[0] >= max_clicks:
                elapsed = time.time() - start_time[0]
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
            result_text[0] = f"✓ 你在{time.time()-start_time[0]:.1f}秒内喝完了!\n获得 £30!"
            player.cash += 30
            player.sober -= 20
        else:
            result_text[0] = "✗ 你喝得太慢了...\n没有得到奖金"
            player.sober -= 10

        result_callback(result_text[0])

    @staticmethod
    def handle_steal_bar_liquor(root, player, result_callback):
        """偷酒小游戏 - 时机游戏"""
        import tkinter as tk
        from config import BG_DARK, DARK_GRAY, BLACK

        dialog = tk.Toplevel(root)
        dialog.title("偷酒")
        dialog.geometry("400x250")
        dialog.configure(bg=BG_DARK)

        # 游戏状态
        colors = ["#FF0000", "#FF6600", "#FFFF00", "#00FF00", "#00FF00", "#FF0000"]
        color_names = ["太早!", "太早!", "准备...", "抢!", "成功!", "太晚!"]
        current_idx = [0]
        game_running = [True]
        result_text = [""]

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
            if current_idx[0] in [3, 4]:  # 绿色
                result_text[0] = "✓ 你成功偷到一瓶好酒!\n当掉获得 £25"
                player.cash += 25
            else:
                result_text[0] = "✗ 被发现了! 你拔腿就跑,\n什么都没拿到"
                player.sober -= 10
            dialog.destroy()

        indicator = tk.Label(dialog, text="等待...", fg=BLACK, bg="#FF0000",
                           font=("Courier", 24, "bold"), width=10, height=3)
        indicator.pack(pady=20)

        tk.Button(dialog, text="动手!", fg=RED, bg=DARK_GRAY,
                  font=("Courier", 16), width=15, height=2, command=try_steal).pack(pady=20)

        dialog.after(1000 + random.randint(500, 2000), change_color)
        dialog.wait_window()
        result_callback(result_text[0])

    @staticmethod
    def handle_spud_cards(root, player, result_callback):
        """和Spud玩纸牌 - 21点"""
        from tkinter import simpledialog

        player_total = 15
        result_text = [""]

        choice = simpledialog.askstring("21点",
            "你的初始两张牌:\nJ和5 = 15点\n\n要牌(y)或停止(n)?",
            parent=root)

        if choice and choice.lower() == 'y':
            card = random.randint(2, 11)
            player_total += card
            if player_total > 21:
                result_text[0] = f"你抽到了{card}, 总共{player_total}点 - 爆了!\n你输了£15"
                player.cash -= 15
            else:
                # 第二次选择
                choice2 = simpledialog.askstring("21点",
                    f"你现在{player_total}点\n要牌(y)或停止(n)?",
                    parent=root)
                if choice2 and choice2.lower() == 'y':
                    card2 = random.randint(2, 11)
                    player_total += card2
                    if player_total > 21:
                        result_text[0] = f"你抽到了{card2}, 总共{player_total}点 - 爆了!\n你输了£15"
                        player.cash -= 15
                    else:
                        result_text[0] = f"你停牌, {player_total}点.\n"
                else:
                    result_text[0] = f"你停牌, {player_total}点.\n"
        else:
            result_text[0] = f"你停牌, {player_total}点.\n"

        # Spud的牌
        spud_total = random.randint(15, 21)
        result_text[0] += f"Spud: {spud_total}点\n"

        if player_total <= 21:
            if player_total > spud_total:
                result_text[0] += "✓ 你赢了! 获得 £15!"
                player.cash += 15
            elif player_total == spud_total:
                result_text[0] += "平局! 钱退给你."
            else:
                result_text[0] += "✗ 你输了."
                player.cash -= 15
        else:
            result_text[0] += "✗ 你已经爆了."

        result_callback(result_text[0])

    @staticmethod
    def handle_pawnshop(root, player, result_callback):
        """当铺讨价还价"""
        from tkinter import simpledialog

        result_text = [""]

        choice = simpledialog.askstring("当铺",
            "你有什么可以当的?\n1. 旧手表 (值£20)\n2. 收音机 (值£15)\n3. 相机 (值£30)\n4. 什么都不当\n输入 1, 2, 3 或 4:",
            parent=root)

        if choice == "1":
            result_text[0] = "你拿出旧手表...\n老板看了看: '£8, 要当就当.'\n\n你与他讨价还价..."
            offer = 8
        elif choice == "2":
            result_text[0] = "你拿出收音机...\n老板按下开关: '坏的. £5, 爱当不当.'\n\n你与他讨价还价..."
            offer = 5
        elif choice == "3":
            result_text[0] = "你拿出相机...\n老板检查了一下: '镜头花了. £15.'\n\n你与他讨价还价..."
            offer = 15
        else:
            result_text[0] = "你看了一圈, 什么都没当."
            result_callback(result_text[0])
            return

        # 讨价还价小游戏
        counter = simpledialog.askstring("讨价还价",
            f"老板开价£{offer}, 你想加多少?\n(输入数字, 如 5 表示要加£5)\n或者直接回车接受:",
            parent=root)

        if counter:
            try:
                add = int(counter)
                final_offer = offer + add
                if final_offer <= offer * 1.5:  # 最高加50%
                    result_text[0] += f"\n老板摇头: '不行, {final_offer}太多了.'"
                    result_text[0] += f"\n最终以 £{offer} 当掉."
                    player.cash += offer
                else:
                    result_text[0] += f"\n老板叹气: '行行行, 你的了. £{final_offer}'"
                    player.cash += final_offer
            except:
                result_text[0] += f"\n你接受了 £{offer}."
                player.cash += offer
        else:
            result_text[0] += f"\n你接受了 £{offer}."
            player.cash += offer

        result_callback(result_text[0])

    @staticmethod
    def handle_dumpster_dive(root, player, result_callback):
        """翻垃圾桶小游戏"""
        import tkinter as tk
        from config import BG_DARK, DARK_GRAY, YELLOW, GREEN

        dialog = tk.Toplevel(root)
        dialog.title("翻垃圾桶")
        dialog.geometry("400x200")
        dialog.configure(bg=BG_DARK)

        clicks = [0]
        max_clicks = 10
        result_text = [""]

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

        result_text[0] = f"\n\n你找到了: {item[0]}!\n现金: £{item[1]}, 清醒度: {item[2]}"
        player.cash = max(0, player.cash + item[1])
        player.sober = max(0, min(100, player.sober + item[2]))
        result_callback(result_text[0])

    @staticmethod
    def handle_find_job(root, player, result_callback):
        """找工作面试小游戏"""
        from tkinter import simpledialog

        score = 0
        result_text = [""]

        choice = simpledialog.askstring("面试",
            "面试官问: 你为什么想来这里工作?\n1. 因为我需要钱\n2. 我热爱工作\n3. 没为什么\n输入 1, 2 或 3:",
            parent=root)

        if choice == "1":
            score += 2
            result_text[0] = "面试官点了点头"
        elif choice == "2":
            score += 1
            result_text[0] = "面试官茫然看着你"
        else:
            result_text[0] = "面试官皱起眉头"

        choice2 = simpledialog.askstring("面试",
            "面试官问: 你的最长工作时间 是?\n1. 一天\n2. 一星期\n3. 我很勤奋\n输入 1, 2 或 3:",
            parent=root)

        if choice2 == "1":
            score += 2
        elif choice2 == "2":
            score += 1

        if score >= 3:
            result_text[0] += f"\n\n恭喜! 你被录取了!\n日薪£50!"
            player.cash += 50
            player.sober += 10
        elif score >= 1:
            result_text[0] += f"\n\n面试官说会考虑...\n\n三天后你收到通知，被录用! 日薪£25"
            player.cash += 25
        else:
            result_text[0] += f"\n\n面试官摆了摆手:\n'你可以走了。'"

        result_callback(result_text[0])
