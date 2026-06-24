# 《西游记观音院》游戏需求分析文档

## 1. 项目概述

### 1.1 项目背景
本项目为软件项目开发课程实训项目，以Pygame为开发框架，实现一款以西游记"祸起观音院"为故事背景的2D RPG游戏。玩家扮演孙悟空，需要在村庄中找到土地公获取线索，最终找到观音院。

### 1.2 项目目标
- 实现一个可操作的RPG游戏原型
- 掌握Pygame模块的使用
- 运用面向对象编程思想
- 熟悉软件开发流程

### 1.3 开发周期
| 阶段 | 时长 | 内容 |
|------|------|------|
| 集中学习 | 6天 | 学习Pygame基础知识 |
| 分散实现 | 6天 | 项目开发实现 |
| 答辩 | 1天 | 项目展示与答辩 |

---

## 2. 功能需求

### 2.1 核心功能模块

#### 2.1.1 场景显示模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-001 | 背景图片显示 | 在窗口中显示游戏背景图片 | 高 |
| F-002 | TMX地图渲染 | 使用pytmx加载并渲染Tiled地图 | 高 |
| F-003 | 多图层支持 | 支持图块层、图像层、对象层 | 高 |
| F-004 | 地图封装 | 将TMX地图封装为可复用的类 | 中 |

#### 2.1.2 角色系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-010 | 精灵基类 | 创建pygame.sprite.Sprite基类 | 高 |
| F-011 | 动画行为类 | Action类管理帧动画 | 高 |
| F-012 | 玩家角色 | 孙悟空角色实现 | 高 |
| F-013 | NPC角色 | 村民、土地公等NPC实现 | 高 |
| F-014 | 怪物角色 | 战斗怪物实现 | 中 |

#### 2.1.3 控制系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-020 | 键盘控制 | 方向键/WASD控制玩家移动 | 高 |
| F-021 | 4方向动画 | 根据移动方向播放对应动画 | 高 |
| F-022 | TMX位置加载 | 从TMX对象层读取初始位置 | 高 |
| F-023 | 交互提示显示 | 靠近NPC/怪物时显示"按空格键发起对话/战斗"提示 | 高 |

#### 2.1.4 碰撞系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-030 | 矩形碰撞 | pygame.sprite.collide_rect | 高 |
| F-031 | 障碍物碰撞 | 玩家与障碍物碰撞停步 | 高 |
| F-032 | NPC碰撞 | 玩家与NPC碰撞停步，防止重叠 | 高 |
| F-033 | NPC交互检测 | 玩家靠近NPC时触发交互提示，inflate(20,20)扩大检测范围 | 高 |
| F-034 | 怪物碰撞 | 玩家与怪物碰撞停步 | 高 |
| F-035 | 怪物交互检测 | 玩家靠近怪物时触发战斗提示，inflate(40,40)扩大检测范围 | 高 |
| F-036 | 圆碰撞 | pygame.sprite.collide_circle | 低 |
| F-037 | 遮罩碰撞 | pygame.sprite.collide_mask | 低 |

#### 2.1.5 场景管理模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-040 | 相机系统 | 窗口跟随玩家移动 | 高 |
| F-041 | 边界控制 | 避免玩家和窗口越界 | 高 |
| F-042 | 场景切换 | 村庄→寺庙→结束场景切换 | 高 |
| F-043 | 渐变效果 | 场景切换渐入渐出效果 | 中 |

#### 2.1.6 对话系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-050 | 对话框显示 | 显示半透明黑色对话框UI | 高 |
| F-051 | 文字绘制 | 第一行显示"角色名：对话内容"（24px粗体） | 高 |
| F-052 | 透明Surface | 对话框半透明效果 (alpha=200) | 中 |
| F-053 | 操作提示 | 第二行显示"按空格键继续 · 按Esc键退出"（14px粗体） | 高 |
| F-054 | 多行支持 | 对话内容自动换行显示 | 中 |

