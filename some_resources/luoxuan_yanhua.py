# some_resources/luoxuan_yanhua.py
"""
螺旋烟花效果模块 - 重构版
添加了控制接口，与其他烟花模块保持一致的接口
"""

import math
import random
from typing import List, Tuple, Optional, Dict, Any


class SpiralFireworkParticle:
    """螺旋烟花粒子类"""

    def __init__(self, screen_width: int, screen_height: int, colors: List[Tuple[int, int, int]]):
        """
        初始化螺旋烟花粒子

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
            colors: 颜色数组
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.colors = colors

        # 初始位置（屏幕底部）
        self.x = random.randint(50, self.screen_width - 50)
        self.y = self.screen_height

        # 运动参数 - 修改这些参数
        self.rise_speed = random.uniform(6.0, 7.5)  # 增加初始上升速度
        self.gravity = 0.002  # 减小重力影响
        self.angle = 0
        self.angle_speed = random.uniform(0.08, 0.15)
        self.spiral_radius = random.uniform(1.5, 3.0)  # 稍微增加螺旋半径

        # 外观参数
        self.size = random.choices([3, 4], weights=[7, 3])[0]
        self.color = random.choice(self.colors)
        self.active = True

        # 轨迹参数
        self.trail_points = []  # 存储(位置x, 位置y, 方向x, 方向y)
        self.max_trail_length = random.randint(6, 10)
        self.trail_spread = random.uniform(1.0, 1.5)

        # 生命周期
        self.life = 300  # 增加到5秒（60FPS），确保有足够时间到达顶端
        self.max_life = self.life

    def update(self) -> None:
        """更新粒子状态"""
        if not self.active:
            return

        # 更新位置
        self.y -= self.rise_speed
        self.rise_speed = max(3.0, self.rise_speed - self.gravity)  # 提高最小速度限制

        # 螺旋运动
        self.angle += self.angle_speed
        self.x += math.cos(self.angle) * self.spiral_radius

        # 计算运动方向向量
        dir_x = math.cos(self.angle) * self.spiral_radius
        dir_y = -self.rise_speed
        length = math.sqrt(dir_x ** 2 + dir_y ** 2)
        if length > 0:
            dir_x /= length
            dir_y /= length

        # 存储位置和方向
        self.trail_points.append((self.x, self.y, dir_x, dir_y))

        # 限制轨迹长度
        if len(self.trail_points) > self.max_trail_length:
            self.trail_points.pop(0)

        # 生命周期减少
        self.life -= 1

        # 消失条件 - 只检查生命周期
        if self.life <= 0:
            self.active = False

    def alive(self) -> bool:
        """兼容性方法，返回active状态"""
        return self.active

    def get_draw_data(self) -> List[Dict[str, Any]]:
        """获取绘制数据 - 返回绘制命令列表"""
        draw_commands = []

        total_points = len(self.trail_points)
        if total_points < 2:
            return draw_commands

        # 绘制圆锥尾巴
        for i in range(total_points):
            tx, ty, dir_x, dir_y = self.trail_points[i]

            # 计算透明度（线性渐变）
            # 头部不透明，尾部逐渐透明
            alpha_ratio = i / (total_points - 1)
            alpha = int(255 * (0.5 + 0.5 * alpha_ratio))

            if alpha < 10:
                continue

            # 计算尺寸
            trail_size = max(1, int(self.size * alpha_ratio))

            # 垂直偏移方向
            perpendicular_x = -dir_y
            perpendicular_y = dir_x

            # 扩散范围
            spread = self.trail_spread * alpha_ratio

            # 绘制主轨迹点
            color_with_alpha = (*self.color, alpha)
            draw_commands.append({
                "type": "circle",
                "position": (int(tx), int(ty)),
                "color": color_with_alpha,
                "radius": trail_size
            })

            # 绘制两侧扩散点（如果有足够透明度）
            side_alpha = int(alpha * 0.7)
            if side_alpha > 10:
                # 左侧点
                left_x = tx + perpendicular_x * spread
                left_y = ty + perpendicular_y * spread
                draw_commands.append({
                    "type": "circle",
                    "position": (int(left_x), int(left_y)),
                    "color": (*self.color, side_alpha),
                    "radius": max(1, trail_size - 1)
                })

                # 右侧点
                right_x = tx - perpendicular_x * spread
                right_y = ty - perpendicular_y * spread
                draw_commands.append({
                    "type": "circle",
                    "position": (int(right_x), int(right_y)),
                    "color": (*self.color, side_alpha),
                    "radius": max(1, trail_size - 1)
                })

        # 绘制烟花头部（如果粒子还活着）
        if self.active and self.life > 0:
            # 头部完全不透明
            head_alpha = 255
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, head_alpha),
                "radius": self.size
            })

        return draw_commands


class SpiralFireworkEffect:
    """
    螺旋烟花特效主类
    提供与其他烟花模块一致的接口
    """

    def __init__(self, screen_width: int = 800, screen_height: int = 600, max_fireworks: int = 10):
        """
        初始化螺旋烟花效果

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
            max_fireworks: 最大同时存在的烟花数量
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.max_fireworks = max_fireworks

        # 烟花数组
        self.fireworks: List[SpiralFireworkParticle] = []

        # 颜色数组
        self.COLORS = [
            (255, 0, 0), (255, 165, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255),
            (128, 0, 128), (255, 255, 255), (255, 215, 0), (255, 192, 203), (0, 255, 255),
            (0, 128, 128), (128, 255, 0), (255, 105, 180), (192, 192, 192), (255, 105, 97),
            (255, 255, 204), (135, 206, 250), (124, 252, 0), (255, 69, 0), (173, 216, 230)
        ]

        # 控制参数
        self.spawn_timer = 0
        self.spawn_interval = random.randint(30, 45)  # 生成间隔（帧数）
        self.is_active = False

        # 时间控制
        self.start_time = 0.0
        self.duration = None
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

        # 重置生成计时器
        self.spawn_timer = 0

        # 不清除现有烟花，允许自然消失

    def deactivate(self) -> None:
        """停用效果，不再生成新烟花，现有烟花继续播放"""
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
        try:
            # 检查是否超过持续时间
            if (self.duration is not None and
                    self.is_active and
                    current_time >= self.end_time):
                self.deactivate()

            # 生成新烟花
            if self.is_active and len(self.fireworks) < self.max_fireworks:
                self.spawn_timer += 1
                if self.spawn_timer >= self.spawn_interval:
                    self.fireworks.append(SpiralFireworkParticle(
                        self.screen_width, self.screen_height, self.COLORS
                    ))
                    self.spawn_timer = 0
                    self.spawn_interval = random.randint(30, 45)

            # 更新所有烟花
            self.fireworks = [fw for fw in self.fireworks if fw.alive()]
            for firework in self.fireworks:
                firework.update()

            # 收集所有绘制命令
            all_draw_commands = []
            for firework in self.fireworks:
                commands = firework.get_draw_data()
                all_draw_commands.extend(commands)

            return all_draw_commands if all_draw_commands else None

        except Exception as e:
            # 调试：打印异常信息
            import traceback
            print(f"烟花效果更新异常: {e}")
            traceback.print_exc()
            return None

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
            "alive_fireworks": sum(1 for fw in self.fireworks if fw.alive()),
            "start_time": self.start_time,
            "end_time": self.end_time if self.duration else None,
            "duration": self.duration,
            "max_fireworks": self.max_fireworks
        }


