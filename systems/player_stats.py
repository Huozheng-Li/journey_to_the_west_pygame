"""
玩家属性系统
管理孙悟空的HP、攻击力等持久化属性
"""


class PlayerStats:
    """
    玩家属性管理
    在main.py中创建单例，传递给各场景
    """

    # 可调节的配置值 - 直接修改这里调整数值
    BASE_HP = 60              # 初始血量
    BASE_ATTACK_POWER = 5     # 初始攻击力
    ELDER_HP_BONUS = 20       # 每次与村民交互增加血量
    TANG_ATTACK_BONUS = 10    # 每次与唐僧交互增加攻击力
    MAX_ELDER_BONUSES = 4     # 最多4个村民可交互
    MAX_TANG_BONUSES = 1      # 1个唐僧可交互

    def __init__(self):
        """初始化属性"""
        self.hp = self.BASE_HP
        self.attack_power = self.BASE_ATTACK_POWER
        self.elder_bonus_count = 0
        self.tang_bonus_count = 0
        self.total_enemies_defeated = 0
        self.last_battle_won = False  # 上次战斗结果

    def add_elder_hp(self):
        """
        与村民交互增加血量
        :return: 是否成功增加
        """
        if self.elder_bonus_count < self.MAX_ELDER_BONUSES:
            self.hp += self.ELDER_HP_BONUS
            self.elder_bonus_count += 1
            return True
        return False

    def add_tang_attack(self):
        """
        与唐僧交互增加攻击力
        :return: 是否成功增加
        """
        if self.tang_bonus_count < self.MAX_TANG_BONUSES:
            self.attack_power += self.TANG_ATTACK_BONUS
            self.tang_bonus_count += 1
            return True
        return False

    def reset(self):
        """重置所有属性"""
        self.hp = self.BASE_HP
        self.attack_power = self.BASE_ATTACK_POWER
        self.elder_bonus_count = 0
        self.tang_bonus_count = 0
        self.total_enemies_defeated = 0
