import React, { useState, useEffect, useRef, useCallback } from "react";

// ─────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────
const BASE_RADIUS = 30;

const RARITY = {
  COMMON:   { name: "common",   chance: 0.65, color: "#a78bfa", glow: "#7c3aed", mult: 1,  size: 1.0, label: ""           },
  UNCOMMON: { name: "uncommon", chance: 0.22, color: "#34d399", glow: "#059669", mult: 2,  size: 1.2, label: "BONUS x2"   },
  RARE:     { name: "rare",     chance: 0.10, color: "#fbbf24", glow: "#d97706", mult: 5,  size: 1.5, label: "RARE x5"    },
  EPIC:     { name: "epic",     chance: 0.03, color: "#f472b6", glow: "#db2777", mult: 15, size: 1.8, label: "EPIC x15"   },
};

const THEMES = [
  { id: "neon",   name: "Neon Purple", bg: "#0f0a1e", accent: "#a78bfa", secondary: "#6d28d9", unlockLevel: 1  },
  { id: "cyber",  name: "Cyber Blue",  bg: "#051520", accent: "#22d3ee", secondary: "#0e7490", unlockLevel: 5  },
  { id: "fire",   name: "Fire",        bg: "#1a0a00", accent: "#f97316", secondary: "#b45309", unlockLevel: 10 },
  { id: "matrix", name: "Matrix",      bg: "#001a00", accent: "#4ade80", secondary: "#166534", unlockLevel: 20 },
  { id: "gold",   name: "Gold",        bg: "#1a1400", accent: "#fbbf24", secondary: "#92400e", unlockLevel: 30 },
];

const ACHIEVEMENTS = [
  { id: "first_tap",    label: "First Blood",    desc: "Tap your first target",          icon: "👆" },
  { id: "streak_10",    label: "On Fire",         desc: "Reach a 10-tap streak",          icon: "🔥" },
  { id: "streak_50",    label: "Unstoppable",     desc: "Reach a 50-tap streak",          icon: "⚡" },
  { id: "first_rare",   label: "Lucky",           desc: "Hit your first rare target",     icon: "⭐" },
  { id: "first_epic",   label: "Legendary",       desc: "Hit your first epic target",     icon: "💎" },
  { id: "level_5",      label: "Rising",          desc: "Reach level 5",                  icon: "📈" },
  { id: "level_10",     label: "Veteran",         desc: "Reach level 10",                 icon: "🏆" },
  { id: "score_500",    label: "High Scorer",     desc: "Score 500 in one game",          icon: "💯" },
  { id: "score_2000",   label: "Master",          desc: "Score 2000 in one game",         icon: "🎯" },
  { id: "fever_mode",   label: "Fever!",          desc: "Trigger Fever Mode",             icon: "🌡️" },
  { id: "powerup_use",  label: "Power Hungry",    desc: "Use your first power-up",        icon: "⚡" },
  { id: "missions_all", label: "Daily Champion",  desc: "Complete all 3 daily missions",  icon: "📋" },
];

const MISSION_TEMPLATES = [
  { id: "tap_30",          desc: "Tap 30 targets",          key: "tapsTotal",        goal: 30  },
  { id: "combo_10",        desc: "Reach a 10x combo",       key: "bestCombo",        goal: 10  },
  { id: "score_500",       desc: "Score 500 points",        key: "score",            goal: 500 },
  { id: "hit_3_rare",      desc: "Hit 3 rare/epic targets", key: "rareHits",         goal: 3   },
  { id: "survive_60",      desc: "Survive 60 seconds",      key: "timeSurvived",     goal: 60  },
  { id: "fever_1",         desc: "Trigger Fever Mode",      key: "feverCount",       goal: 1   },
  { id: "powerup_3",       desc: "Collect 3 power-ups",     key: "powerupCollected", goal: 3   },
];

const XP_PER_LEVEL   = 100;
const FEVER_STREAK   = 15;
const FEVER_DURATION = 8000;

// ─────────────────────────────────────────────
// AUDIO ENGINE
// ─────────────────────────────────────────────
function createAudio() {
  let ctx = null;
  const getCtx = () => {
    if (!ctx) ctx = new (window.AudioContext || window.webkitAudioContext)();
    return ctx;
  };
  const tone = (freq, type, dur, vol = 0.3, delay = 0) => {
    try {
      const c = getCtx();
      const o = c.createOscillator();
      const g = c.createGain();
      o.connect(g); g.connect(c.destination);
      o.type = type;
      o.frequency.setValueAtTime(freq, c.currentTime + delay);
      g.gain.setValueAtTime(vol, c.currentTime + delay);
      g.gain.exponentialRampToValueAtTime(0.001, c.currentTime + delay + dur);
      o.start(c.currentTime + delay);
      o.stop(c.currentTime + delay + dur + 0.05);
    } catch {}
  };
  return {
    tap:        () => { tone(520, "sine",     0.1,  0.25); tone(780,  "sine",     0.08, 0.1,  0.05); },
    miss:       () => { tone(200, "sawtooth", 0.3,  0.2);  },
    rare:       () => { tone(660, "sine", 0.15, 0.3); tone(880,  "sine", 0.15, 0.25, 0.08); tone(1100, "sine", 0.12, 0.2, 0.16); },
    epic:       () => { [440, 554, 659, 880, 1108].forEach((f, i) => tone(f, "sine", 0.25, 0.3, i * 0.07)); },
    bomb:       () => { tone(120, "sawtooth", 0.4,  0.35); tone(80,   "sawtooth", 0.3,  0.25, 0.1); },
    bombHit:    () => { tone(100, "sawtooth", 0.5,  0.4);  tone(60,   "sawtooth", 0.3,  0.3,  0.15); },
    powerUp:    () => { [440, 554, 659, 880].forEach((f, i) => tone(f, "sine", 0.15, 0.25, i * 0.06)); },
    feverStart: () => { [440, 554, 659, 880].forEach((f, i) => tone(f, "square", 0.12, 0.2, i * 0.05)); },
    feverEnd:   () => { [880, 659, 554, 440].forEach((f, i) => tone(f, "sine",   0.12, 0.2, i * 0.06)); },
    levelUp:    () => { [523, 659, 784, 1047].forEach((f, i) => tone(f, "sine",  0.15, 0.3, i * 0.08)); },
  };
}

// ─────────────────────────────────────────────
// HELPERS
// ─────────────────────────────────────────────
function getRarity() {
  const r = Math.random();
  let cumul = 0;
  for (const v of Object.values(RARITY)) {
    cumul += v.chance;
    if (r < cumul) return v;
  }
  return RARITY.COMMON;
}

function getLevelFromXP(xp)  { return Math.floor(xp / XP_PER_LEVEL) + 1; }

function seededRng(seed) {
  let s = seed;
  return () => { s = (s * 1664525 + 1013904223) & 0xffffffff; return (s >>> 0) / 0xffffffff; };
}

