// === Audio Engine (Web Audio API) ===
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
    osc.frequency.setValueAtTime(1046.50, audioCtx.currentTime);
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
    const bufferSize = audioCtx.sampleRate * 0.2;
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

// === ESC Pause Overlay ===
const overlay = document.createElement('div');
overlay.id = 'esc-overlay';
overlay.className = 'esc-overlay';
overlay.innerHTML = `
    <div class="esc-box">
        <div class="esc-title">\u2728 中场休息 \u2728</div>
        <button class="esc-btn" id="btn-continue">\u25b6 继续玩耍</button>
        <button class="esc-btn" id="btn-restart">\u21ba 返回主页</button>
        <button class="esc-btn danger" id="btn-exit">\u2716 溜了溜了</button>
    </div>
`;
document.body.appendChild(overlay);

document.querySelectorAll('.esc-btn').forEach(b => {
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

// === Game Over Overlay ===
const goOverlay = document.createElement('div');
goOverlay.id = 'gameover-overlay';
goOverlay.className = 'custom-overlay';
goOverlay.innerHTML = `
    <div class="esc-box" style="border-color: #ff6b6b; box-shadow: 0 15px 35px rgba(255, 107, 107, 0.2);">
        <div class="esc-title" style="color: #ff6b6b; font-size: 40px; font-weight: bold;">\ud83d\udc94 失败啦 T_T</div>
        <div style="color: #999; margin-bottom: 10px; font-size: 20px;">小蛋糕被碰坏了...</div>
        <button class="esc-btn" id="btn-go-retry" style="border-color: #ff6b6b; color: #ff6b6b;">\u21ba 重新护驾</button>
        <button class="esc-btn danger" id="btn-go-exit">\u2716 回去碎觉</button>
    </div>
`;

// === Game Win Overlay ===
const winOverlay = document.createElement('div');
winOverlay.id = 'gamewin-overlay';
winOverlay.className = 'custom-overlay';
winOverlay.innerHTML = `
    <div class="esc-box" style="background: rgba(255,255,255,0.9); border-color: #ffd700; box-shadow: 0 15px 35px rgba(255, 215, 0, 0.4); text-shadow: 0 0 10px rgba(255,215,0,0.8);">
        <div style="font-size: 80px; line-height: 1; margin-bottom: -10px;">\ud83d\udc51\ud83d\udc3e</div>
        <div class="esc-title" style="color: #ffb347; font-size: 40px; font-weight: bold; margin-top: 10px;">恭喜你！清理完成啦！</div>
        <div style="color: #888; margin-bottom: 20px; font-size: 18px;">成功守护了所有小星星和小蛋糕 \u2728</div>
        <div style="display: flex; gap: 15px; justify-content: center;">
            <button class="esc-btn" id="btn-win-next" style="border-color: #ffd700; color: #ffaa00; background: #fffdf0; padding: 15px 40px;">\u25b6 下一关</button>
            <button class="esc-btn" id="btn-win-retry" style="border-color: #ffb6c1; color: #ff69b4; padding: 15px 40px;">\u21ba 再玩一次</button>
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

// === Life HUD ===
const lifeHud = document.createElement('div');
lifeHud.id = 'hud-life';
lifeHud.style.cssText = 'position: absolute; top: 15px; left: 20px; z-index: 9999; font-family: "Courier New", monospace; font-weight: bold; color: white; display: none; font-size: 24px; text-shadow: 2px 2px 0 #000; letter-spacing: 2px;';
lifeHud.innerHTML = 'LIFE: <span id="life-hearts" style="color:white;">♥♥♥</span>';

// Load font
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

// === Event Listeners ===
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
    winNextBtn.onclick = () => { playMarimba(); setTimeout(()=>window.location.reload(), 150); };
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
    const subtitle = goOverlay.querySelectorAll('div')[1];
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

console.log('[game-inject.js] Audio + Overlays loaded OK');
