# 《西游记观音院》类设计文档

## 1. 类继承体系

```
pygame.sprite.Sprite
    │
    └── ActorBase (角色基类)
            │
            ├── Player (孙悟空-探索版)
            │
            ├── BattlePlayer (孙悟空-战斗版)
            │
            ├── NPCBase (NPC基类)
            │       │
            │       ├── Elder (村民)
            │       │
            │       └── God (土地公)
            │
            └── EnemyBase (怪物基类)
                    │
                    └── Cattle (牛怪)

SceneBase (场景基类)
    │
    ├── VillageScene (村庄场景)
    │
    ├── TempleScene (寺庙场景)
    │
    ├── BattleScene (战斗场景)
    │
    └── EndScene (结束场景)

TiledScene (TMX场景封装)

Action (动画行为类)

Camera (相机系统)

CollisionSystem (碰撞系统)

DialogSystem (对话系统)

BattleSystem (战斗系统)

FadeScene (渐变效果)

SceneManager (场景管理器)

Game (游戏主类)
```

---

## 2. 核心类详细设计

### 2.1 Action - 动画行为类

```python
class Action:
    """
    角色动画行为类
    管理帧动画的加载、播放、切换
    """

    # 成员变量
    image_index: int          # 当前帧索引
    action_images: list       # 帧图像列表 [pygame.Surface, ...]
    image_count: int          # 总帧数
    is_loop: bool             # 是否循环播放

    # 构造函数
    def __init__(self, path: str, prefix: str, image_count: int, is_loop: bool = True):
        """
        初始化动画行为
        :param path: 图片目录路径 (如 'elder', 'cattle/fight')
        :param prefix: 文件名前缀 (如 'elder1-0000')
        :param image_count: 帧数量
        :param is_loop: 是否循环播放
        """

    # 成员函数
    def get_current_image(self) -> pygame.Surface:
        """
        获取当前帧图像
        :return: 当前帧的Surface
        自动推进帧索引
        """

    def is_end(self) -> bool:
        """
        检查动画是否播放完毕
        :return: 是否结束
        循环动画始终返回False
        """

    def reset(self):
        """
        重置动画到第一帧
        用于切换方向或重新播放
        """

    def set_image_count(self, count: int):
        """
        设置帧数量
        :param count: 新的帧数
        """
```

---

### 2.2 ActorBase - 角色基类

```python
class ActorBase(pygame.sprite.Sprite):
    """
    所有角色的基类
    继承自pygame.sprite.Sprite
    """

    # 类常量 (方向)
    DOWN: int = 0
    LEFT: int = 1
    UP: int = 2
    RIGHT: int = 3

    # 成员变量
    pos_x: float              # x坐标
    pos_y: float              # y坐标
    width: int                # 角色宽度
    height: int               # 角色高度
    speed: int                # 移动速度
    direction: int            # 当前方向
    image: pygame.Surface     # 当前显示图像
    rect: pygame.Rect         # 碰撞矩形

    # 构造函数
    def __init__(self, x: float, y: float, width: int, height: int, speed: int = 4):
        """
        初始化角色
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 角色宽度
        :param height: 角色高度
        :param speed: 移动速度
        """

    # 成员函数
    def update_rect(self):
        """
        更新碰撞矩形位置
        根据pos_x, pos_y更新rect
        """

    def draw(self, surface: pygame.Surface):
        """
        绘制角色到surface
        :param surface: 目标surface
        """

    def get_position(self) -> tuple:
        """
        获取角色位置
        :return: (x, y) 元组
        """

    def set_position(self, x: float, y: float):
        """
        设置角色位置
        :param x: x坐标
        :param y: y坐标
        """

    def get_rect(self) -> pygame.Rect:
        """
        获取碰撞矩形
        :return: pygame.Rect
        """
```

---

### 2.3 Player - 孙悟空（探索版）