function getDailyMissions() {
  const d = new Date();
  const seed = d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
  const rng  = seededRng(seed);
  return [...MISSION_TEMPLATES].sort(() => rng() - 0.5).slice(0, 3);
}

function getTodayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
}

const DEFAULT_SAVE = {
  highScore: 0, xp: 0, bestStreak: 0,
  unlockedAchievements: [],
  themeId: "neon", soundEnabled: true,
  scores: [],
  lastLoginDate: null,
  missionDate: null, missionProgress: {}, missionCompleted: false,
};

function loadSave() {
  try {
    const raw = localStorage.getItem("nexustap_v3");
    if (raw) return { ...DEFAULT_SAVE, ...JSON.parse(raw) };
  } catch {}
  return { ...DEFAULT_SAVE };
}

function vibrate(pattern) {
  try { if (navigator.vibrate) navigator.vibrate(pattern); } catch {}
}

// ─────────────────────────────────────────────
// NEON BUTTON
// ─────────────────────────────────────────────
function NeonButton({ children, onClick, style, className = "", disabled = false }) {
  const [pressed, setPressed] = useState(false);
  return (
    <button
      disabled={disabled}
      onMouseDown={() => setPressed(true)}
      onMouseUp={() => setPressed(false)}
      onMouseLeave={() => setPressed(false)}
      onTouchStart={(e) => { e.preventDefault(); setPressed(true); }}
      onTouchEnd={(e) => { e.preventDefault(); setPressed(false); if (!disabled && onClick) onClick(e); }}
      onClick={(e) => { if (!disabled && onClick) onClick(e); }}
      className={`select-none transition-all duration-100 rounded-xl font-bold text-white ${className}`}
      style={{
        transform: pressed ? "scale(0.94)" : "scale(1)",
        opacity: disabled ? 0.4 : 1,
        cursor: disabled ? "not-allowed" : "pointer",
        userSelect: "none",
        WebkitTapHighlightColor: "transparent",
        ...style,
      }}
    >
      {children}
    </button>
  );
}

// ─────────────────────────────────────────────
// TARGET SVG SHAPES
// ─────────────────────────────────────────────
function TargetShape({ type, rarity, radius: r, color, glow, bombPulse }) {
  const shadow = `drop-shadow(0 0 ${r * 0.4}px ${glow})`;

  if (type === "bomb") {
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <circle cx={r} cy={r} r={r - 2} fill="#1a0000" stroke="#ef4444" strokeWidth={3}
          style={{ filter: `drop-shadow(0 0 ${bombPulse ? 14 : 6}px #ef4444)` }} />
        <line x1={r * 0.42} y1={r * 0.42} x2={r * 1.58} y2={r * 1.58} stroke="#ef4444" strokeWidth={3} strokeLinecap="round" />
        <line x1={r * 1.58} y1={r * 0.42} x2={r * 0.42} y2={r * 1.58} stroke="#ef4444" strokeWidth={3} strokeLinecap="round" />
      </svg>
    );
  }

  if (type === "powerup") {
    const arm = r * 0.55, thick = r * 0.32;
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <circle cx={r} cy={r} r={r - 2} fill="#1e3a8a" stroke="#60a5fa" strokeWidth={2}
          style={{ filter: "drop-shadow(0 0 8px #3b82f6)" }} />
        <rect x={r - thick / 2} y={r - arm} width={thick} height={arm * 2} rx={thick / 2} fill="#60a5fa" />
        <rect x={r - arm} y={r - thick / 2} width={arm * 2} height={thick} rx={thick / 2} fill="#60a5fa" />
      </svg>
    );
  }

  if (rarity?.name === "common") {
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <circle cx={r} cy={r} r={r - 2}    fill={color + "33"} stroke={color} strokeWidth={2.5} style={{ filter: shadow }} />
        <circle cx={r} cy={r} r={r * 0.62} fill="none"         stroke={color} strokeWidth={1.5} opacity={0.6} />
        <circle cx={r} cy={r} r={r * 0.28} fill={color}        opacity={0.9} />
      </svg>
    );
  }

  if (rarity?.name === "uncommon") {
    const d = r - 3;
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <polygon points={`${r},${r - d} ${r + d},${r} ${r},${r + d} ${r - d},${r}`}
          fill={color + "33"} stroke={color} strokeWidth={2.5} style={{ filter: shadow }} />
        <polygon points={`${r},${r - d * 0.55} ${r + d * 0.55},${r} ${r},${r + d * 0.55} ${r - d * 0.55},${r}`}
          fill={color} opacity={0.7} />
      </svg>
    );
  }

  if (rarity?.name === "rare") {
    const pts = Array.from({ length: 5 }, (_, i) => {
      const a = (i * 72 - 90) * Math.PI / 180;
      const b = (i * 72 - 90 + 36) * Math.PI / 180;
      const or = r - 3, ir = (r - 3) * 0.45;
      return `${r + or * Math.cos(a)},${r + or * Math.sin(a)} ${r + ir * Math.cos(b)},${r + ir * Math.sin(b)}`;
    }).join(" ");
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <polygon points={pts} fill={color + "55"} stroke={color} strokeWidth={2.5} style={{ filter: shadow }} />
        <polygon points={pts} fill="none" stroke={color} strokeWidth={1} opacity={0.4}
          transform={`rotate(6, ${r}, ${r})`} />
      </svg>
    );
  }

  if (rarity?.name === "epic") {
    const pts = Array.from({ length: 6 }, (_, i) => {
      const a = (i * 60 - 90) * Math.PI / 180;
      const b = (i * 60 - 90 + 30) * Math.PI / 180;
      const or = r - 3, ir = (r - 3) * 0.5;
      return `${r + or * Math.cos(a)},${r + or * Math.sin(a)} ${r + ir * Math.cos(b)},${r + ir * Math.sin(b)}`;
    }).join(" ");
    return (
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        <polygon points={pts} fill={color + "44"} stroke={color} strokeWidth={2.5} style={{ filter: shadow }} />
        <polygon points={pts} fill="none" stroke={color} strokeWidth={1.5} opacity={0.5}
          transform={`rotate(15, ${r}, ${r})`} />
        <circle cx={r} cy={r} r={r * 0.22} fill={color} />
      </svg>
    );
  }

  return null;
}