#### 2.1.7 战斗系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-060 | 战斗场景 | 独立的战斗场景 | 高 |
| F-061 | 怪物出现 | 战斗场景中怪物出现 | 高 |
| F-062 | 战斗状态 | 战斗状态变化和结算 | 高 |
| F-063 | 打斗玩家 | 打斗版孙悟空实现 | 高 |
| F-064 | 怪物动画 | 怪物多种动画状态 | 中 |
| F-065 | 战斗触发 | 按空格键触发战斗（非自动触发） | 高 |
| F-066 | 战斗提示 | 靠近怪物时显示"按空格键发起战斗" | 高 |

#### 2.1.8 音效系统模块
| 功能编号 | 功能名称 | 功能描述 | 优先级 |
|----------|----------|----------|--------|
| F-070 | 背景音乐 | 各场景背景音乐循环播放 | 高 |
| F-071 | 音效播放 | 打斗、交互等音效 | 高 |
| F-072 | 音乐切换 | 不同场景不同背景音乐 | 中 |

---

## 3. 非功能需求

### 3.1 性能需求
| 需求编号 | 需求描述 | 指标 |
|----------|----------|------|
| NF-001 | 帧率 | 游戏运行帧率 ≥ 40 FPS |
| NF-002 | 响应时间 | 键盘操作响应延迟 < 50ms |
| NF-003 | 内存占用 | 游戏内存占用 < 500MB |

### 3.2 兼容性需求
| 需求编号 | 需求描述 |
|----------|----------|
| NF-010 | 支持Windows 10/11操作系统 |
| NF-011 | 支持Python 3.0及以上版本 |
| NF-012 | 支持Pygame 2.0及以上版本 |

### 3.3 可维护性需求
| 需求编号 | 需求描述 |
|----------|----------|
| NF-020 | 代码采用面向对象设计，支持扩展 |
| NF-021 | 角色基类支持新角色继承扩展 |
| NF-022 | 场景基类支持新场景扩展 |

---

## 4. 系统架构设计

### 4.1 模块结构
```
journey_to_the_west/
├── main.py              # 游戏入口
├── config.py            # 全局配置
├── core/                # 核心模块
│   ├── game.py          # Game主类
│   ├── camera.py        # 相机系统
│   └── scene_manager.py # 场景管理器
├── actors/              # 角色模块
│   ├── action.py        # 动画行为类
│   ├── base_actor.py    # 角色基类
│   ├── player.py        # 玩家类
│   ├── npc.py           # NPC基类
│   ├── elder.py         # 村民类
│   ├── god.py           # 土地公类
│   └── enemy.py         # 怪物基类
├── systems/             # 系统模块
│   ├── dialog.py        # 对话系统
│   ├── battle.py        # 战斗系统
│   └── collision.py     # 碰撞系统
├── scenes/              # 场景模块
│   ├── base_scene.py    # 场景基类
│   ├── village.py       # 村庄场景
│   ├── temple.py        # 寺庙场景
│   ├── battle_scene.py  # 战斗场景
│   └── end_scene.py     # 结束场景
├── utils/               # 工具模块
│   ├── tiled_render.py  # TMX渲染器
│   └── fade_scene.py    # 渐变效果
└── resource/            # 资源文件
```

### 4.2 类图关系
```
pygame.sprite.Sprite
    └── ActorBase (角色基类)
        ├── Player (玩家)
        ├── NPCBase (NPC基类)
        │   ├── Elder (村民)
        │   └── God (土地公)
        └── EnemyBase (怪物基类)

SceneBase (场景基类)
    ├── VillageScene (村庄)
    ├── TempleScene (寺庙)
    ├── BattleScene (战斗)
    └── EndScene (结束)
```

---

## 5. 数据需求

### 5.1 资源文件

| 类型 | 路径 | 说明 |
|------|------|------|
| 玩家精灵 | resource/img/swk2/ | 孙悟空128帧PNG |
| NPC精灵 | resource/img/elder/ | 村民TGA格式 |
| 怪物精灵 | resource/img/cattle/ | 牛怪TGA格式 |
| 土地公 | resource/img/god/ | 土地公4方向40帧 |
| 地图文件 | resource/tmx/village1.tmx | 村庄地图 |
| 地图文件 | resource/tmx/temple.tmx | 寺庙地图 |
| 背景图片 | resource/img/village.jpg | 村庄背景 |
| 字体文件 | resource/font/newfont.TTF | 中文字体 |
| 音效文件 | resource/sound/ | 背景音乐和音效 |

