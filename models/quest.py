# -*- coding: utf-8 -*-
"""
Quest system module
"""
from datetime import datetime


# ═══════════════════════════════════════════════════════════════════════════
# 任务系统
# ═══════════════════════════════════════════════════════════════════════════
class Quest:
    """任务数据类"""
    def __init__(self, quest_id, quest_type, title, description, objectives, rewards, prerequisites=None, time_limit=None):
        self.quest_id = quest_id
        self.quest_type = quest_type  # MAIN / SIDE
        self.title = title
        self.description = description
        self.objectives = objectives  # [{'id': str, 'description': str, 'target': int, 'current': int}]
        self.rewards = rewards
        self.prerequisites = prerequisites or {}
        self.time_limit = time_limit
        self.is_active = False
        self.is_completed = False
        self.is_failed = False
        self.completed_at = None
        self.failed_at = None
        self.activated_at = None

    def to_dict(self):
        return {
            'quest_id': self.quest_id,
            'quest_type': self.quest_type,
            'title': self.title,
            'description': self.description,
            'objectives': self.objectives,
            'rewards': self.rewards,
            'prerequisites': self.prerequisites,
            'time_limit': self.time_limit,
            'is_active': self.is_active,
            'is_completed': self.is_completed,
            'is_failed': self.is_failed,
            'completed_at': self.completed_at,
            'failed_at': self.failed_at,
            'activated_at': self.activated_at,
        }

    @classmethod
    def from_dict(cls, data):
        q = cls(
            data.get('quest_id', ''),
            data.get('quest_type', 'SIDE'),
            data.get('title', ''),
            data.get('description', ''),
            data.get('objectives', []),
            data.get('rewards', {}),
            data.get('prerequisites', {}),
            data.get('time_limit', None)
        )
        q.is_active = data.get('is_active', False)
        q.is_completed = data.get('is_completed', False)
        q.is_failed = data.get('is_failed', False)
        q.completed_at = data.get('completed_at', None)
        q.failed_at = data.get('failed_at', None)
        q.activated_at = data.get('activated_at', None)
        return q

    def check_completion(self):
        """检查任务是否完成"""
        if self.is_completed or self.is_failed:
            return
        for obj in self.objectives:
            if obj.get('current', 0) < obj.get('target', 1):
                return False
        self.is_completed = True
        self.completed_at = datetime.now().isoformat()
        return True

    def check_failure(self, current_day):
        """检查任务是否失败"""
        if self.is_completed or self.is_failed:
            return False
        if self.time_limit and self.activated_at:
            if current_day - self.activated_at > self.time_limit:
                self.is_failed = True
                self.failed_at = datetime.now().isoformat()
                return True
        return False