```python
class Player(ActorBase):
    """
    孙悟空 - 探索模式
    支持4方向移动和动画
    """

    # 成员变量
    animations: dict          # {方向: Action} 动画字典
    is_moving: bool           # 是否正在移动
    is_talking: bool          # 是否正在对话

    # 构造函数
    def __init__(self, x: float, y: float):
        """
        初始化孙悟空
        :param x: 初始x坐标
        :param y: 初始y坐标
        使用swk2素材 (128帧, 4方向x32帧)
        """

    # 成员函数
    def handle_input(self, keys):
        """
        处理键盘输入
        :param keys: pygame.key.get_pressed() 返回的按键状态
        根据方向键设置移动方向和速度
        """

    def update(self):
        """
        更新玩家状态
        根据is_moving更新动画帧
        更新碰撞矩形
        """

    def move_up(self):
        """向上移动"""

    def move_down(self):
        """向下移动"""

    def move_left(self):
        """向左移动"""

    def move_right(self):
        """向右移动"""

    def stop(self):
        """停止移动"""

    def start_talk(self):
        """开始对话"""

    def end_talk(self):
        """结束对话"""
```

---

### 2.4 BattlePlayer - 孙悟空（战斗版）

```python
class BattlePlayer(ActorBase):
    """
    孙悟空 - 战斗模式
    支持攻击、防御、受伤等状态
    """

    # 成员变量
    animations: dict          # {状态: Action} 动画字典
    hp: int                   # 当前血量
    max_hp: int               # 最大血量
    attack_power: int         # 攻击力
    defense: int              # 防御力
    state: str                # 当前状态 (idle, attack, defense, hurt)

    # 构造函数
    def __init__(self, x: float, y: float):
        """
        初始化战斗版孙悟空
        :param x: 初始x坐标
        :param y: 初始y坐标
        使用swk素材 (16帧)
        """

    # 成员函数
    def update(self):
        """
        更新战斗状态
        根据state更新动画
        """

    def attack(self) -> int:
        """
        执行攻击
        :return: 伤害值
        播放攻击动画，返回攻击伤害
        """

    def defend(self):
        """
        执行防御
        播放防御动画
        """

    def take_damage(self, damage: int):
        """
        受到伤害
        :param damage: 伤害值
        扣除血量，播放受伤动画
        """

    def is_alive(self) -> bool:
        """
        检查是否存活
        :return: 血量>0返回True
        """

    def reset(self):
        """
        重置战斗状态
        恢复血量和状态
        """
```

---

### 2.5 NPCBase - NPC基类

```python
class NPCBase(ActorBase):
    """
    NPC基类
    继承自ActorBase，增加NPC特有功能
    """

    # 成员变量
    name: str                 # NPC名称
    dialogs: list             # 对话内容列表
    is_talking: bool          # 是否正在对话

    # 构造函数
    def __init__(self, name: str, x: float, y: float, width: int, height: int):
        """
        初始化NPC
        :param name: NPC名称
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 宽度
        :param height: 高度
        """

    # 成员函数
    def set_dialogs(self, dialogs: list):
        """
        设置对话内容
        :param dialogs: 对话列表 [{"speaker": str, "text": str}, ...]
        """

    def get_dialogs(self) -> list:
        """
        获取对话内容
        :return: 对话列表
        """

    def on_interact(self) -> list:
        """
        被交互时触发
        :return: 对话内容
        设置is_talking=True，返回对话列表
        """

    def end_interact(self):
        """
        结束交互
        设置is_talking=False
        """

    def update(self):
        """
        更新NPC状态
        子类重写此方法
        """
```

---

### 2.6 Elder - 村民类

```python
class Elder(NPCBase):
    """
    村民NPC
    继承自NPCBase
    """

    # 成员变量
    elder_id: int             # 村民编号 (1-4)
    animation: Action         # 动画 (单一方向)

    # 构造函数
    def __init__(self, elder_id: int, x: float, y: float):
        """
        初始化村民
        :param elder_id: 村民编号 (1-4)
        :param x: 初始x坐标
        :param y: 初始y坐标
        根据elder_id加载对应的帧数
        elder1: 10帧, elder2: 6帧, elder3: 7帧, elder4: 10帧
        """

    # 成员函数
    def get_frame_count(self, elder_id: int) -> int:
        """
        获取各村民的帧数
        :param elder_id: 村民编号
        :return: 帧数
        """

    def update(self):
        """
        更新村民状态
        播放动画
        更新碰撞矩形
        """
```

