# 多彩生日烟花祝福

一个使用 **Python + Pygame** 开发的精美音乐同步烟花动画程序，包含 9 种烟花特效、16 段浪漫字幕、精确时间控制。

---

## 项目概览

本程序是一个完整的**音乐同步烟花特效系统**，将一首约 233 秒的背景音乐与精心编排的烟花特效、字幕文案精确同步，营造沉浸式的生日祝福体验。

核心设计理念：

- **时间驱动**：所有特效基于绝对时间（秒）驱动，不依赖帧率，确保每次播放都与音乐精确同步
- **模块化架构**：9 种特效完全独立成模块，共享统一的接口规范
- **命令式渲染**：特效模块生成"绘制命令列表"，主程序统一渲染，实现渲染与逻辑分离
- **粒子系统**：每个烟花本质是一个粒子系统，包含上升、爆炸、消散的完整生命周期

---

## 功能特点

### 9 种烟花特效

| 特效 | 文件 | 时间窗口 | 视觉特点 |
|------|------|---------|---------|
| 开场效果 | `opening.py` | 0-4 秒 | 两条交叉水平飞行粒子 + 4 条螺旋上升粒子，迸发 20 色火花 |
| 简单烟花 | `simple_yanhua.py` | 4-113 秒 / 140-222 秒 | 单次爆炸，每朵 15-18 个粒子，先保持不透明再渐变消失 |
| 日期显示 | `date_display.py` | 36-44 秒 | 底部显示 "2026 . 0626"，三段式淡入-停留-淡出 |
| 祝福烟花 | `zhufu_yanhua.py` | 45-51 秒 | 精确计算弹道，一次爆炸（浅粉红）→ 二次爆炸（多彩）→ 显示 "Happy Birthday" |
| 二次爆炸烟花 | `double_yanhua.py` | 113-140 秒 | 一次爆炸粒子在生命周期 20-30% 时触发二次爆炸（6-10 个子粒子） |
| 螺旋烟花 | `luoxuan_yanhua.py` | 113-140 秒 | 粒子呈螺旋上升，锥形拖尾，左右两侧扩散效果 |
| 三级爆炸烟花 | `three_yanhua.py` | 170 秒 / 188 秒 | 浅粉红 → 多彩 → 更小粒子，三层逐级爆炸 |
| 地面烟花 | `pen_yanhua.py` | 195-220 秒 | 3 个地面发射器持续喷射粒子，淡入→全速→淡出 |
| 结束效果 | `ending.py` | 222-233 秒 | 4 个心形粒子 + 4 个圆形粒子，沿心形/椭圆轨迹运动 |

### 16 段字幕

字幕系统提供 16 段精美文案，按时间线分为 9 个段落，涵盖从"时光长河"到"圆满如初"的完整情感叙事：

1. **时光节拍** (4-17 秒) - 时光是一条长河
2. **破土宣言** (17-31 秒) - 破茧而出，向光而立
3. **自我庆典** (31-58 秒) - 今日如歌，庆祝我即是我
4. **成长之诗** (58-85 秒) - 根须延伸，永续生长
5. **内在宇宙** (85-113 秒) - 我体内自成宇宙
6. **烟花盛典** (113-140 秒) - 夜幕是最广阔的画布
7. **重生之焰** (140-168 秒) - 灰烬之下，星火低鸣
8. **永恒回响** (168-195 秒) - 我即是不灭恒星
9. **归于中心** (195-222 秒) - 收束所有回响，圆满如初

### 4 种字幕动画

| 动画 | 描述 | 实现方式 |
|------|------|---------|
| fade | 淡入淡出 | 前 30% 淡入，中间 40% 完全显示，后 30% 淡出 |
| slide | 滑动进入 | 从屏幕边缘（上方/下方）滑动到中心位置 |
| zoom | 缩放效果 | 前 50% 字体从 0 放大到正常大小，后 50% 保持 |
| typewriter | 打字机效果 | 前 50% 逐个字符显示，50-75% 完全显示，后 25% 淡出 |