class QuestManager:
    """任务管理器"""
    def __init__(self, player):
        self.player = player
        self.all_quests = {}
        self.active_quests = []
        self.completed_quests = []
        self.failed_quests = []
        self._init_quests()

    def _init_quests(self):
        """初始化所有任务"""
        # 主线任务
        self.all_quests['main_ch1_1'] = Quest(
            'main_ch1_1', 'MAIN',
            '生存的本能',
            '你已经三天没吃东西了。必须找到钱或者食物。',
            [
                {'id': 'obj_1', 'description': '获得£20或更多现金', 'target': 20, 'current': 0, 'type': 'stat', 'stat': 'cash', 'operator': '>=', 'check_type': 'gain'},
                {'id': 'obj_2', 'description': '保持清醒度高于20', 'target': 20, 'current': 0, 'type': 'stat', 'stat': 'sober', 'operator': '>', 'check_type': 'maintain'},
            ],
            {'cash': 20, 'sober': 10, 'reputation': 5},
            {'min_day': 1, 'max_day': 3}
        )

        self.all_quests['main_ch1_2'] = Quest(
            'main_ch1_2', 'MAIN',
            '联系旧友',
            'Renton走了。但也许Mark能帮上忙...',
            [
                {'id': 'obj_1', 'description': '联系Mark', 'target': 1, 'current': 0, 'type': 'npc_interaction', 'npc': 'mark'},
                {'id': 'obj_2', 'description': '联系Renton', 'target': 1, 'current': 0, 'type': 'npc_interaction', 'npc': 'renton'},
            ],
            {'cash': 30},
            {'required_quests': ['main_ch1_1']}
        )

        self.all_quests['main_ch2_1'] = Quest(
            'main_ch2_1', 'MAIN',
            'Mark的威胁',
            'Mark说三天内要还£100。否则...',
            [
                {'id': 'obj_1', 'description': '还清Mark的债务£100', 'target': 100, 'current': 0, 'type': 'stat', 'stat': 'cash', 'operator': '>=', 'check_type': 'pay'},
            ],
            {'reputation': 20, 'mark_trust': 15},
            {'required_quests': ['main_ch1_2']},
            time_limit=18
        )

        # 支线任务
        self.all_quests['side_spud_1'] = Quest(
            'side_spud_1', 'SIDE',
            'Spud的鞋子',
            'Spud借了你£50买药，现在他想要回...',
            [
                {'id': 'obj_1', 'description': '找到£50还给Spud', 'target': 50, 'current': 0, 'type': 'stat', 'stat': 'cash', 'operator': '>=', 'check_type': 'gain'},
            ],
            {'spud_affinity': 25, 'spud_trust': 20},
        )

        self.all_quests['side_diane_1'] = Quest(
            'side_diane_1', 'SIDE',
            'Diane的消息',
            'Diane发来消息：好久不见，想聊聊吗？',
            [
                {'id': 'obj_1', 'description': '回复Diane的消息', 'target': 1, 'current': 0, 'type': 'choice', 'choice_id': 'diane_reconnect'},
            ],
            {'diane_affinity': 10, 'hope': 5},
            {'required_quests': ['main_ch1_2']}
        )

        self.all_quests['side_community_1'] = Quest(
            'side_community_1', 'SIDE',
            '戒毒互助会',
            '也许该试试正经的帮助',
            [
                {'id': 'obj_1', 'description': '参加互助会3次', 'target': 3, 'current': 0, 'type': 'action_count', 'action_id': 'support_group'},
            ],
            {'withdrawal': -30, 'sober': 20, 'hope': 15},
        )

    def check_prerequisites(self, quest_id):
        """检查任务前置条件"""
        quest = self.all_quests.get(quest_id)
        if not quest:
            return False

        prereqs = quest.prerequisites

        # 检查天数范围
        min_day = prereqs.get('min_day', 1)
        max_day = prereqs.get('max_day', 999)
        if not (min_day <= self.player.day <= max_day):
            return False

        # 检查必需完成的任务
        required_quests = prereqs.get('required_quests', [])
        for req_quest_id in required_quests:
            if req_quest_id not in self.completed_quests:
                return False

        # 检查NPC关系
        npc_reqs = prereqs.get('npc_relationships', {})
        for npc_id, (req_state, min_affinity) in npc_reqs.items():
            rel = self.player.relationships.get(npc_id)
            if not rel or rel.state not in req_state or rel.affinity < min_affinity:
                return False

        return True

    def activate_quest(self, quest_id):
        """激活任务"""
        quest = self.all_quests.get(quest_id)
        if not quest or quest.is_active or quest.is_completed or quest.is_failed:
            return False

        if not self.check_prerequisites(quest_id):
            return False

        quest.is_active = True
        quest.activated_at = self.player.day
        if quest_id not in self.active_quests:
            self.active_quests.append(quest_id)
        return True

    def update_quest_progress(self, stat=None, value=None, action_id=None, npc_id=None, choice_id=None):
        """更新任务进度"""
        for quest_id in self.active_quests:
            quest = self.all_quests.get(quest_id)
            if not quest or not quest.is_active:
                continue

            for obj in quest.objectives:
                obj_type = obj.get('type')

                if obj_type == 'stat' and stat:
                    # 检查是否满足条件
                    target = obj.get('target', 0)
                    current = obj.get('current', 0)
                    check_type = obj.get('check_type', 'gain')

                    if obj.get('stat') == stat:
                        if check_type == 'gain' and value > 0:
                            obj['current'] = current + value
                        elif check_type == 'maintain':
                            # 获取当前属性值，检查是否满足维持条件
                            current_stat_value = getattr(self.player, stat, 0)
                            if current_stat_value >= target:
                                obj['current'] = target  # 维持住了
                        elif check_type == 'pay' and value > 0:
                            obj['current'] = current + value

                elif obj_type == 'npc_interaction' and npc_id:
                    if obj.get('npc') == npc_id:
                        obj['current'] = obj.get('current', 0) + 1

                elif obj_type == 'action_count' and action_id:
                    if obj.get('action_id') == action_id:
                        obj['current'] = obj.get('current', 0) + 1

                elif obj_type == 'choice' and choice_id:
                    if obj.get('choice_id') == choice_id:
                        obj['current'] = obj.get('current', 0) + 1

                # 检查是否完成
                if quest.check_completion():
                    self.active_quests.remove(quest_id)
                    self.completed_quests.append(quest_id)
                    self.apply_rewards(quest)

    def apply_rewards(self, quest):
        """应用任务奖励"""
        from .npc import update_relationship_state
        rewards = quest.rewards
        for stat, value in rewards.items():
            if stat.endswith('_affinity') or stat.endswith('_trust'):
                # NPC关系奖励
                npc_id = stat.replace('_affinity', '').replace('_trust', '')
                rel = self.player.relationships.get(npc_id)
                if rel:
                    if '_affinity' in stat:
                        rel.affinity = max(0, min(100, rel.affinity + value))
                    elif '_trust' in stat:
                        rel.trust = max(0, min(100, rel.trust + value))
                    update_relationship_state(rel)
            else:
                # 属性奖励
                self.player.apply_effect(stat, value)

    def check_failures(self):
        """检查任务失败"""
        for quest_id in list(self.active_quests):
            quest = self.all_quests.get(quest_id)
            if quest and quest.check_failure(self.player.day):
                if quest_id in self.active_quests:
                    self.active_quests.remove(quest_id)
                self.failed_quests.append(quest_id)

    def check_new_quests(self):
        """检查可以激活的新任务"""
        newly_activated = []
        for quest_id, quest in self.all_quests.items():
            if quest_id not in self.active_quests and not quest.is_active and not quest.is_completed and not quest.is_failed:
                if self.check_prerequisites(quest_id):
                    if self.activate_quest(quest_id):
                        newly_activated.append(quest_id)
        return newly_activated

    def to_dict(self):
        return {
            'active_quests': self.active_quests,
            'completed_quests': self.completed_quests,
            'failed_quests': self.failed_quests,
            'quest_data': {qid: q.to_dict() for qid, q in self.all_quests.items()}
        }

    @classmethod
    def from_dict(cls, data, player):
        qm = cls(player)
        qm.active_quests = data.get('active_quests', [])
        qm.completed_quests = data.get('completed_quests', [])
        qm.failed_quests = data.get('failed_quests', [])
        # 重建任务对象
        for qid, qdata in data.get('quest_data', {}).items():
            if qid in qm.all_quests:
                qm.all_quests[qid] = Quest.from_dict(qdata)
        return qm
