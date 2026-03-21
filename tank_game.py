
import sys, os, json
import webview

DIR        = os.path.dirname(os.path.abspath(__file__))
GAME_HTML  = os.path.join(DIR, 'frontend', 'index.html')
SCORE_FILE = os.path.join(DIR, 'highscore.json')

win_instance = None
class Api:
    def toggle_fullscreen(self):
        if win_instance:
            win_instance.toggle_fullscreen()

    """暴露给 JavaScript 的 Python 接口"""

    def get_high_score(self):
        try:
            with open(SCORE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f).get('high', 0)
        except Exception:
            return 0

    def save_high_score(self, score):
        try:
            with open(SCORE_FILE, 'w', encoding='utf-8') as f:
                json.dump({'high': int(score)}, f)
        except Exception:
            pass

    def quit(self):
        """从 JS 端关闭窗口"""
        import threading
        threading.Thread(target=win.destroy, daemon=True).start()

if __name__ == '__main__':
    if not os.path.exists(GAME_HTML):
        print(f"[错误] 找不到 game.html，请确保它在同目录下:\n  {GAME_HTML}")
        sys.exit(1)

    url = 'file:///' + GAME_HTML.replace('\\', '/')
    win_instance = win = webview.create_window(
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
