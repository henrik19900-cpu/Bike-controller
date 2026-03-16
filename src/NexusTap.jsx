import React, { useState, useEffect, useRef, useCallback, useReducer } from "react";

// ─────────────────────────────────────────────
// CONSTANTS
// ─────────────────────────────────────────────
const RARITY = {
  COMMON:   { name: "common",   chance: 0.70, color: "#a78bfa", glow: "#7c3aed", mult: 1,  size: 1.0, label: ""        },
  UNCOMMON: { name: "uncommon", chance: 0.25, color: "#34d399", glow: "#059669", mult: 2,  size: 1.2, label: "BONUS x2" },
  RARE:     { name: "rare",     chance: 0.05, color: "#fbbf24", glow: "#d97706", mult: 5,  size: 1.5, label: "RARE x5"  },
};

const THEMES = [
  { id: "neon",   name: "Neon Purple", bg: "#0f0a1e", accent: "#a78bfa", secondary: "#6d28d9", unlockLevel: 1  },
  { id: "cyber",  name: "Cyber Blue",  bg: "#051520", accent: "#22d3ee", secondary: "#0e7490", unlockLevel: 5  },
  { id: "fire",   name: "Fire",        bg: "#1a0a00", accent: "#f97316", secondary: "#b45309", unlockLevel: 10 },
  { id: "matrix", name: "Matrix",      bg: "#001a00", accent: "#4ade80", secondary: "#166534", unlockLevel: 20 },
  { id: "gold",   name: "Gold",        bg: "#1a1400", accent: "#fbbf24", secondary: "#b45309", unlockLevel: 30 },
];

const ACHIEVEMENTS = [
  { id: "first_tap",    label: "First Blood",      desc: "Tap your first target",           icon: "👆" },
  { id: "streak_10",   label: "On Fire",           desc: "Reach a 10-tap streak",           icon: "🔥" },
  { id: "streak_50",   label: "Unstoppable",       desc: "Reach a 50-tap streak",           icon: "⚡" },
  { id: "first_rare",  label: "Lucky",             desc: "Hit your first rare target",      icon: "⭐" },
  { id: "level_5",     label: "Rising",            desc: "Reach level 5",                   icon: "📈" },
  { id: "level_10",    label: "Veteran",           desc: "Reach level 10",                  icon: "🏆" },
  { id: "score_1k",    label: "One Grand",         desc: "Score 1,000 points",              icon: "💎" },
  { id: "score_10k",   label: "Ten K",             desc: "Score 10,000 points",             icon: "👑" },
  { id: "daily_done",  label: "Daily Grind",       desc: "Complete a daily challenge",      icon: "📅" },
  { id: "login_7",     label: "Faithful",          desc: "7-day login streak",              icon: "🗓️" },
  { id: "combo_20",    label: "Combo Master",      desc: "Reach a 20x combo",               icon: "💥" },
];

const XP_PER_LEVEL = (lvl) => Math.floor(100 * Math.pow(1.4, lvl - 1));
const BASE_TARGET_RADIUS = 36;
const MAX_LIVES = 3;
const COMBO_WINDOW_MS = 2000;

// ─────────────────────────────────────────────
// SEEDED RANDOM (for daily challenge)
// ─────────────────────────────────────────────
function seededRng(seed) {
  let s = seed;
  return () => {
    s = (s * 1664525 + 1013904223) & 0xffffffff;
    return (s >>> 0) / 0xffffffff;
  };
}

function getTodaySeed() {
  const d = new Date();
  return d.getFullYear() * 10000 + (d.getMonth() + 1) * 100 + d.getDate();
}

function getTodayString() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

// ─────────────────────────────────────────────
// WEB AUDIO ENGINE
// ─────────────────────────────────────────────
class AudioEngine {
  constructor() {
    this.ctx = null;
    this.enabled = true;
  }
  init() {
    if (this.ctx) return;
    try { this.ctx = new (window.AudioContext || window.webkitAudioContext)(); } catch (_) {}
  }
  _play(freq, type, duration, gain = 0.3, delay = 0) {
    if (!this.enabled || !this.ctx) return;
    try {
      const osc = this.ctx.createOscillator();
      const gainNode = this.ctx.createGain();
      osc.connect(gainNode);
      gainNode.connect(this.ctx.destination);
      osc.type = type;
      osc.frequency.setValueAtTime(freq, this.ctx.currentTime + delay);
      gainNode.gain.setValueAtTime(gain, this.ctx.currentTime + delay);
      gainNode.gain.exponentialRampToValueAtTime(0.001, this.ctx.currentTime + delay + duration);
      osc.start(this.ctx.currentTime + delay);
      osc.stop(this.ctx.currentTime + delay + duration);
    } catch (_) {}
  }
  pop(rarity = "common") {
    this.init();
    const freqs = { common: 520, uncommon: 660, rare: 880 };
    this._play(freqs[rarity] || 520, "sine", 0.12, 0.25);
    if (rarity === "rare") {
      this._play(1100, "sine", 0.2, 0.2, 0.1);
      this._play(1320, "sine", 0.15, 0.15, 0.2);
    }
  }
  streak(count) {
    this.init();
    const base = 300 + Math.min(count * 15, 400);
    this._play(base, "square", 0.08, 0.15);
  }
  miss() {
    this.init();
    this._play(120, "sawtooth", 0.25, 0.35);
    this._play(90, "sawtooth", 0.2, 0.2, 0.1);
  }
  levelUp() {
    this.init();
    [440, 554, 659, 880].forEach((f, i) => this._play(f, "sine", 0.3, 0.3, i * 0.12));
  }
  achievement() {
    this.init();
    [660, 880, 1100, 1320].forEach((f, i) => this._play(f, "triangle", 0.25, 0.3, i * 0.1));
  }
  combo(mult) {
    this.init();
    const freq = 220 * mult;
    this._play(Math.min(freq, 1200), "sine", 0.1, 0.2);
  }
}

const audio = new AudioEngine();

// ─────────────────────────────────────────────
// PARTICLE HELPERS
// ─────────────────────────────────────────────
let _uid = 0;
const uid = () => ++_uid;

function spawnParticles(x, y, color, count = 8) {
  return Array.from({ length: count }, () => ({
    id: uid(),
    x, y,
    vx: (Math.random() - 0.5) * 8,
    vy: (Math.random() - 0.7) * 9,
    life: 1,
    color,
    size: 3 + Math.random() * 5,
  }));
}