---

## 项目结构详解

```
06_多彩生日烟花祝福/
│
├── main.py                                  # [核心入口] 主程序 - 时间同步、特效调度、渲染循环
├── main1.py / main2.py                      # [备用] 旧版本备份
│
├── some_resources/                          # [特效模块包] 9 种特效 + 1 个工具模块
│   ├── __init__.py                          #   包初始化（空文件，标记为 Python 包）
│   │
│   ├── opening.py                           #   特效1 - 开场效果
│   │   └── 类: OpeningEffect                #     主类
│   │       ├── PlaneParticle (内部类)       #     水平飞行粒子（交叉轨迹）
│   │       └── SpiralParticle (内部类)      #     螺旋上升粒子
│   │
│   ├── simple_yanhua.py                     #   特效2 - 简单烟花（单次爆炸）
│   │   └── 类结构:
│   │       ├── FireworksEffect              #     主类 - 调度器
│   │       ├── RisingFirework               #     单个烟花（上升→爆炸）
│   │       └── ExplosionParticle            #     爆炸粒子（不透明→渐变消失）
│   │
│   ├── date_display.py                      #   特效3 - 日期显示
│   │   └── 类: DateEffect                   #     主类，三段式动画控制
│   │
│   ├── zhufu_yanhua.py                      #   特效4 - 祝福烟花（含 "Happy Birthday"）
│   │   └── 类结构:
│   │       ├── BlessingFirework             #     主类 - 精密弹道计算 + 文字渲染
│   │       ├── ExplosionParticleWithSecond  #     一次爆炸粒子（触发二次爆炸）
│   │       └── FinalParticle                #     二次爆炸粒子（随机生命周期 + 提前死亡）
│   │
│   ├── double_yanhua.py                     #   特效5 - 二次爆炸烟花（批量生成）
│   │   └── 类结构:
│   │       ├── FireworksWithSecondExplosionEffect  # 主类 - 批量烟花调度器
│   │       ├── RisingFireworkWithSecond            # 单个烟花（上升→爆炸→二次爆炸）
│   │       ├── ExplosionParticleWithSecond         # 一次爆炸粒子
│   │       └── FinalParticle                       # 二次爆炸粒子
│   │
│   ├── luoxuan_yanhua.py                    #   特效6 - 螺旋烟花
│   │   └── 类结构:
│   │       ├── SpiralFireworkEffect         #     主类 - 调度器
│   │       └── SpiralFireworkParticle       #     螺旋粒子（锥形拖尾 + 两侧扩散）
│   │
│   ├── three_yanhua.py                      #   特效7 - 三级爆炸烟花
│   │   └── 类结构:
│   │       ├── ThreeExplosionEffect         #     主类 - 支持多次激活
│   │       ├── TripleExplosionFirework      #     单个烟花（上升→三级爆炸）
│   │       ├── FirstLevelParticle           #     一级粒子（浅粉红）→ 产生 10 个二级粒子
│   │       ├── SecondLevelParticle          #     二级粒子 → 产生 8 个三级粒子
│   │       └── ThirdLevelParticle           #     三级粒子（最小，慢慢消散）
│   │
│   ├── pen_yanhua.py                        #   特效8 - 地面烟花
│   │   └── 类结构:
│   │       ├── GroundFireworkEffect         #     主类 - 三段式控制（淡入→发射→淡出）
│   │       ├── Firework (内部类)            #     单个发射器 - 方向管理 + 粒子发射
│   │       └── FireworkParticle (内部类)    #     单个粒子（抛物线运动 + 渐变消失）
│   │
│   └── ending.py                            #   特效9 - 结束效果
│       └── 类结构:
│           ├── EndingEffect                 #     主类 - 10 秒定时控制
│           ├── HeartParticle (内部类)       #     心形轨迹粒子（分 2 组，2 阶段运动）
│           └── CircleParticle (内部类)      #     椭圆轨迹粒子（3 阶段：进入→绕行→退出）
│
├── subtitle_module/                         # [字幕模块包] 独立的字幕播放系统
│   ├── __init__.py                          #   包初始化（空文件）
│   ├── configs.py                           #   段落配置 - 9 个生成函数，128 个节拍数据
│   │   └── 函数:
│   │       ├── create_transition_1_paragraph()     #   段落1: 时光节拍 (4-17s, 8 节拍)
│   │       ├── create_louder_paragraph()           #   段落2: 破土宣言 (17-31s, 8 节拍)
│   │       ├── create_lively_paragraph()           #   段落3: 自我庆典 (31-58s, 16 节拍)
│   │       ├── create_vitality_paragraph()         #   段落4: 成长之诗 (58-85s, 16 节拍)
│   │       ├── create_universe_paragraph()         #   段落5: 内在宇宙 (85-113s, 16 节拍)
│   │       ├── create_full_firework_paragraph()    #   段落6: 烟花盛典 (113-140s, 16 节拍)
│   │       ├── create_rebirth_paragraph()          #   段落7: 重生之焰 (140-168s, 16 节拍)
│   │       ├── create_eternal_paragraph()          #   段落8: 永恒回响 (168-195s, 16 节拍)
│   │       └── create_transition_2_paragraph()     #   段落9: 归于中心 (195-222s, 16 节拍)
│   │
│   ├── player.py                            #   字幕播放器
│   │   └── 类:
│   │       ├── ParagraphPlayer              #     主播放器 - 加载/播放/计算/渲染
│   │       └── MultiParagraphManager        #     多段落管理器（支持并发播放）
│   │
│   └── resources.py                         #   资源仓库
│       └── 数据:
│           ├── COLORS                       #     10 种预定义颜色（RGB）
│           ├── FONT_PATHS                   #     6 种字体路径映射
│           ├── ANIMATIONS                   #     4 种动画类型
│           └── 函数: get_color(), get_font(), validate_animation()
│
├── fonts/                                   # [资源] 字体文件（9 个）
│   ├── SIMHEI.TTF / simhei.ttf             #   黑体（中文字体，最保险的备选）
│   ├── SIMKAI.TTF / simkai.ttf             #   楷体
│   ├── SIMFANG.TTF / simfang.ttf           #   仿宋
│   ├── SIMSUN.TTC                          #   宋体（华文宋体）
│   ├── STFANGSO.TTF                        #   华文仿宋
│   ├── STKAITI.TTF                         #   华文楷体
│   ├── segoesc.ttf / segoescb.ttf          #   Segoe Script 花体字
│   └── BRUSHSCI.TTF                        #   Brush Script MT 花体字
│
├── BasicContent/                            # [资源] 旧版内容配置（仅供参考）
│   ├── SomeInfo.txt                         #   一些说明信息
│   ├── 字幕内容（旧）.txt                    #   旧版字幕文案
│   ├── 字幕动画.txt                         #   动画配置说明
│   ├── 字幕字体.txt                         #   字体配置说明
│   └── 完整内容效果.txt                     #   完整效果描述
│
├── 新愿-四季音色.mp3                        # [资源] 背景音乐（约 233 秒）
│
├── requirements.txt                         # Python 依赖清单
├── .gitignore                               # Git 忽略规则
└── README.md                                # 本文件（项目文档）
```

