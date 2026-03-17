import React, { useState, useEffect, useRef, useCallback } from "react";

// ═══════════════════════════════════════════════════════════════
// WORLD & LEVEL DEFINITIONS
// ═══════════════════════════════════════════════════════════════
const WORLDS = [
  { id:1,  name:"Neon Meadow",   color:"#a78bfa", bg:"#0c0718", grid:"rgba(167,139,250,0.05)", accent:"#6d28d9" },
  { id:2,  name:"Cyber Coast",   color:"#22d3ee", bg:"#020c18", grid:"rgba(34,211,238,0.04)",  accent:"#0e7490" },
  { id:3,  name:"Fire Valley",   color:"#ff6030", bg:"#180400", grid:"rgba(255,96,48,0.05)",   accent:"#b45309" },
  { id:4,  name:"Shadow Realm",  color:"#c084fc", bg:"#08021a", grid:"rgba(192,132,252,0.05)", accent:"#7c3aed" },
  { id:5,  name:"Storm Peak",    color:"#60a5fa", bg:"#020818", grid:"rgba(96,165,250,0.05)",  accent:"#1d4ed8" },
  { id:6,  name:"Ghost Domain",  color:"#e879f9", bg:"#0f0520", grid:"rgba(232,121,249,0.05)", accent:"#9333ea" },
  { id:7,  name:"Inferno Core",  color:"#f97316", bg:"#1a0200", grid:"rgba(249,115,22,0.05)",  accent:"#c2410c" },
  { id:8,  name:"Void Abyss",    color:"#818cf8", bg:"#00000f", grid:"rgba(129,140,248,0.05)", accent:"#4338ca" },
  { id:9,  name:"Crystal Apex",  color:"#34d399", bg:"#000f06", grid:"rgba(52,211,153,0.05)",  accent:"#059669" },
  { id:10, name:"Nexus Throne",  color:"#fbbf24", bg:"#0f0a00", grid:"rgba(251,191,36,0.06)",  accent:"#d97706" },
];

const LEVEL_NAMES = [
  // World 1
  "First Steps","Warm Up","Getting It","Tap Dance","Rhythm Flow","Neon Lights","Grid Walk","Pulse Path","Ring Road","Boss Gate",
  // World 2
  "On the Move","Sliding In","Current Rush","Drift Avenue","Float Street","Wave Rider","Glide Gap","Surge Lane","Tidal Run","Sea Boss",
  // World 3
  "Fire Starter","Bomb Squad","Heat Wave","Danger Zone","Inferno Run","Burn Trail","Ash Path","Ember Road","Lava Lake","Fire Boss",
  // World 4
  "Fade In","Phase Walk","Ghost Alley","Flicker Hall","Shadow Lane","Phantom Path","Mist Road","Specter Run","Void Walk","Shade Boss",
  // World 5
  "Storm Brew","Thunder Road","Lightning Run","Bolt Alley","Charged Up","Volt Trail","Arc Path","Surge Run","Storm Eye","Storm Boss",
  // World 6
  "Haunt Begin","Specter Surge","Wraith Road","Phantom Rush","Ghost Blitz","Spirit Wave","Echo Hall","Shadow Blitz","Realm Run","Ghost Boss",
  // World 7
  "Ignite","Blaze Road","Fury Run","Inferno Blitz","Char Trail","Flame Rush","Burn Blitz","Cinder Road","Ash Blitz","Flame Boss",
  // World 8
  "Dark Matter","Void Pulse","Abyss Walk","Null Zone","Zero Hour","Blank Space","Deep Dark","Rift Road","Null Rush","Void Boss",
  // World 9
  "Crystal Clear","Gem Trail","Prism Road","Shard Run","Facet Blitz","Diamond Road","Quartz Rush","Emerald Lane","Crystal Blitz","Gem Boss",
  // World 10
  "Throne Approach","Royal Road","Crown Trail","Scepter Rush","Nexus Gate","Power Surge","Ultimate Run","Apex Blitz","Final Stand","NEXUS FINAL",
];

// Special milestone modifiers
const MILESTONE_MODS = {
  10:  { type:"boss_kill",  desc:"Defeat a Boss to win!" },
  20:  { type:"combo_20",   desc:"Reach 20× combo!" },
  30:  { type:"fever_2",    desc:"Trigger Fever twice!" },
  40:  { type:"no_miss",    desc:"Don't miss a single target!" },
  50:  { type:"speed_run",  desc:"Score fast — targets expire quickly!" },
  60:  { type:"moving_only",desc:"Only moving targets appear!" },
  70:  { type:"ghost_rush", desc:"Ghost targets everywhere!" },
  80:  { type:"combo_40",   desc:"Reach 40× combo!" },
  90:  { type:"fever_3",    desc:"Trigger Fever 3 times!" },
  100: { type:"final_boss", desc:"Defeat the NEXUS BOSS!" },
};

function getLevelConfig(n) {
  const world = Math.ceil(n / 10);
  const w = WORLDS[world - 1];
  const diff = (n - 1) / 99;
  const scoreGoal = Math.floor(200 + n * 100 + n * n * 0.6);
  const lives = n <= 10 ? 5 : n <= 30 ? 4 : n <= 70 ? 3 : 2;
  const spawnInterval = Math.max(420, 1400 - n * 9.5);
  const targetLifetime = Math.max(800, 3200 - n * 19);
  const bombRate = n < 6  ? 0 : Math.min(0.26, n * 0.0024);
  const movingRate = n < 11 ? 0 : Math.min(0.60, (n - 10) * 0.0068);
  const ghostRate = n < 21 ? 0 : Math.min(0.26, (n - 20) * 0.0032);
  const bossEnabled = n >= 25;
  const bossRate = n >= 25 ? Math.min(0.07, (n - 25) * 0.001) : 0;
  const mod = MILESTONE_MODS[n] || null;
  return {
    id: n, world, worldName: w.name, worldColor: w.color, worldBg: w.bg, worldGrid: w.grid,
    name: LEVEL_NAMES[n - 1] || `Level ${n}`,
    scoreGoal, lives, spawnInterval, targetLifetime,
    bombRate, movingRate, ghostRate, bossEnabled, bossRate,
    modifier: mod,
    rarityBonus: Math.min(0.14, diff * 0.14),
    isBoss: n % 10 === 0,
    isLast: n === 100,
  };
}

const ALL_LEVELS = Array.from({ length: 100 }, (_, i) => getLevelConfig(i + 1));

// ═══════════════════════════════════════════════════════════════
// GAME CONSTANTS
// ═══════════════════════════════════════════════════════════════
const BASE_R       = 26;
const MAX_LIVES    = 5;
const FEVER_STREAK = 15;
const FEVER_DUR    = 8000;
const XP_PER_LVL   = 150;

const RARITY = {
  COMMON:    { name:"common",    chance:0.55, color:"#a78bfa", glow:"#7c3aed", mult:1,  size:1.0,  label:""             },
  UNCOMMON:  { name:"uncommon",  chance:0.23, color:"#34d399", glow:"#059669", mult:2,  size:1.15, label:"BONUS ×2"     },
  RARE:      { name:"rare",      chance:0.13, color:"#fbbf24", glow:"#d97706", mult:5,  size:1.4,  label:"RARE ×5"      },
  EPIC:      { name:"epic",      chance:0.07, color:"#f472b6", glow:"#db2777", mult:15, size:1.8,  label:"EPIC ×15"     },
  LEGENDARY: { name:"legendary", chance:0.02, color:"#ff6030", glow:"#ff2000", mult:50, size:2.2,  label:"LEGENDARY ×50"},
};

const THEMES = [
  { id:"neon",   name:"Neon Purple",bg:"#0c0718",accent:"#a78bfa",secondary:"#6d28d9",grid:"rgba(167,139,250,0.05)",unlockLevel:1  },
  { id:"cyber",  name:"Cyber Blue", bg:"#020c18",accent:"#22d3ee",secondary:"#0e7490",grid:"rgba(34,211,238,0.04)", unlockLevel:5  },
  { id:"inferno",name:"Inferno",    bg:"#180400",accent:"#ff6030",secondary:"#b45309",grid:"rgba(255,96,48,0.05)", unlockLevel:10 },
  { id:"matrix", name:"Matrix",     bg:"#000e00",accent:"#39ff14",secondary:"#166534",grid:"rgba(57,255,20,0.04)", unlockLevel:20 },
  { id:"abyss",  name:"Deep Abyss", bg:"#00000f",accent:"#6060ff",secondary:"#1a1a9a",grid:"rgba(96,96,255,0.04)",unlockLevel:30 },
  { id:"rose",   name:"Rose Gold",  bg:"#180810",accent:"#ff8fab",secondary:"#9d174d",grid:"rgba(255,143,171,0.04)",unlockLevel:40},
];

const COMBO_LABELS = [
  [50,"GODLIKE!! 🔥"],[35,"UNSTOPPABLE! ⚡"],[20,"AMAZING! 💥"],[10,"GREAT! ⭐"],[5,"NICE!"],
];

const ACHIEVEMENTS = [
  { id:"first_tap",    label:"First Blood",   desc:"Tap your first target",      icon:"👆", xp:10  },
  { id:"streak_10",    label:"On Fire",        desc:"10-tap streak",              icon:"🔥", xp:20  },
  { id:"streak_25",    label:"Blazing",        desc:"25-tap streak",              icon:"⚡", xp:40  },
  { id:"streak_50",    label:"Unstoppable",    desc:"50-tap streak",              icon:"💥", xp:80  },
  { id:"first_rare",   label:"Lucky",          desc:"Hit a rare target",          icon:"⭐", xp:15  },
  { id:"first_epic",   label:"Epic!",          desc:"Hit an epic target",         icon:"💎", xp:30  },
  { id:"legendary",    label:"Legendary",      desc:"Hit a legendary target",     icon:"👑", xp:100 },
  { id:"boss_kill",    label:"Boss Slayer",    desc:"Defeat a boss",              icon:"🐲", xp:50  },
  { id:"perfect_tap",  label:"Sharpshooter",   desc:"Land a Perfect Tap",         icon:"🎯", xp:15  },
  { id:"level_10",     label:"Adventurer",     desc:"Complete Level 10",          icon:"🗺", xp:50  },
  { id:"level_25",     label:"Explorer",       desc:"Complete Level 25",          icon:"🧭", xp:80  },
  { id:"level_50",     label:"Champion",       desc:"Complete Level 50",          icon:"🏆", xp:120 },
  { id:"level_100",    label:"NEXUS MASTER",   desc:"Complete all 100 levels",    icon:"👑", xp:500 },
  { id:"three_stars",  label:"Perfectionist",  desc:"3-star any level",           icon:"🌟", xp:25  },
  { id:"fever_mode",   label:"Fever!",         desc:"Trigger Fever Mode",         icon:"🌡️",xp:30  },
  { id:"score_2000",   label:"Legend",         desc:"Score 2000 in a level",      icon:"🚀", xp:50  },
  { id:"missions_all", label:"Daily Champ",    desc:"Complete all daily missions",icon:"📋", xp:50  },
  { id:"daily_7",      label:"Dedicated",      desc:"7-day login streak",         icon:"🏅", xp:75  },
  { id:"five_star",    label:"Flawless",       desc:"Complete a boss level 3-star",icon:"🌟",xp:100 },
];

const MISSION_TEMPLATES = [
  { id:"tap_30",    desc:"Tap 30 targets",        key:"tapsTotal",        goal:30  },
  { id:"rare_5",    desc:"Hit 5 rare+ targets",   key:"rareHits",         goal:5   },
  { id:"combo_15",  desc:"Reach 15× streak",      key:"bestCombo",        goal:15  },
  { id:"boss_1",    desc:"Defeat a boss",          key:"bossKills",        goal:1   },
  { id:"fever_2",   desc:"Trigger Fever 2×",       key:"feverCount",       goal:2   },
  { id:"perfect_5", desc:"5 Perfect Taps",         key:"perfectTaps",      goal:5   },
  { id:"levels_3",  desc:"Complete 3 levels",      key:"levelsCompleted",  goal:3   },
  { id:"powerup_3", desc:"Collect 3 power-ups",   key:"powerupCollected", goal:3   },
  { id:"score_500", desc:"Score 500 in one level", key:"score",            goal:500 },
];

const SHOP_ITEMS = [
  { id:"extra_life",   name:"Extra Life",    desc:"Start with +1 life",          cost:60,  icon:"❤️" },
  { id:"head_start",   name:"Head Start",    desc:"+300 score at start",          cost:80,  icon:"🚀" },
  { id:"shield_start", name:"Shield",        desc:"Begin with active Shield",    cost:100, icon:"🛡" },
  { id:"power_pack",   name:"Power Pack",    desc:"Start with a random power-up",cost:120, icon:"⚡" },
];

const DEFAULT_SAVE = {
  highScore:0, xp:0, bestStreak:0, coins:0, totalCoins:0,
  unlockedAchievements:[], themeId:"neon", soundEnabled:true,
  scores:[], lastLoginDate:null, loginStreak:0,
  missionDate:null, missionProgress:{}, missionCompleted:false,
  levelStars:{}, unlockedLevel:1,
};

