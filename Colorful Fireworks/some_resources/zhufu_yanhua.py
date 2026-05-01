# some_resources/zhufu_yanhua.py
"""
祝福烟花模块 - 精确时间控制
在44.0883秒激活，45.292秒爆炸，显示"Happy Birthday"文字
修改说明：
1. 上升轨迹颜色改为白色，粗细加粗
2. 增加二次爆炸效果
3. 第一次爆炸颜色为浅粉红色
"""
import math
import random
from typing import List, Dict, Any, Optional, Tuple

# 第二次爆炸粒子的颜色列表（从参考代码中复制）
SECONDARY_COLORS = [
    (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255),
    (128, 0, 128), (255, 255, 255), (255, 215, 0), (255, 192, 203), (0, 255, 255),
    (0, 128, 128), (128, 255, 0), (255, 105, 180), (192, 192, 192), (255, 105, 97),
    (255, 255, 204), (135, 206, 250), (124, 252, 0), (255, 69, 0), (173, 216, 230)
]

# 字体加载函数 - 与日期显示模块保持一致
def get_font(font_name, size):
    """
    获取字体对象 - 绝对路径强制版本
    只从本地fonts文件夹加载指定字体文件，失败时直接报错
    """
    import os
    import pygame

    # 字体名称到字体文件的映射
    FONT_MAP = {
        "Segoe Script": "segoesc.ttf",  # 第一种花体字
        "Brush Script MT": "BRUSHSCI.TTF",  # 第二种花体字
        "SimHei": "SIMHEI.TTF",  # 默认字体
    }

    # 检查字体名是否在我们的映射中
    if font_name not in FONT_MAP:
        raise ValueError(f"字体 '{font_name}' 不在允许的字体列表中。只允许: {list(FONT_MAP.keys())}")

    # 获取字体文件名
    font_filename = FONT_MAP[font_name]

    # 查找字体文件的绝对路径
    # 方法1: 尝试在当前脚本所在目录的fonts文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(script_dir, "fonts")
    font_path = os.path.join(fonts_dir, font_filename)

    # 如果方法1找不到，尝试方法2: 在项目根目录的fonts文件夹
    if not os.path.exists(font_path):
        project_root = os.path.dirname(script_dir)
        fonts_dir = os.path.join(project_root, "fonts")
        font_path = os.path.join(fonts_dir, font_filename)

    # 检查字体文件是否存在
    if not os.path.exists(font_path):
        # 列出可用的字体文件，帮助用户排查
        if os.path.exists(fonts_dir):
            available_fonts = os.listdir(fonts_dir)
            error_msg = f"错误：找不到字体文件 '{font_filename}'\n"
            error_msg += f"搜索路径: {font_path}\n"
            error_msg += f"fonts文件夹中现有的文件:\n"
            for f in available_fonts:
                error_msg += f"  - {f}\n"
            error_msg += f"请确保 '{font_filename}' 文件存在于fonts文件夹中"
        else:
            error_msg = f"错误：fonts文件夹不存在于路径: {fonts_dir}\n"
            error_msg += f"请创建fonts文件夹并放入以下字体文件:\n"
            error_msg += f"  - segoesc.ttf (Segoe Script 花体字)\n"
            error_msg += f"  - BRUSHSCI.TTF (Brush Script MT 花体字)\n"
            error_msg += f"  - SIMHEI.TTF (黑体)"

        print(f"❌ {error_msg}")
        raise FileNotFoundError(f"字体文件未找到: {font_filename}")

    # 尝试加载字体
    try:
        font = pygame.font.Font(font_path, size)
        print(f"✅ 成功加载字体: {font_name} ({font_filename})")
        return font
    except Exception as e:
        print(f"❌ 错误：无法加载字体文件 {font_path}")
        print(f"错误信息: {e}")
        raise Exception(f"字体文件加载失败: {font_filename}")

