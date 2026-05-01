# some_resources/double_yanhua.py
"""
简化版烟花效果模块
保留了轨迹、透明度、二次爆炸等核心效果，去掉了闪光效果

修改说明：
1. 一次爆炸粒子（ExplosionParticleWithSecond）：
   - 在触发二次爆炸前保持完全不透明（alpha=255）
   - 触发二次爆炸后立即消失

2. 二次爆炸粒子（FinalParticle）：
   - 前0.5秒（30帧，假设60FPS）保持完全不透明
   - 0.5秒后开始线性渐变消失
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any

# 颜色定义 - 保留原版丰富的颜色
COLORS = [
    (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255),
    (128, 0, 128), (255, 255, 255), (255, 215, 0), (255, 192, 203), (0, 255, 255),
    (0, 128, 128), (128, 255, 0), (255, 105, 180), (192, 192, 192), (255, 105, 97),
    (255, 255, 204), (135, 206, 250), (124, 252, 0), (255, 69, 0), (173, 216, 230)
]


class FinalParticle:
    """二次爆炸粒子类 - 最终散落的小粒子"""

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y
        # 随机颜色，不继承父粒子颜色
        self.color = random.choice(COLORS)
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1.5, 3.0)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.05
        self.drag = 0.98

        # 随机生命周期参数
        min_life = 30  # 最小生命周期
        max_life = 80  # 最大生命周期
        self.max_life = random.randint(min_life, max_life)
        self.life = self.max_life

        # 随机渐变开始时间（生命周期的一定比例）
        fade_start_ratio = random.uniform(0.3, 0.7)  # 30%-70%时开始渐变
        self.fade_start = int(self.max_life * fade_start_ratio)

        # 随机提前死亡概率
        self.early_death_chance = random.uniform(0.0, 0.05)  # 0-5%提前死亡概率

        self.trail: List[Tuple[int, int]] = []
        self.frame_count = 0

    def update(self) -> None:
        """更新粒子状态"""
        # 应用阻力和重力
        self.vx *= self.drag
        self.vy *= self.drag
        self.vy += self.gravity

        # 更新位置
        self.x += self.vx
        self.y += self.vy

        # 更新轨迹
        self.frame_count += 1
        if self.frame_count % 1 == 0:
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > 8:  # 轨迹长度限制
                self.trail.pop(0)

        # 生命周期递减
        self.life -= 1

        # 在消失阶段，有概率提前死亡
        if self.life <= self.fade_start and self.life > 0:
            if random.random() < self.early_death_chance:
                self.life = 0  # 标记为立即死亡
                return

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return self.life > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据 - 返回绘制命令列表"""
        draw_commands = []

        # 计算透明度
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
                "radius": 1
            })

        # 绘制粒子本身
        if alpha > 10:
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": 1
            })

        return draw_commands


