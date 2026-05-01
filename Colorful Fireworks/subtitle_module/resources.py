# subtitle_module/resources.py

import os
import pygame

"""
资源仓库模块
功能：集中管理所有颜色、字体、动画资源定义
特点：纯数据定义，不包含任何逻辑
"""

# ============================
# 颜色资源库 - 10种颜色，全部使用RGB值
# ============================
COLORS = {
    "lightpink": (255, 182, 193),  # 1. 浅粉色
    "lightsteelblue": (176, 196, 222),  # 2. 浅钢蓝色
    "lightcyan": (224, 255, 255),  # 3. 浅青色
    "lavenderblush": (255, 240, 245),  # 4. 淡紫红色
    "honeydew": (240, 255, 240),  # 5. 蜜露色
    "aliceblue": (240, 248, 255),  # 6. 爱丽丝蓝
    "mintcream": (245, 255, 250),  # 7. 薄荷奶油色
    "lightblue": (173, 216, 230),  # 8. 浅蓝色
    "lavender": (230, 230, 250),  # 9. 薰衣草色
    "mistyrose": (255, 228, 225)  # 10. 雾玫瑰色
}

# ============================
# 字体资源库 - 5种主字体
FONT_PATHS = {
    "FangSong": "fonts/SIMFANG.TTF",         # 仿宋
    "KaiTi": "fonts/SIMKAI.TTF",             # 楷体
    "华文仿宋": "fonts/STFANGSO.TTF",         # 华文仿宋
    "华文楷体": "fonts/STKAITI.TTF",          # 华文楷体
    "华文宋体": "fonts/SIMSUN.TTC",           # 华文宋体
    "SimHei": "fonts/SIMHEI.TTF",            # 黑体（最保险的字体）

    "default": "fonts/SIMHEI.TTF"            # 默认字体
}

# ============================
# 动画资源库 - 4种动画类型
# ============================
ANIMATIONS = [
    "typewriter",  # 1. 打字机效果
    "fade",  # 2. 淡入淡出
    "slide",  # 3. 滑动进入
    "zoom"  # 4. 缩放效果
]


# ============================
# 辅助函数
# ============================
def get_color(color_name):
    """
    获取颜色RGB值

    Args:
        color_name: 颜色名称

    Returns:
        tuple: RGB颜色值，如果颜色不存在则返回白色(255, 255, 255)
    """
    return COLORS.get(color_name, (255, 255, 255))



def validate_animation(animation_name):
    """
    验证动画类型是否可用

    Args:
        animation_name: 动画名称

    Returns:
        bool: 动画是否在可用动画列表中
    """
    return animation_name in ANIMATIONS


def get_all_colors():
    """
    获取所有可用颜色名称

    Returns:
        list: 所有颜色名称列表
    """
    return list(COLORS.keys())


def get_all_animations():
    """
    获取所有可用动画类型

    Returns:
        list: 所有动画类型列表
    """
    return ANIMATIONS.copy()


def get_font(font_name, size):
    """
    获取字体对象

    Args:
        font_name: 字体名称
        size: 字体大小

    Returns:
        pygame.font.Font 对象
    """
    # 检查字体名称是否在路径映射中
    if font_name in FONT_PATHS:
        font_path = FONT_PATHS[font_name]

        # 如果指定了字体文件路径
        if font_path and os.path.exists(font_path):
            try:
                return pygame.font.Font(font_path, size)
            except Exception as e:
                print(f"警告：无法加载字体文件 {font_path}，错误: {e}")

    # 对于花体字和其他系统字体，尝试直接使用系统字体
    try:
        return pygame.font.SysFont(font_name, size)
    except Exception as e:
        print(f"警告：无法使用系统字体 {font_name}，错误: {e}")

    # 回退方案：使用默认字体文件
    default_path = FONT_PATHS.get("default")
    if default_path and os.path.exists(default_path):
        try:
            return pygame.font.Font(default_path, size)
        except:
            pass

    # 最后回退：使用系统默认无衬线字体
    return pygame.font.SysFont("sans-serif", size)