class FinalParticle:
    """二次爆炸粒子类 - 添加与三级粒子相同的随机消失效果"""

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y

        # 随机颜色
        self.color = random.choice(SECONDARY_COLORS)

        # 运动参数
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2.0, 3.5)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.05
        self.drag = 0.98

        # 随机生命周期参数
        min_life = 60
        max_life = 150
        self.max_life = random.randint(min_life, max_life)
        self.life = self.max_life

        # 随机渐变开始时间（生命周期的一定比例）
        fade_start_ratio = random.uniform(0.3, 0.7)  # 30%-70%时开始渐变
        self.fade_start = int(self.max_life * fade_start_ratio)

        # 随机提前死亡概率
        self.early_death_chance = random.uniform(0.0, 0.05)  # 0-5%提前死亡概率

        # 轨迹系统
        self.trail: List[Tuple[int, int]] = []
        self.max_trail_length = 8
        self.frame_count = 0

        # 粒子状态
        self.is_destroyed = False

    def update(self, dt: float = 1.0) -> None:
        """更新粒子状态"""
        if self.is_destroyed:
            return

        # 应用阻力和重力
        self.vx *= self.drag
        self.vy *= self.drag
        self.vy += self.gravity

        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 更新轨迹
        self.frame_count += 1
        if self.frame_count % 1 == 0:
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > self.max_trail_length:
                self.trail.pop(0)

        # 生命周期递减
        self.life -= 1

        # 在渐变阶段，有概率提前死亡
        if self.life <= self.fade_start and self.life > 0:
            if random.random() < self.early_death_chance:
                self.is_destroyed = True
                return

        # 当生命结束时，标记为销毁状态
        if self.life <= 0:
            self.is_destroyed = True

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return not self.is_destroyed

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据"""
        if self.is_destroyed:
            return []

        draw_commands = []

        # 计算透明度 - 与ThirdLevelParticle完全相同的逻辑
        if self.life > self.fade_start:
            # 不透明阶段：前阶段，透明度为255
            alpha = 255
        else:
            # 渐变阶段：后阶段，线性渐变
            fade_life = self.life
            fade_max = self.fade_start
            if fade_max > 0:
                alpha = int(255 * (fade_life / fade_max))
            else:
                alpha = 0

        # 绘制轨迹
        for (tx, ty) in self.trail:
            if alpha <= 10:
                continue
            draw_commands.append({
                "type": "circle",
                "position": (tx, ty),
                "color": (*self.color, alpha),
                "radius": 1.2
            })

        # 绘制粒子本身
        if alpha > 10:
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": 1.2
            })

        return draw_commands

class ExplosionParticleWithSecond:
    """一次爆炸粒子类（会再次爆炸）"""
    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y
        self.explode_speed = random.uniform(4.0, 6.0)
        self.drag = 0.975

        # 第一次爆炸颜色：浅粉红色
        self.color = (255, 192, 203)  # 浅粉红色

        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.explode_speed
        self.vy = math.sin(self.angle) * self.explode_speed
        self.gravity = 0.04

        # 滞留时间缩短为原来的2/3
        random_life = random.randint(80, 100)  # 原参考代码的生命帧数范围
        self.life = int(random_life * 2 / 3)
        self.max_life = self.life

        self.trail: List[Tuple[int, int]] = []
        self.frame_count = 0
        self.secondary_exploded = False
        self.secondary_particles: List[FinalParticle] = []
        self.has_triggered_second = False  # 标记是否已触发二次爆炸

    def update(self, dt: float = 1.0) -> None:
        """更新粒子状态"""
        # 如果已经触发了二次爆炸，只更新二次爆炸粒子
        if self.has_triggered_second:
            self.secondary_particles = [p for p in self.secondary_particles if p.is_alive()]
            for particle in self.secondary_particles:
                particle.update(dt)
            return

        # 应用阻力和重力
        self.vx *= self.drag
        self.vy *= self.drag
        self.vy += self.gravity

        # 更新位置
        self.x += self.vx * dt
        self.y += self.vy * dt

        # 更新轨迹
        self.frame_count += 1
        if self.frame_count % 1 == 0:
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > 15:
                self.trail.pop(0)

        # 检查是否该进行二次爆炸（在生命周期的20%-30%时）
        if not self.secondary_exploded and self.life < self.max_life * 0.3:
            self.secondary_exploded = True
            self.has_triggered_second = True

            # 生成二次爆炸粒子（5-12个）
            particle_count = random.randint(5, 12)
            self.secondary_particles = [
                FinalParticle(self.x, self.y)
                for _ in range(particle_count)
            ]

        # 更新二次爆炸粒子
        if self.secondary_exploded:
            self.secondary_particles = [p for p in self.secondary_particles if p.is_alive()]
            for particle in self.secondary_particles:
                particle.update(dt)

        # 只有没有触发二次爆炸时才减少生命
        if not self.has_triggered_second:
            self.life -= 1

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return (self.life > 0 and not self.has_triggered_second) or len(self.secondary_particles) > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据"""
        draw_commands = []

        # 只有在生命大于0且没有触发二次爆炸时才绘制一次爆炸粒子
        if self.life > 0 and not self.has_triggered_second:
            # 绘制轨迹 - 一次爆炸粒子保持完全不透明
            for (tx, ty) in self.trail:
                alpha = 255
                if alpha <= 10:
                    continue
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 3  # 从2改为3
                })

            # 绘制粒子本身 - 一次爆炸粒子保持完全不透明
            alpha = 255
            if alpha > 10:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.color, alpha),
                    "radius": 3  # 从2改为3
                })

        # 绘制二次爆炸粒子
        for particle in self.secondary_particles:
            particle_commands = particle.get_draw_data()
            draw_commands.extend(particle_commands)

        return draw_commands

