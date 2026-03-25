# -*- coding: utf-8 -*-
"""
Player model module
"""
from config import STAT_BOUNDS, SAVE_FORMAT_VERSION
from .npc import NPCRelationship, NPC_DEFINITIONS, update_relationship_state


# ═══════════════════════════════════════════════════════════════════════════
# 玩家类 - 重构版
# ═══════════════════════════════════════════════════════════════════════════
class Player:
    """重构后的玩家类"""
    def __init__(self):
        # 财务维度
        self.cash = 50
        self.bank_balance = 0
        self.debt = 0
        self.income_level = 0
        # 身体健康维度
        self.sober = 60
        self.health = 80
        self.withdrawal = 20
        # 精神健康维度
        self.anxiety = 90
        self.despair = 50
        self.hope = 30
        # 社交维度
        self.reputation = 40
        self.social_connections = 2
        self.influence = 10
        # 时间
        self.day = 1
        self.round = 0
        self.hour = 12
        self.rent_due = 6
        # 记录
        self.choices_log = []
        self.history = []
        # NPC关系
        self.relationships = {npc_id: NPCRelationship(npc_id) for npc_id in NPC_DEFINITIONS.keys()}
        # 任务系统（稍后初始化）
        self.quest_manager = None
        # 故事进度
        self.current_chapter = 'chapter_1'
        self.story_flags = {}
        # 触发的事件
        self.triggered_events = set()
        # 活跃效果
        self.active_effects = []

    def apply_effect(self, stat, value):
        """应用属性变化，带边界约束和跨维度影响"""
        if not hasattr(self, stat):
            return

        bounds = STAT_BOUNDS.get(stat, {'min': 0, 'max': 100})
        old_value = getattr(self, stat)
        new_value = old_value + value

        # 钳制到边界
        new_value = max(bounds['min'], min(bounds['max'], new_value))
        setattr(self, stat, new_value)

        # 跨维度影响
        if stat == 'withdrawal':
            if value > 0:  # 戒断加深
                self.sober = max(0, self.sober - int(value * 0.3))
            elif value < 0:  # 戒断减轻
                self.sober = max(0, self.sober + int(value * 0.2))

        elif stat == 'despair':
            if new_value >= 80:
                self.sober = max(0, self.sober - 2)
            if new_value >= 95:
                self.anxiety = min(100, self.anxiety + 10)

        elif stat == 'anxiety':
            if new_value >= 80:
                self.sober = max(0, self.sober - 1)

        elif stat == 'reputation':
            if new_value < 20:
                # 所有人际关系变差
                for rel in self.relationships.values():
                    rel.affinity = max(0, rel.affinity - 5)
                    update_relationship_state(rel)

        elif stat == 'sober':
            if new_value < 20:
                self.anxiety = min(100, self.anxiety + 5)

    def to_dict(self):
        """转换为字典用于存档"""
        return {
            'version': SAVE_FORMAT_VERSION,
            'cash': self.cash,
            'bank_balance': self.bank_balance,
            'debt': self.debt,
            'income_level': self.income_level,
            'sober': self.sober,
            'health': self.health,
            'withdrawal': self.withdrawal,
            'anxiety': self.anxiety,
            'despair': self.despair,
            'hope': self.hope,
            'reputation': self.reputation,
            'social_connections': self.social_connections,
            'influence': self.influence,
            'day': self.day,
            'round': self.round,
            'hour': self.hour,
            'rent_due': self.rent_due,
            'choices_log': self.choices_log,
            'history': self.history,
            'relationships': {npc_id: rel.to_dict() for npc_id, rel in self.relationships.items()},
            'current_chapter': self.current_chapter,
            'story_flags': self.story_flags,
            'triggered_events': list(self.triggered_events),
        }

    @classmethod
    def from_dict(cls, data):
        """从字典恢复"""
        player = cls()
        player.cash = data.get('cash', 50)
        player.bank_balance = data.get('bank_balance', 0)
        player.debt = data.get('debt', 0)
        player.income_level = data.get('income_level', 0)
        player.sober = data.get('sober', 60)
        player.health = data.get('health', 80)
        player.withdrawal = data.get('withdrawal', 20)
        player.anxiety = data.get('anxiety', 90)
        player.despair = data.get('despair', 50)
        player.hope = data.get('hope', 30)
        player.reputation = data.get('reputation', 40)
        player.social_connections = data.get('social_connections', 2)
        player.influence = data.get('influence', 10)
        player.day = data.get('day', 1)
        player.round = data.get('round', 0)
        player.hour = data.get('hour', 12)
        player.rent_due = data.get('rent_due', 6)
        player.choices_log = data.get('choices_log', [])
        player.history = data.get('history', [])
        player.current_chapter = data.get('current_chapter', 'chapter_1')
        player.story_flags = data.get('story_flags', {})
        player.triggered_events = set(data.get('triggered_events', []))

        # 恢复NPC关系
        for npc_id, rel_data in data.get('relationships', {}).items():
            player.relationships[npc_id] = NPCRelationship.from_dict(rel_data)

        return player


# 向后兼容：保留HumanTrash作为Player的别名
HumanTrash = Player
