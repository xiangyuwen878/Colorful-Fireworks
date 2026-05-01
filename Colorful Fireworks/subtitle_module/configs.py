# subtitle_module/configs.py
"""
段落配置文件
功能：定义各个段落的详细配置
注意：这里是纯数据配置，不包含任何播放逻辑
"""


"""
create_transition_1_paragraph
create_louder_paragraph
create_lively_paragraph
create_vitality_paragraph
create_universe_paragraph
create_full_yanhua_paragraph
create_rebirth_paragraph
create_eternal_paragraph
create_transition_2_paragraph
"""


from typing import Dict, Any

def create_transition_1_paragraph() -> Dict[str, Any]:
    """
    创建过渡段落1 (transition_1)
    时间：4秒到17秒，共13秒，8个节拍
    节拍间隔：1.625秒（除了第7个节拍是1.625 * 1.75秒）
    """
    return {
        "name": "transition_1",
        "description": "过渡・时光节拍 4~17秒",
        "start_time": 4.0,  # 参考开始时间
        "total_duration": 13.0,  # 8个节拍
        "beats": [
            # 节拍1: 4.000秒 - 重音1
            {
                "text": "时光",
                "color": "lightcyan",        # 颜色
                "font_name": "华文宋体",     # 字体
                "duration": 1.625,          # 持续时间
                "font_size": 60,            # 字体大小
                "animation": "fade",         # 动画效果：淡入淡出
                "position": "center"         # 位置：中间
            },
            # 节拍2: 5.625秒 - 轻音1
            {
                "text": "是一条长河",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.625,
                "font_size": 60,
                "animation": "fade",
                "position": "top"            # 位置：上面
            },
            # 节拍3: 7.250秒 - 重音2
            {
                "text": "静默与奔流",
                "color": "lavender",        # 更换颜色
                "font_name": "KaiTi",       # 更换字体
                "duration": 1.625,
                "font_size": 60,
                "animation": "slide",        # 动画效果：滑动进入
                "position": "bottom"         # 位置：下面
            },
            # 节拍4: 8.875秒 - 轻音2
            {
                "text": "声响不息",
                "color": "lavender",
                "font_name": "KaiTi",
                "duration": 1.625,
                "font_size": 60,
                "animation": "slide",
                "position": "top"            # 位置：上面
            },
            # 节拍5: 10.500秒 - 重音3
            {
                "text": "它淘洗昨日",       # 修正：去掉"所有"
                "color": "honeydew",        # 更换颜色
                "font_name": "华文楷体",   # 更换字体
                "duration": 1.625,
                "font_size": 60,
                "animation": "zoom",         # 动画效果：缩放效果
                "position": "bottom"         # 位置：下面
            },
            # 节拍6: 12.125秒 - 轻音3
            {
                "text": "凝结成",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.625,
                "font_size": 60,
                "animation": "zoom",
                "position": "center"         # 位置：中间
            },
            # 节拍7: 13.750秒 - 重音4
            {
                "text": "此刻的 “我” ",      # 修正：添加空格，使用中文引号
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.625 * 1.75,  # 1.625 * 1.75
                "font_size": 60,
                "animation": "zoom",
                "position": "center"         # 位置：中间
            },
            # 节拍8: 15.375秒 - 轻音4
            {
                "text": "",  # 没有内容
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.625,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "zoom",
                "position": "center"         # 位置：中间
            }
        ]
    }

