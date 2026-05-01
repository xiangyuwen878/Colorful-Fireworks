# some_resources/ending.py
"""
结束特效模块 - 心形和圆形粒子轨迹效果
修改说明：
1. 接口与其他烟花模块保持一致
2. 返回绘制命令列表而不是直接绘制
3. 移除地面线和测试代码
4. 保持原有的视觉效果和时间控制
"""

import math
import random


class EndingEffect:
    """
    结束特效主类
    接口与其他烟花模块保持一致
    """

    def __init__(self, window_size=(1600, 900)):
        """
        初始化结束特效

        参数：
        window_size: 元组，窗口大小 (width, height)
        """
        # 窗口尺寸
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = window_size

        # 核心常量
        self.BLACK = (0, 0, 0)

        # 颜色配置
        self.HEART_PINK_COLORS = [
            (255, 228, 235),  # 极浅粉
            (255, 192, 203),  # 浅粉
            (255, 140, 186),  # 中粉
            (255, 105, 180)  # 深粉
        ]

        self.SPARK_20_COLORS = [
            (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128),
            (255, 165, 0), (255, 255, 255), (178, 34, 34), (219, 112, 147), (199, 21, 133),
            (192, 192, 192), (255, 215, 0), (255, 192, 203), (139, 69, 19), (0, 255, 255),
            (46, 139, 87), (135, 206, 250), (255, 105, 180), (255, 255, 204), (148, 0, 211)
        ]

        self.CIRCLE_COLORS = [
            (135, 206, 250),  # 淡蓝色
            (211, 211, 211)  # 银白色
        ]

        # 可调整的参数
        self.HEART_SCALE = 12.5
        self.CIRCLE_RADIUS_X = 187.5
        self.CIRCLE_RADIUS_Y = 75.0
        self.PARTICLE_ENTRY_OFFSET = 50
        self.TRAIL_LENGTH_HEART = 50
        self.TRAIL_LENGTH_CIRCLE = 25

        # 控制变量
        self.start_time = 0
        self.is_active = False
        self.duration = None
        self.end_time = 0

        # 创建粒子
        self.heart_particles = []
        self.circle_particles = []
        self._create_particles()

    def _create_particles(self):
        """创建所有粒子实例"""
        # 创建4个心形粒子
        for i in range(4):
            self.heart_particles.append(self.HeartParticle(self, i))

        # 创建4个圆形粒子
        for i in range(4):
            self.circle_particles.append(self.CircleParticle(self, i))

    def activate(self, start_time: float, duration: float = None) -> None:
        """
        激活特效

        Args:
            start_time: 开始时间（秒）
            duration: 持续时间（秒），忽略此参数，固定为10秒
        """
        self.is_active = True
        self.start_time = start_time
        self.duration = 10.0  # 固定10秒
        self.end_time = start_time + 10.0

    def deactivate(self) -> None:
        """停用特效，不再更新"""
        self.is_active = False

    def clear_all(self) -> None:
        """立即清除所有粒子"""
        self.heart_particles.clear()
        self.circle_particles.clear()
        self._create_particles()

    def update(self, current_time: float):
        """
        更新特效状态

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
            return None  # 还未开始

        # 检查是否结束
        if elapsed_time >= 10.0:
            self.is_active = False
            return None

        # 是否处于结束阶段
        is_ending_phase = elapsed_time >= 7.0

        # 更新所有粒子
        all_draw_commands = []

        for heart in self.heart_particles:
            heart.update(elapsed_time, is_ending_phase)
            heart_commands = heart.get_draw_commands()
            if heart_commands:
                all_draw_commands.extend(heart_commands)

        for circle in self.circle_particles:
            circle.update(elapsed_time, is_ending_phase)
            circle_commands = circle.get_draw_commands()
            if circle_commands:
                all_draw_commands.extend(circle_commands)

        return all_draw_commands if all_draw_commands else None

    def is_finished(self) -> bool:
        """检查特效是否已完成"""
        return not self.is_active

    def get_status(self):
        """获取特效状态"""
        return {
            "is_active": self.is_active,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "duration": self.duration
        }

    # ========== 内部类：心形粒子 ==========
    class HeartParticle:
        def __init__(self, effect, group_idx):
            self.effect = effect
            self.group_idx = group_idx
            self.color = effect.HEART_PINK_COLORS[group_idx % len(effect.HEART_PINK_COLORS)]
            self.size = 4
            self.life = 420  # 7秒 * 60FPS
            self.trail = []
            self.spark_particles = []
            self.popped_trail_pos = None

            # 心形轨迹参数
            self.angle = math.pi
            self.target_angle = 0
            self.scale = effect.HEART_SCALE

            # 心形中心位置
            self.center_x = effect.WINDOW_WIDTH // 2
            self.center_y = effect.WINDOW_HEIGHT // 4

            # 左右轮廓区分
            self.is_left = group_idx % 2 == 0
            # 运动阶段区分
            self.phase = 1 if group_idx < 2 else 2

            # 初始位置
            self.x, self.y = self.calculate_heart_position(self.angle)

            # 运动状态标记
            self.moving = False
            self.reached = False
            self.fading_out = False
            self.fade_start_time = 0
            self.reached_time = 0

        def calculate_heart_position(self, angle):
            """计算心形轨迹上的位置"""
            x = 16 * (math.sin(angle) ** 3)
            y = 13 * math.cos(angle) - 5 * math.cos(2 * angle) - 2 * math.cos(3 * angle) - math.cos(4 * angle)
            return self.center_x + x * self.scale, self.center_y - y * self.scale

        def update(self, elapsed_time, is_ending_phase=False):
            # 在结束阶段且粒子已到达顶端，开始渐出
            if is_ending_phase and self.reached and not self.fading_out:
                self.fading_out = True
                self.fade_start_time = elapsed_time

            # 渐出处理
            if self.fading_out:
                fade_duration = 1.0
                fade_progress = min(1.0, (elapsed_time - self.fade_start_time) / fade_duration)
                self.life = max(0, self.life - int(10 * fade_progress))

            # 时间分段
            phase1_end = 3.25
            phase2_end = 6.5

            # 确定当前粒子是否处于活跃运动阶段
            if self.phase == 1:
                self.moving = 0 <= elapsed_time < phase1_end
                progress = min(max(0, elapsed_time / phase1_end), 1) if self.moving else 1

                # 第一次粒子到达顶端后，在3.5秒开始渐出
                if self.reached and not self.fading_out and elapsed_time >= 3.5:
                    self.fading_out = True
                    self.fade_start_time = elapsed_time

            else:  # phase == 2
                self.moving = phase1_end <= elapsed_time < phase2_end
                progress = min(max(0, (elapsed_time - phase1_end) / (phase2_end - phase1_end)), 1) if self.moving else 1

                # 第二次粒子到达顶端后，在6.75秒开始渐出
                if self.reached and not self.fading_out and elapsed_time >= 6.75:
                    self.fading_out = True
                    self.fade_start_time = elapsed_time

            # 计算当前角度
            if self.moving and not self.reached:
                if self.is_left:
                    self.angle = math.pi - progress * math.pi
                else:
                    self.angle = math.pi + progress * math.pi
                    if self.angle > 2 * math.pi:
                        self.angle = 2 * math.pi

                # 更新位置
                self.x, self.y = self.calculate_heart_position(self.angle)

                # 检查是否到达顶部凹处
                if progress >= 1.0:
                    self.reached = True
                    self.reached_time = elapsed_time

            # 轨迹处理
            if self.moving or self.reached:
                self.trail.append((int(self.x), int(self.y)))
                if len(self.trail) > self.effect.TRAIL_LENGTH_HEART:
                    self.popped_trail_pos = self.trail.pop(0)
                    self._generate_trail_pop_sparks()
                else:
                    self.popped_trail_pos = None

            # 火花生成逻辑
            if not is_ending_phase and not self.fading_out:
                if self.moving:
                    if random.random() < 0.9:
                        for _ in range(random.randint(2, 3)):
                            self._add_normal_spark()
                elif self.reached and random.random() < 0.3:
                    self._add_normal_spark()

            # 更新火花粒子
            for spark in self.spark_particles[:]:
                spark["x"] += spark["vx"]
                spark["y"] += spark["vy"]
                spark["vy"] += 0.02
                spark["life"] -= 1
                if spark["life"] <= 0:
                    self.spark_particles.remove(spark)

            self.life -= 1

        def _add_normal_spark(self):
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(1, 4)
            angle = random.uniform(-math.pi, math.pi)
            self.spark_particles.append({
                "x": self.x, "y": self.y,
                "vx": math.cos(angle) * random.uniform(1, 1.8),
                "vy": math.sin(angle) * random.uniform(1, 1.8),
                "color": spark_color, "size": spark_size,
                "life": random.randint(18, 35),
                "is_grounded": False
            })

        def _generate_trail_pop_sparks(self):
            if not self.popped_trail_pos:
                return
            tx, ty = self.popped_trail_pos
            for _ in range(2):
                spark_color = random.choice(self.effect.SPARK_20_COLORS)
                spark_size = random.uniform(2, 5)
                angle = random.uniform(-math.pi, math.pi)
                self.spark_particles.append({
                    "x": tx, "y": ty,
                    "vx": math.cos(angle) * random.uniform(1, 2),
                    "vy": math.sin(angle) * random.uniform(1, 2),
                    "color": spark_color, "size": spark_size,
                    "life": random.randint(25, 45),
                    "is_grounded": False
                })

        def get_draw_commands(self):
            """获取绘制命令列表"""
            draw_commands = []

            # 绘制轨迹
            for i, (tx, ty) in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)) * (self.life / 420))
                if alpha <= 10:
                    continue
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 2
                })

            # 绘制粒子
            if (
                    self.moving or self.reached) and self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH and 0 <= self.y <= self.effect.WINDOW_HEIGHT:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.color, 255),  # 完全不透明
                    "radius": self.size
                })

            # 绘制火花
            for spark in self.spark_particles:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(spark["x"]), int(spark["y"])),
                    "color": (*spark["color"], 255),  # 火花完全不透明
                    "radius": int(spark["size"])
                })

            return draw_commands

    # ========== 内部类：圆形粒子 ==========
    class CircleParticle:
        def __init__(self, effect, group_idx):
            self.effect = effect
            self.group_idx = group_idx
            # 分组：0和1为上面一组，2和3为下面一组
            self.color = effect.CIRCLE_COLORS[group_idx % 2]
            self.size = 5
            self.life = 420
            self.trail = []
            self.spark_particles = []
            self.popped_trail_pos = None

            # 椭圆轨迹参数
            self.radius_x = effect.CIRCLE_RADIUS_X
            self.radius_y = effect.CIRCLE_RADIUS_Y
            self.center_x = effect.WINDOW_WIDTH // 2
            self.center_y = effect.WINDOW_HEIGHT * 3 // 4

            # 根据组别设置目标位置
            if group_idx < 2:  # 上面一组
                self.target_y = self.center_y - self.radius_y
                self.start_angle = 3 * math.pi / 2
                self.rotation_direction = -1
            else:  # 下面一组
                self.target_y = self.center_y + self.radius_y
                self.start_angle = math.pi / 2
                self.rotation_direction = 1

            # 初始位置 - 从屏幕右侧进入
            self.x = effect.WINDOW_WIDTH + effect.PARTICLE_ENTRY_OFFSET
            self.y = self.target_y

            # 组内偏移
            self.phase_offset = 0.5 if group_idx % 2 == 0 else 0

            # 阶段时间参数
            self.stage_duration = 7.0
            self.enter_duration = 1.5
            self.circle_duration = 4.0
            self.exit_duration = 1.5

        def update(self, elapsed_time, is_ending_phase=False):
            # 在结束阶段，如果粒子已经完成运动，则快速减少生命值
            if is_ending_phase and elapsed_time > self.enter_duration + self.circle_duration + self.exit_duration:
                self.life = max(0, self.life - 5)

            # 根据时间计算阶段
            if elapsed_time < self.enter_duration:
                # 阶段1：从右端→椭圆上下端点
                progress = elapsed_time / self.enter_duration
                start_x = self.effect.WINDOW_WIDTH + self.effect.PARTICLE_ENTRY_OFFSET
                end_x = self.center_x

                # 水平移动
                self.x = start_x - (start_x - end_x) * progress

                # 添加缠绕效果
                wave_offset = math.sin(progress * 10 * math.pi + self.phase_offset * math.pi) * 10
                self.y = self.target_y + wave_offset

            elif elapsed_time < self.enter_duration + self.circle_duration:
                # 阶段2：绕椭圆一周
                circle_progress = (elapsed_time - self.enter_duration) / self.circle_duration

                # 计算角度
                current_angle = self.start_angle + self.rotation_direction * circle_progress * 2 * math.pi

                # 添加缠绕效果
                phase_wave = math.sin(current_angle * 2 + self.phase_offset * math.pi) * 0.1
                current_angle += phase_wave

                # 计算椭圆轨迹上的位置
                self.x = self.center_x + math.cos(current_angle) * self.radius_x
                self.y = self.center_y + math.sin(current_angle) * self.radius_y

            else:
                # 阶段3：椭圆上下端点→左端
                exit_progress = (elapsed_time - self.enter_duration - self.circle_duration) / self.exit_duration
                start_x = self.center_x
                end_x = -self.effect.PARTICLE_ENTRY_OFFSET

                # 水平移动
                self.x = start_x - (start_x - end_x) * exit_progress

                # 添加缠绕效果
                wave_offset = math.sin(exit_progress * 10 * math.pi + self.phase_offset * math.pi) * 10
                self.y = self.target_y + wave_offset

            # 轨迹处理
            self.trail.append((int(self.x), int(self.y)))
            if len(self.trail) > self.effect.TRAIL_LENGTH_CIRCLE:
                self.popped_trail_pos = self.trail.pop(0)
                self._generate_trail_pop_sparks()
            else:
                self.popped_trail_pos = None

            # 火花生成逻辑
            if not is_ending_phase:
                if self.life > 240 and elapsed_time < self.enter_duration + self.circle_duration:
                    if random.random() < 0.9:
                        for _ in range(random.randint(2, 3)):
                            self._add_flight_spark()
                else:
                    if random.random() < 0.3:
                        self._add_flight_spark()

            # 更新火花粒子
            for spark in self.spark_particles[:]:
                if not spark["is_grounded"]:
                    spark["x"] += spark["vx"]
                    spark["y"] += spark["vy"]
                    spark["vy"] += 0.12
                spark["life"] -= 1
                if spark["life"] <= 0:
                    self.spark_particles.remove(spark)

            self.life -= 1

        def _add_flight_spark(self):
            angle_offset = random.uniform(math.pi * 0.8, math.pi * 1.2)
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(1, 4)
            self.spark_particles.append({
                "x": self.x, "y": self.y,
                "vx": math.cos(angle_offset) * random.uniform(1, 1.8),
                "vy": math.sin(angle_offset) * random.uniform(1, 1.8) + 0.3,
                "color": spark_color, "size": spark_size,
                "life": random.randint(18, 35),
                "is_grounded": False
            })

        def _generate_trail_pop_sparks(self):
            if not self.popped_trail_pos:
                return
            tx, ty = self.popped_trail_pos
            for _ in range(2):
                spark_color = random.choice(self.effect.SPARK_20_COLORS)
                spark_size = random.uniform(2, 5)
                angle = random.uniform(-math.pi, math.pi)
                self.spark_particles.append({
                    "x": tx, "y": ty,
                    "vx": math.cos(angle) * random.uniform(1, 2),
                    "vy": math.sin(angle) * random.uniform(1, 2) + 0.3,
                    "color": spark_color, "size": spark_size,
                    "life": random.randint(30, 55),
                    "is_grounded": False
                })

        def get_draw_commands(self):
            """获取绘制命令列表"""
            draw_commands = []

            # 绘制轨迹
            for i, (tx, ty) in enumerate(self.trail):
                alpha = int(255 * (i / len(self.trail)) * 0.7)
                if alpha <= 10:
                    continue
                draw_commands.append({
                    "type": "circle",
                    "position": (tx, ty),
                    "color": (*self.color, alpha),
                    "radius": 2
                })

            # 绘制粒子
            if self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(self.x), int(self.y)),
                    "color": (*self.color, 255),  # 完全不透明
                    "radius": self.size
                })

            # 绘制火花
            for spark in self.spark_particles:
                draw_commands.append({
                    "type": "circle",
                    "position": (int(spark["x"]), int(spark["y"])),
                    "color": (*spark["color"], 255),  # 火花完全不透明
                    "radius": int(spark["size"])
                })

            return draw_commands


import pygame
import sys
import os


def draw_commands_main_style(screen: pygame.Surface, commands):
    """
    绘制命令，使用主程序的绘制风格：
    - 对于圆形命令，使用pygame.draw.circle
    - 如果颜色是RGBA，只使用RGB部分（忽略Alpha）
    """
    for cmd in commands:
        if cmd.get("type") == "circle":
            x, y = cmd["position"]
            color = cmd["color"]
            # 只使用RGB部分，忽略Alpha通道
            if isinstance(color, (list, tuple)) and len(color) >= 3:
                rgb = (color[0], color[1], color[2])
            else:
                rgb = (255, 255, 255)
            radius = cmd.get("radius", 1)
            try:
                pygame.draw.circle(screen, rgb, (int(x), int(y)), int(radius))
            except Exception:
                # 防御性绘制
                pass


def main():
    # 初始化pygame
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    # 窗口设置
    screen_w, screen_h = 1600, 900
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("结束特效演示")
    clock = pygame.time.Clock()

    # 创建结束特效实例
    effect = EndingEffect((screen_w, screen_h))

    # 获取当前时间作为开始时间
    music_start = pygame.time.get_ticks()  # 毫秒
    start_time = (pygame.time.get_ticks() - music_start) / 1000.0

    # 激活特效
    effect.activate(start_time)

    # 状态变量
    running = True
    effect_finished = False

    print("结束特效演示开始")
    print("按ESC键退出")
    print("效果将持续10秒...")

    # 主循环
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_r:
                    # 按R键重置特效
                    effect.clear_all()
                    effect.activate((pygame.time.get_ticks() - music_start) / 1000.0)
                    effect_finished = False
                    print("特效已重置")

        # 计算当前时间（秒）
        current_time = (pygame.time.get_ticks() - music_start) / 1000.0

        # 更新特效
        draw_commands = effect.update(current_time)

        # 检查特效是否结束
        if effect.is_finished() and not effect_finished:
            effect_finished = True
            print(f"特效结束，持续时间: {current_time:.1f}秒")
            print("按R键重新开始，按ESC键退出")

        # 清屏
        screen.fill((0, 0, 0))  # 黑色背景

        # 绘制特效
        if draw_commands:
            draw_commands_main_style(screen, draw_commands)

        # 显示时间和状态
        font = pygame.font.Font(None, 28)

        # 显示当前时间
        time_text = f"时间: {current_time:.1f}s"
        time_surface = font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surface, (20, 20))

        # 显示特效状态
        status = "运行中" if effect.is_active else "已结束"
        status_surface = font.render(f"状态: {status}", True, (255, 255, 255))
        screen.blit(status_surface, (20, 50))

        # 显示操作提示
        tips = font.render("ESC:退出  R:重置", True, (200, 200, 200))
        screen.blit(tips, (20, screen_h - 40))

        # 更新显示
        pygame.display.flip()

        # 控制帧率
        clock.tick(60)

        # 特效结束后等待一段时间再退出
        if effect_finished and not effect.is_active:
            # 这里可以添加延时退出逻辑，但为了用户体验，我们让用户自己控制
            pass

    # 退出程序
    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()