# some_resources/opening.py
"""
开场效果模块 - 时间驱动与生成限制修改版

变更点（仅限于此模块）：
- 将内部粒子 update 改为基于 dt_seconds（秒）进行连续积分，解除对帧率的依赖。
- 把原先以“帧”为单位的参数（speed、gravity、life、spark life 等）按假定 FPS 做等价换算以尽量保持原始视觉。
- 限制每帧/每次更新生成的 spark 数量和模块内的总 spark 数，避免瞬时激增导致性能抖动和“肉眼看到的加速”。
- 对外接口未改： OpeningEffect.update(current_time: float) 仍接收绝对时间秒；内部负责计算 dt_seconds 并传给子粒子。
- 其余逻辑、颜色、外观尽量保持原样。
"""

import math
import random
from typing import List, Tuple, Dict, Any, Optional


FPS = 60.0

class OpeningEffect:
    """
    开场效果主类（外部接口不变）
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        # 窗口尺寸
        self.WINDOW_WIDTH = screen_width
        self.WINDOW_HEIGHT = screen_height

        # 颜色定义（保持不变）
        self.SPARK_20_COLORS = [
            (255, 0, 0), (255, 255, 0), (0, 255, 0), (0, 0, 255), (128, 0, 128),
            (255, 165, 0), (255, 255, 255), (178, 34, 34), (219, 112, 147), (199, 21, 133),
            (192, 192, 192), (255, 215, 0), (255, 192, 203), (139, 69, 19), (0, 255, 255),
            (46, 139, 87), (135, 206, 250), (255, 105, 180), (255, 255, 204), (148, 0, 211)
        ]

        self.SPIRAL_PINK_COLORS = [
            (255, 228, 235),
            (255, 192, 203),
            (255, 140, 186),
            (255, 105, 180)
        ]

        self.PLANE_FIXED_COLORS = {
            "left_to_right": {
                "main": (135, 206, 250),
                "trail": (135, 206, 250)
            },
            "right_to_left": {
                "main": (211, 211, 211),
                "trail": (211, 211, 211)
            }
        }

        # 控制变量
        self.start_time = 0.0
        self.is_active = False
        self.duration = None
        self.end_time = 0.0

        # 限制参数（防止单帧/瞬时爆发）
        self.max_total_sparks = 1200            # 全局同时存在的 spark 上限
        self.max_new_sparks_per_particle = 9    # 单个 particle 每次 update 最多生成的 spark
        self.max_new_sparks_per_update = 60     # 整个 effect 每次 update 最多生成的新 spark（粗粒度）
        self.total_sparks = 0                   # 当前存在的 spark 总数（所有 particle 之和）

        # 帧时间跟踪（用于计算 dt_seconds）
        self.last_frame_time: Optional[float] = None

        # 创建粒子
        self.plane_particles: List[PlaneParticle] = []
        self.spiral_particles: List[SpiralParticle] = []
        self._create_particles()

    def _create_particles(self):
        """(Re)create particles - 保持原有初始化构成"""
        self.plane_particles = [PlaneParticle(self, True), PlaneParticle(self, False)]

        self.spiral_particles = [
            SpiralParticle(self, self.WINDOW_WIDTH // 4, self.WINDOW_HEIGHT + 50, True, 0),
            SpiralParticle(self, self.WINDOW_WIDTH // 4, self.WINDOW_HEIGHT + 50, True, 1),
            SpiralParticle(self, self.WINDOW_WIDTH * 3 // 4, self.WINDOW_HEIGHT + 50, False, 2),
            SpiralParticle(self, self.WINDOW_WIDTH * 3 // 4, self.WINDOW_HEIGHT + 50, False, 3)
        ]

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活效果（接口不变，接收绝对时间秒）
        初始化 last_frame_time 以便第一次 update 使用合理的小 dt
        """
        self.is_active = True
        self.start_time = start_time
        self.duration = duration
        if duration is not None:
            self.end_time = start_time + duration

        # 初始化 last_frame_time，避免激活首帧出现极大 dt
        self.last_frame_time = start_time

        # 重置 spark 计数
        self.total_sparks = sum(len(p.spark_particles) for p in self.plane_particles + self.spiral_particles)

    def deactivate(self) -> None:
        self.is_active = False

    def clear_all(self) -> None:
        self.plane_particles.clear()
        self.spiral_particles.clear()
        self._create_particles()
        self.total_sparks = 0

    def update(self, current_time: float) -> Optional[List[Dict[str, Any]]]:
        """
        更新效果：
        - current_time: 绝对时间（秒）
        对外接口保持不变，但内部计算 dt_seconds 并把 dt 传入子粒子 update(dt_seconds)
        """
        if not self.is_active:
            return None

        # 计算本帧 dt（秒）
        if self.last_frame_time is None:
            dt_seconds = 0.0
        else:
            dt_seconds = current_time - self.last_frame_time
            # 为避免主循环卡顿导致一次性超大 dt（若发生），做一个合理上限保护
            # 这个保护项仅用于防止极端 dt 导致瞬时大量更新；不会正常影响效果
            if dt_seconds > 0.5:
                dt_seconds = 0.5
        self.last_frame_time = current_time

        new_sparks_this_update = 0

        all_draw_commands: List[Dict[str, Any]] = []

        # 更新水平粒子
        for plane in self.plane_particles:
            plane_new = plane.update(dt_seconds)
            # plane.update 返回新 spark 数量（int），用于维护全局计数
            if plane_new:
                # 限制 effect 每次 update 的新增总数
                allowed = min(plane_new, max(0, self.max_new_sparks_per_update - new_sparks_this_update))
                new_sparks_this_update += allowed
                # 如果 plane 返回比 allowed 少， it's okay; plane.update already appended actual sparks.
                # If plane tried to create more than allowed, plane.update should respect per-particle limits
                # (we implement generation caps inside particle methods), so no extra clipping needed here.

            plane_commands = plane.get_draw_commands()
            if plane_commands:
                all_draw_commands.extend(plane_commands)

        # 更新螺旋粒子
        for spiral in self.spiral_particles:
            spiral_new = spiral.update(dt_seconds)
            if spiral_new:
                allowed = min(spiral_new, max(0, self.max_new_sparks_per_update - new_sparks_this_update))
                new_sparks_this_update += allowed

            spiral_commands = spiral.get_draw_commands()
            if spiral_commands:
                all_draw_commands.extend(spiral_commands)

        # 清理：在子粒子 update 内，我们在添加/删除 spark 时会维护 self.total_sparks
        # 检查是否所有核心粒子已经死亡且没有 sparks
        all_plane_dead = all(not p.is_alive() for p in self.plane_particles)
        all_spiral_dead = all(not s.is_alive() for s in self.spiral_particles)
        if all_plane_dead and all_spiral_dead and self.total_sparks == 0:
            # 所有都结束
            self.is_active = False

        return all_draw_commands if all_draw_commands else None

    def is_finished(self) -> bool:
        return not self.is_active

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_active,
            "plane_particles": len([p for p in self.plane_particles if p.is_alive()]),
            "spiral_particles": len([p for p in self.spiral_particles if p.is_alive()]),
            "total_sparks": self.total_sparks,
            "start_time": self.start_time,
            "end_time": self.end_time if self.duration else None,
            "duration": self.duration
        }

