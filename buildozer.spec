[app]
# 应用名称（显示在主屏幕上）
title = 倒计时轮盘
# 包名（必须唯一，反向域名格式）
package.name = com.gofy.countdownwheel
package.domain = com.gofy

# 源代码文件（所有需要打包进APK的Python文件）
source.dir = .
source.include_exts = py,png,jpg,kv,wav,ttf

# 应用主入口
source.include_patterns = assets/*,images/*
version = 1.0
version.code = 1

# 应用要求
requirements = python3,kivy,cython<3.0

# p4a 使用 develop 分支（修复 HIDDeviceManager 与 Cython 3.x 兼容问题）
p4a.branch = develop

# 图标（需要自行添加）

# 是否全面屏支持
fullscreen = 0

# 权限
android.permissions = VIBRATE,WAKE_LOCK
# android.features = 

# Android API 版本
android.api = 30
android.minapi = 21
android.targetapi = 30

# 屏幕方向（portrait=竖屏，删除本行则横竖自适应）
orientation = portrait

# 状态栏
android.statusbar = HIDDEN

# 保持屏幕常亮（计时器应用需要）
wake_lock = True

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]
# 构建输出目录
builddir = ./build
# 不自动清理构建缓存
buildozer.bin = buildozer

# 跳过 Android SDK/NDK 自动下载（如果本机已有）
# 自动接受Android SDK许可
android.accept_sdk_license = True
# android.sdk_path = 
# android.ndk_path = 

# 日志等级
log_level = 2
