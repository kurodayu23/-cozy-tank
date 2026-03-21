
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
        title='Cozy Tank — A Hybrid Python/React Retro Game',
        url=url,
        js_api=Api(),
        width=700,
        height=740,
        fullscreen=True,
        resizable=True,
        min_size=(500, 530),
        background_color='#f7ece1',
    )

    def on_loaded():
        js_code = """

        const style = document.createElement('style');
        style.innerHTML = `
                display: none;
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                background: rgba(253, 246, 245, 0.4);
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
                z-index: 999999;
                flex-direction: column; align-items: center; justify-content: center;
                font-family: 'ZCOOL KuaiLe', '幼圆', sans-serif;
            }
            .esc-box {
                background: rgba(255, 255, 255, 0.85);
                border: 1px solid rgba(255, 182, 193, 0.4);
                border-radius: 20px;
                padding: 40px 60px;
                text-align: center;
                box-shadow: 0 15px 35px rgba(255, 182, 193, 0.15);
                display: flex; flex-direction: column; gap: 20px;
            }
            .esc-title {
                font-size: 32px; font-weight: normal; letter-spacing: 4px;
                margin-bottom: 20px; color: #ff8da1;
            }
            .esc-btn {
                background: #fff;
                border: 1px solid #ffb6c1;
                border-radius: 12px;
                color: #ff69b4;
                font-size: 18px; letter-spacing: 2px;
                padding: 12px 30px;
                cursor: pointer;
                transition: all 0.2s ease;
                box-shadow: 0 4px 10px rgba(255, 182, 193, 0.1);
            }
            .esc-btn:hover {
                background: #fff0f5;
                transform: translateY(-2px);
                box-shadow: 0 6px 15px rgba(255, 182, 193, 0.25);
            }
            .esc-btn.danger { color: #ff8da1; border-color: #ffd1dc; }
            .esc-btn.danger:hover { background: #ffe4e1; }
        `;
        document.head.appendChild(style);

        const AudioContext = window.AudioContext || window.webkitAudioContext;
        const audioCtx = new AudioContext();

        function wakeUpAudio() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            window.removeEventListener('click', wakeUpAudio);
            window.removeEventListener('keydown', wakeUpAudio, {capture: true});
        }
        window.addEventListener('click', wakeUpAudio);
        window.addEventListener('keydown', wakeUpAudio, {capture: true});

        function playShoot() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(800, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(300, audioCtx.currentTime + 0.1);
            gain.gain.setValueAtTime(0.15, audioCtx.currentTime); 
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.1);
        }

        function playMarimba() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain();
            osc.type = 'sine';
            osc.frequency.setValueAtTime(1046.50, audioCtx.currentTime); // C6
            gain.gain.setValueAtTime(0.08, audioCtx.currentTime); 
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.15);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.15);
        }

        function playHit() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain();
            osc.type = 'triangle';
            osc.frequency.setValueAtTime(1200, audioCtx.currentTime);
            osc.frequency.exponentialRampToValueAtTime(600, audioCtx.currentTime + 0.05);
            gain.gain.setValueAtTime(0.1, audioCtx.currentTime); 
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.05);
            osc.connect(gain); gain.connect(audioCtx.destination);
            osc.start(); osc.stop(audioCtx.currentTime + 0.05);
        }

        function playExplode() {
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const bufferSize = audioCtx.sampleRate * 0.2; // 0.2s
            const buffer = audioCtx.createBuffer(1, bufferSize, audioCtx.sampleRate);
            const data = buffer.getChannelData(0);
            for (let i = 0; i < bufferSize; i++) { data[i] = Math.random() * 2 - 1; }
            const noise = audioCtx.createBufferSource(); noise.buffer = buffer;
            const filter = audioCtx.createBiquadFilter(); filter.type = 'lowpass';
            filter.frequency.setValueAtTime(1000, audioCtx.currentTime);
            filter.frequency.exponentialRampToValueAtTime(100, audioCtx.currentTime + 0.2);
            const gain = audioCtx.createGain();
            gain.gain.setValueAtTime(0.3, audioCtx.currentTime);
            gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.2);
            noise.connect(filter); filter.connect(gain); gain.connect(audioCtx.destination);
            noise.start();
        }

        window.addEventListener('yyc_shoot', playShoot);
        window.addEventListener('yyc_hit', playHit);
        window.addEventListener('yyc_boom', playExplode);

        const overlay = document.createElement('div');
        overlay.id = 'esc-overlay';
        overlay.innerHTML = `
            <div class="esc-box">
                <div class="esc-title">✨ 中场休息 ✨</div>
                <button class="esc-btn" id="btn-continue">▶ 继续玩耍</button>
                <button class="esc-btn" id="btn-restart">↺ 返回主页</button>
                <button class="esc-btn danger" id="btn-exit">✖ 溜了溜了</button>
            </div>
        `;
        document.body.appendChild(overlay);

        const btns = document.querySelectorAll('.esc-btn');
        btns.forEach(b => {
            b.addEventListener('mouseenter', playMarimba);
        });

        document.getElementById('btn-continue').onclick = () => { overlay.style.display = 'none'; playMarimba(); };
        document.getElementById('btn-restart').onclick = () => { playMarimba(); setTimeout(()=>window.location.reload(), 150); };
        document.getElementById('btn-exit').onclick = () => { playMarimba(); setTimeout(()=>{if(window.pywebview) window.pywebview.api.quit();}, 150) };

        window.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                e.preventDefault(); e.stopPropagation();
                if (overlay.style.display === 'flex') overlay.style.display = 'none';
                else overlay.style.display = 'flex';
                playMarimba();
            }
            if (e.target !== document.body && e.target !== window) return;
            if ((e.code === 'Space' || e.code === 'Enter') && !e.repeat) {
                playShoot();
            }
        }, {capture: true});

        style.innerHTML += `
            .custom-overlay {
                display: none;
                position: fixed; top: 0; left: 0; width: 100vw; height: 100vh;
                backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px);
                z-index: 9999999;
                flex-direction: column; align-items: center; justify-content: center;
                transition: all 0.5s ease;
                font-family: 'ZCOOL KuaiLe', '幼圆', sans-serif;
            }
            
            /* Game over grayscale failure effect */
            .game-failed canvas { filter: grayscale(80%) sepia(20%) hue-rotate(-50deg) saturate(150%) brightness(70%); transition: filter 2s; }
            /* Game win vibrant success effect */
            .game-won canvas { filter: contrast(120%) brightness(110%) hue-rotate(-10deg); transition: filter 2s; }

            /* Start Screen custom mapped styles */
            .yyc-bg-pink { background-color: #f7ece1 !important; }
            .yyc-bg-cream { background-color: #fffdf0 !important; }
            .yyc-bg-hover { background-color: #fff0f5 !important; }
            .yyc-bg-rose { background-color: #ffb6c1 !important; }
            .yyc-bg-brown { background-color: #5c4033 !important; }
            
            .yyc-text-brown { color: #5c4033 !important; }
            .yyc-text-rose { color: #b56576 !important; }
            
            /* Aggressive Typography Override */
            .z-50.yyc-bg-pink, .z-50.yyc-bg-pink * {
                font-family: 'LXGW WenKai Lite', '幼圆', 'Microsoft YaHei', sans-serif !important;
                letter-spacing: 0.05em;
            }
            .yyc-font { font-family: 'LXGW WenKai Lite', '幼圆', sans-serif !important; }
            .yyc-shadow-hover:hover { box-shadow: 0 4px 20px 0 rgba(181,101,118,0.4) !important; }
            .yyc-rounded { border-radius: 12px !important; }
            
            /* Sticker Stroke and Shadow Effect */
            .yyc-title-stroke {
                color: #5c4033 !important;
                text-shadow: 2px 2px 0px #fff, -2px -2px 0px #fff, 2px -2px 0px #fff, -2px 2px 0px #fff, 4px 4px 5px rgba(0,0,0,0.1) !important;
            }
            
            /* Float Breathing Animation */
            @keyframes yycFloat {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-8px); }
            }
            .yyc-float-anim {
                animation: yycFloat 3.5s ease-in-out infinite;
                transform-style: preserve-3d;
            }
            
            .yyc-text-dark { color: #666666 !important; }
            
            /* Mega Typography Layout Substitutions */
            .yyc-pad-left { padding-left: 15vw !important; }
            @media (max-width: 768px) { .yyc-pad-left { padding-left: 5vw !important; } }
            
            .yyc-margin-left { margin-left: 30% !important; }
            .yyc-tracking-mega { letter-spacing: 0.2em !important; }
            .yyc-mega-bg { background-color: rgba(255, 182, 193, 0.4) !important; }
            
            .yyc-mega-title { font-size: 160px !important; line-height: 1 !important; margin-top: 1rem !important; margin-bottom: 2rem !important; }
            @media (max-width: 768px) { .yyc-mega-title { font-size: 90px !important; } }
            
            .yyc-sub-title { font-size: 100px !important; line-height: 1 !important; margin-top: -3rem !important; }
            @media (max-width: 768px) { .yyc-sub-title { font-size: 60px !important; } }
        `;

        const goOverlay = document.createElement('div');
        goOverlay.id = 'gameover-overlay';
        goOverlay.className = 'custom-overlay';
        goOverlay.innerHTML = `
            <div class="esc-box" style="border-color: #ff6b6b; box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);">
                <div class="esc-title" style="color: #ff6b6b; font-size: 40px; font-weight: bold;">💔 失败啦 T_T</div>
                <div style="color: #999; margin-bottom: 10px; font-size: 20px;">小蛋糕被碰坏了...</div>
                <button class="esc-btn" id="btn-go-retry" style="border-color: #ff6b6b; color: #ff6b6b;">↺ 重新护驾</button>
                <button class="esc-btn danger" id="btn-go-exit">✖ 回去碎觉</button>
            </div>
        `;
        
        const winOverlay = document.createElement('div');
        winOverlay.id = 'gamewin-overlay';
        winOverlay.className = 'custom-overlay';
        winOverlay.innerHTML = `
            <div class="esc-box" style="background: rgba(255,255,255,0.9); border-color: #ffd700; box-shadow: 0 15px 35px rgba(255, 215, 0, 0.4); text-shadow: 0 0 10px rgba(255,215,0,0.8);">
                <div style="font-size: 80px; line-height: 1; margin-bottom: -10px;">👑🐾</div>
                <div class="esc-title" style="color: #ffb347; font-size: 40px; font-weight: bold; margin-top: 10px;">恭喜你！清理完成啦！</div>
                <div style="color: #888; margin-bottom: 20px; font-size: 18px;">成功守护了所有小星星和小蛋糕 ✨</div>
                <div style="display: flex; gap: 15px; justify-content: center;">
                    <button class="esc-btn" id="btn-win-next" style="border-color: #ffd700; color: #ffaa00; background: #fffdf0; padding: 15px 40px;">▶ 下一关</button>
                    <button class="esc-btn" id="btn-win-retry" style="border-color: #ffb6c1; color: #ff69b4; padding: 15px 40px;">↺ 再玩一次</button>
                </div>
            </div>
            <canvas id="confetti-canvas" style="position: absolute; top:0; left:0; width:100vw; height:100vh; pointer-events:none; z-index:-1;"></canvas>
        `;
        
        function startConfetti() {
            const cvs = document.getElementById('confetti-canvas');
            if(!cvs) return;
            const ctx = cvs.getContext('2d');
            cvs.width = window.innerWidth; cvs.height = window.innerHeight;
            const pieces = [];
            for(let i=0; i<150; i++) {
                pieces.push({
                    x: Math.random() * cvs.width,
                    y: Math.random() * cvs.height - cvs.height,
                    vx: (Math.random() - 0.5) * 5,
                    vy: Math.random() * 3 + 2,
                    s: Math.random() * 10 + 5,
                    c: ['#ffb6c1', '#a8e6cf', '#ffd166', '#ff99cc', '#99ccff'][Math.floor(Math.random()*5)],
                    r: Math.random() * 360,
                    rs: (Math.random() - 0.5) * 10
                });
            }
            function loop() {
                ctx.clearRect(0,0,cvs.width,cvs.height);
                pieces.forEach(p => {
                    p.x += p.vx; p.y += p.vy; p.r += p.rs;
                    if(p.y > cvs.height) p.y = -20;
                    ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.r * Math.PI / 180);
                    ctx.fillStyle = p.c; ctx.fillRect(-p.s/2, -p.s/2, p.s, p.s);
                    ctx.restore();
                });
                if(winOverlay.style.display === 'flex') requestAnimationFrame(loop);
            }
            loop();
        }
        
        const lifeHud = document.createElement('div');
        lifeHud.id = 'hud-life';
        lifeHud.style.cssText = 'position: absolute; top: 15px; left: 20px; z-index: 9999; font-family: "Courier New", monospace; font-weight: bold; color: white; display: none; font-size: 24px; text-shadow: 2px 2px 0 #000; letter-spacing: 2px;';
        lifeHud.innerHTML = 'LIFE: <span id="life-hearts" style="color:white;">♥♥♥</span>';
        
        if (!document.getElementById('lxgw-font')) {
            const link = document.createElement('link');
            link.id = 'lxgw-font';
            link.rel = 'stylesheet';
            link.href = 'https://cdn.jsdelivr.net/npm/lxgw-wenkai-lite-webfont@1.1.0/style.css';
            document.head.appendChild(link);
        }
        
        document.body.appendChild(goOverlay);
        document.body.appendChild(winOverlay);
        document.body.appendChild(lifeHud);
        
        window.addEventListener('yyc_lives', (e) => {
            const hearts = Math.max(0, e.detail);
            document.getElementById('life-hearts').innerHTML = '<span style="color:white;">♥</span>'.repeat(hearts);
            if(goOverlay.style.display !== 'flex' && winOverlay.style.display !== 'flex') {
                lifeHud.style.display = 'block';
            }
        });

        [document.getElementById('btn-go-retry'), document.getElementById('btn-win-retry')].forEach(b => {
            if(b) {
                b.onmouseenter = playMarimba;
                b.onclick = () => { playMarimba(); setTimeout(()=>window.location.reload(), 150); };
            }
        });
        const winNextBtn = document.getElementById('btn-win-next');
        if(winNextBtn) {
            winNextBtn.onmouseenter = playMarimba;
            winNextBtn.onclick = () => { playMarimba(); setTimeout(()=>window.location.reload(), 150); }; // For now, restart handles next level
        }
        const goExitBtn = document.getElementById('btn-go-exit');
        if(goExitBtn) {
            goExitBtn.onmouseenter = playMarimba;
            goExitBtn.onclick = () => { playMarimba(); setTimeout(()=>{if(window.pywebview) window.pywebview.api.quit();}, 150) };
        }
        
        window.addEventListener('yyc_gameover', (e) => {
            lifeHud.style.display = 'none';
            document.body.classList.add('game-failed');
            const reason = e.detail;
            const subtitle = document.querySelector('
            if(subtitle) subtitle.innerText = reason === 'player' ? '小汽车抛锚了...' : '小蛋糕被碰坏了...';
            
            if(audioCtx.state === 'suspended') audioCtx.resume();
            [349.23, 329.63, 311.13, 293.66].forEach((freq, i) => {
                setTimeout(() => {
                    const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain();
                    osc.type = 'triangle'; osc.frequency.value = freq;
                    gain.gain.setValueAtTime(0.15, audioCtx.currentTime); 
                    gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.6);
                    osc.connect(gain); gain.connect(audioCtx.destination);
                    osc.start(); osc.stop(audioCtx.currentTime + 0.6);
                }, i * 300);
            });
            setTimeout(() => { goOverlay.style.display = 'flex'; }, 1000);
        });
        
        window.addEventListener('yyc_gamewin', () => {
            lifeHud.style.display = 'none';
            document.body.classList.add('game-won');
            if(audioCtx.state === 'suspended') audioCtx.resume();
            const melody = [
                {f: 523.25, d: 200}, {f: 523.25, d: 200}, {f: 523.25, d: 200}, {f: 523.25, d: 400},
                {f: 415.30, d: 400}, {f: 466.16, d: 400}, {f: 523.25, d: 200}, {f: 466.16, d: 200}, {f: 523.25, d: 800}
            ];
            let t = 0;
            melody.forEach(note => {
                setTimeout(() => {
                    const osc = audioCtx.createOscillator(); const gain = audioCtx.createGain();
                    osc.type = 'triangle'; osc.frequency.value = note.f;
                    gain.gain.setValueAtTime(0.12, audioCtx.currentTime); gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + note.d/1000);
                    osc.connect(gain); gain.connect(audioCtx.destination);
                    osc.start(); osc.stop(audioCtx.currentTime + note.d/1000);
                }, t);
                t += note.d;
            });
            setTimeout(() => { winOverlay.style.display = 'flex'; startConfetti(); }, 1200);
        });
        """
        try:
            win.evaluate_js(js_code)
        except Exception as e:
            print("[Injection Error]", e)

    win.events.loaded += on_loaded
    webview.start()