function spawnFloatingText(x, y, text, color) {
  return { id: uid(), x, y, text, color, life: 1, vy: -2 };
}

// ─────────────────────────────────────────────
// LOCALSTORAGE HELPERS
// ─────────────────────────────────────────────
const LS_KEY = "nexustap_v2";
function loadSave() {
  try {
    const raw = localStorage.getItem(LS_KEY);
    return raw ? JSON.parse(raw) : null;
  } catch (_) { return null; }
}
function writeSave(data) {
  try { localStorage.setItem(LS_KEY, JSON.stringify(data)); } catch (_) {}
}

function defaultSave() {
  return {
    highScore: 0,
    level: 1,
    xp: 0,
    totalGames: 0,
    loginStreak: 0,
    lastLoginDate: null,
    lastDailyDate: null,
    bestDailyScore: 0,
    achievements: [],
    unlockedThemes: ["neon"],
    selectedTheme: "neon",
    leaderboard: [],
    dailyCalendarDay: 0,
    lastCalendarDate: null,
    loginStreak7Notified: false,
  };
}

// ─────────────────────────────────────────────
// MAIN COMPONENT
// ─────────────────────────────────────────────
export default function NexusTap() {
  // ── Persistent save ──
  const [save, setSave] = useState(() => {
    const s = loadSave();
    return s ? { ...defaultSave(), ...s } : defaultSave();
  });

  // Update save and persist
  const updateSave = useCallback((patch) => {
    setSave((prev) => {
      const next = { ...prev, ...patch };
      writeSave(next);
      return next;
    });
  }, []);

  // ── Theme ──
  const theme = THEMES.find((t) => t.id === save.selectedTheme) || THEMES[0];

  // ── Screen: menu | playing | gameover | achievements | leaderboard | daily | settings ──
  const [screen, setScreen] = useState("menu");
  const [isDailyMode, setIsDailyMode] = useState(false);

  // ── Game state ──
  const [score, setScore] = useState(0);
  const [lives, setLives] = useState(MAX_LIVES);
  const [streak, setStreak] = useState(0);
  const [combo, setCombo] = useState(1);
  const [targets, setTargets] = useState([]);
  const [particles, setParticles] = useState([]);
  const [floatingTexts, setFloatingTexts] = useState([]);
  const [shakeFrame, setShakeFrame] = useState(0);
  const [showLevelUp, setShowLevelUp] = useState(null);
  const [showAchievement, setShowAchievement] = useState(null);
  const [gameOver, setGameOver] = useState(false);
  const [finalScore, setFinalScore] = useState(0);
  const [shareText, setShareText] = useState("");

  // Session-level XP tracking
  const sessionXpRef = useRef(0);
  const scoreRef = useRef(0);
  const livesRef = useRef(MAX_LIVES);
  const streakRef = useRef(0);
  const comboRef = useRef(1);
  const lastTapRef = useRef(0);
  const comboTimerRef = useRef(null);
  const rafRef = useRef(null);
  const targetsRef = useRef([]);
  const spawnTimerRef = useRef(null);
  const difficultyRef = useRef(1);
  const gameActiveRef = useRef(false);
  const saveRef = useRef(save);

  useEffect(() => { saveRef.current = save; }, [save]);

  // ── Daily login streak update ──
  useEffect(() => {
    const today = getTodayString();
    const lastLogin = save.lastLoginDate;
    if (lastLogin === today) return;

    const yesterday = (() => {
      const d = new Date(); d.setDate(d.getDate() - 1);
      return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
    })();

    const newStreak = lastLogin === yesterday ? save.loginStreak + 1 : 1;

    // Daily calendar
    const calendarDay = save.lastCalendarDate === yesterday
      ? Math.min(save.dailyCalendarDay + 1, 7)
      : 1;

    const newAchievements = [...save.achievements];
    if (newStreak >= 7 && !newAchievements.includes("login_7")) {
      newAchievements.push("login_7");
    }

    updateSave({
      loginStreak: newStreak,
      lastLoginDate: today,
      dailyCalendarDay: calendarDay,
      lastCalendarDate: today,
      achievements: newAchievements,
    });
  }, []); // eslint-disable-line

  // ─────────────────────────────────────────────
  // DIFFICULTY
  // ─────────────────────────────────────────────
  function getDifficulty(lvl, roundsPlayed) {
    const base = 1 + (lvl - 1) * 0.15 + roundsPlayed * 0.01;
    return Math.min(base, 5);
  }

  function getSpawnInterval(diff) {
    return Math.max(600, 1800 - diff * 200);
  }

  function getTargetLifetime(diff) {
    return Math.max(1000, 3200 - diff * 300);
  }

  // ─────────────────────────────────────────────
  // RARITY ROLL
  // ─────────────────────────────────────────────
  function rollRarity(rng = Math.random) {
    const r = rng();
    if (r < RARITY.RARE.chance) return RARITY.RARE;
    if (r < RARITY.RARE.chance + RARITY.UNCOMMON.chance) return RARITY.UNCOMMON;
    return RARITY.COMMON;
  }

  // ─────────────────────────────────────────────
  // SPAWN TARGET
  // ─────────────────────────────────────────────
  const roundsPlayedRef = useRef(0);

  function spawnTarget(rng = Math.random) {
    const rarity = rollRarity(rng);
    const diff = difficultyRef.current;
    const lifetime = getTargetLifetime(diff);
    const margin = 60;
    const vw = window.innerWidth;
    const vh = window.innerHeight;
    const r = BASE_TARGET_RADIUS * rarity.size;

    return {
      id: uid(),
      x: margin + rng() * (vw - margin * 2),
      y: 120 + rng() * (vh - 240),
      radius: r,
      rarity,
      value: Math.floor((10 + Math.floor(diff * 5)) * rarity.mult),
      timeLeft: lifetime,
      maxTime: lifetime,
      born: Date.now(),
    };
  }

  // ─────────────────────────────────────────────
  // GAME LOOP
  // ─────────────────────────────────────────────
  const lastFrameRef = useRef(0);

  const gameLoop = useCallback((ts) => {
    if (!gameActiveRef.current) return;
    const dt = Math.min(ts - lastFrameRef.current, 100);
    lastFrameRef.current = ts;

    // Update targets
    let missed = false;
    const nextTargets = targetsRef.current
      .map((t) => ({ ...t, timeLeft: t.timeLeft - dt }))
      .filter((t) => {
        if (t.timeLeft <= 0) {
          missed = true;
          return false;
        }
        return true;
      });

    if (missed) {
      livesRef.current = Math.max(0, livesRef.current - 1);
      setLives(livesRef.current);
      streakRef.current = 0;
      setStreak(0);
      comboRef.current = 1;
      setCombo(1);
      audio.miss();
      setShakeFrame((f) => f + 1);
      if (livesRef.current <= 0) {
        endGame();
        return;
      }
    }

    targetsRef.current = nextTargets;
    setTargets([...nextTargets]);

    // Update particles
    setParticles((prev) =>
      prev
        .map((p) => ({ ...p, x: p.x + p.vx, y: p.y + p.vy, vy: p.vy + 0.35, life: p.life - 0.035 }))
        .filter((p) => p.life > 0)
    );

    // Update floating texts
    setFloatingTexts((prev) =>
      prev
        .map((ft) => ({ ...ft, y: ft.y + ft.vy, life: ft.life - 0.03 }))
        .filter((ft) => ft.life > 0)
    );

    rafRef.current = requestAnimationFrame(gameLoop);
  }, []);

  // ─────────────────────────────────────────────
  // SPAWN LOOP
  // ─────────────────────────────────────────────
  const doSpawn = useCallback((rng = Math.random) => {
    if (!gameActiveRef.current) return;
    const diff = difficultyRef.current;
    // Spawn 1-2 targets depending on difficulty
    const count = diff > 3 ? 2 : 1;
    const newTargets = Array.from({ length: count }, () => spawnTarget(rng));
    targetsRef.current = [...targetsRef.current, ...newTargets];
    setTargets([...targetsRef.current]);
    roundsPlayedRef.current += 1;
    difficultyRef.current = getDifficulty(saveRef.current.level, roundsPlayedRef.current);

    spawnTimerRef.current = setTimeout(() => doSpawn(rng), getSpawnInterval(diff));
  }, []);

  // ─────────────────────────────────────────────
  // CHECK ACHIEVEMENTS
  // ─────────────────────────────────────────────
  function checkAchievements(newScore, newStreak, newCombo, newLevel, rarityName, currentAchievements) {
    const earned = [];
    const has = (id) => currentAchievements.includes(id);
    if (!has("first_tap")) earned.push("first_tap");
    if (newStreak >= 10 && !has("streak_10")) earned.push("streak_10");
    if (newStreak >= 50 && !has("streak_50")) earned.push("streak_50");
    if (rarityName === "rare" && !has("first_rare")) earned.push("first_rare");
    if (newLevel >= 5 && !has("level_5")) earned.push("level_5");
    if (newLevel >= 10 && !has("level_10")) earned.push("level_10");
    if (newScore >= 1000 && !has("score_1k")) earned.push("score_1k");
    if (newScore >= 10000 && !has("score_10k")) earned.push("score_10k");
    if (newCombo >= 20 && !has("combo_20")) earned.push("combo_20");
    return earned;
  }

  // ─────────────────────────────────────────────
  // TAP TARGET
  // ─────────────────────────────────────────────
  const handleTap = useCallback((targetId, tx, ty, rarityKey, value) => {
    if (!gameActiveRef.current) return;

    // Remove target
    targetsRef.current = targetsRef.current.filter((t) => t.id !== targetId);

    // Combo
    const now = Date.now();
    if (now - lastTapRef.current < COMBO_WINDOW_MS) {
      comboRef.current = Math.min(comboRef.current + 1, 20);
    } else {
      comboRef.current = 1;
    }
    lastTapRef.current = now;
    setCombo(comboRef.current);

    if (comboTimerRef.current) clearTimeout(comboTimerRef.current);
    comboTimerRef.current = setTimeout(() => {
      comboRef.current = 1;
      setCombo(1);
    }, COMBO_WINDOW_MS);

    audio.pop(rarityKey);
    if (comboRef.current > 1) audio.combo(comboRef.current);

    // Score
    const points = value * comboRef.current;
    scoreRef.current += points;
    setScore(scoreRef.current);

    // Streak
    streakRef.current += 1;
    setStreak(streakRef.current);
    audio.streak(streakRef.current);

    // XP
    const xpGain = Math.floor(points / 5) + 1;
    sessionXpRef.current += xpGain;

    // Level up check
    let curLevel = saveRef.current.level;
    let curXp = saveRef.current.xp + xpGain;
    let leveledUp = false;
    while (curXp >= XP_PER_LEVEL(curLevel)) {
      curXp -= XP_PER_LEVEL(curLevel);
      curLevel += 1;
      leveledUp = true;
    }

    // Unlock themes
    const newUnlocked = [...saveRef.current.unlockedThemes];
    THEMES.forEach((t) => {
      if (curLevel >= t.unlockLevel && !newUnlocked.includes(t.id)) {
        newUnlocked.push(t.id);
      }
    });

    if (leveledUp) {
      audio.levelUp();
      setShowLevelUp(curLevel);
      setTimeout(() => setShowLevelUp(null), 2500);
    }

    // Achievements
    const earned = checkAchievements(
      scoreRef.current,
      streakRef.current,
      comboRef.current,
      curLevel,
      rarityKey,
      saveRef.current.achievements
    );
    const newAchievements = [...saveRef.current.achievements, ...earned];

    if (earned.length > 0) {
      audio.achievement();
      const ach = ACHIEVEMENTS.find((a) => a.id === earned[0]);
      setShowAchievement(ach);
      setTimeout(() => setShowAchievement(null), 3000);
    }

    updateSave({
      level: curLevel,
      xp: curXp,
      unlockedThemes: newUnlocked,
      achievements: newAchievements,
    });

    // Particles & floating text
    const rarityData = Object.values(RARITY).find((r) => r.name === rarityKey) || RARITY.COMMON;
    const pCount = rarityKey === "rare" ? 16 : rarityKey === "uncommon" ? 10 : 6;
    setParticles((prev) => [...prev, ...spawnParticles(tx, ty, rarityData.color, pCount)]);

    const label = comboRef.current > 1 ? `+${points} x${comboRef.current}` : `+${points}`;
    setFloatingTexts((prev) => [...prev, spawnFloatingText(tx, ty - 20, label, rarityData.color)]);
  }, [updateSave]);

  // ─────────────────────────────────────────────
  // END GAME
  // ─────────────────────────────────────────────
  function endGame() {
    gameActiveRef.current = false;
    cancelAnimationFrame(rafRef.current);
    clearTimeout(spawnTimerRef.current);
    clearTimeout(comboTimerRef.current);

    const sc = scoreRef.current;
    const newHigh = Math.max(sc, saveRef.current.highScore);

    // Leaderboard
    const entry = { name: "YOU", score: sc, date: getTodayString() };
    const lb = [entry, ...saveRef.current.leaderboard]
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    // Daily mode
    let dailyPatch = {};
    if (isDailyMode) {
      const newBest = Math.max(sc, saveRef.current.bestDailyScore);
      const newAch = [...saveRef.current.achievements];
      if (!newAch.includes("daily_done")) newAch.push("daily_done");
      dailyPatch = {
        lastDailyDate: getTodayString(),
        bestDailyScore: newBest,
        achievements: newAch,
      };
    }

    updateSave({
      highScore: newHigh,
      totalGames: saveRef.current.totalGames + 1,
      leaderboard: lb,
      ...dailyPatch,
    });

    // Share text
    const streakEmojis = Array.from({ length: Math.min(streakRef.current, 9) }, (_, i) =>
      i < 3 ? "🟩" : i < 6 ? "🟨" : "⬜"
    ).join("");
    setShareText(`NEXUS TAP\nScore: ${sc.toLocaleString()}\nStreak: ${streakRef.current} ${streakEmojis}\nPlay now!`);

    setFinalScore(sc);
    setGameOver(true);
    setScreen("gameover");
  }

  // ─────────────────────────────────────────────
  // START GAME
  // ─────────────────────────────────────────────
  function startGame(daily = false) {
    // Reset state
    scoreRef.current = 0;
    livesRef.current = MAX_LIVES;
    streakRef.current = 0;
    comboRef.current = 1;
    lastTapRef.current = 0;
    roundsPlayedRef.current = 0;
    sessionXpRef.current = 0;
    difficultyRef.current = getDifficulty(save.level, 0);
    targetsRef.current = [];
    gameActiveRef.current = true;

    setScore(0);
    setLives(MAX_LIVES);
    setStreak(0);
    setCombo(1);
    setTargets([]);
    setParticles([]);
    setFloatingTexts([]);
    setGameOver(false);
    setIsDailyMode(daily);
    setScreen("playing");

    // Start loops
    lastFrameRef.current = performance.now();
    rafRef.current = requestAnimationFrame(gameLoop);

    const rng = daily ? seededRng(getTodaySeed()) : Math.random;
    spawnTimerRef.current = setTimeout(() => doSpawn(rng), 500);
  }

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      cancelAnimationFrame(rafRef.current);
      clearTimeout(spawnTimerRef.current);
      clearTimeout(comboTimerRef.current);
    };
  }, []);

  // ─────────────────────────────────────────────
  // RENDER
  // ─────────────────────────────────────────────
  const xpPercent = Math.min(100, Math.floor((save.xp / XP_PER_LEVEL(save.level)) * 100));

  return (
    <div
      className="fixed inset-0 overflow-hidden select-none touch-none"
      style={{ background: theme.bg, fontFamily: "'Inter', 'Segoe UI', sans-serif" }}
    >
      {screen === "menu"         && <MenuScreen    save={save} theme={theme} updateSave={updateSave} startGame={startGame} setScreen={setScreen} xpPercent={xpPercent} />}
      {screen === "playing"      && <GameScreen    save={save} theme={theme} score={score} lives={lives} streak={streak} combo={combo} targets={targets} particles={particles} floatingTexts={floatingTexts} shakeFrame={shakeFrame} showLevelUp={showLevelUp} showAchievement={showAchievement} xpPercent={xpPercent} handleTap={handleTap} isDailyMode={isDailyMode} />}
      {screen === "gameover"     && <GameOverScreen save={save} theme={theme} finalScore={finalScore} streak={streakRef.current} shareText={shareText} startGame={startGame} setScreen={setScreen} isDailyMode={isDailyMode} />}
      {screen === "achievements" && <AchievementsScreen save={save} theme={theme} setScreen={setScreen} />}
      {screen === "leaderboard"  && <LeaderboardScreen  save={save} theme={theme} setScreen={setScreen} />}
      {screen === "settings"     && <SettingsScreen     save={save} theme={theme} updateSave={updateSave} setScreen={setScreen} />}
    </div>
  );
}