import pygame
import sys
import time


def main():
    """主程序入口"""
    # 初始化pygame
    pygame.init()

    # 设置窗口参数
    SCREEN_WIDTH = 1600
    SCREEN_HEIGHT = 900
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("螺旋烟花效果")

    # 创建时钟对象
    clock = pygame.time.Clock()
    FPS = 60

    # 创建螺旋烟花效果实例
    firework_effect = SpiralFireworkEffect(SCREEN_WIDTH, SCREEN_HEIGHT, max_fireworks = 15)

    # 记录程序开始时间
    program_start_time = time.time()

    # 控制变量
    running = True
    effect_started = False
    effect_ended = False
    shutdown_timer = None

    # 字体设置
    font = pygame.font.Font(None, 36)  # 使用默认字体

    # 主循环
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # 计算当前运行时间
        current_time = time.time() - program_start_time

        # 控制烟花效果的启动和停止
        if not effect_started and current_time >= 3.0:
            # 在第3秒启动烟花效果，持续10秒
            firework_effect.activate(current_time, duration=10.0)
            effect_started = True

        # 检查效果是否已结束
        if effect_started and not effect_ended and current_time >= 13.0:
            effect_ended = True
            firework_effect.deactivate()
            shutdown_timer = current_time  # 记录结束时间

        # 在效果结束后等待2秒关闭程序
        if shutdown_timer and (current_time - shutdown_timer) >= 2.0:
            running = False

        # 清屏
        screen.fill((0, 0, 0))

        # 更新烟花效果
        draw_commands = firework_effect.update(current_time)

        # 如果有绘制命令，绘制烟花
        if draw_commands:
            for command in draw_commands:
                if command["type"] == "circle":
                    pos = command["position"]
                    color = command["color"]
                    radius = command["radius"]

                    # 创建一个表面来绘制带透明度的圆
                    circle_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                    pygame.draw.circle(circle_surface, color, (radius, radius), radius)
                    screen.blit(circle_surface, (pos[0] - radius, pos[1] - radius))

        # 只在左上角显示时间（不显示"时间"文字）
        time_text = f"{current_time:.2f}"
        time_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surface, (10, 10))

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(FPS)

    # 退出pygame
    pygame.quit()
    sys.exit()


# 程序入口
if __name__ == "__main__":
    main()