# -*- coding: utf-8 -*-
"""
Game engine module
Core game logic including turn management, events, endings, etc.
"""
import random
from models.event import STORY_EVENTS, EventType, GameEvent
from models.npc import update_relationship_state
from data.events_data import CHOICE_RESULTS, BASIC_EVENTS, HEAVY_EVENTS


class GameEngine:
    """Core game engine handling game logic"""

    def __init__(self, player):
        self.player = player
        self.last_event_round = 0

    def trigger_events(self):
        """触发事件"""
        current_round = self.player.round
        triggered_texts = []

        # 检查条件触发事件
        for event_id, event in STORY_EVENTS.items():
            if event.event_type in (EventType.CONDITION_TRIGGERED, EventType.STORY_CHAPTER):
                if event_id not in self.player.triggered_events:
                    if event.can_trigger(self.player, current_round):
                        narrative = event.trigger(self.player)
                        triggered_texts.append(narrative)
                        self.player.triggered_events.add(event_id)

        # 随机事件 - 降低概率
        if current_round - self.last_event_round > 3:
            if random.random() < 0.10:  # 10% 概率
                event = random.choice(BASIC_EVENTS)
                triggered_texts.append(event[0])
                if len(event) > 2:
                    self.player.apply_effect('cash', event[2])
                self.last_event_round = current_round

            elif random.random() < 0.03:  # 3% 概率重型事件
                event = random.choice(HEAVY_EVENTS)
                triggered_texts.append(event[0])
                if len(event) > 2:
                    self.player.apply_effect('cash', event[2])
                self.last_event_round = current_round

        return "\n\n".join(triggered_texts) if triggered_texts else None

    def parse_effect(self, effect_str):
        """解析效果字符串"""
        effect_map = {
            "清醒度-": "sober",
            "清醒度+": "sober",
            "信誉-": "reputation",
            "信誉+": "reputation",
            "戒断值-": "withdrawal",
            "戒断值+": "withdrawal",
            "焦虑+": "anxiety",
            "焦虑-": "anxiety",
            "绝望+": "despair",
            "绝望-": "despair",
            "money": "cash",
        }

        for prefix, stat in effect_map.items():
            if effect_str.startswith(prefix):
                try:
                    value = int(effect_str[len(prefix):])
                    return stat, value
                except:
                    pass
        return None, None

    def apply_choice_result(self, action_id):
        """应用选择结果"""
        results = CHOICE_RESULTS.get(action_id, [])
        if not results:
            return None, []

        result = random.choice(results)
        narrative = result[0]
        effects = result[1:]

        effect_texts = []
        for effect in effects:
            if isinstance(effect, str):
                stat, value = self.parse_effect(effect)
                if stat:
                    self.player.apply_effect(stat, value)
                    effect_texts.append(f"{stat}+{value}" if value > 0 else f"{stat}{value}")
                    # 更新任务进度
                    if self.player.quest_manager:
                        self.player.quest_manager.update_quest_progress(stat=stat, value=value)
            elif isinstance(effect, (int, float)):
                self.player.apply_effect('cash', effect)
                # 更新任务进度
                if self.player.quest_manager:
                    self.player.quest_manager.update_quest_progress(stat='cash', value=effect)

        return narrative, effect_texts

    def check_endings(self):
        """检查是否触发结局"""
        # 清醒度归零
        if self.player.sober <= 0:
            return "sober"
        # 现金为负
        if self.player.cash < 0:
            return "debt"

        # 戒断值过高可能导致过量
        if self.player.withdrawal >= 95 and random.random() < 0.3:
            return "overdose"

        # 没钱+低清醒度可能入狱
        if self.player.cash < 10 and self.player.sober < 20 and random.random() < 0.2:
            return "arrest"

        # 长时间存活可能触发神秘结局
        if self.player.day > 20 and self.player.round > 50 and random.random() < 0.1:
            return "mysterious"

        # 高绝望值可能触发特殊结局
        if self.player.despair >= 95:
            if random.random() < 0.3:
                return "overdose"

        # 正面结局触发条件
        # 高清醒度+高信誉+有钱 = 人生赢家
        if self.player.sober >= 80 and self.player.reputation >= 70 and self.player.cash >= 200:
            if random.random() < 0.15:
                return "success"

        # 戒掉毒瘾 = 救赎
        if self.player.withdrawal == 0 and self.player.sober >= 60 and self.player.day > 10:
            if random.random() < 0.1:
                return "redemption"

        return None

    def get_ending(self, reason):
        """获取结局文本"""
        endings = {
            "normal": ("混沌烂局", "你选了那么久，最后还是回到这间出租屋...\n\n钱花光了，朋友背叛了，清醒度归零了。\n\n你终于明白了：\n\n人生就是TM一坨屎——\n而你只是屎上那只蠕动的蛆。"),
            "landlord": ("被赶出门", "房东把你赶出来了！\n\n你连房租都交不起，还谈什么人生？\n\n滚出去喝西北风吧！\n\n——不过想想，你本来就 在喝西北风。"),
            "debt": ("债务爆炸", "你欠了一屁股债！\n\n追债的天天上门，你还能躲去哪？"),
            "sober": ("清醒度归零", "你终于彻底麻木了...\n\n清醒度归零，你活着跟死了有什么区别？\n\n没有。\n\n真的没有。"),
            "hiv": ("绝望深渊", "你收到了HIV检测结果——阳性。\n\n这个世界在你眼前崩塌。\n\n也许这就是你最后一次放纵的代价。"),
            "arrest": ("锒铛入狱", "警车带走了你。\n\n在监狱里，你终于有了栖身之地。\n\n只是这代价太大了。"),
            "overdose": ("过量身亡", "你的人生在那一刻停止了。\n\n也许在某个瞬间，你曾经想要改变。\n\n但现在一切都晚了。"),
            "redemption": ("自我救赎", "你终于戒掉了毒瘾！\n\n虽然人生已经一团糟，但你决定重新开始。\n\n这是你应得的——一个新的开始。"),
            "success": ("人生赢家", "你他妈的居然成功了！\n\n找到工作，戒掉毒瘾，还清债务。\n\n在这个操蛋的世界里，你赢了。"),
            "mysterious": ("神秘消失", "你消失了。\n\n没有人知道你去了哪里。\n\n也许这是最好的结局。"),
        }
        return endings.get(reason, endings["normal"])

    def save_record(self, ending_type):
        """保存游戏记录"""
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

    def handle_call_mark(self):
        """处理给Mark打电话"""
        from tkinter import simpledialog
        import tkinter as tk

        choice = simpledialog.askstring("Mark", "Mark接了电话:\n'哟，怎么想起给我打电话了？'\n\n1. 问他最近怎么样\n2. 跟他套近乎\n3. 直接挂断", parent=self.player.root)

        result_text = ""
        mark_rel = self.player.relationships.get('mark')

        if choice == "1":
            result_text = "Mark: '还行吧，最近生意不错.'\n"
            if mark_rel:
                mark_rel.affinity += 5
                mark_rel.positive_interactions += 1
                update_relationship_state(mark_rel)
            self.result_label.configure(text=self.result_label.cget("text") +
                "\n\n" + "Mark: '还行吧，最近生意不错.'")
        elif choice == "2":
            result_text = "Mark: '少来这套，有屁快放。'\n"
            if mark_rel:
                mark_rel.affinity -= 5
                mark_rel.negative_interactions += 1
                update_relationship_state(mark_rel)
            self.result_label.configure(text=self.result_label.cget("text") +
                "\n\n" + "Mark: '少来这套，有屁快放。'")
        else:
            result_text = "你挂断了电话。\n"
            self.result_label.configure(text=self.result_label.cget("text") +
                "\n\n" + "你挂断了电话。")

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='mark')

        return result_text

    def handle_call_parents(self):
        """处理给父母打电话"""
        from tkinter import simpledialog

        choice = simpledialog.askstring("父母",
            "电话接通了...\n\n1. 嘘寒问暖\n2. 委婉地要钱\n3. 告诉他们你想回家\n4. 挂断", parent=self.player.root)

        result_text = ""
        if choice == "1":
            result_text = "► 你选择了：嘘寒问暖\n\n母亲的声音有些颤抖：\n'儿子，我们都很担心你...'"
            self.player.apply_effect('reputation', 5)
            self.player.apply_effect('hope', 5)
            self.player.story_flags['called_parents_home'] = True
        elif choice == "2":
            result_text = "► 你选择了：要钱\n\n父亲沉默了很久，然后叹了口气：\n'我下午转账给你...'"
            self.player.apply_effect('cash', 40)
            self.player.apply_effect('reputation', -5)
            self.player.story_flags['asked_parents_for_money'] = True
        elif choice == "3":
            result_text = "► 你选择了：告诉他们想回家\n\n母亲哭了出来：\n'太好了太好了...你爸虽然嘴上不说，但天天念叨你...'"
            self.player.apply_effect('hope', 15)
            self.player.apply_effect('despair', -10)
            self.player.story_flags['reconnected_with_mother'] = True
        else:
            result_text = "► 你选择了：挂断\n\n你按下挂断键，泪水在眼眶里打转..."

        return result_text

    def handle_text_diane(self):
        """处理给Diane发短信"""
        from tkinter import simpledialog

        choice = simpledialog.askstring("Diane",
            "你编辑着给Diane的消息...\n\n1. 发一句'最近还好吗'\n2. 发一句'我想你'\n3. 算了，不发了", parent=self.player.root)

        result_text = ""
        diane_rel = self.player.relationships.get('diane')

        if choice == "1":
            result_text = "► 你选择了：问好\n\nDiane很快回复了:\n'挺好的，你呢？'"
            if diane_rel:
                diane_rel.affinity += 10
                diane_rel.positive_interactions += 1
                update_relationship_state(diane_rel)
            self.player.apply_effect('hope', 5)
        elif choice == "2":
            result_text = "► 你选择了：表白\n\n消息显示已读...\n\n很久之后，Diane回复:\n'我们已经结束了.'"
            if diane_rel:
                diane_rel.affinity -= 10
                diane_rel.negative_interactions += 1
                update_relationship_state(diane_rel)
            self.player.apply_effect('despair', 10)
        else:
            result_text = "► 你选择了：放弃\n\n你删掉了打好的字，心里空落落的..."

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='diane')

        return result_text

    def handle_contact_renton(self):
        """处理联系Renton"""
        from tkinter import simpledialog

        choice = simpledialog.askstring("Renton",
            "你拨通了Renton的号码...\n\n1. 求他回来\n2. 问他在伦敦怎么样\n3. 什么都不说", parent=self.player.root)

        result_text = ""
        renton_rel = self.player.relationships.get('renton')

        if choice == "1":
            result_text = "► 你选择了：求他回来\n\n电话那头沉默了很久...\n\n'我会回来的。但你要答应我，好好活着。'"
            if renton_rel:
                renton_rel.affinity += 15
                renton_rel.positive_interactions += 1
                update_relationship_state(renton_rel)
            self.player.apply_effect('hope', 20)
        elif choice == "2":
            result_text = "► 你选择了：问近况\n\n'伦敦很好，一切都重新开始。'\n\n'Renton，我...'"
            if renton_rel:
                renton_rel.affinity -= 5
                update_relationship_state(renton_rel)
        else:
            result_text = "► 你选择了：什么都不说\n\n电话那头只有你的呼吸声...\n\n然后Renton先挂断了。"
            if renton_rel:
                renton_rel.affinity -= 5
                update_relationship_state(renton_rel)

        if self.player.quest_manager:
            self.player.quest_manager.update_quest_progress(npc_id='renton')

        return result_text

    def handle_call_sick_boy(self):
        """处理给Sick Boy打电话"""
        from tkinter import simpledialog

        choice = simpledialog.askstring("Sick Boy",
            "Sick Boy接了电话：\n'Shit happens. 什么事？'\n\n1. 问有没有新货\n2. 问他最近在干嘛\n3. 问能不能帮忙", parent=self.player.root)

        result_text = ""
        sick_boy_rel = self.player.relationships.get('sick_boy')

        if choice == "1":
            result_text = "► 你选择了：问新货\n\n'新货到了，要来点吗？£40一包'"
            self.player.apply_effect('cash', -40)
            self.player.apply_effect('withdrawal', -30)
            if sick_boy_rel:
                sick_boy_rel.affinity += 5
                update_relationship_state(sick_boy_rel)
        elif choice == "2":
            result_text = "► 你选择了：闲聊\n\n'我？我在写诗。在这座腐烂的城市里，只有艺术是永恒的。'"
            self.player.apply_effect('sober', 5)
            if sick_boy_rel:
                sick_boy_rel.affinity += 10
                update_relationship_state(sick_boy_rel)
        else:
            result_text = "► 你选择了：求助\n\n'我？帮你？你拿什么还？'"
            if sick_boy_rel:
                sick_boy_rel.affinity -= 5
                update_relationship_state(sick_boy_rel)
            self.player.apply_effect('despair', 5)

        return result_text