---

### 2.7 God - 土地公类

```python
class God(NPCBase):
    """
    土地公 - 有方向的NPC
    继承自NPCBase，支持4方向移动
    """

    # 成员变量
    animations: dict          # {方向: Action} 动画字典
    auto_move_timer: int      # 自主移动计时器

    # 构造函数
    def __init__(self, x: float, y: float):
        """
        初始化土地公
        :param x: 初始x坐标
        :param y: 初始y坐标
        使用god素材 (4方向x10帧)
        设置默认对话内容
        """

    # 成员函数
    def auto_move(self):
        """
        自主随机移动
        随机改变方向并移动
        """

    def update(self):
        """
        更新土地公状态
        执行自主移动
        更新动画
        更新碰撞矩形
        """

    def set_default_dialogs(self):
        """
        设置默认对话内容
        关于袈裟和观音院的线索
        """
```

---

### 2.8 EnemyBase - 怪物基类

```python
class EnemyBase(ActorBase):
    """
    怪物基类
    继承自ActorBase，增加怪物特有功能
    """

    # 成员变量
    name: str                 # 怪物名称
    hp: int                   # 当前血量
    max_hp: int               # 最大血量
    attack_power: int         # 攻击力
    defense: int              # 防御力
    is_alive: bool            # 是否存活
    state: str                # 当前状态
    animations: dict          # {状态: Action} 动画字典

    # 构造函数
    def __init__(self, name: str, x: float, y: float, width: int, height: int,
                 hp: int, attack_power: int, defense: int = 0):
        """
        初始化怪物
        :param name: 怪物名称
        :param x: 初始x坐标
        :param y: 初始y坐标
        :param width: 宽度
        :param height: 高度
        :param hp: 血量
        :param attack_power: 攻击力
        :param defense: 防御力
        """

    # 成员函数
    def take_damage(self, damage: int):
        """
        受到伤害
        :param damage: 伤害值
        扣除血量，检查是否死亡
        """

    def attack(self) -> int:
        """
        执行攻击
        :return: 伤害值
        播放攻击动画，返回攻击伤害
        """

    def is_alive_check(self) -> bool:
        """
        检查是否存活
        :return: 血量>0返回True
        """

    def update(self):
        """
        更新怪物状态
        根据state更新动画
        子类重写此方法
        """
```

---

### 2.9 Cattle - 牛怪类

```python
class Cattle(EnemyBase):
    """
    牛怪
    继承自EnemyBase
    """

    # 构造函数
    def __init__(self, x: float, y: float):
        """
        初始化牛怪
        :param x: 初始x坐标
        :param y: 初始y坐标
        使用cattle素材 (7种动画状态)
        """

    # 成员函数
    def update(self):
        """
        更新牛怪状态
        根据state播放对应动画
        """

    def set_state(self, state: str):
        """
        设置动画状态
        :param state: 状态名称 (station, walk1, walk2, fight, die, back, look, run)
        """
```

---

### 2.10 TiledScene - TMX场景封装

```python
class TiledScene:
    """
    TMX地图场景封装类
    负责加载和渲染TMX地图
    """

    # 成员变量
    tiled_path: str           # TMX文件路径
    tiled: TiledRenderer      # 地图渲染器
    surface: pygame.Surface   # 地图surface

    # 构造函数
    def __init__(self, path: str):
        """
        初始化TMX场景
        :param path: TMX文件路径
        加载地图并渲染到surface
        """

    # 成员函数
    def get_surface(self) -> pygame.Surface:
        """
        获取地图surface
        :return: 地图surface
        """

    def get_tiled(self) -> TiledRenderer:
        """
        获取地图渲染器
        :return: TiledRenderer对象
        """

    def get_objects_by_name(self, name: str) -> list:
        """
        根据名称获取TMX对象
        :param name: 对象名称
        :return: 对象列表
        """
```

