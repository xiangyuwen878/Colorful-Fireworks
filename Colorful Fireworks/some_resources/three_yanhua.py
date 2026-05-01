# some_resources/three_yanhua.py
"""
三级爆炸烟花效果模块 - 支持多次激活
在指定的多个时间点激活，每个激活时间创建一个三级爆炸烟花
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

# 浅粉红色定义
LIGHT_PINK = (255, 182, 193)


class ThirdLevelParticle:
    """三级爆炸粒子 - 最小的粒子，不再爆炸"""

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y

        # 随机颜色
        self.color = random.choice(COLORS)

        # 运动参数
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(1.5, 2.5)  # 速度更慢
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.02  # 重力更小
        self.drag = 0.99  # 阻力更大

        # 随机生命周期参数
        min_life = 50  # 最小生命周期
        max_life = 150  # 最大生命周期
        self.max_life = random.randint(min_life, max_life)
        self.life = self.max_life

        # 随机渐变开始时间（生命周期的一定比例）
        fade_start_ratio = random.uniform(0.3, 0.7)  # 30%-70%时开始渐变
        self.fade_start = int(self.max_life * fade_start_ratio)

        # 随机提前死亡概率
        self.early_death_chance = random.uniform(0.0, 0.05)  # 0-5%提前死亡概率

        # 轨迹系统 - 修改：拖尾长度增加到10
        self.trail: List[Tuple[int, int]] = []
        self.max_trail_length = 10
        self.frame_count = 0

        # 粒子状态
        self.is_destroyed = False

    def update(self) -> None:
        """更新粒子状态"""
        if self.is_destroyed:
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
            if len(self.trail) > self.max_trail_length:  # 轨迹长度
                self.trail.pop(0)

        # 生命周期递减
        self.life -= 1

        # 在消失阶段，有概率提前死亡
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


class SecondLevelParticle:
    """二级爆炸粒子 - 会爆炸产生三级粒子"""

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y

        # 随机颜色
        self.color = random.choice(COLORS)

        # 运动参数
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(2.5, 3.0)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.03
        self.drag = 0.98

        # 生命周期参数
        self.life = 45  # 固定45帧（0.75秒），完全不透明
        self.max_life = self.life

        # 轨迹系统 - 修改：拖尾长度增加到12
        self.trail: List[Tuple[int, int]] = []
        self.max_trail_length = 12
        self.frame_count = 0

        # 三级爆炸相关
        self.third_exploded = False
        self.third_particles: List[ThirdLevelParticle] = []

        # 粒子状态
        self.has_started_fading = False
        self.is_destroyed = False

    def update(self) -> None:
        """更新粒子状态"""
        if self.is_destroyed:
            # 即使自身被销毁，也要更新子粒子
            self.third_particles = [p for p in self.third_particles if p.is_alive()]
            for particle in self.third_particles:
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
            if len(self.trail) > self.max_trail_length:  # 轨迹长度
                self.trail.pop(0)

        # 检查是否该进行三级爆炸
        if not self.third_exploded and self.life <= 0:
            self.third_exploded = True
            # 修改：生成三级爆炸粒子（8个）
            self.third_particles = [
                ThirdLevelParticle(self.x, self.y)
                for _ in range(8)
            ]
            # 标记自身开始消失
            self.has_started_fading = True

        # 生命周期递减
        if not self.third_exploded:
            self.life -= 1

        # 更新三级爆炸粒子
        self.third_particles = [p for p in self.third_particles if p.is_alive()]
        for particle in self.third_particles:
            particle.update()

        # 检查是否可以完全销毁
        if self.has_started_fading and len(self.third_particles) == 0:
            self.is_destroyed = True

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return not self.is_destroyed or len(self.third_particles) > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据"""
        if self.is_destroyed and len(self.third_particles) == 0:
            return []

        draw_commands = []

        # 如果自身还存活，绘制自己
        if not self.is_destroyed and self.life > 0:
            # 完全不透明
            alpha = 255

            # 绘制轨迹
            for (tx, ty) in self.trail:
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 1.5  # 修改：调细到1.5
                })

            # 绘制粒子本身
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": 1.5  # 修改：调细到1.5
            })

        # 绘制三级爆炸粒子
        for particle in self.third_particles:
            particle_commands = particle.get_draw_data()
            draw_commands.extend(particle_commands)

        return draw_commands


