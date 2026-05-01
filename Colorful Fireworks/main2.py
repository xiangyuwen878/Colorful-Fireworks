import os
import sys

import pygame

sys.path.append('.')

# 只导入 universe 段落配置
from subtitle_module.configs import create_universe_paragraph
from subtitle_module.player import ParagraphPlayer

# -------------------------
# 配置
# -------------------------
music_start_offset = 80.0  # 音乐从第80秒开始播放
program_end_time = 115.0  # 程序在音乐115秒时结束
enable_logging = True  # 启用日志


# -------------------------
# 辅助函数
# -------------------------
def get_playback_time(music_start_ms: int, music_loaded: bool) -> float:
    """
    返回当前播放时间（秒，相对于音乐开始）。
    优先使用 pygame.mixer.music.get_pos()，回退到基于 get_ticks() 的模拟时间。
    """
    if music_loaded:
        try:
            pos_ms = pygame.mixer.music.get_pos()
            if pos_ms is not None and pos_ms >= 0 and pygame.mixer.music.get_busy():
                return pos_ms / 1000.0
        except Exception:
            pass
    # fallback：使用 ticks 基准
    return (pygame.time.get_ticks() - music_start_ms) / 1000.0


def main():
    # 窗口居中
    os.environ['SDL_VIDEO_CENTERED'] = '1'

    # 初始化
    pygame.init()
    try:
        pygame.mixer.init()
    except Exception:
        if enable_logging:
            print("Warning: pygame.mixer.init() failed; running without audio backend.")

    # 设置窗口
    screen = pygame.display.set_mode((1600, 900))
    pygame.display.set_caption("新愿-四季音色 - Universe")
    clock = pygame.time.Clock()

    # 创建字幕播放器
    player = ParagraphPlayer(1600, 900)

    # Universe 段落配置
    universe_config = create_universe_paragraph()

    # 状态变量
    universe_preloaded = False
    universe_active = False
    music_loaded = False
    running = True

    # 等待2秒
    pygame.time.wait(2000)

    # 加载音乐并从80秒开始播放
    try:
        pygame.mixer.music.load("新愿-四季音色.mp3")
        # 从80秒开始播放
        pygame.mixer.music.play(start=80.0)
        music_loaded = True
        if enable_logging:
            print(f"Music loaded and playing from {music_start_offset}s")
    except Exception as e:
        music_loaded = False
        if enable_logging:
            print("Warning: music load/play failed, using simulated time. Exception:", e)

    # 等待音乐真正开始
    pygame.time.wait(20)

    # 记录音乐开始时间
    music_start_ticks = pygame.time.get_ticks()

    # 主循环
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        # 获取当前播放时间
        playback_time = get_playback_time(music_start_ticks, music_loaded)
        # 计算实际音乐时间（从音乐开始计算，0秒对应原音乐文件0秒）
        current_music_time = music_start_offset + playback_time

        if enable_logging:
            print(f"Playback: {playback_time:.1f}s, Music time: {current_music_time:.1f}s")

        # ====================== Universe 段落控制 ======================
        # Universe 段落设计开始时间：85.0秒
        universe_design_start = 85.0
        offset = 0.0
        universe_actual_start = universe_design_start + offset

        # 预加载段落（提前0.3秒）
        if not universe_preloaded and current_music_time >= (universe_actual_start - 0.3):
            player.load(universe_config)
            universe_preloaded = True
            if enable_logging:
                print(f"[{current_music_time:.3f}s] PRELOAD universe paragraph")

        # 激活段落
        if not universe_active and current_music_time >= universe_actual_start:
            universe_active = True
            # 重新加载并播放段落
            player.load(universe_config)
            player.play(0.0)
            if enable_logging:
                print(f"[{current_music_time:.3f}s] ACTIVATE universe paragraph")

        # 更新当前播放的段落
        if universe_active:
            # 计算段落内部时间
            internal_time = current_music_time - universe_actual_start
            frame = player.update(internal_time)
        else:
            frame = None

        # ====================== 清屏 ======================
        screen.fill((0, 0, 0))

        # ====================== 显示字幕（中心/页面） ======================
        if frame:
            try:
                font = pygame.font.SysFont(frame['font_name'], frame['font_size'])
            except:
                font = pygame.font.Font(None, frame['font_size'])

            text = font.render(frame['text'], True, frame['color'])

            if frame['alpha'] < 255:
                text.set_alpha(frame['alpha'])

            x, y = frame['position']
            pos = text.get_rect(center=(x, y))
            screen.blit(text, pos)

        # ====================== 左上角：仅显示当前音乐时间（秒） ======================
        time_font = pygame.font.Font(None, 36)
        time_text = f"{current_music_time:.1f}s"
        time_surface = time_font.render(time_text, True, (255, 255, 255))
        screen.blit(time_surface, (20, 20))

        # ====================== 检查是否结束 ======================
        if current_music_time >= program_end_time:
            if enable_logging:
                print(f"[{current_music_time:.3f}s] EXIT: reached program end time {program_end_time}s")
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