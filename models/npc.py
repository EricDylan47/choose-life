# -*- coding: utf-8 -*-
"""
NPC relationship system module
"""
from datetime import datetime

# ═══════════════════════════════════════════════════════════════════════════
# NPC关系系统
# ═══════════════════════════════════════════════════════════════════════════
class NPCRelationship:
    """NPC关系数据类"""
    def __init__(self, npc_id):
        self.npc_id = npc_id
        self.affinity = 20       # 好感度 0-100
        self.trust = 10          # 信任度 0-100
        self.state = 'stranger'  # enemy/stranger/acquaintance/friend/close_friend
        self.interaction_count = 0
        self.last_interaction_day = 0
        self.positive_interactions = 0
        self.negative_interactions = 0
        self.has_met = False
        self.special_unlocked = False

    def to_dict(self):
        return {
            'npc_id': self.npc_id,
            'affinity': self.affinity,
            'trust': self.trust,
            'state': self.state,
            'interaction_count': self.interaction_count,
            'last_interaction_day': self.last_interaction_day,
            'positive_interactions': self.positive_interactions,
            'negative_interactions': self.negative_interactions,
            'has_met': self.has_met,
            'special_unlocked': self.special_unlocked,
        }

    @classmethod
    def from_dict(cls, data):
        rel = cls(data.get('npc_id', ''))
        rel.affinity = data.get('affinity', 20)
        rel.trust = data.get('trust', 10)
        rel.state = data.get('state', 'stranger')
        rel.interaction_count = data.get('interaction_count', 0)
        rel.last_interaction_day = data.get('last_interaction_day', 0)
        rel.positive_interactions = data.get('positive_interactions', 0)
        rel.negative_interactions = data.get('negative_interactions', 0)
        rel.has_met = data.get('has_met', False)
        rel.special_unlocked = data.get('special_unlocked', False)
        return rel


# NPC定义
NPC_DEFINITIONS = {
    'renton': {
        'name': 'Renton',
        'role': 'best_friend',
        'description': '你的发小，早已离开这座城市',
        'state_thresholds': {'stranger': 0, 'acquaintance': 15, 'friend': 35, 'close_friend': 60},
        'enemy_threshold': -999,  # 不会主动变敌人
    },
    'mark': {
        'name': 'Mark',
        'role': 'debt_collector',
        'description': '危险的债务人，心狠手辣',
        'state_thresholds': {'stranger': 0, 'acquaintance': 10, 'friend': 40, 'close_friend': 70},
        'enemy_threshold': -20,
    },
    'sick_boy': {
        'name': 'Sick Boy',
        'role': 'dealer',
        'description': '毒贩，总有新货和歪点子',
        'state_thresholds': {'stranger': 0, 'acquaintance': 10, 'friend': 30, 'close_friend': 55},
        'enemy_threshold': -999,
    },
    'begbie': {
        'name': 'Begbie',
        'role': 'criminal',
        'description': '暴力倾向严重，最好别惹他',
        'state_thresholds': {'stranger': 0, 'acquaintance': 5, 'friend': 25, 'close_friend': 50},
        'enemy_threshold': -10,
    },
    'spud': {
        'name': 'Spud',
        'role': 'friend',
        'description': '最忠诚的朋友，但太懦弱',
        'state_thresholds': {'stranger': 0, 'acquaintance': 5, 'friend': 20, 'close_friend': 45},
        'enemy_threshold': -999,
    },
    'diane': {
        'name': 'Diane',
        'role': 'ex_girlfriend',
        'description': '你的前女友，已经有了新生活',
        'state_thresholds': {'stranger': 0, 'acquaintance': 10, 'friend': 30, 'close_friend': 55},
        'enemy_threshold': -15,
    },
}


def update_relationship_state(rel):
    """根据好感度更新NPC关系状态"""
    npc_def = NPC_DEFINITIONS.get(rel.npc_id, {})
    thresholds = npc_def.get('state_thresholds', {})
    enemy_thresh = npc_def.get('enemy_threshold', -20)

    if rel.affinity <= enemy_thresh:
        rel.state = 'enemy'
    elif rel.affinity >= thresholds.get('close_friend', 60):
        rel.state = 'close_friend'
    elif rel.affinity >= thresholds.get('friend', 35):
        rel.state = 'friend'
    elif rel.affinity >= thresholds.get('acquaintance', 15):
        rel.state = 'acquaintance'
    else:
        rel.state = 'stranger'

    # 解锁特殊互动
    if rel.affinity >= thresholds.get('close_friend', 60):
        rel.special_unlocked = True

    return rel