class BlessingFirework:
    """
    祝福烟花效果
    精确时间控制，在45.292秒爆炸显示"Happy Birthday"
    修改：增加二次爆炸效果
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        """
        初始化祝福烟花

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        # 窗口尺寸
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 固定参数 - 确保精确时间控制
        self.start_y = screen_height  # 起始位置：屏幕底部
        self.explode_y = 250  # 爆炸高度：250像素
        self.rise_distance = self.start_y - self.explode_y  # 上升距离：650像素

        # 运动参数（固定值）
        self.initial_velocity = 800.0  # 初始速度：800像素/秒
        self.acceleration = 432.0  # 加速度：432像素/秒²

        # 计算上升时间：s = v₀t - ½at²
        # 解二次方程：½at² - v₀t + s = 0
        a = 0.5 * self.acceleration
        b = -self.initial_velocity
        c = self.rise_distance

        # 计算判别式
        discriminant = b ** 2 - 4 * a * c

        if discriminant < 0:
            raise ValueError("参数设置错误，无法到达目标高度")

        # 解二次方程，取较小的正根（上升过程）
        sqrt_discriminant = math.sqrt(discriminant)
        t1 = (-b - sqrt_discriminant) / (2 * a)
        t2 = (-b + sqrt_discriminant) / (2 * a)

        # 取正数且较小的解
        self.rise_time = min(t for t in [t1, t2] if t > 0)

        # 验证计算
        print(f"祝福烟花参数验证:")
        print(f"  上升距离: {self.rise_distance}像素")
        print(f"  初始速度: {self.initial_velocity}像素/秒")
        print(f"  加速度: {self.acceleration}像素/秒²")
        print(f"  计算上升时间: {self.rise_time:.6f}秒")
        print(f"  理论爆炸时间: 激活时间 + {self.rise_time:.6f}秒")

        # 控制变量
        self.is_active = False
        self.start_time = 0.0
        self.exploded = False
        self.text_finished = False

        # 上升轨迹
        self.current_x = screen_width // 2
        self.current_y = self.start_y
        self.rise_trail = []

        # 颜色设置
        self.rise_color = (255, 255, 255)  # 白色
        self.first_explosion_color = (255, 192, 203)  # 浅粉红色
        self.text_color = (255, 192, 203)  # 粉色

        # 爆炸粒子
        self.explosion_particles = []
        self.explosion_duration = 2.5  # 爆炸总持续时间（包括二次爆炸）

        # 文字参数
        self.text_duration = 5.8  # 文字总持续时间（5秒显示 + 0.8秒淡出）
        self.text_show_duration = 5.0  # 文字完全显示时间
        self.text_fade_duration = 0.8  # 文字淡出时间

        # 状态跟踪
        self.explosion_start_time = 0.0
        self.text_start_time = 0.0

        # 初始化文字
        self._init_text()

    def _init_text(self):
        """初始化文字"""
        font_size = 90

        # 只尝试这3种字体，按优先级顺序
        font_names = [
            "Segoe Script",  # 第一种花体字
            "Brush Script MT",  # 第二种花体字
            "SimHei",  # 默认字体
        ]

        font_loaded = False
        for font_name in font_names:
            try:
                # 使用我们的get_font函数加载字体
                # 注意：原代码有bold=True，但我们的字体文件可能不包含粗体版本
                # 如果需要粗体，可以增加粗体字体文件
                self.text_font = get_font(font_name, font_size)

                # 测试字体渲染是否正常
                test_surface = self.text_font.render("Happy Birthday", True, self.text_color)
                if test_surface.get_width() > 0:
                    print(f"✅ 祝福烟花成功加载字体: {font_name}")
                    font_loaded = True
                    break
                else:
                    print(f"⚠️ 字体 {font_name} 渲染测试失败")
            except Exception as e:
                print(f"❌ 字体 {font_name} 加载失败: {e}")
                if font_name == "SimHei":  # 如果是最后一种字体也失败
                    print("❌ 所有指定字体加载失败！程序无法继续运行。")
                    raise Exception("祝福烟花字体加载失败，程序终止。")
                # 继续尝试下一种字体

        if not font_loaded:
            raise Exception("字体加载失败，程序终止。")

        # 创建文字表面
        self.text_surface = self.text_font.render("Happy Birthday", True, self.text_color)
        text_width, text_height = self.text_surface.get_size()

        # 计算文字位置（屏幕中央偏上）
        self.text_x = (self.screen_width - text_width) // 2
        self.text_y = 300

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活烟花效果

        Args:
            start_time: 开始时间（秒），应为44.0883秒
            duration: 持续时间（秒），忽略此参数
        """
        self.is_active = True
        self.start_time = start_time

        # 重置状态
        self.current_y = self.start_y
        self.rise_trail = []
        self.exploded = False
        self.text_finished = False
        self.explosion_particles = []

        print(f"祝福烟花激活: 开始时间={start_time:.6f}秒")
        print(f"预期爆炸时间: {start_time + self.rise_time:.6f}秒")

    def deactivate(self) -> None:
        """停用效果"""
        self.is_active = False

    def clear_all(self) -> None:
        """清除所有效果"""
        self.is_active = False
        self.explosion_particles = []
        self.rise_trail = []

    def update(self, current_time: float) -> Optional[List[Dict[str, Any]]]:
        """
        更新效果状态

        Args:
            current_time: 当前时间（秒）

        Returns:
            绘制命令列表，如果没有绘制命令则返回None
        """
        if not self.is_active:
            return None

        # 计算经过时间
        elapsed_time = current_time - self.start_time
        if elapsed_time < 0:
            return None

        draw_commands = []

        # 检查是否应该爆炸
        if not self.exploded and elapsed_time >= self.rise_time:
            # 触发爆炸
            self._explode(current_time)

        if not self.exploded:
            # 上升阶段
            self._update_rising(elapsed_time, draw_commands)
        else:
            # 爆炸后阶段
            explosion_elapsed = current_time - self.explosion_start_time
            text_elapsed = current_time - self.text_start_time

            # 更新爆炸粒子
            if explosion_elapsed < self.explosion_duration:
                self._update_explosion_particles(explosion_elapsed, draw_commands)

            # 更新文字
            if text_elapsed < self.text_duration:
                self._update_text(text_elapsed, draw_commands)
            elif not self.text_finished:
                self.text_finished = True

        # 检查是否结束
        if self.text_finished and len(self.explosion_particles) == 0:
            self.is_active = False

        return draw_commands if draw_commands else None

    def _update_rising(self, elapsed_time: float, draw_commands: List[Dict[str, Any]]):
        """更新上升阶段"""
        if elapsed_time > self.rise_time:
            elapsed_time = self.rise_time

        # 计算当前高度：y = y0 - (v₀t - ½at²)
        self.current_y = self.start_y - (
                self.initial_velocity * elapsed_time -
                0.5 * self.acceleration * elapsed_time ** 2
        )

        # 记录轨迹
        self.rise_trail.append((int(self.current_x), int(self.current_y)))
        if len(self.rise_trail) > 60:
            self.rise_trail.pop(0)

        # 绘制上升轨迹
        for i, (tx, ty) in enumerate(self.rise_trail):
            # 轨迹透明度：后面的轨迹更淡
            trail_alpha = int(255 * (i / len(self.rise_trail)))
            if trail_alpha > 10:
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.rise_color, trail_alpha),  # 白色
                    "radius": 5  # 从3改为4
                })

        # 绘制烟花头部
        if elapsed_time < self.rise_time:
            head_alpha = 255
            draw_commands.append({
                "type": "circle",
                "position": (int(self.current_x), int(self.current_y)),
                "color": (*self.rise_color, head_alpha),  # 白色
                "radius": 6  # 从4改为5
            })

    def _explode(self, current_time: float):
        """触发爆炸"""
        self.exploded = True
        self.explosion_start_time = current_time
        self.text_start_time = current_time

        # 创建第一次爆炸粒子（固定30个）
        particle_count = 30
        for _ in range(particle_count):
            self.explosion_particles.append(ExplosionParticleWithSecond(
                self.current_x, self.current_y
            ))

        print(f"祝福烟花爆炸: 时间={current_time:.6f}秒，产生{particle_count}个第一次爆炸粒子")

    def _update_explosion_particles(self, elapsed_time: float, draw_commands: List[Dict[str, Any]]):
        """更新爆炸粒子"""
        # 更新所有粒子
        for particle in self.explosion_particles[:]:
            particle.update()

        # 移除已死亡的粒子
        self.explosion_particles = [
            p for p in self.explosion_particles
            if p.is_alive()
        ]

        # 绘制所有存活的粒子
        for particle in self.explosion_particles:
            particle_commands = particle.get_draw_data()
            draw_commands.extend(particle_commands)

    def _update_text(self, elapsed_time: float, draw_commands: List[Dict[str, Any]]):
        """更新文字显示"""
        if elapsed_time <= self.text_show_duration:
            # 完全显示阶段
            alpha = 255
        elif elapsed_time <= self.text_duration:
            # 淡出阶段
            fade_elapsed = elapsed_time - self.text_show_duration
            fade_progress = fade_elapsed / self.text_fade_duration
            alpha = int(255 * (1.0 - fade_progress))
        else:
            alpha = 0

        if alpha > 10:
            # 创建带透明度的文本表面
            text_surface_copy = self.text_surface.copy()
            text_surface_copy.set_alpha(alpha)
            draw_commands.append({
                "type": "text_surface",
                "surface": text_surface_copy,
                "position": (self.text_x, self.text_y)
            })

    def is_finished(self) -> bool:
        """检查效果是否已完成"""
        return not self.is_active

    def get_status(self) -> Dict[str, Any]:
        """
        获取效果状态

        Returns:
            状态字典
        """
        return {
            "is_active": self.is_active,
            "exploded": self.exploded,
            "text_finished": self.text_finished,
            "start_time": self.start_time,
            "explosion_time": self.start_time + self.rise_time if not self.exploded else None,
            "rise_time": self.rise_time,
            "current_y": self.current_y
        }


"""
祝福烟花效果演示程序
"""

import pygame
import sys
import time


def main():
    """主程序入口"""

    # 初始化Pygame
    pygame.init()

    # 设置窗口参数
    screen_width = 1600
    screen_height = 900
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("祝福烟花效果演示")

    # 存储所有烟花实例的列表
    firework_instances = []

    # 第一个烟花的激活时间
    first_activation_time = 3.7963  # 在第3.7963秒激活，第5秒爆炸

    # 游戏循环变量
    clock = pygame.time.Clock()
    start_time = time.time()  # 程序开始时间
    program_running = True
    first_firework_activated = False

    print("祝福烟花效果演示程序")
    print(f"第一个烟花将在程序运行{first_activation_time:.4f}秒后激活")
    print(f"预期在第5.0000秒精确爆炸")
    print("按下空格键：立即激活新的祝福烟花")
    print("按下ESC键：退出程序")

    # 主循环
    while program_running:
        # 计算当前时间（从程序开始计算的秒数）
        current_time = time.time() - start_time

        # 检查是否到达第一个烟花的激活时间
        if not first_firework_activated and current_time >= first_activation_time:
            # 创建第一个祝福烟花实例
            new_firework = BlessingFirework(screen_width, screen_height)
            new_firework.activate(first_activation_time)
            firework_instances.append(new_firework)
            first_firework_activated = True
            print(f"第一个烟花已激活，激活时间: {current_time:.4f}秒")

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键创建并激活新的祝福烟花
                    new_firework = BlessingFirework(screen_width, screen_height)
                    new_firework.activate(current_time)
                    firework_instances.append(new_firework)
                    print(f"在 {current_time:.4f} 秒激活新祝福烟花")

        # 清除屏幕
        screen.fill((0, 0, 0))

        # 更新所有烟花实例，并收集绘制命令
        all_draw_commands = []

        # 移除已完成的烟花实例
        firework_instances = [fw for fw in firework_instances if not fw.is_finished()]

        # 更新每个烟花实例
        for firework in firework_instances:
            draw_commands = firework.update(current_time)
            if draw_commands:
                all_draw_commands.extend(draw_commands)

        # 绘制所有效果
        for command in all_draw_commands:
            if command["type"] == "circle":
                # 绘制圆形粒子
                pos = command["position"]
                color = command["color"][:3]  # 只取RGB，忽略Alpha
                radius = command["radius"]
                pygame.draw.circle(screen, color, pos, radius)
            elif command["type"] == "text_surface":
                # 绘制文字表面
                surface = command["surface"]
                pos = command["position"]
                screen.blit(surface, pos)

        # 在左上角显示当前时间（只显示数字，保留1位小数）
        time_font = pygame.font.Font(None, 72)  # 使用较大的字体
        time_text = time_font.render(f"{current_time:.1f}", True, (255, 255, 255))
        screen.blit(time_text, (20, 20))

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(60)

    # 退出程序
    pygame.quit()
    sys.exit()


# 如果这个文件被直接运行，执行主程序
if __name__ == "__main__":
    main()