### 5.2 TMX地图结构 (village1.tmx)

| 图层名称 | 类型 | 说明 |
|----------|------|------|
| backgroud | imagelayer | 背景图层 |
| actor | objectgroup | 玩家位置 (sun, tang) |
| elder | objectgroup | 村民NPC位置 (elder1~4) |
| god | objectgroup | 土地公位置 |
| child | objectgroup | 儿童NPC位置 |
| obstacle | objectgroup | 障碍物碰撞区域 |

---

## 6. 约束条件

### 6.1 技术约束
| 约束编号 | 约束描述 |
|----------|----------|
| C-001 | 必须使用Pygame框架开发 |
| C-002 | 必须使用pytmx库加载TMX地图 |
| C-003 | 必须使用面向对象编程思想 |
| C-004 | 必须实现角色基类以支持扩展 |
| C-005 | 必须实现战斗系统（教程步骤18-21） |
| C-006 | 必须实现渐变效果（教程步骤16） |
| C-007 | 必须实现音效系统（教程步骤23） |

### 6.2 资源约束
| 约束编号 | 约束描述 |
|----------|----------|
| C-010 | 使用提供的资源文件，不可外部引入 |
| C-011 | 地图使用village1.tmx和temple.tmx |
| C-012 | 字体使用resource/font/newfont.TTF |

### 6.3 开发约束
| 约束编号 | 约束描述 |
|----------|----------|
| C-020 | 按照23步教程顺序实现 |
| C-021 | 每步完成后需测试验证 |
| C-022 | 代码需有适当注释 |

---

## 7. 故事情节

### 7.1 背景
孙悟空保护唐僧西天取路，来到一座观音院前。需要找到土地公了解情况，得知寺院中有妖怪偷走了袈裟。

### 7.2 场景流程
```
┌─────────────┐
│  村庄场景   │ ← 初始场景，玩家可自由移动
│  (village)  │
└──────┬──────┘
       │ 孙悟空移动，遇到土地公碰撞
       ▼
┌─────────────┐
│  对话触发   │ ← 土地公对话
│  土地公对话  │   "去寺庙找回袈裟"
└──────┬──────┘
       │ 对话结束，触发场景切换
       ▼
┌─────────────┐
│  渐变效果   │ ← FadeScene alpha渐变
│  (FadeScene) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  寺庙场景   │ ← 玩家继续探索
│  (temple)   │
└──────┬──────┘
       │ 遇到怪物或触发战斗
       ▼
┌─────────────┐
│  战斗场景   │ ← 与怪物战斗
│ (battle)    │
└──────┬──────┘
       │ 战斗结束
       ▼
┌─────────────┐
│  结束场景   │ ← 显示胜利/失败画面
│  (end)      │
└─────────────┘
```

### 7.3 角色设定
| 角色 | 位置 | 功能 | 素材 |
|------|------|------|------|
| 孙悟空 | 村庄/寺庙 | 玩家控制主角 | swk2 (128帧PNG) |
| 唐僧 | 村庄 | 剧情角色，TMX中定义 | - |
| 村民 (elder1~4) | 村庄 | 背景NPC，可扩展对话 | elder目录 (TGA) |
| 土地公 | 村庄 | 剧情NPC，触发场景切换 | god目录 (40帧TGA) |
| 怪物 | 战斗场景 | 战斗敌人 | cattle目录 (TGA) |
| 打斗孙悟空 | 战斗场景 | 战斗版玩家 | swk目录 (16帧TGA) |

### 7.4 对话内容设计
```python
# 土地公对话（触发场景切换）
god_dialog = [
    {"speaker": "土地公", "text": "施主可是孙悟空？"},
    {"speaker": "土地公", "text": "贫僧知道袈裟在何处。"},
    {"speaker": "土地公", "text": "请随我来，去观音院找回袈裟。"},
]

# 村民对话（扩展任务）
elder_dialogs = {
    "elder1": [
        {"speaker": "村民", "text": "欢迎来到村庄！"},
    ],
    "elder2": [
        {"speaker": "村民", "text": "听说寺庙里有妖怪。"},
    ],
}
```

