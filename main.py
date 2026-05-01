# main.py
"""
主程序（已做小规模改动）：
- 优先使用音乐实际播放位置（pygame.mixer.music.get_pos）作为 timeline 源，回退到 ticks 基准
- 在 activate/deactivate/preload 处添加简短控制台日志（由 enable_logging 控制）
- 使用 music_length + exit_buffer 作为退出时间阈值（避免硬编码 234.0）
- 保持所有 effect 接口不变，仅修改主程序内部时间源与少量日志
- 屏幕左上角仅显示当前音乐时间（秒），不显示其它调试文字
"""

import os
import sys
import pygame

sys.path.append('.')

# 导入所有段落配置
from subtitle_module.configs import (
    create_transition_1_paragraph, create_louder_paragraph,
    create_lively_paragraph, create_vitality_paragraph,
    create_universe_paragraph, create_full_firework_paragraph,
    create_rebirth_paragraph, create_eternal_paragraph,
    create_transition_2_paragraph
)
from subtitle_module.player import ParagraphPlayer
# 导入字体辅助函数
from subtitle_module.resources import get_font

# 导入九个效果模块
from some_resources import simple_yanhua
from some_resources import double_yanhua
from some_resources import luoxuan_yanhua
from some_resources import opening
from some_resources import ending
from some_resources import date_display
from some_resources import zhufu_yanhua
from some_resources import pen_yanhua
from some_resources import three_yanhua

# -------------------------
# 小配置（可根据需要调整）
# -------------------------
enable_logging = True        # 开发阶段建议 True；发布/演出阶段可设为 False
music_length = 233.0         # 你的音乐时长（秒）
exit_buffer = 1.0            # 音乐结束后的缓冲（秒），用于安全退出

# -------------------------
# 辅助函数
# -------------------------
def get_playback_time(music_start_ms: int, music_loaded: bool) -> float:
    """
    返回当前播放时间（秒）。
    优先使用 pygame.mixer.music.get_pos()（返回相对于播放开始的毫秒），
    在不可用或音乐未加载时回退到基于 get_ticks() 的模拟时间。
    """
    # 当音乐成功加载并处于播放状态时，尝试使用 get_pos()
    if music_loaded:
        try:
            pos_ms = pygame.mixer.music.get_pos()  # 返回相对于播放开始的毫秒，-1 表示不可用
            if pos_ms is not None and pos_ms >= 0 and pygame.mixer.music.get_busy():
                return pos_ms / 1000.0
        except Exception:
            # 在极少数平台或初始化/驱动异常时，get_pos 可能引发异常，回退到 ticks
            pass
    # fallback：使用 ticks 基准（相对于 music_start_ms）
    return (pygame.time.get_ticks() - music_start_ms) / 1000.0


