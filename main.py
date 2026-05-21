#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
倒计时轮盘 - 安卓竖屏版 (Kivy)
Gofy高飞团队出品
适配手机竖屏，圆形轮盘在上，控制面板在下
"""
import time, math
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.floatlayout import FloatLayout
from kivy.graphics import Color, Ellipse, Line, Rectangle
from kivy.core.text import Label as CoreLabel
from kivy.core.audio import SoundLoader

# ── 颜色 (RGBA 0~1) ──
C_BG     = (0.04, 0.04, 0.16, 1)
C_GREEN  = (0.0,  0.75, 0.0,  1)
C_YELLOW = (0.95, 0.9,  0.0,  1)
C_RED    = (0.9,  0.0,  0.0,  1)
C_WHITE  = (1.0,  1.0,  1.0,  1)
C_BLACK  = (0.0,  0.0,  0.0,  1)
C_RING   = (0.1,  0.28, 0.1,  1)
C_RING_F = (0.2,  0.6,  0.2,  1)

# ── 全局状态 ──
total_s  = 120
remain_s = 120
running  = False
is_ot   = False
ot_s     = 0
flash    = 0
last_t   = 0
snd_on  = True

PRESETS = [
    ("2分",  120), ("7分",  420), ("10分", 600), ("15分", 900),
    ("30分", 1800), ("1小时", 3600), ("1.5h", 5400), ("2h", 7200),
]

def fmt(s):
    s = abs(int(s))
    h, m, sec = s // 3600, (s % 3600) // 60, s % 60
    return f"{h:02d}:{m:02d}:{sec:02d}" if h else f"{m:02d}:{sec:02d}"

def thresholds(mins):
    if mins < 3:   return 60, 30
    if mins <= 10: return 120, 60
    return 300, 120

def get_phase():
    if is_ot or remain_s <= 0:
        return 'ot'
    g, y = thresholds(total_s / 60)
    if remain_s > g: return 'black'
    if remain_s > y: return 'green'
    return 'yellow'

def phase_colors(ph):
    if ph == 'ot':     return C_RED,   C_RING_F, C_WHITE
    if ph == 'yellow': return C_YELLOW, C_RING_F, C_BLACK
    if ph == 'green':  return C_GREEN,  C_RING_F, C_BLACK
    return C_BG, C_RING_F, C_WHITE


class WheelWidget(Widget):
    """圆形倒计时轮盘 — 自动适应父容器大小"""
    def __init__(self, **kw):
        super().__init__(**kw)
        self.bind(pos=self.redraw, size=self.redraw)

    def redraw(self, *a):
        self.canvas.clear()
        with self.canvas:
            cw = self.width
            ch = self.height
            if cw < 10 or ch < 10:
                return

            # 竖屏布局：圆心在区域中央偏上，给"已超时"文字留空间
            cx = cw / 2.0
            cy = ch * 0.48          # 偏上，让圆形在区域内居中
            scale = min(cw, ch) / 1080.0
            rad = min(cw, ch) * 0.36
            rw  = max(6, 22 * scale)

            ph = get_phase()
            bg, ring_fg, tc = phase_colors(ph)

            # 背景
            Color(*bg)
            Rectangle(pos=(0, 0), size=(cw, ch))

            # 进度比例
            walked = 0.0
            if not is_ot and total_s > 0:
                walked = max(0.0, min(1.0, 1.0 - remain_s / total_s))

            # 底环
            Color(*C_RING)
            Line(circle=(cx, cy, rad), width=rw, cap='round')

            # 进度弧
            if not is_ot:
                if walked < 1.0:
                    sa = 90 - walked * 360
                    ea = sa - (1.0 - walked) * 360
                    Color(*ring_fg)
                    Line(circle=(cx, cy, rad),
                         angle_start=sa, angle_end=ea,
                         width=rw, cap='round')
                # 已走过部分用背景色覆盖（消失效果）
                Color(*bg)
                Line(circle=(cx, cy, rad),
                     angle_start=90,
                     angle_end=90 - walked * 360,
                     width=rw, cap='round')

            # 刻度 60 格
            filled = int(walked * 60)
            light = ph in ('green', 'yellow')
            c_maj = (0.35, 0.35, 0.4, 1)  if light else (0.67, 0.67, 0.8, 1)
            c_min = (0.50, 0.50, 0.55, 1) if light else (0.50, 0.50, 0.6, 1)
            for i in range(60):
                a  = i / 60.0 * 2 * math.pi - math.pi / 2
                maj = (i % 5 == 0)
                r1 = rad - (16 if maj else 10) * scale
                r2 = rad - (7  if maj else 5)  * scale
                lw = max(1, int(2 * scale if maj else 1 * scale))
                Color(*(bg if i < filled else (c_maj if maj else c_min)))
                Line(points=[cx + r1*math.cos(a), cy + r1*math.sin(a),
                             cx + r2*math.cos(a), cy + r2*math.sin(a)],
                     width=lw, cap='round')

            # 指针
            if not is_ot:
                ang = -math.pi / 2 + walked * 2 * math.pi
                px, py = (cx + (rad - 10*scale)*math.cos(ang),
                            cy + (rad - 10*scale)*math.sin(ang))
                bx1 = cx + 45*scale * math.cos(ang + 0.11)
                by1 = cy + 45*scale * math.sin(ang + 0.11)
                bx2 = cx + 45*scale * math.cos(ang - 0.11)
                by2 = cy + 45*scale * math.sin(ang - 0.11)
                Color(0.9, 0.9, 1.0, 1)
                Line(points=[px, py, bx1, by1, bx2, by2, px, py], width=2)
                Color(0.9, 0.9, 1.0, 1)
                Ellipse(pos=(cx - 6*scale, cy - 6*scale), size=(12*scale, 12*scale))
                Color(*bg)
                Ellipse(pos=(cx - 3*scale, cy - 3*scale), size=(6*scale, 6*scale))

            # 时间文字
            if is_ot:
                disp = "-" + fmt(ot_s)
                tc2 = C_YELLOW if (running and flash % 2 == 0) else tc
            else:
                disp = fmt(remain_s)
                if remain_s <= 10 and remain_s > 0 and running:
                    tc2 = C_RED if (flash % 2 == 0) else C_BLACK
                else:
                    tc2 = tc

            fs = max(32, int(100 * scale))
            lbl = CoreLabel(text=disp, font_size=fs, bold=True, color=tc2)
            lbl.refresh()
            t = lbl.texture
            if t:
                Color(1, 1, 1, 1)
                Rectangle(texture=t, pos=(cx - t.width/2, cy - t.height/2), size=t.size)

            # "已超时" 文字（圆形下方）
            if is_ot:
                fs2 = max(22, int(52 * scale))
                l2 = CoreLabel(text="已  超  时", font_size=fs2, bold=True, color=C_YELLOW)
                l2.refresh()
                t2 = l2.texture
                if t2:
                    Color(1, 1, 1, 1)
                    Rectangle(texture=t2, pos=(cx - t2.width/2, cy + rad + 20*scale), size=t2.size)

            # 标题（圆形上方）
            fs3 = max(14, int(30 * scale))
            l3 = CoreLabel(text="⏱ 倒计时", font_size=fs3, color=tc)
            l3.refresh()
            t3 = l3.texture
            if t3:
                Color(1, 1, 1, 1)
                Rectangle(texture=t3, pos=(cx - t3.width/2, cy - rad - 40*scale - t3.height), size=t3.size)


class CountdownApp(App):

    def build(self):
        global last_t
        last_t = time.time()

        root = FloatLayout()

        # ── 轮盘区域（上方 58%）──
        self.wheel = WheelWidget()
        self.wheel.size_hint = (1, 0.58)
        self.wheel.pos_hint   = {'x': 0, 'y': 0.42}
        root.add_widget(self.wheel)

        # ── 底部控制面板（下方 42%）──
        panel = BoxLayout(orientation='vertical',
                          size_hint=(1, 0.42),
                          pos_hint={'x': 0, 'y': 0},
                          spacing=2,
                          padding=[8, 4, 8, 8])
        root.add_widget(panel)

        # 第一行：预设按钮（4列 × 2行）
        r1 = GridLayout(cols=4, spacing=4, size_hint=(1, 0.35))
        panel.add_widget(r1)
        for lbl, secs in PRESETS:
            b = Button(text=lbl, font_size=13,
                        background_normal='',
                        background_color=(0.12, 0.12, 0.22, 1),
                        color=(0.88, 0.88, 0.92, 1))
            b.bind(on_press=lambda inst, s=secs: self.on_preset(s))
            r1.add_widget(b)

        # 第二行：开始/暂停 + 声音开关
        r2 = BoxLayout(spacing=8, size_hint=(1, 0.30),
                         padding=[0, 2, 0, 2])
        panel.add_widget(r2)
        self.btn_go = Button(text='▶ 开始/暂停',
                              font_size=15, bold=True,
                              background_normal='',
                              background_color=(0.75, 0.35, 0.0, 1),
                              color=C_WHITE)
        self.btn_go.bind(on_press=self.on_toggle)
        r2.add_widget(self.btn_go)

        self.btn_snd = Button(text='🔔 开',
                               font_size=12,
                               background_normal='',
                               background_color=(0.1, 0.32, 0.1, 1),
                               color=(0.8, 1.0, 0.8, 1),
                               size_hint=(0.35, 1))
        self.btn_snd.bind(on_press=self.on_toggle_snd)
        r2.add_widget(self.btn_snd)

        # 第三行：时/分/秒输入 + 确认 + 重置
        r3 = BoxLayout(spacing=4, size_hint=(1, 0.35),
                         padding=[0, 2, 0, 0])
        panel.add_widget(r3)

        def make_input(label, default):
            """创建一个带标签的输入控件"""
            box = BoxLayout(orientation='vertical',
                           size_hint=(0.18, 1), spacing=1)
            r3.add_widget(box)
            l = Label(text=label,
                       font_size=11,
                       color=(0.85, 0.85, 0.9, 1),
                       size_hint=(1, 0.30))
            box.add_widget(l)
            ti = TextInput(text=str(default),
                           input_filter='int',
                           font_size=16, halign='center',
                           multiline=False,
                           size_hint=(1, 0.70),
                           background_color=(0.10, 0.10, 0.20, 1),
                           foreground_color=C_WHITE,
                           cursor_color=C_WHITE)
            box.add_widget(ti)
            return ti

        self.e_h = make_input('时', 0)
        self.e_m = make_input('分', 2)
        self.e_s = make_input('秒', 0)

        btn_ok = Button(text='确认',
                        font_size=12,
                        background_normal='',
                        background_color=(0.12, 0.40, 0.70, 1),
                        color=C_WHITE,
                        size_hint=(0.18, 1))
        btn_ok.bind(on_press=lambda *a: self.on_confirm())
        r3.add_widget(btn_ok)

        btn_rst = Button(text='重置',
                         font_size=12,
                         background_normal='',
                         background_color=(0.55, 0.15, 0.0, 1),
                         color=C_WHITE,
                         size_hint=(0.18, 1))
        btn_rst.bind(on_press=lambda *a: self.on_reset())
        r3.add_widget(btn_rst)

        # 计时器
        Clock.schedule_interval(self.on_tick, 0.5)

        # 提示音
        self.snd = None
        try:
            self.snd = SoundLoader.load('beep.wav')
        except Exception:
            pass

        return root

    # ── 输入工具 ──
    def read_entries(self):
        try:
            h = max(0, int(self.e_h.text or 0))
            m = max(0, int(self.e_m.text or 0))
            s = max(0, int(self.e_s.text or 0))
            return max(1, h*3600 + m*60 + s)
        except Exception:
            return None

    def write_entries(self, t):
        self.e_h.text = str(t // 3600)
        self.e_m.text = str((t % 3600) // 60)
        self.e_s.text = str(t % 60)

    # ── 按钮回调 ──
    def on_preset(self, secs):
        global total_s, remain_s, running, is_ot, ot_s, flash
        if running or is_ot:
            return
        total_s = remain_s = secs
        flash   = 0
        self.write_entries(secs)
        self.wheel.redraw()

    def on_confirm(self):
        global total_s, remain_s, flash
        if running or is_ot:
            return
        t = self.read_entries()
        if t and t >= 1:
            total_s  = t
            remain_s = t
            flash    = 0
            self.wheel.redraw()

    def on_toggle(self, *a):
        global running, is_ot
        if is_ot and not running:
            running = True
        else:
            running = not running
        self.btn_go.text = '⏸ 暂停' if running else '▶ 开始/暂停'

    def on_reset(self):
        global running, is_ot, ot_s, remain_s, total_s, flash
        running  = False
        is_ot   = False
        ot_s     = 0
        flash    = 0
        remain_s = total_s
        self.btn_go.text = '▶ 开始/暂停'
        self.write_entries(total_s)
        self.wheel.redraw()

    def on_toggle_snd(self):
        global snd_on
        snd_on = not snd_on
        self.btn_snd.text = '🔔 开' if snd_on else '🔇 关'
        c = (0.1, 0.32, 0.1, 1) if snd_on else (0.32, 0.1, 0.1, 1)
        self.btn_snd.background_color = c

    def play_beep(self):
        if not snd_on:
            return
        try:
            if self.snd:
                self.snd.play()
        except Exception:
            pass

    # ── 计时循环 ──
    def on_tick(self, dt):
        global remain_s, is_ot, ot_s, flash, running, last_t

        now = time.time()
        if running and now - last_t >= 1.0:
            last_t = now
            if not is_ot:
                if remain_s <= 0:
                    is_ot  = True
                    ot_s   = 0
                    flash  = 0
                    self.play_beep()
                else:
                    remain_s -= 1
                    flash = (flash + 1) if remain_s <= 10 else 0
            else:
                ot_s  += 1
                flash += 1
                if ot_s < 30 and ot_s % 2 == 0:
                    self.play_beep()

        self.wheel.redraw()
        return True


if __name__ == '__main__':
    CountdownApp().run()
