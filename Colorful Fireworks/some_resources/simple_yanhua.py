# some_resources/simple_yanhua.py
"""
简化版烟花效果模块
修改为一次爆炸效果，不进行二次爆炸
修改为：一次爆炸粒子先保持1秒不透明，然后在0.5秒内渐变消失
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any

# 颜色定义 - 20种预定义颜色
COLORS = [
    (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255),
    (128, 0, 128), (255, 255, 255), (255, 215, 0), (255, 192, 203), (0, 255, 255),
    (0, 128, 128), (128, 255, 0), (255, 105, 180), (192, 192, 192), (255, 105, 97),
    (255, 255, 204), (135, 206, 250), (124, 252, 0), (255, 69, 0), (173, 216, 230)
]


class ExplosionParticle:
    """
    一次爆炸粒子类（不再有二次爆炸）
    修改为：先保持随机时间不透明，然后在一定时间内渐变消失
    """

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y

        # 运动参数
        self.explode_speed = random.uniform(3.0, 4.0)  # 爆炸速度
        self.drag = 0.98  # 阻力系数
        self.color = random.choice(COLORS)  # 随机颜色

        # 初始速度和方向
        self.angle = random.uniform(0, 2 * math.pi)
        self.vx = math.cos(self.angle) * self.explode_speed
        self.vy = math.sin(self.angle) * self.explode_speed
        self.gravity = 0.035  # 重力加速度

        # 随机生命周期参数
        # 总生命周期随机：60-100帧
        self.total_life = random.randint(60, 100)

        # 随机渐变开始时间：生命周期的40%-80%之间
        fade_start_ratio = random.uniform(0.4, 0.8)  # 50%-80%
        self.fade_start = int(self.total_life * fade_start_ratio)

        # 当前生命周期
        self.life = self.total_life
        self.max_life = self.total_life

        # 轨迹系统
        self.trail: List[Tuple[int, int]] = []
        self.frame_count = 0

    # update方法保持不变
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
            if len(self.trail) > 15:  # 保留最近15个位置
                self.trail.pop(0)

        # 生命周期递减
        self.life -= 1

    # is_alive方法保持不变
    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return self.life > 0

    # get_draw_data方法保持不变（它会自动使用新的fade_start值）
    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据 - 返回绘制命令列表"""
        draw_commands = []

        # 计算透明度
        if self.life > self.fade_start:
            # 不透明阶段：前阶段，透明度为255
            alpha = 255
        else:
            # 渐变阶段：后阶段，线性渐变
            # 剩余生命在渐变阶段中的比例
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
                "radius": 2
            })

        # 绘制粒子本身
        if alpha > 10:
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": 2
            })

        return draw_commands


class RisingFirework:
    """
    上升烟花类
    负责从屏幕底部上升到爆炸高度，然后爆炸
    """

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 起始位置
        self.x = random.randint(50, screen_width - 50)  # 随机水平位置
        self.y = screen_height  # 从屏幕底部开始

        # 上升参数
        self.rise_speed = random.uniform(12, 15)  # 上升速度
        self.gravity = 0.15  # 上升阶段的重力
        self.rise_trail_radius = 3  # 上升轨迹点的大小

        # 运动状态
        self.vy = -self.rise_speed  # 初始向上速度
        self.rise_trail: List[Tuple[int, int, int]] = []  # 上升轨迹
        self.rise_color = random.choice(COLORS)  # 上升颜色
        self.is_rising = True  # 是否在上升阶段

        # 爆炸参数
        self.particle_count = random.randint(15, 18)  # 一次爆炸粒子数

        # 爆炸粒子
        self.explosion_particles: List[ExplosionParticle] = []

    def update(self) -> None:
        """更新烟花状态"""
        if self.is_rising:
            # 上升阶段
            self.vy += self.gravity  # 重力使上升减速
            self.y += self.vy  # 更新垂直位置

            # 记录轨迹
            self.rise_trail.append((int(self.x), int(self.y), self.rise_trail_radius))
            max_trail = 40
            if len(self.rise_trail) > max_trail:
                self.rise_trail.pop(0)

            # 爆炸条件：达到合适高度或速度变为向下
            max_height = 300
            min_height = 150
            if (self.y <= max_height and self.y >= min_height) or self.vy >= 0:
                self.is_rising = False
                # 生成一次爆炸粒子
                self.explosion_particles = [
                    ExplosionParticle(self.x, self.y)
                    for _ in range(self.particle_count)
                ]

        else:
            # 爆炸阶段
            # 只保留还存活的粒子
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
                # 轨迹透明度：后面的轨迹更淡
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
            # 刚开始上升时头部会淡入
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