def create_louder_paragraph() -> Dict[str, Any]:
    """
    创建Louder段落 (加重・破土宣言)
    时间：17秒到31秒，共14秒，8个节拍
    节拍间隔：1.75秒，除了第15个节拍是1.75 * 1.75
    """
    return {
        "name": "louder",
        "description": "加重・破土宣言 17~31秒",
        "start_time": 17.0,  # 参考开始时间
        "total_duration": 14.0,  # 8个节拍
        "beats": [
            # 节拍9: 17.000秒
            {
                "text": "我",
                "color": "lightsteelblue",  # 颜色
                "font_name": "华文宋体",    # 字体
                "duration": 1.75,         # 持续时间
                "font_size": 60,           # 字体大小
                "animation": "zoom",        # 动画效果：缩放效果
                "position": "center"       # 位置：中间
            },
            # 节拍10: 18.750秒
            {
                "text": "破茧而出",
                "color": "lightsteelblue",
                "font_name": "华文宋体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "zoom",
                "position": "top"          # 位置：上面
            },
            # 节拍11: 20.500秒
            {
                "text": "躯壳与黑暗",
                "color": "lightblue",      # 更换颜色
                "font_name": "KaiTi",      # 更换字体
                "duration": 1.75,
                "font_size": 60,
                "animation": "typewriter",  # 动画效果：打字机效果
                "position": "center"       # 位置：中间
            },
            # 节拍12: 22.250秒
            {
                "text": "应声碎裂",
                "color": "lightblue",
                "font_name": "KaiTi",
                "duration": 1.75,
                "font_size": 60,
                "animation": "typewriter",
                "position": "center"       # 位置：中间
            },
            # 节拍13: 24.000秒
            {
                "text": "以此新生",
                "color": "aliceblue",      # 更换颜色
                "font_name": "华文楷体",  # 更换字体
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",        # 动画效果：淡入淡出
                "position": "top"          # 位置：上面
            },
            # 节拍14: 25.750秒
            {
                "text": "向光而立",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "bottom"       # 位置：下面
            },
            # 节拍15: 27.500秒
            {
                "text": "野蛮生长",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.75 * 1.75,  # 注意：这里是乘法表达式，计算结果为3.0625秒
                "font_size": 60,
                "animation": "fade",
                "position": "center"       # 位置：中间
            },
            # 节拍16: 29.250秒
            {
                "text": "",  # 没有内容
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.75,  # 最后1.75秒
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "fade",
                "position": "center"       # 位置：中间
            }
        ]
    }