---

## 8. 详细设计规格

### 8.1 战斗系统设计

#### 战斗流程
```
进入战斗场景 → 怪物出现 → 玩家攻击 → 怪物攻击 → 判定胜负 → 结束战斗
```

#### 战斗状态
| 状态 | 说明 | 转换条件 |
|------|------|----------|
| READY | 战斗准备 | 进入战斗场景 |
| FIGHTING | 战斗中 | 开始攻击 |
| WIN | 胜利 | 怪物血量≤0 |
| LOSE | 失败 | 玩家血量≤0 |

#### 怪物动画状态
| 状态 | 素材目录 | 说明 |
|------|----------|------|
| station | cattle/station/ | 待机状态 |
| walk1/walk2 | cattle/walk1/, walk2/ | 行走动画 |
| fight | cattle/fight/ | 攻击动画 |
| die | cattle/die/ | 死亡动画 |
| back | cattle/back/ | 后退动画 |
| look | cattle/look/ | 观察动画 |
| run | cattle/run/ | 奔跑动画 |

### 8.2 渐变效果设计

#### FadeScene状态机
```
状态转换：
In (渐入) → Normal (正常显示) → Out (渐出) → Over (结束)
```

#### Alpha值变化
| 状态 | Alpha变化 | 步长 | 说明 |
|------|-----------|------|------|
| In | 0→255 | +20/帧 | 从透明到不透明 |
| Normal | 255 | 不变 | 正常显示 |
| Out | 255→0 | -20/帧 | 从不透明到透明 |
| Over | 0 | 不变 | 渐变结束 |

#### 实现代码框架
```python
class SceneStatus(enum.IntEnum):
    In = 1
    Normal = 2
    Out = 3
    Over = 4

class FadeScene:
    def __init__(self, back_image):
        self.back_image = back_image
        self.alpha = 0
        self.status = SceneStatus.In
        self.alpha_step = 20

    def set_status(self, status):
        self.status = status
        if status == SceneStatus.In:
            self.alpha = 0
        elif status == SceneStatus.Normal:
            self.alpha = 255
        elif status == SceneStatus.Out:
            self.alpha = 255

    def get_out(self):
        return self.status == SceneStatus.Over

    def update(self):
        if self.status == SceneStatus.In:
            self.alpha = min(255, self.alpha + self.alpha_step)
            if self.alpha >= 255:
                self.status = SceneStatus.Normal
        elif self.status == SceneStatus.Out:
            self.alpha = max(0, self.alpha - self.alpha_step)
            if self.alpha <= 0:
                self.status = SceneStatus.Over
```

### 8.3 音效系统设计

#### 音乐配置
| 场景 | 背景音乐 | 循环播放 |
|------|----------|----------|
| 村庄 | aigei.mp3 | 是 |
| 寺庙 | nmw.mp3 | 是 |
| 战斗 | swk.wav | 否 |

#### 音效触发
| 事件 | 音效 | 说明 |
|------|------|------|
| 场景切换 | swk.wav | 切换音效 |
| 攻击 | - | 战斗攻击音效 |
| 胜利 | - | 战斗胜利音效 |

#### 实现代码
```python
# 初始化声音模块
pygame.mixer.init()

# 加载背景音乐
pygame.mixer.music.load('resource/sound/aigei.mp3')
pygame.mixer.music.play(-1)  # -1表示无限循环

# 播放音效
sound = pygame.mixer.Sound('resource/sound/swk.wav')
sound.play()
```

### 8.4 相机系统设计