---

## 核心架构设计

### 1. 程序总体架构

程序采用**主循环调度 + 模块化特效 + 统一渲染**的架构模式：

```
┌─────────────────────────────────────────────────────────┐
│                      初始化阶段                          │
│  Pygame 初始化 → 混音器初始化 → 窗口创建 → 字幕播放器    │
│  → 9 个特效实例创建 → 音乐加载 → 2 秒等待               │
└──────────────────────┬──────────────────────────────────┘
                        ↓
┌──────────────────────┴──────────────────────────────────┐
│                    主循环 (60 FPS)                       │
│                                                         │
│  1. 获取当前播放时间 (get_playback_time)                  │
│     ├── 优先: pygame.mixer.music.get_pos()               │
│     └── 回退: pygame.time.get_ticks()                    │
│                                                         │
│  2. 特效控制逻辑                                         │
│     ├── 根据 current_time 检查每个特效的激活窗口           │
│     ├── 到达窗口 → 调用 effect.activate(current_time)     │
│     └── 离开窗口 → 调用 effect.deactivate()              │
│                                                         │
│  3. 更新所有特效 (effect.update(current_time))            │
│     └── 每个特效返回 → List[Dict] 绘制命令                │
│                                                         │
│  4. 字幕段落管理                                         │
│     ├── 预加载 (提前 0.3 秒)                             │
│     ├── 激活段落 (按序播放)                              │
│     └── player.update(internal_time) → 渲染数据          │
│                                                         │
│  5. 渲染绘制 (按 Z 轴顺序)                               │
│     ├── 日期显示 (最底层)                                 │
│     ├── 开场效果 → 简单烟花 → 螺旋烟花 → 二次爆炸         │
│     ├── 祝福烟花 → 三级爆炸 → 地面烟花 → 结束效果         │
│     └── 字幕 (最上层)                                    │
│                                                         │
│  6. 显示时间 → pygame.display.flip() → clock.tick(60)   │
│                                                         │
│  7. 检查退出条件                                         │
│     └── current_time > music_length + exit_buffer        │
└─────────────────────────────────────────────────────────┘
```

