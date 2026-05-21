# 倒计时轮盘 - 安卓版 说明文档

> 作者：Gofy高飞团队  
> 版本：1.0  
> 最后更新：2026-05-20

---

## 功能说明

| 功能 | 说明 |
|------|------|
| 圆形倒计时轮盘 | 可视化进度，颜色随剩余时间变化（蓝→绿→黄→红） |
| 8个预设时间 | 2分/7分/10分/15分/30分/1小时/1.5小时/2小时 |
| 自定义时间 | 支持时/分/秒输入，上下箭头微调 |
| 到时提示 | 超时后持续计时 + 蜂鸣提示（可关闭） |
| 横屏锁定 | 适合演讲/会议场景使用 |

---

## 文件结构

```
安卓版本/
├── main.py           # 主程序（Kivy App）
├── buildozer.spec    # APK 打包配置
├── generate_beep.py # 生成提示音 beep.wav
├── README_安卓版.md # 本文档
└── assets/           # 资源目录（图标/启动图）
```

---

## 本地运行测试（Windows）

### 1. 安装 Kivy

```bash
pip install kivy[base] kivy_examples
```

### 2. 运行

```bash
cd "E:\Programs\WorkBuddy\倒计时轮盘\安卓版本"
python main.py
```

---

## 打包成 APK（需要 Linux / WSL）

### 方式一：WSL（Windows 推荐）

1. 安装 WSL（管理员 PowerShell）：
   ```powershell
   wsl --install
   ```
2. 进入 Ubuntu，安装依赖：
   ```bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk
   pip3 install --upgrade pip
   pip3 install buildozer
   ```
3. 将项目复制到 WSL 目录，执行：
   ```bash
   buildozer -v android debug
   ```
4. 生成的 APK 位于：
   ```
   bin/倒计时轮盘-1.0-debug.apk
   ```

### 方式二：用 Buildozer 云端构建（无需本地Linux）

访问 [https://buildozer.app/](https://buildozer.app/) 上传代码，在线构建 APK。

---

## 提示音文件

程序启动时会尝试加载 `beep.wav` 作为到时提示音。

如需自定义提示音，将自己的 `beep.wav` 放在 `main.py` 同目录下即可。

或运行 `generate_beep.py` 生成默认蜂鸣声：

```bash
python generate_beep.py
```

---

## 已移除的桌面版功能

以下功能在安卓版中无意义，已移除：

- OBS 虚拟摄像头（移动端无需此功能）
- 键盘快捷键（S/F/数字键，触屏无键盘）
- Windows 专属 API（`winsound` 等）

---

## 故障排查

| 问题 | 解决方法 |
|------|----------|
| 轮盘不显示 | 确认 Kivy 正确安装，运行 `python -c "import kivy; print(kivy.__version__)"` |
| 提示音不响 | 检查 `beep.wav` 是否存在；安卓端需授予通知/声音权限 |
| 打包失败 | 检查 `buildozer.spec` 中 SDK/NDK 路径是否正确 |
| 屏幕方向不对 | 修改 `buildozer.spec` 中 `orientation = portrait` 改为竖屏 |

---

## 接下来可以做

- [ ] 添加应用图标（替换 `icon.png`）
- [ ] 添加启动画面（替换 `presplash.png`）
- [ ] 支持震动反馈（超时后手机震动）
- [ ] 支持后台计时（通知栏常驻）
- [ ] 支持保存常用预设到本地存储