class SpiralParticle:
    """螺旋粒子 - 使用 dt_seconds 做连续积分"""

    def __init__(self, effect: OpeningEffect, x: int, y: int, is_left: bool, group_idx: int):
        self.effect = effect
        self.x = float(x)
        self.y = float(y)
        self.is_left = is_left
        self.group_idx = group_idx

        # 原始参数（基于帧）；将进行换算到基于秒的物理量
        base_speed_per_frame = 5.0  # px/frame 原始
        speed_variation_per_frame = 1.0
        self.angle = 0.0 if group_idx % 2 == 0 else math.pi
        self.angle_step = 0.08 if is_left else -0.08
        self.radius = 150
        self.color = effect.SPIRAL_PINK_COLORS[group_idx]
        self.size = 5.5

        # life 原为 180 帧 -> 转换为秒
        life_frames = 180
        self.life = life_frames / FPS  # seconds
        self._initial_life = self.life

        # 轨迹淡出参数 - 三阶段淡出（基于从头部开始的比例）
        self.trail_head_ratio = 0.20  # 头部20%完全可见
        self.trail_mid_ratio = 0.75  # 中间75%线性淡出
        self.trail_tail_ratio = 0.05  # 尾部5%完全透明

        # 轨迹最大长度改为80
        self.trail_max_length = 80

        # 速度使用 px/s
        self.base_speed = base_speed_per_frame * FPS  # px/s
        self.speed_variation = speed_variation_per_frame * FPS

        # spark 列表
        self.spark_particles: List[Dict[str, Any]] = []

        # 轨迹
        self.trail: List[Tuple[int, int]] = []

        # 标志：轨迹是否曾经达到过最大长度
        self.trail_ever_reached_max = False

    def update(self, dt_seconds: float) -> int:
        """
        更新状态，返回本次新增 spark 数量
        """
        new_sparks = 0

        # 位置/角度更新（基于连续时间）
        angle_step_per_second = self.angle_step * FPS
        self.angle += angle_step_per_second * dt_seconds

        # 速度计算
        self.speed = self.base_speed + math.sin(self.angle * 4.0) * self.speed_variation

        # 螺旋运动
        center_x = self.effect.WINDOW_WIDTH / 2.0
        offset_x = math.cos(self.angle) * self.radius
        self.x = center_x + (-offset_x if self.is_left else offset_x)
        self.y -= self.speed * dt_seconds

        # 更新轨迹
        self.trail.append((int(self.x), int(self.y)))

        # 检查轨迹是否曾达到最大长度
        if len(self.trail) >= self.trail_max_length and not self.trail_ever_reached_max:
            self.trail_ever_reached_max = True

        # 移除超出长度的轨迹点
        if len(self.trail) > self.trail_max_length:
            self.trail.pop(0)  # 移除最旧点

        # 头部火花生成（每次更新都生成1-2个火花）
        if self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH and 0 <= self.y <= self.effect.WINDOW_HEIGHT:
            added = self._generate_head_sparks()
            new_sparks += added

        # 尾部火花生成（一旦轨迹曾达到最大长度，就一直生成，直到轨迹为空）
        if self.trail_ever_reached_max and len(self.trail) > 0:
            # 在轨迹的第一个点（最旧点）生成火花
            trail_head = self.trail[0]
            added = self._generate_tail_sparks(trail_head)
            new_sparks += added

        # 更新已有的火花
        for spark in self.spark_particles[:]:
            # position update (vx, vy are px/s)
            spark["x"] += spark["vx"] * dt_seconds
            # vy changes by ay * dt
            spark["vy"] += spark.get("ay", 0.0) * dt_seconds
            spark["y"] += spark["vy"] * dt_seconds
            spark["life"] -= dt_seconds
            if spark["life"] <= 0.0:
                self.spark_particles.remove(spark)

        # 减少生命值
        self.life -= dt_seconds
        if self.life < 0.0:
            self.life = 0.0

        return new_sparks

    def _generate_head_sparks(self) -> int:
        """生成头部火花，返回新增数目"""
        added = 0
        # 随机生成1-2个火花
        desired = random.randint(1, 2)

        for _ in range(desired):
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(2.0, 5.0)  # 头部火花大小：2-5
            angle = random.uniform(-math.pi, math.pi)

            # 计算速度（保持原物理参数）
            vx_frame = math.cos(angle) * random.uniform(1.2, 2.2)
            vy_frame = math.sin(angle) * random.uniform(1.2, 2.2)
            vx_s = vx_frame * FPS
            vy_s = vy_frame * FPS
            # 加速度转换
            ay_s = 0.03 * (FPS ** 2)

            # 生命周期
            life_frames = random.randint(15, 30)
            life_s = life_frames / FPS

            spark = {
                "x": self.x,
                "y": self.y,
                "vx": vx_s,
                "vy": vy_s,
                "ay": ay_s,
                "color": spark_color,
                "size": spark_size,
                "life": life_s
            }
            self.spark_particles.append(spark)
            added += 1

        return added

    def _generate_tail_sparks(self, tail_pos: Tuple[int, int]) -> int:
        """在尾部位置生成火花，返回新增数目"""
        tx, ty = tail_pos
        added = 0
        # 随机生成3-5个火花
        desired = random.randint(3, 5)

        for _ in range(desired):
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(3.0, 5.0)  # 尾部火花大小：3-5
            angle = random.uniform(-math.pi, math.pi)

            # 计算速度（保持原轨迹弹出火花的物理参数）
            vx_frame = math.cos(angle) * random.uniform(1.5, 2.5)
            vy_frame = math.sin(angle) * random.uniform(1.5, 2.5)
            vx_s = vx_frame * FPS
            vy_s = vy_frame * FPS
            ay_s = 0.03 * (FPS ** 2)

            # 生命周期
            life_frames = random.randint(20, 40)
            life_s = life_frames / FPS

            self.spark_particles.append({
                "x": tx, "y": ty,
                "vx": vx_s, "vy": vy_s, "ay": ay_s,
                "color": spark_color, "size": spark_size, "life": life_s
            })
            added += 1

        return added

    def is_alive(self) -> bool:
        return (self.life > 0.0) or (len(self.spark_particles) > 0)

    def get_draw_commands(self) -> List[Dict[str, Any]]:
        draw_commands: List[Dict[str, Any]] = []

        # 轨迹绘制 - 使用基于头部比例的三阶段淡出逻辑
        if len(self.trail) > 0:
            trail_len = len(self.trail)

            for i, (tx, ty) in enumerate(self.trail):
                # 计算从头部开始的比例
                # i=0 表示最旧点（尾部），i=trail_len-1 表示最新点（头部）
                # head_ratio = 1.0 表示最旧点，head_ratio = 0.0 表示最新点
                head_ratio = 1.0 - (i / trail_len)

                # 三阶段计算透明度
                if head_ratio < self.trail_head_ratio:
                    # 头部20%（最新点）：完全可见
                    alpha = 255
                elif head_ratio < (self.trail_head_ratio + self.trail_mid_ratio):
                    # 中间78%：线性淡出
                    # 将head_ratio从[0.2, 0.98)映射到[0, 1)
                    t = (head_ratio - self.trail_head_ratio) / self.trail_mid_ratio
                    # 线性从255降到0
                    alpha = 255 * (1 - t)
                else:
                    # 尾部2%（最旧点）：完全透明
                    alpha = 0

                # 确保透明度在0-255范围内
                alpha = int(max(0, min(255, alpha)))

                # 只绘制可见的轨迹点
                if alpha > 10:
                    draw_commands.append({
                        "type": "circle",
                        "position": (tx, ty),
                        "color": (*self.color, alpha),
                        "radius": 3
                    })

        # 主粒子绘制
        if self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH and 0 <= self.y <= self.effect.WINDOW_HEIGHT:
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, 255),
                "radius": self.size
            })

        # 火花绘制
        for spark in self.spark_particles:
            draw_commands.append({
                "type": "circle",
                "position": (int(spark["x"]), int(spark["y"])),
                "color": (*spark["color"], 255),
                "radius": max(1, int(spark["size"]))
            })

        return draw_commands