---

### 2.11 SceneBase - 场景基类

```python
class SceneBase:
    """
    场景基类
    所有场景的父类
    """

    # 成员变量
    screen: pygame.Surface    # 游戏窗口
    tiled_scene: TiledScene   # TMX场景
    actors: list              # 角色列表
    camera: Camera            # 相机系统
    collision_system: CollisionSystem  # 碰撞系统
    dialog_system: DialogSystem        # 对话系统
    is_running: bool          # 场景是否运行中

    # 构造函数
    def __init__(self, screen: pygame.Surface, tmx_path: str):
        """
        初始化场景
        :param screen: 游戏窗口surface
        :param tmx_path: TMX地图路径
        """

    # 成员函数
    def load_actors_from_tmx(self):
        """
        从TMX对象层加载角色
        读取actor、elder、god等对象层
        """

    def handle_events(self, events: list):
        """
        处理事件
        :param events: 事件列表
        子类重写此方法
        """

    def update(self):
        """
        更新场景状态
        更新所有角色
        更新相机
        子类重写此方法
        """

    def draw(self):
        """
        绘制场景
        绘制地图
        绘制所有角色
        子类重写此方法
        """

    def run(self) -> bool:
        """
        运行场景
        :return: 是否退出
        主循环：处理事件→更新→绘制
        """
```

---

### 2.12 VillageScene - 村庄场景

```python
class VillageScene(SceneBase):
    """
    村庄场景
    继承自SceneBase
    """

    # 成员变量
    player: Player            # 玩家对象
    god: God                  # 土地公对象
    elders: list              # 村民列表

    # 构造函数
    def __init__(self, screen: pygame.Surface):
        """
        初始化村庄场景
        :param screen: 游戏窗口surface
        加载village1.tmx地图
        """

    # 成员函数
    def load_actors_from_tmx(self):
        """
        从TMX加载角色
        加载玩家、土地公、村民
        """

    def handle_events(self, events: list):
        """
        处理事件
        处理键盘输入
        处理NPC交互
        """

    def update(self):
        """
        更新村庄状态
        更新玩家移动
        更新NPC动画
        检测碰撞
        """

    def draw(self):
        """
        绘制村庄场景
        绘制地图
        绘制角色
        绘制对话框
        """

    def check_npc_collision(self):
        """
        检测NPC碰撞
        检测玩家与土地公碰撞
        触发对话
        """

    def on_god_talk_end(self):
        """
        土地公对话结束
        触发场景切换到寺庙
        """
```

---

### 2.13 TempleScene - 寺庙场景

```python
class TempleScene(SceneBase):
    """
    寺庙场景
    继承自SceneBase
    """

    # 成员变量
    player: Player            # 玩家对象
    enemies: list             # 怪物列表

    # 构造函数
    def __init__(self, screen: pygame.Surface, player: Player):
        """
        初始化寺庙场景
        :param screen: 游戏窗口surface
        :param player: 从村庄传递过来的玩家对象
        加载temple.tmx地图
        """

    # 成员函数
    def load_actors_from_tmx(self):
        """
        从TMX加载角色
        加载玩家、怪物
        """

    def handle_events(self, events: list):
        """
        处理事件
        """

    def update(self):
        """
        更新寺庙状态
        """

    def draw(self):
        """
        绘制寺庙场景
        """

    def check_enemy_collision(self):
        """
        检测怪物碰撞
        触发战斗
        """

    def on_battle_trigger(self):
        """
        战斗触发
        切换到战斗场景
        """
```

---

### 2.14 BattleScene - 战斗场景