// ─────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────
export default function NexusTap() {
  // Persistent data
  const saveRef      = useRef(loadSave());
  const audioRef     = useRef(null);
  const saveTimerRef = useRef(null);

  // UI state
  const [screen,       setScreen]       = useState("menu");
  const [theme,        setTheme]        = useState(() => THEMES.find(t => t.id === saveRef.current.themeId) || THEMES[0]);
  const [soundOn,      setSoundOn]      = useState(() => saveRef.current.soundEnabled);
  const [notification, setNotification] = useState(null);

  // Game display state
  const [scoreDisplay,   setScoreDisplay]   = useState(0);
  const [livesDisplay,   setLivesDisplay]   = useState(3);
  const [streakDisplay,  setStreakDisplay]  = useState(0);
  const [feverDisplay,   setFeverDisplay]   = useState(false);
  const [targetsDisplay, setTargetsDisplay] = useState([]);
  const [particlesDisp,  setParticlesDisp]  = useState([]);
  const [popupsDisp,     setPopupsDisp]     = useState([]);
  const [activePwrDisp,  setActivePwrDisp]  = useState([]);
  const [gameOverData,   setGameOverData]   = useState(null);
  const [screenShake,    setScreenShake]    = useState(false);
  const [epicFlash,      setEpicFlash]      = useState(false);

  // Game refs (mutation only, no re-renders)
  const gsRef          = useRef(null);
  const targetsRef     = useRef([]);
  const particlesRef   = useRef([]);
  const popupsRef      = useRef([]);
  const activePwrRef   = useRef([]);
  const rafRef         = useRef(null);
  const lastTickRef    = useRef(0);
  const spawnTimerRef  = useRef(0);
  const bombPulseRef   = useRef(false);
  const canvasRef      = useRef(null);
  const bgParticlesRef = useRef([]);
  const ripplePoolRef  = useRef([]);
  const missionProgRef = useRef({});

  // ── Audio ──
  useEffect(() => { audioRef.current = createAudio(); }, []);
  const sfx = useCallback((name) => {
    if (soundOn && audioRef.current?.[name]) audioRef.current[name]();
  }, [soundOn]);

  // ── Save ──
  const flushSave = useCallback(() => {
    try { localStorage.setItem("nexustap_v3", JSON.stringify(saveRef.current)); } catch {}
  }, []);
  const debouncedSave = useCallback(() => {
    if (saveTimerRef.current) clearTimeout(saveTimerRef.current);
    saveTimerRef.current = setTimeout(flushSave, 2000);
  }, [flushSave]);

  // ── Notifications ──
  useEffect(() => {
    if (!notification) return;
    const t = setTimeout(() => setNotification(null), 2500);
    return () => clearTimeout(t);
  }, [notification]);

  // ── Achievements ──
  const unlockAchievement = useCallback((id) => {
    const sv = saveRef.current;
    if (sv.unlockedAchievements.includes(id)) return;
    sv.unlockedAchievements = [...sv.unlockedAchievements, id];
    const ach = ACHIEVEMENTS.find(a => a.id === id);
    if (ach) setNotification(`${ach.icon} ${ach.label} unlocked!`);
    debouncedSave();
  }, [debouncedSave]);

  // ── Daily login XP ──
  useEffect(() => {
    const sv = saveRef.current;
    const today = getTodayKey();
    if (sv.lastLoginDate !== today) {
      sv.lastLoginDate = today;
      const prevLevel = getLevelFromXP(sv.xp);
      sv.xp += 20;
      const newLevel = getLevelFromXP(sv.xp);
      if (newLevel > prevLevel) setNotification(`Level Up! Now Level ${newLevel}!`);
      else setNotification("Daily bonus! +20 XP");
      flushSave();
    }
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Missions ──
  const initMissions = useCallback(() => {
    const sv = saveRef.current;
    const today = getTodayKey();
    if (sv.missionDate !== today) {
      sv.missionDate = today;
      sv.missionProgress = {};
      sv.missionCompleted = false;
      flushSave();
    }
    missionProgRef.current = { ...sv.missionProgress };
  }, [flushSave]);

  const updateMissions = useCallback((stats) => {
    const missions = getDailyMissions();
    const prog = missionProgRef.current;
    let changed = false;
    missions.forEach(m => {
      const cur = prog[m.id] || 0;
      const val = stats[m.key] || 0;
      if (val > cur) { prog[m.id] = Math.min(val, m.goal); changed = true; }
    });
    if (changed) {
      saveRef.current.missionProgress = { ...prog };
      if (missions.every(m => (prog[m.id] || 0) >= m.goal) && !saveRef.current.missionCompleted) {
        saveRef.current.missionCompleted = true;
        saveRef.current.xp += 200;
        setNotification("All daily missions complete! +200 XP");
        unlockAchievement("missions_all");
      }
      debouncedSave();
    }
  }, [debouncedSave, unlockAchievement]);

  // ── Canvas ──
  const initBgParticles = useCallback(() => {
    bgParticlesRef.current = Array.from({ length: 40 }, () => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.4,
      vy: (Math.random() - 0.5) * 0.4,
      r: Math.random() * 2 + 1,
      alpha: Math.random() * 0.4 + 0.1,
    }));
  }, []);

  const drawCanvas = useCallback((ts) => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    const w = canvas.width, h = canvas.height;
    ctx.clearRect(0, 0, w, h);

    const fever = gsRef.current?.feverActive;
    const gridSize = 40;
    const pulse = 0.5 + 0.5 * Math.sin(ts / 1200);

    // grid
    ctx.save();
    ctx.strokeStyle = fever ? `rgba(251,191,36,${0.05 + pulse * 0.03})` : `rgba(167,139,250,${0.03 + pulse * 0.02})`;
    ctx.lineWidth = 1;
    for (let x = 0; x < w; x += gridSize) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
    for (let y = 0; y < h; y += gridSize) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }
    ctx.restore();

    // accent grid lines
    ctx.save();
    ctx.strokeStyle = fever ? `rgba(251,191,36,0.15)` : `rgba(167,139,250,0.08)`;
    ctx.lineWidth = 1.5;
    ctx.globalAlpha = 0.5 + pulse * 0.5;
    for (let x = 0; x < w; x += gridSize * 4) { ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, h); ctx.stroke(); }
    for (let y = 0; y < h; y += gridSize * 4) { ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(w, y); ctx.stroke(); }
    ctx.restore();

    // ambient particles
    bgParticlesRef.current.forEach(p => {
      p.x += p.vx; p.y += p.vy;
      if (p.x < 0) p.x = w; if (p.x > w) p.x = 0;
      if (p.y < 0) p.y = h; if (p.y > h) p.y = 0;
      ctx.save();
      ctx.globalAlpha = p.alpha;
      ctx.fillStyle = fever ? "#fbbf24" : "#a78bfa";
      ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
    });

    // tap ripples
    ripplePoolRef.current = ripplePoolRef.current.filter(rp => {
      rp.r += 3; rp.alpha -= 0.045;
      if (rp.alpha <= 0) return false;
      ctx.save();
      ctx.globalAlpha = rp.alpha;
      ctx.strokeStyle = rp.color;
      ctx.lineWidth = 2;
      ctx.beginPath(); ctx.arc(rp.x, rp.y, rp.r, 0, Math.PI * 2); ctx.stroke();
      ctx.restore();
      return true;
    });
  }, []);

  // ── Spawn ──
  const pickSpawnPos = useCallback((radius) => {
    const margin = radius * 1.6 + 20;
    const w = window.innerWidth, h = window.innerHeight;
    let best = null, bestDist = -1;
    for (let i = 0; i < 5; i++) {
      const x = margin + Math.random() * (w - margin * 2);
      const y = margin + 90 + Math.random() * (h - margin * 2 - 90);
      let minDist = Infinity;
      targetsRef.current.forEach(t => {
        const d = Math.hypot(t.x - x, t.y - y);
        if (d < minDist) minDist = d;
      });
      if (minDist > bestDist) { bestDist = minDist; best = { x, y }; }
    }
    return best;
  }, []);

  const spawnTarget = useCallback(() => {
    const gs = gsRef.current;
    if (!gs || gs.lives <= 0) return;

    const diff = Math.min(10, 1 + gs.score / 200);
    const bombChance  = Math.min(0.18, 0.04 + diff * 0.01);
    const powerChance = 0.08;
    const r = Math.random();

    let type = "normal", rarity = getRarity(), color, glow;
    if (r < bombChance) {
      type = "bomb"; color = "#ef4444"; glow = "#dc2626"; sfx("bomb");
    } else if (r < bombChance + powerChance) {
      type = "powerup"; color = "#60a5fa"; glow = "#3b82f6";
    } else {
      color = rarity.color; glow = rarity.glow;
    }

    const radius = type === "normal" ? BASE_RADIUS * rarity.size : BASE_RADIUS;
    const pos = pickSpawnPos(radius);
    if (!pos) return;

    let lifetime = Math.max(1500, 3000 - diff * 150);
    if (activePwrRef.current.some(p => p.type === "SLOW" && p.endsAt > Date.now())) lifetime *= 1.5;

    targetsRef.current.push({
      id: Math.random().toString(36).slice(2),
      type, rarity: type === "normal" ? rarity : null,
      x: pos.x, y: pos.y, radius, color, glow,
      lifetime, spawnedAt: Date.now(), born: performance.now(),
    });
    setTargetsDisplay([...targetsRef.current]);
  }, [sfx, pickSpawnPos]);

  // ── Particles / popups ──
  const spawnParticles = useCallback((x, y, color, count = 10) => {
    const now = performance.now();
    const newP = Array.from({ length: count }, () => ({
      id: Math.random().toString(36).slice(2),
      x, y,
      vx: (Math.random() - 0.5) * 8,
      vy: (Math.random() - 0.5) * 8,
      color,
      size: Math.random() * 5 + 2,
      life: 1,
      born: now,
      duration: 500 + Math.random() * 300,
    }));
    particlesRef.current = [...particlesRef.current, ...newP];
  }, []);

  const spawnPopup = useCallback((x, y, text, color) => {
    const id = Math.random().toString(36).slice(2);
    popupsRef.current = [...popupsRef.current, { id, x, y, text, color, born: performance.now() }];
    setPopupsDisp([...popupsRef.current]);
  }, []);

  // ── Power-ups ──
  const activatePowerUp = useCallback((x, y) => {
    const gs = gsRef.current;
    const types = ["SHIELD", "SLOW", "DOUBLE", "LIFE"];
    const type = types[Math.floor(Math.random() * types.length)];
    sfx("powerUp");
    vibrate([10, 30, 10]);
    unlockAchievement("powerup_use");
    if (type === "LIFE") {
      if (gs.lives < 3) { gs.lives++; setLivesDisplay(gs.lives); }
      spawnPopup(x, y, "+LIFE", "#34d399");
    } else {
      const dur = type === "SLOW" ? 6000 : 8000;
      activePwrRef.current = activePwrRef.current.filter(p => p.type !== type);
      activePwrRef.current.push({ type, endsAt: Date.now() + dur });
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x, y, `+${type}`, "#60a5fa");
    }
    const cur = missionProgRef.current;
    missionProgRef.current = { ...cur, powerupCollected: (cur.powerupCollected || 0) + 1 };
  }, [sfx, spawnPopup, unlockAchievement]);

  // ── End game ──
  const endGame = useCallback(() => {
    const gs = gsRef.current;
    if (!gs) return;
    if (rafRef.current) { cancelAnimationFrame(rafRef.current); rafRef.current = null; }

    const sv = saveRef.current;
    const score = gs.score;
    const isNewHigh = score > sv.highScore;
    if (isNewHigh) sv.highScore = score;
    if (gs.streak > sv.bestStreak) sv.bestStreak = gs.streak;

    const xpEarned = Math.floor(score / 10) + gs.sessionStats.rareHits * 5;
    const prevLevel = getLevelFromXP(sv.xp);
    sv.xp += xpEarned;
    if (getLevelFromXP(sv.xp) > prevLevel) sfx("levelUp");

    sv.scores = [score, ...sv.scores].slice(0, 10).sort((a, b) => b - a);

    let grade = "D";
    const ratio = sv.highScore > 0 ? score / sv.highScore : 0;
    if      (ratio >= 0.9) grade = "S";
    else if (ratio >= 0.7) grade = "A";
    else if (ratio >= 0.5) grade = "B";
    else if (ratio >= 0.3) grade = "C";
    if (sv.scores.length === 1) grade = "C";

    const soClose = !isNewHigh && sv.highScore > 0 && (sv.highScore - score) / sv.highScore < 0.15;
    const timeSurvived = Math.floor((Date.now() - gs.startTime) / 1000);
    updateMissions({ ...gs.sessionStats, timeSurvived });

    setGameOverData({
      score, isNewHigh, grade, xpEarned,
      soClose: soClose ? sv.highScore - score : null,
      bestStreak: sv.bestStreak,
      sessionStats: { ...gs.sessionStats, timeSurvived },
    });

    flushSave();
    gsRef.current = null;
    targetsRef.current = [];
    activePwrRef.current = [];
    setTargetsDisplay([]);
    setActivePwrDisp([]);
    setScreen("gameover");
  }, [sfx, flushSave, updateMissions]);

  // ── Game loop ──
  const gameLoop = useCallback((ts) => {
    const gs = gsRef.current;
    if (!gs) return;

    const dt = Math.min(100, ts - lastTickRef.current);
    lastTickRef.current = ts;
    bombPulseRef.current = Math.sin(ts / 400) > 0;

    drawCanvas(ts);

    const now = Date.now();
    let lostLife = false;

    targetsRef.current = targetsRef.current.filter(t => {
      const age = now - t.spawnedAt;
      if (age < t.lifetime) return true;
      if (t.type === "bomb" || t.type === "powerup") return false;
      // missed normal target
      gs.streak = 0;
      const hasShield = activePwrRef.current.some(p => p.type === "SHIELD" && p.endsAt > now);
      if (hasShield) {
        activePwrRef.current = activePwrRef.current.filter(p => p.type !== "SHIELD");
        setActivePwrDisp([...activePwrRef.current]);
      } else {
        gs.lives--;
        sfx("miss");
        vibrate(40);
        lostLife = true;
      }
      return false;
    });

    if (lostLife) {
      setLivesDisplay(gs.lives);
      setStreakDisplay(0);
      if (gs.lives <= 0) { endGame(); return; }
    }

    // expire power-ups
    const prevPwrLen = activePwrRef.current.length;
    activePwrRef.current = activePwrRef.current.filter(p => p.endsAt > now);
    if (activePwrRef.current.length !== prevPwrLen) setActivePwrDisp([...activePwrRef.current]);

    // fever countdown
    if (gs.feverActive) {
      gs.feverTimeLeft -= dt;
      if (gs.feverTimeLeft <= 0) {
        gs.feverActive = false;
        setFeverDisplay(false);
        sfx("feverEnd");
      }
    }

    // spawn
    spawnTimerRef.current += dt;
    const diff = Math.min(10, 1 + gs.score / 200);
    const spawnInterval = Math.max(600, 1400 - diff * 70);
    if (spawnTimerRef.current >= spawnInterval) {
      spawnTimerRef.current = 0;
      spawnTarget();
    }

    // particles
    const pnow = performance.now();
    particlesRef.current = particlesRef.current.filter(p => {
      const age = pnow - p.born;
      p.life = 1 - age / p.duration;
      p.x += p.vx * 0.95; p.y += p.vy * 0.95; p.vy += 0.12;
      return p.life > 0;
    });
    setParticlesDisp([...particlesRef.current]);

    // popups
    popupsRef.current = popupsRef.current.filter(p => (pnow - p.born) < 900);
    setPopupsDisp([...popupsRef.current]);
    setTargetsDisplay([...targetsRef.current]);

    rafRef.current = requestAnimationFrame(gameLoop);
  }, [drawCanvas, sfx, spawnTarget, endGame]);

  // ── Tap handler ──
  const handleTap = useCallback((e) => {
    e.preventDefault();
    const gs = gsRef.current;
    if (!gs || gs.lives <= 0) return;

    const rect = e.currentTarget.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const clientY = e.touches ? e.touches[0].clientY : e.clientY;
    const tx = clientX - rect.left;
    const ty = clientY - rect.top;

    let hit = null, hitDist = Infinity;
    for (const t of targetsRef.current) {
      const d = Math.hypot(t.x - tx, t.y - ty);
      if (d < t.radius * 1.3 && d < hitDist) { hit = t; hitDist = d; }
    }

    ripplePoolRef.current.push({
      x: tx, y: ty, r: 10, alpha: 0.7,
      color: hit ? (hit.color || "#a78bfa") : "#ffffff55",
    });

    if (!hit) return;

    targetsRef.current = targetsRef.current.filter(t => t.id !== hit.id);
    setTargetsDisplay([...targetsRef.current]);

    if (hit.type === "bomb") {
      sfx("bombHit");
      vibrate(40);
      spawnParticles(hit.x, hit.y, "#ef4444", 14);
      const hasShield = activePwrRef.current.some(p => p.type === "SHIELD" && p.endsAt > Date.now());
      if (hasShield) {
        activePwrRef.current = activePwrRef.current.filter(p => p.type !== "SHIELD");
        setActivePwrDisp([...activePwrRef.current]);
        spawnPopup(hit.x, hit.y, "SHIELD!", "#60a5fa");
      } else {
        gs.lives = Math.max(0, gs.lives - 1);
        gs.streak = 0;
        setLivesDisplay(gs.lives);
        setStreakDisplay(0);
        spawnPopup(hit.x, hit.y, "BOMB!", "#ef4444");
        setScreenShake(true);
        setTimeout(() => setScreenShake(false), 400);
        if (gs.lives <= 0) endGame();
      }
      return;
    }

    if (hit.type === "powerup") {
      activatePowerUp(hit.x, hit.y);
      spawnParticles(hit.x, hit.y, "#60a5fa", 12);
      gs.sessionStats.powerupCollected = (gs.sessionStats.powerupCollected || 0) + 1;
      return;
    }

    // normal target
    gs.streak++;
    const combo = Math.min(10, 1 + Math.floor(gs.streak / 5));
    const isDouble = activePwrRef.current.some(p => p.type === "DOUBLE" && p.endsAt > Date.now());
    const feverMult = gs.feverActive ? 2 : 1;
    const pts = hit.rarity.mult * combo * feverMult * (isDouble ? 2 : 1);
    gs.score += pts;
    gs.sessionStats.tapsTotal++;
    gs.sessionStats.score = gs.score;
    if (hit.rarity.name === "rare" || hit.rarity.name === "epic") gs.sessionStats.rareHits++;
    if (gs.streak > gs.sessionStats.bestCombo) gs.sessionStats.bestCombo = gs.streak;

    setScoreDisplay(gs.score);
    setStreakDisplay(gs.streak);

    if (hit.rarity.name === "epic") {
      sfx("epic"); vibrate([20, 30, 20]);
      setEpicFlash(true); setTimeout(() => setEpicFlash(false), 400);
      spawnParticles(hit.x, hit.y, hit.color, 30);
    } else if (hit.rarity.name === "rare") {
      sfx("rare"); vibrate([20, 20]);
      spawnParticles(hit.x, hit.y, hit.color, 18);
    } else {
      sfx("tap"); vibrate(10);
      spawnParticles(hit.x, hit.y, hit.color, 8);
    }

    if (hit.rarity.label) spawnPopup(hit.x, hit.y, hit.rarity.label, hit.color);

    unlockAchievement("first_tap");
    if (hit.rarity.name === "rare" || hit.rarity.name === "epic") unlockAchievement("first_rare");
    if (hit.rarity.name === "epic") unlockAchievement("first_epic");
    if (gs.streak >= 10)  unlockAchievement("streak_10");
    if (gs.streak >= 50)  unlockAchievement("streak_50");
    if (gs.score >= 500)  unlockAchievement("score_500");
    if (gs.score >= 2000) unlockAchievement("score_2000");

    // Fever
    if (gs.streak >= FEVER_STREAK && !gs.feverActive) {
      gs.feverActive = true;
      gs.feverTimeLeft = FEVER_DURATION;
      setFeverDisplay(true);
      sfx("feverStart");
      vibrate([30, 20, 30, 20, 50]);
      spawnPopup(hit.x, hit.y - 30, "FEVER!", "#fbbf24");
      unlockAchievement("fever_mode");
      gs.sessionStats.feverCount = (gs.sessionStats.feverCount || 0) + 1;
    }

    updateMissions({ ...gs.sessionStats, bestCombo: gs.streak });
    debouncedSave();
  }, [sfx, spawnParticles, spawnPopup, activatePowerUp, unlockAchievement, updateMissions, debouncedSave, endGame]);

  // ── Start game ──
  const startGame = useCallback(() => {
    initMissions();
    particlesRef.current   = [];
    popupsRef.current      = [];
    targetsRef.current     = [];
    activePwrRef.current   = [];
    ripplePoolRef.current  = [];
    spawnTimerRef.current  = 0;

    gsRef.current = {
      score: 0, lives: 3, streak: 0,
      feverActive: false, feverTimeLeft: 0,
      startTime: Date.now(),
      sessionStats: { tapsTotal: 0, rareHits: 0, bestCombo: 0, score: 0, feverCount: 0, powerupCollected: 0 },
    };

    setScoreDisplay(0); setLivesDisplay(3); setStreakDisplay(0);
    setFeverDisplay(false); setTargetsDisplay([]); setParticlesDisp([]);
    setPopupsDisp([]); setActivePwrDisp([]); setGameOverData(null);
    setEpicFlash(false); setScreenShake(false);

    setScreen("playing");
    lastTickRef.current = performance.now();
    rafRef.current = requestAnimationFrame(gameLoop);
  }, [initMissions, gameLoop]);

  // cleanup
  useEffect(() => () => { if (rafRef.current) cancelAnimationFrame(rafRef.current); }, []);

  // canvas resize
  useEffect(() => {
    const resize = () => {
      if (canvasRef.current) {
        canvasRef.current.width  = window.innerWidth;
        canvasRef.current.height = window.innerHeight;
      }
    };
    resize();
    window.addEventListener("resize", resize);
    initBgParticles();
    return () => window.removeEventListener("resize", resize);
  }, [initBgParticles]);

  // menu canvas animation
  useEffect(() => {
    if (screen !== "menu") return;
    let raf;
    const loop = (ts) => { drawCanvas(ts); raf = requestAnimationFrame(loop); };
    raf = requestAnimationFrame(loop);
    return () => cancelAnimationFrame(raf);
  }, [screen, drawCanvas]);

  // ── Combo color ──
  const comboColor = () => {
    const s = streakDisplay;
    if (s >= 20) return "#ff00ff";
    if (s >= 15) return "#ef4444";
    if (s >= 10) return "#f97316";
    if (s >= 5)  return "#fbbf24";
    return "#ffffff";
  };

  const sv  = saveRef.current;
  const lvl = getLevelFromXP(sv.xp);

  // ════════════════════════════════════════════
  // SCREEN RENDERERS
  // ════════════════════════════════════════════

  const renderMenu = () => (
    <div className="flex flex-col items-center justify-center h-full gap-4 px-6 relative z-10">
      <div className="text-center mb-2">
        <h1 className="text-5xl font-black tracking-widest mb-1"
          style={{ color: theme.accent, textShadow: `0 0 30px ${theme.accent}` }}>
          NEXUS<span style={{ color: "#f472b6" }}>TAP</span>
        </h1>
        <p className="text-xs opacity-50 mb-1" style={{ color: theme.accent }}>
          Level {lvl} · {sv.xp % XP_PER_LEVEL}/{XP_PER_LEVEL} XP to next
        </p>
        <div className="w-36 h-1.5 rounded-full mx-auto" style={{ background: "#ffffff22" }}>
          <div className="h-full rounded-full transition-all"
            style={{ width: `${(sv.xp % XP_PER_LEVEL) / XP_PER_LEVEL * 100}%`, background: theme.accent }} />
        </div>
      </div>

      <NeonButton onClick={startGame} className="w-full py-4 text-2xl"
        style={{ background: `linear-gradient(135deg, ${theme.secondary}, ${theme.accent})`,
          boxShadow: `0 0 28px ${theme.accent}88` }}>
        ▶ PLAY
      </NeonButton>

      <div className="grid grid-cols-2 gap-3 w-full">
        {[
          { label: "🎯 Daily Missions",  sc: "missions"     },
          { label: "🏆 Leaderboard",     sc: "leaderboard"  },
          { label: "🎖 Medals",          sc: "achievements" },
          { label: "⚙ Settings",        sc: "settings"     },
        ].map(b => (
          <NeonButton key={b.sc} onClick={() => setScreen(b.sc)} className="py-3 text-sm"
            style={{ background: "#ffffff10", border: `1px solid ${theme.accent}44` }}>
            {b.label}
          </NeonButton>
        ))}
      </div>

      {sv.highScore > 0 && (
        <p className="text-sm opacity-40 mt-1" style={{ color: theme.accent }}>
          Best: {sv.highScore.toLocaleString()}
        </p>
      )}
    </div>
  );

  const renderPlaying = () => (
    <div className="absolute inset-0 overflow-hidden"
      onTouchStart={handleTap} onClick={handleTap}
      style={{ touchAction: "none" }}>

      {/* HUD */}
      <div className="absolute top-0 left-0 right-0 z-20 flex items-center justify-between px-4 py-3"
        style={{ background: "rgba(0,0,0,0.55)", backdropFilter: "blur(4px)" }}>
        <div className="text-center">
          <div className="text-xs opacity-50" style={{ color: theme.accent }}>SCORE</div>
          <div className="text-2xl font-black" style={{ color: theme.accent }}>{scoreDisplay.toLocaleString()}</div>
        </div>
        <div className="flex gap-1">
          {Array.from({ length: 3 }, (_, i) => (
            <span key={i} className="text-xl">{i < livesDisplay ? "❤️" : "🖤"}</span>
          ))}
        </div>
        <div className="text-center">
          <div className="text-xs opacity-50" style={{ color: theme.accent }}>STREAK</div>
          <div className="text-2xl font-black" style={{ color: comboColor(),
            textShadow: streakDisplay >= 5 ? `0 0 12px ${comboColor()}` : "none" }}>
            {streakDisplay}×
          </div>
        </div>
      </div>

      {/* Active power-ups bar */}
      {activePwrDisp.length > 0 && (
        <div className="absolute z-20 flex justify-center gap-2 left-0 right-0" style={{ top: 72 }}>
          {activePwrDisp.map(p => (
            <div key={p.type} className="px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1"
              style={{ background: "#1e3a8acc", border: "1px solid #60a5fa66", color: "#60a5fa" }}>
              {p.type === "SHIELD" ? "🛡" : p.type === "SLOW" ? "🐢" : p.type === "DOUBLE" ? "×2" : "❤️"}
              {" "}{p.type}{" "}
              <span className="opacity-50">{Math.max(0, Math.ceil((p.endsAt - Date.now()) / 1000))}s</span>
            </div>
          ))}
        </div>
      )}

      {/* Fever border */}
      {feverDisplay && (
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{ border: "4px solid #fbbf24",
            boxShadow: "inset 0 0 50px #fbbf2440, 0 0 50px #fbbf2440",
            animation: "feverPulse 0.6s ease-in-out infinite alternate" }} />
      )}

      {/* Epic flash */}
      {epicFlash && (
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{ background: "#f472b633", animation: "epicFlash 0.4s ease-out forwards" }} />
      )}

      {/* Fever label */}
      {feverDisplay && (
        <div className="absolute left-0 right-0 flex justify-center z-30 pointer-events-none" style={{ top: 110 }}>
          <span className="font-black text-lg px-4 py-1 rounded-full"
            style={{ color: "#fbbf24", textShadow: "0 0 20px #fbbf24",
              background: "#fbbf2420", animation: "feverPulse 0.5s infinite alternate" }}>
            🌡 FEVER MODE!
          </span>
        </div>
      )}

      {/* Targets */}
      {targetsDisplay.map(t => {
        const ageMs = performance.now() - t.born;
        const spawnProg = Math.min(1, ageMs / 150);
        const scale = spawnProg < 1 ? 0.05 + spawnProg * 1.08 : 1;
        const timeLeft = Math.max(0, 1 - (Date.now() - t.spawnedAt) / t.lifetime);
        return (
          <div key={t.id} className="absolute pointer-events-none"
            style={{ left: t.x - t.radius, top: t.y - t.radius,
              transform: `scale(${scale})`, transformOrigin: "center" }}>
            <TargetShape type={t.type} rarity={t.rarity} radius={t.radius}
              color={t.color} glow={t.glow} bombPulse={bombPulseRef.current} />
            {t.type !== "bomb" && (
              <svg className="absolute inset-0 pointer-events-none" width={t.radius * 2} height={t.radius * 2}
                style={{ transform: "rotate(-90deg)" }}>
                <circle cx={t.radius} cy={t.radius} r={t.radius - 4} fill="none"
                  stroke={t.color} strokeWidth={2.5} strokeOpacity={0.4}
                  strokeDasharray={2 * Math.PI * (t.radius - 4)}
                  strokeDashoffset={2 * Math.PI * (t.radius - 4) * (1 - timeLeft)} />
              </svg>
            )}
          </div>
        );
      })}

      {/* Particles */}
      {particlesDisp.map(p => (
        <div key={p.id} className="absolute pointer-events-none rounded-full"
          style={{ left: p.x - p.size / 2, top: p.y - p.size / 2,
            width: p.size, height: p.size,
            background: p.color, opacity: p.life,
            boxShadow: `0 0 ${p.size * 2}px ${p.color}` }} />
      ))}

      {/* Score popups */}
      {popupsDisp.map(p => {
        const age = performance.now() - p.born;
        return (
          <div key={p.id} className="absolute pointer-events-none font-black text-sm select-none"
            style={{ left: p.x, top: p.y - age * 0.06,
              transform: "translateX(-50%)",
              color: p.color, opacity: Math.max(0, 1 - age / 900),
              textShadow: `0 0 10px ${p.color}`, letterSpacing: "0.1em" }}>
            {p.text}
          </div>
        );
      })}
    </div>
  );

  const renderGameOver = () => {
    if (!gameOverData) return null;
    const { score, isNewHigh, grade, xpEarned, soClose, bestStreak, sessionStats } = gameOverData;
    const gradeColor = { S: "#fbbf24", A: "#34d399", B: "#60a5fa", C: "#a78bfa", D: "#6b7280" }[grade] || "#fff";
    return (
      <div className="flex flex-col items-center justify-start h-full overflow-y-auto px-6 py-8 gap-5 relative z-10">
        {/* Grade */}
        <div className="text-center">
          <div className="text-7xl font-black mb-1"
            style={{ color: gradeColor, textShadow: `0 0 40px ${gradeColor}`,
              animation: "gradeReveal 0.6s ease-out" }}>
            {grade}
          </div>
          {isNewHigh && <div className="text-yellow-400 font-bold text-sm animate-bounce">🎉 NEW HIGH SCORE!</div>}
        </div>

        <div className="text-4xl font-black" style={{ color: theme.accent }}>
          {score.toLocaleString()}
        </div>

        {soClose && (
          <div className="text-sm font-bold px-4 py-2 rounded-xl text-center"
            style={{ color: "#f97316", background: "#f9731618", border: "1px solid #f9731644" }}>
            SO CLOSE! Only {soClose} away from your best!
          </div>
        )}

        {/* Stats grid */}
        <div className="w-full rounded-2xl p-4 grid grid-cols-2 gap-3"
          style={{ background: "#ffffff08", border: `1px solid ${theme.accent}33` }}>
          {[
            ["Targets Hit",  sessionStats.tapsTotal],
            ["Rare / Epic",  sessionStats.rareHits],
            ["Best Streak",  bestStreak + "×"],
            ["Survived",     sessionStats.timeSurvived + "s"],
            ["XP Earned",    "+" + xpEarned],
            ["Level",        "Lv " + getLevelFromXP(sv.xp)],
          ].map(([label, val]) => (
            <div key={label} className="text-center">
              <div className="text-xs opacity-40 mb-0.5" style={{ color: theme.accent }}>{label}</div>
              <div className="font-bold text-base" style={{ color: theme.accent }}>{val}</div>
            </div>
          ))}
        </div>

        <NeonButton onClick={startGame} className="w-full py-4 text-xl"
          style={{ background: `linear-gradient(135deg, ${theme.secondary}, ${theme.accent})`,
            boxShadow: `0 0 24px ${theme.accent}88` }}>
          ▶ PLAY AGAIN
        </NeonButton>
        <NeonButton onClick={() => setScreen("menu")} className="w-full py-3"
          style={{ background: "#ffffff10", border: `1px solid ${theme.accent}44` }}>
          ← MENU
        </NeonButton>
      </div>
    );
  };

  const renderMissions = () => {
    const missions = getDailyMissions();
    const prog = sv.missionProgress || {};
    return (
      <div className="flex flex-col h-full px-4 py-6 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={() => setScreen("menu")} className="px-3 py-2 text-sm"
            style={{ background: "#ffffff10" }}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{ color: theme.accent }}>Daily Missions</h2>
        </div>
        {missions.map(m => {
          const cur = Math.min(prog[m.id] || 0, m.goal);
          const pct = cur / m.goal * 100;
          const done = cur >= m.goal;
          return (
            <div key={m.id} className="rounded-2xl p-4"
              style={{ background: done ? `${theme.accent}1a` : "#ffffff08",
                border: `1px solid ${done ? theme.accent : "#ffffff1a"}` }}>
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-sm" style={{ color: done ? theme.accent : "#fff" }}>
                  {done ? "✓ " : ""}{m.desc}
                </span>
                <span className="text-xs opacity-50" style={{ color: theme.accent }}>{cur}/{m.goal}</span>
              </div>
              <div className="h-2 rounded-full" style={{ background: "#ffffff1a" }}>
                <div className="h-full rounded-full transition-all"
                  style={{ width: `${pct}%`, background: done ? theme.accent : `${theme.accent}99` }} />
              </div>
            </div>
          );
        })}
        {sv.missionCompleted && (
          <div className="text-center font-bold py-2" style={{ color: "#fbbf24" }}>
            🏆 All missions complete! +200 XP claimed
          </div>
        )}
      </div>
    );
  };

  const renderAchievements = () => (
    <div className="flex flex-col h-full px-4 py-6 gap-4 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={() => setScreen("menu")} className="px-3 py-2 text-sm"
          style={{ background: "#ffffff10" }}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{ color: theme.accent }}>Medals</h2>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {ACHIEVEMENTS.map(a => {
          const unlocked = sv.unlockedAchievements.includes(a.id);
          return (
            <div key={a.id} className="rounded-2xl p-3 text-center"
              style={{ background: unlocked ? `${theme.accent}1a` : "#ffffff06",
                border: `1px solid ${unlocked ? theme.accent + "66" : "#ffffff12"}`,
                opacity: unlocked ? 1 : 0.45 }}>
              <div className="text-2xl mb-1">{a.icon}</div>
              <div className="text-xs font-bold mb-0.5" style={{ color: unlocked ? theme.accent : "#ccc" }}>{a.label}</div>
              <div className="text-xs opacity-50" style={{ color: theme.accent }}>{a.desc}</div>
            </div>
          );
        })}
      </div>
    </div>
  );

  const renderLeaderboard = () => (
    <div className="flex flex-col h-full px-4 py-6 gap-4 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={() => setScreen("menu")} className="px-3 py-2 text-sm"
          style={{ background: "#ffffff10" }}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{ color: theme.accent }}>Leaderboard</h2>
      </div>
      {sv.scores.length === 0
        ? <p className="text-center opacity-40 mt-8" style={{ color: theme.accent }}>No scores yet. Play a game!</p>
        : sv.scores.map((s, i) => (
          <div key={i} className="flex items-center justify-between px-4 py-3 rounded-2xl"
            style={{ background: i === 0 ? `${theme.accent}1a` : "#ffffff06",
              border: `1px solid ${i === 0 ? theme.accent + "66" : "#ffffff12"}` }}>
            <span className="font-black text-xl" style={{ color: i === 0 ? "#fbbf24" : i === 1 ? "#d1d5db" : i === 2 ? "#d97706" : theme.accent }}>
              {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
            </span>
            <span className="font-bold text-xl" style={{ color: theme.accent }}>{s.toLocaleString()}</span>
          </div>
        ))
      }
    </div>
  );

  const renderSettings = () => (
    <div className="flex flex-col h-full px-4 py-6 gap-5 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={() => setScreen("menu")} className="px-3 py-2 text-sm"
          style={{ background: "#ffffff10" }}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{ color: theme.accent }}>Settings</h2>
      </div>

      {/* Sound */}
      <div>
        <p className="text-xs font-bold opacity-50 mb-2 uppercase" style={{ color: theme.accent }}>Sound</p>
        <NeonButton onClick={() => {
          const next = !soundOn;
          setSoundOn(next);
          saveRef.current.soundEnabled = next;
          debouncedSave();
        }} className="px-6 py-3"
          style={{ background: soundOn ? `${theme.accent}25` : "#ffffff0a",
            border: `1px solid ${soundOn ? theme.accent : "#ffffff22"}`,
            color: soundOn ? theme.accent : "#888" }}>
          {soundOn ? "🔊 Sound ON" : "🔇 Sound OFF"}
        </NeonButton>
      </div>

      {/* Themes */}
      <div>
        <p className="text-xs font-bold opacity-50 mb-2 uppercase" style={{ color: theme.accent }}>Theme</p>
        <div className="flex flex-col gap-2">
          {THEMES.map(t => {
            const locked = lvl < t.unlockLevel;
            return (
              <NeonButton key={t.id} disabled={locked}
                onClick={() => { setTheme(t); saveRef.current.themeId = t.id; debouncedSave(); }}
                className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{ background: theme.id === t.id ? `${t.accent}20` : "#ffffff06",
                  border: `1px solid ${theme.id === t.id ? t.accent : "#ffffff12"}` }}>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 rounded-full" style={{ background: t.accent }} />
                  <span style={{ color: locked ? "#444" : t.accent }}>{t.name}</span>
                </div>
                {locked
                  ? <span className="text-xs opacity-40">Lv {t.unlockLevel}</span>
                  : theme.id === t.id && <span style={{ color: t.accent }}>✓</span>}
              </NeonButton>
            );
          })}
        </div>
      </div>

      {/* Reset */}
      <div className="border-t border-white border-opacity-10 pt-4">
        <NeonButton onClick={() => {
          if (window.confirm("Reset ALL progress? This cannot be undone.")) {
            saveRef.current = { ...DEFAULT_SAVE };
            flushSave();
            setTheme(THEMES[0]);
            setSoundOn(true);
            setScreen("menu");
          }
        }} className="w-full py-3 text-sm"
          style={{ background: "#ef444418", border: "1px solid #ef444455", color: "#ef4444" }}>
          Reset All Progress
        </NeonButton>
      </div>
    </div>
  );

  // ════════════════════════════════════════════
  // MAIN RENDER
  // ════════════════════════════════════════════
  return (
    <div className="relative w-full h-screen overflow-hidden select-none"
      style={{
        background: theme.bg,
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        transform: screenShake ? `translate(${Math.random() > 0.5 ? 4 : -4}px, ${Math.random() > 0.5 ? 3 : -3}px)` : "none",
        transition: screenShake ? "none" : "transform 0.05s ease",
      }}>

      <style>{`
        @keyframes feverPulse {
          from { opacity: 0.65; }
          to   { opacity: 1;    }
        }
        @keyframes epicFlash {
          from { opacity: 1; }
          to   { opacity: 0; }
        }
        @keyframes gradeReveal {
          0%   { transform: scale(0) rotate(-20deg); opacity: 0; }
          60%  { transform: scale(1.25) rotate(6deg); opacity: 1; }
          100% { transform: scale(1) rotate(0deg); }
        }
        * {
          -webkit-tap-highlight-color: transparent;
          box-sizing: border-box;
        }
      `}</style>

      {/* Canvas background */}
      <canvas ref={canvasRef} className="absolute inset-0 pointer-events-none z-0"
        style={{ width: "100%", height: "100%" }} />

      {/* Notification toast */}
      {notification && (
        <div className="absolute top-4 left-1/2 z-50 px-4 py-2 rounded-xl text-sm font-bold text-center pointer-events-none"
          style={{ transform: "translateX(-50%)", background: "#000000dd",
            border: `1px solid ${theme.accent}`, color: theme.accent,
            boxShadow: `0 0 20px ${theme.accent}44`, maxWidth: "80vw",
            whiteSpace: "nowrap" }}>
          {notification}
        </div>
      )}

      {/* Screen routing */}
      {screen === "menu"         && renderMenu()}
      {screen === "playing"      && renderPlaying()}
      {screen === "gameover"     && renderGameOver()}
      {screen === "missions"     && renderMissions()}
      {screen === "achievements" && renderAchievements()}
      {screen === "leaderboard"  && renderLeaderboard()}
      {screen === "settings"     && renderSettings()}
    </div>
  );
}