def create_lively_paragraph() -> Dict[str, Any]:
    """
    创建Lively段落 (欢快・自我庆典)
    时间：31秒到58秒，共27秒，16个节拍
    节拍间隔：1.688秒
    """
    return {
        "name": "lively",
        "description": "欢快・自我庆典 31~58秒",
        "start_time": 31.0,  # 参考开始时间
        "total_duration": 27.0,  # 16个节拍
        "beats": [
            # 节拍17: 31.000秒
            {
                "text": "今日如歌",
                "color": "lightpink",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍18: 32.688秒
            {
                "text": "被光镀过",
                "color": "lightpink",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍19: 34.376秒
            {
                "text": "用蜜酿成",
                "color": "lightpink",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍20: 36.064秒
            {
                "text": "2026 . 0619",
                "color": "lavenderblush",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍21: 37.752秒
            {
                "text": "坐标已亮起",
                "color": "lavenderblush",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "top"  # 位置：上面
            },
            # 节拍22: 39.440秒
            {
                "text": "名为 “我” 的星",
                "color": "lavenderblush",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍23: 41.128秒
            {
                "text": "我转身",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍24: 42.816秒
            {
                "text": "对自己发出邀请函",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍25: 44.504秒
            {
                "text": "上面只写着",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍26: 46.192秒
            {
                "text": "HappyBirthday",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍27: 47.880秒
            {
                "text": "这声祝福",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍28: 49.568秒
            {
                "text": "是庆典的开幕致辞",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍29: 51.256秒
            {
                "text": "庆贺生命",
                "color": "aliceblue",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上间
            },
            # 节拍30: 52.944秒
            {
                "text": "庆贺此刻",
                "color": "aliceblue",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍31: 54.632秒
            {
                "text": "庆祝我即是我",
                "color": "aliceblue",
                "font_name": "华文宋体",
                "duration": 1.688 * 1.75,  # 注意：这里是乘法表达式
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍32: 56.320秒
            {
                "text": "",  # 没有内容
                "color": "aliceblue",
                "font_name": "华文宋体",
                "duration": 1.688,  # 最后1.688秒
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            }
        ]
    }

def create_vitality_paragraph() -> Dict[str, Any]:
    """
    创建Vitality段落 (生命力・成长之诗)
    时间：58秒到85秒，共27秒，16个节拍
    节拍间隔：1.688秒（除了第47个节拍是1.688 * 1.75秒）
    """
    return {
        "name": "vitality",
        "description": "生命力・成长之诗 58~85秒",
        "start_time": 58.0,  # 参考开始时间
        "total_duration": 27.0,  # 16个节拍
        "beats": [
            # 节拍33: 58.000秒
            {
                "text": "根须延伸",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍34: 59.688秒
            {
                "text": "向黑暗深处",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍35: 61.376秒
            {
                "text": "献出沉默之力",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍36: 63.064秒
            {
                "text": "为枝叶奠基",
                "color": "mintcream",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍37: 64.752秒
            {
                "text": "迎来光的交响",
                "color": "mintcream",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍38: 66.440秒
            {
                "text": "每圈年轮",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍39: 68.128秒
            {
                "text": "都是",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍40: 69.816秒
            {
                "text": "时光之诗",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍41: 71.504秒
            {
                "text": "是生命",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "top"  # 位置：上面
            },
            # 节拍42: 73.192秒
            {
                "text": "赠予我的",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "bottom"  # 位置：下面
            },
            # 节拍43: 74.880秒
            {
                "text": "沉默勋章",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍44: 76.568秒
            {
                "text": "而我",
                "color": "aliceblue",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍45: 78.256秒
            {
                "text": "仍在生长",
                "color": "aliceblue",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍46: 79.944秒
            {
                "text": "不断生长",
                "color": "aliceblue",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍47: 81.632秒
            {
                "text": "永续生长",
                "color": "aliceblue",
                "font_name": "华文仿宋",
                "duration": 1.688 * 1.75,  # 注意：这是表达式
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍48: 83.320秒
            {
                "text": "",  # 没有内容
                "color": "aliceblue",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            }
        ]
    }

def create_universe_paragraph() -> Dict[str, Any]:
    """
    创建Universe段落 (生命力加强・内在宇宙)
    时间：85秒到113秒，共28秒，16个节拍
    节拍间隔：1.750秒（除了第63个节拍是1.750 * 1.75秒）
    """
    return {
        "name": "universe",
        "description": "生命力加强・内在宇宙 85~113秒",
        "start_time": 85.0,  # 参考开始时间
        "total_duration": 28.0,  # 16个节拍
        "beats": [
            # 节拍49: 85.000秒
            {
                "text": "我",
                "color": "lightsteelblue",
                "font_name": "华文宋体",
                "duration": 1.750,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍50: 86.750秒
            {
                "text": "不止是一棵树",
                "color": "lightsteelblue",
                "font_name": "华文宋体",
                "duration": 1.750,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍51: 88.500秒
            {
                "text": "我体内",
                "color": "lavender",
                "font_name": "华文楷体",  # 修正：改为华文楷体
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍52: 90.250秒
            {
                "text": "自成宇宙",
                "color": "lavender",
                "font_name": "华文楷体",  # 修正：改为华文楷体
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍53: 92.000秒
            {
                "text": "有季风奔涌",
                "color": "lavender",
                "font_name": "华文楷体",  # 修正：改为华文楷体
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍54: 93.750秒
            {
                "text": "有星辰生灭",
                "color": "lavender",
                "font_name": "华文楷体",  # 修正：改为华文楷体
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍55: 95.500秒
            {
                "text": "有星空流转",
                "color": "lavender",
                "font_name": "华文楷体",  # 修正：改为华文楷体
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍56: 97.250秒
            {
                "text": "我的呼吸",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍57: 99.000秒
            {
                "text": "便是潮汐",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍58: 100.750秒
            {
                "text": "我的血脉",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍59: 102.500秒
            {
                "text": "便是江河",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍60: 104.250秒
            {
                "text": "我每一次心跳",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍61: 106.000秒
            {
                "text": "都与世界共振",
                "color": "lightblue",
                "font_name": "FangSong",
                "duration": 1.750,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍62: 107.750秒
            {
                "text": "我即是",
                "color": "mistyrose",  # 修正：改为mistyrose
                "font_name": "华文仿宋",  # 修正：改为华文仿宋
                "duration": 1.750,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍63: 109.500秒
            {
                "text": "万物生灵",
                "color": "mistyrose",  # 修正：改为mistyrose
                "font_name": "华文仿宋",  # 修正：改为华文仿宋
                "duration": 1.750 * 1.75,  # 注意：这是表达式
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍64: 111.250秒
            {
                "text": "",  # 没有内容
                "color": "mistyrose",  # 修正：改为mistyrose
                "font_name": "华文仿宋",  # 修正：改为华文仿宋
                "duration": 1.750,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            }
        ]
    }

def create_full_firework_paragraph() -> Dict[str, Any]:
    """
    创建烟花段落 (烟花盛典)
    时间：113秒到140秒，共27秒，16个节拍
    节拍间隔：1.688秒（除了第79个节拍是1.688 * 1.75秒）
    """
    return {
        "name": "full_firework",  # 修改段落名称
        "description": "烟花盛典 113~140秒",
        "start_time": 113.0,  # 参考开始时间
        "total_duration": 27.0,  # 16个节拍
        "beats": [
            # 节拍65: 113.000秒
            {
                "text": "夜幕",
                "color": "lightblue",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍66: 114.688秒
            {
                "text": "是最广阔的",
                "color": "lightblue",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍67: 116.376秒
            {
                "text": "画布",
                "color": "lightblue",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍68: 118.064秒
            {
                "text": "光点持续迸发",
                "color": "lightpink",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍69: 119.752秒
            {
                "text": "向上飞升",
                "color": "lightpink",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍70: 121.440秒
            {
                "text": "看那螺旋的轨迹",
                "color": "lavenderblush",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍71: 123.128秒
            {
                "text": "摇曳着攀升",
                "color": "lavenderblush",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍72: 124.816秒
            {
                "text": "抵达至高",
                "color": "lavenderblush",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍73: 126.504秒
            {
                "text": "轰然绽开",
                "color": "lavenderblush",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍74: 128.192秒
            {
                "text": "再次绽开",
                "color": "lavenderblush",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍75: 129.880秒
            {
                "text": "轰鸣与光芒交织",
                "color": "mistyrose",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "top"  # 位置：上面
            },
            # 节拍76: 131.568秒
            {
                "text": "成不休乐章",
                "color": "mistyrose",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "bottom"  # 位置：下面
            },
            # 节拍77: 133.256秒
            {
                "text": "这就是",
                "color": "lightcyan",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍78: 134.944秒
            {
                "text": "我",
                "color": "lightcyan",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍79: 136.632秒
            {
                "text": "生命的庆典",
                "color": "lightcyan",
                "font_name": "华文仿宋",
                "duration": 1.688 * 1.75,  # 注意：这是表达式
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍80: 138.320秒
            {
                "text": "",  # 没有内容
                "color": "lightcyan",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            }
        ]
    }

def create_rebirth_paragraph() -> Dict[str, Any]:
    """
    创建重生段落 (生命力恢复・重生之焰)
    时间：140秒到168秒，共28秒，16个节拍
    节拍间隔：1.75秒（除了第95个节拍是1.75 * 1.75秒）
    """
    return {
        "name": "rebirth",
        "description": "生命力恢复・重生之焰 140~168秒",
        "start_time": 140.0,
        "total_duration": 28.0,
        "beats": [
            # 节拍81: 140.000秒
            {
                "text": "盛大的烟花",
                "color": "lightsteelblue",
                "font_name": "华文宋体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "center"
            },
            # 节拍82: 141.750秒
            {
                "text": "光屑如雨",
                "color": "lightsteelblue",
                "font_name": "华文宋体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "bottom"
            },
            # 节拍83: 143.500秒
            {
                "text": "光点缓缓飘坠",
                "color": "mistyrose",
                "font_name": "KaiTi",
                "duration": 1.75,
                "font_size": 60,
                "animation": "slide",
                "position": "top"
            },
            # 节拍84: 145.250秒
            {
                "text": "落为余温",
                "color": "mistyrose",
                "font_name": "KaiTi",
                "duration": 1.75,
                "font_size": 60,
                "animation": "slide",
                "position": "bottom"
            },
            # 节拍85: 147.000秒
            {
                "text": "沉作余烬",
                "color": "mistyrose",
                "font_name": "KaiTi",
                "duration": 1.75,
                "font_size": 60,
                "animation": "slide",
                "position": "top"
            },
            # 节拍86: 148.750秒
            {
                "text": "灰烬之下",
                "color": "lightpink",
                "font_name": "FangSong",
                "duration": 1.75,
                "font_size": 60,
                "animation": "typewriter",
                "position": "center"
            },
            # 节拍87: 150.500秒
            {
                "text": "仍能听见",
                "color": "lightpink",
                "font_name": "FangSong",
                "duration": 1.75,
                "font_size": 60,
                "animation": "typewriter",
                "position": "center"
            },
            # 节拍88: 152.250秒
            {
                "text": "星火低鸣",
                "color": "lightpink",
                "font_name": "FangSong",
                "duration": 1.75,
                "font_size": 60,
                "animation": "typewriter",
                "position": "center"
            },
            # 节拍89: 154.000秒
            {
                "text": "沉默不是结局",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "zoom",
                "position": "bottom"
            },
            # 节拍90: 155.750秒
            {
                "text": "而是",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "zoom",
                "position": "top"
            },
            # 节拍91: 157.500秒
            {
                "text": "力量的序言",
                "color": "honeydew",
                "font_name": "华文楷体",
                "duration": 1.75,
                "font_size": 60,
                "animation": "zoom",
                "position": "center"
            },
            # 节拍92: 159.250秒
            {
                "text": "我将",
                "color": "lavenderblush",
                "font_name": "华文仿宋",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "bottom"
            },
            # 节拍93: 161.000秒
            {
                "text": "再次燃起",
                "color": "lavenderblush",
                "font_name": "华文仿宋",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "top"
            },
            # 节拍94: 162.750秒
            {
                "text": "更为炽烈",
                "color": "lavenderblush",
                "font_name": "华文仿宋",
                "duration": 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "center"
            },
            # 节拍95: 164.500秒
            {
                "text": "更为磅礴",
                "color": "lavenderblush",
                "font_name": "华文仿宋",
                "duration": 1.75 * 1.75,
                "font_size": 60,
                "animation": "fade",
                "position": "center"
            },
            # 节拍96: 166.250秒
            {
                "text": "",
                "color": "lavenderblush",
                "font_name": "华文仿宋",
                "duration": 1.75,
                "font_size": 0,
                "animation": "fade",
                "position": "center"
            }
        ]
    }

def create_eternal_paragraph() -> Dict[str, Any]:
    """
    创建永恒段落 (生命力再次增强・永恒回响)
    时间：168秒到195秒，共27秒，16个节拍
    节拍间隔：1.688秒（除了第111个节拍是1.688 * 1.75秒）
    """
    return {
        "name": "eternal",
        "description": "生命力再次增强・永恒回响 168~195秒",
        "start_time": 168.0,  # 参考开始时间
        "total_duration": 27.0,  # 16个节拍
        "beats": [
            # 节拍97: 168.000秒
            {
                "text": "我生发的光",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍98: 169.688秒
            {
                "text": "自此独立",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍99: 171.376秒
            {
                "text": "无需黑夜",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "top"  # 位置：上面
            },
            # 节拍100: 173.064秒
            {
                "text": "映衬与定义",
                "color": "lightcyan",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍101: 174.752秒
            {
                "text": "长夜已尽",
                "color": "aliceblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍102: 176.440秒
            {
                "text": "我抵达黎明",
                "color": "aliceblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍103: 178.128秒
            {
                "text": "并成为黎明",
                "color": "aliceblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 修正：改为top（上面）
            },
            # 节拍104: 179.816秒
            {
                "text": "我即是",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "bottom"  # 位置：下面
            },
            # 节拍105: 181.504秒
            {
                "text": "不灭恒星",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍106: 183.192秒
            {
                "text": "我即是",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "top"  # 位置：上面
            },
            # 节拍107: 184.880秒
            {
                "text": "永恒太阳",
                "color": "mintcream",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍108: 186.568秒
            {
                "text": "自是轨迹",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍109: 188.256秒
            {
                "text": "自是光焰",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍110: 189.944秒
            {
                "text": "自是宇宙",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍111: 191.632秒
            {
                "text": "自是本源",
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688 * 1.75,  # 注意：这是表达式
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍112: 193.320秒
            {
                "text": "",  # 没有内容
                "color": "lavender",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            }
        ]
    }

def create_transition_2_paragraph() -> Dict[str, Any]:
    """
    创建过渡段落2 (过渡・归于中心)
    时间：195秒到222秒，共27秒，16个节拍
    节拍间隔：1.688秒（除了第127个节拍是1.688 * 1.75秒）
    """
    return {
        "name": "transition_2",
        "description": "过渡・归于中心 195~222秒",
        "start_time": 195.0,  # 参考开始时间
        "total_duration": 27.0,  # 16个节拍
        "beats": [
            # 节拍113: 195.000秒
            {
                "text": "最后的声浪",
                "color": "lavender",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍114: 196.688秒
            {
                "text": "已然平息",
                "color": "lavender",
                "font_name": "华文宋体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍115: 198.376秒
            {
                "text": "世界复归",
                "color": "lightblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍116: 200.064秒
            {
                "text": "我转身归来",
                "color": "lightblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "bottom"  # 位置：下面
            },
            # 节拍117: 201.752秒
            {
                "text": "回归静寂原点",
                "color": "lightblue",
                "font_name": "KaiTi",
                "duration": 1.688,
                "font_size": 60,
                "animation": "slide",  # 滑动进入
                "position": "top"  # 位置：上面
            },
            # 节拍118: 203.440秒
            {
                "text": "如古树安驻",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍119: 205.128秒
            {
                "text": "根系深沉",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍120: 206.816秒
            {
                "text": "如湖泊静默",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍121: 208.504秒
            {
                "text": "映照苍穹",
                "color": "honeydew",
                "font_name": "FangSong",
                "duration": 1.688,
                "font_size": 60,
                "animation": "typewriter",  # 打字机效果
                "position": "center"  # 位置：中间
            },
            # 节拍122: 210.192秒
            {
                "text": "收束所有回响",
                "color": "mistyrose",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "center"  # 位置：中间
            },
            # 节拍123: 211.880秒
            {
                "text": "归于中心寂静",
                "color": "mistyrose",
                "font_name": "华文仿宋",
                "duration": 1.688,
                "font_size": 60,
                "animation": "fade",  # 淡入淡出
                "position": "bottom"  # 位置：下面
            },
            # 节拍124: 213.568秒
            {
                "text": "在原点之中",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍125: 215.256秒
            {
                "text": "我完整",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "top"  # 位置：上面
            },
            # 节拍126: 216.944秒
            {
                "text": "我自足",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "bottom"  # 位置：下面
            },
            # 节拍127: 218.632秒
            {
                "text": "圆满如初",
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.688 * 1.75,  # 注意：这是表达式
                "font_size": 60,
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            },
            # 节拍128: 220.320秒
            {
                "text": "",  # 没有内容
                "color": "aliceblue",
                "font_name": "华文楷体",
                "duration": 1.688,
                "font_size": 0,  # 字体大小为0，不显示
                "animation": "zoom",  # 缩放效果
                "position": "center"  # 位置：中间
            }
        ]
    }