```python
class BattleScene(SceneBase):
    """
    战斗场景
    继承自SceneBase
    """

    # 成员变量
    battle_player: BattlePlayer  # 战斗版玩家
    enemy: EnemyBase             # 敌人
    battle_system: BattleSystem  # 战斗系统
    state: str                   # 战斗状态 (READY, FIGHTING, WIN, LOSE)

    # 构造函数
    def __init__(self, screen: pygame.Surface, player: Player, enemy: EnemyBase):
        """
        初始化战斗场景
        :param screen: 游戏窗口surface
        :param player: 探索版玩家 (用于传递属性)
        :param enemy: 敌人对象
        """

    # 成员函数
    def handle_events(self, events: list):
        """
        处理事件
        处理战斗操作 (攻击、防御等)
        """

    def update(self):
        """
        更新战斗状态
        更新玩家和敌人
        检查胜负
        """

    def draw(self):
        """
        绘制战斗场景
        绘制背景
        绘制玩家和敌人
        绘制血条
        """

    def on_player_attack(self):
        """
        玩家攻击
        扣除敌人血量
        检查敌人是否死亡
        """

    def on_enemy_attack(self):
        """
        敌人攻击
        扣除玩家血量
        检查玩家是否死亡
        """

    def check_battle_end(self):
        """
        检查战斗结束
        切换到胜利或失败场景
        """
```

---

### 2.15 EndScene - 结束场景

```python
class EndScene(SceneBase):
    """
    结束场景
    继承自SceneBase
    """

    # 成员变量
    is_win: bool              # 是否胜利
    background: pygame.Surface  # 背景图片

    # 构造函数
    def __init__(self, screen: pygame.Surface, is_win: bool):
        """
        初始化结束场景
        :param screen: 游戏窗口surface
        :param is_win: 是否胜利
        加载胜利或失败背景
        """

    # 成员函数
    def handle_events(self, events: list):
        """
        处理事件
        按键重新开始或退出
        """

    def update(self):
        """
        更新结束场景
        """

    def draw(self):
        """
        绘制结束场景
        绘制背景和文字
        """
```

---

### 2.16 Camera - 相机系统

```python
class Camera:
    """
    相机系统
    负责视角跟随和边界控制
    """

    # 成员变量
    offset_x: int             # x偏移量
    offset_y: int             # y偏移量
    map_width: int            # 地图宽度
    map_height: int           # 地图高度
    screen_width: int         # 窗口宽度
    screen_height: int        # 窗口高度

    # 构造函数
    def __init__(self, map_width: int, map_height: int, screen_width: int, screen_height: int):
        """
        初始化相机
        :param map_width: 地图宽度
        :param map_height: 地图高度
        :param screen_width: 窗口宽度
        :param screen_height: 窗口高度
        """

    # 成员函数
    def update(self, target_x: float, target_y: float):
        """
        更新相机位置
        :param target_x: 目标x坐标 (玩家位置)
        :param target_y: 目标y坐标 (玩家位置)
        计算偏移量，限制在地图范围内
        """

    def apply(self, x: float, y: float) -> tuple:
        """
        应用相机偏移
        :param x: 世界x坐标
        :param y: 世界y坐标
        :return: 屏幕坐标 (screen_x, screen_y)
        """

    def apply_rect(self, rect: pygame.Rect) -> pygame.Rect:
        """
        应用相机偏移到矩形
        :param rect: 世界坐标矩形
        :return: 屏幕坐标矩形
        """

    def reset(self):
        """
        重置相机偏移
        """
```

---

### 2.17 CollisionSystem - 碰撞系统