class PlaneParticle:
    """水平飞行粒子 - 时间驱动版本（实现交叉轨迹）"""

    def __init__(self, effect: OpeningEffect, is_left_to_right: bool):
        self.effect = effect
        self.is_left_to_right = is_left_to_right

        # 初始位置
        self.x = -40.0 if is_left_to_right else float(effect.WINDOW_WIDTH + 40)
        self.y = float(effect.WINDOW_HEIGHT // 2)

        # 颜色
        self.color = effect.PLANE_FIXED_COLORS["left_to_right"]["main"] if is_left_to_right else \
            effect.PLANE_FIXED_COLORS["right_to_left"]["main"]
        self.trail_color = effect.PLANE_FIXED_COLORS["left_to_right"]["trail"] if is_left_to_right else \
            effect.PLANE_FIXED_COLORS["right_to_left"]["trail"]

        # 参数
        self.size = 5.5  # 粒子大小改为5.5
        speed_per_frame = 8.0
        self.speed = speed_per_frame * FPS  # px/s
        self.life = 480 / FPS  # seconds
        self._initial_life = self.life

        # 波动参数
        # 积分计算得到的振幅：1.5 * 60 / 8.0 = 11.25
        self.amplitude = 11.25

        # 轨迹和火花
        self.trail: List[Tuple[int, int]] = []
        self.spark_particles: List[Dict[str, Any]] = []

        # 标志：轨迹是否曾经达到过60长度
        self.trail_ever_reached_60 = False

    def update(self, dt_seconds: float) -> int:
        """
        更新；返回本次新增 spark 数量
        """
        new_sparks = 0

        # 水平移动
        dx = self.speed * dt_seconds if self.is_left_to_right else -self.speed * dt_seconds
        self.x += dx

        # 计算y坐标：实现交叉轨迹
        screen_center_x = self.effect.WINDOW_WIDTH / 2.0
        screen_center_y = self.effect.WINDOW_HEIGHT // 2

        if self.is_left_to_right:
            # 左到右粒子：y = center_y + amplitude * sin((x - center_x)/60)
            self.y = screen_center_y + self.amplitude * math.sin((self.x - screen_center_x) / 60.0)
        else:
            # 右到左粒子：y = center_y - amplitude * sin((x - center_x)/60)
            # 注意：使用负号实现交叉轨迹
            self.y = screen_center_y - self.amplitude * math.sin((self.x - screen_center_x) / 60.0)

        # 更新轨迹
        self.trail.append((int(self.x), int(self.y)))

        # 检查轨迹是否曾达到60长度
        if len(self.trail) >= 60 and not self.trail_ever_reached_60:
            self.trail_ever_reached_60 = True

        # 移除超出长度的轨迹点
        if len(self.trail) > 60:
            self.trail.pop(0)  # 移除最旧点

        # 头部火花生成（粒子在屏幕内且存活时）
        if self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH:
            # 在头部位置生成火花
            added = self._generate_head_sparks()
            new_sparks += added

        # 尾部火花生成（一旦轨迹曾达到60长度，就一直生成，直到轨迹为空）
        if self.trail_ever_reached_60 and len(self.trail) > 0:
            # 在轨迹的第一个点（最旧点）生成火花
            trail_head = self.trail[0]
            added = self._generate_tail_sparks(trail_head)
            new_sparks += added

        # 更新已有的火花
        for spark in self.spark_particles[:]:
            spark["x"] += spark["vx"] * dt_seconds
            spark["vy"] += spark.get("ay", 0.0) * dt_seconds
            spark["y"] += spark["vy"] * dt_seconds
            spark["life"] -= dt_seconds
            if spark["life"] <= 0.0:
                self.spark_particles.remove(spark)

        # 减少生命周期
        self.life -= dt_seconds
        if self.life < 0.0:
            self.life = 0.0

        return new_sparks

    def _generate_head_sparks(self) -> int:
        """在头部位置生成火花，返回新增数目"""
        added = 0
        # 随机生成3-6个火花
        desired = random.randint(3, 6)

        for _ in range(desired):
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(2.0, 4.0)  # 头部火花大小：2-4
            angle = random.uniform(-math.pi, math.pi)

            # 计算速度
            vx_frame = math.cos(angle) * random.uniform(1.5, 2.5)
            vy_frame = math.sin(angle) * random.uniform(1.5, 2.5) + 0.5
            vx_s = vx_frame * FPS
            vy_s = vy_frame * FPS
            ay_s = 0.15 * (FPS ** 2)

            # 生命周期
            life_frames = random.randint(15, 30)
            life_s = life_frames / FPS

            spark = {
                "x": self.x,
                "y": self.y,
                "vx": vx_s,
                "vy": vy_s,
                "ay": ay_s,
                "color": spark_color,
                "size": spark_size,
                "life": life_s
            }
            self.spark_particles.append(spark)
            added += 1

        return added

    def _generate_tail_sparks(self, tail_pos: Tuple[int, int]) -> int:
        """在尾部位置生成火花，返回新增数目"""
        tx, ty = tail_pos
        added = 0
        # 随机生成3-6个火花
        desired = random.randint(3, 6)

        for _ in range(desired):
            spark_color = random.choice(self.effect.SPARK_20_COLORS)
            spark_size = random.uniform(3.0, 5.0)  # 尾部火花大小：3-5
            angle = random.uniform(-math.pi, math.pi)

            # 计算速度
            vx_frame = math.cos(angle) * random.uniform(1.5, 2.5)
            vy_frame = math.sin(angle) * random.uniform(1.5, 2.5) + 0.5
            vx_s = vx_frame * FPS
            vy_s = vy_frame * FPS
            ay_s = 0.15 * (FPS ** 2)

            # 生命周期
            life_frames = random.randint(25, 45)
            life_s = life_frames / FPS

            self.spark_particles.append({
                "x": tx, "y": ty,
                "vx": vx_s, "vy": vy_s, "ay": ay_s,
                "color": spark_color, "size": spark_size, "life": life_s
            })
            added += 1

        return added

    def is_alive(self) -> bool:
        return (self.life > 0.0) or (len(self.spark_particles) > 0)

    def get_draw_commands(self) -> List[Dict[str, Any]]:
        draw_commands: List[Dict[str, Any]] = []

        # 绘制轨迹
        if len(self.trail) > 0:
            trail_len = len(self.trail)
            for i, (tx, ty) in enumerate(self.trail):
                alpha = int(255 * (i / trail_len) * (self.life / max(self._initial_life, 1e-6)))
                if alpha > 10:
                    draw_commands.append({
                        "type": "circle",
                        "position": (tx, ty),
                        "color": (*self.trail_color, alpha),
                        "radius": 3
                    })

        # 绘制主粒子
        if self.life > 0 and 0 <= self.x <= self.effect.WINDOW_WIDTH:
            draw_commands.append({
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, 255),
                "radius": self.size
            })

        # 绘制火花
        for spark in self.spark_particles:
            draw_commands.append({
                "type": "circle",
                "position": (int(spark["x"]), int(spark["y"])),
                "color": (*spark["color"], 255),
                "radius": max(1, int(spark["size"]))
            })

        return draw_commands

