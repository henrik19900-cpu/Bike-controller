import React, { useState, useEffect, useRef, useCallback } from "react";

// ═══════════════════════════════════════════════════════════════
// CONSTANTS
// ═══════════════════════════════════════════════════════════════
const BASE_R       = 26;
const MAX_LIVES    = 5;
const FEVER_STREAK = 15;
const FEVER_DUR    = 8000;
const WAVE_DUR     = 35000;
const XP_PER_LVL   = 150;

const RARITY = {
  COMMON:    { name:"common",    chance:0.57, color:"#a78bfa", glow:"#7c3aed", mult:1,  size:1.0, label:""             },
  UNCOMMON:  { name:"uncommon",  chance:0.22, color:"#34d399", glow:"#059669", mult:2,  size:1.15,label:"BONUS ×2"     },
  RARE:      { name:"rare",      chance:0.13, color:"#fbbf24", glow:"#d97706", mult:5,  size:1.4, label:"RARE ×5"      },
  EPIC:      { name:"epic",      chance:0.06, color:"#f472b6", glow:"#db2777", mult:15, size:1.8, label:"EPIC ×15"     },
  LEGENDARY: { name:"legendary", chance:0.02, color:"#ff6030", glow:"#ff2000", mult:50, size:2.2, label:"LEGENDARY ×50"},
};

const THEMES = [
  { id:"neon",   name:"Neon Purple",bg:"#0c0718",accent:"#a78bfa",secondary:"#6d28d9",grid:"rgba(167,139,250,0.06)",unlockLevel:1  },
  { id:"cyber",  name:"Cyber Blue", bg:"#020c18",accent:"#22d3ee",secondary:"#0e7490",grid:"rgba(34,211,238,0.05)", unlockLevel:5  },
  { id:"inferno",name:"Inferno",    bg:"#180400",accent:"#ff6030",secondary:"#b45309",grid:"rgba(255,96,48,0.06)", unlockLevel:10 },
  { id:"matrix", name:"Matrix",     bg:"#000e00",accent:"#39ff14",secondary:"#166534",grid:"rgba(57,255,20,0.05)", unlockLevel:20 },
  { id:"abyss",  name:"Deep Abyss", bg:"#00000f",accent:"#6060ff",secondary:"#1a1a9a",grid:"rgba(96,96,255,0.05)",unlockLevel:30 },
  { id:"rose",   name:"Rose Gold",  bg:"#180810",accent:"#ff8fab",secondary:"#9d174d",grid:"rgba(255,143,171,0.05)",unlockLevel:40},
];

const ACHIEVEMENTS = [
  { id:"first_tap",    label:"First Blood",   desc:"Tap your first target",          icon:"👆", xp:10  },
  { id:"streak_10",    label:"On Fire",        desc:"10-tap streak",                  icon:"🔥", xp:20  },
  { id:"streak_25",    label:"Blazing",        desc:"25-tap streak",                  icon:"⚡", xp:40  },
  { id:"streak_50",    label:"Unstoppable",    desc:"50-tap streak",                  icon:"💥", xp:80  },
  { id:"first_rare",   label:"Lucky",          desc:"Hit a rare target",              icon:"⭐", xp:15  },
  { id:"first_epic",   label:"Epic!",          desc:"Hit an epic target",             icon:"💎", xp:30  },
  { id:"legendary",    label:"Legendary",      desc:"Hit a legendary target",         icon:"👑", xp:100 },
  { id:"boss_kill",    label:"Boss Slayer",    desc:"Defeat your first boss",         icon:"🐲", xp:50  },
  { id:"wave_5",       label:"Wave Breaker",   desc:"Reach Wave 5",                   icon:"🌊", xp:40  },
  { id:"score_500",    label:"High Scorer",    desc:"Score 500 in one game",          icon:"💯", xp:20  },
  { id:"score_2000",   label:"Champion",       desc:"Score 2000 in one game",         icon:"🎯", xp:50  },
  { id:"score_5000",   label:"Legend",         desc:"Score 5000 in one game",         icon:"🚀", xp:100 },
  { id:"fever_mode",   label:"Fever!",         desc:"Trigger Fever Mode",             icon:"🌡️",xp:30  },
  { id:"fever_3",      label:"Fever Addict",   desc:"Trigger Fever 3 times",          icon:"🔥", xp:60  },
  { id:"perfect_tap",  label:"Sharpshooter",   desc:"Land a Perfect Tap",             icon:"🎯", xp:15  },
  { id:"five_star",    label:"Perfect Run",    desc:"Get a 5-star rating",            icon:"🌟", xp:75  },
  { id:"powerup_5",    label:"Power Hungry",   desc:"Collect 5 power-ups",            icon:"⚡", xp:25  },
  { id:"missions_all", label:"Daily Champ",    desc:"Complete all daily missions",    icon:"📋", xp:50  },
  { id:"daily_3",      label:"Consistent",     desc:"3-day login streak",             icon:"📅", xp:30  },
  { id:"daily_7",      label:"Dedicated",      desc:"7-day login streak",             icon:"🏅", xp:75  },
  { id:"coins_200",    label:"Collector",      desc:"Earn 200 total coins",           icon:"🪙", xp:20  },
];

const MISSION_TEMPLATES = [
  { id:"tap_30",     desc:"Tap 30 targets",          key:"tapsTotal",        goal:30   },
  { id:"tap_60",     desc:"Tap 60 targets",           key:"tapsTotal",        goal:60   },
  { id:"combo_15",   desc:"Reach a 15× combo",        key:"bestCombo",        goal:15   },
  { id:"combo_25",   desc:"Reach a 25× combo",        key:"bestCombo",        goal:25   },
  { id:"score_500",  desc:"Score 500 points",          key:"score",            goal:500  },
  { id:"score_1500", desc:"Score 1500 points",         key:"score",            goal:1500 },
  { id:"rare_5",     desc:"Hit 5 rare/epic targets",   key:"rareHits",         goal:5    },
  { id:"survive_90", desc:"Survive 90 seconds",        key:"timeSurvived",     goal:90   },
  { id:"fever_2",    desc:"Trigger Fever 2 times",     key:"feverCount",       goal:2    },
  { id:"powerup_3",  desc:"Collect 3 power-ups",       key:"powerupCollected", goal:3    },
  { id:"wave_3",     desc:"Reach Wave 3",              key:"waveReached",      goal:3    },
  { id:"boss_1",     desc:"Defeat a boss",             key:"bossKills",        goal:1    },
  { id:"perfect_5",  desc:"Get 5 Perfect Taps",        key:"perfectTaps",      goal:5    },
];

const SHOP_ITEMS = [
  { id:"extra_life",   name:"Extra Life",     desc:"Start with 4 lives",          cost:60,  icon:"❤️" },
  { id:"head_start",   name:"Head Start",     desc:"+300 bonus score at start",   cost:80,  icon:"🚀" },
  { id:"shield_start", name:"Shield",         desc:"Begin with an active Shield", cost:100, icon:"🛡" },
  { id:"power_pack",   name:"Power Pack",     desc:"Start with a random power-up",cost:120, icon:"⚡" },
];

const COMBO_LABELS = [
  [50, "GODLIKE!! 🔥"],
  [35, "UNSTOPPABLE! ⚡"],
  [20, "AMAZING! 💥"],
  [10, "GREAT! ⭐"],
  [5,  "NICE!"],
];

const FAKE_SCORES = [9820,7450,5900,4200,3100,2400,1850,1200,800,420];

const DEFAULT_SAVE = {
  highScore:0, xp:0, bestStreak:0, coins:0, totalCoins:0,
  unlockedAchievements:[], themeId:"neon", soundEnabled:true,
  scores:[], lastLoginDate:null, loginStreak:0,
  missionDate:null, missionProgress:{}, missionCompleted:false,
};

// ═══════════════════════════════════════════════════════════════
// AUDIO ENGINE
// ═══════════════════════════════════════════════════════════════
function createAudio() {
  let ctx = null;
  const C = () => { if (!ctx) ctx = new (window.AudioContext||window.webkitAudioContext)(); return ctx; };
  const t = (freq, type, dur, vol=0.28, delay=0) => {
    try {
      const c=C(), o=c.createOscillator(), g=c.createGain();
      o.connect(g); g.connect(c.destination);
      o.type=type; o.frequency.setValueAtTime(freq, c.currentTime+delay);
      g.gain.setValueAtTime(vol, c.currentTime+delay);
      g.gain.exponentialRampToValueAtTime(0.001, c.currentTime+delay+dur);
      o.start(c.currentTime+delay); o.stop(c.currentTime+delay+dur+0.05);
    } catch {}
  };
  const chord = (freqs, type, dur, vol, dt=0.06) => freqs.forEach((f,i)=>t(f,type,dur,vol,i*dt));
  return {
    tap:        ()=>{ t(540,"sine",0.09,0.22); t(810,"sine",0.07,0.1,0.04); },
    miss:       ()=>{ t(180,"sawtooth",0.35,0.22); },
    uncommon:   ()=>{ t(600,"sine",0.12,0.25); t(900,"sine",0.08,0.18,0.06); },
    rare:       ()=>{ chord([660,880,1100],"sine",0.18,0.28,0.07); },
    epic:       ()=>{ chord([440,554,659,880,1108],"sine",0.22,0.28,0.065); },
    legendary:  ()=>{ chord([330,440,550,660,880,1100,1320],"sine",0.3,0.3,0.055); },
    boss:       ()=>{ t(100,"sawtooth",0.5,0.35); t(140,"square",0.3,0.2,0.1); },
    bossHit:    ()=>{ t(200,"sawtooth",0.2,0.3); t(260,"sine",0.15,0.2,0.05); },
    bossKill:   ()=>{ chord([262,330,392,523,659],"sine",0.35,0.32,0.08); },
    bombSpawn:  ()=>{ t(110,"sawtooth",0.4,0.3); t(75,"sawtooth",0.25,0.2,0.12); },
    bombHit:    ()=>{ t(90,"sawtooth",0.55,0.38); t(55,"sawtooth",0.3,0.28,0.18); },
    powerUp:    ()=>{ chord([440,554,659,880],"sine",0.14,0.24,0.055); },
    feverStart: ()=>{ chord([440,554,659,880,1108],"square",0.12,0.2,0.05); },
    feverEnd:   ()=>{ chord([880,659,554,440],"sine",0.14,0.2,0.07); },
    levelUp:    ()=>{ chord([523,659,784,1047,1319],"sine",0.18,0.3,0.08); },
    waveUp:     ()=>{ chord([330,415,523,659],"square",0.2,0.22,0.07); },
    perfect:    ()=>{ chord([880,1108,1320],"sine",0.15,0.28,0.06); },
    countdown:  ()=>{ t(440,"sine",0.15,0.3); },
    go:         ()=>{ chord([523,659,784],"sine",0.2,0.32,0.05); },
    gameOver:   ()=>{ chord([440,370,294,220],"sawtooth",0.25,0.2,0.1); },
    coin:       ()=>{ t(1200,"sine",0.08,0.18); t(1500,"sine",0.06,0.14,0.06); },
  };
}

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════
function getRarity(wave=1) {
  const r = Math.random();
  // Scale rare/epic/legendary up slightly with wave
  const bonus = Math.min(0.12, (wave-1)*0.015);
  let cumul = 0;
  const entries = Object.values(RARITY);
  // Adjust last 3 chances
  const adj = entries.map((v,i) => ({
    ...v, adjChance: i < 2 ? Math.max(0.1, v.chance - (i===0?bonus*0.7:bonus*0.3)) : v.chance + bonus*(i===2?0.5:i===3?0.35:0.15)
  }));
  for (const v of adj) {
    cumul += v.adjChance;
    if (r < cumul) return v;
  }
  return RARITY.COMMON;
}