### 2. 特效模块统一接口规范

所有 9 种特效共享相同的接口约定，这是实现模块化的关键：

```python
class SomeEffect:
    # ─── 生命周期方法 ────────────────────────────

    def __init__(self, screen_width: int, screen_height: int):
        """初始化特效，创建粒子/资源"""
        pass

    def activate(self, start_time: float, duration: Optional[float] = None):
        """激活特效，start_time 为绝对时间（秒）"""
        pass

    def deactivate(self):
        """停用特效（不再生成新粒子，但已有粒子继续播放）"""
        pass

    def clear_all(self):
        """立即清除所有粒子"""
        pass

    def update(self, current_time: float) -> Optional[List[Dict]]:
        """核心方法：更新状态，返回绘制命令列表"""
        # 返回值格式:
        # [
        #     {"type": "circle", "position": (x,y), "color": (r,g,b,a), "radius": n},
        #     {"type": "text_surface", "surface": ..., "position": (x,y)},
        #     {"type": "rect", "position": (x,y), "size": (w,h), "color": (r,g,b,a)}
        # ]
        pass

    # ─── 查询方法 ────────────────────────────────

    def is_finished(self) -> bool:
        """检查特效是否完全结束"""
        pass

    def get_status(self) -> Dict:
        """获取当前状态信息"""
        pass
```

### 3. 烟花粒子系统通用生命周期

所有烟花特效的粒子遵循相似的生命周期模式：

```
    上升阶段                         爆炸阶段
┌─────────────┐              ┌─────────────────────────┐
│  从底部升起  │              │  1. 一级爆炸             │
│  白色/彩色轨迹│  到达高度    │     ├── 向外扩散          │
│  速度递减    │ ────────→   │     ├── 保持不透明         │
│  受重力影响  │              │     └── 到达生命周期点     │
└─────────────┘              │  2. 二级/三级爆炸         │
                              │     ├── 生成更多子粒子     │
                              │     ├── 更小、更慢         │
                              │     └── 父粒子消失         │
                              │  3. 消散阶段              │
                              │     ├── 透明度渐变下降      │
                              │     ├── 随机提前死亡        │
                              │     └── 轨迹淡出           │
                              └─────────────────────────┘
```

### 4. 时间同步机制