#### 相机跟随逻辑
```python
class Camera:
    def __init__(self, map_width, map_height, screen_width, screen_height):
        self.map_width = map_width
        self.map_height = map_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.offset_x = 0
        self.offset_y = 0

    def update(self, target_x, target_y):
        # 计算偏移，使玩家居中
        self.offset_x = target_x - self.screen_width // 2
        self.offset_y = target_y - self.screen_height // 2

        # 边界限制
        self.offset_x = max(0, min(self.offset_x, self.map_width - self.screen_width))
        self.offset_y = max(0, min(self.offset_y, self.map_height - self.screen_height))

    def apply(self, x, y):
        # 世界坐标转屏幕坐标
        return x - self.offset_x, y - self.offset_y
```

### 8.5 碰撞系统设计

碰撞检测采用两层设计，直接在各场景中实现：

#### 物理碰撞（停步检测）
```python
# 在场景的update方法中，将NPC/怪物碰撞框作为障碍物传入玩家更新
npc_rects = [npc.get_rect() for npc in self.npcs if npc is not self.current_npc]
self.player.update(keys, self.obstacles + npc_rects)
```

#### 交互检测（inflate扩大范围）
```python
# NPC交互检测 - inflate(20,20)扩大检测范围
def _update_nearby_npc(self):
    player_rect = self.player.get_rect()
    self.nearby_npc = None
    for npc in self.npcs:
        npc_rect = npc.get_rect().inflate(20, 20)
        if player_rect.colliderect(npc_rect):
            self.nearby_npc = npc
            break

# 怪物交互检测 - inflate(40,40)扩大检测范围
def _update_nearby_monster(self):
    player_rect = self.player.get_rect()
    monster_rect = self.monster.get_rect().inflate(40, 40)
    self.nearby_monster = player_rect.colliderect(monster_rect)
```

---

## 9. 测试需求

### 9.1 功能测试
| 测试编号 | 测试内容 | 预期结果 | 优先级 |
|----------|----------|----------|--------|
| T-001 | 地图显示 | 村庄地图正确显示 | 高 |
| T-002 | 玩家移动 | 方向键/WASD控制移动正常 | 高 |
| T-003 | 动画效果 | 移动时播放行走动画 | 高 |
| T-004 | 障碍物碰撞 | 无法穿越建筑物 | 高 |
| T-005 | NPC交互 | 与土地公对话触发场景切换 | 高 |
| T-006 | 场景切换 | 村庄→寺庙切换正常 | 高 |
| T-007 | 渐变效果 | 场景切换有渐入渐出 | 高 |
| T-008 | 战斗场景 | 战斗场景正常运行 | 高 |
| T-009 | 音效播放 | 背景音乐循环播放 | 高 |
| T-010 | 相机跟随 | 窗口跟随玩家移动 | 高 |
| T-011 | 边界控制 | 玩家和窗口不越界 | 高 |
| T-012 | 村民对话 | 与村民对话显示文字 | 中 |
| T-013 | 战斗胜利 | 战斗胜利显示结束画面 | 中 |
| T-014 | NPC碰撞 | 玩家遇到NPC停步，防止重叠 | 高 |
| T-015 | 怪物碰撞 | 玩家遇到怪物停步 | 高 |
| T-016 | NPC交互提示 | 靠近NPC显示"按空格键发起对话" | 高 |
| T-017 | 怪物战斗提示 | 靠近怪物显示"按空格键发起战斗" | 高 |
| T-018 | 空格键触发战斗 | 按空格键触发战斗（非自动） | 高 |
| T-019 | 对话框格式 | 第一行显示"角色：内容"，第二行显示操作提示 | 高 |
| T-020 | 村民加载 | 4个村民正确加载并显示 | 高 |

### 9.2 性能测试
| 测试编号 | 测试内容 | 预期结果 |
|----------|----------|----------|
| T-023 | 帧率测试 | 稳定40FPS以上 |
| T-021 | 内存测试 | 运行时内存稳定 |
| T-022 | 响应测试 | 键盘操作响应延迟<50ms |

---

## 10. 文档清单

| 文档名称 | 文档类型 | 说明 |
|----------|----------|------|
| 需求分析文档 | 本文档 | 项目需求分析 |
| 设计实现文档 | 待编写 | 系统设计与实现 |
| 测试文档 | 待编写 | 测试用例与结果 |
