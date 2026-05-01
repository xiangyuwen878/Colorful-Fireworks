# some_resources/date_display.py
"""
日期显示模块 - 绝对字体版本
只使用3种指定字体文件，不尝试系统字体
"""

import os
import pygame
from typing import List, Dict, Any, Optional


# 字体加载函数 - 绝对路径强制版本
def get_font(font_name, size):
    """
    获取字体对象 - 绝对路径强制版本
    只从本地fonts文件夹加载指定字体文件，失败时直接报错
    """
    # 字体名称到字体文件的映射
    # 这里只定义我们要用的3种字体
    FONT_MAP = {
        "Segoe Script": "segoesc.ttf",  # 第一种花体字
        "Brush Script MT": "BRUSHSCI.TTF",  # 第二种花体字
        "SimHei": "SIMHEI.TTF",  # 默认字体
    }

    # 检查字体名是否在我们的映射中
    if font_name not in FONT_MAP:
        raise ValueError(f"字体 '{font_name}' 不在允许的字体列表中。只允许: {list(FONT_MAP.keys())}")

    # 获取字体文件名
    font_filename = FONT_MAP[font_name]

    # 查找字体文件的绝对路径
    # 方法1: 尝试在当前脚本所在目录的fonts文件夹
    script_dir = os.path.dirname(os.path.abspath(__file__))
    fonts_dir = os.path.join(script_dir, "fonts")
    font_path = os.path.join(fonts_dir, font_filename)

    # 如果方法1找不到，尝试方法2: 在项目根目录的fonts文件夹
    if not os.path.exists(font_path):
        project_root = os.path.dirname(script_dir)
        fonts_dir = os.path.join(project_root, "fonts")
        font_path = os.path.join(fonts_dir, font_filename)

    # 检查字体文件是否存在
    if not os.path.exists(font_path):
        # 列出可用的字体文件，帮助用户排查
        if os.path.exists(fonts_dir):
            available_fonts = os.listdir(fonts_dir)
            error_msg = f"错误：找不到字体文件 '{font_filename}'\n"
            error_msg += f"搜索路径: {font_path}\n"
            error_msg += f"fonts文件夹中现有的文件:\n"
            for f in available_fonts:
                error_msg += f"  - {f}\n"
            error_msg += f"请确保 '{font_filename}' 文件存在于fonts文件夹中"
        else:
            error_msg = f"错误：fonts文件夹不存在于路径: {fonts_dir}\n"
            error_msg += f"请创建fonts文件夹并放入以下字体文件:\n"
            error_msg += f"  - segoesc.ttf (Segoe Script 花体字)\n"
            error_msg += f"  - BRUSHSCI.TTF (Brush Script MT 花体字)\n"
            error_msg += f"  - SIMHEI.TTF (黑体)"

        print(f"❌ {error_msg}")
        raise FileNotFoundError(f"字体文件未找到: {font_filename}")

    # 尝试加载字体
    try:
        font = pygame.font.Font(font_path, size)
        print(f"✅ 成功加载字体: {font_name} ({font_filename})")
        return font
    except Exception as e:
        print(f"❌ 错误：无法加载字体文件 {font_path}")
        print(f"错误信息: {e}")
        raise Exception(f"字体文件加载失败: {font_filename}")