程序的核心挑战是将视觉效果与音乐精确同步，采用多层时间方案：

```python
def get_playback_time(music_start_ms, music_loaded):
    """
    时间源优先级:
    1. pygame.mixer.music.get_pos() - 从声卡驱动获取实际播放位置
       - 精度高，与音乐播放硬件同步
       - 仅在音乐成功加载且正在播放时可用
    2. pygame.time.get_ticks() - 回退到程序自启动以来的毫秒数
       - 作为备用时间源
       - 在无音乐或音乐加载失败时使用
    """
```

所有特效的 `activate(start_time)` 和 `update(current_time)` 都使用这个统一的绝对时间，确保多特效同步。

### 5. 三层渲染管线

```
特效模块内部                   绘制命令                   主程序渲染
                                                         
粒子1 ─→ get_draw_data() ─→ {"type":"circle",...} ─→ pygame.draw.circle()
粒子2 ─→ get_draw_data() ─→ {"type":"circle",...} ─→ pygame.draw.circle()
粒子3 ─→ get_draw_data() ─→ {"type":"text",...}   ─→ screen.blit()
  ·                           ·                        ·
  ·                           ·                        ·
```

这种设计的好处：
- **逻辑与渲染分离**：特效只关心粒子物理，不关心如何绘制
- **统一 Z 轴排序**：主程序决定绘制顺序，控制图层
- **易于调试**：可以插入代理层记录/分析绘制命令

---

## 各特效模块深度解析

### 特效 1：OpeningEffect（开场效果）

**文件**: `some_resources/opening.py`

以时间驱动（`dt_seconds`）为特色的开场效果。

**粒子组成**：
- **2 个 PlaneParticle**：水平交叉飞行，一个从左到右（天蓝色），一个从右到左（银白色），在屏幕中心交叉
- **4 个 SpiralParticle**：左右各 2 个，螺旋上升轨迹，粉色系

**关键设计**：
- 使用 `dt_seconds`（秒级时间差）进行连续积分，解除对帧率的依赖
- 火花生成限制机制：`max_total_sparks=1200`，`max_new_sparks_per_update=60`
- 轨迹淡出采用三阶段控制（头部 20% 可见，中间 75% 线性淡出，尾部 5% 透明）

### 特效 2：FireworksEffect（简单烟花）

**文件**: `some_resources/simple_yanhua.py`

最基本的烟花模型，作为其他烟花特效的基础参考。

**类协作流程**：
```
FireworksEffect (调度器)
    │
    ├── spawn_timer 控制生成间隔 (20-40 帧随机)
    ├── max_fireworks = 12 (同时存在上限)
    │
    └── RisingFirework (单个烟花)
        ├── 从随机水平位置升起 (50 ~ screen_width-50)
        ├── 上升速度 12-15 px/frame，受重力 0.15 减速
        ├── 爆炸条件: y <= max_height(300) 且 y >= min_height(150)
        │
        └── ExplosionParticle (15-18 个)
            ├── 随机角度爆炸，速度 3.0-4.0
            ├── 总生命周期 60-100 帧
            ├── 前 40-80% 保持不透明
            └── 后 60-20% 线性淡出
```

**颜色系统**：20 种预定义颜色，每个粒子在创建时随机选择

### 特效 3：DateEffect（日期显示）

**文件**: `some_resources/date_display.py`

纯粹的文本动画，无粒子系统。

**三段式动画控制**：
```
alpha
 255 │      ┌────────────────────┐
     │     /                      \
     │    /                        \
     │   /                          \
   0 └──┴─────────┴─────────────────┴──→ time
      淡入         停留               淡出
    1.417秒      4.667秒            1.417秒
```

**字体加载策略**：按优先级尝试 Segoe Script → Brush Script MT → SimHei

### 特效 4：BlessingFirework（祝福烟花）

**文件**: `some_resources/zhufu_yanhua.py`

