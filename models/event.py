# -*- coding: utf-8 -*-
"""
Event system module
"""


# ═══════════════════════════════════════════════════════════════════════════
# 事件系统重构
# ═══════════════════════════════════════════════════════════════════════════
class EventType:
    CONDITION_TRIGGERED = 'condition'
    QUEST_TRIGGERED = 'quest'
    NPC_RELATED = 'npc'
    RANDOM_MINOR = 'random_minor'
    RANDOM_MAJOR = 'random_major'
    STORY_CHAPTER = 'story'


class GameEvent:
    """游戏事件类"""
    def __init__(self, event_id, event_type, narrative, effects, conditions=None, probability=0.0, min_day=None, max_day=None, cooldown_rounds=0, quest_id=None, npc_id=None):
        self.event_id = event_id
        self.event_type = event_type
        self.narrative = narrative
        self.effects = effects  # [{'stat': str, 'value': int}, ...]
        self.conditions = conditions or {}
        self.probability = probability
        self.min_day = min_day
        self.max_day = max_day
        self.cooldown_rounds = cooldown_rounds
        self.quest_id = quest_id
        self.npc_id = npc_id
        self.last_triggered_round = None

    def can_trigger(self, player, current_round):
        """检查事件是否可以触发"""
        # 冷却检查
        if self.last_triggered_round and (current_round - self.last_triggered_round) < self.cooldown_rounds:
            return False

        # 天数检查
        if self.min_day and player.day < self.min_day:
            return False
        if self.max_day and player.day > self.max_day:
            return False

        # 条件检查
        if self.conditions:
            # NPC关系条件
            npc_reqs = self.conditions.get('npc_relationships', {})
            for npc_id, (req_state, min_affinity) in npc_reqs.items():
                rel = player.relationships.get(npc_id)
                if not rel:
                    return False
                if isinstance(req_state, list):
                    if rel.state not in req_state:
                        return False
                elif rel.state != req_state:
                    return False
                if min_affinity and rel.affinity < min_affinity:
                    return False

            # 属性条件
            stat_checks = self.conditions.get('stat_checks', {})
            for stat, (op, value) in stat_checks.items():
                current = getattr(player, stat, 0)
                if op == '>=' and not (current >= value):
                    return False
                elif op == '>' and not (current > value):
                    return False
                elif op == '<=' and not (current <= value):
                    return False
                elif op == '<' and not (current < value):
                    return False
                elif op == '==' and not (current == value):
                    return False

            # 故事标志条件
            story_flags_req = self.conditions.get('story_flags', {})
            for flag, expected_value in story_flags_req.items():
                actual_value = player.story_flags.get(flag)
                if expected_value is True:
                    if not actual_value:
                        return False
                elif actual_value != expected_value:
                    return False

        return True

    def trigger(self, player):
        """触发事件"""
        self.last_triggered_round = player.round
        for effect in self.effects:
            player.apply_effect(effect.get('stat'), effect.get('value', 0))
        return self.narrative


# 事件定义 - 关键剧情事件（确定性触发）
STORY_EVENTS = {
    'diane_text_1': GameEvent(
        'diane_text_1', EventType.CONDITION_TRIGGERED,
        '你的手机亮了。是Diane发来的消息..."好久久不见..."',
        [{'stat': 'hope', 'value': 5}, {'stat': 'despair', 'value': -5}],
        conditions={'stat_checks': {'day': ('>=', 3)}},
        npc_id='diane'
    ),
    'mark_appears': GameEvent(
        'mark_appears', EventType.CONDITION_TRIGGERED,
        'Mark出现在你家门口。他笑了，但那笑容让你背脊发凉..."£100，三天。"',
        [{'stat': 'anxiety', 'value': 20}, {'stat': 'despair', 'value': 15}],
        conditions={'stat_checks': {'day': ('==', 5), 'cash': ('<', 50)}}
    ),
    # 父母相关后续事件
    'parents_followup_home': GameEvent(
        'parents_followup_home', EventType.CONDITION_TRIGGERED,
        '几天后，母亲又打来电话..."儿子，回家看看吧。你爸...他其实也很想你。"',
        [{'stat': 'hope', 'value': 10}, {'stat': 'despair', 'value': -5}],
        conditions={'story_flags': {'called_parents_home': True}, 'stat_checks': {'day': ('>=', 7)}}
    ),
    'parents_followup_rejected': GameEvent(
        'parents_followup_rejected', EventType.CONDITION_TRIGGERED,
        '父亲托人带话：你还欠我们一次探视。下次再拒绝，就别回来了。',
        [{'stat': 'anxiety', 'value': 15}, {'stat': 'despair', 'value': 10}],
        conditions={'story_flags': {'asked_parents_for_money': True}, 'stat_checks': {'day': ('>=', 5)}}
    ),
    'parents_followup_mother': GameEvent(
        'parents_followup_mother', EventType.CONDITION_TRIGGERED,
        '母亲发来消息："儿子，最近还好吗？妈妈给你留了你爱吃的..."',
        [{'stat': 'hope', 'value': 8}, {'stat': 'despair', 'value': -8}],
        conditions={'story_flags': {'reconnected_with_mother': True}, 'stat_checks': {'day': ('>=', 4)}}
    ),
    # Diane后续事件
    'diane_regrets': GameEvent(
        'diane_regrets', EventType.CONDITION_TRIGGERED,
        'Diane发来消息："其实...我有时候也会想起我们在一起的时光。"',
        [{'stat': 'hope', 'value': 10}, {'stat': 'anxiety', 'value': 5}],
        conditions={'stat_checks': {'day': ('>=', 8), 'reputation': ('>=', 50)}}
    ),
    # Mark债务后续
    'mark_debt_reminder': GameEvent(
        'mark_debt_reminder', EventType.CONDITION_TRIGGERED,
        'Mark的伙计来提醒："Mark说你还欠着钱。别想跑。"',
        [{'stat': 'anxiety', 'value': 15}, {'stat': 'despair', 'value': 10}],
        conditions={'story_flags': {'owed_mark': True}, 'stat_checks': {'day': ('>=', 4)}}
    ),
    'mark_threat': GameEvent(
        'mark_threat', EventType.CONDITION_TRIGGERED,
        'Mark发来最后通牒："最后期限到了。你知道的，欠债还钱，欠命还命。"',
        [{'stat': 'anxiety', 'value': 25}, {'stat': 'despair', 'value': 20}],
        conditions={'story_flags': {'owed_mark': True}, 'stat_checks': {'day': ('>=', 7)}}
    ),
    # Spud相关
    'spud_asks_money': GameEvent(
        'spud_asks_money', EventType.CONDITION_TRIGGERED,
        'Spud发来消息："嘿，兄弟...之前那£50，我真的很需要。能还吗？"',
        [{'stat': 'anxiety', 'value': 5}],
        conditions={'stat_checks': {'day': ('>=', 5)}}
    ),
    'spud_death': GameEvent(
        'spud_death', EventType.CONDITION_TRIGGERED,
        '你唯一的朋友Spud死了。overdose。你感觉世界上最后一盏灯也灭了...',
        [{'stat': 'despair', 'value': 40}, {'stat': 'sober', 'value': -20}],
        conditions={'stat_checks': {'day': ('>=', 10), 'withdrawal': ('>=', 80)}}
    ),
}

# 事件链定义
EVENT_CHAINS = {
    'mark_debt_arc': {
        'events': ['mark_appears', 'mark_threat'],
    }
}