```python
class CollisionSystem:
    """
    碰撞检测系统
    负责检测各种碰撞
    """

    # 成员变量
    obstacles: list           # 障碍物列表 [pygame.Rect, ...]

    # 构造函数
    def __init__(self, tmx_data):
        """
        初始化碰撞系统
        :param tmx_data: TMX地图数据
        从obstacle层加载障碍物
        """

    # 成员函数
    def load_obstacles(self, tmx_data) -> list:
        """
        从TMX加载障碍物
        :param tmx_data: TMX地图数据
        :return: 障碍物矩形列表
        """

    def check_obstacle_collision(self, rect: pygame.Rect) -> bool:
        """
        检查矩形是否与障碍物碰撞
        :param rect: 待检测矩形
        :return: 是否碰撞
        """

    def check_sprite_collision(self, sprite1: pygame.sprite.Sprite, 
                               sprite2: pygame.sprite.Sprite) -> bool:
        """
        检查两个精灵碰撞
        :param sprite1: 精灵1
        :param sprite2: 精灵2
        :return: 是否碰撞
        使用pygame.sprite.collide_rect
        """

    def check_sprite_group_collision(self, sprite: pygame.sprite.Sprite, 
                                     group: pygame.sprite.Group) -> list:
        """
        检查精灵与组碰撞
        :param sprite: 精灵
        :param group: 精灵组
        :return: 碰撞的精灵列表
        使用pygame.sprite.spritecollide
        """

    def check_mask_collision(self, sprite1: pygame.sprite.Sprite,
                             sprite2: pygame.sprite.Sprite) -> bool:
        """
        检查遮罩碰撞
        :param sprite1: 精灵1
        :param sprite2: 精灵2
        :return: 是否碰撞
        使用pygame.sprite.collide_mask
        """
```

---

### 2.18 DialogSystem - 对话系统

```python
class DialogSystem:
    """
    对话系统
    负责对话框的显示和文字渲染
    """

    # 成员变量
    font: pygame.font.Font    # 字体对象
    is_active: bool           # 对话是否激活
    current_dialogs: list     # 当前对话列表
    current_index: int        # 当前对话索引
    dialog_box: pygame.Surface  # 对话框surface
    text_color: tuple         # 文字颜色
    bg_color: tuple           # 背景颜色

    # 构造函数
    def __init__(self, font_path: str, font_size: int = 24):
        """
        初始化对话系统
        :param font_path: 字体文件路径
        :param font_size: 字体大小
        """

    # 成员函数
    def start_dialog(self, dialogs: list):
        """
        开始对话
        :param dialogs: 对话列表 [{"speaker": str, "text": str}, ...]
        """

    def next_dialog(self):
        """
        下一条对话
        索引+1，检查是否结束
        """

    def end_dialog(self):
        """
        结束对话
        重置状态
        """

    def is_dialog_active(self) -> bool:
        """
        检查对话是否激活
        :return: 是否激活
        """

    def get_current_dialog(self) -> dict:
        """
        获取当前对话
        :return: {"speaker": str, "text": str}
        """

    def handle_input(self, event: pygame.event.Event):
        """
        处理输入事件
        :param event: pygame事件
        空格/回车：下一条对话
        ESC：结束对话
        """

    def draw(self, surface: pygame.Surface):
        """
        绘制对话框
        :param surface: 目标surface
        绘制半透明对话框
        绘制说话者名字
        绘制对话文字
        """
```

---

### 2.19 BattleSystem - 战斗系统

```python
class BattleSystem:
    """
    战斗系统
    负责战斗逻辑和状态管理
    """

    # 成员变量
    state: str                # 战斗状态 (READY, FIGHTING, WIN, LOSE)
    turn: str                 # 当前回合 (PLAYER, ENEMY)
    player: BattlePlayer      # 玩家对象
    enemy: EnemyBase          # 敌人对象

    # 构造函数
    def __init__(self, player: BattlePlayer, enemy: EnemyBase):
        """
        初始化战斗系统
        :param player: 战斗版玩家
        :param enemy: 敌人
        """

    # 成员函数
    def start_battle(self):
        """
        开始战斗
        设置状态为FIGHTING
        """

    def player_attack(self):
        """
        玩家攻击
        计算伤害
        扣除敌人血量
        检查敌人是否死亡
        """

    def enemy_attack(self):
        """
        敌人攻击
        计算伤害
        扣除玩家血量
        检查玩家是否死亡
        """

    def calculate_damage(self, attacker_power: int, defender_defense: int) -> int:
        """
        计算伤害
        :param attacker_power: 攻击力
        :param defender_defense: 防御力
        :return: 伤害值
        """

    def check_battle_end(self) -> str:
        """
        检查战斗结束
        :return: 'WIN', 'LOSE', 'CONTINUE'
        """

    def get_state(self) -> str:
        """
        获取战斗状态
        :return: 当前状态
        """

    def reset(self):
        """
        重置战斗系统
        """
```