def main():
    # 在初始化前设置窗口居中
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # 初始化
    pygame.init()
    # 尝试初始化混音器（某些环境可能失败）
    try:
        pygame.mixer.init()
    except Exception:
        if enable_logging:
            print("Warning: pygame.mixer.init() failed; running without audio backend.")

    # 设置窗口
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("多彩生日烟花祝福")
    clock = pygame.time.Clock()

    # 创建字幕播放器
    player = ParagraphPlayer(1600, 900)

    # 创建九个效果实例
    opening_effect = opening.OpeningEffect(1600, 900)
    simple_fireworks = simple_yanhua.FireworksEffect(1600, 900)
    date_effect = date_display.DateEffect(1600, 900)
    blessing_firework = zhufu_yanhua.BlessingFirework(1600, 900)
    double_fireworks = double_yanhua.FireworksWithSecondExplosionEffect(1600, 900)
    spiral_fireworks = luoxuan_yanhua.SpiralFireworkEffect(1600, 900, max_fireworks=10)
    triple_explosion_effect = three_yanhua.ThreeExplosionEffect(1600, 900)
    ground_firework_effect = pen_yanhua.GroundFireworkEffect(1600, 900)
    ending_effect = ending.EndingEffect((1600, 900))

    # 效果激活状态标志
    opening_active = False
    simple_active_phase1 = False
    simple_active_phase2 = False
    date_active = False
    blessing_active = False
    double_active = False
    spiral_active = False
    triple_active_170 = False
    triple_active_188 = False
    ground_active = False
    ending_active = False

    # 等待2秒（启动前预留）
    pygame.time.wait(2000)

    # 加载音乐并记录是否成功
    music_loaded = False
    try:
        pygame.mixer.music.load("新愿-四季音色.mp3")
        pygame.mixer.music.play()
        music_loaded = True
        if enable_logging:
            print("Music loaded and playback started.")
    except Exception as e:
        music_loaded = False
        if enable_logging:
            print("Warning: music load/play failed, using simulated time. Exception:", e)

    # 等待音乐真正开始（短暂等待）
    pygame.time.wait(20)

    # 记录音乐开始时间（使用 ticks ms 作为 fallback 基准）
    music_start = pygame.time.get_ticks()

    # 所有段落配置
    paragraphs = [
        ("transition_1", create_transition_1_paragraph, 4.0, -0.5),
        ("louder", create_louder_paragraph, 17.0, 0.0),
        ("lively", create_lively_paragraph, 31.0, 0.0),
        ("vitality", create_vitality_paragraph, 58.0, 0.0),
        ("universe", create_universe_paragraph, 85.0, 0.0),
        ("full_firework", create_full_firework_paragraph, 113.0, 0.0),
        ("rebirth", create_rebirth_paragraph, 140.0, 0.0),
        ("eternal", create_eternal_paragraph, 168.0, 0.0),
        ("transition_2", create_transition_2_paragraph, 195.0, 0.0)
    ]

    # 段落状态
    loaded_paragraphs = [False] * len(paragraphs)
    active_paragraphs = [False] * len(paragraphs)
    current_para_index = -1
    running = True

    # 主循环
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # ----------------------
        # 获取当前播放时间（seconds）
        # ----------------------
        current_time = get_playback_time(music_start, music_loaded)

        # ====================== 特效控制逻辑 ======================
        # 开场效果：0秒激活
        if current_time >= 0.0 and not opening_active:
            opening_effect.activate(current_time)
            opening_active = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE opening_effect")

        # 第一阶段：4-113秒 - 一次爆炸烟花
        if 4.0 <= current_time < 113.0 and not simple_active_phase1:
            simple_fireworks.activate(current_time, 109.0)  # 持续109秒
            simple_active_phase1 = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE simple_fireworks (phase1)")
        # 在113秒时停用一次爆炸烟花
        elif current_time >= 113.0 and simple_active_phase1:
            simple_fireworks.deactivate()
            simple_active_phase1 = False
            if enable_logging:
                print(f"[{current_time:.3f}s] DEACTIVATE simple_fireworks (phase1)")

        # 日期显示效果：36.064秒激活
        if 36.064 <= current_time < 43.564 and not date_active:
            date_effect.activate(current_time)
            date_active = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE date_effect")

        # 祝福烟花：46.192秒激活
        if 44.988 <= current_time < 51.0 and not blessing_active:
            blessing_firework.activate(current_time)
            blessing_active = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE blessing_firework")

        # 第二阶段：113-140秒 - 二次爆炸烟花 + 螺旋烟花
        if 113.0 <= current_time < 140.0:
            # 激活二次爆炸烟花
            if not double_active:
                double_fireworks.activate(current_time, 27.0)  # 持续27秒
                double_active = True
                if enable_logging:
                    print(f"[{current_time:.3f}s] ACTIVATE double_fireworks")

            # 激活螺旋烟花
            if not spiral_active:
                spiral_fireworks.activate(current_time, 27.0)  # 持续27秒
                spiral_active = True
                if enable_logging:
                    print(f"[{current_time:.3f}s] ACTIVATE spiral_fireworks")
        # 在140秒时停用二次爆炸烟花和螺旋烟花
        elif current_time >= 140.0:
            if double_active:
                double_fireworks.deactivate()
                double_active = False
                if enable_logging:
                    print(f"[{current_time:.3f}s] DEACTIVATE double_fireworks")
            if spiral_active:
                spiral_fireworks.deactivate()
                spiral_active = False
                if enable_logging:
                    print(f"[{current_time:.3f}s] DEACTIVATE spiral_fireworks")

        # 第三阶段：140-222秒 - 一次爆炸烟花
        if 140.0 <= current_time < 222.0 and not simple_active_phase2:
            simple_fireworks.activate(current_time, 82.0)  # 持续82秒
            simple_active_phase2 = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE simple_fireworks (phase2)")
        # 在222秒时停用一次爆炸烟花
        elif current_time >= 222.0 and simple_active_phase2:
            simple_fireworks.deactivate()
            simple_active_phase2 = False
            if enable_logging:
                print(f"[{current_time:.3f}s] DEACTIVATE simple_fireworks (phase2)")

        # 三级爆炸烟花：170秒激活
        if 170.0 <= current_time < 175.0 and not triple_active_170:
            triple_explosion_effect.activate(current_time)
            triple_active_170 = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE triple_explosion_effect (170s)")
        # 三级爆炸烟花：188秒激活
        if 188.0 <= current_time < 193.0 and not triple_active_188:
            triple_explosion_effect.activate(current_time)
            triple_active_188 = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE triple_explosion_effect (188s)")

        # 地面烟花：195秒激活
        if 195.0 <= current_time < 220.0 and not ground_active:
            ground_firework_effect.activate(current_time)
            ground_active = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE ground_firework_effect")

        # 结束效果：222秒激活
        if 222.0 <= current_time < 233.0 and not ending_active:
            ending_effect.activate(current_time)
            ending_active = True
            if enable_logging:
                print(f"[{current_time:.3f}s] ACTIVATE ending_effect")
        # 在233秒时，结束效果自然结束
        elif current_time >= 233.0 and ending_active:
            ending_active = False
            if enable_logging:
                print(f"[{current_time:.3f}s] ENDING_EFFECT_WINDOW_ENDED")

        # ====================== 更新所有效果 ======================
        opening_commands = opening_effect.update(current_time) if opening_active else None
        simple_commands = simple_fireworks.update(current_time)
        date_commands = date_effect.update(current_time) if date_active else None
        blessing_commands = blessing_firework.update(current_time) if blessing_active else None
        double_commands = double_fireworks.update(current_time) if double_active or (
                    hasattr(double_fireworks, 'fireworks') and double_fireworks.fireworks) else None
        spiral_commands = spiral_fireworks.update(current_time) if spiral_active or (
                    hasattr(spiral_fireworks, 'fireworks') and spiral_fireworks.fireworks) else None
        triple_commands = triple_explosion_effect.update(current_time)
        ground_commands = ground_firework_effect.update(current_time) if ground_active else None
        ending_commands = ending_effect.update(current_time) if ending_active else None

        # ====================== 处理所有字幕段落 ======================
        for i, (name, create_func, design_start, offset) in enumerate(paragraphs):
            actual_start = design_start + offset

            # 预加载段落（提前0.3秒）
            if not loaded_paragraphs[i] and current_time >= (actual_start - 0.3):
                config = create_func()
                player.load(config)
                loaded_paragraphs[i] = True
                if enable_logging:
                    print(f"[{current_time:.3f}s] PRELOAD paragraph '{name}'")

            # 激活段落
            if not active_paragraphs[i] and current_time >= actual_start:
                # 确保按序播放或按设计允许激活
                if i == 0 or (i > 0 and active_paragraphs[i - 1] and not player.is_playing_paragraph()):
                    active_paragraphs[i] = True
                    current_para_index = i

                    # 重新加载并播放段落
                    config = create_func()
                    player.load(config)
                    player.play(0.0)
                    if enable_logging:
                        print(f"[{current_time:.3f}s] ACTIVATE paragraph '{name}'")

        # 更新当前播放的段落
        if current_para_index >= 0:
            name, _, design_start, offset = paragraphs[current_para_index]
            actual_start = design_start + offset
            internal_time = current_time - actual_start
            frame = player.update(internal_time)
        else:
            frame = None

        # ====================== 清屏 ======================
        screen.fill((0, 0, 0))

        # ====================== 绘制所有特效（从下到上） ======================
        # 1. 日期显示效果（最下面）
        if date_commands:
            for command in date_commands:
                if command["type"] == "text_surface":
                    surface = command["surface"]
                    position = command["position"]
                    screen.blit(surface, position)

        # 2. 开场效果
        if opening_commands:
            for command in opening_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # 3. 一次爆炸烟花
        if simple_commands:
            for command in simple_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # 4. 螺旋烟花
        if spiral_commands:
            for command in spiral_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # 5. 二次爆炸烟花
        if double_commands:
            for command in double_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # 6. 祝福烟花
        if blessing_commands:
            for command in blessing_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)
                elif command["type"] == "text_surface":
                    surface = command["surface"]
                    position = command["position"]
                    screen.blit(surface, position)

        # 7. 三级爆炸烟花
        if triple_commands:
            for command in triple_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # 8. 地面烟花
        if ground_commands:
            for command in ground_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)
                elif command["type"] == "rect":
                    x, y = command["position"]
                    width, height = command["size"]
                    color = command["color"]
                    # 创建临时表面来绘制带透明度的矩形
                    temp_surf = pygame.Surface((width, height), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surf, color, (0, 0, width, height))
                    screen.blit(temp_surf, (x, y))

        # 9. 结束效果
        if ending_commands:
            for command in ending_commands:
                if command["type"] == "circle":
                    x, y = command["position"]
                    color = command["color"]
                    radius = command["radius"]
                    pygame.draw.circle(screen, color, (x, y), radius)

        # ====================== 显示字幕（中心/页面） ======================
        # 保留字幕渲染（frame），因为字幕是内容的一部分；不在左上角显示其它文字
        if frame:
            # 使用新的get_font函数
            font = get_font(frame['font_name'], frame['font_size'])
            text = font.render(frame['text'], True, frame['color'])

            if frame['alpha'] < 255:
                text.set_alpha(frame['alpha'])

            x, y = frame['position']
            pos = text.get_rect(center=(x, y))
            screen.blit(text, pos)

        # ====================== 左上角：仅显示当前音乐时间（秒） ======================
        time_font = pygame.font.Font(None, 36)
        time_text = f"{current_time:.1f}s"
        time_surface = time_font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surface, (20, 20))

        # ====================== 检查是否所有段落都已完成 ======================
        all_completed = all(active_paragraphs)
        if all_completed and not player.is_playing_paragraph():
            if current_time > 233.0:
                # 等待1秒后退出
                pygame.time.wait(1000)
                running = False

        # 使用音乐长度 + 缓冲来判断程序退出（更靠近音乐结束）
        if current_time > (music_length + exit_buffer):
            if enable_logging:
                print(f"[{current_time:.3f}s] EXIT: reached music_length + buffer")
            running = False

        pygame.display.flip()
        clock.tick(60)

    # 停止音乐
    try:
        pygame.mixer.music.stop()
    except Exception:
        pass
    pygame.quit()


if __name__ == "__main__":
    main()