// ─────────────────────────────────────────────
// MENU SCREEN
// ─────────────────────────────────────────────
function MenuScreen({ save, theme, updateSave, startGame, setScreen, xpPercent }) {
  const todayDone = save.lastDailyDate === getTodayString();
  const [pulseKey, setPulseKey] = useState(0);

  useEffect(() => {
    const t = setInterval(() => setPulseKey((k) => k + 1), 2000);
    return () => clearInterval(t);
  }, []);

  return (
    <div className="flex flex-col items-center justify-between h-full py-8 px-4">
      {/* Logo */}
      <div className="flex flex-col items-center mt-4">
        <div
          className="text-6xl font-black tracking-tighter mb-1"
          style={{
            color: theme.accent,
            textShadow: `0 0 30px ${theme.accent}88, 0 0 60px ${theme.accent}44`,
            animation: "pulse 2s infinite",
          }}
        >
          NEXUS
        </div>
        <div className="text-2xl font-bold tracking-[0.4em]" style={{ color: theme.secondary }}>
          TAP
        </div>

        {/* Level + XP */}
        <div className="mt-3 w-48">
          <div className="flex justify-between text-xs mb-1" style={{ color: theme.accent }}>
            <span>LVL {save.level}</span>
            <span>{xpPercent}%</span>
          </div>
          <div className="h-2 rounded-full overflow-hidden" style={{ background: `${theme.accent}22` }}>
            <div
              className="h-full rounded-full transition-all duration-700"
              style={{ width: `${xpPercent}%`, background: theme.accent, boxShadow: `0 0 8px ${theme.accent}` }}
            />
          </div>
        </div>

        {/* High score */}
        <div className="mt-3 text-center">
          <div className="text-xs uppercase tracking-widest" style={{ color: `${theme.accent}88` }}>Best</div>
          <div className="text-3xl font-black" style={{ color: theme.accent }}>
            {save.highScore.toLocaleString()}
          </div>
        </div>
      </div>

      {/* Buttons */}
      <div className="flex flex-col gap-3 w-full max-w-xs">
        <NeonButton color={theme.accent} onClick={() => startGame(false)} large>
          PLAY
        </NeonButton>

        <NeonButton
          color={todayDone ? `${theme.accent}55` : "#fbbf24"}
          onClick={() => !todayDone && startGame(true)}
          disabled={todayDone}
        >
          {todayDone ? "✓ DAILY DONE" : "⭐ DAILY CHALLENGE"}
        </NeonButton>

        {/* Login streak calendar */}
        <DailyCalendar save={save} theme={theme} />

        <div className="flex gap-2">
          <NeonButton color={theme.secondary} onClick={() => setScreen("leaderboard")} small>
            🏆 SCORES
          </NeonButton>
          <NeonButton color={theme.secondary} onClick={() => setScreen("achievements")} small>
            🎖️ ACHEIVS
          </NeonButton>
          <NeonButton color={theme.secondary} onClick={() => setScreen("settings")} small>
            ⚙️ SET
          </NeonButton>
        </div>
      </div>

      {/* Login streak */}
      <div className="text-xs" style={{ color: `${theme.accent}66` }}>
        Login streak: {save.loginStreak} day{save.loginStreak !== 1 ? "s" : ""} 🔥
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// DAILY CALENDAR
// ─────────────────────────────────────────────
function DailyCalendar({ save, theme }) {
  const rewards = ["50", "100", "200", "300", "500", "750", "1K XP"];
  return (
    <div className="rounded-xl p-3" style={{ background: `${theme.accent}11`, border: `1px solid ${theme.accent}33` }}>
      <div className="text-xs text-center mb-2 font-semibold" style={{ color: theme.accent }}>
        DAILY REWARDS — DAY {save.dailyCalendarDay || 1} / 7
      </div>
      <div className="flex gap-1 justify-between">
        {rewards.map((r, i) => {
          const done = i < (save.dailyCalendarDay || 0);
          const active = i === (save.dailyCalendarDay || 0);
          return (
            <div
              key={i}
              className="flex flex-col items-center rounded-lg py-1 px-1 flex-1"
              style={{
                background: done ? `${theme.accent}33` : active ? `${theme.accent}22` : "transparent",
                border: active ? `1px solid ${theme.accent}` : "1px solid transparent",
              }}
            >
              <div className="text-xs" style={{ color: done ? theme.accent : active ? theme.accent : `${theme.accent}44` }}>
                {done ? "✓" : `D${i + 1}`}
              </div>
              <div className="text-xs font-bold" style={{ color: done ? theme.accent : `${theme.accent}55`, fontSize: 9 }}>
                {r}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// GAME SCREEN
// ─────────────────────────────────────────────
function GameScreen({
  save, theme, score, lives, streak, combo, targets, particles, floatingTexts,
  shakeFrame, showLevelUp, showAchievement, xpPercent, handleTap, isDailyMode,
}) {
  const shakeStyle = shakeFrame % 2 === 1
    ? { animation: "shake 0.3s ease-out" }
    : {};

  return (
    <div className="relative w-full h-full" style={shakeStyle}>
      {/* HUD */}
      <div className="absolute top-0 left-0 right-0 z-20 px-4 pt-safe-top pt-3">
        <div className="flex items-start justify-between">
          {/* Score */}
          <div>
            <div className="text-xs uppercase tracking-widest" style={{ color: `${theme.accent}88` }}>
              {isDailyMode ? "⭐ DAILY" : "SCORE"}
            </div>
            <div
              className="text-4xl font-black leading-none"
              style={{ color: theme.accent, textShadow: `0 0 20px ${theme.accent}66` }}
            >
              {score.toLocaleString()}
            </div>
          </div>

          {/* Streak + Lives */}
          <div className="flex flex-col items-end gap-1">
            <div className="flex gap-1">
              {Array.from({ length: MAX_LIVES }).map((_, i) => (
                <span key={i} style={{ fontSize: 18, opacity: i < lives ? 1 : 0.2 }}>❤️</span>
              ))}
            </div>
            {streak > 0 && (
              <div
                className="flex items-center gap-1 rounded-full px-3 py-1"
                style={{
                  background: `${theme.accent}22`,
                  border: `1px solid ${theme.accent}55`,
                  color: theme.accent,
                  boxShadow: streak > 10 ? `0 0 12px ${theme.accent}66` : "none",
                }}
              >
                <span className="text-sm font-black">{streak}</span>
                <span className="text-xs">streak</span>
                {streak >= 10 && <span>🔥</span>}
              </div>
            )}
          </div>
        </div>

        {/* Combo */}
        {combo > 1 && (
          <div className="flex justify-center mt-1">
            <div
              className="text-lg font-black px-4 py-1 rounded-full"
              style={{
                color: "#fbbf24",
                background: "#fbbf2422",
                border: "1px solid #fbbf2466",
                textShadow: "0 0 15px #fbbf24",
                animation: "pop 0.15s ease-out",
              }}
            >
              {combo}x COMBO
            </div>
          </div>
        )}

        {/* XP bar */}
        <div className="mt-2 h-1 rounded-full overflow-hidden" style={{ background: `${theme.accent}22` }}>
          <div
            className="h-full rounded-full transition-all duration-500"
            style={{ width: `${xpPercent}%`, background: theme.accent }}
          />
        </div>
      </div>

      {/* Targets */}
      {targets.map((t) => (
        <Target key={t.id} target={t} theme={theme} onTap={handleTap} />
      ))}

      {/* Particles */}
      <svg className="absolute inset-0 pointer-events-none z-10 w-full h-full">
        {particles.map((p) => (
          <circle
            key={p.id}
            cx={p.x} cy={p.y} r={p.size}
            fill={p.color}
            opacity={p.life}
          />
        ))}
      </svg>

      {/* Floating texts */}
      {floatingTexts.map((ft) => (
        <div
          key={ft.id}
          className="absolute pointer-events-none z-30 font-black text-sm"
          style={{
            left: ft.x, top: ft.y,
            transform: "translateX(-50%)",
            color: ft.color,
            opacity: ft.life,
            textShadow: `0 0 10px ${ft.color}`,
          }}
        >
          {ft.text}
        </div>
      ))}

      {/* Level up */}
      {showLevelUp && (
        <div className="absolute inset-0 flex items-center justify-center z-40 pointer-events-none">
          <div
            className="text-center"
            style={{ animation: "levelUpAnim 2.5s ease-out forwards" }}
          >
            <div className="text-6xl">⚡</div>
            <div className="text-3xl font-black mt-2" style={{ color: theme.accent, textShadow: `0 0 30px ${theme.accent}` }}>
              LEVEL {showLevelUp}!
            </div>
          </div>
        </div>
      )}

      {/* Achievement toast */}
      {showAchievement && (
        <div
          className="absolute left-4 right-4 z-50 rounded-2xl px-4 py-3 flex items-center gap-3"
          style={{
            bottom: 100,
            background: `${theme.bg}ee`,
            border: `2px solid ${theme.accent}`,
            boxShadow: `0 0 30px ${theme.accent}66`,
            animation: "slideUp 0.4s ease-out",
          }}
        >
          <span className="text-3xl">{showAchievement.icon}</span>
          <div>
            <div className="font-black text-sm" style={{ color: theme.accent }}>ACHIEVEMENT UNLOCKED</div>
            <div className="font-bold text-base" style={{ color: "#fff" }}>{showAchievement.label}</div>
            <div className="text-xs" style={{ color: `${theme.accent}aa` }}>{showAchievement.desc}</div>
          </div>
        </div>
      )}

      <GlobalStyles />
    </div>
  );
}

// ─────────────────────────────────────────────
// TARGET COMPONENT
// ─────────────────────────────────────────────
function Target({ target, theme, onTap }) {
  const progress = target.timeLeft / target.maxTime;
  const { rarity } = target;
  const isRare = rarity.name === "rare";
  const isUncommon = rarity.name === "uncommon";

  const handleTouch = (e) => {
    e.preventDefault();
    e.stopPropagation();
    const touch = e.changedTouches[0];
    onTap(target.id, touch.clientX, touch.clientY, rarity.name, target.value);
  };
  const handleClick = (e) => {
    e.stopPropagation();
    onTap(target.id, e.clientX, e.clientY, rarity.name, target.value);
  };

  const r = target.radius;
  const outerR = r;
  const innerR = r * 0.72;
  const timerR = r * 0.85;
  const circum = 2 * Math.PI * timerR;
  const dashOffset = circum * (1 - progress);

  return (
    <div
      className="absolute"
      style={{
        left: target.x - r,
        top: target.y - r,
        width: r * 2,
        height: r * 2,
        cursor: "pointer",
        willChange: "transform",
        animation: isRare ? "rarePulse 0.8s ease-in-out infinite" : isUncommon ? "uncommonPop 0.5s ease-out" : undefined,
      }}
      onTouchStart={handleTouch}
      onClick={handleClick}
    >
      <svg width={r * 2} height={r * 2} style={{ overflow: "visible" }}>
        {/* Glow */}
        <circle
          cx={r} cy={r} r={outerR + 4}
          fill="none"
          stroke={rarity.glow}
          strokeWidth={isRare ? 6 : 3}
          opacity={0.3 + progress * 0.4}
          style={{ filter: `blur(${isRare ? 6 : 3}px)` }}
        />
        {/* Timer ring */}
        <circle
          cx={r} cy={r} r={timerR}
          fill="none"
          stroke={rarity.color}
          strokeWidth={3}
          strokeDasharray={circum}
          strokeDashoffset={dashOffset}
          strokeLinecap="round"
          transform={`rotate(-90 ${r} ${r})`}
          opacity={0.9}
        />
        {/* Main circle */}
        <circle
          cx={r} cy={r} r={innerR}
          fill={`${rarity.color}22`}
          stroke={rarity.color}
          strokeWidth={2}
        />
        {/* Value text */}
        <text
          x={r} y={r + 1}
          textAnchor="middle" dominantBaseline="middle"
          fill={rarity.color}
          fontSize={r * 0.45}
          fontWeight="900"
          fontFamily="Inter, sans-serif"
          style={{ textShadow: `0 0 10px ${rarity.color}` }}
        >
          {isRare ? "★" : isUncommon ? "◆" : "●"}
        </text>
        {/* Value number */}
        <text
          x={r} y={r + r * 0.45}
          textAnchor="middle" dominantBaseline="middle"
          fill={rarity.color}
          fontSize={r * 0.28}
          fontWeight="700"
          fontFamily="Inter, sans-serif"
          opacity={0.85}
        >
          +{target.value}
        </text>
      </svg>
    </div>
  );
}

// ─────────────────────────────────────────────
// GAME OVER SCREEN
// ─────────────────────────────────────────────
function GameOverScreen({ save, theme, finalScore, streak, shareText, startGame, setScreen, isDailyMode }) {
  const isNewHigh = finalScore >= save.highScore;
  const avg = save.leaderboard.length > 0
    ? Math.floor(save.leaderboard.reduce((s, e) => s + e.score, 0) / save.leaderboard.length)
    : 0;
  const [copied, setCopied] = useState(false);

  const handleShare = async () => {
    try {
      if (navigator.share) {
        await navigator.share({ text: shareText });
      } else {
        await navigator.clipboard.writeText(shareText);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      }
    } catch (_) {
      try { await navigator.clipboard.writeText(shareText); setCopied(true); setTimeout(() => setCopied(false), 2000); } catch (_2) {}
    }
  };

  return (
    <div className="flex flex-col items-center justify-between h-full py-10 px-6">
      <div className="flex flex-col items-center gap-4 mt-4">
        {isNewHigh && (
          <div
            className="text-2xl font-black px-6 py-2 rounded-full"
            style={{
              color: "#fbbf24",
              background: "#fbbf2422",
              border: "2px solid #fbbf24",
              textShadow: "0 0 20px #fbbf24",
              animation: "pop 0.3s ease-out",
            }}
          >
            🏆 NEW HIGH SCORE!
          </div>
        )}

        <div className="text-center">
          <div className="text-xs uppercase tracking-widest" style={{ color: `${theme.accent}88` }}>
            {isDailyMode ? "Daily Score" : "Score"}
          </div>
          <div
            className="text-7xl font-black"
            style={{ color: theme.accent, textShadow: `0 0 40px ${theme.accent}88` }}
          >
            {finalScore.toLocaleString()}
          </div>
        </div>

        {/* Stats grid */}
        <div className="grid grid-cols-2 gap-3 w-full max-w-xs">
          <StatCard label="Best Streak" value={streak} icon="🔥" theme={theme} />
          <StatCard label="High Score" value={save.highScore.toLocaleString()} icon="👑" theme={theme} />
          <StatCard label="Your Avg" value={avg.toLocaleString()} icon="📊" theme={theme} />
          <StatCard label="Level" value={save.level} icon="⚡" theme={theme} />
        </div>

        {/* Share button */}
        <button
          className="w-full max-w-xs rounded-2xl py-3 font-black text-sm"
          onClick={handleShare}
          style={{
            background: `${theme.accent}22`,
            border: `1px solid ${theme.accent}66`,
            color: theme.accent,
          }}
        >
          {copied ? "✓ COPIED!" : "📤 SHARE RESULT"}
        </button>

        {/* Share preview */}
        <div
          className="rounded-xl px-4 py-3 text-xs font-mono w-full max-w-xs"
          style={{ background: `${theme.accent}11`, color: `${theme.accent}aa`, border: `1px solid ${theme.accent}22` }}
        >
          {shareText}
        </div>
      </div>

      {/* Buttons */}
      <div className="flex flex-col gap-3 w-full max-w-xs">
        <NeonButton color={theme.accent} onClick={() => startGame(false)} large>
          PLAY AGAIN
        </NeonButton>
        <NeonButton color={theme.secondary} onClick={() => setScreen("menu")}>
          MENU
        </NeonButton>
      </div>
    </div>
  );
}

function StatCard({ label, value, icon, theme }) {
  return (
    <div
      className="rounded-2xl p-3 flex flex-col items-center"
      style={{ background: `${theme.accent}11`, border: `1px solid ${theme.accent}33` }}
    >
      <div className="text-xl">{icon}</div>
      <div className="text-lg font-black" style={{ color: theme.accent }}>{value}</div>
      <div className="text-xs" style={{ color: `${theme.accent}88` }}>{label}</div>
    </div>
  );
}

// ─────────────────────────────────────────────
// ACHIEVEMENTS SCREEN
// ─────────────────────────────────────────────
function AchievementsScreen({ save, theme, setScreen }) {
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-4 py-4" style={{ borderBottom: `1px solid ${theme.accent}22` }}>
        <button onClick={() => setScreen("menu")} style={{ color: theme.accent, fontSize: 24 }}>←</button>
        <h1 className="text-xl font-black" style={{ color: theme.accent }}>ACHIEVEMENTS</h1>
        <span className="text-sm ml-auto" style={{ color: `${theme.accent}88` }}>
          {save.achievements.length}/{ACHIEVEMENTS.length}
        </span>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-3 flex flex-col gap-2">
        {ACHIEVEMENTS.map((a) => {
          const done = save.achievements.includes(a.id);
          return (
            <div
              key={a.id}
              className="rounded-2xl p-4 flex items-center gap-4"
              style={{
                background: done ? `${theme.accent}18` : `${theme.accent}08`,
                border: `1px solid ${done ? theme.accent + "55" : theme.accent + "22"}`,
                opacity: done ? 1 : 0.5,
              }}
            >
              <div className="text-3xl">{done ? a.icon : "🔒"}</div>
              <div>
                <div className="font-black text-sm" style={{ color: done ? theme.accent : `${theme.accent}88` }}>
                  {done ? a.label : "???"}
                </div>
                <div className="text-xs" style={{ color: `${theme.accent}77` }}>
                  {done ? a.desc : "Keep playing to unlock"}
                </div>
              </div>
              {done && <div className="ml-auto text-green-400 text-lg">✓</div>}
            </div>
          );
        })}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// LEADERBOARD SCREEN
// ─────────────────────────────────────────────
function LeaderboardScreen({ save, theme, setScreen }) {
  const lb = save.leaderboard.length > 0 ? save.leaderboard : [{ name: "---", score: 0, date: "---" }];
  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-4 py-4" style={{ borderBottom: `1px solid ${theme.accent}22` }}>
        <button onClick={() => setScreen("menu")} style={{ color: theme.accent, fontSize: 24 }}>←</button>
        <h1 className="text-xl font-black" style={{ color: theme.accent }}>LEADERBOARD</h1>
      </div>
      <div className="flex-1 overflow-y-auto px-4 py-3">
        {lb.map((entry, i) => (
          <div
            key={i}
            className="flex items-center gap-4 rounded-2xl p-4 mb-2"
            style={{
              background: i === 0 ? `${theme.accent}22` : `${theme.accent}0a`,
              border: `1px solid ${i === 0 ? theme.accent + "66" : theme.accent + "22"}`,
            }}
          >
            <div
              className="text-xl font-black w-8 text-center"
              style={{ color: i === 0 ? "#fbbf24" : i === 1 ? "#9ca3af" : i === 2 ? "#b87333" : theme.accent }}
            >
              {i === 0 ? "🥇" : i === 1 ? "🥈" : i === 2 ? "🥉" : `#${i + 1}`}
            </div>
            <div className="flex-1">
              <div className="font-black text-sm" style={{ color: theme.accent }}>{entry.name}</div>
              <div className="text-xs" style={{ color: `${theme.accent}66` }}>{entry.date}</div>
            </div>
            <div className="text-lg font-black" style={{ color: theme.accent }}>
              {entry.score.toLocaleString()}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SETTINGS SCREEN
// ─────────────────────────────────────────────
function SettingsScreen({ save, theme, updateSave, setScreen }) {
  const [soundOn, setSoundOn] = useState(audio.enabled);

  return (
    <div className="flex flex-col h-full">
      <div className="flex items-center gap-3 px-4 py-4" style={{ borderBottom: `1px solid ${theme.accent}22` }}>
        <button onClick={() => setScreen("menu")} style={{ color: theme.accent, fontSize: 24 }}>←</button>
        <h1 className="text-xl font-black" style={{ color: theme.accent }}>SETTINGS</h1>
      </div>

      <div className="flex-1 overflow-y-auto px-4 py-4 flex flex-col gap-4">
        {/* Sound toggle */}
        <div
          className="rounded-2xl p-4 flex items-center justify-between"
          style={{ background: `${theme.accent}11`, border: `1px solid ${theme.accent}33` }}
        >
          <div>
            <div className="font-black text-sm" style={{ color: theme.accent }}>Sound Effects</div>
            <div className="text-xs" style={{ color: `${theme.accent}77` }}>Tap sounds, streak, level up</div>
          </div>
          <button
            className="rounded-full w-12 h-6 relative transition-colors duration-200"
            style={{ background: soundOn ? theme.accent : `${theme.accent}44` }}
            onClick={() => {
              audio.enabled = !audio.enabled;
              setSoundOn(audio.enabled);
            }}
          >
            <div
              className="absolute top-0.5 w-5 h-5 rounded-full bg-white transition-all duration-200"
              style={{ left: soundOn ? "calc(100% - 22px)" : 2 }}
            />
          </button>
        </div>

        {/* Theme selection */}
        <div>
          <div className="text-xs font-black uppercase tracking-widest mb-2" style={{ color: `${theme.accent}88` }}>
            THEMES
          </div>
          {THEMES.map((t) => {
            const unlocked = save.unlockedThemes.includes(t.id);
            const active = save.selectedTheme === t.id;
            return (
              <button
                key={t.id}
                className="w-full rounded-2xl p-4 flex items-center gap-3 mb-2"
                style={{
                  background: active ? `${t.accent}22` : `${t.accent}0a`,
                  border: `1px solid ${active ? t.accent + "88" : t.accent + "22"}`,
                  opacity: unlocked ? 1 : 0.4,
                }}
                onClick={() => unlocked && updateSave({ selectedTheme: t.id })}
                disabled={!unlocked}
              >
                <div className="w-6 h-6 rounded-full" style={{ background: t.accent, boxShadow: `0 0 10px ${t.accent}` }} />
                <div className="flex-1 text-left">
                  <div className="font-black text-sm" style={{ color: t.accent }}>{t.name}</div>
                  {!unlocked && (
                    <div className="text-xs" style={{ color: `${t.accent}77` }}>Unlocks at level {t.unlockLevel}</div>
                  )}
                </div>
                {active && <div style={{ color: t.accent }}>✓</div>}
                {!unlocked && <div className="text-sm">🔒</div>}
              </button>
            );
          })}
        </div>

        {/* Reset */}
        <button
          className="rounded-2xl p-4 text-sm font-bold"
          style={{ background: "#ff444422", border: "1px solid #ff444466", color: "#ff6666" }}
          onClick={() => {
            if (window.confirm("Reset all progress? This cannot be undone.")) {
              const fresh = defaultSave();
              writeSave(fresh);
              window.location.reload();
            }
          }}
        >
          Reset All Progress
        </button>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────
// SHARED UI COMPONENTS
// ─────────────────────────────────────────────
function NeonButton({ children, color, onClick, disabled, large, small }) {
  const [pressing, setPressing] = useState(false);
  return (
    <button
      className={`rounded-2xl font-black transition-all duration-100 flex items-center justify-center ${
        large ? "py-5 text-xl tracking-wider" : small ? "py-2 text-xs flex-1" : "py-4 text-base"
      }`}
      style={{
        background: disabled ? `${color}11` : `${color}22`,
        border: `2px solid ${disabled ? color + "33" : color + "88"}`,
        color: disabled ? `${color}44` : color,
        boxShadow: pressing ? "none" : `0 0 ${large ? 20 : 10}px ${color}44`,
        transform: pressing ? "scale(0.96)" : "scale(1)",
        textShadow: disabled ? "none" : `0 0 10px ${color}88`,
        cursor: disabled ? "not-allowed" : "pointer",
        WebkitTapHighlightColor: "transparent",
      }}
      onTouchStart={() => !disabled && setPressing(true)}
      onTouchEnd={() => { setPressing(false); if (!disabled && onClick) onClick(); }}
      onMouseDown={() => !disabled && setPressing(true)}
      onMouseUp={() => { setPressing(false); if (!disabled && onClick) onClick(); }}
      onMouseLeave={() => setPressing(false)}
    >
      {children}
    </button>
  );
}

// ─────────────────────────────────────────────
// GLOBAL STYLES (injected once)
// ─────────────────────────────────────────────
function GlobalStyles() {
  return (
    <style>{`
      @keyframes shake {
        0%   { transform: translateX(0); }
        20%  { transform: translateX(-8px); }
        40%  { transform: translateX(8px); }
        60%  { transform: translateX(-5px); }
        80%  { transform: translateX(5px); }
        100% { transform: translateX(0); }
      }
      @keyframes pop {
        0%   { transform: scale(0.7); opacity: 0; }
        60%  { transform: scale(1.15); }
        100% { transform: scale(1); opacity: 1; }
      }
      @keyframes pulse {
        0%, 100% { opacity: 1; }
        50%       { opacity: 0.7; }
      }
      @keyframes rarePulse {
        0%, 100% { transform: scale(1);    filter: brightness(1); }
        50%       { transform: scale(1.06); filter: brightness(1.3); }
      }
      @keyframes uncommonPop {
        0%   { transform: scale(0.85); }
        70%  { transform: scale(1.05); }
        100% { transform: scale(1); }
      }
      @keyframes levelUpAnim {
        0%   { opacity: 0; transform: scale(0.5); }
        20%  { opacity: 1; transform: scale(1.2); }
        40%  { transform: scale(1); }
        80%  { opacity: 1; }
        100% { opacity: 0; transform: scale(1.1) translateY(-30px); }
      }
      @keyframes slideUp {
        0%   { opacity: 0; transform: translateY(20px); }
        100% { opacity: 1; transform: translateY(0); }
      }
      * { -webkit-tap-highlight-color: transparent; box-sizing: border-box; }
      body { overscroll-behavior: none; }
    `}</style>
  );
}

// ─────────────────────────────────────────────
// INJECT GLOBAL STYLES AT ROOT LEVEL TOO
// ─────────────────────────────────────────────
if (typeof document !== "undefined" && !document.getElementById("nexustap-styles")) {
  const style = document.createElement("style");
  style.id = "nexustap-styles";
  style.textContent = `
    @keyframes shake { 0%{transform:translateX(0)} 20%{transform:translateX(-8px)} 40%{transform:translateX(8px)} 60%{transform:translateX(-5px)} 80%{transform:translateX(5px)} 100%{transform:translateX(0)} }
    @keyframes pop { 0%{transform:scale(0.7);opacity:0} 60%{transform:scale(1.15)} 100%{transform:scale(1);opacity:1} }
    @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.7} }
    @keyframes rarePulse { 0%,100%{transform:scale(1);filter:brightness(1)} 50%{transform:scale(1.06);filter:brightness(1.3)} }
    @keyframes levelUpAnim { 0%{opacity:0;transform:scale(0.5)} 20%{opacity:1;transform:scale(1.2)} 40%{transform:scale(1)} 80%{opacity:1} 100%{opacity:0;transform:scale(1.1) translateY(-30px)} }
    @keyframes slideUp { 0%{opacity:0;transform:translateY(20px)} 100%{opacity:1;transform:translateY(0)} }
    *{-webkit-tap-highlight-color:transparent;box-sizing:border-box}
    html,body{overscroll-behavior:none;margin:0;padding:0}
  `;
  document.head.appendChild(style);
}