---

### 2.20 FadeScene - 渐变效果

```python
class SceneStatus(enum.IntEnum):
    """场景状态枚举"""
    In = 1      # 渐入
    Normal = 2  # 正常显示
    Out = 3     # 渐出
    Over = 4    # 结束


class FadeScene:
    """
    场景渐变效果类
    实现alpha通道渐变
    """

    # 成员变量
    back_image: pygame.Surface  # 背景图片
    alpha: int                  # 当前alpha值
    status: SceneStatus         # 当前状态
    screen_width: int           # 窗口宽度
    screen_height: int          # 窗口高度
    step: int                   # alpha变化步长

    # 构造函数
    def __init__(self, back_image: pygame.Surface, screen_width: int = 800, screen_height: int = 600):
        """
        初始化渐变效果
        :param back_image: 背景图片
        :param screen_width: 窗口宽度
        :param screen_height: 窗口高度
        """

    # 成员函数
    def set_status(self, status: SceneStatus):
        """
        设置状态
        :param status: 新状态
        根据状态重置alpha值
        """

    def get_out(self) -> bool:
        """
        检查渐出是否完成
        :return: 是否完成
        """

    def get_back_image(self, x: int, y: int) -> pygame.Surface:
        """
        获取带alpha的背景图片
        :param x: x偏移
        :param y: y偏移
        :return: 处理后的surface
        根据状态应用alpha渐变
        """

    def update(self):
        """
        更新渐变状态
        根据状态更新alpha值
        """
```

---

### 2.21 SceneManager - 场景管理器

```python
class SceneManager:
    """
    场景管理器
    负责场景切换和管理
    """

    # 成员变量
    scenes: dict              # {名称: 场景对象}
    current_scene: SceneBase  # 当前场景
    current_name: str         # 当前场景名称
    fade_scene: FadeScene     # 渐变效果
    is_transitioning: bool    # 是否正在切换

    # 构造函数
    def __init__(self, screen: pygame.Surface):
        """
        初始化场景管理器
        :param screen: 游戏窗口surface
        """

    # 成员函数
    def add_scene(self, name: str, scene: SceneBase):
        """
        添加场景
        :param name: 场景名称
        :param scene: 场景对象
        """

    def switch_scene(self, name: str):
        """
        切换场景
        :param name: 目标场景名称
        开始渐变效果
        """

    def update(self):
        """
        更新场景
        更新当前场景
        更新渐变效果
        """

    def draw(self):
        """
        绘制场景
        绘制当前场景
        绘制渐变效果
        """

    def run(self):
        """
        运行场景管理器
        主循环
        """
```

---

### 2.22 Game - 游戏主类

```python
class Game:
    """
    游戏主类
    负责初始化和主循环
    """

    # 成员变量
    screen: pygame.Surface    # 游戏窗口
    clock: pygame.time.Clock  # 时钟
    scene_manager: SceneManager  # 场景管理器
    is_running: bool          # 游戏是否运行中

    # 构造函数
    def __init__(self):
        """
        初始化游戏
        初始化pygame
        创建窗口
        初始化场景管理器
        加载各场景
        """

    # 成员函数
    def init_pygame(self):
        """
        初始化pygame
        初始化display、mixer等模块
        """

    def create_window(self, width: int, height: int):
        """
        创建游戏窗口
        :param width: 窗口宽度
        :param height: 窗口高度
        """

    def init_scenes(self):
        """
        初始化场景
        创建村庄、寺庙、战斗、结束场景
        添加到场景管理器
        """

    def run(self):
        """
        运行游戏
        主循环：处理事件→更新→绘制
        """

    def handle_events(self):
        """
        处理事件
        处理pygame事件
        处理QUIT事件
        """

    def update(self):
        """
        更新游戏状态
        更新场景管理器
        """

    def draw(self):
        """
        绘制游戏画面
        清除屏幕
        绘制场景管理器
        更新显示
        """

    def quit(self):
        """
        退出游戏
        退出pygame
        退出程序
        """
```

