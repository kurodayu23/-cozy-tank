# 🎮 Cozy Tank - 坦克大战

基于 **Python + pywebview + React** 的混合架构坦克大战游戏。

## 🚀 一键启动

**双击** `启动游戏.bat` 即可运行。

或手动启动：
```bash
pip install pywebview>=4.0
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
