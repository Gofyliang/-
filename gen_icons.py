"""
生成倒计时轮盘安卓版的 icon.png 和 presplash.png
不需要额外依赖，用纯 Pillow 实现
"""
import math
from PIL import Image, ImageDraw, ImageFont

def draw_wheel(draw, cx, cy, radius, walked=0.0, bg_color=(10,10,42), ring_color=(26,74,26)):
    """绘制轮盘圆环"""
    # 底环
    for angle_deg in range(360):
        a = math.radians(angle_deg - 90)
        x1 = cx + (radius - 12) * math.cos(a)
        y1 = cy + (radius - 12) * math.sin(a)
        x2 = cx + (radius + 12) * math.cos(a)
        y2 = cy + (radius + 12) * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=ring_color, width=1)

    # 进度弧（已走过用背景色覆盖）
    if walked > 0:
        for angle_deg in range(int(walked * 360)):
            a = math.radians(angle_deg - 90)
            x1 = cx + (radius - 13) * math.cos(a)
            y1 = cy + (radius - 13) * math.sin(a)
            x2 = cx + (radius + 13) * math.cos(a)
            y2 = cy + (radius + 13) * math.sin(a)
            draw.line([(x1, y1), (x2, y2)], fill=bg_color, width=1)

    # 刻度
    for i in range(60):
        a = math.radians(i * 6 - 90)
        major = (i % 5 == 0)
        r1 = radius - (24 if major else 18)
        r2 = radius - (10 if major else 8)
        lw = 3 if major else 1
        filled = i < int(walked * 60)
        if filled:
            color = bg_color
        else:
            color = (170, 170, 204) if major else (136, 136, 153)
        x1 = cx + r1 * math.cos(a)
        y1 = cy + r1 * math.sin(a)
        x2 = cx + r2 * math.cos(a)
        y2 = cy + r2 * math.sin(a)
        draw.line([(x1, y1), (x2, y2)], fill=color, width=lw)

    # 指针
    ang = math.radians(walked * 360 - 90)
    px = cx + (radius - 8) * math.cos(ang)
    py = cy + (radius - 8) * math.sin(ang)
    bx1 = cx + 50 * math.cos(ang + 0.12)
    by1 = cy + 50 * math.sin(ang + 0.12)
    bx2 = cx + 50 * math.cos(ang - 0.12)
    by2 = cy + 50 * math.sin(ang - 0.12)
    draw.polygon([(px, py), (bx1, by1), (bx2, by2)], fill=(230, 230, 255))
    # 中心点
    draw.ellipse([cx - 10, cy - 10, cx + 10, cy + 10], fill=(230, 230, 255))
    draw.ellipse([cx - 5, cy - 5, cx + 5, cy + 5], fill=bg_color)


def make_icon(size=512):
    """生成应用图标 512x512"""
    img = Image.new('RGBA', (size, size), (10, 10, 42, 255))
    draw = ImageDraw.Draw(img)

    # 圆形背景
    margin = 20
    draw.ellipse([margin, margin, size - margin, size - margin], fill=(10, 10, 42))

    # 轮盘
    cx, cy = size // 2, size // 2
    radius = (size - 80) // 2
    draw_wheel(draw, cx, cy, radius, walked=0.35, bg_color=(10, 10, 42))

    # 时间文字 "05:30"
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size // 4)
        small_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", size // 14)
    except:
        font = ImageFont.load_default()
        small_font = font

    text = "05:30"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2 - 10), text, fill=(255, 255, 255), font=font)

    # 标题
    title = "⏱ 倒计时"
    bbox2 = draw.textbbox((0, 0), title, font=small_font)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, 40), title, fill=(200, 200, 220), font=small_font)

    # 圆角遮罩
    mask = Image.new('L', (size, size), 0)
    mask_draw = ImageDraw.Draw(mask)
    mask_draw.ellipse([0, 0, size, size], fill=255)
    img.putalpha(mask)

    img.save(r"E:\Programs\WorkBuddy\倒计时轮盘\安卓版本\icon.png")
    print("icon.png 已生成")


def make_presplash():
    """生成启动画面 1242x2448 (全屏竖屏)"""
    w, h = 1242, 2448
    img = Image.new('RGB', (w, h), (10, 10, 42))
    draw = ImageDraw.Draw(img)

    # 渐变背景效果
    for y in range(h):
        ratio = y / h
        r = int(10 + 5 * ratio)
        g = int(10 + 5 * ratio)
        b = int(42 + 20 * ratio)
        draw.line([(0, y), (w, y)], fill=(r, g, b))

    # 轮盘
    cx, cy = w // 2, h // 2 - 100
    radius = min(w, h) // 3
    draw_wheel(draw, cx, cy, radius, walked=0.25, bg_color=(10, 10, 42))

    # 时间文字
    try:
        font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 160)
        title_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 72)
        sub_font = ImageFont.truetype("C:/Windows/Fonts/msyh.ttc", 48)
    except:
        font = ImageFont.load_default()
        title_font = font
        sub_font = font

    text = "05:30"
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    draw.text((cx - tw // 2, cy - th // 2), text, fill=(255, 255, 255), font=font)

    # 标题
    title = "倒计时轮盘"
    bbox2 = draw.textbbox((0, 0), title, font=title_font)
    tw2 = bbox2[2] - bbox2[0]
    draw.text((cx - tw2 // 2, cy + radius + 80), title, fill=(200, 200, 220), font=title_font)

    # 署名
    sub = "Gofy高飞团队出品"
    bbox3 = draw.textbbox((0, 0), sub, font=sub_font)
    tw3 = bbox3[2] - bbox3[0]
    draw.text((cx - tw3 // 2, h - 200), sub, fill=(120, 120, 140), font=sub_font)

    img.save(r"E:\Programs\WorkBuddy\倒计时轮盘\安卓版本\presplash.png")
    print("presplash.png 已生成")


if __name__ == "__main__":
    make_icon()
    make_presplash()