最复杂的单个烟花特效，包含精密的弹道计算。

**精密弹道计算**：
```python
# 已知：
#   上升距离 s = start_y - explode_y = 650 像素
#   初始速度 v₀ = 800 像素/秒
#   加速度 a = 432 像素/秒²
# 求解上升时间 t：
#   s = v₀t - ½at²
#   ½at² - v₀t + s = 0  →  216t² - 800t + 650 = 0
#   t = (800 - sqrt(800² - 4*216*650)) / (2*216) ≈ 1.204 秒
```

**爆炸层级**：
```
一级爆炸 (30 个粒子)
    ├── 颜色: 浅粉红 (255, 192, 203)
    ├── 速度: 4.0-6.0
    └── 生命周期 20-30% 时触发二次爆炸
            │
            └── 二级爆炸 (每个父粒子产生 5-12 个 FinalParticle)
                ├── 随机多彩颜色
                ├── 速度 2.0-3.5
                ├── 生命周期 60-150 帧
                ├── 30-70% 时开始渐变
                └── 0-5% 概率提前死亡
```

**文字显示**：爆炸后立即显示 "Happy Birthday"，停留 5 秒后 0.8 秒淡出

### 特效 5：FireworksWithSecondExplosionEffect（二次爆炸烟花）

**文件**: `some_resources/double_yanhua.py`

类似特效 4 的批量版本，持续生成多个二次爆炸烟花。

**与特效 2 的区别**：
- `ExplosionParticleWithSecond` 在生命周期 20-30% 时触发二次爆炸
- 二次爆炸粒子数量 6-10 个
- 二次爆炸父粒子的生命周期缩短为原来的 2/3

### 特效 6：SpiralFireworkEffect（螺旋烟花）

**文件**: `some_resources/luoxuan_yanhua.py`

独特的螺旋上升轨迹和锥形拖尾效果。

**粒子特性**：
- 上升速度 6.0-7.5 px/frame（较慢以显现螺旋轨迹）
- 螺旋半径 1.5-3.0，角速度 0.08-0.15 rad/frame
- 最大轨迹长度 6-10 点
- **锥形拖尾**：尾部粒子逐步扩散，形成圆锥形状
- **两侧扩散**：在轨迹点的垂直方向绘制两个半透明副本

### 特效 7：ThreeExplosionEffect（三级爆炸烟花）

**文件**: `some_resources/three_yanhua.py`

最壮观的爆炸效果，支持在多个时间点独立激活。

**三级爆炸链**：
```
TripleExplosionFirework
    │
    ├── 上升阶段 (白色轨迹，速度 13 px/frame)
    │
    └── 一级爆炸 (12 个 FirstLevelParticle)
        ├── 颜色: 浅粉红 (固定)
        ├── 大小/轨迹半径: 3
        ├── 生命周期: 45 帧
        │
        └── 二级爆炸 (每个产生 10 个 SecondLevelParticle)
            ├── 颜色: 随机多彩
            ├── 大小: 1.5
            ├── 生命周期: 45 帧
            │
            └── 三级爆炸 (每个产生 8 个 ThirdLevelParticle)
                ├── 颜色: 随机多彩
                ├── 大小: 1
                ├── 生命周期: 50-150 帧
                ├── 30-70% 时开始渐变
                └── 0-5% 提前死亡
```

**支持多次激活**：`ThreeExplosionEffect` 维护 `activation_times` 列表，可以在 170 秒和 188 秒分别激活

### 特效 8：GroundFireworkEffect（地面烟花）

**文件**: `some_resources/pen_yanhua.py`

模拟地面烟花发射器，持续喷射粒子。

**三段式控制**：
```
phase:    delay       fade_in          launch          fade_out
          (2s)        (3s)            (17s)            (3s)
alpha:     0     0→255     255    255     255→0
          ─────┬──────────┬──────────────────┬──────────┬────→ time
              0          2                  5         22     25s
```

