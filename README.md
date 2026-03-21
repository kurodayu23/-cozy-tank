<div align="center">

# 🎮 Cozy Tank

一个用 Python + React 混合架构实现的手账风坦克大战

[![CI](https://github.com/kurodayu23/-cozy-tank/actions/workflows/ci.yml/badge.svg)](https://github.com/kurodayu23/-cozy-tank/actions)
![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=white)
![WebView2](https://img.shields.io/badge/WebView2-Edge%20Chromium-0078D4?logo=microsoftedge&logoColor=white)

</div>

---

## 关于这个项目

经典坦克大战的现代复刻，但不是传统的黑底像素风——
我把整个画面改成了粉色手账本的风格，坦克变成了圆圆的小动物脸，子弹是飞出去的小红心 ❤️

底层架构比较特别：Python 负责窗口管理和数据持久化，
游戏引擎和 UI 全部跑在内嵌的 Edge WebView2 里面，前端用 React 19 写的。
音效没有用任何音频文件，全部是 Web Audio API 实时合成的波形。

## 主要特性

- 🐾 可爱的动物风坦克 + 弹跳待机动画
- 🌸 过关时的毛玻璃弹窗 + 满屏礼花粒子特效
- 🎵 Web Audio API 实时合成音效（三角波/方波），零资源依赖
- 🧱 多种地形：砖墙、钢墙、水面（动态）、草丛（伪装）
- 💥 爆炸粒子系统 + 屏幕震动 + 坦克履带痕迹
- ⭐ 道具系统：加速射击、冻结、护盾、空袭、加固
- 💾 本地最高分存储（Python JSON 桥接）
- 🎯 两关制战役，难度递进

## 跑起来

```bash
git clone https://github.com/kurodayu23/-cozy-tank.git
cd cozy-tank

pip install -r requirements.txt   # 只需要 pywebview

python tank_game.py
```

> 需要 Python 3.10+ 和 Windows（WebView2 运行时，Win10/11 自带）

## 操作方式

| 按键 | 功能 |
|------|------|
| `W A S D` / `方向键` | 移动 |
| `空格` / `回车` | 开火 |
| `P` | 暂停 |
| `ESC` | 全屏切换 |

## 技术架构

```
Python 后端（pywebview）
    ↕ JS ↔ Python RPC 桥接
React 19 前端（Canvas 2D 引擎 + Web Audio + Tailwind）
```

- **窗口宿主**: pywebview + Edge WebView2
- **游戏引擎**: Canvas 2D，AABB 碰撞检测
- **UI 框架**: React 19 + Tailwind CSS
- **音频**: Web Audio API 振荡器合成
- **字体加载**: `rel="preload"` 异步方案，0ms 首屏

## 项目结构

```
cozy-tank/
├── .github/workflows/ci.yml   # CI 验证
├── frontend/                   # 前端编译产物
│   ├── index.html
│   └── assets/
├── tank_game.py                # 入口
├── requirements.txt
└── .gitignore
```

## License

MIT
