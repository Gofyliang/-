[app]
# 搴旂敤鍚嶇О锛堟樉绀哄湪涓诲睆骞曚笂锛?title = 鍊掕鏃惰疆鐩?# 鍖呭悕锛堝繀椤诲敮涓€锛屽弽鍚戝煙鍚嶆牸寮忥級
package.name = com.gofy.countdownwheel
package.domain = com.gofy

# 婧愪唬鐮佹枃浠讹紙鎵€鏈夐渶瑕佹墦鍖呰繘APK鐨凱ython鏂囦欢锛?source.dir = .
source.include_exts = py,png,jpg,kv,wav,ttf

# 搴旂敤涓诲叆鍙?source.include_patterns = assets/*,images/*
version = 1.0
version.code = 1

# 搴旂敤瑕佹眰
requirements = python3,kivy,cython<3.0

# p4a 浣跨敤 develop 鍒嗘敮锛堜慨澶?HIDDeviceManager 涓?Cython 3.x 鍏煎闂锛?p4a.branch = develop

# 鍥炬爣锛堥渶瑕佽嚜琛屾坊鍔狅級

# 鏄惁鍏ㄩ潰灞忔敮鎸?fullscreen = 0

# 鏉冮檺
android.permissions = VIBRATE,WAKE_LOCK
# android.features = 

# Android API 鐗堟湰锛圔LUETOOTH_CONNECT 闇€瑕?API 31+锛?android.api = 31
android.minapi = 21
android.targetapi = 31

# 灞忓箷鏂瑰悜锛坧ortrait=绔栧睆锛屽垹闄ゆ湰琛屽垯妯珫鑷€傚簲锛?orientation = portrait

# 鐘舵€佹爮
android.statusbar = HIDDEN

# 淇濇寔灞忓箷甯镐寒锛堣鏃跺櫒搴旂敤闇€瑕侊級
wake_lock = True

presplash.filename = %(source.dir)s/presplash.png
icon.filename = %(source.dir)s/icon.png

[buildozer]
# 鏋勫缓杈撳嚭鐩綍
builddir = ./build
# 涓嶈嚜鍔ㄦ竻鐞嗘瀯寤虹紦瀛?buildozer.bin = buildozer

# 璺宠繃 Android SDK/NDK 鑷姩涓嬭浇锛堝鏋滄湰鏈哄凡鏈夛級
# 鑷姩鎺ュ彈Android SDK璁稿彲
android.accept_sdk_license = True
# android.sdk_path = 
# android.ndk_path = 

# 鏃ュ織绛夌骇
log_level = 2