class FireworksEffect:
    """
    烟花特效主类（不再有二次爆炸）
    提供简单的调用接口

    使用示例：
    effect = FireworksEffect(800, 600)
    effect.activate(0, 10)  # 立即开始，持续10秒

    在主循环中：
    while True:
        commands = effect.update(current_time)
        for cmd in commands:
            # 绘制命令
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
        self.fireworks: List[RisingFirework] = []

        # 烟花生成控制
        self.spawn_timer = 0
        self.spawn_interval = random.randint(20, 40)  # 生成间隔（30-60帧）
        self.is_active = False  # 是否激活
        self.max_fireworks = 12  # 最大同时存在的烟花数量

        # 时间控制
        self.start_time = 0.0
        self.duration = None  # 持续时间，None表示无限
        self.end_time = 0.0

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
                self.fireworks.append(RisingFirework(
                    self.screen_width, self.screen_height
                ))
                self.spawn_timer = 0
                self.spawn_interval = random.randint(20, 40)

        # 更新所有烟花
        self.fireworks = [fw for fw in self.fireworks if fw.is_alive()]
        for firework in self.fireworks:
            firework.update()

        # 收集所有绘制命令
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


# 如果这个文件被直接运行，执行主程序
if __name__ == "__main__":
    def main():
        import pygame
        import sys
        import time

        # 初始化pygame
        pygame.init()

        # 屏幕设置
        SCREEN_WIDTH = 1600
        SCREEN_HEIGHT = 900
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("烟花效果测试")

        # 创建时钟
        clock = pygame.time.Clock()
        FPS = 60

        # 创建烟花效果实例
        fireworks = FireworksEffect(SCREEN_WIDTH, SCREEN_HEIGHT)

        # 启动时间
        start_time = time.time()

        # 与主工程代码保持一致：先立即开始，持续10秒
        fireworks.activate(start_time, 10.0)

        # 字体设置
        font = pygame.font.SysFont(None, 36)

        # 主循环
        running = True
        while running:
            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False

            # 清屏 - 黑色背景
            screen.fill((0, 0, 0))

            # 更新烟花效果
            current_time = time.time()
            draw_commands = fireworks.update(current_time)

            # 绘制烟花
            if draw_commands:
                for cmd in draw_commands:
                    if cmd["type"] == "circle":
                        x, y = cmd["position"]
                        color = cmd["color"]
                        radius = cmd["radius"]

                        # 处理带透明度的绘制
                        if len(color) == 4:
                            r, g, b, a = color
                            # 创建一个临时surface来绘制带透明度的圆
                            temp_surface = pygame.Surface((radius * 2 + 2, radius * 2 + 2), pygame.SRCALPHA)
                            pygame.draw.circle(temp_surface, (r, g, b, a), (radius + 1, radius + 1), radius)
                            screen.blit(temp_surface, (x - radius - 1, y - radius - 1))
                        else:
                            pygame.draw.circle(screen, color, (x, y), radius)

            # 左上角显示运行时间（只显示数字）
            elapsed_time = current_time - start_time
            time_text = f"{elapsed_time:.1f}"
            time_surface = font.render(time_text, True, (200, 200, 200))
            screen.blit(time_surface, (20, 20))

            # 更新显示
            pygame.display.flip()

            # 控制帧率
            clock.tick(FPS)

        # 退出pygame
        pygame.quit()
        sys.exit()


    main()