**三个发射器位置**：屏幕宽度的 1/4、1/2、3/4

**发射器内部机制**：
- `manage_directions()`: 维护 10 个发射方向，每个方向计划发射 5-10 个粒子
- `emit_particles()`: 每 50ms 对每个方向发射一个粒子
- 粒子颜色固定为白色系（带轻微暖色调）

### 特效 9：EndingEffect（结束效果）

**文件**: `some_resources/ending.py`

优雅的落幕动画，包含心形和圆形轨迹。

**心形粒子 (HeartParticle)**：
- 4 个粒子，分别沿心形轨迹的左/右半轮廓运动
- 分 2 组 (phase 1/2)，每组 2 个粒子，依次完成轨迹
- 心形公式：`x = 16·sin³(θ), y = 13·cos(θ) - 5·cos(2θ) - 2·cos(3θ) - cos(4θ)`
- 粉色系（4 种深浅不同的粉色）
- 粒子运动过程中持续迸发火花

**圆形粒子 (CircleParticle)**：
- 4 个粒子，分上下两组，沿椭圆轨迹运动
- 3 个阶段：从右侧进入 → 绕椭圆一周 → 从左侧退出
- 天蓝色和银白色，与粉色心形形成对比

---

## 字幕系统架构

### 数据流

```
configs.py (配置层)
    │
    │  每个 create_xxx_paragraph() 返回 Dict
    │  {
    │    "name": "段落名",
    │    "description": "描述",
    │    "start_time": 开始时间,
    │    "total_duration": 总时长,
    │    "beats": [{text, color, font, duration, animation, position}, ...]
    │  }
    │
    ▼
player.py (播放层)
    │
    │  ParagraphPlayer:
    │  ├── load(config) → 预处理节拍数据
    │  ├── play(start_time) → 开始播放
    │  └── update(current_time) → 计算当前帧渲染数据
    │      └── _calculate_frame(beat, progress)
    │          ├── _calculate_alpha() → 透明度
    │          ├── 根据动画类型计算位置/字体大小
    │          └── 返回 {text, color, font_name, font_size, position, alpha}
    │
    ▼
resources.py (资源层)
    │
    ├── COLORS = {名称: RGB} (10 种颜色)
    ├── FONT_PATHS = {名称: 路径} (6 种字体)
    ├── get_color(name) → RGB tuple
    └── get_font(name, size) → pygame.Font
```

### 128 个节拍的精确编排

整个字幕系统包含 **128 个节拍**，分布在 9 个段落中，每个节拍精确到毫秒级：

| 段落 | 时间范围 | 节拍数 | 节拍间隔 | 文案主题 |
|------|---------|-------|---------|---------|
| transition_1 | 4-17 秒 | 8 | 1.625 秒 | 时光长河 |
| louder | 17-31 秒 | 8 | 1.75 秒 | 破土宣言 |
| lively | 31-58 秒 | 16 | 1.688 秒 | 自我庆典 |
| vitality | 58-85 秒 | 16 | 1.688 秒 | 成长之诗 |
| universe | 85-113 秒 | 16 | 1.75 秒 | 内在宇宙 |
| full_firework | 113-140 秒 | 16 | 1.688 秒 | 烟花盛典 |
| rebirth | 140-168 秒 | 16 | 1.75 秒 | 重生之焰 |
| eternal | 168-195 秒 | 16 | 1.688 秒 | 永恒回响 |
| transition_2 | 195-222 秒 | 16 | 1.688 秒 | 归于中心 |

### 字体资源管理

字幕模块使用 6 种字体，路径配置在 `resources.py` 中：

| 字体名称 | 文件名 | 用途 |
|---------|-------|------|
| FangSong | SIMFANG.TTF | 打字机效果 |
| KaiTi | SIMKAI.TTF | 滑动进入效果 |
| 华文仿宋 | STFANGSO.TTF | 淡入淡出效果 |
| 华文楷体 | STKAITI.TTF | 缩放效果 |
| 华文宋体 | SIMSUN.TTC | 淡入淡出、缩放 |
| SimHei | SIMHEI.TTF | 默认备选 |