class DateEffect:
    """
    日期显示效果
    接口与其他烟花模块保持一致
    """

    def __init__(self, screen_width: int = 1600, screen_height: int = 900):
        """
        初始化日期显示效果

        Args:
            screen_width: 屏幕宽度
            screen_height: 屏幕高度
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # 状态变量
        self.is_active = False
        self.start_time = 0.0
        self.duration = 7.5  # 固定7.5秒

        # 动画参数（基于时间而非帧数）
        self.fade_in_time = 1.417  # 淡入时间（秒）
        self.stay_time = 4.667  # 停留时间（秒）
        self.fade_out_time = 1.417  # 淡出时间（秒）

        # 字体和颜色
        self.year_text = "2026"
        self.date_text = "0626"
        self.color = (173, 216, 230)  # 浅蓝色

        # 字体相关
        self.font = None
        self.year_surface = None
        self.date_surface = None
        self.year_pos = None
        self.date_pos = None

        # 初始化字体
        self._init_fonts()

    def _init_fonts(self):
        """初始化字体 - 只尝试3种指定字体，全部失败则报错"""
        font_size = self.screen_height // 5

        # 只尝试这3种字体，按优先级顺序
        font_names = [
            "Segoe Script",  # 第一种花体字
            "Brush Script MT",  # 第二种花体字
            "SimHei",  # 默认字体
        ]

        for font_name in font_names:
            try:
                # 使用绝对路径加载字体
                self.font = get_font(font_name, font_size)

                # 测试字体渲染是否正常
                test_surface = self.font.render("2026", True, self.color)
                if test_surface.get_width() > 0:
                    print(f"✅ 日期显示成功加载字体: {font_name}")

                    # 创建实际要显示的文字表面
                    self.year_surface = self.font.render(self.year_text, True, self.color)
                    self.date_surface = self.font.render(self.date_text, True, self.color)

                    # 计算位置
                    self._calculate_positions()
                    return  # 成功加载，直接返回
                else:
                    print(f"⚠️ 字体 {font_name} 渲染测试失败，尝试下一种字体")
            except Exception as e:
                print(f"❌ 字体 {font_name} 加载失败: {e}")
                if font_name == "SimHei":  # 如果是最后一种字体也失败
                    print("❌ 所有指定字体加载失败！程序无法继续运行。")
                    raise Exception("日期显示字体加载失败，程序终止。")
                # 继续尝试下一种字体

        # 如果循环结束还没成功（理论上不会执行到这里）
        raise Exception("字体加载失败，程序终止。")

    def _calculate_positions(self):
        """计算文字位置"""
        center_x = self.screen_width // 2

        # 获取文字尺寸
        year_width, year_height = self.year_surface.get_size()
        date_width, date_height = self.date_surface.get_size()

        # 左边年份位置
        year_x = (center_x - year_width) // 2
        year_y = self.screen_height - year_height - 80  # 距离底部80像素
        self.year_pos = (year_x, year_y)

        # 右边日期位置
        date_x = center_x + (center_x - date_width) // 2
        date_y = self.screen_height - date_height - 80  # 距离底部80像素
        self.date_pos = (date_x, date_y)

    def activate(self, start_time: float, duration: Optional[float] = None) -> None:
        """
        激活日期显示效果

        Args:
            start_time: 开始时间（秒）
            duration: 持续时间（秒），忽略此参数，固定为7.5秒
        """
        self.is_active = True
        self.start_time = start_time

    def deactivate(self) -> None:
        """停用效果"""
        self.is_active = False

    def clear_all(self) -> None:
        """清除效果（重置状态）"""
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

        # 计算经过时间
        elapsed_time = current_time - self.start_time
        if elapsed_time < 0:
            return None  # 还未开始

        # 检查是否结束
        if elapsed_time >= self.duration:
            self.is_active = False
            return None

        # 计算透明度
        alpha = self._calculate_alpha(elapsed_time)
        if alpha <= 0:
            return None

        # 返回绘制命令
        draw_commands = []

        # 年份绘制命令
        if self.year_surface and self.year_pos:
            # 创建带透明度的副本
            year_surface_copy = self.year_surface.copy()
            year_surface_copy.set_alpha(alpha)
            draw_commands.append({
                "type": "text_surface",
                "surface": year_surface_copy,
                "position": self.year_pos
            })

        # 日期绘制命令
        if self.date_surface and self.date_pos:
            # 创建带透明度的副本
            date_surface_copy = self.date_surface.copy()
            date_surface_copy.set_alpha(alpha)
            draw_commands.append({
                "type": "text_surface",
                "surface": date_surface_copy,
                "position": self.date_pos
            })

        return draw_commands if draw_commands else None

    def _calculate_alpha(self, elapsed_time: float) -> int:
        """
        根据经过时间计算透明度

        Args:
            elapsed_time: 经过时间（秒）

        Returns:
            透明度值（0-255）
        """
        if elapsed_time < 0:
            return 0
        elif elapsed_time < self.fade_in_time:
            # 淡入阶段
            progress = elapsed_time / self.fade_in_time
            return int(progress * 255)
        elif elapsed_time < self.fade_in_time + self.stay_time:
            # 停留阶段
            return 255
        elif elapsed_time < self.fade_in_time + self.stay_time + self.fade_out_time:
            # 淡出阶段
            fade_out_elapsed = elapsed_time - (self.fade_in_time + self.stay_time)
            progress = fade_out_elapsed / self.fade_out_time
            return int((1.0 - progress) * 255)
        else:
            # 结束
            return 0

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
            "start_time": self.start_time,
            "duration": self.duration
        }