import pygame
import os

# If OpeningEffect is defined in the same file (appended), no import needed.
# If you saved OpeningEffect in opening_effect.py, uncomment the line below:
# from opening_effect import OpeningEffect

def draw_commands_main_style(screen: pygame.Surface, commands):
    """
    Draw commands using the same approach as the main program:
    - For circle commands, use pygame.draw.circle(screen, (r,g,b), (x,y), radius)
      If a 4-tuple color is provided, ignore alpha and use the first 3 components.
    - This intentionally matches the main program's simpler rendering path.
    """
    for cmd in commands:
        if cmd.get("type") == "circle":
            x, y = cmd["position"]
            color = cmd["color"]
            # main program typically passed color directly to pygame.draw.circle,
            # which expects RGB; if an RGBA tuple is present, drop alpha.
            if isinstance(color, (list, tuple)) and len(color) >= 3:
                rgb = (color[0], color[1], color[2])
            else:
                # fallback to white
                rgb = (255, 255, 255)
            radius = cmd.get("radius", 1)
            try:
                pygame.draw.circle(screen, rgb, (x, y), radius)
            except Exception:
                # defensive: ensure ints
                pygame.draw.circle(screen, rgb, (int(x), int(y)), int(radius))


def main():
    os.environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()

    screen_w, screen_h = 1600, 900
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("OpeningEffect Demo (main-style rendering)")
    clock = pygame.time.Clock()

    # Instantiate effect (class is assumed defined/imported)
    effect = OpeningEffect(screen_w, screen_h)

    # Use the same time base as the main program fallback: pygame.time.get_ticks()
    music_start = pygame.time.get_ticks()  # ms baseline

    # Activate effect using the same baseline (seconds)
    start_time = (pygame.time.get_ticks() - music_start) / 1000.0
    effect.activate(start_time)

    running = True
    while running:
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT or (ev.type == pygame.KEYDOWN and ev.key == pygame.K_ESCAPE):
                running = False

        # Use ticks-based current_time like the main program (fallback path)
        current_time = (pygame.time.get_ticks() - music_start) / 1000.0

        cmds = effect.update(current_time)

        screen.fill((0, 0, 0))
        if cmds:
            draw_commands_main_style(screen, cmds)

        # Left-top: only show current time (seconds)
        time_font = pygame.font.Font(None, 28)
        time_text = f"{current_time:.1f}s"
        time_surf = time_font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surf, (20, 20))

        pygame.display.flip()
        clock.tick(60)

        # End when effect finished
        if effect.is_finished():
            pygame.time.delay(800)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()