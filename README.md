# 🎮 Cozy Tank - 坦克大战

**[下载 Windows x64 运行包](https://github.com/kurodayu23/-cozy-tank/releases/latest)**：下载 `CozyTank-v1.0.0-Windows-x64.zip`，完整解压后双击 `CozyTank.exe`，无需安装 Python。需要 Windows 10/11 和 WebView2 Runtime。

基于 **Python + pywebview + React** 的混合架构坦克大战游戏。

## Vibe Coding / AI 辅助开发

本项目采用 AI 辅助开发，通过需求描述与迭代反馈，使用 AI 辅助编写和修改代码。Vibe Coding 在这里描述开发方式；项目的具体功能与完成度以源码、运行说明和验证记录为准。

当前游戏不包含大模型控制功能。展示重点是桌面启动器、Python/JavaScript 交互、游戏运行与回归测试；前端完整源码的现状见下方验证边界。

维护时以明确需求、审查代码改动和可复现验证为准；具体测试及尚未验证的部分见下方说明。

## 🚀 一键启动

**双击** `启动游戏.bat` 即可运行。

或手动启动：
```bash
python -m pip install -r requirements.txt
python tank_game.py
```

## 🎯 游戏操作

| 按键 | 功能 |
|------|------|
| `↑ ↓ ← →` | 移动坦克 |
| `空格` / `Enter` | 发射子弹 |
| `ESC` | 暂停 / 菜单 |

## 🔊 音效系统

使用 Web Audio API 实时合成，无需外部音频文件：
- 射击音效 (正弦波下滑)
- 命中音效 (三角波)
- 爆炸音效 (滤波噪声)
- UI 悬停音效 (马林巴)
- 游戏结束 / 胜利旋律

## 📁 项目结构

```
├── tank_game.py           # Python 启动器 (pywebview)
├── 启动游戏.bat           # 一键启动脚本
├── requirements.txt       # Python 依赖
├── frontend/
│   ├── index.html         # 主页面 + 主题 CSS
│   ├── game-inject.js     # 音效 + 暂停弹窗 + HUD
│   └── assets/
│       ├── index-*.js     # React 游戏引擎 (打包)
│       └── index-*.css    # Tailwind 样式 (打包)
└── README.md
```

## 🛠 技术栈

- **后端**: Python 3 + pywebview (WebView2/Edge Chromium)
- **前端**: React 19 + Canvas 2D + Web Audio API
- **主题**: 粉色可爱风 (ZCOOL KuaiLe + LXGW WenKai 字体)

## 📋 环境要求

- Windows 10+ (需要 Edge WebView2 运行时)
- Python 3.8+
- pywebview >= 4.0

## 开发与验证边界

当前仓库包含 Python 启动器、手写交互脚本和已经打包的前端资源，尚未包含可重新构建 React 游戏的完整源码与构建配置。因此目前适合运行和维护启动器、交互脚本，不应视为完整的 React 工程模板。

```bash
python -m pip install -r requirements.txt pytest
python -m pytest -q
node --check frontend/game-inject.js
```

测试覆盖高分保存、损坏数据读取、窗口接口和本地资源完整性。CI 不启动桌面窗口，不能替代 WebView2 窗口、键盘操作和游戏流程的实际验收。界面字体引用外部资源，离线时可能使用系统回退字体。

## 构建 Windows 下载包

使用 Python 3.11 x64，建议在独立虚拟环境中运行：

```powershell
python -m pip install -r scripts/build-requirements.txt
.\scripts\package_windows.ps1
```

输出在 `dist/`。脚本会包含运行时和所需资源，生成包含 EXE 与 `_internal` 的 ZIP；发布前需验证解压后的程序。