// ═══════════════════════════════════════════════════════════════
// AUDIO ENGINE
// ═══════════════════════════════════════════════════════════════
function createAudio() {
  let ctx = null;
  const C = () => { if(!ctx) ctx=new(window.AudioContext||window.webkitAudioContext)(); return ctx; };
  const t = (freq,type,dur,vol=0.26,delay=0)=>{
    try{
      const c=C(),o=c.createOscillator(),g=c.createGain();
      o.connect(g);g.connect(c.destination);
      o.type=type;o.frequency.setValueAtTime(freq,c.currentTime+delay);
      g.gain.setValueAtTime(vol,c.currentTime+delay);
      g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+delay+dur);
      o.start(c.currentTime+delay);o.stop(c.currentTime+delay+dur+0.05);
    }catch{}
  };
  const chord=(freqs,type,dur,vol,dt=0.06)=>freqs.forEach((f,i)=>t(f,type,dur,vol,i*dt));
  return{
    tap:        ()=>{t(540,"sine",0.09,0.22);t(810,"sine",0.07,0.1,0.04);},
    miss:       ()=>{t(160,"sawtooth",0.38,0.22);},
    uncommon:   ()=>{t(600,"sine",0.12,0.24);t(900,"sine",0.08,0.16,0.07);},
    rare:       ()=>{chord([660,880,1100],"sine",0.18,0.26,0.07);},
    epic:       ()=>{chord([440,554,659,880,1108],"sine",0.22,0.26,0.065);},
    legendary:  ()=>{chord([330,440,550,660,880,1100,1320],"sine",0.28,0.28,0.055);},
    boss:       ()=>{t(100,"sawtooth",0.5,0.32);t(140,"square",0.3,0.18,0.1);},
    bossHit:    ()=>{t(200,"sawtooth",0.2,0.28);t(260,"sine",0.12,0.18,0.06);},
    bossKill:   ()=>{chord([262,330,392,523,659],"sine",0.35,0.3,0.08);},
    bombSpawn:  ()=>{t(110,"sawtooth",0.4,0.28);t(75,"sawtooth",0.22,0.18,0.14);},
    bombHit:    ()=>{t(90,"sawtooth",0.55,0.36);t(55,"sawtooth",0.28,0.26,0.2);},
    powerUp:    ()=>{chord([440,554,659,880],"sine",0.14,0.22,0.055);},
    feverStart: ()=>{chord([440,554,659,880,1108],"square",0.12,0.18,0.05);},
    feverEnd:   ()=>{chord([880,659,554,440],"sine",0.14,0.18,0.07);},
    levelUp:    ()=>{chord([523,659,784,1047,1319],"sine",0.18,0.28,0.08);},
    levelComplete:()=>{chord([523,659,784,1047],"sine",0.22,0.3,0.09);},
    perfect:    ()=>{chord([880,1108,1320],"sine",0.14,0.26,0.06);},
    countdown:  ()=>{t(440,"sine",0.15,0.28);},
    go:         ()=>{chord([523,659,784],"sine",0.2,0.3,0.05);},
    gameOver:   ()=>{chord([440,370,294,220],"sawtooth",0.25,0.18,0.1);},
    coin:       ()=>{t(1200,"sine",0.08,0.16);t(1500,"sine",0.05,0.12,0.07);},
    starEarn:   ()=>{t(880,"sine",0.15,0.25);t(1108,"sine",0.1,0.2,0.12);},
    unlock:     ()=>{chord([440,554,659,784],"sine",0.2,0.22,0.07);},
    waveUp:     ()=>{chord([330,415,523,659],"square",0.2,0.2,0.07);},
  };
}

// ═══════════════════════════════════════════════════════════════
// HELPERS
// ═══════════════════════════════════════════════════════════════
function getRarity(rarityBonus=0) {
  const r=Math.random();
  let cumul=0;
  const entries=Object.values(RARITY);
  // Shift probability toward rarer items
  const adj=entries.map((v,i)=>({...v,adjChance:i<2?Math.max(0.08,v.chance-rarityBonus*(i===0?0.7:0.3)):v.chance+rarityBonus*(i===2?0.4:i===3?0.35:0.25)}));
  for(const v of adj){ cumul+=v.adjChance; if(r<cumul) return v; }
  return RARITY.COMMON;
}