class FirstLevelParticle:
    """一级爆炸粒子 - 浅粉红色，会爆炸产生二级粒子"""

    def __init__(self, start_x: float, start_y: float):
        self.x = start_x
        self.y = start_y

        # 固定颜色：浅粉红色
        self.color = LIGHT_PINK

        # 运动参数
        self.angle = random.uniform(0, 2 * math.pi)
        self.speed = random.uniform(3.5, 4.5)
        self.vx = math.cos(self.angle) * self.speed
        self.vy = math.sin(self.angle) * self.speed
        self.gravity = 0.04
        self.drag = 0.975

        # 生命周期参数
        self.life = 45  # 固定45帧（0.75秒），完全不透明
        self.max_life = self.life

        # 轨迹系统 - 修改：拖尾长度增加到15
        self.trail: List[Tuple[int, int]] = []
        self.max_trail_length = 15
        self.frame_count = 0

        # 二级爆炸相关
        self.second_exploded = False
        self.second_particles: List[SecondLevelParticle] = []

        # 粒子状态
        self.has_started_fading = False
        self.is_destroyed = False

    def update(self) -> None:
        """更新粒子状态"""
        if self.is_destroyed:
            # 即使自身被销毁，也要更新子粒子
            self.second_particles = [p for p in self.second_particles if p.is_alive()]
            for particle in self.second_particles:
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
            if len(self.trail) > self.max_trail_length:  # 轨迹长度
                self.trail.pop(0)

        # 检查是否该进行二级爆炸
        if not self.second_exploded and self.life <= 0:
            self.second_exploded = True
            # 修改：生成二级爆炸粒子（10个）
            self.second_particles = [
                SecondLevelParticle(self.x, self.y)
                for _ in range(10)  # 修改：从8个改为10个
            ]
            # 标记自身开始消失
            self.has_started_fading = True

        # 生命周期递减
        if not self.second_exploded:
            self.life -= 1

        # 更新二级爆炸粒子
        self.second_particles = [p for p in self.second_particles if p.is_alive()]
        for particle in self.second_particles:
            particle.update()

        # 检查是否可以完全销毁
        if self.has_started_fading and len(self.second_particles) == 0:
            self.is_destroyed = True

    def is_alive(self) -> bool:
        """检查粒子是否存活"""
        return not self.is_destroyed or len(self.second_particles) > 0

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据"""
        if self.is_destroyed and len(self.second_particles) == 0:
            return []

        draw_commands = []

        # 如果自身还存活，绘制自己
        if not self.is_destroyed and self.life > 0:
            # 完全不透明
            alpha = 255

            # 绘制轨迹
            for (tx, ty) in self.trail:
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 3
                })

            # 绘制粒子本身
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": 3
            })

        # 绘制二级爆炸粒子
        for particle in self.second_particles:
            particle_commands = particle.get_draw_data()
            draw_commands.extend(particle_commands)

        return draw_commands


class TripleExplosionFirework:
    """三级爆炸烟花 - 单个烟花"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 从屏幕底端中央开始上升
        self.x = screen_width // 2  # 屏幕中央
        self.y = screen_height  # 从屏幕底部开始

        # 上升参数
        self.rise_speed = random.uniform(13, 13)  # 上升速度
        self.gravity = 0.12  # 上升阶段的重力
        self.rise_trail_radius = 5

        # 运动状态
        self.vy = -self.rise_speed  # 初始向上速度
        self.rise_trail: List[Tuple[int, int, int]] = []  # 上升轨迹
        self.max_rise_trail_length = 40
        self.rise_color = (255, 255, 255)  # 白色上升轨迹
        self.is_rising = True  # 是否在上升阶段

        # 爆炸参数
        self.particle_count = 12  # 修改：一级爆炸粒子数改为12

        # 爆炸粒子
        self.first_particles: List[FirstLevelParticle] = []

        # 烟花状态
        self.has_exploded = False
        self.is_destroyed = False

    def update(self) -> None:
        """更新烟花状态"""
        if self.is_destroyed:
            return

        if self.is_rising:
            # 上升阶段
            self.vy += self.gravity
            self.y += self.vy

            # 记录轨迹
            self.rise_trail.append((int(self.x), int(self.y), self.rise_trail_radius))
            if len(self.rise_trail) > self.max_rise_trail_length:
                self.rise_trail.pop(0)

            # 爆炸条件：达到合适高度或速度变为向下
            max_height = 250
            min_height = 120
            if (self.y <= max_height and self.y >= min_height) or self.vy >= 0:
                self.is_rising = False
                self.has_exploded = True
                # 生成一级爆炸粒子
                self.first_particles = [
                    FirstLevelParticle(self.x, self.y)
                    for _ in range(self.particle_count)
                ]

        else:
            # 爆炸阶段
            # 只保留还存活的粒子
            self.first_particles = [p for p in self.first_particles if p.is_alive()]
            for particle in self.first_particles:
                particle.update()

            # 检查是否可以完全销毁
            if len(self.first_particles) == 0:
                self.is_destroyed = True

    def is_alive(self) -> bool:
        """检查烟花是否存活"""
        return not self.is_destroyed

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据"""
        if self.is_destroyed:
            return []

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
            head_radius = 4
            head_alpha = 255 if len(self.rise_trail) > 5 else int(255 * len(self.rise_trail) / 5)
            if head_alpha > 10:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.rise_color, head_alpha),
                    "radius": head_radius
                })
        else:
            # 绘制所有爆炸粒子
            for particle in self.first_particles:
                particle_commands = particle.get_draw_data()
                draw_commands.extend(particle_commands)

        return draw_commands


class ThreeExplosionEffect:
    """
    三级爆炸烟花特效主类 - 支持多次激活
    可以在不同的时间点激活，每个激活时间创建一个三级爆炸烟花
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        """
        初始化烟花特效

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 烟花列表
        self.fireworks: List[TripleExplosionFirework] = []

        # 激活时间管理
        self.is_active = False
        self.activation_times = []  # 存储所有激活时间
        self.processed_times = []  # 存储已处理的激活时间

        # 控制变量
        self.duration = None
        self.end_time = 0.0

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活烟花效果

        Args:
            start_time: 开始时间（秒）
            duration: 持续时间（秒），忽略此参数，烟花自然结束
        """
        self.is_active = True

        # 记录激活时间
        if start_time not in self.activation_times:
            self.activation_times.append(start_time)
            self.activation_times.sort()  # 按时间排序

        # 设置持续时间（可选）
        self.duration = duration
        if duration is not None:
            self.end_time = start_time + duration

    def deactivate(self) -> None:
        """停用效果，不再生成新烟花"""
        self.is_active = False

    def clear_all(self) -> None:
        """立即清除所有烟花"""
        self.fireworks.clear()
        self.activation_times.clear()
        self.processed_times.clear()
        self.is_active = False

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

        # 检查是否超过持续时间
        if (self.duration is not None and
                self.is_active and
                current_time >= self.end_time):
            self.deactivate()
            return None

        # 检查是否需要创建新烟花
        for activation_time in self.activation_times:
            if (activation_time not in self.processed_times and
                    current_time >= activation_time):
                # 创建新烟花
                new_firework = TripleExplosionFirework(
                    self.screen_width,
                    self.screen_height
                )
                self.fireworks.append(new_firework)
                self.processed_times.append(activation_time)

        # 更新所有烟花
        for firework in self.fireworks:
            firework.update()

        # 清理已销毁的烟花
        self.fireworks = [fw for fw in self.fireworks if fw.is_alive()]

        # 收集所有绘制命令
        all_draw_commands = []
        for firework in self.fireworks:
            commands = firework.get_draw_data()
            if commands:
                all_draw_commands.extend(commands)

        # 检查是否所有烟花都已结束
        if (len(self.processed_times) == len(self.activation_times) and
                len(self.fireworks) == 0):
            self.is_active = False

        return all_draw_commands if all_draw_commands else None

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
            "firework_count": len(self.fireworks),
            "activation_times": self.activation_times,
            "processed_times": self.processed_times,
            "duration": self.duration
        }


"""
三级爆炸烟花效果 - 演示程序
在主程序运行时，会展示三级爆炸烟花效果
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
    pygame.display.set_caption("三级爆炸烟花效果演示")

    # 创建烟花效果实例
    firework_effect = ThreeExplosionEffect(screen_width, screen_height)

    # 只在第3秒激活一个烟花
    firework_effect.activate(3.0)

    # 游戏循环变量
    clock = pygame.time.Clock()
    start_time = time.time()  # 程序开始时间
    running = True
    font = pygame.font.Font(None, 36)  # 用于显示时间的字体

    print("三级爆炸烟花演示程序")
    print("烟花将在程序运行3秒后激活")
    print("按下空格键：触发新的烟花")
    print("按下ESC键：退出程序")

    # 主循环
    while running:
        # 计算当前时间（从程序开始计算的秒数）
        current_time = time.time() - start_time

        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # 空格键触发新的烟花
                    new_activation_time = current_time
                    firework_effect.activate(new_activation_time)
                    print(f"在 {new_activation_time:.1f} 秒触发新烟花")

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

        # 在左上角显示当前时间（秒数，保留一位小数）
        time_text = font.render(f"{current_time:.1f}s", True, (200, 200, 200))
        screen.blit(time_text, (10, 10))

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