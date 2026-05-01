# some_resources/pen_yanhua.py
"""
地面烟花效果 - 恢复原始视觉参数并修复“末期被强行加速”问题
- 保持外部接口不变： update(current_time: float) 接受绝对时间（秒）
- 统一时间单位为秒（内部使用 dt_seconds），但原始以“帧”为单位的参数已转换为秒以保留视觉行为
- 增大速度的倍数 speed_multiplier=1.5 以使粒子飞得更远（其余视觉参数恢复为原始）
- 注意：我没有对单帧 dt 做上限保护（按你要求暂不采用）
"""

import math
import random
import time
from typing import List, Dict, Any, Optional

import pygame


class GroundFireworkEffect:
    """
    地面烟花效果类
    外部接口保持与原来一致：调用 update(current_time_seconds)
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        # 屏幕尺寸（像素）
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 控制变量
        self.is_active = False
        self.start_time = 0.0  # 以秒为单位的绝对时间戳（time.time()）

        # 时间参数（单位：秒）
        self.total_duration = 25.0  # 总时长（秒）
        self.start_delay = 2.0
        self.fade_in_duration = 3.0
        self.launch_duration = 17.0
        self.fade_out_duration = 3.0

        # 恢复原始三发射器位置
        self.fireworks = []
        positions = [screen_width / 4, screen_width / 2, screen_width * 3 / 4]
        for pos in positions:
            self.fireworks.append(self.Firework(pos, screen_height - 8, screen_height))

        # 状态
        self.box_alpha = 0
        self.phase = "delay"  # delay, fade_in, launch, fade_out, finished

        # 上一帧时间（绝对秒），用于计算本帧 dt_seconds = current_time - last_frame_time
        # 在 activate 时会初始化为 start_time
        self.last_frame_time: Optional[float] = None

    class FireworkParticle:
        """
        粒子类——尽量保留原始视觉参数语义，但以秒为主时间单位。
        原始代码中 speed 是以“像素/帧”为语义，这里把它转换为 px/s：
            speed_px_per_frame = random.uniform(1, 3.5)  # 原始语义
            speed_px_per_second = speed_px_per_frame * 60
        为达到“飞得更远”的要求，乘以 speed_multiplier。
        原始 gravity 每帧是 0.0125（像素/帧^2），因此 gravity_per_second = 0.0125 * 60.
        原始 fly_duration / fade_duration 是以帧为单位，转换为秒： frames / 60
        """

        def __init__(self, x: float, y: float, angle: float, speed_multiplier: float = 1.5):
            # position in pixels (float)
            self.x = float(x)
            self.y = float(y)

            # 保留原始尺寸范围（像素）
            self.size = random.randint(1, 2)

            # 颜色保持不变（白系），按你的要求不修改颜色
            self.color = random.choice([
                (255, 255, 255), (255, 245, 230),
                (255, 250, 250), (240, 248, 255)
            ])

            self.angle = angle

            # 原始 speed 是 px/frame；转换到 px/s 并放大以飞得更远
            speed_px_per_frame = random.uniform(1.0, 3.5)  # 原始语义
            speed_px_per_second = speed_px_per_frame * 60.0 * speed_multiplier  # px/s
            self.vx = speed_px_per_second * math.cos(angle)
            # 注意原代码里 vy = -speed * sin(angle)（y 向下为正）
            self.vy = -speed_px_per_second * math.sin(angle)

            # gravity: 原来每帧加 0.0125，所以转为每秒： *60
            self.gravity = 0.0125 * 60.0  # px/s^2

            # 原始 fly_duration/fade_duration 是帧数 -> 转成秒
            fly_frames = random.randint(40, 53)
            fade_frames = random.randint(13, 27)
            self.fly_duration = fly_frames / 60.0  # seconds
            self.fade_duration = fade_frames / 60.0  # seconds
            self.max_life = self.fly_duration + self.fade_duration
            self.life = self.max_life

            # early_death 逻辑保留（按原始语义）
            self.early_death = random.random() < 0.15
            if self.early_death:
                fly_frames = random.randint(7, 27)
                self.fly_duration = fly_frames / 60.0
                extra_fade_frames = random.randint(3, 10)
                self.fade_duration = extra_fade_frames / 60.0
                self.max_life = self.fly_duration + self.fade_duration
                self.life = self.max_life

        def update(self, dt_seconds: float):
            """
            用本帧真实 dt（秒）做连续积分更新，避免把累计时间当本帧时间传入导致重复推进问题。
            这个改动是为了解决“末期被强行加速”问题：外层必须保证这里传入的 dt_seconds 是
            本帧时间差（current_time - last_frame_time）。
            """

            if dt_seconds <= 0.0 or self.life <= 0.0:
                # 仍然减少生命但不做位移
                self.life = max(0.0, self.life - dt_seconds)
                return

            # 运动学积分（连续）
            self.x += self.vx * dt_seconds
            # 重力对速度的影响（y 轴正向向下）
            self.vy += self.gravity * dt_seconds
            self.y += self.vy * dt_seconds

            # 生命减少（秒为单位）
            self.life -= dt_seconds
            if self.life < 0.0:
                self.life = 0.0

        def get_draw_commands(self) -> List[Dict[str, Any]]:
            if self.life <= 0.0:
                return []

            # alpha 计算：当剩余生命 <= fade_duration 时线性衰减
            if self.life > self.fade_duration:
                alpha = 255
            else:
                # 把 fade_duration 视为秒
                alpha = int(255 * (self.life / max(self.fade_duration, 1e-6)))
                alpha = max(0, min(255, alpha))

            return [{
                "type": "circle",
                "position": (int(self.x), int(self.y)),
                "color": (*self.color, alpha),
                "radius": max(1, int(self.size))
            }]

    class Firework:
        """
        单个发射器。保留原始的 directions/emit_interval 语义。
        注意：emit_interval 在原始代码是以毫秒为单位（50），这里仍然以毫秒为准用于比较（elapsed_ms）
        """

        def __init__(self, x: float, y: float, screen_height: int, speed_multiplier: float = 1.5):
            self.x = x
            self.y = y
            self.screen_height = screen_height
            self.box_width = 15
            self.box_height = 8
            self.box_x = int(self.x - self.box_width // 2)
            self.box_y = screen_height - self.box_height
            self.particles: List[GroundFireworkEffect.FireworkParticle] = []
            # directions: [angle, emitted_count, total]
            self.directions: List[List[Any]] = []
            self.max_directions = 10
            # last_emit_time 保留原始语义（毫秒的时间戳或相对 ms 值），用于判断发射间隔
            self.last_emit_time = 0.0  # in ms (relative to effect start)
            self.emit_interval = 50  # ms
            self.purple_color = (200, 180, 255)
            self.speed_multiplier = speed_multiplier

        def update(self, elapsed_ms: float, box_alpha: int, is_active: bool, dt_seconds: float):
            """
            更新粒子状态：
            - elapsed_ms: 自效果开始以来的毫秒数（用于保持原始发射逻辑）
            - dt_seconds: 本帧时间差（秒），必须传入真实本帧差值，供粒子连续积分使用
            """
            # 更新粒子（使用 dt_seconds，不使用 elapsed_ms-last_emit_time）
            for particle in self.particles[:]:
                particle.update(dt_seconds)
                if particle.life <= 0.0:
                    self.particles.remove(particle)

            # 发射新粒子（保留原来按 elapsed_ms 与 last_emit_time 比较的触发逻辑）
            if is_active and (elapsed_ms - self.last_emit_time > self.emit_interval):
                self.manage_directions()
                self.emit_particles()
                # 更新 last_emit_time 为当前 elapsed_ms（与原逻辑一致）
                self.last_emit_time = elapsed_ms

        def manage_directions(self):
            # 保持原始方向管理逻辑
            self.directions = [d for d in self.directions if d[1] < d[2]]
            while len(self.directions) < self.max_directions:
                angle = random.uniform(math.pi / 3, 2 * math.pi / 3)
                total = random.randint(5, 10)
                self.directions.append([angle, 0, total])

        def emit_particles(self):
            # 保持原始发射粒子方式（每次对每个 direction 发射一个粒子并自增计数）
            for d in self.directions:
                if d[1] < d[2]:
                    d[1] += 1
                    angle = d[0]
                    # 创建粒子时传入 speed_multiplier 以实现“飞得更远”
                    p = GroundFireworkEffect.FireworkParticle(self.x, self.y, angle, speed_multiplier=self.speed_multiplier)
                    self.particles.append(p)

        def get_draw_commands(self, box_alpha: int) -> List[Dict[str, Any]]:
            draw_commands: List[Dict[str, Any]] = []
            if box_alpha > 0:
                draw_commands.append({
                    "type": "rect",
                    "position": (int(self.box_x), int(self.box_y)),
                    "size": (self.box_width, self.box_height),
                    "color": (*self.purple_color, box_alpha)
                })

            for particle in self.particles:
                draw_commands.extend(particle.get_draw_commands())

            return draw_commands

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活效果
        - start_time: 以 time.time() 返回的秒为单位的绝对时间戳（外部调用方传入）
        """
        self.is_active = True
        self.start_time = start_time
        self.phase = "delay"
        self.box_alpha = 0

        # 初始化 last_frame_time，确保第一帧 dt 很小（避免激活时产生大跳动）
        self.last_frame_time = start_time

        # 重置所有发射器状态（保留发射语义）
        for firework in self.fireworks:
            firework.particles = []
            firework.directions = []
            firework.last_emit_time = 0.0

    def deactivate(self) -> None:
        self.is_active = False

    def clear_all(self) -> None:
        self.is_active = False
        for firework in self.fireworks:
            firework.particles = []
            firework.directions = []

    def update(self, current_time: float) -> Optional[List[Dict[str, Any]]]:
        """
        更新效果状态（接口保持不变）
        - current_time: 以秒为单位的绝对时间戳
        返回值与原先相同：若无绘制命令返回 None，否则返回命令列表
        """
        if not self.is_active:
            return None

        # 计算自激活以来的 elapsed_time（秒）
        elapsed_time = current_time - self.start_time
        if elapsed_time < 0:
            return None

        # 若超过总时长，结束效果
        if elapsed_time >= self.total_duration:
            self.is_active = False
            return None

        # 计算本帧 dt_seconds（以秒为单位）
        if self.last_frame_time is None:
            dt_seconds = 0.0
        else:
            dt_seconds = current_time - self.last_frame_time
            # 说明：按你要求暂不对 dt 做上限保护（如果需要可以再加）
        self.last_frame_time = current_time

        # 把 elapsed_time 转为毫秒用于保留原始发射判定逻辑
        elapsed_ms = elapsed_time * 1000.0

        # 阶段判定与 box_alpha 设置（保持原始逻辑）
        if elapsed_time < self.start_delay:
            self.phase = "delay"
            self.box_alpha = 0
        elif elapsed_time < self.start_delay + self.fade_in_duration:
            self.phase = "fade_in"
            progress = (elapsed_time - self.start_delay) / self.fade_in_duration
            self.box_alpha = int(255 * progress)
        elif elapsed_time < self.start_delay + self.fade_in_duration + self.launch_duration:
            self.phase = "launch"
            self.box_alpha = 255
        elif elapsed_time < self.total_duration:
            self.phase = "fade_out"
            progress = (elapsed_time - (self.start_delay + self.fade_in_duration + self.launch_duration)) / self.fade_out_duration
            self.box_alpha = int(255 * (1.0 - progress))
        else:
            self.phase = "finished"
            self.box_alpha = 0

        is_active_phase = (self.phase == "launch")

        # 更新每个发射器：传入 elapsed_ms（用于发射判定，保留原始语义）以及 dt_seconds（用于粒子更新，避免末期加速）
        all_draw_commands: List[Dict[str, Any]] = []
        for firework in self.fireworks:
            firework.update(elapsed_ms, self.box_alpha, is_active_phase, dt_seconds)
            all_draw_commands.extend(firework.get_draw_commands(self.box_alpha))

        return all_draw_commands if all_draw_commands else None

    def is_finished(self) -> bool:
        return not self.is_active

    def get_status(self) -> Dict[str, Any]:
        return {
            "is_active": self.is_active,
            "phase": self.phase,
            "box_alpha": self.box_alpha,
            "start_time": self.start_time
        }