---

## 3. 类关系图

### 3.1 继承关系
```
pygame.sprite.Sprite
    └── ActorBase
            ├── Player
            ├── BattlePlayer
            ├── NPCBase
            │       ├── Elder
            │       └── God
            └── EnemyBase
                    └── Cattle

SceneBase
    ├── VillageScene
    ├── TempleScene
    ├── BattleScene
    └── EndScene
```

### 3.2 组合关系
```
Game
    └── SceneManager
            ├── VillageScene
            │       ├── Player
            │       ├── God
            │       ├── Elder[]
            │       ├── TiledScene
            │       ├── Camera
            │       ├── CollisionSystem
            │       └── DialogSystem
            ├── TempleScene
            │       ├── Player
            │       ├── Cattle[]
            │       ├── TiledScene
            │       ├── Camera
            │       └── CollisionSystem
            ├── BattleScene
            │       ├── BattlePlayer
            │       ├── Cattle
            │       └── BattleSystem
            ├── EndScene
            └── FadeScene
```

### 3.3 依赖关系
```
Player ──────► Action (使用动画)
God ─────────► Action (使用动画)
Elder ───────► Action (使用动画)
Cattle ──────► Action (使用动画)
BattlePlayer ► Action (使用动画)

VillageScene ► Player (拥有)
VillageScene ► God (拥有)
VillageScene ► Elder[] (拥有)
VillageScene ► TiledScene (使用)
VillageScene ► Camera (使用)
VillageScene ► CollisionSystem (使用)
VillageScene ► DialogSystem (使用)

BattleScene ─► BattlePlayer (拥有)
BattleScene ─► Cattle (拥有)
BattleScene ─► BattleSystem (使用)

SceneManager ► SceneBase[] (管理)
SceneManager ► FadeScene (使用)

Game ────────► SceneManager (拥有)
```

---

## 4. 数据流

### 4.1 玩家移动数据流
```
键盘输入 → Player.handle_input() → 更新pos_x, pos_y
                ↓
        Player.update() → 更新动画帧
                ↓
        Camera.update() → 计算偏移
                ↓
        CollisionSystem.check_obstacle_collision() → 检测碰撞
                ↓
        Scene.draw() → 绘制场景
```

### 4.2 NPC交互数据流
```
玩家移动 → CollisionSystem.check_sprite_collision() → 检测与NPC碰撞
                ↓
        Player.start_talk() → 设置is_talking=True
                ↓
        NPC.on_interact() → 返回对话列表
                ↓
        DialogSystem.start_dialog() → 开始对话
                ↓
        DialogSystem.draw() → 绘制对话框
                ↓
        空格键 → DialogSystem.next_dialog() → 下一条对话
                ↓
        对话结束 → Player.end_talk() → 恢复移动
```

### 4.3 场景切换数据流
```
触发条件 → SceneManager.switch_scene(name)
                ↓
        FadeScene.set_status(SceneStatus.Out) → 开始渐出
                ↓
        FadeScene.update() → alpha递减
                ↓
        FadeScene.get_out() → 渐出完成
                ↓
        SceneManager.current_scene = scenes[name] → 切换场景
                ↓
        FadeScene.set_status(SceneStatus.In) → 开始渐入
                ↓
        FadeScene.update() → alpha递增
                ↓
        FadeScene.set_status(SceneStatus.Normal) → 渐入完成
```

### 4.4 战斗数据流
```
触发战斗 → SceneManager.switch_scene('battle')
                ↓
        BattleScene.__init__() → 创建BattlePlayer和Cattle
                ↓
        BattleSystem.__init__() → 初始化战斗系统
                ↓
        玩家攻击 → BattleSystem.player_attack()
                ↓
        BattleSystem.calculate_damage() → 计算伤害
                ↓
        Cattle.take_damage() → 扣除血量
                ↓
        BattleSystem.check_battle_end() → 检查胜负
                ↓
        胜利/失败 → SceneManager.switch_scene('end')
```
