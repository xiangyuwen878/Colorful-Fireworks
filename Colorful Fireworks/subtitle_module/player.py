# subtitle_module/player.py
"""
通用段落播放器模块
功能：加载段落配置，管理播放状态，计算动画效果，生成渲染数据
注意：此版本专注于基本功能实现，暂不做健壮性处理
"""

from typing import Dict, List, Optional, Tuple, Any

from .resources import get_color


class ParagraphPlayer:
    """通用段落播放器"""

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        """
        初始化播放器

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.center_position = (screen_width // 2, screen_height // 2)

        # 播放状态
        self.current_config = None
        self.beat_data = []  # 处理过的节拍数据
        self.current_beat_index = -1
        self.current_beat_start_time = 0
        self.is_playing = False
        self.start_time = 0
        self.total_progress = 0
        self.paragraph_duration = 0

    def load(self, config: Dict[str, Any]) -> None:
        """
        加载段落配置

        Args:
            config: 段落配置字典
        """
        self.current_config = config
        self.beat_data = []

        # 预处理节拍数据
        for i, beat in enumerate(config.get("beats", [])):
            beat_data = beat.copy()

            # 获取动画类型
            animation = beat.get("animation", "fade")

            # 获取位置类型，如果没有指定则使用默认值
            position_type = beat.get("position")
            if position_type is None:
                # 根据动画类型设置默认位置
                if animation in ["fade", "zoom", "typewriter"]:
                    position_type = "center"
                elif animation == "slide":
                    position_type = "top"
                else:
                    position_type = "center"

            beat_data["position_type"] = position_type

            # 为不同动画类型初始化额外数据
            if animation == "zoom":
                # 缩放动画：添加起始和结束大小
                beat_data["start_font_size"] = 0
                beat_data["end_font_size"] = beat.get("font_size", 60)
            elif animation == "typewriter":
                # 打字机动画：初始化显示字符数
                beat_data["displayed_chars"] = 0

            # 根据动画类型和位置类型计算位置
            if animation in ["fade", "zoom"]:
                beat_data["position"] = self._get_position(position_type)
            elif animation == "typewriter":
                # 打字机动画固定使用中心位置
                beat_data["position"] = self._get_position("center")
            elif animation == "slide":
                # 滑动动画：起点为指定位置的屏幕外，终点为中心
                if position_type == "center":
                    # 如果指定了center，则转换为top
                    start_position_type = "top"
                else:
                    start_position_type = position_type
                beat_data["start_position"] = self._get_edge_position(start_position_type)
                beat_data["position"] = self._get_position("center")  # 终点为中心

            self.beat_data.append(beat_data)

        # 计算段落总时长
        self.paragraph_duration = sum(beat.get("duration", 0) for beat in config.get("beats", []))

        # 重置状态
        self.current_beat_index = -1
        self.current_beat_start_time = 0
        self.is_playing = False
        self.start_time = 0
        self.total_progress = 0

    def play(self, start_time: float = 0.0) -> None:
        """
        开始播放段落

        Args:
            start_time: 开始播放的时间（绝对时间）
        """
        if not self.current_config:
            return

        self.is_playing = True
        self.start_time = start_time
        self.current_beat_index = -1
        self.current_beat_start_time = 0
        self.total_progress = 0

    def update(self, current_time: float) -> Optional[Dict[str, Any]]:
        """
        更新播放状态

        Args:
            current_time: 当前时间（绝对时间）

        Returns:
            渲染数据字典，如果没有内容则返回None
        """
        if not self.is_playing or not self.current_config:
            return None

        # 计算相对于段落开始的时间
        elapsed_time = current_time - self.start_time

        # 如果段落已结束
        if elapsed_time < 0 or elapsed_time >= self.paragraph_duration:
            self.is_playing = False
            return None

        # 更新总进度
        self.total_progress = elapsed_time / self.paragraph_duration if self.paragraph_duration > 0 else 0

        # 检查是否需要切换到下一个节拍
        if (self.current_beat_index < 0 or
                elapsed_time >= self.current_beat_start_time +
                self.beat_data[self.current_beat_index].get("duration", 0)):

            # 切换到下一个节拍
            self.current_beat_index += 1

            # 检查是否超出节拍范围
            if self.current_beat_index >= len(self.beat_data):
                self.is_playing = False
                return None

            self.current_beat_start_time = elapsed_time

        # 获取当前节拍
        current_beat = self.beat_data[self.current_beat_index]

        # 计算当前节拍的进度
        beat_duration = current_beat.get("duration", 0)
        if beat_duration > 0:
            beat_progress = (elapsed_time - self.current_beat_start_time) / beat_duration
            beat_progress = max(0, min(beat_progress, 1.0))  # 限制在0-1之间
        else:
            beat_progress = 1.0

        # 生成渲染数据
        return self._calculate_frame(current_beat, beat_progress)

    def _calculate_frame(self, beat: Dict[str, Any], progress: float) -> Optional[Dict[str, Any]]:
        """
        计算当前帧的渲染数据

        Args:
            beat: 节拍数据
            progress: 节拍进度（0-1）

        Returns:
            渲染数据字典
        """
        # 如果是空文本，返回None
        if not beat.get("text", ""):
            return None

        # 获取动画类型
        animation = beat.get("animation", "fade")

        # 计算透明度
        alpha = self._calculate_alpha(animation, progress)

        # 计算位置、字体大小和显示文本
        if animation == "fade":
            position = beat.get("position", self.center_position)
            font_size = beat.get("font_size", 60)
            display_text = beat.get("text", "")

        elif animation == "zoom":
            position = beat.get("position", self.center_position)
            # 缩放动画：字体大小从0逐渐放大
            if progress <= 0.5:
                # 前50%时间：从0放大到目标大小
                zoom_progress = progress * 2
                font_size = int(beat.get("start_font_size", 0) +
                                (beat.get("end_font_size", 60) - beat.get("start_font_size", 0)) * zoom_progress)
            else:
                # 后50%时间：保持目标大小
                font_size = beat.get("end_font_size", 60)
            display_text = beat.get("text", "")

        elif animation == "slide":
            # 滑动动画：从边缘滑动到中心
            start_position = beat.get("start_position", self._get_edge_position("top"))
            end_position = beat.get("position", self._get_position("center"))
            current_x = start_position[0] + (end_position[0] - start_position[0]) * progress
            current_y = start_position[1] + (end_position[1] - start_position[1]) * progress
            position = (int(current_x), int(current_y))
            font_size = beat.get("font_size", 60)
            display_text = beat.get("text", "")

        elif animation == "typewriter":
            # 打字机动画：固定在屏幕中心
            position = beat.get("position", self._get_position("center"))
            font_size = beat.get("font_size", 60)

            # 打字机效果：逐个显示字符
            total_chars = len(beat.get("text", ""))

            # 修改后的时间阶段划分
            typewriter_phase_end = 0.5  # 50%时间用于打字
            full_display_end = 0.75  # 50-75%时间完全显示
            # 75-100%时间用于淡出

            if progress <= typewriter_phase_end:
                # 打字阶段：在typewriter_phase_end时间内完成所有字符显示
                phase_progress = progress / typewriter_phase_end
                display_chars = int(total_chars * phase_progress)
                display_text = beat.get("text", "")[:display_chars]
                # 打字阶段不计算透明度（使用完全显示时的透明度）
                alpha = 255
            elif progress <= full_display_end:
                # 完全显示阶段
                display_text = beat.get("text", "")
                alpha = 255
            else:
                # 淡出阶段
                display_text = beat.get("text", "")
                fade_progress = (progress - full_display_end) / (1 - full_display_end)
                alpha = int(255 * (1 - fade_progress))

            # 确保显示字符数不超过总字符数
            if 'display_chars' in locals():
                display_chars = min(display_chars, total_chars)
                display_text = beat.get("text", "")[:display_chars]

        else:
            # 默认使用fade动画
            position = beat.get("position", self.center_position)
            font_size = beat.get("font_size", 60)
            display_text = beat.get("text", "")

        # 获取颜色RGB值
        color_name = beat.get("color", "aliceblue")
        color_rgb = get_color(color_name)

        return {
            "text": display_text,
            "color": color_rgb,
            "font_name": beat.get("font_name", "华文宋体"),
            "font_size": font_size,
            "position": position,
            "alpha": alpha
        }

    def _calculate_alpha(self, animation: str, progress: float) -> int:
        """
        计算透明度

        Args:
            animation: 动画类型
            progress: 节拍进度（0-1）

        Returns:
            透明度值（0-255）
        """
        # 不同动画的淡入淡出时间点
        fade_in_end = 0.3  # 淡入结束点

        if animation == "typewriter":
            # 打字机效果：延长完全显示时间
            fade_out_start = 0.8
        else:
            # 其他效果
            fade_out_start = 0.7

        if progress <= fade_in_end:
            # 淡入阶段
            alpha = int(255 * (progress / fade_in_end))
        elif progress >= fade_out_start:
            # 淡出阶段
            alpha = int(255 * (1 - (progress - fade_out_start) / (1 - fade_out_start)))
        else:
            # 完全显示阶段
            alpha = 255

        return max(0, min(alpha, 255))  # 确保在0-255范围内

    def _get_position(self, position_type: str) -> Tuple[int, int]:
        """
        获取指定类型的位置

        Args:
            position_type: 位置类型，可选 "center", "top", "bottom"

        Returns:
            (x, y) 坐标
        """
        center_x, center_y = self.center_position

        if position_type == "top":
            return (center_x, center_y - 150)
        elif position_type == "bottom":
            return (center_x, center_y + 150)
        else:  # center
            return (center_x, center_y)

    def _get_edge_position(self, position_type: str) -> Tuple[int, int]:
        """
        获取屏幕边缘的位置（用于slide动画）

        Args:
            position_type: 位置类型，可选 "top", "bottom"

        Returns:
            (x, y) 坐标
        """
        center_x, center_y = self.center_position

        if position_type == "bottom":
            # 从下方进入
            return (center_x, self.screen_height - 100)
        else:  # top
            # 从上方进入
            return (center_x, +100)

    def pause(self) -> None:
        """暂停播放"""
        self.is_playing = False

    def resume(self) -> None:
        """恢复播放"""
        if self.current_config:
            self.is_playing = True

    def stop(self) -> None:
        """停止播放"""
        self.is_playing = False
        self.current_beat_index = -1
        self.current_beat_start_time = 0
        self.start_time = 0
        self.total_progress = 0

    def is_playing_paragraph(self) -> bool:
        """
        检查是否正在播放段落

        Returns:
            是否正在播放
        """
        return self.is_playing

    def get_current_beat_info(self) -> Dict[str, Any]:
        """
        获取当前节拍信息

        Returns:
            节拍信息字典
        """
        if (self.current_beat_index < 0 or
                self.current_beat_index >= len(self.beat_data)):
            return {}

        beat = self.beat_data[self.current_beat_index]
        return {
            "index": self.current_beat_index,
            "text": beat.get("text", ""),
            "color": beat.get("color", ""),
            "font_name": beat.get("font_name", ""),
            "font_size": beat.get("font_size", 0),
            "animation": beat.get("animation", ""),
            "position_type": beat.get("position_type", "center"),
            "progress": self.total_progress
        }

    def get_paragraph_info(self) -> Dict[str, Any]:
        """
        获取段落信息

        Returns:
            段落信息字典
        """
        if not self.current_config:
            return {}

        return {
            "name": self.current_config.get("name", ""),
            "description": self.current_config.get("description", ""),
            "total_duration": self.paragraph_duration,
            "beat_count": len(self.beat_data),
            "progress": self.total_progress
        }

    def seek(self, time_seconds: float) -> None:
        """
        跳转到段落内的指定时间点

        Args:
            time_seconds: 段落内部时间（从段落开始算起）
        """
        if not self.current_config or time_seconds < 0:
            return

        # 计算当前应该处于哪个节拍
        accumulated_time = 0.0
        target_beat_index = 0

        for i, beat in enumerate(self.beat_data):
            duration = beat.get("duration", 0)

            if time_seconds < accumulated_time + duration:
                # 找到了当前节拍
                target_beat_index = i
                break
            else:
                accumulated_time += duration
        else:
            # 如果超过了所有节拍，停在最后一个节拍
            target_beat_index = len(self.beat_data) - 1
            accumulated_time = self.paragraph_duration

        # 设置当前状态
        self.current_beat_index = target_beat_index
        self.current_beat_start_time = accumulated_time

        # 标记为正在播放
        self.is_playing = True
        self.start_time = 0
        self.total_progress = time_seconds / self.paragraph_duration if self.paragraph_duration > 0 else 0

    def update_by_time(self, time_seconds: float) -> Optional[Dict[str, Any]]:
        """
        根据段落内部时间更新

        Args:
            time_seconds: 段落内部时间（从段落开始算起）

        Returns:
            渲染数据字典
        """
        if not self.current_config or time_seconds < 0:
            return None

        # 如果还没有开始播放，先seek到当前位置
        if not self.is_playing or self.current_beat_index < 0:
            self.seek(time_seconds)

        # 计算当前节拍
        current_beat = self.beat_data[self.current_beat_index]
        beat_start_time = self.current_beat_start_time
        beat_duration = current_beat.get("duration", 0)

        # 检查是否需要切换到下一个节拍
        if time_seconds >= beat_start_time + beat_duration:
            # 查找当前时间对应的节拍
            accumulated_time = 0.0
            new_beat_index = 0

            for i, beat in enumerate(self.beat_data):
                duration = beat.get("duration", 0)

                if time_seconds < accumulated_time + duration:
                    new_beat_index = i
                    break
                else:
                    accumulated_time += duration
            else:
                # 超过所有节拍
                new_beat_index = len(self.beat_data) - 1
                accumulated_time = self.paragraph_duration

            # 更新节拍索引
            if new_beat_index != self.current_beat_index:
                self.current_beat_index = new_beat_index
                self.current_beat_start_time = accumulated_time
                current_beat = self.beat_data[new_beat_index]
                beat_start_time = accumulated_time

        # 计算当前节拍的进度
        if beat_duration > 0:
            beat_progress = (time_seconds - beat_start_time) / beat_duration
            beat_progress = max(0, min(beat_progress, 1.0))
        else:
            beat_progress = 1.0

        # 更新总进度
        if self.paragraph_duration > 0:
            self.total_progress = time_seconds / self.paragraph_duration
        else:
            self.total_progress = 0

        return self._calculate_frame(current_beat, beat_progress)


# 简单的多段落管理器（如果需要同时播放多个段落）
class MultiParagraphManager:
    """多段落管理器（可同时播放多个段落）"""

    def __init__(self, screen_width: int = 800, screen_height: int = 600):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.players = []  # 播放器列表
        self.next_player_id = 0

    def create_player(self) -> ParagraphPlayer:
        """创建新的播放器实例"""
        player = ParagraphPlayer(self.screen_width, self.screen_height)
        player.id = self.next_player_id
        self.next_player_id += 1
        self.players.append(player)
        return player

    def remove_player(self, player_id: int) -> bool:
        """移除播放器"""
        for i, player in enumerate(self.players):
            if hasattr(player, 'id') and player.id == player_id:
                self.players.pop(i)
                return True
        return False

    def update_all(self, current_time: float) -> List[Dict[str, Any]]:
        """
        更新所有播放器

        Args:
            current_time: 当前时间

        Returns:
            所有播放器的渲染数据列表
        """
        frames = []

        for player in self.players:
            frame = player.update(current_time)
            if frame:
                frames.append(frame)

        return frames

    def clear_all(self) -> None:
        """清除所有播放器"""
        self.players.clear()