const getLvl   = xp => Math.floor(xp/XP_PER_LVL)+1;
const xpToNext = xp => XP_PER_LVL-(xp%XP_PER_LVL);
function seededRng(seed){let s=seed;return()=>{s=(s*1664525+1013904223)&0xffffffff;return(s>>>0)/0xffffffff;};}
function getDailyMissions(){const d=new Date();const seed=d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();const rng=seededRng(seed);return[...MISSION_TEMPLATES].sort(()=>rng()-0.5).slice(0,3);}
function getTodayKey(){const d=new Date();return`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;}
function loadSave(){try{const r=localStorage.getItem("nexustap_v5");if(r)return{...DEFAULT_SAVE,...JSON.parse(r)};}catch{}return{...DEFAULT_SAVE};}
function vibrate(p){try{if(navigator.vibrate)navigator.vibrate(p);}catch{}}

// ═══════════════════════════════════════════════════════════════
// CANVAS DRAWING — ENHANCED ANIMATED SHAPES
// ═══════════════════════════════════════════════════════════════

// Urgency pulse: blinks when < 25% lifetime remains
function urgencyAlpha(timeLeft, ts) {
  if(timeLeft>0.25) return 1;
  return 0.55+0.45*Math.abs(Math.sin(ts/120));
}

// Draw orbiting dots around a center
function drawOrbiters(ctx, count, orbitR, dotR, color, ts, speed=1) {
  for(let i=0;i<count;i++){
    const a = ts*speed*0.001 + i*(Math.PI*2/count);
    const x = Math.cos(a)*orbitR, y = Math.sin(a)*orbitR;
    ctx.save();
    ctx.fillStyle=color; ctx.shadowColor=color; ctx.shadowBlur=dotR*3;
    ctx.globalAlpha=0.9;
    ctx.beginPath(); ctx.arc(x,y,dotR,0,Math.PI*2); ctx.fill();
    ctx.restore();
  }
}

// Radial light beams from center
function drawBeams(ctx, count, r, color, ts, speed=0.4) {
  const rot = ts*speed*0.001;
  for(let i=0;i<count;i++){
    const a = rot + i*(Math.PI*2/count);
    ctx.save();
    ctx.globalAlpha=0.18;
    ctx.strokeStyle=color;
    ctx.lineWidth=3;
    ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r); ctx.stroke();
    ctx.restore();
  }
}

// Electric arc between two points
function drawArc(ctx, x1,y1,x2,y2, color, ts, id=0) {
  const steps=8, amp=4+2*Math.sin(ts*0.01+id);
  ctx.beginPath(); ctx.moveTo(x1,y1);
  for(let i=1;i<steps;i++){
    const p=i/steps;
    const mx=x1+(x2-x1)*p, my=y1+(y2-y1)*p;
    const nx=-(y2-y1)/Math.hypot(x2-x1,y2-y1), ny=(x2-x1)/Math.hypot(x2-x1,y2-y1);
    const jitter=amp*Math.sin(ts*0.015+id*7+i*1.3);
    ctx.lineTo(mx+nx*jitter, my+ny*jitter);
  }
  ctx.lineTo(x2,y2);
  ctx.strokeStyle=color; ctx.lineWidth=1.5; ctx.globalAlpha=0.6;
  ctx.shadowColor=color; ctx.shadowBlur=6;
  ctx.stroke();
}

// ── Common: Animated radar rings ──
function drawCommon(ctx, r, color, glow, ts, timeLeft) {
  const ua=urgencyAlpha(timeLeft,ts);
  ctx.save(); ctx.globalAlpha=ua;
  // Pulsing fill
  const pulse=0.5+0.5*Math.sin(ts*0.003);
  ctx.fillStyle=color; ctx.globalAlpha=ua*(0.08+pulse*0.06);
  ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill();
  // 3 rings rotating at different speeds
  const speeds=[0.5,0.8,-0.6]; const radii=[r*0.98,r*0.72,r*0.46];
  speeds.forEach((sp,i)=>{
    ctx.save(); ctx.rotate(ts*sp*0.001);
    ctx.strokeStyle=color; ctx.lineWidth= i===0?2.5:1.8; ctx.globalAlpha=ua*(0.8-i*0.15);
    ctx.shadowColor=glow; ctx.shadowBlur=8;
    // Dashed for inner rings
    if(i>0) ctx.setLineDash([radii[i]*0.4,radii[i]*0.2]);
    ctx.beginPath(); ctx.arc(0,0,radii[i],0,Math.PI*2); ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
  });
  // Scanning laser line
  ctx.save(); ctx.rotate(ts*0.002);
  const scanGrad=ctx.createLinearGradient(0,0,r*0.92,0);
  scanGrad.addColorStop(0,color+"ff"); scanGrad.addColorStop(1,color+"00");
  ctx.strokeStyle=scanGrad; ctx.lineWidth=2; ctx.globalAlpha=ua*0.8;
  ctx.shadowColor=glow; ctx.shadowBlur=12;
  ctx.beginPath(); ctx.moveTo(0,0); ctx.lineTo(r*0.92,0); ctx.stroke();
  ctx.restore();
  // Pulsing center dot
  const dotR=r*0.18*(1+pulse*0.2);
  ctx.fillStyle=color; ctx.globalAlpha=ua*0.9; ctx.shadowColor=glow; ctx.shadowBlur=16;
  ctx.beginPath(); ctx.arc(0,0,dotR,0,Math.PI*2); ctx.fill();
  ctx.restore();
}

// ── Uncommon: Spinning diamond with orbiting sparks ──
function drawUncommon(ctx, r, color, glow, ts, timeLeft) {
  const ua=urgencyAlpha(timeLeft,ts);
  ctx.save(); ctx.globalAlpha=ua;
  // Outer diamond
  ctx.save(); ctx.rotate(ts*0.0008);
  ctx.shadowColor=glow; ctx.shadowBlur=r*1;
  const d=r-2;
  ctx.fillStyle=color+"28"; ctx.strokeStyle=color; ctx.lineWidth=2.5;
  ctx.beginPath(); ctx.moveTo(0,-d); ctx.lineTo(d*0.8,0); ctx.lineTo(0,d); ctx.lineTo(-d*0.8,0); ctx.closePath();
  ctx.fill(); ctx.stroke(); ctx.restore();
  // Inner diamond counter-rotating
  ctx.save(); ctx.rotate(-ts*0.0015);
  const id2=r*0.52;
  ctx.fillStyle=color+"55"; ctx.strokeStyle=color+"aa"; ctx.lineWidth=1.5;
  ctx.beginPath(); ctx.moveTo(0,-id2); ctx.lineTo(id2*0.8,0); ctx.lineTo(0,id2); ctx.lineTo(-id2*0.8,0); ctx.closePath();
  ctx.fill(); ctx.stroke(); ctx.restore();
  // 4 orbiting sparks (speed up when urgent)
  const orbSpeed = timeLeft<0.25?3.5:1.5;
  drawOrbiters(ctx,4,r*0.62,r*0.1,color,ts,orbSpeed);
  // Center
  const pulse=0.5+0.5*Math.sin(ts*0.004);
  ctx.fillStyle=color; ctx.globalAlpha=ua*0.9; ctx.shadowColor=glow; ctx.shadowBlur=14;
  ctx.beginPath(); ctx.arc(0,0,r*0.2*(1+pulse*0.15),0,Math.PI*2); ctx.fill();
  ctx.restore();
}

// ── Rare: 5-star with orbiting micro-stars ──
function drawRare(ctx, r, color, glow, ts, timeLeft) {
  const ua=urgencyAlpha(timeLeft,ts);
  const pulse=0.5+0.5*Math.sin(ts*0.0035);
  ctx.save(); ctx.globalAlpha=ua;
  // Glow aura
  const auraGrad=ctx.createRadialGradient(0,0,r*0.2,0,0,r*1.3);
  auraGrad.addColorStop(0,color+"40"); auraGrad.addColorStop(1,color+"00");
  ctx.fillStyle=auraGrad; ctx.beginPath(); ctx.arc(0,0,r*1.3,0,Math.PI*2); ctx.fill();
  // Star shape (rotating)
  ctx.save(); ctx.rotate(ts*0.0007);
  ctx.shadowColor=glow; ctx.shadowBlur=r*1.2;
  ctx.fillStyle=color+"44"; ctx.strokeStyle=color; ctx.lineWidth=2.5;
  ctx.beginPath();
  for(let i=0;i<10;i++){
    const a=i*Math.PI/5-Math.PI/2;
    const cr=i%2===0?r-2:r*0.42;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // Second star counter-rotating (slightly smaller)
  ctx.save(); ctx.rotate(-ts*0.0012);
  ctx.strokeStyle=color+"66"; ctx.lineWidth=1.5; ctx.fillStyle="transparent";
  ctx.beginPath();
  for(let i=0;i<10;i++){
    const a=i*Math.PI/5-Math.PI/2+Math.PI/10;
    const cr=i%2===0?(r-2)*0.75:r*0.35;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.stroke(); ctx.restore();
  // 5 orbiting micro-stars
  const orbSpeed=timeLeft<0.25?4:1.8;
  for(let i=0;i<5;i++){
    const a=ts*orbSpeed*0.001+i*(Math.PI*2/5);
    const ox=Math.cos(a)*(r+9), oy=Math.sin(a)*(r+9);
    ctx.save(); ctx.globalAlpha=ua*0.9; ctx.fillStyle=color; ctx.shadowColor=glow; ctx.shadowBlur=6;
    ctx.beginPath(); ctx.arc(ox,oy,r*0.1,0,Math.PI*2); ctx.fill(); ctx.restore();
  }
  // Inner glowing orb
  const coreR=r*0.22*(1+pulse*0.2);
  const coreGrad=ctx.createRadialGradient(0,0,0,0,0,coreR);
  coreGrad.addColorStop(0,"#fff"); coreGrad.addColorStop(0.5,color); coreGrad.addColorStop(1,glow);
  ctx.fillStyle=coreGrad; ctx.globalAlpha=ua*0.95; ctx.shadowColor=glow; ctx.shadowBlur=20;
  ctx.beginPath(); ctx.arc(0,0,coreR,0,Math.PI*2); ctx.fill();
  ctx.restore();
}

// ── Epic: Layered hexagons with electric arcs ──
function drawEpic(ctx, r, color, glow, ts, timeLeft) {
  const ua=urgencyAlpha(timeLeft,ts);
  const pulse=0.5+0.5*Math.sin(ts*0.004);
  ctx.save(); ctx.globalAlpha=ua;
  // Outer glow
  const auraGrad=ctx.createRadialGradient(0,0,r*0.3,0,0,r*1.5);
  auraGrad.addColorStop(0,color+"50"); auraGrad.addColorStop(1,color+"00");
  ctx.fillStyle=auraGrad; ctx.beginPath(); ctx.arc(0,0,r*1.5,0,Math.PI*2); ctx.fill();
  // Outer 6-star rotating
  ctx.save(); ctx.rotate(ts*0.0007);
  ctx.shadowColor=glow; ctx.shadowBlur=r*1.4;
  ctx.fillStyle=color+"35"; ctx.strokeStyle=color; ctx.lineWidth=2.8;
  ctx.beginPath();
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6-Math.PI/2;
    const cr=i%2===0?r-2:r*0.5;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // Inner hexagon counter-rotating
  ctx.save(); ctx.rotate(-ts*0.0018);
  ctx.strokeStyle=color+"88"; ctx.lineWidth=2; ctx.fillStyle=color+"18";
  ctx.beginPath();
  for(let i=0;i<6;i++){
    const a=i*Math.PI/3-Math.PI/6;
    const cr=r*0.52;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // Electric arcs between star tips
  ctx.save(); ctx.rotate(ts*0.0007);
  const tips=Array.from({length:6},(_,i)=>{const a=i*Math.PI/3-Math.PI/2; return{x:Math.cos(a)*(r-2),y:Math.sin(a)*(r-2)};});
  ctx.globalAlpha=ua*0.7;
  for(let i=0;i<6;i++) drawArc(ctx,tips[i].x,tips[i].y,tips[(i+2)%6].x,tips[(i+2)%6].y,color,ts,i);
  ctx.restore();
  // 6 orbiting dots
  drawOrbiters(ctx,6,r*0.68,r*0.095,color,ts,timeLeft<0.25?5:2);
  // Bright center
  const coreGrad=ctx.createRadialGradient(0,0,0,0,0,r*(0.28+pulse*0.05));
  coreGrad.addColorStop(0,"#fff"); coreGrad.addColorStop(0.35,color); coreGrad.addColorStop(1,glow+"00");
  ctx.fillStyle=coreGrad; ctx.globalAlpha=ua; ctx.shadowColor=glow; ctx.shadowBlur=28;
  ctx.beginPath(); ctx.arc(0,0,r*(0.28+pulse*0.05),0,Math.PI*2); ctx.fill();
  ctx.restore();
}

// ── Legendary: Full animated explosion star ──
function drawLegendary(ctx, r, color, glow, ts, timeLeft) {
  const ua=urgencyAlpha(timeLeft,ts);
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  const spin=ts*0.0015;
  ctx.save(); ctx.globalAlpha=ua;
  // Massive aura
  const auraGrad=ctx.createRadialGradient(0,0,0,0,0,r*2.0);
  auraGrad.addColorStop(0,color+"55"); auraGrad.addColorStop(0.5,color+"20"); auraGrad.addColorStop(1,color+"00");
  ctx.fillStyle=auraGrad; ctx.beginPath(); ctx.arc(0,0,r*2.0,0,Math.PI*2); ctx.fill();
  // Radial beams
  drawBeams(ctx,12,r*1.6,color,ts,0.5);
  // Outer rotating ring of dashes
  ctx.save(); ctx.rotate(spin*0.7);
  ctx.strokeStyle=color+"88"; ctx.lineWidth=2; ctx.setLineDash([r*0.3,r*0.15]);
  ctx.beginPath(); ctx.arc(0,0,r+8,0,Math.PI*2); ctx.stroke();
  ctx.setLineDash([]); ctx.restore();
  // 8-point star (main body)
  ctx.save(); ctx.rotate(spin);
  ctx.shadowColor=glow; ctx.shadowBlur=r*1.8;
  ctx.fillStyle=color+"45"; ctx.strokeStyle=color; ctx.lineWidth=3;
  ctx.beginPath();
  for(let i=0;i<16;i++){
    const a=i*Math.PI/8-Math.PI/2;
    const cr=i%2===0?r-2:r*0.45;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // Inner rotating star (counter)
  ctx.save(); ctx.rotate(-spin*1.5);
  ctx.strokeStyle=color+"77"; ctx.lineWidth=2; ctx.fillStyle=color+"22";
  ctx.beginPath();
  for(let i=0;i<16;i++){
    const a=i*Math.PI/8-Math.PI/2+Math.PI/16;
    const cr=i%2===0?(r-2)*0.68:r*0.32;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // 3 orbiting satellites at different radii
  [[r*0.88,3,0.9],[r*1.15,2,1.5],[r*1.35,1.5,2.2]].forEach(([orR,dotR,sp],i)=>{
    const a=ts*sp*0.001+i*(Math.PI*2/3);
    const ox=Math.cos(a)*orR, oy=Math.sin(a)*orR;
    ctx.save(); ctx.globalAlpha=ua*0.95; ctx.fillStyle=color; ctx.shadowColor=glow; ctx.shadowBlur=dotR*5;
    ctx.beginPath(); ctx.arc(ox,oy,dotR,0,Math.PI*2); ctx.fill(); ctx.restore();
  });
  // Radiant core
  const coreR=r*(0.22+pulse*0.06);
  const coreGrad=ctx.createRadialGradient(0,0,0,0,0,coreR);
  coreGrad.addColorStop(0,"#fff"); coreGrad.addColorStop(0.3,"#fff"); coreGrad.addColorStop(0.7,color); coreGrad.addColorStop(1,glow);
  ctx.fillStyle=coreGrad; ctx.globalAlpha=ua; ctx.shadowColor="#fff"; ctx.shadowBlur=40;
  ctx.beginPath(); ctx.arc(0,0,coreR,0,Math.PI*2); ctx.fill();
  ctx.restore();
}

// ── Bomb target ──
function drawBomb(ctx, r, color, glow, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.008);
  ctx.shadowColor="#ef4444"; ctx.shadowBlur=r*(0.8+pulse*1.2);
  // Dark body
  const bodyGrad=ctx.createRadialGradient(-r*0.2,-r*0.2,0,0,0,r);
  bodyGrad.addColorStop(0,"#3a0000"); bodyGrad.addColorStop(1,"#0a0000");
  ctx.fillStyle=bodyGrad; ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill();
  // Red ring
  ctx.strokeStyle="#ef4444"; ctx.lineWidth=3; ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.stroke();
  // Warning triangle
  ctx.fillStyle="#ef4444"; ctx.globalAlpha=0.9;
  const tw=r*0.55, th=r*0.55;
  ctx.beginPath(); ctx.moveTo(0,-th); ctx.lineTo(tw*0.86,th*0.5); ctx.lineTo(-tw*0.86,th*0.5); ctx.closePath(); ctx.fill();
  ctx.fillStyle="#1a0000"; ctx.font=`bold ${r*0.55}px sans-serif`; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.fillText("!",0,r*0.08);
  // Spikes
  ctx.globalAlpha=0.4+pulse*0.5;
  ctx.strokeStyle="#ff6666"; ctx.lineWidth=1.5;
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4, s=r*1.05, e=r*1.28+pulse*6;
    ctx.beginPath(); ctx.moveTo(Math.cos(a)*s,Math.sin(a)*s); ctx.lineTo(Math.cos(a)*e,Math.sin(a)*e); ctx.stroke();
  }
  ctx.globalAlpha=1;
}

// ── Power-up target ──
function drawPowerup(ctx, r, pwrType, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  ctx.shadowColor="#60a5fa"; ctx.shadowBlur=r*(0.8+pulse*0.6);
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#1a3060"); grad.addColorStop(1,"#060c20");
  ctx.fillStyle=grad; ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.fill();
  ctx.strokeStyle="#60a5fa"; ctx.lineWidth=2.5; ctx.beginPath(); ctx.arc(0,0,r,0,Math.PI*2); ctx.stroke();
  // Rotating outer ring
  ctx.save(); ctx.rotate(ts*0.002); ctx.strokeStyle="#60a5fa55"; ctx.lineWidth=1.5;
  ctx.setLineDash([r*0.35,r*0.18]); ctx.beginPath(); ctx.arc(0,0,r-4,0,Math.PI*2); ctx.stroke();
  ctx.setLineDash([]); ctx.restore();
  // Icon
  const icons={SHIELD:"🛡",SLOW:"🐢",DOUBLE:"×2",LIFE:"❤️",FREEZE:"❄️"};
  const label=icons[pwrType]||"⚡";
  ctx.font=`bold ${r*0.9}px serif`; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.fillStyle="#fff"; ctx.globalAlpha=0.95+pulse*0.05;
  ctx.fillText(label,0,r*0.05);
  ctx.globalAlpha=1;
}

// ── Boss target ──
function drawBoss(ctx, r, hitsLeft, maxHits, ts) {
  const phase=(maxHits-hitsLeft)/maxHits;
  const colors=["#ff6030","#f472b6","#ef4444"];
  const c=colors[Math.min(Math.floor(phase*3),2)];
  const glow=colors[Math.min(Math.floor(phase*3),2)];
  const spin=ts*0.001;
  const pulse=0.5+0.5*Math.sin(ts*0.006);
  ctx.save();
  // Outer glow aura
  const auraGrad=ctx.createRadialGradient(0,0,r*0.5,0,0,r*1.8);
  auraGrad.addColorStop(0,c+"50"); auraGrad.addColorStop(1,c+"00");
  ctx.fillStyle=auraGrad; ctx.beginPath(); ctx.arc(0,0,r*1.8,0,Math.PI*2); ctx.fill();
  // Rotating spike ring
  ctx.save(); ctx.rotate(spin*0.7);
  ctx.strokeStyle=c+"99"; ctx.lineWidth=2;
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6; const s=r*1.02,e=r*1.35+pulse*8;
    ctx.shadowColor=glow; ctx.shadowBlur=10;
    ctx.beginPath(); ctx.moveTo(Math.cos(a)*s,Math.sin(a)*s); ctx.lineTo(Math.cos(a)*e,Math.sin(a)*e); ctx.stroke();
  }
  ctx.restore();
  // Main 6-star
  ctx.save(); ctx.rotate(spin);
  ctx.shadowColor=glow; ctx.shadowBlur=r*1.8;
  const fcs=ctx.createRadialGradient(0,0,0,0,0,r);
  fcs.addColorStop(0,c+"88"); fcs.addColorStop(1,c+"22");
  ctx.fillStyle=fcs; ctx.strokeStyle=c; ctx.lineWidth=3;
  ctx.beginPath();
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6-Math.PI/2;
    const cr=i%2===0?r-2:r*0.5;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.fill(); ctx.stroke(); ctx.restore();
  // Counter-rotating inner
  ctx.save(); ctx.rotate(-spin*2);
  ctx.strokeStyle=c+"66"; ctx.lineWidth=2; ctx.fillStyle="transparent";
  ctx.beginPath();
  for(let i=0;i<12;i++){
    const a=i*Math.PI/6-Math.PI/2+Math.PI/12;
    const cr=i%2===0?(r-2)*0.62:r*0.3;
    i===0?ctx.moveTo(Math.cos(a)*cr,Math.sin(a)*cr):ctx.lineTo(Math.cos(a)*cr,Math.sin(a)*cr);
  }
  ctx.closePath(); ctx.stroke(); ctx.restore();
  // Electric arcs
  ctx.save(); ctx.rotate(spin);
  const tips=Array.from({length:6},(_,i)=>{const a=i*Math.PI/3-Math.PI/2; return{x:Math.cos(a)*(r-2),y:Math.sin(a)*(r-2)};});
  ctx.globalAlpha=0.75;
  for(let i=0;i<6;i++) drawArc(ctx,tips[i].x,tips[i].y,tips[(i+2)%6].x,tips[(i+2)%6].y,c,ts,i);
  ctx.restore();
  // "BOSS" label
  ctx.save(); ctx.globalAlpha=0.85;
  ctx.font=`bold ${r*0.38}px 'Segoe UI',sans-serif`; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.fillStyle="#fff"; ctx.shadowColor="#fff"; ctx.shadowBlur=10;
  ctx.fillText("BOSS",0,0); ctx.restore();
  // HP bar
  const bw=r*2.4, bh=8, by=r+12;
  ctx.fillStyle="#1a1a1a"; ctx.fillRect(-bw/2,by,bw,bh);
  const hpCol=phase<0.5?"#34d399":phase<0.8?"#fbbf24":"#ef4444";
  ctx.fillStyle=hpCol; ctx.shadowColor=hpCol; ctx.shadowBlur=8;
  ctx.fillRect(-bw/2,by,bw*(hitsLeft/maxHits),bh);
  ctx.strokeStyle="#ffffff33"; ctx.lineWidth=1; ctx.shadowBlur=0;
  ctx.strokeRect(-bw/2,by,bw,bh);
  ctx.restore();
}

// ── Motion trail for moving targets ──
function drawTrail(ctx, t) {
  if(!t.trail||t.trail.length<2) return;
  for(let i=1;i<t.trail.length;i++){
    const a=i/t.trail.length;
    ctx.save(); ctx.globalAlpha=a*0.3;
    ctx.strokeStyle=t.color; ctx.lineWidth=t.radius*1.8*a; ctx.lineCap="round";
    ctx.shadowColor=t.color; ctx.shadowBlur=t.radius*a;
    ctx.beginPath(); ctx.moveTo(t.trail[i-1].x,t.trail[i-1].y); ctx.lineTo(t.trail[i].x,t.trail[i].y);
    ctx.stroke(); ctx.restore();
  }
}

// ── Direction arrow for moving targets ──
function drawArrow(ctx, vx, vy, r, color) {
  const len=Math.hypot(vx,vy); if(len<0.01) return;
  const angle=Math.atan2(vy,vx);
  const ar=r+14, aw=6;
  ctx.save();
  ctx.translate(Math.cos(angle)*ar, Math.sin(angle)*ar);
  ctx.rotate(angle);
  ctx.fillStyle=color; ctx.globalAlpha=0.6; ctx.shadowColor=color; ctx.shadowBlur=6;
  ctx.beginPath(); ctx.moveTo(aw,0); ctx.lineTo(-aw,-aw*0.6); ctx.lineTo(-aw,aw*0.6); ctx.closePath();
  ctx.fill(); ctx.restore();
}

// ── Master target draw dispatcher ──
function drawTarget(ctx, t, ts) {
  const now=Date.now();
  const timeLeft=Math.max(0,1-(now-t.spawnedAt)/t.lifetime);
  const agePn=performance.now()-t.born;
  const spawnScale=agePn<200?Math.min(1.08,agePn/200*1.08):1;
  let ghostAlpha=1;
  if(t.ghost) ghostAlpha=0.3+0.7*(0.5+0.5*Math.sin(ts/200));

  if(t.moving) drawTrail(ctx,t);

  ctx.save();
  ctx.globalAlpha=ghostAlpha;
  ctx.translate(t.x,t.y);
  ctx.scale(spawnScale,spawnScale);

  if     (t.type==="bomb")    drawBomb(ctx,t.radius,t.color,t.glow,ts);
  else if(t.type==="powerup") drawPowerup(ctx,t.radius,t.pwrType,ts);
  else if(t.type==="boss")    drawBoss(ctx,t.radius,t.hitsLeft,t.maxHits,ts);
  else{
    const nm=t.rarity?.name;
    if     (nm==="common")    drawCommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="uncommon")  drawUncommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="rare")      drawRare(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="epic")      drawEpic(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="legendary") drawLegendary(ctx,t.radius,t.color,t.glow,ts,timeLeft);
  }
  // Timer ring
  if(t.type!=="bomb"&&t.type!=="boss"){
    const rr=t.radius+7;
    ctx.shadowBlur=0; ctx.strokeStyle=timeLeft<0.25?"#ef4444":t.color;
    ctx.lineWidth=3; ctx.globalAlpha=0.5*(ghostAlpha);
    ctx.beginPath(); ctx.arc(0,0,rr,-Math.PI/2,-Math.PI/2+2*Math.PI*timeLeft); ctx.stroke();
  }
  // Direction arrow for moving targets
  if(t.moving) drawArrow(ctx,t.vx,t.vy,t.radius,t.color);
  ctx.restore();
}

// ── Particle draw ──
function drawParticle(ctx,p,now){
  const age=now-p.born, life=Math.max(0,1-age/p.duration);
  ctx.save(); ctx.globalAlpha=life*(p.alpha||1);
  if(p.type==="shockwave"){
    ctx.strokeStyle=p.color; ctx.lineWidth=2*(1-life); ctx.shadowColor=p.color; ctx.shadowBlur=12;
    ctx.beginPath(); ctx.arc(p.x,p.y,(1-life)*65,0,Math.PI*2); ctx.stroke();
  } else if(p.type==="popup"){
    const yOff=age*0.065;
    ctx.fillStyle=p.color; ctx.shadowColor=p.color; ctx.shadowBlur=12;
    ctx.font=`bold ${p.size||14}px 'Segoe UI',sans-serif`;
    ctx.textAlign="center"; ctx.textBaseline="middle";
    ctx.fillText(p.text,p.x,p.y-yOff);
  } else if(p.type==="spark"){
    ctx.strokeStyle=p.color; ctx.lineWidth=Math.max(0.5,p.size*life); ctx.lineCap="round";
    ctx.shadowColor=p.color; ctx.shadowBlur=p.size*3;
    ctx.beginPath(); ctx.moveTo(p.x-p.vx*2,p.y-p.vy*2); ctx.lineTo(p.x,p.y); ctx.stroke();
  } else {
    ctx.fillStyle=p.color; ctx.shadowColor=p.color; ctx.shadowBlur=p.size*2.5;
    const s=Math.max(0,p.size*life);
    ctx.beginPath(); ctx.arc(p.x,p.y,s,0,Math.PI*2); ctx.fill();
  }
  ctx.restore();
}

// ── Background ──
function drawBg(ctx,w,h,accent,gridColor,ts,fever){
  ctx.clearRect(0,0,w,h);
  const gs=44, pulse=0.5+0.5*Math.sin(ts/1500);
  // Grid
  ctx.strokeStyle=gridColor; ctx.lineWidth=0.7;
  for(let x=0;x<w;x+=gs){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
  for(let y=0;y<h;y+=gs){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  // Accent lines
  ctx.strokeStyle=accent; ctx.globalAlpha=(0.07+pulse*0.05)*(fever?3:1); ctx.lineWidth=1.2;
  for(let x=0;x<w;x+=gs*5){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
  for(let y=0;y<h;y+=gs*5){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  ctx.globalAlpha=1;
}

function drawBgParticles(ctx,parts,accent,fever){
  const cw=ctx.canvas.width,ch=ctx.canvas.height;
  parts.forEach(p=>{
    p.x+=p.vx; p.y+=p.vy;
    if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;if(p.y<0)p.y=ch;if(p.y>ch)p.y=0;
    ctx.save(); ctx.globalAlpha=p.alpha*(fever?1.8:1);
    ctx.fillStyle=fever?"#fbbf24":accent; ctx.shadowColor=fever?"#fbbf24":accent; ctx.shadowBlur=p.r*4;
    ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill(); ctx.restore();
  });
}

function drawRipples(ctx,ripples){
  for(let i=ripples.length-1;i>=0;i--){
    const rp=ripples[i]; rp.r+=4; rp.alpha-=0.048;
    if(rp.alpha<=0){ripples.splice(i,1);continue;}
    ctx.save(); ctx.globalAlpha=rp.alpha; ctx.strokeStyle=rp.color;
    ctx.lineWidth=2.2; ctx.shadowColor=rp.color; ctx.shadowBlur=10;
    ctx.beginPath(); ctx.arc(rp.x,rp.y,rp.r,0,Math.PI*2); ctx.stroke(); ctx.restore();
  }
}


// ═══════════════════════════════════════════════════════════════
// NEON BUTTON
// ═══════════════════════════════════════════════════════════════
function NeonButton({children,onClick,style,className="",disabled=false}){
  const [pressed,setPressed]=useState(false);
  return(
    <button disabled={disabled}
      onMouseDown={()=>setPressed(true)} onMouseUp={()=>setPressed(false)} onMouseLeave={()=>setPressed(false)}
      onTouchStart={e=>{e.preventDefault();setPressed(true);}}
      onTouchEnd={e=>{e.preventDefault();setPressed(false);if(!disabled&&onClick)onClick(e);}}
      onClick={e=>{if(!disabled&&onClick)onClick(e);}}
      className={`select-none transition-all duration-75 rounded-2xl font-bold text-white ${className}`}
      style={{transform:pressed?"scale(0.93)":"scale(1)",opacity:disabled?0.35:1,cursor:disabled?"not-allowed":"pointer",
        userSelect:"none",WebkitTapHighlightColor:"transparent",...style}}>
      {children}
    </button>
  );
}

// ═══════════════════════════════════════════════════════════════
// MAIN COMPONENT
// ═══════════════════════════════════════════════════════════════
export default function NexusTap(){
  // Persistent
  const saveRef   = useRef(loadSave());
  const audioRef  = useRef(null);
  const saveTimer = useRef(null);

  // UI state
  const [screen,      setScreen]    = useState("menu");
  const [theme,       setTheme]     = useState(()=>THEMES.find(t=>t.id===saveRef.current.themeId)||THEMES[0]);
  const [soundOn,     setSoundOn]   = useState(()=>saveRef.current.soundEnabled);
  const [notif,       setNotif]     = useState(null);
  const [cartItems,   setCartItems] = useState([]);

  // HUD (updated 20fps)
  const [hud,setHud] = useState({score:0,lives:3,streak:0,fever:false,coins:0,timeLeft:null,modGoal:null});
  const hudRef = useRef(0);

  // Overlay
  const [activePwrDisp, setActivePwrDisp] = useState([]);
  const [comboLabel,    setComboLabel]    = useState("");
  const [countdownVal,  setCountdownVal]  = useState(null);
  const [paused,        setPaused]        = useState(false);
  const [screenShake,   setScreenShake]   = useState(false);
  const [epicFlash,     setEpicFlash]     = useState(false);
  const [feverBorder,   setFeverBorder]   = useState(false);
  const [perfectFlash,  setPerfectFlash]  = useState(false);
  const [levelCompleteData, setLevelCompleteData] = useState(null);
  const [gameOverData,      setGameOverData]      = useState(null);
  const [selectedLevel,     setSelectedLevel]     = useState(1);
  const [scrollToLevel,     setScrollToLevel]     = useState(null); // signal map to scroll

  // Canvas & game refs
  const canvasRef    = useRef(null);
  const gsRef        = useRef(null);
  const targetsRef   = useRef([]);
  const particlesRef = useRef([]);
  const activePwrRef = useRef([]);
  const rafRef       = useRef(null);
  const lastTickRef  = useRef(0);
  const spawnTimer   = useRef(0);
  const bgPartsRef   = useRef([]);
  const ripplesRef   = useRef([]);
  const missionProg  = useRef({});
  const pausedRef    = useRef(false);
  const levelCfgRef  = useRef(null); // current level config

  // Audio
  useEffect(()=>{audioRef.current=createAudio();},[]);
  const sfx=useCallback((n)=>{if(soundOn&&audioRef.current?.[n])audioRef.current[n]();},[soundOn]);

  // Save
  const flushSave=useCallback(()=>{try{localStorage.setItem("nexustap_v5",JSON.stringify(saveRef.current));}catch{}},[]);
  const debounceSave=useCallback(()=>{
    if(saveTimer.current)clearTimeout(saveTimer.current);
    saveTimer.current=setTimeout(flushSave,1800);
  },[flushSave]);

  // Notification
  useEffect(()=>{if(!notif)return;const t=setTimeout(()=>setNotif(null),2600);return()=>clearTimeout(t);},[notif]);

  // Achievements
  const unlock=useCallback((id)=>{
    const sv=saveRef.current;
    if(sv.unlockedAchievements.includes(id))return;
    sv.unlockedAchievements=[...sv.unlockedAchievements,id];
    const ach=ACHIEVEMENTS.find(a=>a.id===id);
    if(ach){setNotif(`${ach.icon} ${ach.label}!`);sv.xp+=ach.xp||0;}
    debounceSave();
  },[debounceSave]);

  // Daily login
  useEffect(()=>{
    const sv=saveRef.current, today=getTodayKey();
    if(sv.lastLoginDate===today)return;
    const yesterday=(d=>{d.setDate(d.getDate()-1);return`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;})(new Date());
    sv.loginStreak=sv.lastLoginDate===yesterday?(sv.loginStreak||0)+1:1;
    sv.lastLoginDate=today;
    sv.xp+=20+Math.min(sv.loginStreak,7)*5;
    setNotif(`Day ${sv.loginStreak} login! +${20+Math.min(sv.loginStreak,7)*5} XP`);
    if(sv.loginStreak>=7)unlock("daily_7");
    flushSave();
  },[]);// eslint-disable-line

  // Missions
  const initMissions=useCallback(()=>{
    const sv=saveRef.current,today=getTodayKey();
    if(sv.missionDate!==today){sv.missionDate=today;sv.missionProgress={};sv.missionCompleted=false;flushSave();}
    missionProg.current={...sv.missionProgress};
  },[flushSave]);

  const updateMissions=useCallback((stats)=>{
    const missions=getDailyMissions(),prog=missionProg.current;
    let changed=false;
    missions.forEach(m=>{
      const cur=prog[m.id]||0,val=stats[m.key]||0;
      if(val>cur){prog[m.id]=Math.min(val,m.goal);changed=true;}
    });
    if(changed){
      saveRef.current.missionProgress={...prog};
      if(missions.every(m=>(prog[m.id]||0)>=m.goal)&&!saveRef.current.missionCompleted){
        saveRef.current.missionCompleted=true;saveRef.current.xp+=200;
        setNotif("All missions done! +200 XP 🎉");unlock("missions_all");
      }
      debounceSave();
    }
  },[debounceSave,unlock]);

  // Canvas setup
  const initBgParts=useCallback(()=>{
    bgPartsRef.current=Array.from({length:50},()=>({
      x:Math.random()*window.innerWidth,y:Math.random()*window.innerHeight,
      vx:(Math.random()-0.5)*0.3,vy:(Math.random()-0.5)*0.3,
      r:Math.random()*2+0.5,alpha:Math.random()*0.32+0.06,
    }));
  },[]);

  useEffect(()=>{
    const resize=()=>{if(canvasRef.current){canvasRef.current.width=window.innerWidth;canvasRef.current.height=window.innerHeight;}};
    resize();window.addEventListener("resize",resize);initBgParts();
    return()=>window.removeEventListener("resize",resize);
  },[initBgParts]);

  // Spawn helpers
  const spawnParticles=useCallback((x,y,color,count=10,type="dot")=>{
    const now=performance.now();
    for(let i=0;i<count;i++){
      const angle=Math.random()*Math.PI*2,spd=2+Math.random()*8;
      particlesRef.current.push({type,x,y,vx:Math.cos(angle)*spd,vy:Math.sin(angle)*spd-(type==="spark"?2:0),
        color,size:Math.random()*5+1.5,born:now,duration:380+Math.random()*340,alpha:1});
    }
    if(count>=10) particlesRef.current.push({type:"shockwave",x,y,r:1,color,born:now,duration:480,alpha:0.8});
  },[]);

  const spawnPopup=useCallback((x,y,text,color,size=14)=>{
    particlesRef.current.push({type:"popup",x,y,vx:0,vy:0,text,color,size,born:performance.now(),duration:900,alpha:1});
  },[]);

  const pickPos=useCallback((radius)=>{
    const margin=radius*2+25,w=window.innerWidth,h=window.innerHeight;
    let best=null,bestD=-1;
    for(let i=0;i<6;i++){
      const x=margin+Math.random()*(w-margin*2),y=margin+100+Math.random()*(h-margin*2-100);
      let minD=Infinity;
      targetsRef.current.forEach(t=>{const d=Math.hypot(t.x-x,t.y-y);if(d<minD)minD=d;});
      if(minD>bestD){bestD=minD;best={x,y};}
    }
    return best||{x:margin+Math.random()*(w-margin*2),y:130+Math.random()*(h-280)};
  },[]);

  // Power-ups
  const activatePowerUp=useCallback((x,y,ptype)=>{
    const gs=gsRef.current;if(!gs)return;
    sfx("powerUp");vibrate([10,30,10]);unlock("powerup_use");
    gs.sessionStats.powerupCollected=(gs.sessionStats.powerupCollected||0)+1;
    if(ptype==="LIFE"){
      if(gs.lives<MAX_LIVES)gs.lives++;
      spawnPopup(x,y,"+LIFE","#34d399",16);
    } else {
      const dur=ptype==="SLOW"?7000:ptype==="FREEZE"?5000:9000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!==ptype);
      activePwrRef.current.push({type:ptype,endsAt:Date.now()+dur});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,`+${ptype}`,"#60a5fa",15);
    }
    missionProg.current={...missionProg.current,powerupCollected:(missionProg.current.powerupCollected||0)+1};
  },[sfx,unlock,spawnPopup]);

  // Spawn target
  const spawnTarget=useCallback(()=>{
    const gs=gsRef.current,cfg=levelCfgRef.current;
    if(!gs||gs.lives<=0||!cfg)return;
    const {bombRate,movingRate,ghostRate,bossEnabled,bossRate,rarityBonus,modifier}=cfg;
    // Modifier overrides
    const effMoving=modifier?.type==="moving_only"?0.95:movingRate;
    const effGhost=modifier?.type==="ghost_rush"?0.7:ghostRate;
    const effBomb=modifier?.type==="no_miss"?0:bombRate;
    const r=Math.random();
    let type="normal",rarity=getRarity(rarityBonus),color,glow,moving=false,ghost=false;
    let pwrType=null,hitsLeft=1,maxHits=1,vx=0,vy=0;
    if(modifier?.type==="final_boss"){
      type="boss";color="#fbbf24";glow="#d97706";maxHits=10;hitsLeft=10;
    } else if(r<bossRate&&bossEnabled){
      type="boss";color="#ff6030";glow="#ff2000";maxHits=3;hitsLeft=3;
    } else if(r<(bossRate||0)+effBomb){
      type="bomb";color="#ef4444";glow="#dc2626";sfx("bombSpawn");
    } else if(r<(bossRate||0)+effBomb+0.07){
      type="powerup";color="#60a5fa";glow="#3b82f6";
      const pt=["SHIELD","SLOW","DOUBLE","LIFE","FREEZE"];
      pwrType=pt[Math.floor(Math.random()*pt.length)];
    } else {
      color=rarity.color;glow=rarity.glow;
      if(Math.random()<effMoving){
        moving=true;const a=Math.random()*Math.PI*2,sp=0.6+Math.random()*1.4;
        vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;
      }
      if(!moving&&Math.random()<effGhost)ghost=true;
    }
    const baseR=type==="boss"?BASE_R*2.4:type==="normal"?BASE_R*(rarity?.size||1):BASE_R;
    const pos=pickPos(baseR);
    let lifetime=cfg.targetLifetime;
    if(activePwrRef.current.some(p=>p.type==="SLOW"&&p.endsAt>Date.now()))lifetime*=1.6;
    if(activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>Date.now())){vx=0;vy=0;}
    targetsRef.current.push({
      id:Math.random().toString(36).slice(2),type,rarity:type==="normal"?rarity:null,
      x:pos.x,y:pos.y,radius:baseR,color,glow,lifetime,spawnedAt:Date.now(),born:performance.now(),
      moving,ghost,vx,vy,pwrType,hitsLeft,maxHits,trail:moving?[]:null,
    });
  },[sfx,pickPos]);

  // Level complete / game over
  const endLevel=useCallback((won)=>{
    const gs=gsRef.current;if(!gs)return;
    if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}
    const cfg=levelCfgRef.current;
    const sv=saveRef.current,score=gs.score;
    const timeSurvived=Math.floor((Date.now()-gs.startTime)/1000);
    updateMissions({...gs.sessionStats,timeSurvived,score,levelsCompleted:(missionProg.current.levelsCompleted||0)+(won?1:0)});

    if(won){
      sfx("levelComplete");vibrate([20,30,20,30,60]);
      // Stars
      const stars=score>=cfg.scoreGoal*3?3:score>=cfg.scoreGoal*1.8?2:1;
      const prev=sv.levelStars[cfg.id]||0;
      const newStars=Math.max(prev,stars);
      sv.levelStars={...sv.levelStars,[cfg.id]:newStars};
      // Unlock next
      if(cfg.id>=sv.unlockedLevel) sv.unlockedLevel=Math.min(100,cfg.id+1);
      // XP + coins
      const xpEarned=Math.floor(score/6)+gs.sessionStats.rareHits*8+gs.sessionStats.bossKills*30+(stars-1)*40;
      const coinsEarned=Math.floor(score*0.14)+gs.sessionStats.bossKills*20+stars*15;
      const prevLvl=getLvl(sv.xp);sv.xp+=xpEarned;
      if(getLvl(sv.xp)>prevLvl){sfx("levelUp");setNotif(`Level Up! Lv ${getLvl(sv.xp)} 🎉`);}
      sv.coins=(sv.coins||0)+coinsEarned;sv.totalCoins=(sv.totalCoins||0)+coinsEarned;
      if(score>sv.highScore)sv.highScore=score;
      sv.scores=[score,...sv.scores].slice(0,15).sort((a,b)=>b-a);
      if(gs.streak>sv.bestStreak)sv.bestStreak=gs.streak;
      if(stars===3&&cfg.isBoss)unlock("five_star");
      if(cfg.id>=10)unlock("level_10");if(cfg.id>=25)unlock("level_25");if(cfg.id>=50)unlock("level_50");if(cfg.id>=100)unlock("level_100");
      if(stars>=1)unlock("three_stars");
      flushSave();
      setLevelCompleteData({score,stars,newStars,xpEarned,coinsEarned,levelId:cfg.id,isLast:cfg.isLast,
        bestStreak:sv.bestStreak,sessionStats:{...gs.sessionStats,timeSurvived}});
      setScrollToLevel(cfg.id);
      setScreen("levelcomplete");
    } else {
      sfx("gameOver");
      flushSave();
      setGameOverData({score,levelId:cfg.id,levelName:cfg.name,scoreGoal:cfg.scoreGoal,
        sessionStats:{...gs.sessionStats,timeSurvived}});
      setScreen("gameover");
    }
    gsRef.current=null;targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];
    setActivePwrDisp([]);setFeverBorder(false);setComboLabel("");setPaused(false);pausedRef.current=false;
  },[sfx,flushSave,updateMissions,unlock]);

  // Tap handler
  const handleTap=useCallback((e)=>{
    e.preventDefault();
    const gs=gsRef.current;if(!gs||gs.lives<=0||pausedRef.current)return;
    const rect=e.currentTarget.getBoundingClientRect();
    const cx=e.touches?e.touches[0].clientX:e.clientX;
    const cy=e.touches?e.touches[0].clientY:e.clientY;
    const tx=cx-rect.left,ty=cy-rect.top;
    let hit=null,hitDist=Infinity;
    for(const t of targetsRef.current){
      if(t.ghost&&Math.sin(performance.now()/200)>0.25)continue;
      const d=Math.hypot(t.x-tx,t.y-ty);
      if(d<t.radius*1.35&&d<hitDist){hit=t;hitDist=d;}
    }
    ripplesRef.current.push({x:tx,y:ty,r:12,alpha:0.7,color:hit?(hit.color||"#a78bfa"):"#ffffff44"});
    if(!hit)return;

    // BOMB
    if(hit.type==="bomb"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      sfx("bombHit");vibrate(55);spawnParticles(hit.x,hit.y,"#ef4444",16,"spark");
      const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>Date.now());
      if(hasShield){
        activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");
        setActivePwrDisp([...activePwrRef.current]);
        spawnPopup(hit.x,hit.y,"SHIELD!","#60a5fa",17);vibrate([5,15,5]);
      } else {
        gs.lives=Math.max(0,gs.lives-1);gs.streak=0;
        spawnPopup(hit.x,hit.y,"BOOM!","#ef4444",19);
        setScreenShake(true);setTimeout(()=>setScreenShake(false),450);vibrate([45,20,45]);
        if(gs.lives<=0){endLevel(false);return;}
      }
      return;
    }
    // POWERUP
    if(hit.type==="powerup"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      activatePowerUp(hit.x,hit.y,hit.pwrType);sfx("coin");return;
    }
    // BOSS
    if(hit.type==="boss"){
      hit.hitsLeft--;sfx("bossHit");vibrate(22);spawnParticles(hit.x,hit.y,hit.color,10,"spark");
      if(hit.hitsLeft<=0){
        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
        sfx("bossKill");vibrate([35,20,35,20,60]);spawnParticles(hit.x,hit.y,hit.color,40,"spark");
        const pts=600*Math.min(10,1+Math.floor(gs.streak/5))*(gs.feverActive?2:1);
        gs.score+=pts;gs.sessionStats.bossKills=(gs.sessionStats.bossKills||0)+1;
        spawnPopup(hit.x,hit.y-20,`BOSS! +${pts}`,"#ff6030",21);
        unlock("boss_kill");
        // Check modifier goal
        const cfg=levelCfgRef.current;
        if(cfg?.modifier?.type==="boss_kill"&&gs.sessionStats.bossKills>=1&&gs.score>=cfg.scoreGoal){endLevel(true);return;}
        if(cfg?.modifier?.type==="final_boss"){endLevel(true);return;}
      }
      return;
    }
    // NORMAL
    targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
    gs.streak++;
    const combo=Math.min(10,1+Math.floor(gs.streak/5));
    const isDouble=activePwrRef.current.some(p=>p.type==="DOUBLE"&&p.endsAt>Date.now());
    const feverMult=gs.feverActive?2:1;
    const timeLeft=1-(Date.now()-hit.spawnedAt)/hit.lifetime;
    const isPerfect=hitDist<hit.radius*0.38&&timeLeft>0.36&&timeLeft<0.67;
    const pts=Math.round(hit.rarity.mult*combo*feverMult*(isDouble?2:1)*(isPerfect?1.5:1));
    gs.score+=pts;
    saveRef.current.coins=(saveRef.current.coins||0)+Math.max(1,Math.floor(pts*0.09));
    saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+Math.max(1,Math.floor(pts*0.09));
    gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
    if(hit.rarity.name!=="common")gs.sessionStats.rareHits++;
    if(gs.streak>gs.sessionStats.bestCombo)gs.sessionStats.bestCombo=gs.streak;
    if(isPerfect){gs.sessionStats.perfectTaps=(gs.sessionStats.perfectTaps||0)+1;}

    // SFX + particles
    if(hit.rarity.name==="legendary"){
      sfx("legendary");vibrate([30,15,30,15,60,15,90]);spawnParticles(hit.x,hit.y,hit.color,45,"spark");
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),650);unlock("legendary");
    } else if(hit.rarity.name==="epic"){
      sfx("epic");vibrate([22,30,22]);spawnParticles(hit.x,hit.y,hit.color,30,"spark");
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),420);unlock("first_epic");
    } else if(hit.rarity.name==="rare"){
      sfx("rare");vibrate([20,20]);spawnParticles(hit.x,hit.y,hit.color,18,"dot");unlock("first_rare");
    } else if(hit.rarity.name==="uncommon"){
      sfx("uncommon");vibrate(14);spawnParticles(hit.x,hit.y,hit.color,10,"dot");
    } else {
      sfx("tap");vibrate(8);spawnParticles(hit.x,hit.y,hit.color,7,"dot");
    }
    if(isPerfect){
      sfx("perfect");vibrate([8,8,8]);spawnPopup(hit.x,hit.y-22,"✨ PERFECT!","#fbbf24",18);
      setPerfectFlash(true);setTimeout(()=>setPerfectFlash(false),350);unlock("perfect_tap");
    } else if(hit.rarity.label){
      spawnPopup(hit.x,hit.y,hit.rarity.label,hit.color,14);
    }
    // Combo label
    const cl=COMBO_LABELS.find(([n])=>gs.streak>=n);
    if(cl){setComboLabel(cl[1]);clearTimeout(window.__clt);window.__clt=setTimeout(()=>setComboLabel(""),1300);}
    // Achievements
    unlock("first_tap");
    if(gs.streak>=10)unlock("streak_10");if(gs.streak>=25)unlock("streak_25");if(gs.streak>=50)unlock("streak_50");
    if(gs.score>=2000)unlock("score_2000");
    // Fever
    if(gs.streak>=FEVER_STREAK&&!gs.feverActive){
      gs.feverActive=true;gs.feverTimeLeft=FEVER_DUR;setFeverBorder(true);sfx("feverStart");vibrate([35,20,35,20,65]);
      spawnPopup(hit.x,hit.y-45,"🌡 FEVER!","#fbbf24",21);unlock("fever_mode");
      gs.sessionStats.feverCount=(gs.sessionStats.feverCount||0)+1;
    }
    // Check level win conditions
    const cfg=levelCfgRef.current;
    if(cfg){
      const scoreWin=gs.score>=cfg.scoreGoal;
      const modWin=!cfg.modifier||checkModGoal(cfg.modifier,gs);
      if(scoreWin&&modWin){endLevel(true);return;}
    }
    updateMissions({...gs.sessionStats,bestCombo:gs.streak});
    debounceSave();
  },[sfx,spawnParticles,spawnPopup,activatePowerUp,unlock,updateMissions,debounceSave,endLevel]);

  function checkModGoal(mod,gs){
    if(!mod)return true;
    switch(mod.type){
      case"boss_kill": return(gs.sessionStats.bossKills||0)>=1;
      case"combo_20":  return(gs.sessionStats.bestCombo||0)>=20;
      case"combo_40":  return(gs.sessionStats.bestCombo||0)>=40;
      case"fever_2":   return(gs.sessionStats.feverCount||0)>=2;
      case"fever_3":   return(gs.sessionStats.feverCount||0)>=3;
      case"no_miss":   return true; // enforced by losing life
      default: return true;
    }
  }

  // Countdown
  const runCountdown=useCallback((cb)=>{
    let n=3;
    const tick=()=>{
      setCountdownVal(n);sfx("countdown");
      if(n===0){setCountdownVal("GO!");sfx("go");setTimeout(()=>{setCountdownVal(null);cb();},600);return;}
      n--;setTimeout(tick,900);
    };
    tick();
  },[sfx]);

  // Start game
  const startGame=useCallback((levelId,shopCart=[])=>{
    const cfg=getLevelConfig(levelId);
    levelCfgRef.current=cfg;
    initMissions();
    targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];ripplesRef.current=[];
    spawnTimer.current=0;pausedRef.current=false;setPaused(false);

    const extraLife=shopCart.includes("extra_life");
    const headStart=shopCart.includes("head_start");
    const shieldStart=shopCart.includes("shield_start");
    const powerPack=shopCart.includes("power_pack");

    gsRef.current={
      score:headStart?300:0, lives:Math.min(MAX_LIVES,cfg.lives+(extraLife?1:0)),
      streak:0, feverActive:false, feverTimeLeft:0, startTime:Date.now(),
      sessionStats:{tapsTotal:0,rareHits:0,bestCombo:0,score:0,feverCount:0,powerupCollected:0,bossKills:0,perfectTaps:0},
    };
    if(shieldStart)activePwrRef.current=[{type:"SHIELD",endsAt:Date.now()+25000}];
    if(powerPack){const pt=["SLOW","DOUBLE","SHIELD","FREEZE"];const ty=pt[Math.floor(Math.random()*pt.length)];if(!activePwrRef.current.find(p=>p.type===ty))activePwrRef.current.push({type:ty,endsAt:Date.now()+12000});}
    setActivePwrDisp([...activePwrRef.current]);
    setHud({score:headStart?300:0,lives:gsRef.current.lives,streak:0,fever:false,coins:saveRef.current.coins,timeLeft:null,modGoal:cfg.modifier?.desc||null});
    setLevelCompleteData(null);setGameOverData(null);setEpicFlash(false);setFeverBorder(false);setComboLabel("");
    setCartItems([]);setScreen("playing");
    runCountdown(()=>{lastTickRef.current=performance.now();rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));});
  },[initMissions,runCountdown]); // eslint-disable-line

  // Pause
  const togglePause=useCallback(()=>{
    if(!gsRef.current)return;
    const next=!pausedRef.current;pausedRef.current=next;setPaused(next);
    if(!next){lastTickRef.current=performance.now();rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));}
  },[]);// eslint-disable-line

  useEffect(()=>()=>{if(rafRef.current)cancelAnimationFrame(rafRef.current);},[]);

  // Menu canvas loop
  useEffect(()=>{
    if(screen!=="menu"&&screen!=="levelmap"&&screen!=="shop"&&screen!=="levelcomplete"&&screen!=="gameover")return;
    let raf;
    const loop=(ts)=>{
      const canvas=canvasRef.current;if(!canvas)return;
      const ctx=canvas.getContext("2d");
      const th=THEMES.find(t=>t.id===(saveRef.current.themeId||"neon"))||THEMES[0];
      drawBg(ctx,canvas.width,canvas.height,th.accent,th.grid,ts,false);
      drawBgParticles(ctx,bgPartsRef.current,th.accent,false);
      drawRipples(ctx,ripplesRef.current);
      raf=requestAnimationFrame(loop);
    };
    raf=requestAnimationFrame(loop);return()=>cancelAnimationFrame(raf);
  },[screen]);

  // Game loop function (stored in ref to avoid stale closure issues)
  const gameLoopFn=useCallback((ts)=>{
    const gs=gsRef.current;
    if(!gs||pausedRef.current)return;
    const dt=Math.min(100,ts-lastTickRef.current);lastTickRef.current=ts;
    const canvas=canvasRef.current;if(!canvas)return;
    const ctx=canvas.getContext("2d");
    const w=canvas.width,h=canvas.height;
    const fever=gs.feverActive;
    const cfg=levelCfgRef.current;
    const th=THEMES.find(t=>t.id===(saveRef.current.themeId||"neon"))||THEMES[0];
    // Use world grid color when available
    const gridColor=cfg?WORLDS[cfg.world-1].grid:th.grid;
    const accentColor=cfg?WORLDS[cfg.world-1].color:th.accent;

    drawBg(ctx,w,h,accentColor,gridColor,ts,fever);
    drawBgParticles(ctx,bgPartsRef.current,accentColor,fever);
    drawRipples(ctx,ripplesRef.current);

    // Particles
    const pnow=performance.now();
    particlesRef.current=particlesRef.current.filter(p=>{
      const age=pnow-p.born;if(age>=p.duration)return false;
      if(p.type!=="shockwave"&&p.type!=="popup"){
        p.x+=p.vx*(p.type==="spark"?1:0.91);p.y+=p.vy*(p.type==="spark"?1:0.91);p.vy+=p.type==="spark"?0.22:0.12;
      }
      drawParticle(ctx,p,pnow);return true;
    });

    // Targets
    const now=Date.now();let lostLife=false;
    targetsRef.current=targetsRef.current.filter(t=>{
      // Move
      if(t.moving&&!activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>now)){
        t.x+=t.vx*dt*0.056;t.y+=t.vy*dt*0.056;
        const margin=t.radius+5;
        if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
        if(t.y<t.radius+95||t.y>h-margin){t.vy*=-1;t.y=Math.max(t.radius+95,Math.min(h-margin,t.y));}
        if(t.trail){t.trail.push({x:t.x,y:t.y});if(t.trail.length>12)t.trail.shift();}
      }
      // Expiry
      if((now-t.spawnedAt)>=t.lifetime){
        if(t.type==="powerup"||t.type==="bomb"||t.type==="boss")return false;
        const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
        if(hasShield){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
        else{
          gs.lives--;sfx("miss");vibrate(42);lostLife=true;
          gs.streak=0;
          // no_miss modifier: instant fail
          if(cfg?.modifier?.type==="no_miss"){endLevel(false);return false;}
        }
        return false;
      }
      drawTarget(ctx,t,ts);return true;
    });

    if(lostLife){if(gs.lives<=0){endLevel(false);return;}}

    // Expire power-ups
    const pl=activePwrRef.current.length;
    activePwrRef.current=activePwrRef.current.filter(p=>p.endsAt>now);
    if(activePwrRef.current.length!==pl)setActivePwrDisp([...activePwrRef.current]);

    // Fever
    if(gs.feverActive){gs.feverTimeLeft-=dt;if(gs.feverTimeLeft<=0){gs.feverActive=false;setFeverBorder(false);sfx("feverEnd");}}

    // Spawn
    spawnTimer.current+=dt;
    if(spawnTimer.current>=cfg.spawnInterval){spawnTimer.current=0;spawnTarget();}

    // HUD update 20fps
    if(ts-hudRef.current>50){
      hudRef.current=ts;
      setHud({score:gs.score,lives:gs.lives,streak:gs.streak,fever:gs.feverActive,coins:saveRef.current.coins,
        timeLeft:null,modGoal:cfg?.modifier?.desc||null});
    }

    rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));
  },[sfx,spawnTarget,endLevel]);// eslint-disable-line

  const sv=saveRef.current,lvl=getLvl(sv.xp);

  const streakColor=()=>{
    const s=hud.streak;
    if(s>=35)return"#ff00ff";if(s>=20)return"#ef4444";if(s>=10)return"#f97316";if(s>=5)return"#fbbf24";return"#ffffff";
  };


  // ═════════════════════════════════════════════════════════════
  // SCREEN RENDERERS
  // ═════════════════════════════════════════════════════════════

  // ── Menu ──
  const renderMenu=()=>(
    <div className="flex flex-col items-center justify-center h-full gap-4 px-5 relative z-10 pb-6">
      <div className="text-center">
        <h1 className="text-5xl font-black tracking-widest leading-none"
          style={{color:theme.accent,textShadow:`0 0 40px ${theme.accent},0 0 80px ${theme.accent}44`}}>
          NEXUS<span style={{color:"#f472b6",textShadow:"0 0 40px #f472b6"}}>TAP</span>
        </h1>
        <p className="text-xs mt-1 opacity-40 tracking-widest uppercase" style={{color:theme.accent}}>Ultimate Edition</p>
        <div className="mt-3 flex items-center gap-2 justify-center">
          <span className="text-xs font-bold px-2 py-0.5 rounded-full" style={{background:theme.accent+"22",color:theme.accent}}>LV {lvl}</span>
          <div className="w-28 h-1.5 rounded-full" style={{background:"#ffffff18"}}>
            <div className="h-full rounded-full" style={{width:`${(sv.xp%XP_PER_LVL)/XP_PER_LVL*100}%`,background:theme.accent,boxShadow:`0 0 8px ${theme.accent}`}}/>
          </div>
          <span className="text-xs opacity-35" style={{color:theme.accent}}>{xpToNext(sv.xp)}xp</span>
        </div>
      </div>
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:"#fbbf2415",border:"1px solid #fbbf2430"}}>
          <span>🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>{sv.coins||0}</span>
        </div>
        <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:theme.accent+"15",border:`1px solid ${theme.accent}30`}}>
          <span className="text-xs" style={{color:theme.accent}}>Day {sv.loginStreak||1} 🔥</span>
        </div>
      </div>
      <NeonButton onClick={()=>setScreen("levelmap")} className="w-full py-5 text-2xl"
        style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 32px ${theme.accent}66`}}>
        ▶ PLAY
      </NeonButton>
      <div className="grid grid-cols-2 gap-3 w-full">
        {[{label:"🎯 Daily Missions",sc:"missions"},{label:"🏆 Leaderboard",sc:"leaderboard"},{label:"🎖 Medals",sc:"achievements"},{label:"⚙ Settings",sc:"settings"}].map(b=>(
          <NeonButton key={b.sc} onClick={()=>setScreen(b.sc)} className="py-3 text-sm"
            style={{background:"#ffffff0d",border:`1px solid ${theme.accent}30`}}>{b.label}</NeonButton>
        ))}
      </div>
      {sv.highScore>0&&<p className="text-xs opacity-30" style={{color:theme.accent}}>Best: {sv.highScore.toLocaleString()}</p>}
    </div>
  );

  // ── Level Map ──
  const renderLevelMap=()=>{
    const unlockedTo=sv.unlockedLevel||1;
    // Zigzag column positions: 0=left(20%), 1=center(50%), 2=right(80%)
    const colX=(col,w)=>w*[0.16,0.5,0.84][col];
    const colPattern=[0,1,2,1,0,1,2,1,0,1]; // per position in world (0-9)
    return(
      <div className="flex flex-col h-full relative z-10">
        {/* Header */}
        <div className="flex items-center gap-3 px-4 py-3 z-10" style={{background:"rgba(0,0,0,0.6)",backdropFilter:"blur(6px)",borderBottom:`1px solid ${theme.accent}22`}}>
          <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Level Map</h2>
          <span className="ml-auto text-sm font-bold" style={{color:"#fbbf24"}}>🪙 {sv.coins||0}</span>
        </div>
        {/* Scrollable map */}
        <div className="flex-1 overflow-y-auto" style={{WebkitOverflowScrolling:"touch"}}>
          {WORLDS.map(world=>{
            const levelStart=(world.id-1)*10+1;
            const levels=ALL_LEVELS.slice(levelStart-1,levelStart+9);
            return(
              <div key={world.id} className="mb-2">
                {/* World banner */}
                <div className="flex items-center gap-3 px-4 py-3 mx-2 mt-3 rounded-2xl"
                  style={{background:`${world.color}18`,border:`1px solid ${world.color}44`,backdropFilter:"blur(4px)"}}>
                  <div className="w-3 h-3 rounded-full" style={{background:world.color,boxShadow:`0 0 10px ${world.color}`}}/>
                  <span className="font-black text-base" style={{color:world.color}}>World {world.id}: {world.name}</span>
                  <span className="ml-auto text-xs opacity-50" style={{color:world.color}}>
                    {levels.filter(l=>(sv.levelStars[l.id]||0)>0).length}/10
                  </span>
                </div>
                {/* Level nodes in zigzag */}
                <div className="relative" style={{height:levels.length*88+20}}>
                  {/* SVG connection lines */}
                  <svg className="absolute inset-0 pointer-events-none" width="100%" height="100%">
                    {levels.map((lv,i)=>{
                      if(i>=levels.length-1)return null;
                      const W=window.innerWidth;
                      const c1=colPattern[i],c2=colPattern[i+1];
                      const x1=colX(c1,W),y1=40+i*88;
                      const x2=colX(c2,W),y2=40+(i+1)*88;
                      const unlocked=(sv.levelStars[lv.id]||0)>0;
                      return<line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={unlocked?world.color+"66":"#ffffff15"} strokeWidth={unlocked?2.5:1.5} strokeDasharray={unlocked?"none":"6,4"}/>;
                    })}
                  </svg>
                  {/* Level nodes */}
                  {levels.map((lv,i)=>{
                    const W=window.innerWidth;
                    const col=colPattern[i];
                    const x=colX(col,W);
                    const y=40+i*88;
                    const stars=sv.levelStars[lv.id]||0;
                    const locked=lv.id>unlockedTo;
                    const isAvailable=lv.id===unlockedTo;
                    const isCurrent=lv.id===selectedLevel;
                    const nodeR=lv.isBoss?36:30;
                    return(
                      <div key={lv.id}
                        className="absolute flex flex-col items-center"
                        style={{left:x,top:y,transform:"translate(-50%,-50%)",width:88,cursor:locked?"default":"pointer"}}
                        onClick={()=>{if(!locked){setSelectedLevel(lv.id);setScreen("shop");}}}
                        onTouchEnd={e=>{e.preventDefault();if(!locked){setSelectedLevel(lv.id);setScreen("shop");}}}
                      >
                        {/* Node circle */}
                        <div className="flex items-center justify-center rounded-full font-black text-base transition-all"
                          style={{
                            width:nodeR*2,height:nodeR*2,
                            background:locked?"#1a1a2a":stars>0?`${world.color}33`:`${world.color}22`,
                            border:`${isCurrent||isAvailable?3:2}px solid ${locked?"#333":world.color}`,
                            boxShadow:isAvailable?`0 0 20px ${world.color}88`:stars===3?`0 0 14px ${world.color}66`:"none",
                            color:locked?"#444":world.color,
                            animation:isAvailable?"levelPulse 1.5s ease-in-out infinite":"none",
                            fontSize:lv.isBoss?18:14,
                          }}>
                          {locked?"🔒":stars>0&&lv.isBoss?"👑":lv.isBoss?"⚔":lv.id}
                        </div>
                        {/* Stars */}
                        <div className="flex gap-0.5 mt-1">
                          {[1,2,3].map(s=>(
                            <span key={s} style={{fontSize:9,opacity:stars>=s?1:0.15,color:"#fbbf24",
                              filter:stars>=s?"drop-shadow(0 0 3px #fbbf24)":"none"}}>★</span>
                          ))}
                        </div>
                        {/* Name (only available/current) */}
                        {(isAvailable||isCurrent)&&!locked&&(
                          <div className="text-center mt-0.5" style={{fontSize:9,color:world.color,opacity:0.8,maxWidth:80,lineHeight:1.2}}>
                            {lv.name}
                          </div>
                        )}
                      </div>
                    );
                  })}
                </div>
              </div>
            );
          })}
          <div style={{height:60}}/>
        </div>
      </div>
    );
  };

  // ── Shop ──
  const renderShop=()=>{
    const cfg=getLevelConfig(selectedLevel);
    const coins=sv.coins||0;
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <NeonButton onClick={()=>setScreen("levelmap")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Map</NeonButton>
            <div>
              <div className="font-black text-base" style={{color:cfg.worldColor}}>Level {cfg.id}</div>
              <div className="text-xs opacity-60" style={{color:cfg.worldColor}}>{cfg.name}</div>
            </div>
          </div>
          <div className="flex items-center gap-1 px-3 py-1 rounded-full" style={{background:"#fbbf2415"}}>
            <span>🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>{coins}</span>
          </div>
        </div>
        {/* Level info */}
        <div className="rounded-2xl p-4" style={{background:`${cfg.worldColor}12`,border:`1px solid ${cfg.worldColor}44`}}>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-bold" style={{color:cfg.worldColor}}>Goal: {cfg.scoreGoal.toLocaleString()} pts</span>
            <div className="flex gap-0.5">{[1,2,3].map(s=><span key={s} style={{fontSize:12,opacity:(sv.levelStars[cfg.id]||0)>=s?1:0.2,color:"#fbbf24"}}>★</span>)}</div>
          </div>
          <div className="flex gap-4 text-xs opacity-60" style={{color:cfg.worldColor}}>
            <span>❤️ {cfg.lives} lives</span>
            {cfg.modifier&&<span className="font-bold" style={{color:"#fbbf24"}}>⚡ {cfg.modifier.desc}</span>}
          </div>
        </div>
        <p className="text-xs opacity-40 uppercase tracking-widest" style={{color:cfg.worldColor}}>Optional Boosts</p>
        {SHOP_ITEMS.map(item=>{
          const inCart=cartItems.includes(item.id),canBuy=coins>=item.cost||inCart;
          return(
            <div key={item.id} className="rounded-2xl p-3 flex items-center gap-3"
              style={{background:inCart?`${cfg.worldColor}18`:"#ffffff08",border:`1px solid ${inCart?cfg.worldColor:"#ffffff15"}`}}>
              <span className="text-2xl">{item.icon}</span>
              <div className="flex-1">
                <div className="font-bold text-sm" style={{color:inCart?cfg.worldColor:"#fff"}}>{item.name}</div>
                <div className="text-xs opacity-50">{item.desc}</div>
              </div>
              <NeonButton onClick={()=>{
                if(inCart){setCartItems(c=>c.filter(i=>i!==item.id));}
                else if(coins>=item.cost){setCartItems(c=>[...c,item.id]);}
              }} className="px-3 py-2 text-xs"
                style={{background:inCart?`${cfg.worldColor}33`:"#ffffff0d",border:`1px solid ${inCart?cfg.worldColor:"#ffffff22"}`,
                  color:inCart?cfg.worldColor:canBuy?"#fff":"#444"}}>
                {inCart?"✓":canBuy?`🪙${item.cost}`:`🔒${item.cost}`}
              </NeonButton>
            </div>
          );
        })}
        <NeonButton onClick={()=>{
          const total=cartItems.reduce((s,id)=>s+(SHOP_ITEMS.find(i=>i.id===id)?.cost||0),0);
          if(sv.coins<total){setNotif("Not enough coins! 🪙");return;}
          sv.coins-=total;flushSave();startGame(selectedLevel,cartItems);
        }} className="w-full py-4 text-xl mt-1"
          style={{background:`linear-gradient(135deg,${cfg.worldColor}88,${cfg.worldColor})`,boxShadow:`0 0 28px ${cfg.worldColor}55`}}>
          {cartItems.length>0?`▶ START (${cartItems.reduce((s,id)=>s+(SHOP_ITEMS.find(i=>i.id===id)?.cost||0),0)}🪙)`:"▶ START FREE"}
        </NeonButton>
      </div>
    );
  };

  // ── Playing overlay ──
  const renderPlaying=()=>{
    const cfg=levelCfgRef.current;
    const wc=cfg?WORLDS[cfg.world-1].color:theme.accent;
    return(
      <div className="absolute inset-0" onTouchStart={handleTap} onClick={handleTap} style={{touchAction:"none",zIndex:10}}>
        {/* HUD */}
        <div className="absolute top-0 left-0 right-0 z-20 flex items-stretch"
          style={{background:"rgba(0,0,0,0.62)",backdropFilter:"blur(6px)",borderBottom:`1px solid ${wc}22`}}>
          <div className="flex-1 flex flex-col items-center justify-center py-2 px-1">
            <div className="text-xs opacity-35 tracking-widest uppercase" style={{color:wc}}>Score</div>
            <div className="text-xl font-black tabular-nums" style={{color:wc}}>{hud.score.toLocaleString()}</div>
            {cfg&&<div className="text-xs opacity-40 tabular-nums" style={{color:wc}}>/{cfg.scoreGoal.toLocaleString()}</div>}
          </div>
          <div className="flex flex-col items-center justify-center px-2 py-1.5 gap-1">
            <div className="flex gap-0.5">{Array.from({length:MAX_LIVES},(_,i)=><span key={i} style={{fontSize:13,opacity:i<hud.lives?1:0.18}}>{i<hud.lives?"❤️":"🖤"}</span>)}</div>
            {cfg&&<div className="text-xs font-bold px-1.5 py-0.5 rounded-full" style={{background:wc+"22",color:wc}}>W{cfg.world} L{cfg.id}</div>}
          </div>
          <div className="flex-1 flex flex-col items-center justify-center py-2 px-1">
            <div className="text-xs opacity-35 tracking-widest uppercase" style={{color:wc}}>Streak</div>
            <div className="text-xl font-black tabular-nums"
              style={{color:streakColor(),textShadow:hud.streak>=5?`0 0 14px ${streakColor()}`:"none"}}>
              {hud.streak}×
            </div>
          </div>
          <button onTouchStart={e=>{e.stopPropagation();togglePause();}} onClick={e=>{e.stopPropagation();togglePause();}}
            className="flex items-center justify-center px-4"
            style={{color:wc,fontSize:18,background:"transparent",border:"none",WebkitTapHighlightColor:"transparent"}}>
            {paused?"▶":"⏸"}
          </button>
        </div>
        {/* Modifier goal hint */}
        {hud.modGoal&&(
          <div className="absolute left-0 right-0 flex justify-center z-20" style={{top:76}}>
            <div className="px-3 py-1 rounded-xl text-xs font-bold" style={{background:"#fbbf2420",border:"1px solid #fbbf2444",color:"#fbbf24"}}>
              ⚡ {hud.modGoal}
            </div>
          </div>
        )}
        {/* Power-ups */}
        {activePwrDisp.length>0&&(
          <div className="absolute left-0 right-0 flex justify-center gap-2 z-20" style={{top:hud.modGoal?108:76}}>
            {activePwrDisp.map(p=>(
              <div key={p.type} className="px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1"
                style={{background:"#1e3a8acc",border:"1px solid #60a5fa55",color:"#60a5fa"}}>
                {p.type==="SHIELD"?"🛡":p.type==="SLOW"?"🐢":p.type==="DOUBLE"?"×2":p.type==="FREEZE"?"❄️":"❤️"}
                {" "}{p.type}{" "}<span className="opacity-50">{Math.max(0,Math.ceil((p.endsAt-Date.now())/1000))}s</span>
              </div>
            ))}
          </div>
        )}
        {/* Fever */}
        {feverBorder&&<div className="absolute inset-0 pointer-events-none z-10" style={{border:"4px solid #fbbf24",boxShadow:"inset 0 0 60px #fbbf2445,0 0 60px #fbbf2445",animation:"feverPulse 0.6s ease-in-out infinite alternate"}}/>}
        {feverBorder&&<div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:140}}>
          <span className="font-black text-base px-4 py-1 rounded-full" style={{color:"#fbbf24",textShadow:"0 0 20px #fbbf24",background:"#fbbf2420",animation:"feverPulse 0.5s infinite alternate"}}>🌡 FEVER!</span>
        </div>}
        {epicFlash&&<div className="absolute inset-0 pointer-events-none z-10" style={{background:"#f472b633",animation:"epicFlash 0.5s ease-out forwards"}}/>}
        {perfectFlash&&<div className="absolute inset-0 pointer-events-none z-10" style={{background:"#fbbf2422",animation:"epicFlash 0.35s ease-out forwards"}}/>}
        {comboLabel&&(
          <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:"40%",transform:"translateY(-50%)"}}>
            <div className="font-black text-2xl px-6 py-2 rounded-2xl"
              style={{color:"#fff",textShadow:`0 0 30px ${theme.accent}`,background:theme.accent+"22",border:`2px solid ${theme.accent}`,animation:"comboAnnounce 0.3s ease-out"}}>
              {comboLabel}
            </div>
          </div>
        )}
        {/* Score progress bar */}
        {cfg&&(
          <div className="absolute bottom-0 left-0 right-0 z-20" style={{height:4,background:"#ffffff10"}}>
            <div className="h-full transition-all duration-300"
              style={{width:`${Math.min(100,hud.score/cfg.scoreGoal*100)}%`,background:wc,boxShadow:`0 0 8px ${wc}`}}/>
          </div>
        )}
        {countdownVal!==null&&(
          <div className="absolute inset-0 flex items-center justify-center z-50 pointer-events-none" style={{background:"rgba(0,0,0,0.55)"}}>
            <div className="font-black text-9xl" key={countdownVal}
              style={{color:countdownVal==="GO!"?"#34d399":wc,textShadow:`0 0 70px ${countdownVal==="GO!"?"#34d399":wc}`,animation:"countAnim 0.5s ease-out"}}>
              {countdownVal}
            </div>
          </div>
        )}
        {paused&&(
          <div className="absolute inset-0 flex flex-col items-center justify-center z-50" style={{background:"rgba(0,0,0,0.8)",backdropFilter:"blur(10px)"}}>
            <div className="text-4xl font-black mb-6" style={{color:wc}}>PAUSED</div>
            <NeonButton onClick={togglePause} className="w-48 py-4 text-lg mb-3"
              style={{background:`linear-gradient(135deg,${theme.secondary},${wc})`,boxShadow:`0 0 24px ${wc}55`}}>▶ RESUME</NeonButton>
            <NeonButton onClick={()=>{if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}gsRef.current=null;targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];setActivePwrDisp([]);setFeverBorder(false);setPaused(false);pausedRef.current=false;setScreen("levelmap");}}
              className="w-48 py-3" style={{background:"#ffffff10",border:`1px solid ${wc}44`}}>✕ QUIT</NeonButton>
          </div>
        )}
      </div>
    );
  };

  // ── Level Complete ──
  const renderLevelComplete=()=>{
    if(!levelCompleteData)return null;
    const{score,stars,newStars,xpEarned,coinsEarned,levelId,isLast,sessionStats}=levelCompleteData;
    const cfg=getLevelConfig(levelId);
    return(
      <div className="flex flex-col items-center h-full overflow-y-auto px-5 py-6 gap-4 relative z-10">
        <div className="text-center">
          <div className="text-sm uppercase tracking-widest opacity-50 mb-1" style={{color:cfg.worldColor}}>Level {cfg.id} Complete!</div>
          <div className="text-2xl font-black mb-3" style={{color:cfg.worldColor}}>{cfg.name}</div>
          <div className="flex justify-center gap-2 mb-1">
            {[1,2,3].map(s=>(
              <span key={s} className="transition-all" style={{fontSize:s<=stars?44:28,opacity:s<=stars?1:0.15,
                filter:s<=stars?"drop-shadow(0 0 12px #fbbf24)":"none",animation:s<=stars?`starPop ${0.3+s*0.2}s ease-out`:"none"}}>⭐</span>
            ))}
          </div>
          {newStars>stars&&<div className="text-xs opacity-60" style={{color:"#fbbf24"}}>Best: {newStars}★</div>}
        </div>
        <div className="text-4xl font-black tabular-nums" style={{color:cfg.worldColor}}>{score.toLocaleString()}</div>
        <div className="flex gap-3">
          <div className="px-3 py-1.5 rounded-xl flex items-center gap-1.5" style={{background:"#ffffff08",border:`1px solid ${cfg.worldColor}33`}}>
            <span className="text-sm">✨</span><span className="font-bold text-sm" style={{color:cfg.worldColor}}>+{xpEarned} XP</span>
          </div>
          <div className="px-3 py-1.5 rounded-xl flex items-center gap-1.5" style={{background:"#fbbf2415",border:"1px solid #fbbf2435"}}>
            <span className="text-sm">🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>+{coinsEarned}</span>
          </div>
        </div>
        <div className="w-full rounded-2xl p-4 grid grid-cols-3 gap-3" style={{background:"#ffffff06",border:`1px solid ${cfg.worldColor}28`}}>
          {[["Hits",sessionStats.tapsTotal],["Rare+",sessionStats.rareHits],["Streak",sv.bestStreak+"×"],
            ["Bosses",sessionStats.bossKills||0],["Perfect",sessionStats.perfectTaps||0],["Fever",sessionStats.feverCount||0]
          ].map(([l,v])=>(
            <div key={l} className="text-center">
              <div className="text-xs opacity-35 uppercase mb-0.5" style={{color:cfg.worldColor}}>{l}</div>
              <div className="font-bold text-sm" style={{color:cfg.worldColor}}>{v}</div>
            </div>
          ))}
        </div>
        {!isLast&&(
          <NeonButton onClick={()=>{setSelectedLevel(levelId+1);setCartItems([]);setScreen("shop");}}
            className="w-full py-4 text-xl"
            style={{background:`linear-gradient(135deg,${cfg.worldColor}88,${cfg.worldColor})`,boxShadow:`0 0 28px ${cfg.worldColor}55`}}>
            Next Level →
          </NeonButton>
        )}
        {isLast&&<div className="text-center font-black text-xl" style={{color:"#fbbf24",textShadow:"0 0 30px #fbbf24"}}>🏆 YOU BEAT ALL 100 LEVELS! 🏆</div>}
        <NeonButton onClick={()=>{setScrollToLevel(levelId);setScreen("levelmap");}}
          className="w-full py-3" style={{background:"#ffffff0d",border:`1px solid ${cfg.worldColor}33`}}>← Level Map</NeonButton>
      </div>
    );
  };

  // ── Game Over ──
  const renderGameOver=()=>{
    if(!gameOverData)return null;
    const{score,levelId,levelName,scoreGoal,sessionStats}=gameOverData;
    const cfg=getLevelConfig(levelId);
    const pct=Math.min(100,Math.round(score/scoreGoal*100));
    return(
      <div className="flex flex-col items-center h-full overflow-y-auto px-5 py-6 gap-4 relative z-10">
        <div className="text-center">
          <div className="text-4xl mb-1">💀</div>
          <div className="text-sm uppercase tracking-widest opacity-50 mb-1" style={{color:cfg.worldColor}}>Level {levelId} Failed</div>
          <div className="text-xl font-black" style={{color:cfg.worldColor}}>{levelName}</div>
        </div>
        <div className="text-4xl font-black tabular-nums" style={{color:cfg.worldColor}}>{score.toLocaleString()}</div>
        <div className="w-full rounded-xl p-3" style={{background:"#ffffff08",border:`1px solid ${cfg.worldColor}33`}}>
          <div className="flex justify-between text-xs mb-2 opacity-50" style={{color:cfg.worldColor}}>
            <span>Progress to goal</span><span>{pct}%</span>
          </div>
          <div className="h-3 rounded-full" style={{background:"#ffffff15"}}>
            <div className="h-full rounded-full transition-all" style={{width:`${pct}%`,background:cfg.worldColor,boxShadow:`0 0 8px ${cfg.worldColor}`}}/>
          </div>
        </div>
        <div className="w-full rounded-2xl p-4 grid grid-cols-3 gap-3" style={{background:"#ffffff06",border:`1px solid ${cfg.worldColor}28`}}>
          {[["Hits",sessionStats.tapsTotal],["Rare+",sessionStats.rareHits],["Streak",sessionStats.bestCombo+"×"],
            ["Bosses",sessionStats.bossKills||0],["Perfect",sessionStats.perfectTaps||0],["Time",sessionStats.timeSurvived+"s"]
          ].map(([l,v])=>(
            <div key={l} className="text-center">
              <div className="text-xs opacity-35 uppercase mb-0.5" style={{color:cfg.worldColor}}>{l}</div>
              <div className="font-bold text-sm" style={{color:cfg.worldColor}}>{v}</div>
            </div>
          ))}
        </div>
        <NeonButton onClick={()=>{setSelectedLevel(levelId);setCartItems([]);setScreen("shop");}}
          className="w-full py-4 text-xl"
          style={{background:`linear-gradient(135deg,${cfg.worldColor}88,${cfg.worldColor})`,boxShadow:`0 0 24px ${cfg.worldColor}55`}}>
          🔄 RETRY
        </NeonButton>
        <NeonButton onClick={()=>setScreen("levelmap")} className="w-full py-3"
          style={{background:"#ffffff0d",border:`1px solid ${cfg.worldColor}33`}}>← Level Map</NeonButton>
      </div>
    );
  };

  // ── Missions ──
  const renderMissions=()=>{
    const missions=getDailyMissions(),prog=sv.missionProgress||{};
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Daily Missions</h2>
          {sv.missionCompleted&&<span className="text-xs px-2 py-1 rounded-full font-bold" style={{background:"#34d39922",color:"#34d399"}}>DONE ✓</span>}
        </div>
        <p className="text-xs opacity-40 -mt-2" style={{color:theme.accent}}>Complete all 3 for +200 XP bonus</p>
        {missions.map(m=>{
          const cur=Math.min(prog[m.id]||0,m.goal),pct=cur/m.goal*100,done=cur>=m.goal;
          return(
            <div key={m.id} className="rounded-2xl p-4" style={{background:done?`${theme.accent}18`:"#ffffff07",border:`1px solid ${done?theme.accent+"55":"#ffffff12"}`}}>
              <div className="flex justify-between items-center mb-2">
                <span className="font-bold text-sm" style={{color:done?theme.accent:"#e2e8f0"}}>{done?"✓ ":""}{m.desc}</span>
                <span className="text-xs opacity-50 tabular-nums" style={{color:theme.accent}}>{cur}/{m.goal}</span>
              </div>
              <div className="h-2.5 rounded-full" style={{background:"#ffffff15"}}>
                <div className="h-full rounded-full transition-all duration-500" style={{width:`${pct}%`,background:done?theme.accent:`${theme.accent}88`,boxShadow:done?`0 0 8px ${theme.accent}`:""}}/>
              </div>
            </div>
          );
        })}
        {sv.missionCompleted&&<div className="text-center font-bold py-2" style={{color:"#fbbf24"}}>🏆 All complete! +200 XP</div>}
      </div>
    );
  };

  // ── Achievements ──
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
              style={{background:unlocked?`${theme.accent}18`:"#ffffff05",border:`1px solid ${unlocked?theme.accent+"55":"#ffffff10"}`,opacity:unlocked?1:0.4}}>
              <div className="text-2xl mb-1" style={{filter:unlocked?`drop-shadow(0 0 6px ${theme.accent})`:"none"}}>{a.icon}</div>
              <div className="text-xs font-bold mb-0.5" style={{color:unlocked?theme.accent:"#ccc"}}>{a.label}</div>
              <div className="text-xs opacity-50" style={{color:unlocked?theme.accent:"#888"}}>{a.desc}</div>
              {unlocked&&<div className="text-xs opacity-55 mt-0.5" style={{color:theme.accent}}>+{a.xp}xp</div>}
            </div>
          );
        })}
      </div>
    </div>
  );

  // ── Leaderboard ──
  const renderLeaderboard=()=>{
    const all=[...sv.scores].sort((a,b)=>b-a).slice(0,10);
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Best Scores</h2>
        </div>
        {all.length===0
          ?<p className="text-center opacity-40 mt-8" style={{color:theme.accent}}>No scores yet!</p>
          :all.map((s,i)=>(
            <div key={i} className="flex items-center justify-between px-4 py-3 rounded-2xl"
              style={{background:i===0?`${theme.accent}18`:"#ffffff05",border:`1px solid ${i<3?theme.accent+"44":"#ffffff0d"}`}}>
              <span className="font-black text-xl" style={{color:i===0?"#fbbf24":i===1?"#d1d5db":i===2?"#d97706":theme.accent,minWidth:32}}>
                {i===0?"🥇":i===1?"🥈":i===2?"🥉":`#${i+1}`}
              </span>
              <span className="font-bold text-xl tabular-nums" style={{color:theme.accent}}>{s.toLocaleString()}</span>
            </div>
          ))
        }
        <div className="mt-2 p-4 rounded-2xl text-center" style={{background:"#ffffff06",border:`1px solid ${theme.accent}22`}}>
          <div className="text-xs opacity-40 mb-1" style={{color:theme.accent}}>Level Progress</div>
          <div className="text-2xl font-black" style={{color:theme.accent}}>{sv.unlockedLevel||1}<span className="text-sm opacity-50">/100</span></div>
          <div className="text-xs opacity-40 mt-1" style={{color:theme.accent}}>levels unlocked</div>
        </div>
      </div>
    );
  };

  // ── Settings ──
  const renderSettings=()=>(
    <div className="flex flex-col h-full px-4 py-5 gap-5 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={()=>setScreen("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{color:theme.accent}}>Settings</h2>
      </div>
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Sound</p>
        <NeonButton onClick={()=>{const n=!soundOn;setSoundOn(n);sv.soundEnabled=n;debounceSave();}}
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
                onClick={()=>{setTheme(th);sv.themeId=th.id;debounceSave();}}
                className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{background:theme.id===th.id?`${th.accent}20`:"#ffffff06",border:`1px solid ${theme.id===th.id?th.accent:"#ffffff10"}`}}>
                <div className="flex items-center gap-3">
                  <div className="w-4 h-4 rounded-full" style={{background:th.accent,boxShadow:`0 0 8px ${th.accent}`}}/>
                  <span style={{color:locked?"#444":th.accent}}>{th.name}</span>
                </div>
                {locked?<span className="text-xs opacity-30">Lv{th.unlockLevel}</span>:theme.id===th.id?<span style={{color:th.accent}}>✓</span>:null}
              </NeonButton>
            );
          })}
        </div>
      </div>
      <div className="border-t border-white border-opacity-10 pt-4">
        <NeonButton onClick={()=>{if(window.confirm("Reset ALL progress? Cannot be undone.")){saveRef.current={...DEFAULT_SAVE};flushSave();setTheme(THEMES[0]);setSoundOn(true);setScreen("menu");}}}
          className="w-full py-3 text-sm" style={{background:"#ef444418",border:"1px solid #ef444455",color:"#ef4444"}}>
          Reset All Progress
        </NeonButton>
      </div>
    </div>
  );

  // ═════════════════════════════════════════════════════════════
  // MAIN RENDER
  // ═════════════════════════════════════════════════════════════
  const activeWorldColor = levelCfgRef.current ? WORLDS[levelCfgRef.current.world-1].color : theme.accent;
  return(
    <div className="relative w-full h-screen overflow-hidden select-none"
      style={{background:theme.bg,fontFamily:"'Segoe UI',system-ui,sans-serif",
        transform:screenShake?`translate(${(Math.random()>0.5?1:-1)*5}px,${(Math.random()>0.5?1:-1)*3}px)`:"none",
        transition:screenShake?"none":"transform 0.04s ease"}}>

      <style>{`
        @keyframes feverPulse{from{opacity:.6}to{opacity:1}}
        @keyframes epicFlash{from{opacity:1}to{opacity:0}}
        @keyframes comboAnnounce{0%{transform:scale(.5);opacity:0}60%{transform:scale(1.15)}100%{transform:scale(1);opacity:1}}
        @keyframes countAnim{0%{transform:scale(2);opacity:0}50%{transform:scale(1);opacity:1}100%{transform:scale(.8);opacity:0}}
        @keyframes levelPulse{0%,100%{box-shadow:0 0 12px var(--wc,#a78bfa)}50%{box-shadow:0 0 28px var(--wc,#a78bfa)}}
        @keyframes starPop{0%{transform:scale(0) rotate(-30deg);opacity:0}70%{transform:scale(1.3) rotate(8deg)}100%{transform:scale(1) rotate(0);opacity:1}}
        @keyframes waveIn{0%{transform:scale(.6) translateY(-20px);opacity:0}70%{transform:scale(1.05)}100%{transform:scale(1);opacity:1}}
        *{-webkit-tap-highlight-color:transparent;box-sizing:border-box}
        ::-webkit-scrollbar{width:0}
      `}</style>

      <canvas ref={canvasRef} className="absolute inset-0 z-0" style={{width:"100%",height:"100%",pointerEvents:"none"}}/>

      {notif&&(
        <div className="absolute top-4 left-1/2 z-50 px-4 py-2 rounded-xl text-sm font-bold pointer-events-none"
          style={{transform:"translateX(-50%)",background:"#000000ee",border:`1px solid ${activeWorldColor}`,color:activeWorldColor,
            boxShadow:`0 0 24px ${activeWorldColor}44`,maxWidth:"85vw",whiteSpace:"nowrap",textAlign:"center"}}>
          {notif}
        </div>
      )}

      {screen==="menu"          &&renderMenu()}
      {screen==="levelmap"      &&renderLevelMap()}
      {screen==="shop"          &&renderShop()}
      {screen==="playing"       &&renderPlaying()}
      {screen==="levelcomplete" &&renderLevelComplete()}
      {screen==="gameover"      &&renderGameOver()}
      {screen==="missions"      &&renderMissions()}
      {screen==="achievements"  &&renderAchievements()}
      {screen==="leaderboard"   &&renderLeaderboard()}
      {screen==="settings"      &&renderSettings()}
    </div>
  );
}
