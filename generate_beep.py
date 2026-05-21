#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成倒计时到时提示音 beep.wav
纯 Python 实现，无需外部依赖
"""
import wave, struct, math

DURATION = 0.20        # 每次蜂鸣时长（秒）
FREQ     = 880         # 频率 Hz
SAMPLERATE = 44100

def generate_beep(path):
    with wave.open(path, 'w') as w:
        w.setnchannels(1)          # 单声道
        w.setsampwidth(2)         # 16-bit
        w.setframerate(SAMPLERATE)

        frames = []
        for i in range(int(SAMPLERATE * DURATION)):
            t = i / SAMPLERATE
            # 正弦波 + 淡入淡出
            env = math.sin(math.pi * i / (SAMPLERATE * DURATION))
            val = int(32767 * 0.5 * math.sin(2 * math.pi * FREQ * t) * env)
            frames.append(struct.pack('<h', val))
        w.writeframes(b''.join(frames))
    print(f"✅ 已生成：{path}")

if __name__ == '__main__':
    generate_beep('beep.wav')
