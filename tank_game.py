
import sys
import os
import json
from pathlib import Path
import webview

DIR        = os.path.dirname(os.path.abspath(__file__))
GAME_HTML  = os.path.join(DIR, 'frontend', 'index.html')
SCORE_FILE = os.path.join(DIR, 'highscore.json')

win_instance = None
class Api:
    """暴露给 JavaScript 的 Python 接口。"""

    def toggle_fullscreen(self):
        if win_instance:
            win_instance.toggle_fullscreen()

    def get_high_score(self):
        try:
            with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                score = json.load(f).get('high', 0)
                return max(0, int(score))
        except (OSError, ValueError, TypeError, AttributeError):
            return 0

    def save_high_score(self, score):
        score = max(self.get_high_score(), max(0, int(score)))
        with open(SCORE_FILE, 'w', encoding='utf-8') as f:
            json.dump({'high': score}, f)

    def quit(self):
        """从 JS 端关闭窗口"""
        if win_instance:
            win_instance.destroy()

if __name__ == '__main__':
    if not os.path.exists(GAME_HTML):
        print(f"[错误] 找不到 frontend/index.html，请保持仓库目录完整:\n  {GAME_HTML}")
        sys.exit(1)

    url = Path(GAME_HTML).as_uri()
    win_instance = webview.create_window(
        title='Cozy Tank - Hybrid Python/React Retro Game',
        url=url,
        js_api=Api(),
        width=700,
        height=740,
        fullscreen=True,
        resizable=True,
        min_size=(500, 530),
        background_color='#f7ece1',
    )

    webview.start()