# ---------- 简单 Pygame 主程序用于测试 ----------
def draw_commands_to_surface(screen: pygame.Surface, commands: List[Dict[str, Any]]):
    """
    渲染 get_draw_commands 的命令到 screen。
    支持：
      - rect: color 包含 alpha 时使用 SRCALPHA 临时 surface
      - circle: 同上
    """
    for cmd in commands:
        if cmd["type"] == "rect":
            x, y = cmd["position"]
            w, h = cmd["size"]
            r, g, b, a = cmd["color"]
            if a >= 255:
                pygame.draw.rect(screen, (r, g, b), pygame.Rect(x, y, w, h))
            elif a <= 0:
                continue
            else:
                surf = pygame.Surface((w, h), pygame.SRCALPHA)
                surf.fill((r, g, b, a))
                screen.blit(surf, (x, y))
        elif cmd["type"] == "circle":
            x, y = cmd["position"]
            radius = cmd["radius"]
            r, g, b, a = cmd["color"]
            if a >= 255:
                pygame.draw.circle(screen, (r, g, b), (x, y), radius)
            elif a <= 0:
                continue
            else:
                diameter = max(1, radius * 2)
                surf = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                pygame.draw.circle(surf, (r, g, b, a), (radius, radius), radius)
                screen.blit(surf, (x - radius, y - radius))


def main():
    pygame.init()
    screen_w, screen_h = 1600, 900
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Ground Firework Effect - Restored & Fixed")
    clock = pygame.time.Clock()

    effect = GroundFireworkEffect(screen_w, screen_h)

    start_time = time.time()
    effect.activate(start_time)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        now = time.time()
        draw_cmds = effect.update(now)

        screen.fill((0, 0, 0))
        if draw_cmds:
            draw_commands_to_surface(screen, draw_cmds)

        # HUD
        status = effect.get_status()
        font = pygame.font.SysFont(None, 24)
        txt = f"Phase: {status['phase']}  BoxAlpha: {status['box_alpha']}"
        img = font.render(txt, True, (200, 200, 200))
        screen.blit(img, (10, 10))

        pygame.display.flip()
        clock.tick(60)

        if effect.is_finished():
            time.sleep(1.0)
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()