const getLvl   = xp => Math.floor(xp / XP_PER_LVL) + 1;
const xpToNext = xp => XP_PER_LVL - (xp % XP_PER_LVL);

function seededRng(seed) {
  let s = seed;
  return () => { s = (s * 1664525 + 1013904223) & 0xffffffff; return (s>>>0)/0xffffffff; };
}

function getDailyMissions() {
  const d = new Date();
  const seed = d.getFullYear()*10000 + (d.getMonth()+1)*100 + d.getDate();
  const rng = seededRng(seed);
  return [...MISSION_TEMPLATES].sort(()=>rng()-0.5).slice(0,3);
}

function getTodayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;
}

function loadSave() {
  try { const r=localStorage.getItem("nexustap_v4"); if(r) return {...DEFAULT_SAVE,...JSON.parse(r)}; } catch {}
  return {...DEFAULT_SAVE};
}

function vibrate(p) { try { if(navigator.vibrate) navigator.vibrate(p); } catch {} }

// ═══════════════════════════════════════════════════════════════
// CANVAS DRAWING
// ═══════════════════════════════════════════════════════════════
function drawCircleTarget(ctx, r, color, glow) {
  ctx.shadowColor = glow; ctx.shadowBlur = r * 0.8;
  ctx.strokeStyle = color; ctx.lineWidth = 2.5; ctx.globalAlpha = 0.18;
  ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill();
  ctx.globalAlpha = 1;
  ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.stroke();
  ctx.globalAlpha = 0.5; ctx.beginPath(); ctx.arc(0,0,r*0.6,0,Math.PI*2); ctx.stroke();
  ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.arc(0,0,r*0.25,0,Math.PI*2); ctx.fill();
  ctx.globalAlpha = 1;
}

function drawDiamond(ctx, r, color, glow) {
  ctx.shadowColor = glow; ctx.shadowBlur = r * 1;
  ctx.strokeStyle = color; ctx.lineWidth = 2.5;
  ctx.fillStyle = color + "33";
  ctx.beginPath(); ctx.moveTo(0,-r); ctx.lineTo(r,0); ctx.lineTo(0,r); ctx.lineTo(-r,0); ctx.closePath();
  ctx.fill(); ctx.stroke();
  const ir = r*0.55;
  ctx.globalAlpha = 0.7; ctx.fillStyle = color;
  ctx.beginPath(); ctx.moveTo(0,-ir); ctx.lineTo(ir,0); ctx.lineTo(0,ir); ctx.lineTo(-ir,0); ctx.closePath();
  ctx.fill(); ctx.globalAlpha = 1;
}