class ExplosionParticleWithSecond:
    """一次爆炸粒子类（会再次爆炸）"""

    def __init__(self, start_x: float, start_y: float, random_life: int):
        self.x = start_x
        self.y = start_y
        self.explode_speed = random.uniform(2.5, 4.0)
        self.drag = 0.975
        self.color = random.choice(COLORS)

        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.explode_speed
        self.vy = math.sin(self.angle) * self.explode_speed
        self.gravity = 0.04

        # 滞留时间缩短为原来的2/3
        self.life = int(random_life * 2 / 3)
        self.max_life = self.life
        self.trail: List[Tuple[int, int]] = []
        self.frame_count = 0
        self.secondary_exploded = False  # 是否已经二次爆炸
        self.secondary_particles: List[FinalParticle] = []  # 二次爆炸产生的粒子

        # 修改2: 添加标志，标记是否已触发二次爆炸
        self.has_triggered_second = False

    def update(self) -> None:
        """更新粒子状态"""
        # 修改3: 如果已经触发了二次爆炸，就不更新这个粒子了
        if self.has_triggered_second:
            # 只更新二次爆炸粒子
            self.secondary_particles = [p for p in self.secondary_particles if p.is_alive()]
            for particle in self.secondary_particles:
                particle.update()
            return

        # 应用阻力和重力
        self.vx *= self.drag
        self.vy *= self.drag
        self.vy += self.gravity

        # 更新位置
        self.x += self.vx
        self.y += self.vy

        # 更新轨迹
        self.frame_count += 1
        if self.frame_count % 1 == 0:
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > 15:
                self.trail.pop(0)

        # 检查是否该进行二次爆炸（在生命周期的20%-30%时）
        if not self.secondary_exploded and self.life < self.max_life * 0.3:
            self.secondary_exploded = True
            self.has_triggered_second = True  # 修改4: 标记已触发二次爆炸

            # 生成二次爆炸粒子（6-10个）
            particle_count = random.randint(6, 10)
            self.secondary_particles = [
                FinalParticle(self.x, self.y)
                for _ in range(particle_count)
            ]

        # 更新二次爆炸粒子
        if self.secondary_exploded:
            self.secondary_particles = [p for p in self.secondary_particles if p.is_alive()]
            for particle in self.secondary_particles:
                particle.update()

        # 修改5: 只有没有触发二次爆炸时才减少生命
        if not self.has_triggered_second:
            self.life -= 1

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return (self.life > 0 and not self.has_triggered_second) or len(self.secondary_particles) > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据 - 返回绘制命令列表"""
        draw_commands = []

        # 修改6: 只有在生命大于0且没有触发二次爆炸时才绘制一次爆炸粒子
        if self.life > 0 and not self.has_triggered_second:
            # 绘制轨迹 - 修改7: 一次爆炸粒子保持完全不透明
            for (tx, ty) in self.trail:
                alpha = 255  # 修改8: 改为固定255
                if alpha <= 10:
                    continue
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 2
                })

            # 绘制粒子本身 - 修改9: 一次爆炸粒子保持完全不透明
            alpha = 255  # 修改10: 改为固定255
            if alpha > 10:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.color, alpha),
                    "radius": 2
                })

        # 绘制二次爆炸粒子
        for particle in self.secondary_particles:
            particle_commands = particle.get_draw_data()
            draw_commands.extend(particle_commands)

        return draw_commands


class RisingFireworkWithSecond:
    """上升烟花类"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = random.randint(50, screen_width - 50)
        self.y = screen_height

        self.rise_speed = random.uniform(12, 15)
        self.gravity = 0.15
        self.rise_trail_radius = 3

        self.vy = -self.rise_speed
        self.rise_trail: List[Tuple[int, int, int]] = []
        self.rise_color = random.choice(COLORS)
        self.is_rising = True
        self.particle_count = random.randint(12, 18)
        self.random_life = random.randint(60, 80)
        self.explosion_particles: List[ExplosionParticleWithSecond] = []

    def update(self) -> None:
        """更新烟花状态"""
        if self.is_rising:
            self.vy += self.gravity
            self.y += self.vy
            self.rise_trail.append((int(self.x), int(self.y), self.rise_trail_radius))
            max_trail = 40
            if len(self.rise_trail) > max_trail:
                self.rise_trail.pop(0)

            max_height = 180
            min_height = 100
            if (self.y <= max_height and self.y >= min_height) or self.vy >= 0:
                self.is_rising = False
                self.explosion_particles = [
                    ExplosionParticleWithSecond(self.x, self.y, self.random_life)
                    for _ in range(self.particle_count)
                ]

        else:
            # 只保留还存活的粒子（包括有二次爆炸粒子的情况）
            self.explosion_particles = [p for p in self.explosion_particles if p.is_alive()]
            for particle in self.explosion_particles:
                particle.update()

    def is_alive(self) -> bool:
        """检查烟花是否存活"""
        return self.is_rising or len(self.explosion_particles) > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据 - 返回绘制命令列表"""
        draw_commands = []

        if self.is_rising:
            # 绘制上升轨迹
            for i, (tx, ty, radius) in enumerate(self.rise_trail):
                trail_alpha = int(255 * (i / len(self.rise_trail)))
                if trail_alpha <= 10:
                    continue
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.rise_color, trail_alpha),
                    "radius": radius
                })

            # 绘制头部粒子
            head_radius = 3
            head_alpha = 255 if len(self.rise_trail) > 5 else int(255 * len(self.rise_trail) / 5)
            if head_alpha > 10:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.rise_color, head_alpha),
                    "radius": head_radius
                })
        else:
            # 绘制爆炸粒子
            for particle in self.explosion_particles:
                particle_commands = particle.get_draw_data()
                draw_commands.extend(particle_commands)

        return draw_commands


class FireworksWithSecondExplosionEffect:
    """
    带二次爆炸的烟花特效主类
    提供简单的调用接口
    """

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """
        初始化烟花特效

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fireworks: List[RisingFireworkWithSecond] = []
        self.spawn_timer = 0
        self.spawn_interval = random.randint(20, 40)
        self.is_active = False
        self.start_time = 0.0
        self.duration = None  # 持续时间，None表示无限
        self.end_time = 0.0
        self.max_fireworks = 12  # 最大同时存在的烟花数量

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活烟花效果

        Args:
            start_time: 开始时间（秒）
            duration: 持续时间（秒），None表示无限直到手动停止
        """
        self.is_active = True
        self.start_time = start_time
        self.duration = duration
        if duration is not None:
            self.end_time = start_time + duration
        self.fireworks = []
        self.spawn_timer = 0

    def deactivate(self) -> None:
        """停用效果，不再生成新烟花，但现有烟花会继续播放"""
        self.is_active = False

    def clear_all(self) -> None:
        """立即清除所有烟花"""
        self.fireworks.clear()

    def update(self, current_time: float) -> Optional[List[Dict[str, Any]]]:
        """
        更新效果状态

        Args:
            current_time: 当前时间（秒）

        Returns:
            绘制命令列表，如果没有任何绘制命令则返回None
        """
        # 检查是否超过持续时间
        if (self.duration is not None and
                self.is_active and
                current_time >= self.end_time):
            self.deactivate()

        # 生成新烟花
        if self.is_active:
            self.spawn_timer += 1
            if (self.spawn_timer >= self.spawn_interval and
                    len(self.fireworks) < self.max_fireworks):
                self.fireworks.append(RisingFireworkWithSecond(
                    self.screen_width, self.screen_height
                ))
                self.spawn_timer = 0
                self.spawn_interval = random.randint(20, 40)

        # 更新烟花
        self.fireworks = [fw for fw in self.fireworks if fw.is_alive()]
        for firework in self.fireworks:
            firework.update()

        # 收集绘制命令
        all_draw_commands = []
        for firework in self.fireworks:
            commands = firework.get_draw_data()
            all_draw_commands.extend(commands)

        return all_draw_commands if all_draw_commands else None

    def is_finished(self) -> bool:
        """
        检查效果是否完全结束（无存活烟花且已停用）

        Returns:
            是否完全结束
        """
        return not self.is_active and len(self.fireworks) == 0

    def get_status(self) -> Dict[str, Any]:
        """
        获取效果状态

        Returns:
            状态字典
        """
        return {
            "is_active": self.is_active,
            "firework_count": len(self.fireworks),
            "alive_fireworks": sum(1 for fw in self.fireworks if fw.is_alive()),
            "start_time": self.start_time,
            "end_time": self.end_time if self.duration else None,
            "duration": self.duration
        }


"""
简化版烟花效果演示程序
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
    pygame.display.set_caption("简化版烟花效果演示")

    # 创建烟花效果实例
    firework_effect = FireworksWithSecondExplosionEffect(screen_width, screen_height)

    # 游戏循环变量
    clock = pygame.time.Clock()
    start_time = time.time()  # 程序开始时间
    program_running = True
    firework_active = False
    program_exit_time = 17.0  # 程序在第17秒自动关闭

    print("简化版烟花效果演示程序")
    print("烟花将在程序运行3秒后激活")
    print("烟花持续10秒，程序在第17秒自动关闭")
    print("按下ESC键可提前退出程序")

    # 主循环
    while program_running:
        # 计算当前时间（从程序开始计算的秒数）
        current_time = time.time() - start_time

        # 检查是否到达烟花激活时间（第3秒）
        if not firework_active and current_time >= 3.0:
            firework_effect.activate(3.0, 10.0)  # 在第3秒激活，持续10秒
            firework_active = True
            print(f"烟花已激活，将在第13秒结束")

        # 检查是否到达程序退出时间（第17秒）
        if current_time >= program_exit_time:
            print(f"程序运行{current_time:.1f}秒，自动退出")
            program_running = False
            break

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                program_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    program_running = False

        # 清除屏幕
        screen.fill((0, 0, 0))

        # 更新烟花效果
        draw_commands = firework_effect.update(current_time)

        # 如果有绘制命令，绘制所有烟花效果
        if draw_commands:
            for command in draw_commands:
                if command["type"] == "circle":
                    # 绘制圆形粒子
                    pos = command["position"]
                    color = command["color"][:3]  # 只取RGB，忽略Alpha
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, pos, radius)

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