---

## 完整时间线

以下是整个节目 233 秒的完整时间线：

```
 0s  ─── OpeningEffect 开场效果激活 (粒子聚集、水平交叉、螺旋上升)
 4s  ─── transition_1 字幕开始・简单烟花开始
        "时光是一条长河..."
17s  ─── louder 字幕开始
        "我破茧而出..."
31s  ─── lively 字幕开始
        "今日如歌..."
36s  ─── DateEffect 日期显示 "2026 . 0626"
45s  ─── BlessingFirework 祝福烟花 "Happy Birthday"
58s  ─── vitality 字幕开始
        "根须延伸..."
85s  ─── universe 字幕开始
        "我体内自成宇宙..."
113s ─── full_firework 字幕开始・二次爆炸烟花 + 螺旋烟花开始
        "夜幕是最广阔的画布..."
140s ─── rebirth 字幕开始・简单烟花第二阶段开始
        "盛大的烟花光屑如雨..."
168s ─── eternal 字幕开始
        "我生发的光，自此独立..."
170s ─── 三级爆炸烟花 #1
188s ─── 三级爆炸烟花 #2
195s ─── transition_2 字幕开始・地面烟花开始
        "最后的声浪已然平息..."
222s ─── EndingEffect 结束效果
        "我完整，我自足，圆满如初"
233s ─── 节目结束
```

---

## 安装说明

### 前置要求

- Python 3.8 或更高版本
- pip 包管理器

### 安装步骤

1. **克隆或下载项目**
   ```bash
   git clone <仓库地址>
   cd 06_多彩生日烟花祝福
   ```

2. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```
   或者直接安装 Pygame：
   ```bash
   pip install pygame
   ```

3. **准备音乐文件**
   将背景音乐文件命名为 `新愿-四季音色.mp3` 放在项目根目录，或在 `main.py` 中修改 `music_length` 参数和音乐文件名。

### 运行

```bash
python main.py
```

### 控制

- 程序启动后自动播放（含 2 秒启动延迟）
- 按 `ESC` 键可随时退出

---

## 自定义配置

### 调整音乐同步

在 `main.py` 顶部的小配置区域：

```python
enable_logging = True    # 设为 False 关闭控制台日志
music_length = 233.0     # 修改为你的音乐实际时长（秒）
exit_buffer = 1.0        # 音乐结束后的缓冲时间
```

### 自定义字幕内容

编辑 `subtitle_module/configs.py` 中的段落生成函数：

- 修改 `text` 字段更改文案
- 修改 `color` 字段更改颜色（使用 `resources.py` 中定义的颜色名）
- 修改 `font_name` 字段更改字体
- 修改 `animation` 字段切换动画效果
- 修改 `duration` 字段调整节拍时长

### 调整特效时间

在 `main.py` 的主循环特效控制逻辑中：

```python
# 修改激活时间窗口
if 4.0 <= current_time < 113.0 and not simple_active_phase1:
    simple_fireworks.activate(current_time, 109.0)
```

### 添加字体

1. 将字体文件 (.ttf/.ttc) 放入 `fonts/` 目录
2. 在需要的特效模块的 `FONT_MAP` 或 `resources.py` 的 `FONT_PATHS` 中添加映射

---

## 技术栈

| 技术 | 用途 |
|------|------|
| **Python 3.12+** | 编程语言 |
| **Pygame 2.5+** | 游戏引擎/多媒体库 |
| **面向对象设计** | 模块化特效架构 |
| **粒子系统** | 烟花物理模拟 |
| **时间驱动架构** | 音乐同步机制 |

---

## 开源许可证

本项目仅供学习和个人使用。

---

## 作者

生日烟花祝福项目团队

---

祝你生日快乐！