function drawStar(ctx, r, pts, color, glow, innerRatio=0.45) {
  ctx.shadowColor = glow; ctx.shadowBlur = r * 1.2;
  ctx.strokeStyle = color; ctx.lineWidth = 2.5; ctx.fillStyle = color + "44";
  ctx.beginPath();
  for (let i=0; i<pts*2; i++) {
    const a = (i*Math.PI/pts) - Math.PI/2;
    const cr = i%2===0 ? r : r*innerRatio;
    i===0 ? ctx.moveTo(Math.cos(a)*cr, Math.sin(a)*cr) : ctx.lineTo(Math.cos(a)*cr, Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke();
  ctx.globalAlpha = 0.8; ctx.fillStyle = color;
  ctx.beginPath(); ctx.arc(0,0,r*0.22,0,Math.PI*2); ctx.fill();
  ctx.globalAlpha = 1;
}

function drawLegendaryBurst(ctx, r, color, glow, ts) {
  const spin = ts * 0.0015;
  ctx.shadowColor = glow; ctx.shadowBlur = r * 2;
  // Outer rotating halo
  ctx.save(); ctx.rotate(spin);
  ctx.strokeStyle = color; ctx.lineWidth = 1.5; ctx.globalAlpha = 0.4;
  ctx.beginPath();
  for (let i=0;i<16;i++) { const a=i*Math.PI/8; ctx.moveTo(Math.cos(a)*(r+5),Math.sin(a)*(r+5)); ctx.lineTo(Math.cos(a)*(r+12),Math.sin(a)*(r+12)); }
  ctx.stroke(); ctx.restore();
  ctx.save(); ctx.rotate(-spin*0.7);
  drawStar(ctx, r, 8, color, glow, 0.42);
  ctx.restore();
  // Bright center
  const grad = ctx.createRadialGradient(0,0,0,0,0,r*0.35);
  grad.addColorStop(0,"#fff"); grad.addColorStop(0.4,color); grad.addColorStop(1,glow);
  ctx.fillStyle = grad; ctx.globalAlpha = 0.9;
  ctx.beginPath(); ctx.arc(0,0,r*0.35,0,Math.PI*2); ctx.fill();
  ctx.globalAlpha = 1;
}

function drawBombTarget(ctx, r, pulse) {
  const p = 0.5 + 0.5*Math.sin(pulse*0.012);
  ctx.shadowColor = "#ef4444"; ctx.shadowBlur = r * (0.8 + p*0.8);
  ctx.fillStyle = "#1a0000"; ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 3;
  ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill(); ctx.stroke();
  // X
  ctx.strokeStyle = "#ef4444"; ctx.lineWidth = 3.5; ctx.lineCap = "round";
  const d = r*0.48;
  ctx.beginPath(); ctx.moveTo(-d,-d); ctx.lineTo(d,d); ctx.moveTo(d,-d); ctx.lineTo(-d,d); ctx.stroke();
  // Spikes
  ctx.globalAlpha = 0.5+p*0.4;
  ctx.strokeStyle = "#ff6666"; ctx.lineWidth = 1.5;
  for (let i=0;i<8;i++) {
    const a = i*Math.PI/4, s=r*1.05, e=r*1.3+p*5;
    ctx.beginPath(); ctx.moveTo(Math.cos(a)*s,Math.sin(a)*s); ctx.lineTo(Math.cos(a)*e,Math.sin(a)*e); ctx.stroke();
  }
  ctx.globalAlpha = 1;
}

function drawPowerupTarget(ctx, r, ptype) {
  ctx.shadowColor = "#60a5fa"; ctx.shadowBlur = r * 1;
  ctx.fillStyle = "#0a1a3a"; ctx.strokeStyle = "#60a5fa"; ctx.lineWidth = 2.5;
  ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill(); ctx.stroke();
  ctx.fillStyle = "#60a5fa"; ctx.strokeStyle = "#60a5fa"; ctx.lineWidth = 2;
  const icons = { SHIELD:"🛡", SLOW:"🐢", DOUBLE:"×2", LIFE:"❤️", FREEZE:"❄️" };
  const label = ptype ? (icons[ptype]||"⚡") : "⚡";
  // Use canvas font for icon
  ctx.font = `bold ${r*0.9}px serif`;
  ctx.textAlign = "center"; ctx.textBaseline = "middle";
  ctx.fillStyle = "#fff"; ctx.globalAlpha = 0.9;
  ctx.fillText(label, 0, 1);
  ctx.globalAlpha = 1;
}

function drawBossTarget(ctx, r, hitsLeft, maxHits, ts) {
  const phase = (maxHits - hitsLeft) / maxHits;
  const colors = ["#ff6030","#f472b6","#ef4444"];
  const c = colors[Math.min(Math.floor(phase*3), 2)];
  const spin = ts * 0.001;
  ctx.shadowColor = c; ctx.shadowBlur = r * 1.5;
  ctx.save(); ctx.rotate(spin);
  drawStar(ctx, r, 6, c, c, 0.55);
  ctx.restore();
  // HP bar
  const bw = r*2.2, bh = 7;
  ctx.fillStyle = "#333"; ctx.fillRect(-bw/2, r+8, bw, bh);
  ctx.fillStyle = phase < 0.5 ? "#34d399" : phase < 0.8 ? "#fbbf24" : "#ef4444";
  ctx.fillRect(-bw/2, r+8, bw*(hitsLeft/maxHits), bh);
  ctx.strokeStyle = "#ffffff44"; ctx.lineWidth = 1;
  ctx.strokeRect(-bw/2, r+8, bw, bh);
}

function drawMoveTrail(ctx, t) {
  if (!t.trail || t.trail.length < 2) return;
  for (let i=1; i<t.trail.length; i++) {
    const a = i/t.trail.length;
    ctx.globalAlpha = a*0.25;
    ctx.strokeStyle = t.color;
    ctx.lineWidth = t.radius * 2 * a * 0.6;
    ctx.lineCap = "round";
    ctx.beginPath();
    ctx.moveTo(t.trail[i-1].x, t.trail[i-1].y);
    ctx.lineTo(t.trail[i].x, t.trail[i].y);
    ctx.stroke();
  }
  ctx.globalAlpha = 1;
}

function drawTarget(ctx, t, ts, bombPulse) {
  const now = Date.now();
  const timeLeft = Math.max(0, 1-(now-t.spawnedAt)/t.lifetime);
  const agePn = performance.now()-t.born;
  let spawnScale = agePn < 220 ? (0.05 + (agePn/220)*1.05) : 1;

  // Ghost flicker
  let alpha = 1;
  if (t.type === "ghost") {
    alpha = 0.35 + 0.65*(0.5+0.5*Math.sin(ts/220));
  }

  // Trail for moving targets
  if (t.moving) drawMoveTrail(ctx, t);

  ctx.save();
  ctx.globalAlpha = alpha;
  ctx.translate(t.x, t.y);
  ctx.scale(spawnScale, spawnScale);

  if      (t.type==="bomb")    drawBombTarget(ctx, t.radius, bombPulse);
  else if (t.type==="powerup") drawPowerupTarget(ctx, t.radius, t.pwrType);
  else if (t.type==="boss")    drawBossTarget(ctx, t.radius, t.hitsLeft, t.maxHits, ts);
  else {
    const r = t.radius, color=t.color, glow=t.glow, name=t.rarity?.name;
    if      (name==="common")    drawCircleTarget(ctx,r,color,glow);
    else if (name==="uncommon")  drawDiamond(ctx,r,color,glow);
    else if (name==="rare")      drawStar(ctx,r,5,color,glow,0.42);
    else if (name==="epic")      drawStar(ctx,r,6,color,glow,0.48);
    else if (name==="legendary") drawLegendaryBurst(ctx,r,color,glow,ts);
  }

  // Timer ring (not on boss — has HP bar)
  if (t.type!=="bomb" && t.type!=="boss") {
    const ringR = t.radius + 6;
    ctx.shadowBlur = 0;
    ctx.strokeStyle = t.color;
    ctx.lineWidth = 2.5;
    ctx.globalAlpha = 0.5;
    ctx.beginPath();
    ctx.arc(0,0,ringR, -Math.PI/2, -Math.PI/2+2*Math.PI*timeLeft);
    ctx.stroke();
  }

  ctx.restore();
}

function drawParticle(ctx, p, now) {
  const age = now - p.born;
  const life = Math.max(0, 1-age/p.duration);
  ctx.save();
  ctx.globalAlpha = life * (p.alpha||1);
  if (p.type === "shockwave") {
    ctx.strokeStyle = p.color;
    ctx.lineWidth = 2*(1-life);
    ctx.shadowColor = p.color; ctx.shadowBlur = 10;
    ctx.beginPath(); ctx.arc(p.x, p.y, p.r*(1-life)*60, 0, Math.PI*2); ctx.stroke();
  } else if (p.type === "spark") {
    ctx.strokeStyle = p.color;
    ctx.lineWidth = p.size * life;
    ctx.lineCap = "round";
    ctx.shadowColor = p.color; ctx.shadowBlur = p.size*2;
    ctx.beginPath();
    ctx.moveTo(p.x - p.vx*3, p.y - p.vy*3);
    ctx.lineTo(p.x, p.y);
    ctx.stroke();
  } else {
    ctx.fillStyle = p.color;
    ctx.shadowColor = p.color; ctx.shadowBlur = p.size*2;
    const s = Math.max(0, p.size * (p.type==="dust" ? life*0.8 : life));
    ctx.beginPath(); ctx.arc(p.x, p.y, s, 0, Math.PI*2); ctx.fill();
  }
  ctx.restore();
}

function drawBackground(ctx, w, h, accent, gridColor, ts, feverActive) {
  ctx.clearRect(0,0,w,h);
  // Animated grid
  const gs = 44;
  const pulse = 0.5+0.5*Math.sin(ts/1400);
  ctx.strokeStyle = gridColor;
  ctx.lineWidth = 0.8;
  for (let x=0; x<w; x+=gs) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
  for (let y=0; y<h; y+=gs) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
  // Accent lines
  ctx.strokeStyle = accent;
  ctx.globalAlpha = (0.08+pulse*0.06) * (feverActive ? 2.5 : 1);
  ctx.lineWidth = 1.2;
  for (let x=0; x<w; x+=gs*5) { ctx.beginPath(); ctx.moveTo(x,0); ctx.lineTo(x,h); ctx.stroke(); }
  for (let y=0; y<h; y+=gs*5) { ctx.beginPath(); ctx.moveTo(0,y); ctx.lineTo(w,y); ctx.stroke(); }
  ctx.globalAlpha = 1;
}

function drawBgParticles(ctx, bgParts, accent, feverActive) {
  bgParts.forEach(p => {
    p.x += p.vx; p.y += p.vy;
    if (p.x<0) p.x=ctx.canvas.width; if (p.x>ctx.canvas.width) p.x=0;
    if (p.y<0) p.y=ctx.canvas.height; if (p.y>ctx.canvas.height) p.y=0;
    ctx.save();
    ctx.globalAlpha = p.alpha * (feverActive ? 1.6 : 1);
    ctx.fillStyle = feverActive ? "#fbbf24" : accent;
    ctx.shadowColor = feverActive ? "#fbbf24" : accent;
    ctx.shadowBlur = p.r*3;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
    ctx.restore();
  });
}

function drawRipples(ctx, ripples) {
  const dead=[];
  ripples.forEach((rp,i) => {
    rp.r+=4; rp.alpha-=0.05;
    if (rp.alpha<=0) { dead.push(i); return; }
    ctx.save();
    ctx.globalAlpha = rp.alpha;
    ctx.strokeStyle = rp.color;
    ctx.lineWidth = 2;
    ctx.shadowColor = rp.color; ctx.shadowBlur = 8;
    ctx.beginPath(); ctx.arc(rp.x,rp.y,rp.r,0,Math.PI*2); ctx.stroke();
    ctx.restore();
  });
  for (let i=dead.length-1;i>=0;i--) ripples.splice(dead[i],1);
}


// ═══════════════════════════════════════════════════════════════
// NEON BUTTON
// ═══════════════════════════════════════════════════════════════
function NeonButton({ children, onClick, style, className="", disabled=false }) {
  const [pressed, setPressed] = useState(false);
  return (
    <button
      disabled={disabled}
      onMouseDown={()=>setPressed(true)} onMouseUp={()=>setPressed(false)} onMouseLeave={()=>setPressed(false)}
      onTouchStart={e=>{e.preventDefault();setPressed(true);}}
      onTouchEnd={e=>{e.preventDefault();setPressed(false);if(!disabled&&onClick)onClick(e);}}
      onClick={e=>{if(!disabled&&onClick)onClick(e);}}
      className={`select-none transition-all duration-75 rounded-2xl font-bold text-white ${className}`}
      style={{ transform:pressed?"scale(0.93)":"scale(1)", opacity:disabled?0.35:1,
        cursor:disabled?"not-allowed":"pointer", userSelect:"none",
        WebkitTapHighlightColor:"transparent", ...style }}
    >{children}</button>
  );
}

// ═══════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════
export default function NexusTap() {
  // ── Persistent ──
  const saveRef      = useRef(loadSave());
  const audioRef     = useRef(null);
  const saveTimerRef = useRef(null);

  // ── UI state ──
  const [screen,       setScreen]      = useState("menu");
  const [theme,        setTheme]       = useState(()=>THEMES.find(t=>t.id===saveRef.current.themeId)||THEMES[0]);
  const [soundOn,      setSoundOn]     = useState(()=>saveRef.current.soundEnabled);
  const [notification, setNotif]       = useState(null);
  const [cartItems,    setCartItems]   = useState([]); // pre-game shop

  // ── HUD display (20fps update) ──
  const [hud, setHud] = useState({ score:0, lives:3, streak:0, wave:1, combo:1, fever:false, coins:0 });
  const hudUpdateRef  = useRef(0);

  // ── Overlay states ──
  const [activePwrDisp,  setActivePwrDisp]  = useState([]);
  const [comboLabel,     setComboLabel]     = useState("");
  const [waveAnnounce,   setWaveAnnounce]   = useState(null);
  const [countdownVal,   setCountdownVal]   = useState(null);
  const [gameOverData,   setGameOverData]   = useState(null);
  const [paused,         setPaused]         = useState(false);
  const [screenShake,    setScreenShake]    = useState(false);
  const [epicFlash,      setEpicFlash]      = useState(false);
  const [feverBorder,    setFeverBorder]    = useState(false);
  const [perfectFlash,   setPerfectFlash]   = useState(false);

  // ── Canvas & game refs ──
  const canvasRef      = useRef(null);
  const gsRef          = useRef(null);
  const targetsRef     = useRef([]);
  const particlesRef   = useRef([]);
  const activePwrRef   = useRef([]);
  const rafRef         = useRef(null);
  const lastTickRef    = useRef(0);
  const spawnTimerRef  = useRef(0);
  const waveTimerRef   = useRef(0);
  const bombPulseRef   = useRef(0);
  const bgPartsRef     = useRef([]);
  const ripplesRef     = useRef([]);
  const missionProgRef = useRef({});
  const pausedRef      = useRef(false);

  // ── Audio ──
  useEffect(()=>{ audioRef.current = createAudio(); },[]);
  const sfx = useCallback((name)=>{ if(soundOn&&audioRef.current?.[name]) audioRef.current[name](); },[soundOn]);

  // ── Save ──
  const flushSave = useCallback(()=>{ try{localStorage.setItem("nexustap_v4",JSON.stringify(saveRef.current));}catch{} },[]);
  const debounceSave = useCallback(()=>{
    if(saveTimerRef.current) clearTimeout(saveTimerRef.current);
    saveTimerRef.current = setTimeout(flushSave, 1800);
  },[flushSave]);

  // ── Notification ──
  useEffect(()=>{ if(!notification) return; const t=setTimeout(()=>setNotif(null),2600); return()=>clearTimeout(t); },[notification]);

  // ── Achievements ──
  const unlock = useCallback((id)=>{
    const sv=saveRef.current;
    if(sv.unlockedAchievements.includes(id)) return;
    sv.unlockedAchievements=[...sv.unlockedAchievements,id];
    const ach=ACHIEVEMENTS.find(a=>a.id===id);
    if(ach){ setNotif(`${ach.icon} ${ach.label}!`); sv.xp+=ach.xp||0; }
    debounceSave();
  },[debounceSave]);

  // ── Daily login + streak ──
  useEffect(()=>{
    const sv=saveRef.current;
    const today=getTodayKey();
    if(sv.lastLoginDate===today) return;
    const yesterday=(d=>{d.setDate(d.getDate()-1);return`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;})(new Date());
    sv.loginStreak = sv.lastLoginDate===yesterday ? (sv.loginStreak||0)+1 : 1;
    sv.lastLoginDate=today;
    sv.xp+=20+Math.min(sv.loginStreak,7)*5;
    setNotif(`Day ${sv.loginStreak} login! +${20+Math.min(sv.loginStreak,7)*5} XP`);
    if(sv.loginStreak>=3) unlock("daily_3");
    if(sv.loginStreak>=7) unlock("daily_7");
    flushSave();
  },[]);// eslint-disable-line

  // ── Missions ──
  const initMissions = useCallback(()=>{
    const sv=saveRef.current, today=getTodayKey();
    if(sv.missionDate!==today){ sv.missionDate=today; sv.missionProgress={}; sv.missionCompleted=false; flushSave(); }
    missionProgRef.current={...sv.missionProgress};
  },[flushSave]);

  const updateMissions = useCallback((stats)=>{
    const missions=getDailyMissions(), prog=missionProgRef.current;
    let changed=false;
    missions.forEach(m=>{
      const cur=prog[m.id]||0, val=stats[m.key]||0;
      if(val>cur){ prog[m.id]=Math.min(val,m.goal); changed=true; }
    });
    if(changed){
      saveRef.current.missionProgress={...prog};
      if(missions.every(m=>(prog[m.id]||0)>=m.goal)&&!saveRef.current.missionCompleted){
        saveRef.current.missionCompleted=true; saveRef.current.xp+=200;
        setNotif("All missions done! +200 XP 🎉"); unlock("missions_all");
      }
      debounceSave();
    }
  },[debounceSave,unlock]);

  // ── Canvas setup ──
  const initBgParts = useCallback(()=>{
    bgPartsRef.current=Array.from({length:50},()=>({
      x:Math.random()*window.innerWidth, y:Math.random()*window.innerHeight,
      vx:(Math.random()-0.5)*0.35, vy:(Math.random()-0.5)*0.35,
      r:Math.random()*2+0.5, alpha:Math.random()*0.35+0.07,
    }));
  },[]);

  useEffect(()=>{
    const resize=()=>{ if(canvasRef.current){ canvasRef.current.width=window.innerWidth; canvasRef.current.height=window.innerHeight; }};
    resize(); window.addEventListener("resize",resize); initBgParts();
    return()=>window.removeEventListener("resize",resize);
  },[initBgParts]);

  // ── Spawn helpers ──
  const spawnParticles = useCallback((x,y,color,count=10,type="dot")=>{
    const now=performance.now();
    for(let i=0;i<count;i++){
      const angle=Math.random()*Math.PI*2, spd=2+Math.random()*7;
      particlesRef.current.push({
        type, x, y, vx:Math.cos(angle)*spd, vy:Math.sin(angle)*spd-(type==="spark"?2:0),
        color, size:Math.random()*5+1.5, born:now, duration:400+Math.random()*350, alpha:1,
      });
    }
    // shockwave
    if(count>=10) particlesRef.current.push({type:"shockwave",x,y,r:1,color,born:now,duration:500,alpha:0.8});
  },[]);

  const spawnPopup = useCallback((x,y,text,color,size=14)=>{
    particlesRef.current.push({
      type:"popup", x, y, vx:0, vy:-1.2, text, color, size,
      born:performance.now(), duration:900, alpha:1,
    });
  },[]);

  const pickPos = useCallback((radius)=>{
    const margin=radius*2+25, w=window.innerWidth, h=window.innerHeight;
    let best=null, bestD=-1;
    for(let i=0;i<6;i++){
      const x=margin+Math.random()*(w-margin*2);
      const y=margin+100+Math.random()*(h-margin*2-100);
      let minD=Infinity;
      targetsRef.current.forEach(t=>{ const d=Math.hypot(t.x-x,t.y-y); if(d<minD)minD=d; });
      if(minD>bestD){ bestD=minD; best={x,y}; }
    }
    return best||{x:margin+Math.random()*(w-margin*2), y:130+Math.random()*(h-280)};
  },[]);

  // ── Power-ups ──
  const activatePowerUp = useCallback((x,y,ptype)=>{
    const gs=gsRef.current; if(!gs) return;
    sfx("powerUp"); vibrate([10,30,10]); unlock("powerup_5");
    gs.sessionStats.powerupCollected=(gs.sessionStats.powerupCollected||0)+1;

    if(ptype==="LIFE"){
      if(gs.lives<MAX_LIVES){ gs.lives++; } spawnPopup(x,y,"+LIFE","#34d399",16);
    } else {
      const dur=ptype==="SLOW"?7000:ptype==="FREEZE"?5000:9000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!==ptype);
      activePwrRef.current.push({type:ptype,endsAt:Date.now()+dur});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,`+${ptype}`,"#60a5fa",15);
      if(ptype==="SHIELD") spawnParticles(x,y,"#60a5fa",8,"spark");
    }
    const cur=missionProgRef.current;
    missionProgRef.current={...cur,powerupCollected:(cur.powerupCollected||0)+1};
  },[sfx,unlock,spawnPopup,spawnParticles]);

  // ── Spawn target ──
  const spawnTarget = useCallback(()=>{
    const gs=gsRef.current; if(!gs||gs.lives<=0) return;
    const wave=gs.wave, score=gs.score;
    const diff=Math.min(12, 1+score/180);
    const bombChance=Math.min(0.2,0.04+diff*0.012);
    const powerChance=0.07;
    const bossChance=wave>=4?0.04:0;
    const movingChance=wave>=2?Math.min(0.45,0.15+(wave-2)*0.08):0;
    const ghostChance=wave>=3?Math.min(0.2,0.06+(wave-3)*0.04):0;

    const r=Math.random();
    let type="normal", rarity=getRarity(wave), color, glow, moving=false, ghost=false;
    let pwrType=null, hitsLeft=1, maxHits=1, vx=0, vy=0;

    if(r<bossChance){
      type="boss"; color="#ff6030"; glow="#ff2000";
      maxHits=3; hitsLeft=3;
    } else if(r<bossChance+bombChance){
      type="bomb"; color="#ef4444"; glow="#dc2626"; sfx("bombSpawn");
    } else if(r<bossChance+bombChance+powerChance){
      type="powerup"; color="#60a5fa"; glow="#3b82f6";
      const pwrTypes=["SHIELD","SLOW","DOUBLE","LIFE","FREEZE"];
      pwrType=pwrTypes[Math.floor(Math.random()*pwrTypes.length)];
    } else {
      color=rarity.color; glow=rarity.glow;
      if(Math.random()<movingChance){ moving=true; const a=Math.random()*Math.PI*2; const spd=0.6+Math.random()*1.2; vx=Math.cos(a)*spd; vy=Math.sin(a)*spd; }
      if(!moving&&Math.random()<ghostChance) ghost=true;
    }

    const baseR = type==="boss"?BASE_R*2.2 : type==="normal"?BASE_R*(rarity?.size||1):BASE_R;
    const pos=pickPos(baseR);

    // lifetime
    let lifetime=Math.max(1200,3200-diff*160);
    if(activePwrRef.current.some(p=>p.type==="SLOW"&&p.endsAt>Date.now())) lifetime*=1.6;
    if(activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>Date.now())){ vx=0; vy=0; }

    targetsRef.current.push({
      id:Math.random().toString(36).slice(2),
      type, rarity:type==="normal"?rarity:null,
      x:pos.x, y:pos.y, radius:baseR, color, glow,
      lifetime, spawnedAt:Date.now(), born:performance.now(),
      moving, ghost, vx, vy, pwrType,
      hitsLeft, maxHits, trail:moving?[]:null,
    });
  },[sfx,pickPos]);

  // ── End game ──
  const endGame = useCallback(()=>{
    const gs=gsRef.current; if(!gs) return;
    if(rafRef.current){ cancelAnimationFrame(rafRef.current); rafRef.current=null; }

    sfx("gameOver");
    const sv=saveRef.current, score=gs.score;
    const isNewHigh=score>sv.highScore;
    if(isNewHigh) sv.highScore=score;
    if(gs.streak>sv.bestStreak) sv.bestStreak=gs.streak;

    const xpEarned=Math.floor(score/8)+gs.sessionStats.rareHits*8+gs.sessionStats.bossKills*25;
    const prevLvl=getLvl(sv.xp);
    sv.xp+=xpEarned;
    if(getLvl(sv.xp)>prevLvl){ sfx("levelUp"); setNotif(`Level Up! Now Level ${getLvl(sv.xp)}! 🎉`); }

    const coinsEarned=Math.floor(score*0.12)+gs.sessionStats.bossKills*15;
    sv.coins=(sv.coins||0)+coinsEarned;
    sv.totalCoins=(sv.totalCoins||0)+coinsEarned;
    if(sv.totalCoins>=200) unlock("coins_200");

    sv.scores=[score,...sv.scores].slice(0,15).sort((a,b)=>b-a);

    const stars=score>=5000?5:score>=2000?4:score>=1000?3:score>=500?2:score>=200?1:1;
    if(stars>=5) unlock("five_star");

    const timeSurvived=Math.floor((Date.now()-gs.startTime)/1000);
    updateMissions({...gs.sessionStats,timeSurvived,score});

    if(score>=500)  unlock("score_500");
    if(score>=2000) unlock("score_2000");
    if(score>=5000) unlock("score_5000");
    if(gs.wave>=5)  unlock("wave_5");

    setGameOverData({ score,isNewHigh,stars,xpEarned,coinsEarned,
      soClose:(!isNewHigh&&sv.highScore>0&&(sv.highScore-score)/sv.highScore<0.12)?sv.highScore-score:null,
      bestStreak:sv.bestStreak, sessionStats:{...gs.sessionStats,timeSurvived}, wave:gs.wave });

    flushSave();
    gsRef.current=null;
    targetsRef.current=[]; particlesRef.current=[]; activePwrRef.current=[];
    setActivePwrDisp([]); setFeverBorder(false); setComboLabel("");
    setPaused(false); pausedRef.current=false;
    setScreen("gameover");
  },[sfx,flushSave,updateMissions,unlock]);

  // ── Game loop ──
  const gameLoop = useCallback((ts)=>{
    const gs=gsRef.current;
    if(!gs||pausedRef.current) return;

    const dt=Math.min(100,ts-lastTickRef.current);
    lastTickRef.current=ts;
    bombPulseRef.current=ts;

    const canvas=canvasRef.current; if(!canvas) return;
    const ctx=canvas.getContext("2d");
    const w=canvas.width, h=canvas.height;
    const fever=gs.feverActive;
    const th=THEMES.find(t=>t.id===(saveRef.current.themeId||"neon"))||THEMES[0];

    // 1. Background
    drawBackground(ctx,w,h,th.accent,th.grid,ts,fever);
    drawBgParticles(ctx,bgPartsRef.current,th.accent,fever);
    drawRipples(ctx,ripplesRef.current);

    // 2. Update + draw particles
    const pnow=performance.now();
    particlesRef.current=particlesRef.current.filter(p=>{
      const age=pnow-p.born;
      if(age>=p.duration) return false;
      if(p.type!=="shockwave"&&p.type!=="popup"){
        p.x+=p.vx*(p.type==="spark"?1:0.92);
        p.y+=p.vy*(p.type==="spark"?1:0.92);
        p.vy+=(p.type==="spark"?0.18:0.1);
      }
      if(p.type==="popup"){
        p.x+=p.vx; p.y+=p.vy;
        const life=1-age/p.duration;
        ctx.save();
        ctx.globalAlpha=life;
        ctx.fillStyle=p.color;
        ctx.shadowColor=p.color; ctx.shadowBlur=10;
        ctx.font=`bold ${p.size||14}px 'Segoe UI',sans-serif`;
        ctx.textAlign="center"; ctx.textBaseline="middle";
        ctx.fillText(p.text,p.x,p.y);
        ctx.restore();
        return true;
      }
      drawParticle(ctx,p,pnow);
      return true;
    });

    // 3. Update + draw targets
    const now=Date.now(); let lostLife=false;
    targetsRef.current=targetsRef.current.filter(t=>{
      // Move
      if(t.moving&&!activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>now)){
        t.x+=t.vx*dt*0.055; t.y+=t.vy*dt*0.055;
        if(t.x<t.radius||t.x>w-t.radius){ t.vx*=-1; t.x=Math.max(t.radius,Math.min(w-t.radius,t.x)); }
        if(t.y<t.radius+90||t.y>h-t.radius){ t.vy*=-1; t.y=Math.max(t.radius+90,Math.min(h-t.radius,t.y)); }
        if(t.trail){ t.trail.push({x:t.x,y:t.y}); if(t.trail.length>10) t.trail.shift(); }
      }
      // Expiry
      if((now-t.spawnedAt)>=t.lifetime){
        if(t.type==="powerup"||t.type==="bomb") return false;
        if(t.type==="boss") return false;
        // missed
        const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
        if(hasShield){
          activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");
          setActivePwrDisp([...activePwrRef.current]);
        } else {
          gs.lives--; sfx("miss"); vibrate(40); lostLife=true;
          gs.streak=0;
        }
        return false;
      }
      drawTarget(ctx,t,ts,bombPulseRef.current);
      return true;
    });

    if(lostLife){
      if(gs.lives<=0){ endGame(); return; }
    }

    // 4. Expire power-ups
    const prevLen=activePwrRef.current.length;
    activePwrRef.current=activePwrRef.current.filter(p=>p.endsAt>now);
    if(activePwrRef.current.length!==prevLen) setActivePwrDisp([...activePwrRef.current]);

    // 5. Fever countdown
    if(gs.feverActive){
      gs.feverTimeLeft-=dt;
      if(gs.feverTimeLeft<=0){ gs.feverActive=false; setFeverBorder(false); sfx("feverEnd"); }
    }

    // 6. Wave timer
    waveTimerRef.current+=dt;
    if(waveTimerRef.current>=WAVE_DUR){
      waveTimerRef.current=0; gs.wave++;
      gs.sessionStats.waveReached=gs.wave;
      setWaveAnnounce(gs.wave);
      sfx("waveUp"); vibrate([20,40,20]);
      setTimeout(()=>setWaveAnnounce(null),2200);
    }

    // 7. Spawn
    spawnTimerRef.current+=dt;
    const diff=Math.min(12,1+gs.score/180);
    const si=Math.max(500,1500-diff*80-(gs.wave-1)*40);
    if(spawnTimerRef.current>=si){ spawnTimerRef.current=0; spawnTarget(); }

    // 8. HUD update (20fps)
    if(ts-hudUpdateRef.current>50){
      hudUpdateRef.current=ts;
      setHud({score:gs.score,lives:gs.lives,streak:gs.streak,wave:gs.wave,fever:gs.feverActive,coins:saveRef.current.coins});
    }

    rafRef.current=requestAnimationFrame(gameLoop);
  },[sfx,spawnTarget,endGame]);

  // ── Tap ──
  const handleTap = useCallback((e)=>{
    e.preventDefault();
    const gs=gsRef.current; if(!gs||gs.lives<=0||pausedRef.current) return;
    const rect=e.currentTarget.getBoundingClientRect();
    const clientX=e.touches?e.touches[0].clientX:e.clientX;
    const clientY=e.touches?e.touches[0].clientY:e.clientY;
    const tx=clientX-rect.left, ty=clientY-rect.top;

    // Hit detection
    let hit=null, hitDist=Infinity;
    for(const t of targetsRef.current){
      if(t.type==="ghost"&&Math.sin(performance.now()/220)>0.2) continue; // not tappable when invisible
      const d=Math.hypot(t.x-tx,t.y-ty);
      if(d<t.radius*1.35&&d<hitDist){ hit=t; hitDist=d; }
    }

    ripplesRef.current.push({x:tx,y:ty,r:12,alpha:0.7,color:hit?(hit.color||"#a78bfa"):"#ffffff44"});
    if(!hit) return;

    // BOMB
    if(hit.type==="bomb"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      sfx("bombHit"); vibrate(50);
      spawnParticles(hit.x,hit.y,"#ef4444",16,"spark");
      const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>Date.now());
      if(hasShield){
        activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");
        setActivePwrDisp([...activePwrRef.current]);
        spawnPopup(hit.x,hit.y,"SHIELD!","#60a5fa",16);
        vibrate([5,20,5]);
      } else {
        gs.lives=Math.max(0,gs.lives-1); gs.streak=0;
        spawnPopup(hit.x,hit.y,"BOOM!","#ef4444",18);
        setScreenShake(true); setTimeout(()=>setScreenShake(false),450);
        vibrate([40,20,40]);
        if(gs.lives<=0){ endGame(); return; }
      }
      return;
    }

    // POWER-UP
    if(hit.type==="powerup"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      activatePowerUp(hit.x,hit.y,hit.pwrType);
      sfx("coin");
      return;
    }

    // BOSS
    if(hit.type==="boss"){
      hit.hitsLeft--;
      sfx("bossHit"); vibrate(20);
      spawnParticles(hit.x,hit.y,hit.color,8,"spark");
      if(hit.hitsLeft<=0){
        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
        sfx("bossKill"); vibrate([30,20,30,20,50]);
        spawnParticles(hit.x,hit.y,hit.color,35,"spark");
        const pts=500*Math.min(10,1+Math.floor(gs.streak/5))*(gs.feverActive?2:1);
        gs.score+=pts; gs.sessionStats.bossKills=(gs.sessionStats.bossKills||0)+1;
        spawnPopup(hit.x,hit.y,`BOSS! +${pts}`,"#ff6030",20);
        unlock("boss_kill");
      }
      return;
    }

    // NORMAL target
    targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
    gs.streak++;
    const combo=Math.min(10,1+Math.floor(gs.streak/5));
    const isDouble=activePwrRef.current.some(p=>p.type==="DOUBLE"&&p.endsAt>Date.now());
    const feverMult=gs.feverActive?2:1;

    // Perfect tap (center hit, 40-60% lifetime remaining)
    const timeLeft=1-(Date.now()-hit.spawnedAt)/hit.lifetime;
    const isPerfect=hitDist<hit.radius*0.35&&timeLeft>0.38&&timeLeft<0.65;
    const perfectMult=isPerfect?1.5:1;

    const pts=Math.round(hit.rarity.mult*combo*feverMult*(isDouble?2:1)*perfectMult);
    gs.score+=pts;
    const coinsGained=Math.max(1,Math.floor(pts*0.08));
    saveRef.current.coins=(saveRef.current.coins||0)+coinsGained;
    saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinsGained;

    gs.sessionStats.tapsTotal++;
    gs.sessionStats.score=gs.score;
    if(hit.rarity.name==="rare"||hit.rarity.name==="epic"||hit.rarity.name==="legendary") gs.sessionStats.rareHits++;
    if(gs.streak>gs.sessionStats.bestCombo) gs.sessionStats.bestCombo=gs.streak;
    if(isPerfect){ gs.sessionStats.perfectTaps=(gs.sessionStats.perfectTaps||0)+1; }

    // SFX + particles
    if(hit.rarity.name==="legendary"){
      sfx("legendary"); vibrate([30,15,30,15,50,15,80]);
      spawnParticles(hit.x,hit.y,hit.color,40,"spark");
      setEpicFlash(true); setTimeout(()=>setEpicFlash(false),600);
      unlock("legendary");
    } else if(hit.rarity.name==="epic"){
      sfx("epic"); vibrate([20,30,20]);
      spawnParticles(hit.x,hit.y,hit.color,28,"spark");
      setEpicFlash(true); setTimeout(()=>setEpicFlash(false),400);
      unlock("first_epic");
    } else if(hit.rarity.name==="rare"){
      sfx("rare"); vibrate([20,20]);
      spawnParticles(hit.x,hit.y,hit.color,16,"dot");
      unlock("first_rare");
    } else if(hit.rarity.name==="uncommon"){
      sfx("uncommon"); vibrate(15);
      spawnParticles(hit.x,hit.y,hit.color,10,"dot");
    } else {
      sfx("tap"); vibrate(8);
      spawnParticles(hit.x,hit.y,hit.color,7,"dot");
    }

    if(isPerfect){
      sfx("perfect"); vibrate([10,10,10]);
      spawnPopup(hit.x,hit.y-20,"✨ PERFECT!","#fbbf24",17);
      setPerfectFlash(true); setTimeout(()=>setPerfectFlash(false),350);
      unlock("perfect_tap");
    } else if(hit.rarity.label){
      spawnPopup(hit.x,hit.y,hit.rarity.label,hit.color,14);
    }

    // Combo label
    const label=COMBO_LABELS.find(([n])=>gs.streak>=n);
    if(label){ setComboLabel(label[1]); clearTimeout(window.__comboLabelTimer); window.__comboLabelTimer=setTimeout(()=>setComboLabel(""),1200); }

    // Achievements
    unlock("first_tap");
    if(gs.streak>=10) unlock("streak_10");
    if(gs.streak>=25) unlock("streak_25");
    if(gs.streak>=50) unlock("streak_50");
    if(gs.score>=500) unlock("score_500");
    if(gs.score>=2000) unlock("score_2000");
    if(gs.score>=5000) unlock("score_5000");

    // Fever
    if(gs.streak>=FEVER_STREAK&&!gs.feverActive){
      gs.feverActive=true; gs.feverTimeLeft=FEVER_DUR;
      setFeverBorder(true); sfx("feverStart"); vibrate([30,20,30,20,60]);
      spawnPopup(hit.x,hit.y-40,"🌡 FEVER!","#fbbf24",20);
      unlock("fever_mode");
      gs.sessionStats.feverCount=(gs.sessionStats.feverCount||0)+1;
      if(gs.sessionStats.feverCount>=3) unlock("fever_3");
    }

    updateMissions({...gs.sessionStats,bestCombo:gs.streak});
    debounceSave();
  },[sfx,spawnParticles,spawnPopup,activatePowerUp,unlock,updateMissions,debounceSave,endGame]);

  // ── Countdown ──
  const runCountdown = useCallback((cb)=>{
    let n=3;
    const tick=()=>{
      setCountdownVal(n); sfx("countdown");
      if(n===0){ setCountdownVal("GO!"); sfx("go"); setTimeout(()=>{ setCountdownVal(null); cb(); },600); return; }
      n--; setTimeout(tick,900);
    };
    tick();
  },[sfx]);

  // ── Start game ──
  const startGame = useCallback((shopCart=[])=>{
    initMissions();
    targetsRef.current=[]; particlesRef.current=[]; activePwrRef.current=[]; ripplesRef.current=[];
    spawnTimerRef.current=0; waveTimerRef.current=0;
    pausedRef.current=false; setPaused(false);

    const extraLife=shopCart.includes("extra_life");
    const headStart=shopCart.includes("head_start");
    const shieldStart=shopCart.includes("shield_start");
    const powerPack=shopCart.includes("power_pack");

    const startLives=extraLife?4:3;
    const startScore=headStart?300:0;

    gsRef.current={
      score:startScore, lives:startLives, streak:0, wave:1,
      feverActive:false, feverTimeLeft:0, startTime:Date.now(),
      sessionStats:{ tapsTotal:0,rareHits:0,bestCombo:0,score:startScore,feverCount:0,powerupCollected:0,bossKills:0,perfectTaps:0,waveReached:1 },
    };

    if(shieldStart) activePwrRef.current=[{type:"SHIELD",endsAt:Date.now()+30000}];
    if(powerPack){
      const types=["SLOW","DOUBLE","SHIELD","FREEZE"];
      const t=types[Math.floor(Math.random()*types.length)];
      if(!activePwrRef.current.find(p=>p.type===t)) activePwrRef.current.push({type:t,endsAt:Date.now()+12000});
    }
    setActivePwrDisp([...activePwrRef.current]);

    setHud({score:startScore,lives:startLives,streak:0,wave:1,fever:false,coins:saveRef.current.coins});
    setGameOverData(null); setEpicFlash(false); setFeverBorder(false);
    setComboLabel(""); setWaveAnnounce(null); setCartItems([]);

    setScreen("playing");
    runCountdown(()=>{
      lastTickRef.current=performance.now();
      rafRef.current=requestAnimationFrame(gameLoop);
    });
  },[initMissions,activatePowerUp,runCountdown,gameLoop]);

  useEffect(()=>()=>{ if(rafRef.current) cancelAnimationFrame(rafRef.current); },[]);

  // Menu canvas loop
  useEffect(()=>{
    if(screen!=="menu") return;
    let raf;
    const loop=(ts)=>{
      const canvas=canvasRef.current; if(!canvas) return;
      const ctx=canvas.getContext("2d");
      const th=THEMES.find(t=>t.id===(saveRef.current.themeId||"neon"))||THEMES[0];
      drawBackground(ctx,canvas.width,canvas.height,th.accent,th.grid,ts,false);
      drawBgParticles(ctx,bgPartsRef.current,th.accent,false);
      drawRipples(ctx,ripplesRef.current);
      raf=requestAnimationFrame(loop);
    };
    raf=requestAnimationFrame(loop);
    return()=>cancelAnimationFrame(raf);
  },[screen]);

  // ── Pause ──
  const togglePause = useCallback(()=>{
    if(!gsRef.current) return;
    const next=!pausedRef.current;
    pausedRef.current=next; setPaused(next);
    if(!next){
      lastTickRef.current=performance.now();
      rafRef.current=requestAnimationFrame(gameLoop);
    }
  },[gameLoop]);

  const sv=saveRef.current;
  const lvl=getLvl(sv.xp);

  // ── Combo color ──
  const streakColor=()=>{
    const s=hud.streak;
    if(s>=35) return["#ff00ff","#ff00ff"];
    if(s>=20) return["#ef4444","#ff6666"];
    if(s>=10) return["#f97316","#fb923c"];
    if(s>=5)  return["#fbbf24","#fde68a"];
    return["#ffffff","#ffffff"];
  };
  const [sc1]=streakColor();

  // ═════════════════════════════════════════════════════════════
  // SCREEN RENDERERS
  // ═════════════════════════════════════════════════════════════

  const renderMenu=()=>(
    <div className="flex flex-col items-center justify-center h-full gap-4 px-5 relative z-10 pb-4">
      {/* Title */}
      <div className="text-center mb-1">
        <h1 className="text-5xl font-black tracking-widest leading-none"
          style={{color:theme.accent,textShadow:`0 0 40px ${theme.accent},0 0 80px ${theme.accent}55`}}>
          NEXUS<span style={{color:"#f472b6",textShadow:"0 0 40px #f472b6"}}>TAP</span>
        </h1>
        <p className="text-xs mt-1 opacity-50 tracking-widest uppercase" style={{color:theme.accent}}>Ultimate Edition</p>
        <div className="mt-3 flex items-center gap-2 justify-center">
          <span className="text-xs font-bold px-2 py-0.5 rounded-full" style={{background:theme.accent+"22",color:theme.accent}}>
            LV {lvl}
          </span>
          <div className="flex-1 w-32 h-1.5 rounded-full" style={{background:"#ffffff18"}}>
            <div className="h-full rounded-full" style={{width:`${(sv.xp%XP_PER_LVL)/XP_PER_LVL*100}%`,background:theme.accent,boxShadow:`0 0 8px ${theme.accent}`}}/>
          </div>
          <span className="text-xs opacity-40" style={{color:theme.accent}}>{xpToNext(sv.xp)} XP</span>
        </div>
      </div>

      {/* Coins */}
      <div className="flex items-center gap-2 px-4 py-2 rounded-xl" style={{background:"#fbbf2415",border:"1px solid #fbbf2440"}}>
        <span className="text-base">🪙</span>
        <span className="font-bold text-base" style={{color:"#fbbf24"}}>{sv.coins||0}</span>
        <span className="text-xs opacity-50 text-white">coins</span>
      </div>

      {/* Play + Shop */}
      <NeonButton onClick={()=>setScreen("shop")} className="w-full py-4 text-2xl"
        style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 30px ${theme.accent}66`}}>
        ▶ PLAY
      </NeonButton>

      <div className="grid grid-cols-2 gap-3 w-full">
        {[
          {label:"🎯 Daily Missions",sc:"missions"},
          {label:"🏆 Leaderboard",   sc:"leaderboard"},
          {label:"🎖 Medals",        sc:"achievements"},
          {label:"⚙ Settings",      sc:"settings"},
        ].map(b=>(
          <NeonButton key={b.sc} onClick={()=>setScreen(b.sc)} className="py-3 text-sm"
            style={{background:"#ffffff0d",border:`1px solid ${theme.accent}33`}}>
            {b.label}
          </NeonButton>
        ))}
      </div>

      {sv.highScore>0&&(
        <div className="flex items-center gap-3 opacity-50">
          <span className="text-xs text-white">Best:</span>
          <span className="text-sm font-bold" style={{color:theme.accent}}>{sv.highScore.toLocaleString()}</span>
          <span className="text-xs text-white">· Day {sv.loginStreak||1} streak</span>
        </div>
      )}
    </div>
  );

  const renderShop=()=>{
    const coins=sv.coins||0;
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm"
              style={{background:"#ffffff10"}}>← Back</NeonButton>
            <h2 className="text-xl font-black" style={{color:theme.accent}}>Pre-Game Shop</h2>
          </div>
          <div className="flex items-center gap-1 px-3 py-1 rounded-full" style={{background:"#fbbf2415"}}>
            <span>🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>{coins}</span>
          </div>
        </div>
        <p className="text-xs opacity-40 -mt-2" style={{color:theme.accent}}>Buy boosts for your next game</p>

        {SHOP_ITEMS.map(item=>{
          const inCart=cartItems.includes(item.id);
          const canBuy=coins>=item.cost||inCart;
          return(
            <div key={item.id} className="rounded-2xl p-4 flex items-center gap-4"
              style={{background:inCart?`${theme.accent}1a`:"#ffffff08",border:`1px solid ${inCart?theme.accent:"#ffffff15"}`}}>
              <span className="text-3xl">{item.icon}</span>
              <div className="flex-1">
                <div className="font-bold" style={{color:inCart?theme.accent:"#fff"}}>{item.name}</div>
                <div className="text-xs opacity-60">{item.desc}</div>
              </div>
              <NeonButton onClick={()=>{
                if(inCart){ setCartItems(c=>c.filter(i=>i!==item.id)); }
                else if(coins>=item.cost){ setCartItems(c=>[...c,item.id]); }
              }} className="px-3 py-2 text-sm"
                style={{background:inCart?`${theme.accent}33`:"#ffffff10",border:`1px solid ${inCart?theme.accent:"#ffffff22"}`,
                  color:inCart?theme.accent:canBuy?"#fff":"#555"}}>
                {inCart?"✓ Added":`🪙 ${item.cost}`}
              </NeonButton>
            </div>
          );
        })}

        <NeonButton onClick={()=>{
          // Deduct coins
          const total=cartItems.reduce((sum,id)=>sum+(SHOP_ITEMS.find(i=>i.id===id)?.cost||0),0);
          if(sv.coins<total){ setNotif("Not enough coins!"); return; }
          sv.coins-=total; flushSave();
          startGame(cartItems);
        }} className="w-full py-4 text-xl mt-2"
          style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 24px ${theme.accent}66`}}>
          {cartItems.length>0?`▶ PLAY (${cartItems.reduce((s,id)=>s+(SHOP_ITEMS.find(i=>i.id===id)?.cost||0),0)}🪙)`:"▶ PLAY FREE"}
        </NeonButton>
      </div>
    );
  };

  const renderPlaying=()=>(
    <div className="absolute inset-0" onTouchStart={handleTap} onClick={handleTap}
      style={{touchAction:"none",zIndex:10}}>

      {/* HUD top bar */}
      <div className="absolute top-0 left-0 right-0 z-20 flex items-stretch"
        style={{background:"rgba(0,0,0,0.6)",backdropFilter:"blur(6px)",borderBottom:`1px solid ${theme.accent}22`}}>
        <div className="flex-1 flex flex-col items-center justify-center py-2">
          <div className="text-xs opacity-40 tracking-widest uppercase" style={{color:theme.accent}}>Score</div>
          <div className="text-2xl font-black tabular-nums" style={{color:theme.accent}}>{hud.score.toLocaleString()}</div>
        </div>
        <div className="flex flex-col items-center justify-center px-2 py-2 gap-1">
          <div className="flex gap-1">
            {Array.from({length:MAX_LIVES},((_,i)=>(
              <span key={i} style={{fontSize:14,opacity:i<hud.lives?1:0.2}}>{i<hud.lives?"❤️":"🖤"}</span>
            )))}
          </div>
          <div className="text-xs font-bold px-2 py-0.5 rounded-full"
            style={{background:theme.accent+"22",color:theme.accent}}>W{hud.wave}</div>
        </div>
        <div className="flex-1 flex flex-col items-center justify-center py-2">
          <div className="text-xs opacity-40 tracking-widest uppercase" style={{color:theme.accent}}>Streak</div>
          <div className="text-2xl font-black tabular-nums"
            style={{color:sc1,textShadow:hud.streak>=5?`0 0 15px ${sc1}`:"none"}}>
            {hud.streak}×
          </div>
        </div>
        {/* Pause */}
        <button onTouchStart={e=>{e.stopPropagation();togglePause();}}
          onClick={e=>{e.stopPropagation();togglePause();}}
          className="flex items-center justify-center px-4"
          style={{color:theme.accent,fontSize:20,background:"transparent",border:"none",WebkitTapHighlightColor:"transparent"}}>
          {paused?"▶":"⏸"}
        </button>
      </div>

      {/* Power-up badges */}
      {activePwrDisp.length>0&&(
        <div className="absolute left-0 right-0 flex justify-center gap-2 z-20" style={{top:76}}>
          {activePwrDisp.map(p=>(
            <div key={p.type} className="px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1"
              style={{background:"#1e3a8acc",border:"1px solid #60a5fa55",color:"#60a5fa"}}>
              {p.type==="SHIELD"?"🛡":p.type==="SLOW"?"🐢":p.type==="DOUBLE"?"×2":p.type==="FREEZE"?"❄️":"❤️"}
              {" "}{p.type}{" "}
              <span className="opacity-50">{Math.max(0,Math.ceil((p.endsAt-Date.now())/1000))}s</span>
            </div>
          ))}
        </div>
      )}

      {/* Fever border */}
      {feverBorder&&(
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{border:"4px solid #fbbf24",boxShadow:"inset 0 0 60px #fbbf2440,0 0 60px #fbbf2440",animation:"feverPulse 0.6s ease-in-out infinite alternate"}}/>
      )}
      {feverBorder&&(
        <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:116}}>
          <span className="font-black text-base px-4 py-1 rounded-full"
            style={{color:"#fbbf24",textShadow:"0 0 20px #fbbf24",background:"#fbbf2420",animation:"feverPulse 0.5s infinite alternate"}}>
            🌡 FEVER MODE!
          </span>
        </div>
      )}

      {/* Epic flash */}
      {epicFlash&&(
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{background:"#f472b633",animation:"epicFlash 0.5s ease-out forwards"}}/>
      )}
      {perfectFlash&&(
        <div className="absolute inset-0 pointer-events-none z-10"
          style={{background:"#fbbf2422",animation:"epicFlash 0.35s ease-out forwards"}}/>
      )}

      {/* Combo announcer */}
      {comboLabel&&(
        <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30"
          style={{top:"40%",transform:"translateY(-50%)"}}>
          <div className="font-black text-2xl px-6 py-2 rounded-2xl"
            style={{color:"#fff",textShadow:`0 0 30px ${theme.accent}`,background:theme.accent+"22",
              border:`2px solid ${theme.accent}`,animation:"comboAnnounce 0.3s ease-out"}}>
            {comboLabel}
          </div>
        </div>
      )}

      {/* Wave announcement */}
      {waveAnnounce&&(
        <div className="absolute inset-0 flex items-center justify-center pointer-events-none z-40">
          <div className="text-center px-8 py-5 rounded-3xl"
            style={{background:"rgba(0,0,0,0.85)",border:`2px solid ${theme.accent}`,boxShadow:`0 0 40px ${theme.accent}55`,animation:"waveIn 0.4s ease-out"}}>
            <div className="text-xs uppercase tracking-widest opacity-60 mb-1" style={{color:theme.accent}}>Incoming</div>
            <div className="text-5xl font-black" style={{color:theme.accent,textShadow:`0 0 30px ${theme.accent}`}}>
              WAVE {waveAnnounce}
            </div>
            {waveAnnounce>=4&&<div className="text-sm opacity-70 mt-1" style={{color:theme.accent}}>Bosses incoming!</div>}
          </div>
        </div>
      )}

      {/* Countdown */}
      {countdownVal!==null&&(
        <div className="absolute inset-0 flex items-center justify-center z-50 pointer-events-none"
          style={{background:"rgba(0,0,0,0.5)"}}>
          <div className="font-black text-8xl" key={countdownVal}
            style={{color:countdownVal==="GO!"?"#34d399":theme.accent,
              textShadow:`0 0 60px ${countdownVal==="GO!"?"#34d399":theme.accent}`,
              animation:"countAnim 0.5s ease-out"}}>
            {countdownVal}
          </div>
        </div>
      )}

      {/* Pause overlay */}
      {paused&&(
        <div className="absolute inset-0 flex flex-col items-center justify-center z-50"
          style={{background:"rgba(0,0,0,0.75)",backdropFilter:"blur(8px)"}}>
          <div className="text-4xl font-black mb-6" style={{color:theme.accent}}>PAUSED</div>
          <NeonButton onClick={togglePause} className="w-48 py-4 text-lg mb-3"
            style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 24px ${theme.accent}66`}}>
            ▶ RESUME
          </NeonButton>
          <NeonButton onClick={()=>{ if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;} gsRef.current=null; targetsRef.current=[]; particlesRef.current=[]; activePwrRef.current=[]; setActivePwrDisp([]); setFeverBorder(false); setPaused(false); pausedRef.current=false; setScreen("menu"); }}
            className="w-48 py-3" style={{background:"#ffffff10",border:`1px solid ${theme.accent}44`}}>
            ✕ QUIT
          </NeonButton>
        </div>
      )}
    </div>
  );

  const renderGameOver=()=>{
    if(!gameOverData) return null;
    const{score,isNewHigh,stars,xpEarned,coinsEarned,soClose,bestStreak,sessionStats,wave}=gameOverData;
    return(
      <div className="flex flex-col items-center h-full overflow-y-auto px-5 py-6 gap-4 relative z-10">
        {/* Stars */}
        <div className="text-center">
          <div className="flex justify-center gap-1 mb-2" style={{animation:"gradeReveal 0.6s ease-out"}}>
            {Array.from({length:5},(_,i)=>(
              <span key={i} className="text-3xl transition-all" style={{opacity:i<stars?1:0.15,filter:i<stars?`drop-shadow(0 0 8px #fbbf24)`:"none",fontSize:i<stars?32:24}}>⭐</span>
            ))}
          </div>
          {isNewHigh&&<div className="text-yellow-400 font-bold text-sm animate-bounce">🎉 NEW HIGH SCORE!</div>}
        </div>

        <div className="text-5xl font-black tabular-nums" style={{color:theme.accent,textShadow:`0 0 30px ${theme.accent}`}}>
          {score.toLocaleString()}
        </div>

        {/* XP + Coins earned */}
        <div className="flex gap-3">
          <div className="px-3 py-1.5 rounded-xl flex items-center gap-2"
            style={{background:"#ffffff0a",border:`1px solid ${theme.accent}33`}}>
            <span className="text-sm">✨</span>
            <span className="font-bold text-sm" style={{color:theme.accent}}>+{xpEarned} XP</span>
          </div>
          <div className="px-3 py-1.5 rounded-xl flex items-center gap-2"
            style={{background:"#fbbf2415",border:"1px solid #fbbf2440"}}>
            <span className="text-sm">🪙</span>
            <span className="font-bold text-sm" style={{color:"#fbbf24"}}>+{coinsEarned}</span>
          </div>
        </div>

        {soClose&&(
          <div className="text-sm font-bold px-4 py-2 rounded-xl text-center"
            style={{color:"#f97316",background:"#f9731618",border:"1px solid #f9731644"}}>
            SO CLOSE! Only {soClose} away from your record!
          </div>
        )}

        <div className="w-full rounded-2xl p-4 grid grid-cols-3 gap-3"
          style={{background:"#ffffff07",border:`1px solid ${theme.accent}28`}}>
          {[
            ["Hits",     sessionStats.tapsTotal],
            ["Rare+",    sessionStats.rareHits],
            ["Streak",   bestStreak+"×"],
            ["Wave",     wave],
            ["Bosses",   sessionStats.bossKills||0],
            ["Perfect",  sessionStats.perfectTaps||0],
            ["Time",     sessionStats.timeSurvived+"s"],
            ["Fevers",   sessionStats.feverCount||0],
            ["Level",    "Lv "+lvl],
          ].map(([label,val])=>(
            <div key={label} className="text-center">
              <div className="text-xs opacity-35 mb-0.5 uppercase tracking-wide" style={{color:theme.accent}}>{label}</div>
              <div className="font-bold text-sm" style={{color:theme.accent}}>{val}</div>
            </div>
          ))}
        </div>

        <NeonButton onClick={()=>setScreen("shop")} className="w-full py-4 text-xl"
          style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 24px ${theme.accent}66`}}>
          ▶ PLAY AGAIN
        </NeonButton>
        <NeonButton onClick={()=>setScreen("menu")} className="w-full py-3"
          style={{background:"#ffffff0d",border:`1px solid ${theme.accent}33`}}>
          ← MENU
        </NeonButton>
      </div>
    );
  };

  const renderMissions=()=>{
    const missions=getDailyMissions(), prog=sv.missionProgress||{};
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Daily Missions</h2>
          {sv.missionCompleted&&<span className="text-xs px-2 py-1 rounded-full font-bold" style={{background:"#34d39922",color:"#34d399"}}>DONE ✓</span>}
        </div>
        <p className="text-xs opacity-40 -mt-2" style={{color:theme.accent}}>Complete all 3 for +200 XP bonus</p>
        {missions.map(m=>{
          const cur=Math.min(prog[m.id]||0,m.goal), pct=cur/m.goal*100, done=cur>=m.goal;
          return(
            <div key={m.id} className="rounded-2xl p-4" style={{background:done?`${theme.accent}18`:"#ffffff07",border:`1px solid ${done?theme.accent+"55":"#ffffff12"}`}}>
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-sm" style={{color:done?theme.accent:"#e2e8f0"}}>{done?"✓ ":""}{m.desc}</span>
                <span className="text-xs opacity-50 tabular-nums" style={{color:theme.accent}}>{cur}/{m.goal}</span>
              </div>
              <div className="h-2.5 rounded-full" style={{background:"#ffffff15"}}>
                <div className="h-full rounded-full transition-all duration-500"
                  style={{width:`${pct}%`,background:done?theme.accent:`${theme.accent}88`,boxShadow:done?`0 0 8px ${theme.accent}`:""}}/>
              </div>
            </div>
          );
        })}
        {sv.missionCompleted&&<div className="text-center font-bold py-2" style={{color:"#fbbf24"}}>🏆 All complete! +200 XP earned</div>}
      </div>
    );
  };

  const renderAchievements=()=>(
    <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{color:theme.accent}}>Medals</h2>
        <span className="text-xs opacity-40" style={{color:theme.accent}}>{sv.unlockedAchievements.length}/{ACHIEVEMENTS.length}</span>
      </div>
      <div className="grid grid-cols-2 gap-3">
        {ACHIEVEMENTS.map(a=>{
          const unlocked=sv.unlockedAchievements.includes(a.id);
          return(
            <div key={a.id} className="rounded-2xl p-3 text-center"
              style={{background:unlocked?`${theme.accent}18`:"#ffffff06",border:`1px solid ${unlocked?theme.accent+"55":"#ffffff10"}`,opacity:unlocked?1:0.4}}>
              <div className="text-2xl mb-1" style={{filter:unlocked?`drop-shadow(0 0 6px ${theme.accent})`:"none"}}>{a.icon}</div>
              <div className="text-xs font-bold mb-0.5" style={{color:unlocked?theme.accent:"#ccc"}}>{a.label}</div>
              <div className="text-xs opacity-50" style={{color:unlocked?theme.accent:"#888"}}>{a.desc}</div>
              {unlocked&&<div className="text-xs opacity-60 mt-1" style={{color:theme.accent}}>+{a.xp} XP</div>}
            </div>
          );
        })}
      </div>
    </div>
  );

  const renderLeaderboard=()=>{
    const allScores=[...sv.scores,...FAKE_SCORES].sort((a,b)=>b-a).slice(0,12);
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Leaderboard</h2>
        </div>
        {allScores.length===0
          ?<p className="text-center opacity-40 mt-8" style={{color:theme.accent}}>No scores yet. Play a game!</p>
          :allScores.map((s,i)=>{
            const isYours=sv.scores.includes(s)&&!FAKE_SCORES.includes(s);
            return(
              <div key={i} className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{background:isYours?`${theme.accent}22`:i===0?`${theme.accent}15`:"#ffffff06",
                  border:`1px solid ${isYours?theme.accent:i<3?theme.accent+"33":"#ffffff10"}`}}>
                <span className="font-black text-xl" style={{color:i===0?"#fbbf24":i===1?"#d1d5db":i===2?"#d97706":theme.accent,minWidth:32}}>
                  {i===0?"🥇":i===1?"🥈":i===2?"🥉":`#${i+1}`}
                </span>
                <span className="font-bold text-xl tabular-nums" style={{color:isYours?theme.accent:"#e2e8f0"}}>{s.toLocaleString()}</span>
                {isYours&&<span className="text-xs px-2 py-0.5 rounded-full font-bold" style={{background:theme.accent+"22",color:theme.accent}}>YOU</span>}
              </div>
            );
          })
        }
      </div>
    );
  };

  const renderSettings=()=>(
    <div className="flex flex-col h-full px-4 py-5 gap-5 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{color:theme.accent}}>Settings</h2>
      </div>

      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Sound</p>
        <NeonButton onClick={()=>{ const n=!soundOn; setSoundOn(n); sv.soundEnabled=n; debounceSave(); }}
          className="px-6 py-3"
          style={{background:soundOn?`${theme.accent}22`:"#ffffff0a",border:`1px solid ${soundOn?theme.accent:"#ffffff22"}`,color:soundOn?theme.accent:"#888"}}>
          {soundOn?"🔊  Sound ON":"🔇  Sound OFF"}
        </NeonButton>
      </div>

      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Theme</p>
        <div className="flex flex-col gap-2">
          {THEMES.map(th=>{
            const locked=lvl<th.unlockLevel;
            return(
              <NeonButton key={th.id} disabled={locked}
                onClick={()=>{ setTheme(th); sv.themeId=th.id; debounceSave(); }}
                className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{background:theme.id===th.id?`${th.accent}20`:"#ffffff06",border:`1px solid ${theme.id===th.id?th.accent:"#ffffff10"}`}}>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 rounded-full" style={{background:th.accent,boxShadow:`0 0 8px ${th.accent}`}}/>
                  <span style={{color:locked?"#444":th.accent}}>{th.name}</span>
                </div>
                {locked?<span className="text-xs opacity-30">Lv {th.unlockLevel}</span>
                  :theme.id===th.id?<span style={{color:th.accent}}>✓</span>:null}
              </NeonButton>
            );
          })}
        </div>
      </div>

      <div className="border-t border-white border-opacity-10 pt-4">
        <NeonButton onClick={()=>{ if(window.confirm("Reset ALL progress? This cannot be undone."))
          { saveRef.current={...DEFAULT_SAVE}; flushSave(); setTheme(THEMES[0]); setSoundOn(true); setScreen("menu"); }
        }} className="w-full py-3 text-sm" style={{background:"#ef444418",border:"1px solid #ef444455",color:"#ef4444"}}>
          Reset All Progress
        </NeonButton>
      </div>
    </div>
  );

  // ═════════════════════════════════════════════════════════════
  // MAIN RENDER
  // ═════════════════════════════════════════════════════════════
  return(
    <div className="relative w-full h-screen overflow-hidden select-none"
      style={{background:theme.bg,fontFamily:"'Segoe UI',system-ui,sans-serif",
        transform:screenShake?`translate(${(Math.random()>0.5?1:-1)*4}px,${(Math.random()>0.5?1:-1)*3}px)`:"none",
        transition:screenShake?"none":"transform 0.04s ease"}}>

      <style>{`
        @keyframes feverPulse{from{opacity:.6}to{opacity:1}}
        @keyframes epicFlash{from{opacity:1}to{opacity:0}}
        @keyframes gradeReveal{0%{transform:scale(0) rotate(-15deg);opacity:0}60%{transform:scale(1.2) rotate(4deg)}100%{transform:scale(1) rotate(0);opacity:1}}
        @keyframes comboAnnounce{0%{transform:scale(0.5);opacity:0}60%{transform:scale(1.15)}100%{transform:scale(1);opacity:1}}
        @keyframes waveIn{0%{transform:scale(0.6) translateY(-20px);opacity:0}70%{transform:scale(1.05) translateY(0)}100%{transform:scale(1);opacity:1}}
        @keyframes countAnim{0%{transform:scale(2);opacity:0}50%{transform:scale(1);opacity:1}100%{transform:scale(0.8);opacity:0}}
        *{-webkit-tap-highlight-color:transparent;box-sizing:border-box}
      `}</style>

      {/* Canvas (always present) */}
      <canvas ref={canvasRef} className="absolute inset-0 z-0"
        style={{width:"100%",height:"100%",pointerEvents:"none"}}/>

      {/* Notification toast */}
      {notification&&(
        <div className="absolute top-4 left-1/2 z-50 px-4 py-2 rounded-xl text-sm font-bold text-center pointer-events-none"
          style={{transform:"translateX(-50%)",background:"#000000ee",border:`1px solid ${theme.accent}`,color:theme.accent,
            boxShadow:`0 0 24px ${theme.accent}44`,maxWidth:"85vw",whiteSpace:"nowrap"}}>
          {notification}
        </div>
      )}

      {screen==="menu"         &&renderMenu()}
      {screen==="shop"         &&renderShop()}
      {screen==="playing"      &&renderPlaying()}
      {screen==="gameover"     &&renderGameOver()}
      {screen==="missions"     &&renderMissions()}
      {screen==="achievements" &&renderAchievements()}
      {screen==="leaderboard"  &&renderLeaderboard()}
      {screen==="settings"     &&renderSettings()}
    </div>
  );
}
