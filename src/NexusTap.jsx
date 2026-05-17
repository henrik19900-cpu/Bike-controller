import React, { useState, useEffect, useRef, useCallback, useLayoutEffect } from "react";
import { flushSync } from "react-dom";
import gsap from "gsap";

// ═══════════════════════════════════════════════════════════════
// WORLD & LEVEL DEFINITIONS
// ═══════════════════════════════════════════════════════════════
const WORLDS = [
  { id:1,  name:"Dragon's Lair",    emoji:"🐉", color:"#ff6b35", bg:"#1a0500", grid:"rgba(255,107,53,0.08)",    accent:"#c13b00", atmos:"cave"   },
  { id:2,  name:"Troll Forest",     emoji:"🌿", color:"#4ecb71", bg:"#021408", grid:"rgba(78,203,113,0.08)",    accent:"#1e7a3a", atmos:"forest" },
  { id:3,  name:"Elven Kingdom",    emoji:"✨", color:"#e8c84e", bg:"#080a02", grid:"rgba(232,200,78,0.07)",    accent:"#9a8020", atmos:"magic"  },
  { id:4,  name:"Magic Tower",      emoji:"🔮", color:"#b06de8", bg:"#0a0218", grid:"rgba(176,109,232,0.08)",   accent:"#7a3ab0", atmos:"arcane" },
  { id:5,  name:"Viking Fjords",    emoji:"❄️", color:"#6ec0f5", bg:"#020c1c", grid:"rgba(110,192,245,0.07)",   accent:"#1e66a0", atmos:"frost"  },
  { id:6,  name:"Goblin Mines",     emoji:"⛏️", color:"#f5d240", bg:"#100900", grid:"rgba(245,210,64,0.07)",    accent:"#c09010", atmos:"mine"   },
  { id:7,  name:"Haunted Castle",   emoji:"👻", color:"#9be09b", bg:"#020a04", grid:"rgba(155,224,155,0.07)",   accent:"#3a8a40", atmos:"undead" },
  { id:8,  name:"Ocean Deep",       emoji:"🌊", color:"#22d4b4", bg:"#010c0a", grid:"rgba(34,212,180,0.07)",    accent:"#0e9078", atmos:"ocean"  },
  { id:9,  name:"Giant's Peak",     emoji:"⛰️", color:"#c8d0da", bg:"#060808", grid:"rgba(200,208,218,0.07)",   accent:"#6a7880", atmos:"storm"  },
  { id:10, name:"Rainbow Dragon",   emoji:"🌈", color:"#ffd700", bg:"#120800", grid:"rgba(255,215,0,0.08)",     accent:"#c8a000", atmos:"divine" },
];

// ═══════════════════════════════════════════════════════════════
// MASCOTS — 10 animal companions, each with unique dance
// ═══════════════════════════════════════════════════════════════
const MASCOTS = [
  // ── STARTER ──────────────────────────────────────────────────
  { id:"dragon",    name:"Pip",     color:"#ff8c5a", rarity:"starter",
    e:{idle:"🐲",happy:"🐲",excited:"✨",fire:"🌟",fever:"💛",sad:"🥹",victory:"🥳",scared:"🫣"},
    dance:"danceDragon", catchphrase:"Small dragon, BIG heart! 🐲💕",
    speeches:{
      idle:["Pip is ready! 🐲","You've got this, I believe in you! 💕","Let's do this together! 🌟"],
      happy:["Yay yay yay!! 🐲✨","Pip is SO happy right now! 💛","You're incredible! 🥳"],
      streak:["Streak streak!! 🌟🌟","Pip can't believe how good you are!! 🐲","We're AMAZING together!! ✨"],
      fever:["FEVER TIME!! Pip is glowing!! 💛💛","Best adventure EVER!! 🐲✨"],
      close:["Almost! Don't give up! 🐲","You can do it, I know it! 💕"],
      miss:["It's okay, try again! 🐲💕","Pip still believes in you! 🌟"],
      victory:["WE DID IT!! 🥳","Pip is SO proud of you!! 🐲💕"],
      bonus:["Oh wow FREE bonus!! 🐲✨","Pip is bouncing with joy!! 💛"],
      mystery:["Ooh what could it be?! 🐲🎁","A surprise! Pip loves surprises!! ✨"],
    }},
  { id:"fox",       name:"Rusty",   color:"#e07030", rarity:"starter",
    e:{idle:"🦊",happy:"🦊",excited:"🌟",fire:"✨",fever:"🌸",sad:"🥺",victory:"🎉",scared:"🫣"},
    dance:"danceFox",    catchphrase:"Foxy and clever — that's us! 🦊",
    speeches:{
      idle:["Heyyy! Ready to play? 🦊","You're so good at this! 🌟","Let's go on an adventure! 🦊"],
      happy:["Foxy loves this!! 🦊","Oh yes oh yes!! ✨","You clever, wonderful person! 🌟"],
      streak:["Sneaky streak!! 🦊🌟","Rusty can't keep up with you!! 💨","So fast and smart!! 🌸"],
      fever:["Fox fever!! Woohoo!! 🌸🌸","You're unstoppable!! 🦊"],
      close:["Sooo close! You've got it! 🦊","Almost there! Rusty believes! 🌟"],
      miss:["Aw, you'll get it next time! 🦊","Rusty has faith in you! 💕"],
      victory:["Fox and friend WIN!! 🦊🎉","Best team ever!! 🌟"],
      bonus:["Oh oh oh, bonus time!! 🦊","Free round! Rusty is dancing!! 🌸"],
      mystery:["Ooh a mystery! How exciting!! 🦊🎁","What could it be?! 👀"],
    }},
  // ── COMMON ───────────────────────────────────────────────────
  { id:"frog",      name:"Hoppy",   color:"#4ecb71", rarity:"common",
    unlockCond:{type:"level",value:3}, unlockHint:"Complete Level 3",
    e:{idle:"🐸",happy:"🐸",excited:"💚",fire:"🌿",fever:"🌼",sad:"🥺",victory:"🎊",scared:"🫣"},
    dance:"danceFrog",   catchphrase:"Every hop counts! 🐸💚",
    speeches:{
      idle:["Ribbit! Let's go! 🐸","Hoppy is SO excited! 💚","Boing boing! Ready! 🐸"],
      happy:["Hop hop hooray!! 🐸","Ribbit of joy!! 💚","Best day ever! 🌿"],
      streak:["Hopping streak!! 🐸💚","Frog power activated!! 🌼","Can't stop won't stop! 🐸"],
      fever:["Frog fever!! Hop hop hop!! 💚💚","Lily pad to the stars!! 🐸"],
      close:["So close! One more hop! 🐸","Almost! Hoppy believes! 💚"],
      miss:["Oopsie! Ribbit... 🥺","Frogs always bounce back! 🐸💕"],
      victory:["Frog wins!! Ribbit ribbit!! 🎊","Best hop ever!! 🐸💚"],
      bonus:["Bonus flies!! So many flies!! 🐸","Free round! Hip hip hooray! 💚"],
      mystery:["Ooh what's in the lily pad?! 🐸🎁","Hoppy is so curious!! 🌿"],
    }},
  { id:"cat",       name:"Luna",    color:"#b094d4", rarity:"common",
    unlockCond:{type:"level",value:6}, unlockHint:"Complete Level 6",
    e:{idle:"😸",happy:"😻",excited:"😻",fire:"💜",fever:"✨",sad:"😿",victory:"👑",scared:"🙈"},
    dance:"danceCat",    catchphrase:"Purr-fectly amazing, just like you! 😸",
    speeches:{
      idle:["Purrr... shall we? 😸","Meow! Luna is here! 😸","Luna thinks you're wonderful! 💜"],
      happy:["Purrfect!! 😻","*purrs the happiest purr* ✨","Luna is so pleased! 😸"],
      streak:["Purr-fect streak!! 😻💜","Luna is impressed!! ✨","This is magnificent! 😻"],
      fever:["Luna fever! All sparkly!! ✨✨","The queen is delighted!! 👑"],
      close:["Almost! Luna knows you can! 👑","So close! One more! 😻"],
      miss:["Hmph... Luna still believes! 😿","Try again, little adventurer! 💜"],
      victory:["Luna purrs with pride!! 👑","We won! Luna chose wisely! 😸"],
      bonus:["BONUS! Luna gets ALL the toys!! ✨","Mine mine mine! 😻💜"],
      mystery:["Ooh shiny thing!! Luna WANTS!! 🎁✨","A box?! Luna adores boxes! 😸"],
    }},
  // ── RARE ─────────────────────────────────────────────────────
  { id:"panda",     name:"Bao",     color:"#94a3b8", rarity:"rare",
    unlockCond:{type:"level",value:10}, unlockHint:"Complete Level 10",
    e:{idle:"🐼",happy:"🐼",excited:"⭐",fire:"🌿",fever:"🌟",sad:"🥺",victory:"🎊",scared:"🙈"},
    dance:"dancePanda",  catchphrase:"Chill vibes, big wins! 🐼🍃",
    speeches:{
      idle:["*munch munch* Oh, we playing? 🐼","Bao is calm and ready! 🌿","Very zen, very win. 🐼"],
      happy:["Bao approves! 🐼⭐","*happy panda noises* 🌟","Oh, this is so nice! 🐼"],
      streak:["Bao is on a roll!! ⭐⭐","Panda power! So gentle, so strong! 🐼","Zen master mode!! 🌟"],
      fever:["Panda fever!! Bao is glowing!! 🌟🌟","This is unexpectedly wonderful!! 🐼"],
      close:["Almost! Bao stays calm... 🐼","Breathe and tap! ⭐"],
      miss:["That's okay! Bao has bamboo! 🥺","*gently tries again* 🌿"],
      victory:["Pandas win! Bao is so happy! 🎊","Best day! 🐼⭐🌟"],
      bonus:["Bonus!! Bamboo rain!! 🐼","Free round! Bao is delighted! 🌟"],
      mystery:["Ooh, is it bamboo?! 🐼🎁","Bao is curious and excited! ⭐"],
    }},
  { id:"penguin",   name:"Waddles", color:"#6ec0f5", rarity:"rare",
    unlockCond:{type:"level",value:15}, unlockHint:"Complete Level 15",
    e:{idle:"🐧",happy:"🐧",excited:"❄️",fire:"💙",fever:"🌊",sad:"🥺",victory:"🎉",scared:"🙈"},
    dance:"dancePenguin",catchphrase:"Waddling to victory together! 🐧❄️",
    speeches:{
      idle:["Waddle waddle! Let's go! 🐧","Penguins never give up! ❄️","Slip, slide, smile! 🐧"],
      happy:["Waddles is SO happy!! 🐧❄️","Sliding into success! 💙","Best friends win! 🎉"],
      streak:["Penguin streak! Waddletastic!! 🐧","Sliding on through!! ❄️❄️","Cool cool cool streak! 🐧💙"],
      fever:["Penguin fever!! So cozy but so fast!! 🌊🌊","Waddling at light speed!! 🐧"],
      close:["Almost! Penguins stick together! 🐧","One more slide! ❄️"],
      miss:["*cute slip* That's okay!! 🥺","Penguins bounce right back! ❄️💕"],
      victory:["Waddles wins!! Best day ever!! 🎉🐧","Penguin parade time!! ❄️🎊"],
      bonus:["Bonus!! More fish!! More fun!! 🐧","Free round! Waddles is spinning! ❄️"],
      mystery:["Is it a fish?! Please! 🐧🎁","*slides over excitedly* What is it?! ❄️"],
    }},
  { id:"lion",      name:"Simba",   color:"#fbbf24", rarity:"rare",
    unlockCond:{type:"streak",value:30}, unlockHint:"Achieve a 30-streak",
    e:{idle:"🦁",happy:"🦁",excited:"🌟",fire:"🌻",fever:"💫",sad:"🥺",victory:"🏅",scared:"🙈"},
    dance:"danceLion",   catchphrase:"Brave little lion, brave big heart! 🦁💛",
    speeches:{
      idle:["*tiny roar* Hi!! 🦁","Simba is your friend! 🌟","Ready to be brave together? 🦁"],
      happy:["Roarsome!! 🦁💛","Simba does a little happy dance! 🌟","So wonderful! I love this! 🌻"],
      streak:["Go go go!! 🦁🌟","Simba is cheering SO loud!! 💫","The pride is watching and they're PROUD!! 🦁"],
      fever:["Lion fever!! Simba can't stop smiling!! 💫💫","Bravest lion ever!! 🦁"],
      close:["Almost! Be brave! 🦁","One more! Simba believes in you! 🌟"],
      miss:["Oopsie roar! Try again! 🥺","Even brave lions have oopsies! 🦁💕"],
      victory:["Simba roars with joy!! 🦁🏅","We're the best team!! 🌟💛"],
      bonus:["Bonus!! Simba does zoomies!! 🦁","Free round! So exciting!! 🌻"],
      mystery:["Simba sniffs a gift!! 🦁🎁","What could it be?! Simba wants to know!! 🌟"],
    }},
  // ── EPIC ─────────────────────────────────────────────────────
  { id:"octopus",   name:"Inky",    color:"#b06de8", rarity:"epic",
    unlockCond:{type:"threestars",value:5}, unlockHint:"Get 3 stars on 5 levels",
    e:{idle:"🐙",happy:"🐙",excited:"💜",fire:"🌈",fever:"🌀",sad:"🥺",victory:"🎊",scared:"🙈"},
    dance:"danceOctopus",catchphrase:"Eight hugs for eight friends! 🐙💜",
    speeches:{
      idle:["Eight arms, all for hugging! 🐙","Inky loves you very much! 💜","Let's make waves! 🌊"],
      happy:["Ink-credible!! 🐙💜","Eight arms of happiness!! ✨","Tentacles of triumph! 🎊"],
      streak:["Octopus streak!! Inky is wiggling!! 🐙","Ink everywhere — happy ink!! 💜💜","All eight arms cheering!! 🌀"],
      fever:["Inky fever!! Whirling with joy!! 🌀🌀","Ink all the colours!! 🐙💜"],
      close:["So close! Inky uses all eight to cheer! 🐙","One more! Inky loves you! 💜"],
      miss:["*releases happy ink cloud* It's okay! 🥺","Inky gives you a gentle squeeze! 🐙💕"],
      victory:["Inky wins!! Eight-armed champion of love!! 🎊🐙","Ink-redibly done!! 💜"],
      bonus:["Bonus!! Inky grabs all with eight!! 🐙","Free round! Unlimited wiggling! 🌀"],
      mystery:["Eight arms reach for the gift! 🐙🎁","What is it?! Inky MUST see!! 💜"],
    }},
  { id:"butterfly", name:"Flutter", color:"#f9a8d4", rarity:"epic",
    unlockCond:{type:"coins",value:1000}, unlockHint:"Earn 1,000 total coins",
    e:{idle:"🦋",happy:"🦋",excited:"🌸",fire:"🌺",fever:"🌼",sad:"🥺",victory:"🌟",scared:"🙈"},
    dance:"danceButterfly",catchphrase:"Every tap is a tiny miracle! 🦋🌸",
    speeches:{
      idle:["Flutter flutter! Let's fly! 🦋","Beautiful things happen here! 🌸","Wings open, heart ready! 🦋"],
      happy:["Flutter-mazing!! 🦋🌸","Blooming with joy!! ✨","So beautiful it makes me wiggle! 🌺"],
      streak:["Flutter streak!! Soaring!! 🦋🌸","Wings of wonder!! 🌼","Dancing on the gentlest wind!! 🌺"],
      fever:["Flutter fever!! Blossoming!! 🌼🌼","All petals everywhere!! 🦋✨"],
      close:["Almost! Flutter believes in you! 🦋","One more graceful wingbeat! 🌸"],
      miss:["Even butterflies have wobbly days! 🥺","Flutter flutter, try again! 🦋💕"],
      victory:["Flutter wins!! Most beautiful day!! 🌟🦋","Bloomed into victory!! 🌸🎊"],
      bonus:["Bonus!! Gardens of sparkle!! 🦋","Free round! All the flowers are for you! 🌺"],
      mystery:["A gift wrapped in petals?! 🦋🎁","Flutter trembles with excitement! 🌸"],
    }},
  // ── LEGENDARY ────────────────────────────────────────────────
  { id:"unicorn",   name:"Sparky",  color:"#ffd700", rarity:"legendary",
    unlockCond:{type:"level",value:25}, unlockHint:"Complete Level 25",
    e:{idle:"🦄",happy:"🦄",excited:"🌈",fire:"💖",fever:"💫",sad:"🥺",victory:"💫",scared:"🙈"},
    dance:"danceUnicorn",catchphrase:"You ARE the magic! 🦄✨",
    speeches:{
      idle:["Magic is real, and so are you! 🦄","Sparky sprinkles love everywhere! 🌈","Rainbow hugs! READY! 🌈"],
      happy:["Sparkle sparkle!! 🌈🦄","Magical!! So wonderfully magical!! 💫","Rainbow heart activated! ✨"],
      streak:["Unicorn streak!! Rainbow power!! 🌈🌈","Sparky is doing a happy gallop!! 🦄","Pure magic is happening!! 💫💫"],
      fever:["Unicorn fever!! Maximum sparkle!! 💫💫🌈","Rainbow of love exploding!! 🦄✨🌈"],
      close:["So close!! The magic is almost here!! 🦄","One last spark of belief!! 🌈"],
      miss:["Even unicorns have cloudy days! 🥺","Shine on! Sparky believes! 🦄💕"],
      victory:["Sparky wins!! Most magical day!! 💫🌈","Believe in magic — we made it!! 🦄"],
      bonus:["Bonus!! Rainbow treasure shower!! 🌈🦄","Free round!! Sparky grants ALL wishes!! 💫"],
      mystery:["A magical gift!! Sparky vibrates with joy!! 🦄🎁","Is it rainbow treasure?! 🌈💫"],
    }},
];

// Per-mascot audio profile (base frequency + oscillator wave type)
const MASCOT_AUDIO={
  dragon:   {base:523,wave:"sawtooth"},  fox:      {base:659,wave:"square"},
  cat:      {base:587,wave:"sine"},      frog:     {base:392,wave:"sine"},
  lion:     {base:440,wave:"sawtooth"},  panda:    {base:392,wave:"sine"},
  penguin:  {base:659,wave:"triangle"}, octopus:  {base:349,wave:"sine"},
  butterfly:{base:587,wave:"sine"},      unicorn:  {base:698,wave:"sine"},
};

// Per-mascot vibration pattern on each tap
const MASCOT_HAPTIC={
  dragon:[15],      fox:[8,5,8],    cat:[6],      frog:[10,5,15],
  lion:[20,10,20],  panda:[8],      penguin:[5,8,5], octopus:[4,4,4,4],
  butterfly:[5],    unicorn:[8,4,8,4,12],
};

// Mascot accessories catalog
const MASCOT_ACCESSORIES=[
  {id:"hat",   emoji:"🎩",name:"Top Hat",    cost:200},
  {id:"crown", emoji:"👑",name:"Crown",       cost:350},
  {id:"glasses",emoji:"😎",name:"Sunglasses",  cost:250},
  {id:"halo",  emoji:"✨",name:"Golden Halo",  cost:400},
  {id:"bow",   emoji:"🎀",name:"Bow Tie",      cost:150},
  {id:"star",  emoji:"⭐",name:"Star Badge",   cost:180},
];

// Week key for weekly challenge
function getWeekKey(){const d=new Date();const jan=new Date(d.getFullYear(),0,1);const wk=Math.ceil(((d-jan)/86400000+jan.getDay()+1)/7);return`${d.getFullYear()}-W${wk}`;}

// Daily challenge level (deterministic by date)
function getDailyChallengeLevel(){const d=new Date();const seed=d.getFullYear()*10000+(d.getMonth()+1)*100+d.getDate();const rng=seededRng(seed);return Math.floor(rng()*18)+5;}
function getWeeklyChallengeLevel(){const d=new Date();const jan=new Date(d.getFullYear(),0,1);const wk=Math.ceil(((d-jan)/86400000+jan.getDay()+1)/7);const rng=seededRng(d.getFullYear()*100+wk);return Math.floor(rng()*20)+20;}

// Mystery Box prizes — variable ratio (weights, not percentages)
const MYSTERY_PRIZES=[
  {label:"+500 pts",  emoji:"⭐", type:"points", value:500,  weight:30},
  {label:"+200 pts",  emoji:"✨", type:"points", value:200,  weight:25},
  {label:"+80 🪙",    emoji:"🪙", type:"coins",  value:80,   weight:20},
  {label:"+150 🪙",   emoji:"💰", type:"coins",  value:150,  weight:10},
  {label:"EXTRA LIV", emoji:"❤️", type:"life",   value:1,    weight:10},
  {label:"JACKPOT!",  emoji:"🌈", type:"jackpot",value:2000, weight:5 },
];

// Boss loot table — one guaranteed drop per boss kill
const BOSS_LOOT=[
  {type:"coins",  label:"COIN BURST",    emoji:"💰", min:50,  max:200, weight:40, color:"#ffd700"},
  {type:"xp",     label:"XP SURGE",      emoji:"⚡", min:30,  max:80,  weight:35, color:"#60a5fa"},
  {type:"fragment",label:"RARE FRAGMENT",emoji:"💎", min:1,   max:1,   weight:25, color:"#c084fc"},
];

const LEVEL_NAMES = [
  // World 1 — Dragon's Lair
  "Cave Entrance","Warm Tunnel","Ember Glow","Scale Watch","Fireball Fun","Lava Bridge","Flame Trail","Dragon's Den","Fire Festival","Dragon Buddy",
  // World 2 — Troll Forest
  "Sunny Glade","Mossy Trail","Root Maze","Mushroom Path","Frog Pond","Gnarly Trees","Troll Bridge","Berry Grove","Forest Sing","Troll Chief",
  // World 3 — Elven Kingdom
  "Flower Arch","Elven Trail","Magic Glade","Silver Bow","Arrow Dance","Elven Gates","Crystal Spire","Magic School","Star Garden","Elf Queen",
  // World 4 — Magic Tower
  "Spell School","Wand Study","Magic Maze","Rune Room","Bubble Spell","Rainbow Portal","Sparkle Room","Potion Walk","Star Ritual","Wizard Pal",
  // World 5 — Viking Fjords
  "Shore Landing","Ice Trail","Rune Road","Frost Path","Snow Crossing","Viking Fun","Longship Run","Aurora Path","Rainbow Gate","Viking King",
  // World 6 — Goblin Mines
  "Mine Entry","Gold Vein","Gem Tunnel","Goblin Run","Treasure Hunt","Pickaxe Path","Crystal Cave","Deep Mine","Gem Blitz","Goblin Chief",
  // World 7 — Haunted Castle
  "Spooky Hall","Silly Creep","Ghost Slide","Pumpkin Road","Candy Maze","Friendly Gate","Castle Trail","Giggle Run","Silly Mass","Friendly Ghost",
  // World 8 — Ocean Deep
  "Coral Reef","Sea Cave","Tide Rush","Current Dash","Deep Dive","Jellyfish Trail","Bubble Gate","Seahorse Path","Rainbow Ocean","Friendly Whale",
  // World 9 — Giant's Peak
  "Mountain Base","Boulder Path","Cloud Climb","Thunder Trail","Giant Steps","Peak Rush","Cloud Walk","Lightning Pass","Summit Fun","Gentle Giant",
  // World 10 — Rainbow Dragon
  "Rainbow Path","Treasure Gate","Dragon's Eye","Golden Fire","Rainbow Trial","Colour Flame","Gem Rush","Sparkle Wrath","Final Fun","RAINBOW DRAGON",
];

// Special milestone modifiers
const MILESTONE_MODS = {
  10:  { type:"boss_kill",   desc:"Defeat the Dragon Buddy! 🐉" },
  20:  { type:"combo_20",    desc:"Tap 20 times without stopping! ⭐" },
  30:  { type:"fever_2",     desc:"Activate Magic Mode twice! ✨" },
  40:  { type:"no_miss",     desc:"Don't miss a single target! 🎯" },
  50:  { type:"speed_run",   desc:"Race to the finish! 🏃" },
  60:  { type:"moving_only", desc:"Tap only the moving targets! 💨" },
  70:  { type:"ghost_rush",  desc:"Find the hiding ghosts! 👻" },
  80:  { type:"combo_40",    desc:"Reach a 40× tap chain! 🔥" },
  90:  { type:"fever_3",     desc:"Activate Magic Mode 3 times! 🌟" },
  100: { type:"final_boss",  desc:"Defeat the RAINBOW DRAGON! 🌈" },
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
  const bossEnabled = n >= 25 || n % 10 === 0;
  const bossRate = n % 10 === 0 && n < 25 ? 0.055 : n >= 25 ? Math.min(0.07, (n-25)*0.001) : 0;
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

function getInfinityLevelConfig(round) {
  const n = 100 + round; // equivalent difficulty level
  const worldId = ((round - 1) % 10) + 1;
  const w = WORLDS[worldId - 1];
  const scoreGoal = Math.floor(8000 + round * 600 + round * round * 1.2);
  const spawnInterval = Math.max(280, 520 - round * 3.5);
  const targetLifetime = Math.max(650, 1400 - round * 7);
  const bombRate = Math.min(0.32, 0.18 + round * 0.003);
  const movingRate = Math.min(0.70, 0.40 + round * 0.006);
  const ghostRate = Math.min(0.30, 0.15 + round * 0.003);
  return {
    id:`inf${round}`, world:worldId, worldName:w.name, worldColor:w.color, worldBg:w.bg, worldGrid:w.grid,
    name:`∞ Round ${round}`, scoreGoal, lives:2, spawnInterval, targetLifetime,
    bombRate, movingRate, ghostRate, bossEnabled:false, bossRate:0,
    modifier:null, rarityBonus:0.18, isBoss:false, isLast:false, isInfinity:true,
  };
}

function getZenConfig(worldId=1) {
  const w=WORLDS[(worldId-1)%10];
  return {
    id:`zen${worldId}`, world:worldId, worldName:w.name, worldColor:w.color, worldBg:w.bg, worldGrid:w.grid,
    name:`☯ Zen — ${w.name}`, scoreGoal:99999, lives:99, spawnInterval:700,
    targetLifetime:3000, bombRate:0, movingRate:0.30, ghostRate:0.15,
    bossEnabled:false, bossRate:0, modifier:{type:"zen_timer",desc:"90s Zen — Pure tapping"},
    rarityBonus:0.15, isBoss:false, isLast:false, isZen:true, zenDuration:90000,
  };
}

// ═══════════════════════════════════════════════════════════════
// GAME CONSTANTS
// ═══════════════════════════════════════════════════════════════
const BASE_R       = 26;
const MAX_LIVES    = 5;
const FEVER_STREAK = 15;
const FEVER_DUR    = 8000;
const XP_PER_LVL   = 150;

// Skill tree — 6 skills × 3 levels, costs 1 skill point per upgrade
const SKILL_TREE = [
  { id:"coin_magnet",  icon:"🪙", name:"Coin Magnet",  desc:"Earn more coins per tap",       levels:["+5% coins","+10% coins","+20% coins"],  cost:[1,2,3] },
  { id:"target_sense", icon:"👁", name:"Target Sense", desc:"Targets stay longer",            levels:["+0.5s life","+1s life","+2s life"],      cost:[1,2,3] },
  { id:"fever_rush",   icon:"🔥", name:"Fever Rush",   desc:"Fever lasts longer & fills faster",levels:["+20% fever","+40% fever","+60% fever"],cost:[1,2,3] },
  { id:"critical_eye", icon:"🎯", name:"Critical Eye", desc:"Perfect-tap zone is wider",       levels:["+10% zone","+20% zone","+35% zone"],   cost:[1,2,3] },
  { id:"combo_guard",  icon:"🛡", name:"Combo Guard",  desc:"Streak survives more misses",     levels:["1st miss kept","2nd miss kept","3rd miss kept"],cost:[2,3,4]},
  { id:"xp_boost",     icon:"⚡", name:"XP Boost",     desc:"Earn more XP from levels",        levels:["+10% XP","+20% XP","+30% XP"],         cost:[1,2,3] },
];

const RARITY = {
  COMMON:    { name:"common",    chance:0.55, color:"#a78bfa", glow:"#7c3aed", mult:1,  size:1.0,  label:""            },
  UNCOMMON:  { name:"uncommon",  chance:0.23, color:"#34d399", glow:"#059669", mult:2,  size:1.15, label:"LUCKY ×2"    },
  RARE:      { name:"rare",      chance:0.13, color:"#fbbf24", glow:"#d97706", mult:5,  size:1.4,  label:"MAGIC ×5"    },
  EPIC:      { name:"epic",      chance:0.07, color:"#f472b6", glow:"#db2777", mult:15, size:1.8,  label:"SUPER ×15"   },
  LEGENDARY: { name:"legendary", chance:0.02, color:"#ff6030", glow:"#ff2000", mult:50, size:2.2,  label:"RAINBOW ×50" },
};

const THEMES = [
  { id:"neon",    name:"Arcane Night",  bg:"#0c0718",accent:"#a78bfa",secondary:"#6d28d9",grid:"rgba(167,139,250,0.05)",unlockLevel:1  },
  { id:"cyber",   name:"Ice Kingdom",   bg:"#020c18",accent:"#22d3ee",secondary:"#0e7490",grid:"rgba(34,211,238,0.04)", unlockLevel:5  },
  { id:"inferno", name:"Dragon Fire",   bg:"#180400",accent:"#ff6030",secondary:"#b45309",grid:"rgba(255,96,48,0.05)", unlockLevel:10 },
  { id:"matrix",  name:"Elven Forest",  bg:"#000e00",accent:"#39ff14",secondary:"#166534",grid:"rgba(57,255,20,0.04)", unlockLevel:20 },
  { id:"abyss",   name:"Dark Abyss",    bg:"#00000f",accent:"#6060ff",secondary:"#1a1a9a",grid:"rgba(96,96,255,0.04)",unlockLevel:30 },
  { id:"rose",    name:"Sacred Gold",   bg:"#180810",accent:"#ff8fab",secondary:"#9d174d",grid:"rgba(255,143,171,0.04)",unlockLevel:40},
];

const COMBO_LABELS = [
  [50,"AMAZING!! 🌈"],[35,"SUPER HERO! ⚡"],[20,"CHAMPION! 💥"],[10,"AWESOME! ⭐"],[5,"NICE! 😄"],
];

const ACHIEVEMENTS = [
  { id:"first_tap",    label:"First Tap!",       desc:"Your very first tap in the game",  icon:"👆", xp:10  },
  { id:"streak_10",    label:"On Fire",          desc:"10-tap streak — keep going!",      icon:"🔥", xp:20  },
  { id:"streak_25",    label:"Super Tapper",     desc:"25-tap streak!",                   icon:"⭐", xp:40  },
  { id:"streak_50",    label:"Tap Champion",     desc:"50-tap streak — incredible!",      icon:"🏆", xp:80  },
  { id:"first_rare",   label:"Magic Find",       desc:"Tap a Magic target",               icon:"✨", xp:15  },
  { id:"first_epic",   label:"Super Touch",      desc:"Tap a Super target",               icon:"💎", xp:30  },
  { id:"legendary",    label:"Rainbow Power",    desc:"Tap a Rainbow target",             icon:"🌈", xp:100 },
  { id:"boss_kill",    label:"Boss Beater",      desc:"Defeat a world boss",              icon:"🐉", xp:50  },
  { id:"perfect_tap",  label:"Bulls-Eye!",       desc:"Land a Perfect Tap",               icon:"🎯", xp:15  },
  { id:"level_10",     label:"Dragon Friend",    desc:"Complete Dragon's Lair",           icon:"🐉", xp:50  },
  { id:"level_25",     label:"World Explorer",   desc:"Reach World 3",                   icon:"🧭", xp:80  },
  { id:"level_50",     label:"Adventure Hero",   desc:"Reach World 5",                   icon:"🏆", xp:120 },
  { id:"level_100",    label:"QUEST MASTER",     desc:"Complete all 100 levels!",         icon:"🌈", xp:500 },
  { id:"three_stars",  label:"3 Stars!",         desc:"Get 3 stars on any level",         icon:"🌟", xp:25  },
  { id:"fever_mode",   label:"Magic Mode!",      desc:"Activate Magic Mode",              icon:"⚡", xp:30  },
  { id:"score_2000",   label:"Score Hero",       desc:"Score 2000 points in a level",     icon:"🚀", xp:50  },
  { id:"missions_all", label:"Quest Finisher",   desc:"Complete all daily quests",        icon:"📜", xp:50  },
  { id:"daily_7",      label:"Daily Hero",       desc:"Play 7 days in a row",             icon:"🌞", xp:75  },
  { id:"five_star",    label:"Perfect Boss Win",  desc:"3-star a boss level",             icon:"⭐", xp:100 },
  { id:"weekly_done",  label:"Weekly Champion",   desc:"Clear the Weekly Challenge",       icon:"🗓️", xp:150 },
  // ── Mid-tier achievements (added Phase 4A) ──
  { id:"streak_5",     label:"Warming Up",        desc:"5-tap streak",                     icon:"🌟", xp:8  },
  { id:"combo_15",     label:"Combo Master",      desc:"Reach a 15× combo",                icon:"💫", xp:30 },
  { id:"three_stars_5",label:"Star Collector",    desc:"Get 3 stars on 5 different levels",icon:"✨", xp:60 },
  { id:"mimic_hit",    label:"Mirror Master",     desc:"Tap a Mimic target",               icon:"🪞", xp:25 },
  { id:"shielded_hit", label:"Shield Breaker",    desc:"Destroy a Shielded target",        icon:"🛡", xp:30 },
  { id:"chain_4",      label:"Chain Reaction",    desc:"Trigger 4 chains in one tap",      icon:"⚡", xp:45 },
  { id:"mascot_lv10",  label:"Best Friends",      desc:"Level up a mascot to LV10",        icon:"🐾", xp:80 },
  { id:"prestige_1",   label:"Prestige Pioneer",  desc:"Prestige for the first time",      icon:"👑", xp:200 },
  { id:"tournament_top",label:"Tournament Top",   desc:"Reach Top 15% in a daily tournament",icon:"🏆", xp:90 },
  // Phase 10A — 5 new achievements
  { id:"zen_master",   label:"Zen Master",       desc:"Complete a Zen Mode session",         icon:"☯",  xp:40  },
  { id:"streak_50",    label:"Streak Legend",    desc:"Achieve a 50× streak",                icon:"🔥", xp:75  },
  { id:"coins_500",    label:"Coin Hoarder",     desc:"Collect 500 coins total",             icon:"💰", xp:35  },
  { id:"offline_earn", label:"Passive Earner",   desc:"Earn coins while offline",            icon:"🌙", xp:20  },
  { id:"all_worlds",   label:"World Traveler",   desc:"Play in all 10 worlds",               icon:"🌍", xp:100 },
];

const MISSION_TEMPLATES = [
  { id:"tap_30",    desc:"Tap 30 targets! 👆",          key:"tapsTotal",        goal:30  },
  { id:"rare_5",    desc:"Tap 5 Magic+ targets ✨",      key:"rareHits",         goal:5   },
  { id:"combo_15",  desc:"Reach a 15× tap chain 🔥",    key:"bestCombo",        goal:15  },
  { id:"boss_1",    desc:"Defeat a world boss 🐉",       key:"bossKills",        goal:1   },
  { id:"fever_2",   desc:"Activate Magic Mode 2× ⚡",   key:"feverCount",       goal:2   },
  { id:"perfect_5", desc:"5 Perfect Taps 🎯",           key:"perfectTaps",      goal:5   },
  { id:"levels_3",  desc:"Finish 3 levels 🏆",          key:"levelsCompleted",  goal:3   },
  { id:"powerup_3", desc:"Collect 3 power-ups 🔮",      key:"powerupCollected", goal:3   },
  { id:"score_500", desc:"Score 500 points in a level", key:"score",            goal:500 },
];

const SHOP_ITEMS = [
  { id:"extra_life",   name:"Magic Potion 🧪",  desc:"Start with +1 extra life",            cost:60,  icon:"🧪" },
  { id:"head_start",   name:"Lucky Start ⭐",    desc:"+300 bonus points at the start",      cost:80,  icon:"⭐" },
  { id:"shield_start", name:"Magic Shield 🛡️",  desc:"Begin with a Magic Shield",           cost:100, icon:"🛡️" },
  { id:"power_pack",   name:"Power Pack 🔮",     desc:"Start with a random power-up",        cost:120, icon:"🔮" },
  { id:"fever_potion", name:"Fever Potion 🌡️",  desc:"Start in instant Fever Mode!",        cost:90,  icon:"🌡️" },
  { id:"xp_bomb",      name:"XP Bomb ⚡",        desc:"2× XP reward from this level",        cost:70,  icon:"⚡" },
  { id:"streak_saver", name:"Streak Saver 💛",   desc:"Keep streak on next miss (once)",     cost:50,  icon:"💛" },
];

// ── Prestige cosmetics — unique title + badge per prestige level (12A) ──
const PRESTIGE_TIERS = [
  { level:0, title:null,               badge:null,   color:"#ffffff" },
  { level:1, title:"Dragon Slayer",    badge:"🐉",   color:"#ff6b35",
    desc:"Defeated the Dragon — eternal glory awaits" },
  { level:2, title:"Arcane Scholar",   badge:"🔮",   color:"#b06de8",
    desc:"Mastered the arcane arts beyond mortal limits" },
  { level:3, title:"Frost Warlord",    badge:"❄️",   color:"#6ec0f5",
    desc:"Conquered the Viking Fjords in the frozen north" },
  { level:4, title:"Cosmic Voyager",   badge:"🚀",   color:"#ffd700",
    desc:"Traveled all 10 worlds — the stars themselves bow" },
  { level:5, title:"NEXUS LEGEND",     badge:"🌈",   color:"#ff00ff",
    desc:"All 5 prestiges achieved — a living legend of NexusTap" },
];

// ═══════════════════════════════════════════════════════════════
// STORY DATA
// ═══════════════════════════════════════════════════════════════
const MAIN_STORY = {
  title: "The Rainbow Crystal Quest",
  intro: [
    "Long ago, the Rainbow Dragon kept 10 magical crystals that made the world colourful and happy. ✨",
    "One stormy night a mischievous wizard zapped the crystals away — sending one into each magical world! 🌩️",
    "Now YOU must travel through all 10 worlds, tap your way past creatures and bosses, and bring the crystals home! 🌈",
  ],
};

const WORLD_STORIES = [
  {
    worldId: 1,
    title: "Dragon's Lair",
    panels: [
      { emoji:"🐉", text:"Deep inside a glowing cave lives Ember the Dragon. He accidentally swallowed a crystal and now sneezes fire everywhere! 🔥" },
      { emoji:"😮", text:"All the little dragon hatchlings are running around in a panic — bouncing off the walls!" },
      { emoji:"👆", text:"Tap the fireballs and gems to calm everything down. Help Ember find peace and the crystal will pop right out!" },
    ],
    bossIntro: { emoji:"🐉🔥", title:"EMBER THE DRAGON!", text:"Ember is on his last sneeze! Tap him gently to help him feel better and release the crystal!" },
    victory: "Ember sneezed out the crystal — and said THANK YOU with a happy roar! 🐉💎 World 2 unlocked!",
  },
  {
    worldId: 2,
    title: "Troll Forest",
    panels: [
      { emoji:"🌿", text:"The Troll Forest is usually a quiet, happy place — but the crystal landed in the mushroom patch and now the trolls are dancing and bouncing EVERYWHERE! 🍄" },
      { emoji:"🧌", text:"Big Bork the Troll Chief is doing the wildest dance of all! He can't stop! The magic crystal is making him wiggle!" },
      { emoji:"👆", text:"Tap the bouncing mushrooms and help the trolls calm their wiggles! The crystal will be yours!" },
    ],
    bossIntro: { emoji:"🧌🍄", title:"BORK THE TROLL CHIEF!", text:"Big Bork is wiggling so hard the whole forest is shaking! Tap him in rhythm to stop the dance!" },
    victory: "Bork finally stopped dancing and gave you the crystal as a thank-you gift! 🍄💎 World 3 unlocked!",
  },
  {
    worldId: 3,
    title: "Elven Kingdom",
    panels: [
      { emoji:"✨", text:"The Elven Kingdom glitters with golden light — but ever since the crystal landed here, the elves have been shooting sparkling arrows in every direction! 🏹" },
      { emoji:"🧝", text:"Queen Elara is trying to cast a calming spell but her wand keeps shooting rainbow stars!" },
      { emoji:"👆", text:"Tap the magical sparks before they disappear — collect enough and you'll earn the crystal!" },
    ],
    bossIntro: { emoji:"🧝‍♀️✨", title:"QUEEN ELARA!", text:"The queen's magic is going wild! Tap her sparkling stars to absorb the excess magic — then the crystal will appear!" },
    victory: "Queen Elara's magic calmed down and the crystal floated right into your hands! ✨💎 World 4 unlocked!",
  },
  {
    worldId: 4,
    title: "Magic Tower",
    panels: [
      { emoji:"🔮", text:"In the tallest tower in the land lives Professor Zap, a very friendly wizard — but his spells went haywire when the crystal crashed through his window! 🪟" },
      { emoji:"🧙", text:"Magic orbs, potion bubbles and sparkle bolts are flying around the tower!" },
      { emoji:"👆", text:"Tap the flying magic orbs before they explode — help Professor Zap clean up his tower!" },
    ],
    bossIntro: { emoji:"🧙‍♂️🔮", title:"PROFESSOR ZAP!", text:"Zap has accidentally turned himself into a giant magic orb! Tap him to bring him back to normal!" },
    victory: "Zap popped back to normal and thanked you with the crystal and a bag of magic sweets! 🔮💎 World 5 unlocked!",
  },
  {
    worldId: 5,
    title: "Viking Fjords",
    panels: [
      { emoji:"❄️", text:"The Viking Fjords are icy and beautiful — but the crystal landed on a frozen lake and now the Vikings are having the biggest snowball fight EVER! ❄️🏔️" },
      { emoji:"⛵", text:"Chief Björn is throwing snowballs so fast that even his reindeer are scared!" },
      { emoji:"👆", text:"Tap the snowballs before they land! Survive the blizzard and Chief Björn will give you the crystal!" },
    ],
    bossIntro: { emoji:"⛵❄️", title:"CHIEF BJÖRN!", text:"Björn is spinning on the ice throwing snowballs in every direction! Tap them all to win the crystal!" },
    victory: "Björn declared you the snowball champion and handed over the crystal with a big Viking smile! ❄️💎 World 6 unlocked!",
  },
  {
    worldId: 6,
    title: "Goblin Mines",
    panels: [
      { emoji:"⛏️", text:"The Goblin Mines are full of glittering gems and happy little goblins — but the crystal fell deep in the mine and now ALL the goblins are super excited, throwing gems everywhere! 💎" },
      { emoji:"🟢", text:"The Goblin Chief is so happy he's spinning in circles, flinging gold coins and crystals in all directions!" },
      { emoji:"👆", text:"Tap the flying gems and gold coins! Collect them all to earn the magical crystal!" },
    ],
    bossIntro: { emoji:"⛏️💰", title:"THE GOBLIN CHIEF!", text:"The Chief is dizzy with excitement! Tap him and his flying treasure to claim the magic crystal!" },
    victory: "The Goblin Chief was SO happy to share his treasure with a brave hero like you! ⛏️💎 World 7 unlocked!",
  },
  {
    worldId: 7,
    title: "Haunted Castle",
    panels: [
      { emoji:"👻", text:"Don't be scared — this is actually a FRIENDLY haunted castle! The ghosts love to play hide-and-seek, but the crystal has made them invisible for real! 🏰" },
      { emoji:"😄", text:"Giggles the Ghost is laughing so hard you can barely see him at all!" },
      { emoji:"👆", text:"Tap the spots where ghosts are hiding before they giggle away! Find Giggles last for the crystal!" },
    ],
    bossIntro: { emoji:"👻🎃", title:"GIGGLES THE GHOST!", text:"Giggles is nearly invisible from all the laughing! Tap him when you see a shimmer to win the crystal!" },
    victory: "Giggles laughed so hard the crystal fell out of his pocket! The nicest ghost ever! 👻💎 World 8 unlocked!",
  },
  {
    worldId: 8,
    title: "Ocean Deep",
    panels: [
      { emoji:"🌊", text:"Under the sparkling ocean live wonderful sea creatures — but the crystal sank to the bottom and now everyone is blowing bubbles in total excitement! 🐠🐙" },
      { emoji:"🐋", text:"Wally the Friendly Whale is blowing so many bubbles that the whole ocean looks like a giant bubble bath!" },
      { emoji:"👆", text:"Pop the colourful bubbles before they float to the surface! Pop them all and Wally will give you the crystal!" },
    ],
    bossIntro: { emoji:"🐋🫧", title:"WALLY THE WHALE!", text:"Wally is the biggest bubble-blower in the whole ocean! Tap his bubbles to win the crystal!" },
    victory: "Wally sang you a happy whale song and pushed the crystal to shore with his nose! 🌊💎 World 9 unlocked!",
  },
  {
    worldId: 9,
    title: "Giant's Peak",
    panels: [
      { emoji:"⛰️", text:"High in the clouds live the gentlest giants you've ever met — but the crystal got stuck in a storm cloud and now boulders are rolling down the mountain! 🪨⚡" },
      { emoji:"🌩️", text:"Grumble the Giant is stomping around trying to catch the boulders but his big feet keep making things worse!" },
      { emoji:"👆", text:"Tap the rolling boulders before they reach the bottom! Help Grumble and he'll fish out the crystal!" },
    ],
    bossIntro: { emoji:"⛰️🌩️", title:"GRUMBLE THE GIANT!", text:"Grumble is stomping through a thunderstorm! Tap his boulders to calm the mountain!" },
    victory: "Grumble finally caught all the boulders and found the crystal in his pocket all along! ⛰️💎 World 10 unlocked!",
  },
  {
    worldId: 10,
    title: "Rainbow Dragon",
    panels: [
      { emoji:"🌈", text:"You've made it to the magical sky palace where the Rainbow Dragon lives! All the other creatures cheered you on every step of the way! 🎉" },
      { emoji:"🐲", text:"The Rainbow Dragon has been waiting for a true hero to return the last crystal — this is your moment!" },
      { emoji:"👆", text:"The Rainbow Dragon will test you with its most amazing rainbow powers! Tap everything you see to prove you are the QUEST MASTER!" },
    ],
    bossIntro: { emoji:"🌈👑", title:"THE RAINBOW DRAGON!", text:"The greatest challenge of the whole adventure! Tap every single rainbow burst to prove your skill!" },
    victory: "🌈 YOU DID IT! 🌈 All 10 crystals returned! The Rainbow Dragon crowned you the greatest hero in all the land! 🎊👑",
  },
];

const DEFAULT_SAVE = {
  highScore:0, xp:0, bestStreak:0, coins:0, totalCoins:0,
  unlockedAchievements:[], themeId:"neon", soundEnabled:true,
  scores:[], lastLoginDate:null, loginStreak:0,
  missionDate:null, missionProgress:{}, missionCompleted:false,
  levelStars:{}, unlockedLevel:1,
  seenWorldStories:[], seenMainStory:false, seenBossIntros:[],
  seenTutorial:false, lastSpinDate:null, mascotId:"dragon",
  unlockedMascots:["dragon","fox"],
  // New feature fields
  prestigeLevel:0,       // 0-5 prestiges, each adds +5% score mult
  mascotXP:{},           // { mascotId: totalXP }
  musicVol:80,           // 0-100
  sfxVol:80,             // 0-100
  hapticEnabled:true,    // vibration on/off
  speedMode:1.0,         // 0.7=easy, 1.0=normal, 1.3=hard, 1.6=expert
  colorblindMode:false,  // rarity symbols instead of color-only
  infinityBest:0,        // best score in infinity mode
  infinityScores:[],     // top 10 infinity scores
  gauntletDate:null,     // date string of last gauntlet attempt
  gauntletBest:0,        // bosses defeated in best gauntlet run
  mascotAccessories:{},  // { mascotId: accessoryId } — currently equipped
  ownedAccessories:{},   // { "mascotId:accessoryId": true } — purchased
  weeklyChallengeDate:null, // week key of last weekly attempt
  weeklyChallengeCompleted:false, // true if this week's weekly was beaten
  weeklyChallengeBest:0, // best score on this week's weekly
  tournamentDate:null,    // day key of today's tournament attempt
  tournamentBest:0,       // best score today
  tournamentHistory:[],   // [{date, score, rank}] last 7 days
  bossFragments:0,        // cosmetic fragments from boss loot (10 = 1 accessory unlock)
  bossLootHistory:[],     // [{type, amount, date}] last 20 drops
  skillPoints:0,          // earned via XP milestones, spent in skill tree
  skills:{},              // { skillId: level }
  adaptiveDifficulty:false, // auto-adjusts spawn rate to keep player challenged
  zenBest:0,               // best score in zen mode
  zenBestWorld:1,          // world of best zen run
  lastActiveTime:null,     // timestamp (ms) when player last closed/backgrounded app
  worldBest:{},            // { worldId: bestScore } — per-world records (12B)
  lastWeeklyRecap:null,    // weekKey of last shown weekly recap (12C)
};

// ── Offline coin calculation (max 4 hours, 1 coin per 10s) ──
function calcOfflineCoins(lastActiveMs) {
  if(!lastActiveMs) return 0;
  const elapsed=Date.now()-lastActiveMs;
  const maxMs=4*60*60*1000; // 4 hours
  const cappedMs=Math.min(elapsed,maxMs);
  return Math.floor(cappedMs/10000); // 1 coin every 10 seconds
}

// ═══════════════════════════════════════════════════════════════
// AUDIO ENGINE
// ═══════════════════════════════════════════════════════════════
function createAudio() {
  let ctx = null;
  // Master chain nodes — initialized on first audio context creation
  let comp = null, revConv = null, revWet = null;
  const C = () => {
    if(!ctx) {
      ctx = new(window.AudioContext||window.webkitAudioContext)();
      // Dynamics compressor — adds punch, prevents clipping, makes hits feel physical
      comp = ctx.createDynamicsCompressor();
      comp.threshold.value = -18; comp.knee.value = 12;
      comp.ratio.value = 4; comp.attack.value = 0.003; comp.release.value = 0.28;
      comp.connect(ctx.destination);
      // Programmatic reverb impulse — adds room/space to big moments
      const len = Math.floor(ctx.sampleRate * 1.1);
      const ir = ctx.createBuffer(2, len, ctx.sampleRate);
      for(let ch=0;ch<2;ch++){const d=ir.getChannelData(ch);for(let i=0;i<len;i++)d[i]=(Math.random()*2-1)*Math.pow(1-i/len,2.5);}
      revConv = ctx.createConvolver(); revConv.buffer = ir;
      revWet = ctx.createGain(); revWet.gain.value = 0.22;
      revConv.connect(revWet); revWet.connect(comp);
    }
    return ctx;
  };
  // Dry sound — routes through compressor only
  const t = (freq,type,dur,vol=0.26,delay=0)=>{
    try{
      const c=C(),o=c.createOscillator(),g=c.createGain();
      o.connect(g);g.connect(comp);
      o.type=type;o.frequency.setValueAtTime(freq,c.currentTime+delay);
      g.gain.setValueAtTime(vol,c.currentTime+delay);
      g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+delay+dur);
      o.start(c.currentTime+delay);o.stop(c.currentTime+delay+dur+0.05);
    }catch{}
  };
  // Reverb sound — dry + wet send for big moments (boss kill, legendary, jackpot)
  const tR = (freq,type,dur,vol=0.26,delay=0)=>{
    try{
      const c=C(),o=c.createOscillator(),g=c.createGain(),rv=c.createGain();
      o.connect(g);g.connect(comp);g.connect(rv);rv.gain.value=0.5;rv.connect(revConv);
      o.type=type;o.frequency.setValueAtTime(freq,c.currentTime+delay);
      g.gain.setValueAtTime(vol,c.currentTime+delay);
      g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+delay+dur);
      o.start(c.currentTime+delay);o.stop(c.currentTime+delay+dur+0.05);
    }catch{}
  };
  const chord=(freqs,type,dur,vol,dt=0.06)=>freqs.forEach((f,i)=>t(f,type,dur,vol,i*dt));
  const chordR=(freqs,type,dur,vol,dt=0.06)=>freqs.forEach((f,i)=>tR(f,type,dur,vol,i*dt));
  return{
    tap:        ()=>{t(540,"sine",0.09,0.22);t(810,"sine",0.07,0.1,0.04);},
    miss:       ()=>{t(160,"sawtooth",0.38,0.22);},
    uncommon:   ()=>{t(600,"sine",0.12,0.24);t(900,"sine",0.08,0.16,0.07);},
    rare:       ()=>{chord([660,880,1100],"sine",0.18,0.26,0.07);},
    epic:       ()=>{chord([440,554,659,880,1108],"sine",0.22,0.26,0.065);},
    legendary:  ()=>{chordR([330,440,550,660,880,1100,1320],"sine",0.28,0.28,0.055);},
    boss:       ()=>{t(100,"sawtooth",0.5,0.32);t(140,"square",0.3,0.18,0.1);},
    bossHit:    ()=>{t(200,"sawtooth",0.2,0.28);t(260,"sine",0.12,0.18,0.06);},
    bossKill:   ()=>{chordR([262,330,392,523,659],"sine",0.35,0.3,0.08);},
    bombSpawn:  ()=>{t(110,"sawtooth",0.4,0.28);t(75,"sawtooth",0.22,0.18,0.14);},
    bombHit:    ()=>{t(90,"sawtooth",0.55,0.36);t(55,"sawtooth",0.28,0.26,0.2);},
    powerUp:    ()=>{chord([440,554,659,880],"sine",0.14,0.22,0.055);},
    feverStart: ()=>{chordR([440,554,659,880,1108],"square",0.12,0.18,0.05);},
    feverEnd:   ()=>{chord([880,659,554,440],"sine",0.14,0.18,0.07);},
    levelUp:    ()=>{chord([523,659,784,1047,1319],"sine",0.18,0.28,0.08);},
    levelComplete:()=>{chordR([523,659,784,1047],"sine",0.22,0.3,0.09);},
    perfect:    ()=>{chord([880,1108,1320],"sine",0.14,0.26,0.06);},
    countdown:  ()=>{t(440,"sine",0.15,0.28);},
    go:         ()=>{chord([523,659,784],"sine",0.2,0.3,0.05);},
    gameOver:   ()=>{chord([440,370,294,220],"sawtooth",0.25,0.18,0.1);},
    coin:       ()=>{t(1200,"sine",0.08,0.16);t(1500,"sine",0.05,0.12,0.07);},
    starEarn:   ()=>{tR(880,"sine",0.15,0.25);tR(1108,"sine",0.1,0.2,0.12);},
    unlock:     ()=>{chordR([440,554,659,784],"sine",0.2,0.22,0.07);},
    waveUp:     ()=>{chord([330,415,523,659],"square",0.2,0.2,0.07);},
    // Musical pentatonic scale — each streak note rises chromatically
    // C major pentatonic: C5 D5 E5 G5 A5 C6 D6 E6 G6 A6 C7
    comboNote:  (streak)=>{
      const scale=[523,587,659,784,880,1047,1175,1319,1568,1760,2093,2349];
      const n=scale[Math.min(Math.max(0,streak-1),scale.length-1)];
      const vol=0.13+Math.min(0.09,streak*0.004);
      t(n,"sine",0.09,vol);
      if(streak>=5)t(n*1.498,"sine",0.065,vol*0.4,0.02);  // perfect 5th
      if(streak>=10)t(n*2,"sine",0.045,vol*0.25,0.04);     // octave
      if(streak>=20)t(n*3,"sine",0.03,vol*0.15,0.06);      // 12th
    },
    // Per-mascot combo note — same ratios as comboNote but custom base+wave
    mascotNote: (streak,base,wave)=>{
      const ratios=[1,1.122,1.26,1.498,1.682,2,2.245,2.52,2.996,3.364,4,4.49];
      const n=base*ratios[Math.min(Math.max(0,streak-1),ratios.length-1)];
      const vol=0.13+Math.min(0.09,streak*0.004);
      t(n,wave||"sine",0.09,vol);
      if(streak>=5)t(n*1.498,"sine",0.065,vol*0.4,0.02);
      if(streak>=10)t(n*2,"sine",0.045,vol*0.25,0.04);
      if(streak>=20)t(n*3,"sine",0.03,vol*0.15,0.06);
    },
    chainBonus: ()=>{chord([784,1047,1319],"square",0.1,0.22,0.04);t(1568,"sine",0.08,0.18,0.14);},
    flawless:   ()=>{chordR([523,659,784,1047,1319,1568],"sine",0.24,0.3,0.07);tR(2093,"sine",0.2,0.28,0.6);},
    hotStreak:  ()=>{chord([440,554,659,880],"sawtooth",0.12,0.2,0.055);},
    treasure:   ()=>{chordR([523,659,784,1047,1319,1568],"sine",0.22,0.26,0.06);tR(2093,"sine",0.12,0.2,0.38);},
    jackpot:    ()=>{
      [523,659,784,1047,1319,1568,2093].forEach((f,i)=>tR(f,"sine",0.18,0.28,i*0.055));
      setTimeout(()=>chordR([1047,1319,1568,2093],"sine",0.18,0.24,0.04),500);
    },
    shieldBreak:()=>{t(660,"sine",0.12,0.22);t(440,"sawtooth",0.18,0.16,0.08);},
    lucky:      ()=>{chordR([784,1047,1319,1568],"sine",0.14,0.24,0.06);},
    bossPhase:  ()=>{t(110,"sawtooth",0.4,0.36);t(160,"square",0.3,0.24,0.08);chord([440,330],"sawtooth",0.22,0.18,0.18);},
    prestige:   ()=>{[523,659,784,1047,1319,1568,2093,2349].forEach((f,i)=>tR(f,"sine",0.22,0.32,i*0.07));},
    infinityWin:()=>{chordR([523,659,784,1047,1319],"sine",0.2,0.28,0.06);setTimeout(()=>chordR([1047,1319,1568,2093],"sine",0.18,0.24,0.05),550);},
    nearMiss:   ()=>{chord([262,330,392,523],"sine",0.2,0.2,0.1);},
    // ── Background music ──
    startBgMusic:(wid)=>{
      const WM=[
        [196,220,247,262,294,262,247,220], // Dragon
        [330,370,415,440,494,440,415,370], // Forest
        [440,494,554,587,659,587,554,494], // Elven
        [262,294,330,370,415,370,330,294], // Magic
        [174,196,220,247,262,247,220,196], // Viking
        [220,247,262,294,330,294,262,247], // Goblin
        [196,220,247,262,247,220,196,174], // Haunted
        [294,330,370,415,440,415,370,330], // Ocean
        [262,294,330,370,415,440,415,370], // Giant
        [523,587,659,784,880,784,659,587], // Rainbow
      ];
      if(ctx&&ctx.state==="suspended")ctx.resume().catch(()=>{});
      const mel=WM[Math.max(0,(wid||1)-1)];
      let note=0,tmpo=460,tmr=null,on=true;
      const tick=()=>{
        if(!on)return;
        try{
          const c=C(),o=c.createOscillator(),g=c.createGain();
          o.connect(g);g.connect(comp);
          o.type="triangle";o.frequency.setValueAtTime(mel[note%mel.length],c.currentTime);
          g.gain.setValueAtTime(bgVol,c.currentTime);
          g.gain.exponentialRampToValueAtTime(0.001,c.currentTime+tmpo*0.0008);
          o.start(c.currentTime);o.stop(c.currentTime+tmpo*0.0009);
        }catch{}
        note++;
        tmr=setTimeout(tick,tmpo);
      };
      let bgVol=0.032;
      tick();
      bgMusicCtl={stop:()=>{on=false;if(tmr)clearTimeout(tmr);},setFever:(f)=>{tmpo=f?280:460;},setVol:(v)=>{bgVol=v;}};
    },
    stopBgMusic:()=>{bgMusicCtl&&bgMusicCtl.stop();bgMusicCtl=null;},
    setBgMusicFever:(f)=>{bgMusicCtl&&bgMusicCtl.setFever(f);},
  };
}
let bgMusicCtl=null;
let _bgBlast=null; // {x,y,at:performance.now()} — set on boss kill for bg particle explosion

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
// Module-level flags synced from save on game start
let _hapticOn = true;
let _colorblindOn = false;
function vibrate(p){try{if(_hapticOn&&navigator.vibrate)navigator.vibrate(p);}catch{}}

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

// World boss emojis
const BOSS_EMOJIS=["🐉","🌿","✨","🔮","❄️","⛏️","👻","🌊","⛰️","🌈"];

// ── Boss target ──
function drawBoss(ctx, r, hitsLeft, maxHits, ts, worldId=1, rage=false) {
  const phase=(maxHits-hitsLeft)/maxHits;
  const colors=["#ff6030","#f472b6","#ef4444"];
  const c=rage?"#ff0000":colors[Math.min(Math.floor(phase*3),2)];
  const glow=rage?"#ff0000":colors[Math.min(Math.floor(phase*3),2)];
  // Rage pulsing outer ring
  if(rage){
    const rageAlpha=0.4+0.6*Math.abs(Math.sin(ts*0.012));
    ctx.save();
    ctx.strokeStyle=`rgba(255,0,0,${rageAlpha})`;ctx.lineWidth=4;
    ctx.shadowColor="#ff0000";ctx.shadowBlur=30;
    ctx.beginPath();ctx.arc(0,0,r*2.1,0,Math.PI*2);ctx.stroke();
    ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.stroke();
    ctx.restore();
  }
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
  // World emoji label
  ctx.save(); ctx.globalAlpha=0.9;
  ctx.font=`${r*0.72}px serif`; ctx.textAlign="center"; ctx.textBaseline="middle";
  ctx.shadowColor="#fff"; ctx.shadowBlur=16;
  ctx.fillText(BOSS_EMOJIS[(worldId||1)-1]||"🐉",0,r*0.06); ctx.restore();
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

// ── Treasure chest target ──
function drawTreasure(ctx, r, ts) {
  const bob=Math.sin(ts*0.003)*3;
  const spin=ts*0.0012;
  ctx.save();ctx.translate(0,bob);
  // Outer glow
  const grd=ctx.createRadialGradient(0,0,r*0.3,0,0,r*1.8);
  grd.addColorStop(0,"#ffd70055");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*1.8,0,Math.PI*2);ctx.fill();
  // Chest lid (top half)
  ctx.shadowColor="#ffd700";ctx.shadowBlur=r*0.8;
  ctx.fillStyle="#d4a017";
  ctx.beginPath();ctx.roundRect(-r*0.88,-r*0.72,r*1.76,r*0.82,6);ctx.fill();
  // Chest body (bottom half)
  ctx.fillStyle="#c8860a";
  ctx.beginPath();ctx.roundRect(-r*0.88,-r*0.08,r*1.76,r*0.85,4);ctx.fill();
  // Gold bands
  ctx.strokeStyle="#ffd700";ctx.lineWidth=3;ctx.shadowBlur=8;
  ctx.beginPath();ctx.moveTo(-r*0.88,-r*0.06);ctx.lineTo(r*0.88,-r*0.06);ctx.stroke();
  ctx.strokeStyle="#ffc800";ctx.lineWidth=1.5;
  [-0.62,0.62].forEach(x=>{ctx.beginPath();ctx.moveTo(r*x,-r*0.72);ctx.lineTo(r*x,r*0.77);ctx.stroke();});
  // Keyhole
  ctx.fillStyle="#7a4800";ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(0,r*0.2,r*0.18,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#5a3200";
  ctx.beginPath();ctx.rect(-r*0.08,r*0.2,r*0.16,r*0.28);ctx.fill();
  // "?" sparkling on lid
  ctx.fillStyle="#fff";ctx.shadowColor="#fff";ctx.shadowBlur=16;
  ctx.font=`bold ${r*0.68}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("?",0,-r*0.32);
  // Orbiting sparkles
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4+spin;const dist=r*1.4;
    const sx=Math.cos(a)*dist,sy=Math.sin(a)*dist*0.6;
    const pulse=0.5+0.5*Math.abs(Math.sin(ts*0.006+i*0.8));
    ctx.save();ctx.translate(sx,sy);ctx.globalAlpha=pulse*0.9;
    ctx.fillStyle=i%2===0?"#ffd700":"#fff";ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=8;
    const ss=r*0.18*pulse;
    ctx.beginPath();
    for(let p=0;p<4;p++){const pa=p*Math.PI/2-Math.PI/4;ctx.lineTo(Math.cos(pa)*ss,Math.sin(pa)*ss);}
    ctx.closePath();ctx.fill();
    ctx.restore();
  }
  ctx.restore();
}

// ── Mystery Box target ──
function drawMimic(ctx, r, ts, mimicColor="#c8c8c8", mimicGlow="#ffffff") {
  // Mimic — silvery shape-shifting target with rotating "?" glyph
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  const spin=ts*0.0014;
  ctx.save();
  // Outer halo
  const halo=ctx.createRadialGradient(0,0,r*0.2,0,0,r*2.1);
  halo.addColorStop(0,mimicColor+"55");halo.addColorStop(0.6,mimicColor+"15");halo.addColorStop(1,"transparent");
  ctx.fillStyle=halo;ctx.beginPath();ctx.arc(0,0,r*2.1,0,Math.PI*2);ctx.fill();
  // Pulsing outer ring
  ctx.save();ctx.rotate(spin*0.6);
  ctx.strokeStyle=mimicGlow;ctx.globalAlpha=0.5+pulse*0.4;ctx.lineWidth=2;
  ctx.shadowColor=mimicGlow;ctx.shadowBlur=18;
  ctx.setLineDash([5,8]);
  ctx.beginPath();ctx.arc(0,0,r*1.35,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.restore();
  // Body — shifting prismatic look
  ctx.shadowColor=mimicGlow;ctx.shadowBlur=r*(0.7+pulse*0.5);
  const body=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  body.addColorStop(0,"#f5f5f5");body.addColorStop(0.4,mimicColor);body.addColorStop(1,mimicGlow);
  ctx.fillStyle=body;ctx.beginPath();ctx.arc(0,0,r*(0.92+pulse*0.08),0,Math.PI*2);ctx.fill();
  // "?" glyph
  ctx.fillStyle="#111";ctx.shadowColor="transparent";ctx.shadowBlur=0;
  ctx.font=`bold ${Math.round(r*1.3)}px 'Segoe UI',sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("?",0,r*0.05);
  // Sparkle satellites
  for(let i=0;i<5;i++){
    const a=i*Math.PI*0.4+spin*2;const d=r*1.55;
    const op=0.3+0.7*Math.abs(Math.sin(ts*0.008+i*1.3));
    ctx.save();ctx.translate(Math.cos(a)*d,Math.sin(a)*d);ctx.globalAlpha=op;
    ctx.fillStyle="#ffffff";ctx.shadowColor=mimicGlow;ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(0,0,r*0.08,0,Math.PI*2);ctx.fill();ctx.restore();
  }
  ctx.restore();
}

function drawMystery(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.004);
  const spin=ts*0.0018;
  const bob=Math.sin(ts*0.0035)*4;
  ctx.save();ctx.translate(0,bob);
  // Outer glow ring
  const grd=ctx.createRadialGradient(0,0,r*0.2,0,0,r*2);
  grd.addColorStop(0,"#ffd70066");grd.addColorStop(0.6,"#ffd70022");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*2,0,Math.PI*2);ctx.fill();
  // Rotating dashed ring
  ctx.save();ctx.rotate(spin);
  ctx.strokeStyle=`rgba(255,215,0,${0.5+pulse*0.5})`;ctx.lineWidth=3;
  ctx.shadowColor="#ffd700";ctx.shadowBlur=14;
  ctx.setLineDash([8,6]);ctx.beginPath();ctx.arc(0,0,r*1.22,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.restore();
  // Main body
  ctx.shadowColor="#ffd700";ctx.shadowBlur=r*(0.6+pulse*0.4);
  const bodyGrd=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  bodyGrd.addColorStop(0,"#ffe566");bodyGrd.addColorStop(0.5,"#ffd700");bodyGrd.addColorStop(1,"#c8a000");
  ctx.fillStyle=bodyGrd;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Gift ribbon vertical
  ctx.strokeStyle="#ff6030";ctx.lineWidth=r*0.18;ctx.shadowColor="#ff6030";ctx.shadowBlur=8;
  ctx.beginPath();ctx.moveTo(0,-r*0.95);ctx.lineTo(0,r*0.95);ctx.stroke();
  // Gift ribbon horizontal
  ctx.beginPath();ctx.moveTo(-r*0.95,0);ctx.lineTo(r*0.95,0);ctx.stroke();
  // Bow center
  ctx.fillStyle="#ff6030";ctx.shadowBlur=12;
  ctx.beginPath();ctx.arc(0,0,r*0.22,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#fff";ctx.shadowColor="#fff";ctx.shadowBlur=8;
  ctx.beginPath();ctx.arc(0,0,r*0.1,0,Math.PI*2);ctx.fill();
  // Orbiting stars
  for(let i=0;i<6;i++){
    const a=i*Math.PI/3+spin*1.5;const d=r*1.55;
    const op=0.4+0.6*Math.abs(Math.sin(ts*0.005+i));
    ctx.save();ctx.translate(Math.cos(a)*d,Math.sin(a)*d);ctx.globalAlpha=op;
    ctx.fillStyle=i%2===0?"#ffd700":"#fff";ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=6;
    ctx.font=`${r*0.28}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText(["⭐","✨","💎","⭐","✨","💎"][i],0,0);ctx.restore();
  }
  ctx.restore();
}

function drawAnchor(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.0035);
  const spin=ts*0.0008;
  ctx.save();
  // Outer glow
  const grd=ctx.createRadialGradient(0,0,r*0.2,0,0,r*2);
  grd.addColorStop(0,"#06b6d466");grd.addColorStop(0.6,"#06b6d422");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*2,0,Math.PI*2);ctx.fill();
  // Rotating ring
  ctx.save();ctx.rotate(spin);
  ctx.strokeStyle=`rgba(6,182,212,${0.5+pulse*0.4})`;ctx.lineWidth=2.5;
  ctx.shadowColor="#06b6d4";ctx.shadowBlur=12;
  ctx.setLineDash([6,5]);ctx.beginPath();ctx.arc(0,0,r*1.2,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.restore();
  // Body
  ctx.shadowColor="#06b6d4";ctx.shadowBlur=r*(0.5+pulse*0.5);
  const body=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  body.addColorStop(0,"#67e8f9");body.addColorStop(0.5,"#06b6d4");body.addColorStop(1,"#0e7490");
  ctx.fillStyle=body;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Anchor symbol
  ctx.strokeStyle="#ffffff";ctx.lineWidth=r*0.13;ctx.lineCap="round";ctx.lineJoin="round";
  ctx.shadowColor="#ffffff";ctx.shadowBlur=6;
  // Ring at top
  ctx.beginPath();ctx.arc(0,-r*0.52,r*0.2,0,Math.PI*2);ctx.stroke();
  // Vertical stem
  ctx.beginPath();ctx.moveTo(0,-r*0.32);ctx.lineTo(0,r*0.52);ctx.stroke();
  // Crossbar
  ctx.beginPath();ctx.moveTo(-r*0.38,-r*0.05);ctx.lineTo(r*0.38,-r*0.05);ctx.stroke();
  // Flukes
  ctx.beginPath();ctx.moveTo(-r*0.38,r*0.52);ctx.quadraticCurveTo(-r*0.5,r*0.72,0,r*0.62);ctx.stroke();
  ctx.beginPath();ctx.moveTo(r*0.38,r*0.52);ctx.quadraticCurveTo(r*0.5,r*0.72,0,r*0.62);ctx.stroke();
  ctx.restore();
}

function drawSplitter(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  const spin=ts*0.0022;
  ctx.save();
  // Outer glow
  const grd=ctx.createRadialGradient(0,0,r*0.2,0,0,r*2);
  grd.addColorStop(0,"#f97316aa");grd.addColorStop(0.6,"#f9731633");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*2,0,Math.PI*2);ctx.fill();
  // Spinning triangular ring
  ctx.save();ctx.rotate(spin);
  ctx.strokeStyle=`rgba(251,146,60,${0.6+pulse*0.4})`;ctx.lineWidth=2.5;
  ctx.shadowColor="#fb923c";ctx.shadowBlur=14;
  ctx.beginPath();
  for(let i=0;i<3;i++){const a=i*Math.PI*2/3;ctx.lineTo(Math.cos(a)*r*1.25,Math.sin(a)*r*1.25);}
  ctx.closePath();ctx.stroke();ctx.restore();
  // Body — hexagonal-ish glow
  ctx.shadowColor="#f97316";ctx.shadowBlur=r*(0.7+pulse*0.4);
  const body=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  body.addColorStop(0,"#fed7aa");body.addColorStop(0.5,"#f97316");body.addColorStop(1,"#c2410c");
  ctx.fillStyle=body;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Split arrows (3 outward arrows suggesting the split)
  for(let i=0;i<3;i++){
    const a=i*Math.PI*2/3+Math.PI/6;
    ctx.save();ctx.rotate(a);
    ctx.strokeStyle="#ffffff";ctx.lineWidth=r*0.1;ctx.lineCap="round";ctx.shadowColor="#fff";ctx.shadowBlur=4;
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(0,-r*0.55);ctx.stroke();
    ctx.beginPath();ctx.moveTo(-r*0.15,-r*0.35);ctx.lineTo(0,-r*0.55);ctx.lineTo(r*0.15,-r*0.35);ctx.stroke();
    ctx.restore();
  }
  ctx.restore();
}

// ── Shielded target — 2 taps (shield absorbs first) ──
function drawShielded(ctx, r, shieldUp, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.004);
  const spin=ts*0.0015;
  ctx.save();
  // Outer glow
  const grd=ctx.createRadialGradient(0,0,r*0.3,0,0,r*2.1);
  grd.addColorStop(0,"#818cf855");grd.addColorStop(0.6,"#818cf822");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*2.1,0,Math.PI*2);ctx.fill();
  // Target body (indigo)
  ctx.shadowColor="#6366f1";ctx.shadowBlur=r*(0.5+pulse*0.3);
  const body=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  body.addColorStop(0,"#c7d2fe");body.addColorStop(0.5,"#6366f1");body.addColorStop(1,"#3730a3");
  ctx.fillStyle=body;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Shield ring (hexagonal spinning)
  if(shieldUp){
    ctx.save();ctx.rotate(spin);
    ctx.strokeStyle=`rgba(165,180,252,${0.7+pulse*0.3})`;ctx.lineWidth=3;
    ctx.shadowColor="#a5b4fc";ctx.shadowBlur=12+pulse*8;
    ctx.beginPath();
    for(let i=0;i<6;i++){
      const a=i*Math.PI/3;const nr=(i+1)*Math.PI/3;
      ctx.lineTo(Math.cos(a)*r*1.5,Math.sin(a)*r*1.5);
    }
    ctx.closePath();ctx.stroke();
    // Shield "S" icon
    ctx.font=`bold ${r*0.55}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillStyle="rgba(255,255,255,0.9)";ctx.shadowBlur=6;ctx.shadowColor="#a5b4fc";
    ctx.fillText("🛡",0,0);
    ctx.restore();
  } else {
    // Cracked shield (shield broken — one more hit)
    ctx.save();
    ctx.strokeStyle=`rgba(253,186,116,${0.5+pulse*0.3})`;ctx.lineWidth=1.5;
    ctx.setLineDash([4,4]);ctx.lineDashOffset=ts*0.02;
    ctx.beginPath();ctx.arc(0,0,r*1.45,0,Math.PI*2);ctx.stroke();
    ctx.setLineDash([]);
    ctx.font=`bold ${r*0.55}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillStyle="rgba(255,200,100,0.8)";ctx.shadowColor="#fb923c";ctx.shadowBlur=4;
    ctx.fillText("💥",0,0);
    ctx.restore();
  }
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
  // Anticipation ring: show telegraph pulse before target fully appears
  const anticipateMs=t.anticipateMs||0;
  if(anticipateMs>0&&agePn<anticipateMs){
    const pct=agePn/anticipateMs;
    ctx.save();
    ctx.globalAlpha=0.25+pct*0.55;
    ctx.strokeStyle=t.color||"#ffffff";ctx.shadowColor=t.glow||t.color||"#ffffff";ctx.shadowBlur=18;
    ctx.lineWidth=3*(1-pct*0.6);
    ctx.beginPath();ctx.arc(t.x,t.y,t.radius*(2.2-pct*0.9),0,Math.PI*2);ctx.stroke();
    ctx.globalAlpha=(0.18+pct*0.3)*(0.4+0.6*Math.abs(Math.sin(ts/60)));
    ctx.lineWidth=1.5;
    ctx.beginPath();ctx.arc(t.x,t.y,t.radius*(1.5-pct*0.4),0,Math.PI*2);ctx.stroke();
    ctx.restore();
    return; // don't draw full target during anticipation
  }
  const spawnScale=agePn<200?Math.min(1.08,agePn/200*1.08):1;
  let ghostAlpha=1;
  if(t.ghost) ghostAlpha=0.3+0.7*(0.5+0.5*Math.sin(ts/200));
  // Haunted Castle (W7) ghost wave — temporary translucency
  if(t.waveGhost&&Date.now()<t.waveGhost){
    const remaining=(t.waveGhost-Date.now())/1400;
    ghostAlpha*=0.35+0.65*(1-remaining); // dips then recovers
  }

  if(t.moving) drawTrail(ctx,t);

  // Timing ring — shrinks toward target, turns gold in perfect zone
  if(t.type==="normal" && t.rarity){
    const tl=Math.max(0,1-(now-t.spawnedAt)/t.lifetime);
    const ringR=t.radius*(1.18+tl*1.5);
    const inPerfZone=tl>0.36&&tl<0.67;
    ctx.save();ctx.translate(t.x,t.y);
    ctx.globalAlpha=ghostAlpha*(inPerfZone?0.7:0.28+tl*0.22);
    ctx.strokeStyle=inPerfZone?"#ffd700":t.color;
    ctx.lineWidth=inPerfZone?3:1.5;
    if(inPerfZone){ctx.shadowColor="#ffd700";ctx.shadowBlur=12;}
    ctx.beginPath();ctx.arc(0,0,ringR,0,Math.PI*2);ctx.stroke();
    // Second inner ring pulsing in perfect zone
    if(inPerfZone){
      ctx.globalAlpha=0.35+0.3*Math.abs(Math.sin(ts/80));
      ctx.lineWidth=1.5;
      ctx.beginPath();ctx.arc(0,0,t.radius*1.08,0,Math.PI*2);ctx.stroke();
    }
    ctx.restore();
  }

  ctx.save();
  ctx.globalAlpha=ghostAlpha;
  ctx.translate(t.x,t.y);
  ctx.scale(spawnScale,spawnScale);

  if     (t.type==="bomb")     drawBomb(ctx,t.radius,t.color,t.glow,ts);
  else if(t.type==="powerup")  drawPowerup(ctx,t.radius,t.pwrType,ts);
  else if(t.type==="boss")     drawBoss(ctx,t.radius,t.hitsLeft,t.maxHits,ts,t.worldId||1,t.rage||false);
  else if(t.type==="treasure") drawTreasure(ctx,t.radius,ts);
  else if(t.type==="mystery")  drawMystery(ctx,t.radius,ts);
  else if(t.type==="mimic")    drawMimic(ctx,t.radius,ts);
  else if(t.type==="anchor")   drawAnchor(ctx,t.radius,ts);
  else if(t.type==="splitter") drawSplitter(ctx,t.radius,ts);
  else if(t.type==="shielded") drawShielded(ctx,t.radius,t.hitsLeft>=2,ts);
  else{
    const nm=t.rarity?.name;
    if     (nm==="common")    drawCommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="uncommon")  drawUncommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="rare")      drawRare(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="epic")      drawEpic(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="legendary") drawLegendary(ctx,t.radius,t.color,t.glow,ts,timeLeft);
  }
  // Colorblind rarity symbols
  if(_colorblindOn&&t.type==="normal"&&t.rarity){
    const symbols={common:"●",uncommon:"■",rare:"◆",epic:"★",legendary:"♛"};
    const sym=symbols[t.rarity.name]||"●";
    ctx.save();
    ctx.font=`bold ${Math.max(10,t.radius*0.65)}px sans-serif`;
    ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillStyle="#ffffff";ctx.shadowColor="#000";ctx.shadowBlur=4;
    ctx.fillText(sym,0,0);
    ctx.restore();
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
  } else if(p.type==="arc"){
    // Lightning arc from (x,y) to (x2,y2) — chain reaction visual
    ctx.strokeStyle=p.color; ctx.lineWidth=Math.max(1,4*life); ctx.lineCap="round";
    ctx.shadowColor=p.color; ctx.shadowBlur=20;
    ctx.beginPath(); ctx.moveTo(p.x,p.y);
    const segments=6;
    for(let i=1;i<=segments;i++){
      const t=i/segments;
      const lx=p.x+(p.x2-p.x)*t+(Math.random()-0.5)*16*(1-Math.abs(t-0.5)*2);
      const ly=p.y+(p.y2-p.y)*t+(Math.random()-0.5)*16*(1-Math.abs(t-0.5)*2);
      ctx.lineTo(lx,ly);
    }
    ctx.stroke();
  } else if(p.type==="trail"){
    // Cross/star sparkle — perfect-tap trail effect
    const s=Math.max(0,p.size*life);
    ctx.strokeStyle=p.color; ctx.lineWidth=Math.max(0.5,s*0.6); ctx.lineCap="round";
    ctx.shadowColor=p.color; ctx.shadowBlur=s*3;
    ctx.beginPath();ctx.moveTo(p.x-s,p.y);ctx.lineTo(p.x+s,p.y);ctx.stroke();
    ctx.beginPath();ctx.moveTo(p.x,p.y-s);ctx.lineTo(p.x,p.y+s);ctx.stroke();
    ctx.beginPath();ctx.moveTo(p.x-s*0.7,p.y-s*0.7);ctx.lineTo(p.x+s*0.7,p.y+s*0.7);ctx.stroke();
    ctx.beginPath();ctx.moveTo(p.x+s*0.7,p.y-s*0.7);ctx.lineTo(p.x-s*0.7,p.y+s*0.7);ctx.stroke();
  } else {
    ctx.fillStyle=p.color; ctx.shadowColor=p.color; ctx.shadowBlur=p.size*2.5;
    const s=Math.max(0,p.size*life);
    ctx.beginPath(); ctx.arc(p.x,p.y,s,0,Math.PI*2); ctx.fill();
  }
  ctx.restore();
}

// ── World Foreground Silhouettes (drawn AFTER targets for depth) ──
function drawWorldForeground(ctx,w,h,worldId,ts){
  if(!worldId)return;
  const pulse=0.5+0.5*Math.sin(ts*0.0009);
  ctx.save();
  if(worldId===1){
    // Dragon's Lair: stalactites + lava seam
    ctx.fillStyle="rgba(35,4,0,0.88)";
    for(let i=0;i<9;i++){
      const sx=w*0.06+w*0.88*(i/8);
      const sh=18+Math.sin(i*1.9)*15+Math.sin(i*3.1)*8;
      const sw=10+Math.sin(i*2.4)*5;
      ctx.beginPath();ctx.moveTo(sx-sw,0);ctx.lineTo(sx+sw,0);ctx.lineTo(sx,sh);ctx.closePath();ctx.fill();
    }
    // Lava seam glow at bottom
    const lv=ctx.createLinearGradient(0,h-20,0,h);
    lv.addColorStop(0,"transparent");lv.addColorStop(1,`rgba(255,60,0,${0.35+pulse*0.18})`);
    ctx.fillStyle=lv;ctx.fillRect(0,h-20,w,20);
    ctx.strokeStyle=`rgba(255,100,0,${0.5+pulse*0.2})`;ctx.lineWidth=2.5;
    ctx.shadowColor="#ff4500";ctx.shadowBlur=22;
    ctx.beginPath();ctx.moveTo(0,h-3);ctx.lineTo(w,h-3);ctx.stroke();
    // Drip dots
    for(let i=0;i<5;i++){
      const dx=w*0.12+w*0.76*(i/4),dy=h-6-Math.abs(Math.sin(ts*0.0012+i*1.4))*9;
      ctx.fillStyle=`rgba(255,80,0,${0.7+pulse*0.2})`;
      ctx.beginPath();ctx.arc(dx,dy,2.5+Math.abs(Math.sin(ts*0.0018+i))*1.5,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===2){
    // Troll Forest: pine tree silhouettes on sides + ground fog
    const drawPine=(bx,base,h2,w2)=>{
      ctx.fillStyle="rgba(4,18,4,0.9)";
      ctx.beginPath();ctx.moveTo(bx,base);
      ctx.lineTo(bx-w2*0.5,base-h2*0.3);ctx.lineTo(bx-w2*0.3,base-h2*0.3);
      ctx.lineTo(bx-w2*0.42,base-h2*0.58);ctx.lineTo(bx-w2*0.22,base-h2*0.58);
      ctx.lineTo(bx-w2*0.3,base-h2*0.82);ctx.lineTo(bx,base-h2);
      ctx.lineTo(bx+w2*0.3,base-h2*0.82);ctx.lineTo(bx+w2*0.22,base-h2*0.58);
      ctx.lineTo(bx+w2*0.42,base-h2*0.58);ctx.lineTo(bx+w2*0.3,base-h2*0.3);
      ctx.lineTo(bx+w2*0.5,base-h2*0.3);ctx.closePath();ctx.fill();
    };
    drawPine(-10,h*0.95+5,h*0.58,72);drawPine(50,h*0.98+5,h*0.44,55);
    drawPine(w+10,h*0.95+5,h*0.6,72);drawPine(w-50,h*0.98+5,h*0.46,55);
    // Canopy top hint
    const cg=ctx.createLinearGradient(0,0,0,h*0.12);
    cg.addColorStop(0,"rgba(5,22,5,0.6)");cg.addColorStop(1,"transparent");
    ctx.fillStyle=cg;ctx.fillRect(0,0,w,h*0.12);
    // Ground fog
    const fg=ctx.createLinearGradient(0,h*0.78,0,h);
    fg.addColorStop(0,"transparent");fg.addColorStop(1,"rgba(8,28,8,0.65)");
    ctx.fillStyle=fg;ctx.fillRect(0,h*0.78,w,h*0.22);
  } else if(worldId===3){
    // Elven Kingdom: crystal pillar silhouettes at bottom corners + starlight arch
    const drawCrystal=(cx,base,cw2,ch2)=>{
      ctx.fillStyle=`rgba(200,168,75,${0.12+pulse*0.06})`;
      ctx.shadowColor="#c8a84b";ctx.shadowBlur=25;
      ctx.beginPath();ctx.moveTo(cx-cw2*0.28,base);ctx.lineTo(cx-cw2*0.5,base-ch2*0.8);
      ctx.lineTo(cx,base-ch2);ctx.lineTo(cx+cw2*0.5,base-ch2*0.8);
      ctx.lineTo(cx+cw2*0.28,base);ctx.closePath();ctx.fill();
      ctx.shadowBlur=0;
      // Crystal shine
      ctx.fillStyle=`rgba(255,240,180,${0.35+pulse*0.3})`;
      ctx.beginPath();ctx.arc(cx,base-ch2,3.5,0,Math.PI*2);ctx.fill();
    };
    drawCrystal(16,h,14,h*0.22);drawCrystal(44,h-8,10,h*0.16);
    drawCrystal(w-16,h,14,h*0.22);drawCrystal(w-44,h-8,10,h*0.16);
    // Golden arch at top
    ctx.strokeStyle=`rgba(200,168,75,${0.08+pulse*0.04})`;ctx.lineWidth=2;
    ctx.shadowColor="#c8a84b";ctx.shadowBlur=15;
    ctx.beginPath();ctx.arc(w/2,-h*0.3,w*0.65,0,Math.PI);ctx.stroke();
    ctx.shadowBlur=0;
  } else if(worldId===4){
    // Dark Wizard Tower: floating rune sigils + lightning at corners
    const runes=[[w*0.08,h*0.14],[w*0.9,h*0.22],[w*0.05,h*0.74],[w*0.94,h*0.68]];
    runes.forEach(([rx,ry],i)=>{
      const rr=16+i*3;
      ctx.save();ctx.translate(rx,ry);ctx.rotate(ts*0.00025*(i%2?1:-1));
      ctx.strokeStyle=`rgba(155,89,182,${0.22+pulse*0.1})`;
      ctx.lineWidth=1.5;ctx.setLineDash([3,4]);
      ctx.beginPath();ctx.arc(0,0,rr,0,Math.PI*2);ctx.stroke();
      ctx.setLineDash([]);
      for(let p=0;p<6;p++){
        const pa=(p/6)*Math.PI*2;
        ctx.fillStyle=`rgba(155,89,182,${0.45+pulse*0.3})`;
        ctx.beginPath();ctx.arc(Math.cos(pa)*rr,Math.sin(pa)*rr,2,0,Math.PI*2);ctx.fill();
      }
      ctx.restore();
    });
    if(Math.sin(ts*0.023)>0.88){
      ctx.strokeStyle="rgba(180,80,255,0.65)";ctx.lineWidth=1.5;ctx.shadowColor="#9b59b6";ctx.shadowBlur=18;
      ctx.beginPath();ctx.moveTo(8,0);ctx.lineTo(28,22);ctx.lineTo(14,38);ctx.lineTo(40,58);ctx.stroke();
      ctx.beginPath();ctx.moveTo(w-8,0);ctx.lineTo(w-28,22);ctx.lineTo(w-14,38);ctx.lineTo(w-40,58);ctx.stroke();
      ctx.shadowBlur=0;
    }
  } else if(worldId===5){
    // Viking Fjords: mountain silhouettes + aurora edge
    ctx.fillStyle="rgba(4,12,28,0.85)";
    ctx.beginPath();ctx.moveTo(0,h);ctx.lineTo(0,h*0.7);ctx.lineTo(w*0.07,h*0.55);
    ctx.lineTo(w*0.13,h*0.64);ctx.lineTo(w*0.2,h*0.49);ctx.lineTo(w*0.27,h*0.61);ctx.lineTo(w*0.32,h);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(w,h);ctx.lineTo(w,h*0.7);ctx.lineTo(w*0.93,h*0.55);
    ctx.lineTo(w*0.87,h*0.64);ctx.lineTo(w*0.8,h*0.49);ctx.lineTo(w*0.73,h*0.61);ctx.lineTo(w*0.68,h);ctx.closePath();ctx.fill();
    // Snow caps
    ctx.fillStyle=`rgba(200,225,255,${0.32+pulse*0.12})`;
    [[w*0.07,h*0.55,13],[w*0.2,h*0.49,16],[w*0.93,h*0.55,13],[w*0.8,h*0.49,16]].forEach(([px,py,pr])=>{
      ctx.beginPath();ctx.arc(px,py,pr,Math.PI,0);ctx.fill();
    });
    // Aurora edge at top
    const au=ctx.createLinearGradient(0,0,w,h*0.18);
    au.addColorStop(0,"rgba(0,200,120,0)");au.addColorStop(0.4,`rgba(0,180,140,${0.06+pulse*0.04})`);au.addColorStop(0.7,"rgba(0,150,255,0.04)");au.addColorStop(1,"transparent");
    ctx.fillStyle=au;ctx.fillRect(0,0,w,h*0.18);
  } else if(worldId===6){
    // Goblin Mines: mine frame timbers
    const bc="rgba(55,35,8,0.9)";ctx.fillStyle=bc;
    ctx.fillRect(0,h*0.08,18,h*0.84);ctx.fillRect(w-18,h*0.08,18,h*0.84);
    ctx.fillRect(0,h*0.08,w,18);ctx.fillRect(0,h*0.9,w,18);
    [0.28,0.54,0.77].forEach(f=>{
      ctx.fillRect(0,h*f-8,38,16);ctx.fillRect(w-38,h*f-8,38,16);
    });
    // Gold ore glints in walls
    ctx.shadowColor="#ffd700";ctx.shadowBlur=14;
    [[10,h*0.25],[10,h*0.52],[10,h*0.76],[w-10,h*0.3],[w-10,h*0.6],[w-10,h*0.78]].forEach(([gx,gy])=>{
      ctx.fillStyle=`rgba(255,210,0,${0.4+Math.abs(Math.sin(ts*0.002+gx))*0.4})`;
      ctx.beginPath();ctx.arc(gx,gy,3,0,Math.PI*2);ctx.fill();
    });
    ctx.shadowBlur=0;
  } else if(worldId===7){
    // Undead Catacombs: tombstones + bone arch at top
    const drawTomb=(tx,ty,tw2,th2)=>{
      ctx.fillStyle="rgba(12,22,12,0.92)";
      ctx.beginPath();ctx.moveTo(tx-tw2/2,ty+th2);ctx.lineTo(tx-tw2/2,ty+th2*0.3);
      ctx.arc(tx,ty,tw2/2,Math.PI,0);ctx.lineTo(tx+tw2/2,ty+th2);ctx.closePath();ctx.fill();
      // RIP text
      ctx.fillStyle=`rgba(100,150,100,${0.3+pulse*0.15})`;
      ctx.font=`bold ${tw2*0.28}px monospace`;ctx.textAlign="center";ctx.textBaseline="middle";
      ctx.fillText("R.I.P",tx,ty+th2*0.6);
    };
    drawTomb(w*0.07,h-55,32,58);drawTomb(w*0.18,h-50,26,50);
    drawTomb(w*0.82,h-55,28,52);drawTomb(w*0.93,h-50,30,56);
    // Bone arch at top
    ctx.strokeStyle=`rgba(90,130,90,${0.15+pulse*0.07})`;ctx.lineWidth=14;ctx.lineCap="round";
    ctx.beginPath();ctx.arc(w/2,-h*0.25,w*0.6,0,Math.PI);ctx.stroke();
    // Miasma on ground
    const mg=ctx.createLinearGradient(0,h*0.8,0,h);
    mg.addColorStop(0,"transparent");mg.addColorStop(1,"rgba(15,45,15,0.6)");
    ctx.fillStyle=mg;ctx.fillRect(0,h*0.8,w,h*0.2);
  } else if(worldId===8){
    // Sea Serpent's Deep: seaweed + water surface shimmer
    for(let i=0;i<7;i++){
      const sx=w*0.05+w*0.9*(i/6);
      const sh=50+Math.sin(i*1.8)*22;
      ctx.strokeStyle=`rgba(0,110,85,0.72)`;ctx.lineWidth=7+Math.sin(i*1.3)*3;ctx.lineCap="round";
      ctx.shadowColor="#1abc9c";ctx.shadowBlur=6;
      ctx.beginPath();ctx.moveTo(sx,h);
      for(let j=5;j>=0;j--){
        const t=j/5,sway=Math.sin(ts*0.0009+i*0.9+t*Math.PI)*9;
        ctx.lineTo(sx+sway,h-sh*t);
      }
      ctx.stroke();
      ctx.shadowBlur=0;
    }
    // Water caustic flicker at top
    ctx.strokeStyle=`rgba(26,188,156,${0.18+pulse*0.1})`;ctx.lineWidth=2;
    ctx.beginPath();
    for(let x=0;x<=w;x+=18){
      const y=3+Math.sin(x*0.045+ts*0.0007)*4;
      x===0?ctx.moveTo(x,y):ctx.lineTo(x,y);
    }
    ctx.stroke();
    // Bubble highlights top
    const bs=ctx.createLinearGradient(0,0,0,h*0.08);
    bs.addColorStop(0,`rgba(26,188,156,${0.1+pulse*0.05})`);bs.addColorStop(1,"transparent");
    ctx.fillStyle=bs;ctx.fillRect(0,0,w,h*0.08);
  } else if(worldId===9){
    // Giant's Peak: rocky peaks + lightning flash
    ctx.fillStyle="rgba(18,22,32,0.88)";
    ctx.beginPath();ctx.moveTo(0,h);ctx.lineTo(0,h*0.76);ctx.lineTo(w*0.06,h*0.6);
    ctx.lineTo(w*0.12,h*0.7);ctx.lineTo(w*0.19,h*0.53);ctx.lineTo(w*0.25,h*0.66);ctx.lineTo(w*0.3,h);ctx.closePath();ctx.fill();
    ctx.beginPath();ctx.moveTo(w,h);ctx.lineTo(w,h*0.76);ctx.lineTo(w*0.94,h*0.6);
    ctx.lineTo(w*0.88,h*0.7);ctx.lineTo(w*0.81,h*0.53);ctx.lineTo(w*0.75,h*0.66);ctx.lineTo(w*0.7,h);ctx.closePath();ctx.fill();
    ctx.fillStyle=`rgba(215,228,255,${0.28+pulse*0.1})`;
    [[w*0.06,h*0.6,14],[w*0.19,h*0.53,17],[w*0.94,h*0.6,14],[w*0.81,h*0.53,17]].forEach(([px,py,pr])=>{
      ctx.beginPath();ctx.arc(px,py,pr,Math.PI,0);ctx.fill();
    });
    if(Math.sin(ts*0.019)>0.9){
      ctx.strokeStyle="rgba(210,225,255,0.85)";ctx.lineWidth=2.5;ctx.shadowColor="#dce4ff";ctx.shadowBlur=25;
      const lx=w*0.5+Math.sin(ts*0.003)*w*0.18;
      ctx.beginPath();ctx.moveTo(lx,0);ctx.lineTo(lx-12,h*0.28);ctx.lineTo(lx+6,h*0.28);ctx.lineTo(lx-16,h*0.56);ctx.stroke();
      ctx.shadowBlur=0;
    }
  } else if(worldId===10){
    // Ancient Dragon God: temple pillars + sacred altar
    const drawPillar=(cx,y0,cw2,ch2)=>{
      ctx.fillStyle=`rgba(170,120,8,${0.28+pulse*0.08})`;
      ctx.shadowColor="#ffd700";ctx.shadowBlur=22;
      ctx.fillRect(cx-cw2*0.75,y0,cw2*1.5,ch2*0.06);
      ctx.fillRect(cx-cw2*0.5,y0+ch2*0.06,cw2,ch2*0.88);
      ctx.fillRect(cx-cw2*0.75,y0+ch2*0.94,cw2*1.5,ch2*0.06);
      ctx.shadowBlur=0;
      ctx.strokeStyle="rgba(255,200,50,0.12)";ctx.lineWidth=1;
      for(let li=0;li<3;li++){
        ctx.beginPath();ctx.moveTo(cx-cw2*0.3+li*cw2*0.3,y0+ch2*0.07);
        ctx.lineTo(cx-cw2*0.3+li*cw2*0.3,y0+ch2*0.93);ctx.stroke();
      }
    };
    drawPillar(12,h*0.04,22,h*0.96);drawPillar(w-12,h*0.04,22,h*0.96);
    // Sacred altar glow at bottom
    const ag=ctx.createLinearGradient(w*0.3,h-10,w*0.7,h-10);
    ag.addColorStop(0,"transparent");ag.addColorStop(0.5,`rgba(255,200,0,${0.3+pulse*0.14})`);ag.addColorStop(1,"transparent");
    ctx.fillStyle=ag;ctx.fillRect(w*0.3,h-10,w*0.4,10);
    // Sacred glow pillar
    const sp=ctx.createLinearGradient(w*0.42,0,w*0.58,0);
    sp.addColorStop(0,"transparent");sp.addColorStop(0.5,`rgba(255,200,0,${0.04+pulse*0.03})`);sp.addColorStop(1,"transparent");
    ctx.fillStyle=sp;ctx.fillRect(w*0.42,0,w*0.16,h);
  }
  ctx.restore();
}

// ── Depth vignette ──
function drawVignette(ctx,w,h,worldColor){
  const vg=ctx.createRadialGradient(w/2,h/2,w*0.28,w/2,h/2,w*0.9);
  vg.addColorStop(0,"transparent");
  vg.addColorStop(1,"rgba(0,0,0,0.72)");
  ctx.fillStyle=vg;ctx.fillRect(0,0,w,h);
  if(worldColor){
    const eg=ctx.createRadialGradient(w/2,h/2,w*0.55,w/2,h/2,w*1.05);
    eg.addColorStop(0,"transparent");
    eg.addColorStop(1,worldColor+"18");
    ctx.fillStyle=eg;ctx.fillRect(0,0,w,h);
  }
}

// ── Background ──
function drawBg(ctx,w,h,accent,gridColor,ts,fever,worldId=0){
  ctx.clearRect(0,0,w,h);
  // Fill with world background color
  if(worldId>0){ctx.fillStyle=WORLDS[worldId-1].bg;ctx.fillRect(0,0,w,h);}
  const pulse=0.5+0.5*Math.sin(ts/1500);

  // ── World-specific atmospheric overlays ──
  if(worldId===1){
    // Dragon's Lair: lava glow rising from bottom, flickering heat
    const g=ctx.createLinearGradient(0,h*0.55,0,h);
    g.addColorStop(0,"transparent");
    g.addColorStop(1,`rgba(200,40,0,${0.15+pulse*0.08})`);
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Side lava veins glow
    const gl=ctx.createLinearGradient(0,0,w*0.25,0);
    gl.addColorStop(0,`rgba(255,60,0,${0.07+pulse*0.04})`); gl.addColorStop(1,"transparent");
    ctx.fillStyle=gl; ctx.fillRect(0,0,w,h);
  } else if(worldId===2){
    // Troll Forest: mist settling from top, deep green murk
    const g=ctx.createLinearGradient(0,0,0,h*0.45);
    g.addColorStop(0,`rgba(10,40,10,${0.18+pulse*0.06})`); g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    const g2=ctx.createLinearGradient(0,h*0.7,0,h);
    g2.addColorStop(0,"transparent"); g2.addColorStop(1,`rgba(5,30,5,${0.14+pulse*0.04})`);
    ctx.fillStyle=g2; ctx.fillRect(0,0,w,h);
  } else if(worldId===3){
    // Elven Kingdom: magical radial shimmer
    const g=ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,w*0.65);
    g.addColorStop(0,`rgba(200,168,75,${0.05+pulse*0.04})`); g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Silver edge glow
    const g2=ctx.createRadialGradient(w/2,h/2,w*0.3,w/2,h/2,w*0.8);
    g2.addColorStop(0,"transparent"); g2.addColorStop(1,`rgba(180,220,255,${0.04+pulse*0.02})`);
    ctx.fillStyle=g2; ctx.fillRect(0,0,w,h);
  } else if(worldId===4){
    // Dark Wizard Tower: arcane vortex glow from center
    const g=ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,w*0.55);
    g.addColorStop(0,`rgba(100,20,160,${0.10+pulse*0.06})`); g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Lightning flicker at top
    if(Math.sin(ts*0.03)>0.85){
      ctx.fillStyle=`rgba(150,50,255,${0.06})`; ctx.fillRect(0,0,w,h*0.3);
    }
  } else if(worldId===5){
    // Viking Fjords: aurora borealis shimmer + ice haze
    const g=ctx.createLinearGradient(0,0,0,h*0.5);
    g.addColorStop(0,`rgba(0,60,100,${0.16+pulse*0.06})`);
    g.addColorStop(0.5,`rgba(0,80,60,${0.08+pulse*0.03})`);
    g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Aurora band
    ctx.save(); ctx.globalAlpha=0.05+Math.abs(Math.sin(ts*0.0005))*0.05;
    const ga=ctx.createLinearGradient(0,h*0.05,w,h*0.2);
    ga.addColorStop(0,"rgba(0,200,100,0)"); ga.addColorStop(0.5,"rgba(0,200,150,1)"); ga.addColorStop(1,"rgba(0,150,255,0)");
    ctx.fillStyle=ga; ctx.fillRect(0,h*0.05,w,h*0.15); ctx.restore();
  } else if(worldId===6){
    // Goblin Mines: golden ore glow from below, dusty cave
    const g=ctx.createRadialGradient(w/2,h,0,w/2,h,w*0.8);
    g.addColorStop(0,`rgba(180,130,0,${0.12+pulse*0.06})`); g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Rocky walls darkening sides
    const gl=ctx.createLinearGradient(0,0,w*0.2,0);
    gl.addColorStop(0,`rgba(30,20,0,0.22)`); gl.addColorStop(1,"transparent");
    ctx.fillStyle=gl; ctx.fillRect(0,0,w,h);
    const gr=ctx.createLinearGradient(w,0,w*0.8,0);
    gr.addColorStop(0,`rgba(30,20,0,0.22)`); gr.addColorStop(1,"transparent");
    ctx.fillStyle=gr; ctx.fillRect(0,0,w,h);
  } else if(worldId===7){
    // Undead Catacombs: sickly green miasma on the ground, bone-cold
    const g=ctx.createLinearGradient(0,h*0.65,0,h);
    g.addColorStop(0,"transparent"); g.addColorStop(1,`rgba(20,60,15,${0.18+pulse*0.06})`);
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    const g2=ctx.createLinearGradient(0,0,0,h*0.3);
    g2.addColorStop(0,`rgba(5,10,5,0.25)`); g2.addColorStop(1,"transparent");
    ctx.fillStyle=g2; ctx.fillRect(0,0,w,h);
  } else if(worldId===8){
    // Sea Serpent's Deep: bioluminescent depth gradient, caustic shimmer
    const g=ctx.createLinearGradient(0,0,0,h);
    g.addColorStop(0,`rgba(0,40,60,${0.12+pulse*0.04})`);
    g.addColorStop(1,`rgba(0,80,70,${0.18+pulse*0.06})`);
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Caustic light patches
    ctx.save(); ctx.globalAlpha=0.03+Math.abs(Math.sin(ts*0.0008))*0.03;
    for(let i=0;i<3;i++){
      const gci=ctx.createRadialGradient((w*0.2+i*w*0.3),h*0.4,0,(w*0.2+i*w*0.3),h*0.4,w*0.25);
      gci.addColorStop(0,"rgba(26,188,156,0.6)"); gci.addColorStop(1,"transparent");
      ctx.fillStyle=gci; ctx.fillRect(0,0,w,h);
    }
    ctx.restore();
  } else if(worldId===9){
    // Giant's Peak: stormy sky from top, icy mountain base
    const g=ctx.createLinearGradient(0,0,0,h*0.6);
    g.addColorStop(0,`rgba(30,40,60,${0.20+pulse*0.06})`);
    g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    // Lightning flash
    if(Math.sin(ts*0.017)>0.92){
      ctx.fillStyle=`rgba(176,184,193,0.08)`; ctx.fillRect(0,0,w,h);
    }
  } else if(worldId===10){
    // Ancient Dragon God: divine golden radiance, sacred fire
    const g=ctx.createRadialGradient(w/2,h/2,0,w/2,h/2,w*0.7);
    g.addColorStop(0,`rgba(200,150,0,${0.08+pulse*0.05})`); g.addColorStop(1,"transparent");
    ctx.fillStyle=g; ctx.fillRect(0,0,w,h);
    const g2=ctx.createLinearGradient(0,h*0.6,0,h);
    g2.addColorStop(0,"transparent"); g2.addColorStop(1,`rgba(180,80,0,${0.12+pulse*0.06})`);
    ctx.fillStyle=g2; ctx.fillRect(0,0,w,h);
    // Sacred pillar glow
    ctx.save(); ctx.globalAlpha=0.04+pulse*0.03;
    const gp=ctx.createLinearGradient(w*0.35,0,w*0.65,0);
    gp.addColorStop(0,"transparent"); gp.addColorStop(0.5,"rgba(255,215,0,0.8)"); gp.addColorStop(1,"transparent");
    ctx.fillStyle=gp; ctx.fillRect(w*0.35,0,w*0.3,h); ctx.restore();
  }

  // ── Grid (world-specific style) ──
  const gsize = worldId===6 ? 36 : worldId===8 ? 52 : 44;
  ctx.strokeStyle=gridColor; ctx.lineWidth=0.7;
  if(worldId===8){
    // Ocean: undulating wave lines
    for(let y=0;y<h;y+=gsize){
      ctx.beginPath();
      for(let x=0;x<=w;x+=10){
        const wave=Math.sin((x*0.03)+(ts*0.0006))*7;
        x===0?ctx.moveTo(x,y+wave):ctx.lineTo(x,y+wave);
      }
      ctx.stroke();
    }
    for(let x=0;x<w;x+=gsize){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
  } else if(worldId===2){
    // Forest: slightly diagonal grid for organic feel
    for(let x=-h;x<w+h;x+=gsize){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x+h*0.08,h);ctx.stroke();}
    for(let y=0;y<h;y+=gsize){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  } else {
    for(let x=0;x<w;x+=gsize){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
    for(let y=0;y<h;y+=gsize){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  }

  // ── Accent lines ──
  ctx.strokeStyle=accent; ctx.globalAlpha=(0.07+pulse*0.05)*(fever?3:1); ctx.lineWidth=1.2;
  for(let x=0;x<w;x+=gsize*5){ctx.beginPath();ctx.moveTo(x,0);ctx.lineTo(x,h);ctx.stroke();}
  for(let y=0;y<h;y+=gsize*5){ctx.beginPath();ctx.moveTo(0,y);ctx.lineTo(w,y);ctx.stroke();}
  ctx.globalAlpha=1;
}

function drawBgParticles(ctx,parts,accent,fever,worldId=0,speedMult=1){
  const cw=ctx.canvas.width,ch=ctx.canvas.height;
  const sm=speedMult*(fever?1.8:1); // fever already boosted alpha below
  // Boss kill blast: repel bg particles from explosion point for ~700ms
  const blastAge=_bgBlast?(performance.now()-_bgBlast.at):99999;
  const blastActive=blastAge<700;
  if(blastActive&&blastAge>700)_bgBlast=null;
  parts.forEach(p=>{
    if(blastActive){
      const force=Math.max(0,1-blastAge/700)*14;
      const dx=p.x-_bgBlast.x,dy=p.y-_bgBlast.y;
      const dist=Math.max(Math.hypot(dx,dy),1);
      p.x+=(dx/dist)*force;p.y+=(dy/dist)*force;
    }
    const wid=p.worldId||worldId;
    // World-specific movement
    if(wid===1){
      p.x+=(p.vx+Math.sin(p.phase+(performance.now()*0.001))*0.3)*sm;
      p.y+=p.vy*sm;
      if(p.y<-10){p.y=ch+10;p.x=Math.random()*cw;}
      if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;
    } else if(wid===2){
      p.x+=(p.vx+Math.sin(p.phase+(performance.now()*0.0008))*0.4)*sm;
      p.y+=Math.abs(p.vy)*0.8*sm;
      p.angle=(p.angle||0)+0.02*sm;
      if(p.y>ch+10){p.y=-10;p.x=Math.random()*cw;}
      if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;
    } else if(wid===5||wid===9){
      p.x+=Math.sin(p.phase+(performance.now()*0.0006))*0.5*sm;
      p.y+=(Math.abs(p.vy)*0.6+0.3)*sm;
      if(p.y>ch+10){p.y=-10;p.x=Math.random()*cw;}
      if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;
    } else if(wid===8){
      p.x+=Math.sin(p.phase+(performance.now()*0.001))*0.4*sm;
      p.y-=(Math.abs(p.vy)*0.5+0.2)*sm;
      if(p.y<-10){p.y=ch+10;p.x=Math.random()*cw;}
    } else if(wid===7){
      p.x+=Math.sin(p.phase+(performance.now()*0.0007))*0.8*sm;
      p.y+=Math.cos(p.phase+(performance.now()*0.0005))*0.5*sm;
      if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;if(p.y<0)p.y=ch;if(p.y>ch)p.y=0;
    } else {
      p.x+=p.vx*sm; p.y+=p.vy*sm;
      if(p.x<0)p.x=cw;if(p.x>cw)p.x=0;if(p.y<0)p.y=ch;if(p.y>ch)p.y=0;
    }

    ctx.save();
    ctx.globalAlpha=p.alpha*(fever?1.8:1);
    const pcolor=fever?"#ffd700":(p.color||accent);
    ctx.fillStyle=pcolor; ctx.shadowColor=pcolor; ctx.shadowBlur=p.r*4;

    if(wid===8){
      // Bubbles: hollow circle
      ctx.globalAlpha*=0.6;
      ctx.strokeStyle=pcolor; ctx.lineWidth=0.8; ctx.shadowBlur=p.r*2;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.stroke();
    } else if(wid===2){
      // Leaves: small elongated shape
      ctx.save(); ctx.translate(p.x,p.y); ctx.rotate(p.angle||0);
      ctx.fillStyle=pcolor; ctx.shadowBlur=p.r*2;
      ctx.beginPath();
      ctx.ellipse(0,0,p.r*1.6,p.r*0.7,0,0,Math.PI*2);
      ctx.fill(); ctx.restore();
    } else if(wid===5||wid===9){
      // Snowflakes: 6-pointed star
      ctx.save(); ctx.translate(p.x,p.y); ctx.rotate((performance.now()*0.0005*(p.phase||1)));
      ctx.strokeStyle=pcolor; ctx.lineWidth=0.9; ctx.shadowBlur=p.r*3;
      for(let i=0;i<6;i++){
        ctx.beginPath(); ctx.moveTo(0,0);
        ctx.lineTo(Math.cos(i*Math.PI/3)*p.r*1.5,Math.sin(i*Math.PI/3)*p.r*1.5);
        ctx.stroke();
      }
      ctx.restore();
    } else if(wid===3){
      // Sparkles: cross/star flash
      ctx.save(); ctx.translate(p.x,p.y);
      ctx.strokeStyle=pcolor; ctx.lineWidth=0.8; ctx.shadowBlur=p.r*5;
      const sz=p.r*(1+0.3*Math.sin(performance.now()*0.004+p.phase));
      ctx.beginPath(); ctx.moveTo(-sz,0); ctx.lineTo(sz,0); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(0,-sz); ctx.lineTo(0,sz); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(-sz*0.7,-sz*0.7); ctx.lineTo(sz*0.7,sz*0.7); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(sz*0.7,-sz*0.7); ctx.lineTo(-sz*0.7,sz*0.7); ctx.stroke();
      ctx.restore();
    } else if(wid===1){
      // Embers: tiny bright dot with flicker
      const flickAlpha=0.4+0.6*Math.abs(Math.sin(performance.now()*0.006+p.phase));
      ctx.globalAlpha*=flickAlpha;
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
    } else {
      ctx.beginPath(); ctx.arc(p.x,p.y,p.r,0,Math.PI*2); ctx.fill();
    }
    ctx.restore();
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
      className={`shine-btn select-none rounded-2xl font-bold text-white ${className}`}
      style={{
        transform:pressed?"scale(0.92)":"scale(1)",
        opacity:disabled?0.35:1,
        cursor:disabled?"not-allowed":"pointer",
        userSelect:"none",WebkitTapHighlightColor:"transparent",
        transition:pressed?"transform 0.06s ease":"transform 0.12s cubic-bezier(0.34,1.56,0.64,1)",
        letterSpacing:"0.04em",fontFamily:"inherit",
        ...style
      }}>
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
  const [legendaryFlash,setLegendaryFlash]= useState(false);
  const [feverBorder,   setFeverBorder]   = useState(false);
  const [perfectFlash,  setPerfectFlash]  = useState(false);
  const [levelCompleteData, setLevelCompleteData] = useState(null);
  const [gameOverData,      setGameOverData]      = useState(null);
  const [selectedLevel,     setSelectedLevel]     = useState(1);
  const [scrollToLevel,     setScrollToLevel]     = useState(null);
  const [storyData,         setStoryData]         = useState(null); // {worldId, type:'world'|'main', onDone:fn}
  const [streakShieldActive,setStreakShieldActive] = useState(false);
  const [luckyMode,         setLuckyMode]         = useState(false);
  const [newRecord,         setNewRecord]         = useState(false);
  const [closeBanner,       setCloseBanner]       = useState(false); // "SO CLOSE!" banner
  const luckyRef    = useRef(null);   // null | "active" | "countdown"
  const luckyTimer  = useRef(null);
  const streakShRef = useRef(false);
  const [tutStep,       setTutStep]       = useState(null);
  const [mascotMood,    setMascotMood]    = useState("idle");
  const [mascotDancing, setMascotDancing] = useState(false);
  const [mascotUnlockedData, setMascotUnlockedData] = useState(null); // newly unlocked mascot
  const [dailyBonusData, setDailyBonusData] = useState(null); // {day, coins, xp, isWeekly}
  const [offlineCoinsData, setOfflineCoinsData] = useState(null); // {coins, hours} shown once on startup
  const [weeklyRecapData,  setWeeklyRecapData]  = useState(null); // {levelsPlayed, bestScore, coinsEarned, streak} on Sunday
  const [shopConfirm, setShopConfirm] = useState(null); // {total, items, onConfirm}
  const [spinState,     setSpinState]     = useState(null);
  const [spinResult,    setSpinResult]    = useState(null);
  const [spinDeg,       setSpinDeg]       = useState(0);
  const [streakBurst,   setStreakBurst]   = useState(null); // null | {n, label, color}
  // Las Vegas mechanics
  const [mysteryReveal,  setMysteryReveal]  = useState(null); // null | {phase,reels,prize}
  const tensionRef                          = useRef(0);
  const [tensionLevel,   setTensionLevel]   = useState(0);   // 0-4
  const [rescueSecondsLeft,setRescueSecondsLeft]=useState(0);// 0 = no rescue offered
  const rescuedRef                          = useRef(false);
  const [bonusRound,     setBonusRound]     = useState(false);
  const [displayedCoins, setDisplayedCoins] = useState(0);
  const [displayedXP,    setDisplayedXP]    = useState(0);
  const [payoutDone,     setPayoutDone]     = useState(false);
  // Mascot speech bubble
  const [mascotSpeech,   setMascotSpeech]  = useState(null);
  const speechTimerRef                      = useRef(null);
  const [mascotBounce,   setMascotBounce]  = useState(false);
  const bounceTimerRef                      = useRef(null);
  // New features
  const [streakDecaying, setStreakDecaying] = useState(false);
  const decayTimerRef                       = useRef(null);
  const [achPopup, setAchPopup]             = useState(null); // {icon, label, xp}
  const [replayModal,    setReplayModal]    = useState(null); // null | levelId
  const [infinityRound,  setInfinityRound]  = useState(1);
  const [gauntletState,  setGauntletState]  = useState(null); // null | {bossIndex, lives, score}
  const [prestigeAnim,   setPrestigeAnim]   = useState(false);
  const [chainFlash,     setChainFlash]     = useState(null); // null | {label, at}
  const [lbTab,          setLbTab]          = useState("all"); // "today"|"week"|"all"
  const [zenWorld,       setZenWorld]       = useState(1);    // world selector for zen mode

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

  // View Transition helper — smooth animated screen changes
  const go = useCallback((s)=>{
    if(typeof document.startViewTransition==="function"){
      document.startViewTransition(()=>{flushSync(()=>setScreen(s));});
    }else{
      setScreen(s);
    }
  },[]);

  // GSAP screen entrance — bounces/fades new screen content when screen changes
  useLayoutEffect(()=>{
    if(screen==="playing")return; // no entrance for game canvas
    const el=document.querySelector(".screen-root");
    if(!el)return;
    gsap.fromTo(el,{opacity:0,y:16},{opacity:1,y:0,duration:0.28,ease:"power2.out",clearProps:"all"});
  },[screen]);
  const sfx=useCallback((n,...args)=>{if(soundOn&&audioRef.current?.[n])audioRef.current[n](...args);},[soundOn]);

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
    if(ach){
      sv.xp+=ach.xp||0;
      // Mid-game: show rich popup; out of game: use notif toast
      if(gsRef.current){
        setAchPopup({icon:ach.icon,label:ach.label,xp:ach.xp||0});
        setTimeout(()=>setAchPopup(null),2200);
      } else {
        setNotif(`${ach.icon} ${ach.label}!`);
      }
    }
    debounceSave();
  },[debounceSave]);

  // Daily login — 7-day rotating reward calendar
  useEffect(()=>{
    const sv=saveRef.current, today=getTodayKey();
    if(sv.lastLoginDate===today)return;
    const yesterday=(d=>{d.setDate(d.getDate()-1);return`${d.getFullYear()}-${d.getMonth()}-${d.getDate()}`;})(new Date());
    sv.loginStreak=sv.lastLoginDate===yesterday?(sv.loginStreak||0)+1:1;
    sv.lastLoginDate=today;
    // 7-day cycle — day 7 = jackpot, then resets
    const dayInCycle=((sv.loginStreak-1)%7)+1; // 1..7
    const COIN_REWARD=[40,60,80,120,160,220,400]; // day 1..7
    const XP_REWARD=[25,35,50,75,100,140,250];
    const coinsGiven=COIN_REWARD[dayInCycle-1];
    const xpGiven=XP_REWARD[dayInCycle-1];
    sv.coins=(sv.coins||0)+coinsGiven;
    sv.totalCoins=(sv.totalCoins||0)+coinsGiven;
    sv.xp+=xpGiven;
    if(sv.loginStreak>=7)unlock("daily_7");
    flushSave();
    // Show popup
    setDailyBonusData({day:dayInCycle,streak:sv.loginStreak,coins:coinsGiven,xp:xpGiven,isJackpot:dayInCycle===7});
  },[]);// eslint-disable-line

  // Offline coins — award coins earned while away (max 4 hours, 1 coin/10s)
  useEffect(()=>{
    const sv=saveRef.current;
    const earned=calcOfflineCoins(sv.lastActiveTime);
    if(earned>=5){ // only show if at least 5 coins earned
      sv.coins=(sv.coins||0)+earned;
      sv.totalCoins=(sv.totalCoins||0)+earned;
      const hoursAway=Math.max(0,(Date.now()-(sv.lastActiveTime||Date.now())))/3600000;
      setOfflineCoinsData({coins:earned,hours:Math.min(4,hoursAway)});
      // Achievement: earned coins offline
      if(!sv.unlockedAchievements?.includes("offline_earn")){
        sv.unlockedAchievements=[...(sv.unlockedAchievements||[]),"offline_earn"];
        const ach=ACHIEVEMENTS.find(a=>a.id==="offline_earn");
        if(ach)sv.xp=(sv.xp||0)+(ach.xp||0);
      }
      flushSave();
    }
    // Track active time — update on mount and on page unload
    sv.lastActiveTime=Date.now();
    const onHide=()=>{saveRef.current.lastActiveTime=Date.now();flushSave();};
    document.addEventListener("visibilitychange",onHide);
    window.addEventListener("pagehide",onHide);
    return()=>{document.removeEventListener("visibilitychange",onHide);window.removeEventListener("pagehide",onHide);};
  },[]);// eslint-disable-line

  // Weekly recap — shown on Sunday if player hasn't seen it this week (12C)
  useEffect(()=>{
    const today=new Date();
    if(today.getDay()!==0)return; // only Sunday (0)
    const sv=saveRef.current;
    const wk=getWeekKey();
    if((sv.lastWeeklyRecap||"")===wk)return; // already shown this week
    // Gather this week's data from timestamped scores
    const weekScores=(sv.scores||[]).map(e=>typeof e==="number"?{score:e,week:""}:e).filter(e=>e.week===wk);
    if(weekScores.length===0)return; // nothing to recap
    const bestScore=Math.max(...weekScores.map(e=>e.score));
    const levelsPlayed=weekScores.length;
    // Approximate weekly XP and coins from differences — use rough estimate
    const weeklyCoins=Math.round(weekScores.reduce((s,e)=>s+e.score*0.14,0));
    sv.lastWeeklyRecap=wk;
    flushSave();
    setWeeklyRecapData({levelsPlayed,bestScore,coinsEarned:weeklyCoins,weekKey:wk});
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
  const initBgParts=useCallback((worldId=0)=>{
    const w=window.innerWidth,h=window.innerHeight;
    // World-specific particle configs
    const cfgs={
      1: ()=>({ color:"#ff5500", r:Math.random()*1.8+0.6, vx:(Math.random()-0.5)*0.4, vy:-(Math.random()*0.6+0.2), alpha:Math.random()*0.5+0.2, phase:Math.random()*Math.PI*2 }),
      2: ()=>({ color:Math.random()>0.5?"#3cb371":"#2d8a55", r:Math.random()*2.5+1, vx:(Math.random()-0.5)*0.5, vy:Math.random()*0.3+0.1, alpha:Math.random()*0.4+0.15, phase:Math.random()*Math.PI*2, angle:Math.random()*Math.PI*2 }),
      3: ()=>({ color:Math.random()>0.5?"#ffd700":"#c8a84b", r:Math.random()*1.5+0.5, vx:(Math.random()-0.5)*0.4, vy:(Math.random()-0.5)*0.4, alpha:Math.random()*0.45+0.15, phase:Math.random()*Math.PI*2 }),
      4: ()=>({ color:Math.random()>0.5?"#9b59b6":"#6c3483", r:Math.random()*2+0.8, vx:(Math.random()-0.5)*0.35, vy:(Math.random()-0.5)*0.35, alpha:Math.random()*0.35+0.1, phase:Math.random()*Math.PI*2 }),
      5: ()=>({ color:"#a8d8f0", r:Math.random()*2+0.6, vx:(Math.random()-0.5)*0.3, vy:Math.random()*0.4+0.15, alpha:Math.random()*0.5+0.2, phase:Math.random()*Math.PI*2 }),
      6: ()=>({ color:Math.random()>0.4?"#e8c020":"#ffd700", r:Math.random()*1.4+0.5, vx:(Math.random()-0.5)*0.5, vy:(Math.random()-0.5)*0.3, alpha:Math.random()*0.5+0.2, phase:Math.random()*Math.PI*2 }),
      7: ()=>({ color:Math.random()>0.5?"#7fad7a":"#b0c9a0", r:Math.random()*2.5+1, vx:(Math.random()-0.5)*0.25, vy:(Math.random()-0.5)*0.2, alpha:Math.random()*0.3+0.08, phase:Math.random()*Math.PI*2 }),
      8: ()=>({ color:Math.random()>0.5?"#1abc9c":"#a8f0e0", r:Math.random()*3+1, vx:(Math.random()-0.5)*0.2, vy:-(Math.random()*0.4+0.1), alpha:Math.random()*0.35+0.1, phase:Math.random()*Math.PI*2 }),
      9: ()=>({ color:Math.random()>0.6?"#ffffff":"#b0b8c1", r:Math.random()*2+0.7, vx:(Math.random()-0.5)*0.3, vy:Math.random()*0.35+0.1, alpha:Math.random()*0.5+0.15, phase:Math.random()*Math.PI*2 }),
      10:()=>({ color:Math.random()>0.5?"#ffd700":"#ff8c00", r:Math.random()*2+0.6, vx:(Math.random()-0.5)*0.35, vy:(Math.random()-0.5)*0.25, alpha:Math.random()*0.45+0.15, phase:Math.random()*Math.PI*2 }),
    };
    const getCfg=cfgs[worldId]||(()=>({ r:Math.random()*2+0.5, vx:(Math.random()-0.5)*0.3, vy:(Math.random()-0.5)*0.3, alpha:Math.random()*0.32+0.06, phase:Math.random()*Math.PI*2 }));
    bgPartsRef.current=Array.from({length:55},()=>({
      x:Math.random()*w, y:Math.random()*h, worldId, ...getCfg(),
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
    // Lucky mode: force legendary rarity!
    const isLucky=luckyRef.current==="active";
    let type="normal",rarity=isLucky?RARITY.LEGENDARY:getRarity(rarityBonus),color,glow,moving=false,ghost=false;
    let pwrType=null,hitsLeft=1,maxHits=1,vx=0,vy=0;
    if(modifier?.type==="final_boss"){
      type="boss";color="#fbbf24";glow="#d97706";maxHits=10;hitsLeft=10;
      moving=true;const a0=Math.random()*Math.PI*2;vx=Math.cos(a0)*0.8;vy=Math.sin(a0)*0.8;
    } else if(r<bossRate&&bossEnabled){
      type="boss";color="#ff6030";glow="#ff2000";maxHits=3;hitsLeft=3;
      // Boss patterns by world — every boss now moves from spawn
      moving=true;const ab=Math.random()*Math.PI*2;const spB=0.7+Math.random()*0.6;
      vx=Math.cos(ab)*spB;vy=Math.sin(ab)*spB;
    } else if(r<(bossRate||0)+effBomb){
      type="bomb";color="#ef4444";glow="#dc2626";sfx("bombSpawn");
    } else if(r<(bossRate||0)+effBomb+0.07){
      type="powerup";color="#60a5fa";glow="#3b82f6";
      const pt=["SHIELD","SLOW","DOUBLE","LIFE","FREEZE"];
      pwrType=pt[Math.floor(Math.random()*pt.length)];
    } else if(r<(bossRate||0)+effBomb+0.07+0.045&&(gs.score>0||Math.random()<0.3)&&luckyRef.current!=="active"){
      // 4.5% treasure chest — the variable reward slot machine
      type="treasure";color="#ffd700";glow="#c8a000";
    } else if((cfg.id||0)>=15&&Math.random()<0.04&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 4% Mimic — copies the last tapped rarity for its score
      type="mimic";color="#c8c8c8";glow="#ffffff";
    } else if((cfg.id||0)>=8&&Math.random()<0.03&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 3% Anchor — freezes all targets for 3s when tapped
      type="anchor";color="#06b6d4";glow="#0e7490";
    } else if((cfg.id||0)>=12&&Math.random()<0.025&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.5% Splitter — splits into 3 small targets when tapped
      type="splitter";color="#f97316";glow="#c2410c";
    } else if((cfg.id||0)>=10&&Math.random()<0.03&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 3% Shielded — requires 2 taps (shield absorbs first hit)
      type="shielded";color="#6366f1";glow="#4f46e5";hitsLeft=2;maxHits=2;
    } else if(Math.random()<0.035&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")&&!gs.mysteryPause){
      // 3.5% Mystery Box — Las Vegas variable-ratio slot machine
      type="mystery";color="#ffd700";glow="#b8860b";
    } else {
      if(gs.bonusRoundActive)rarity=RARITY.LEGENDARY; // Bonus Round: ALL LEGENDARY!
      color=rarity.color;glow=rarity.glow;
      if(Math.random()<effMoving){
        moving=true;const a=Math.random()*Math.PI*2,sp=0.6+Math.random()*1.4;
        vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;
      }
      if(!moving&&Math.random()<effGhost)ghost=true;
    }
    const baseR=type==="boss"?BASE_R*2.4:type==="treasure"?BASE_R*1.7:type==="mystery"?BASE_R*1.5:type==="mimic"?BASE_R*1.35:type==="anchor"?BASE_R*1.3:type==="splitter"?BASE_R*1.4:type==="shielded"?BASE_R*1.25:type==="normal"?BASE_R*(rarity?.size||1):BASE_R;
    const pos=pickPos(baseR);
    let lifetime=cfg.targetLifetime;
    // World modifiers: Ocean Deep (8) — slower targets (calmer waters), longer lifetimes
    if(cfg.world===8)lifetime*=1.15;
    // World modifiers: Goblin Mines (6) — slightly faster targets (more chaotic) — short lifetimes
    if(cfg.world===6)lifetime*=0.92;
    if(activePwrRef.current.some(p=>p.type==="SLOW"&&p.endsAt>Date.now()))lifetime*=1.6;
    if(activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>Date.now())){vx=0;vy=0;}
    // Skill: target_sense — extra lifetime
    const tsk=(saveRef.current.skills||{}).target_sense||0;
    if(tsk>=1)lifetime+=500;if(tsk>=2)lifetime+=500;if(tsk>=3)lifetime+=1000;
    // Normal targets telegraph their position 260ms before becoming active
    const anticipateMs=type==="normal"?260:0;
    // Boss pattern: 4 patterns based on worldId, advances phases as HP drops
    const bossPattern=type==="boss"?(cfg.world%4):null;
    targetsRef.current.push({
      id:Math.random().toString(36).slice(2),type,rarity:type==="normal"?rarity:null,
      x:pos.x,y:pos.y,radius:baseR,color,glow,lifetime,
      spawnedAt:Date.now()+anticipateMs, // lifetime starts after anticipation
      born:performance.now(),anticipateMs,
      moving,ghost,vx,vy,pwrType,hitsLeft,maxHits,trail:moving?[]:null,
      worldId:cfg.world, worldColor:cfg.worldColor,
      bossPattern, bossPhase:1, // phase 1 = full HP, 2 = mid, 3 = rage
      cx:pos.x, cy:pos.y, // anchor for orbit patterns
    });
  },[sfx,pickPos]);

  // Level complete / game over
  const endLevel=useCallback((won)=>{
    const gs=gsRef.current;if(!gs)return;
    if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}
    if(luckyTimer.current){clearTimeout(luckyTimer.current);luckyTimer.current=null;}
    luckyRef.current=null;setLuckyMode(false);
    streakShRef.current=false;setStreakShieldActive(false);
    audioRef.current?.stopBgMusic?.();
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
      const _xpBoostLvl=(sv.skills||{}).xp_boost||0;
      const _xpBoostMult=_xpBoostLvl===3?1.3:_xpBoostLvl===2?1.2:_xpBoostLvl===1?1.1:1.0;
      const _xpBombMult=gs._xpBombActive?2.0:1.0;
      const _challengeMult=cfg._challengeBonus?1.5:1.0;
      let xpEarned=Math.round((Math.floor(score/6)+gs.sessionStats.rareHits*8+gs.sessionStats.bossKills*30+(stars-1)*40)*_xpBoostMult*_xpBombMult*_challengeMult);
      if(gs._xpBombActive)setTimeout(()=>setNotif(`⚡ XP Bomb: ×2 XP! +${xpEarned}xp`),500);
      if(cfg._challengeBonus&&won)setTimeout(()=>setNotif(`⚡ Challenge Bonus: +50% XP!`),400);
      let coinsEarned=Math.floor(score*0.14)+gs.sessionStats.bossKills*20+stars*15;
      // Weekly Challenge bonus
      const wk=getWeekKey();
      if(cfg.id===getWeeklyChallengeLevel()&&!cfg.isInfinity&&!cfg.isGauntlet){
        const wasCompleted=sv.weeklyChallengeDate===wk&&sv.weeklyChallengeCompleted;
        sv.weeklyChallengeDate=wk;
        if(sv.weeklyChallengeDate!==wk||!sv.weeklyChallengeBest)sv.weeklyChallengeBest=0;
        if(score>(sv.weeklyChallengeBest||0))sv.weeklyChallengeBest=score;
        if(!wasCompleted){
          sv.weeklyChallengeCompleted=true;
          coinsEarned+=500;xpEarned+=200;
          unlock("weekly_done");
          setTimeout(()=>setNotif("🗓️ Weekly Challenge Cleared! +500🪙 +200XP"),700);
        }
      }
      // Daily Tournament — 2x coins, track best + rank, log history
      const todayKey=getTodayKey();
      if(cfg.id===getDailyChallengeLevel()&&!cfg.isInfinity&&!cfg.isGauntlet){
        if(sv.tournamentDate!==todayKey){
          // Push previous day to history if it exists
          if(sv.tournamentDate&&sv.tournamentBest>0){
            const prevCfg=getLevelConfig(cfg.id); // close enough; we don't store yesterday's level
            const prevRatio=sv.tournamentBest/(prevCfg.scoreGoal||1);
            const prevRank=prevRatio>=3?"Top 5%":prevRatio>=2.2?"Top 15%":prevRatio>=1.5?"Top 35%":prevRatio>=1?"Top 60%":"Bottom 40%";
            sv.tournamentHistory=[{date:sv.tournamentDate,score:sv.tournamentBest,rank:prevRank},...(sv.tournamentHistory||[])].slice(0,7);
          }
          sv.tournamentDate=todayKey;sv.tournamentBest=0;
        }
        if(score>(sv.tournamentBest||0))sv.tournamentBest=score;
        coinsEarned*=2; // 2× coin reward
        setTimeout(()=>setNotif(`🏆 Tournament! 2× coins: +${coinsEarned}🪙`),700);
        // Tournament Top achievement — Top 15% requires ratio >= 2.2
        if(score/(cfg.scoreGoal||1)>=2.2)unlock("tournament_top");
      }
      const prevLvl=getLvl(sv.xp);sv.xp+=xpEarned;
      if(getLvl(sv.xp)>prevLvl){
        const gained=getLvl(sv.xp)-prevLvl;
        sv.skillPoints=(sv.skillPoints||0)+gained;
        sfx("levelUp");setNotif(`Level Up! Lv ${getLvl(sv.xp)} 🎉  +${gained} Skill Point${gained>1?"s":""}!`);
      }
      sv.coins=(sv.coins||0)+coinsEarned;sv.totalCoins=(sv.totalCoins||0)+coinsEarned;
      if(score>sv.highScore)sv.highScore=score;
      // Per-world best score tracking — 12B
      if(!cfg.isInfinity&&!cfg.isZen&&cfg.world){
        const wb=sv.worldBest||{};
        if(score>(wb[cfg.world]||0))wb[cfg.world]=score;
        sv.worldBest=wb;
      }
      // Timestamped score entry — normalise legacy plain-number entries on read
      sv.scores=[{score,date:getTodayKey(),week:getWeekKey()},...(sv.scores||[]).map(e=>typeof e==="number"?{score:e,date:"2000-0-0",week:"2000-W0"}:e)].slice(0,50);
      if(gs.streak>sv.bestStreak)sv.bestStreak=gs.streak;
      if(stars===3&&cfg.isBoss)unlock("five_star");
      if(cfg.id>=10)unlock("level_10");if(cfg.id>=25)unlock("level_25");if(cfg.id>=50)unlock("level_50");if(cfg.id>=100)unlock("level_100");
      if(stars>=1)unlock("three_stars");
      // three_stars_5: count distinct levels with 3 stars
      const tsCount=Object.values(sv.levelStars||{}).filter(n=>n>=3).length;
      if(tsCount>=5)unlock("three_stars_5");
      // Infinity best update
      if(cfg.isInfinity){
        if(score>(sv.infinityBest||0))sv.infinityBest=score;
        sv.infinityScores=[score,...(sv.infinityScores||[])].slice(0,10).sort((a,b)=>b-a);
      }
      // Zen mode best update
      if(cfg.isZen){
        if(score>(sv.zenBest||0)){sv.zenBest=score;sv.zenBestWorld=cfg.world;}
        coinsEarned+=Math.floor(score*0.08); // bonus coins for zen
        unlock("zen_master");
      }
      // Phase 10A achievement checks
      if(gs.streak>=50||sv.bestStreak>=50)unlock("streak_50");
      if((sv.totalCoins||0)>=500)unlock("coins_500");
      // Track world visits — all_worlds achievement
      const visitedWorlds=new Set(Object.keys(sv.levelStars||{}).map(id=>getLevelConfig(Number(id)).world));
      if(visitedWorlds.size>=10)unlock("all_worlds");
      flushSave();
      const canPrestige=cfg.id===100&&(sv.prestigeLevel||0)<5;
      setLevelCompleteData({score,stars,newStars,xpEarned,coinsEarned,levelId:cfg.id,isLast:cfg.isLast,
        bestStreak:sv.bestStreak,sessionStats:{...gs.sessionStats,timeSurvived},canPrestige});
      setScrollToLevel(cfg.id);
      setMascotMood("victory");setMascotDancing(true);
      // Check mascot unlocks AFTER save is flushed
      const newMascots=checkMascotUnlocks();
      if(newMascots.length>0)setMascotUnlockedData(newMascots[0]);
      go("levelcomplete");
    } else {
      const pct=score/cfg.scoreGoal;
      const isNearMiss=pct>=0.82&&pct<1;
      if(isNearMiss)sfx("nearMiss"); else sfx("gameOver");
      flushSave();
      // Rescue gamble — offer on near-miss if player has enough coins
      if(isNearMiss&&sv.coins>=50){
        setRescueSecondsLeft(6);
      }
      setGameOverData({score,levelId:cfg.id,levelName:cfg.name,scoreGoal:cfg.scoreGoal,
        sessionStats:{...gs.sessionStats,timeSurvived},
        nearMiss:isNearMiss,shortfall:Math.max(0,cfg.scoreGoal-score)});
      go("gameover");
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

    // SHIELDED — first tap destroys shield, second tap scores
    if(hit.type==="shielded"){
      if(hit.hitsLeft>1){
        // Shield absorbs hit — crack it
        hit.hitsLeft=1;
        sfx("nearMiss");vibrate([8,5,8]);
        spawnParticles(hit.x,hit.y,"#a5b4fc",16,"spark");
        spawnParticles(hit.x,hit.y,"#818cf8",6,"dot");
        spawnPopup(hit.x,hit.y-22,"🛡 SHIELD BREAK!","#a5b4fc",15);
        // Brief flash — shield cracked visual already handled by drawShielded(hitsLeft<2)
        return;
      }
      // Shield is broken — final tap scores
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(200*combo*feverMult*prestigeMult); // 2× bonus for persistence
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      gs.sessionStats.rareHits++;
      hit.dying=performance.now();
      const coinBonus=Math.max(2,Math.floor(pts*0.12));
      saveRef.current.coins=(saveRef.current.coins||0)+coinBonus;
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinBonus;
      sfx("rare");vibrate([10,8,25]);
      spawnParticles(hit.x,hit.y,"#6366f1",30,"spark");
      spawnParticles(hit.x,hit.y,"#c7d2fe",12,"dot");
      spawnPopup(hit.x,hit.y-24,`🛡 CRACKED! +${pts}`,"#818cf8",20);
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),600);
      sfx("comboNote",gs.streak);
      unlock("shielded_hit");
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // MIMIC — copies last tapped rarity for its score
    if(hit.type==="mimic"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Use last rarity mult (default UNCOMMON if no recent hit)
      const lastMult=gs.lastRarityMult||RARITY.UNCOMMON.mult;
      const lastColor=gs.lastRarityColor||RARITY.UNCOMMON.color;
      const lastName=gs.lastRarityName||"uncommon";
      const pts=Math.round(lastMult*combo*feverMult*prestigeMult*1.3); // 1.3× mimic bonus
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      if(lastName!=="common")gs.sessionStats.rareHits++;
      // Visual: mimic morphs into the copied rarity color
      hit.dying=performance.now();
      sfx(lastName==="legendary"?"legendary":lastName==="epic"?"epic":lastName==="rare"?"rare":"uncommon");
      vibrate([10,8,10]);
      spawnParticles(hit.x,hit.y,lastColor,30,"spark");
      spawnParticles(hit.x,hit.y,"#ffffff",10,"dot");
      spawnPopup(hit.x,hit.y-22,`🪞 MIMIC! +${pts}`,lastColor,18);
      sfx("comboNote",gs.streak);
      unlock("mimic_hit");
      // Save coins
      saveRef.current.coins=(saveRef.current.coins||0)+Math.max(1,Math.floor(pts*0.09));
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+Math.max(1,Math.floor(pts*0.09));
      // Win check
      const cfg2=levelCfgRef.current;
      if(cfg2){const scoreWin=gs.score>=cfg2.scoreGoal;if(scoreWin&&(!cfg2.modifier||checkModGoal(cfg2.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // ANCHOR — freezes all current targets for 3 seconds
    if(hit.type==="anchor"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const pts=Math.round(120*(gs.feverActive?2:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Freeze all current targets
      const freezeUntil=Date.now()+3000;
      targetsRef.current.forEach(t=>{t._anchorFrozenVx=t.vx;t._anchorFrozenVy=t.vy;t.vx=0;t.vy=0;t._frozenUntil=freezeUntil;});
      gs._anchorFreezeUntil=freezeUntil;
      sfx("powerUp");vibrate([10,8,20,8,10]);
      spawnParticles(hit.x,hit.y,"#06b6d4",22,"dot");
      spawnParticles(hit.x,hit.y,"#67e8f9",10,"spark");
      spawnPopup(hit.x,hit.y-24,"⚓ FROZEN! +"+pts,"#06b6d4",20);
      setScreenShake(false); // not shake — calm freeze effect
      sfx("comboNote",gs.streak);
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // SPLITTER — splits into 3 small targets
    if(hit.type==="splitter"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const pts=Math.round(80*(gs.feverActive?2:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("tap");vibrate([5,5,15]);
      spawnParticles(hit.x,hit.y,"#f97316",18,"spark");
      spawnPopup(hit.x,hit.y-24,"💥 SPLIT! +"+pts,"#f97316",18);
      // Spawn 3 small normal targets radiating outward
      const cfg=levelCfgRef.current;
      for(let i=0;i<3;i++){
        const ang=i*Math.PI*2/3+Math.random()*0.4;
        const sr=BASE_R*0.75;
        const sx=Math.max(sr+8,Math.min((canvasRef.current?.width||360)-sr-8,hit.x+Math.cos(ang)*55));
        const sy=Math.max(sr+8,Math.min((canvasRef.current?.height||720)-sr-8,hit.y+Math.sin(ang)*55));
        const shard={
          id:Math.random().toString(36).slice(2),type:"normal",
          rarity:RARITY.UNCOMMON,color:RARITY.UNCOMMON.color,glow:RARITY.UNCOMMON.glow,
          x:sx,y:sy,radius:sr,
          lifetime:Math.max(1500,(cfg?.targetLifetime||2500)*0.7),
          spawnedAt:Date.now(),born:performance.now(),
          moving:true,vx:Math.cos(ang)*1.2,vy:Math.sin(ang)*1.2,
          ghost:false,hitsLeft:1,maxHits:1,trail:[],
          worldId:cfg?.world||1,worldColor:cfg?.worldColor||"#ff6030",
          _isShard:true, // reward is halved for shards
        };
        targetsRef.current.push(shard);
      }
      sfx("comboNote",gs.streak);
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // TREASURE CHEST — jackpot variable reward
    if(hit.type==="treasure"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const cfg=levelCfgRef.current;
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const rewards=[80,120,200,350,600,1000];
      const reward=rewards[Math.floor(Math.random()*rewards.length)]*combo*feverMult;
      const coins=Math.floor(reward*0.25);
      gs.score+=reward;
      saveRef.current.coins=(saveRef.current.coins||0)+coins;
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coins;
      gs.sessionStats.score=gs.score;
      sfx("jackpot");vibrate([20,15,20,15,40,15,80]);
      spawnParticles(hit.x,hit.y,"#ffd700",60,"spark");
      spawnParticles(hit.x,hit.y,"#ff6030",20,"spark");
      spawnPopup(hit.x,hit.y-28,`💰 +${reward}!`,"#ffd700",22);
      setTimeout(()=>spawnPopup(hit.x,hit.y+10,`+${coins}🪙`,"#ffc800",15),300);
      setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1100);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),500);
      const cfg2=levelCfgRef.current;
      if(cfg2){const scoreWin=gs.score>=cfg2.scoreGoal;if(scoreWin&&(!cfg2.modifier||checkModGoal(cfg2.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // MYSTERY BOX — slot machine reveal
    if(hit.type==="mystery"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      sfx("jackpot");vibrate([20,15,20,15,40]);
      gs.mysteryPause=Date.now()+1600; // prevent new mystery during reveal
      // Pick weighted prize
      const total=MYSTERY_PRIZES.reduce((s,p)=>s+p.weight,0);
      let rand=Math.random()*total;
      let prize=MYSTERY_PRIZES[MYSTERY_PRIZES.length-1];
      for(const p of MYSTERY_PRIZES){rand-=p.weight;if(rand<=0){prize=p;break;}}
      // Build 3 reels — last one is always the actual prize
      const fakeReel=()=>Math.floor(Math.random()*MYSTERY_PRIZES.length);
      const prizeIdx=MYSTERY_PRIZES.indexOf(prize);
      setMysteryReveal({phase:0,reels:[fakeReel(),fakeReel(),prizeIdx],prize,x:hit.x,y:hit.y});
      showMascotSpeech("mystery");
      setTimeout(()=>setMysteryReveal(r=>r?{...r,phase:1}:null),420);
      setTimeout(()=>{setMysteryReveal(r=>r?{...r,phase:2}:null);sfx("coin");vibrate(15);},820);
      setTimeout(()=>{setMysteryReveal(r=>r?{...r,phase:3}:null);sfx("coin");vibrate(15);},1200);
      setTimeout(()=>{
        const gs2=gsRef.current;
        if(gs2){
          if(prize.type==="points"||prize.type==="jackpot"){
            gs2.score+=prize.value;
            spawnPopup(hit.x,hit.y-50,`🎁 +${prize.value}pts!`,"#ffd700",prize.type==="jackpot"?26:22);
            if(prize.type==="jackpot"){setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1200);vibrate([30,15,60]);}
          } else if(prize.type==="coins"){
            saveRef.current.coins=(saveRef.current.coins||0)+prize.value;flushSave();
            spawnPopup(hit.x,hit.y-50,`🪙 +${prize.value}!`,"#ffd700",22);
          } else if(prize.type==="life"){
            gs2.lives=Math.min(MAX_LIVES,gs2.lives+1);
            spawnPopup(hit.x,hit.y-50,"❤️ EXTRA LIFE!","#ef4444",20);
          }
        }
        setMysteryReveal(null);
        sfx("levelComplete");vibrate(40);
        showSpeech(prize.type==="jackpot"?"JACKPOT!! YESSS!! 🌈":"Lucky! Lucky! ⭐");
      },1650);
      return;
    }
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
        gs.lives=Math.max(0,gs.lives-1);gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);
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
      // Phase 2 transition at 66% HP (or 2/3 hits remaining for 3-hit bosses)
      const hpPct=hit.hitsLeft/(hit.maxHits||1);
      if(hpPct<=0.66&&hpPct>0.33&&hit.bossPhase===1){
        hit.bossPhase=2;
        sfx("bossPhase");vibrate([20,10,20]);
        spawnPopup(hit.x,hit.y-50,"💨 PHASE 2!",hit.color||"#ff6030",18);
        setScreenShake(true);setTimeout(()=>setScreenShake(false),350);
        // New random direction, also remember new anchor for orbit pattern
        const a2=Math.random()*Math.PI*2;
        hit.vx=Math.cos(a2)*1.5;hit.vy=Math.sin(a2)*1.5;
        hit.cx=hit.x;hit.cy=hit.y;
        // Spawn 2 mini bombs as backup
        const cfgNow=levelCfgRef.current;
        if(cfgNow&&!cfgNow.isBoss){
          for(let i=0;i<2;i++){
            const ang=Math.random()*Math.PI*2;const dist=60+Math.random()*30;
            targetsRef.current.push({
              id:Math.random().toString(36).slice(2),type:"bomb",
              x:hit.x+Math.cos(ang)*dist,y:hit.y+Math.sin(ang)*dist,
              radius:BASE_R,color:"#ef4444",glow:"#dc2626",
              lifetime:Math.min(3500,cfgNow.targetLifetime*0.55),
              spawnedAt:Date.now(),born:performance.now(),
              moving:false,hitsLeft:1,maxHits:1,
              worldId:cfgNow.world,worldColor:cfgNow.worldColor,
            });
          }
        }
      }
      // Rage mode on last hit (phase 3)
      if(hit.hitsLeft===1&&!hit.rage){
        hit.rage=true;hit.bossPhase=3;hit.moving=true;hit.vx=(Math.random()-0.5)*4;hit.vy=(Math.random()-0.5)*4;
        hit.cx=hit.x;hit.cy=hit.y;
        sfx("bossPhase");vibrate([30,15,30,15,60]);
        spawnPopup(hit.x,hit.y-50,"⚠️ RAGE MODE!","#ff0000",20);
        setScreenShake(true);setTimeout(()=>setScreenShake(false),500);
        // Speed up spawning
        if(levelCfgRef.current)levelCfgRef.current._rageSpawn=true;
      }
      if(hit.hitsLeft<=0){
        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
        sfx("jackpot");vibrate([35,20,35,20,60,20,80]);
        // Confetti explosion in world colors
        const wc=hit.worldColor||hit.color;
        const rainbowColors=["#ff6030","#ffd700","#34d399","#60a5fa","#f472b6","#a78bfa","#ff6b35"];
        rainbowColors.forEach(c=>spawnParticles(hit.x,hit.y,c,18,"spark"));
        spawnParticles(hit.x,hit.y,"#ffffff",25,"dot");
        setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1200);
        setScreenShake(true);setTimeout(()=>setScreenShake(false),600);
        const pts=800*Math.min(10,1+Math.floor(gs.streak/5))*(gs.feverActive?2:1);
        gs.score+=pts;gs.sessionStats.bossKills=(gs.sessionStats.bossKills||0)+1;
        _bgBlast={x:hit.x,y:hit.y,at:performance.now()}; // explode bg particles
        spawnPopup(hit.x,hit.y-28,`🏆 BOSS! +${pts}`,"#ffd700",24);
        unlock("boss_kill");
        // Boss loot drop — guaranteed rare reward
        {
          const totalW=BOSS_LOOT.reduce((s,l)=>s+l.weight,0);
          let r=Math.random()*totalW,loot=BOSS_LOOT[BOSS_LOOT.length-1];
          for(const l of BOSS_LOOT){r-=l.weight;if(r<=0){loot=l;break;}}
          const amount=loot.min===loot.max?loot.min:Math.floor(loot.min+Math.random()*(loot.max-loot.min+1));
          const sv2=saveRef.current;
          if(loot.type==="coins"){sv2.coins+=amount;sv2.totalCoins=(sv2.totalCoins||0)+amount;sfx("coin");}
          else if(loot.type==="xp"){sv2.xp=(sv2.xp||0)+amount;}
          else if(loot.type==="fragment"){
            sv2.bossFragments=(sv2.bossFragments||0)+1;
            if(sv2.bossFragments>=10){
              // Every 10 fragments unlock a random unowned accessory
              const allAcc=["hat","crown","glasses","halo","bow","star"];
              const owned=sv2.ownedAccessories||{};
              const avail=allAcc.filter(id=>!Object.keys(owned).some(k=>k.endsWith(":"+id)));
              if(avail.length>0){
                const pick=avail[Math.floor(Math.random()*avail.length)];
                const key=(sv2.mascotId||"dragon")+":"+pick;
                sv2.ownedAccessories={...owned,[key]:true};
                sv2.bossFragments-=10;
                // Celebration — rainbow flash + particles + notification
                setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1000);
                sfx("jackpot");vibrate([20,10,20,10,40,10,60]);
                const cx=canvasRef.current?canvasRef.current.width/2:180;
                const cy=canvasRef.current?canvasRef.current.height/2:360;
                ["#c084fc","#ffd700","#ff6030","#34d399","#60a5fa","#f472b6"].forEach(c=>spawnParticles(cx,cy,c,14,"spark"));
                spawnParticles(cx,cy,"#ffffff",20,"dot");
                setTimeout(()=>setNotif(`🎁 ACCESSORY UNLOCKED: ${pick}! 💜`),400);
              } else {
                // No more accessories to unlock — convert to coins
                sv2.coins=(sv2.coins||0)+150;sv2.totalCoins=(sv2.totalCoins||0)+150;
                sv2.bossFragments-=10;
                setTimeout(()=>setNotif("💰 Fragments → +150 coins! (all accessories owned)"),400);
              }
            }
          }
          sv2.bossLootHistory=[{type:loot.type,amount,date:getTodayKey()},...(sv2.bossLootHistory||[])].slice(0,20);
          debounceSave();
          const lootLabel=loot.type==="fragment"?`${loot.emoji} FRAGMENT x1 (${sv2.bossFragments||1}/10)`:`${loot.emoji} ${loot.label} +${amount}`;
          setTimeout(()=>spawnPopup(hit.x,hit.y-70,lootLabel,loot.color,18),200);
          setTimeout(()=>{sfx("unlock");vibrate([15,10,30]);},350);
        }
        // BONUS ROUND — free spins equivalent (non-boss levels only)
        {const cfgB=levelCfgRef.current;
        if(cfgB&&!cfgB.isBoss&&!gs.bonusRoundActive){
          gs.bonusRoundActive=true;setBonusRound(true);
          spawnPopup(hit.x,hit.y-65,"🌟 BONUS ROUND!","#ffd700",20);
          sfx("lucky");vibrate([25,15,25,15,55]);
          showMascotSpeech("bonus");
          setTimeout(()=>{if(gsRef.current)gsRef.current.bonusRoundActive=false;setBonusRound(false);},9000);
        }}
        // Check modifier goal
        const cfg=levelCfgRef.current;
        if(cfg?.modifier?.type==="boss_kill"&&gs.sessionStats.bossKills>=1&&gs.score>=cfg.scoreGoal){endLevel(true);return;}
        if(cfg?.modifier?.type==="final_boss"){endLevel(true);return;}
      }
      return;
    }
    // NORMAL — squish then remove
    hit.dying=performance.now();
    gs.streak++;
    gs.lastTapTime=Date.now();
    // Log hit for adaptive difficulty
    if(gs._hitLog){gs._hitLog.push({t:Date.now(),hit:true});if(gs._hitLog.length>80)gs._hitLog.shift();}
    setStreakDecaying(false);
    const combo=Math.min(10,1+Math.floor(gs.streak/5));
    const isDouble=activePwrRef.current.some(p=>p.type==="DOUBLE"&&p.endsAt>Date.now());
    const feverMult=gs.feverActive?2:1;
    const timeLeft=1-(Date.now()-hit.spawnedAt)/hit.lifetime;
    const ceLevel=(saveRef.current.skills||{}).critical_eye||0;
    const perfectZone=0.38*(ceLevel===3?1.35:ceLevel===2?1.20:ceLevel===1?1.10:1.0);
    const isPerfect=hitDist<hit.radius*perfectZone&&timeLeft>0.36&&timeLeft<0.67;
    // Prestige score multiplier (+5% per prestige level, max 5 prestiges = +25%)
    const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
    const shardMult=hit._isShard?0.5:1; // splitter shards award half points
    const pts=Math.round(hit.rarity.mult*combo*feverMult*(isDouble?2:1)*(isPerfect?1.5:1)*prestigeMult*shardMult);
    gs.score+=pts;
    // Track last rarity for Mimic targets
    gs.lastRarityMult=hit.rarity.mult;
    gs.lastRarityColor=hit.color;
    gs.lastRarityName=hit.rarity.name;
    // Mascot XP (level 5 = +5% coin bonus)
    const mascotIdNow=saveRef.current.mascotId||"dragon";
    const mXP=saveRef.current.mascotXP||(saveRef.current.mascotXP={});
    const mLvlBefore=Math.min(20,Math.floor((mXP[mascotIdNow]||0)/500));
    mXP[mascotIdNow]=(mXP[mascotIdNow]||0)+Math.max(1,Math.floor(pts*0.01));
    const mLvlNow=Math.min(20,Math.floor((mXP[mascotIdNow]||0)/500));
    // Evolution at LV5/10/15/20 — show popup with new perk
    if(mLvlNow>mLvlBefore&&[5,10,15,20].includes(mLvlNow)){
      const EVO_PERKS={5:"💰 +5% coins",10:"✨ Aura unlocked",15:"⚡ Fast dance",20:"👑 MAX rainbow aura"};
      const m=MASCOTS.find(mm=>mm.id===mascotIdNow);
      sfx("unlock");vibrate([40,20,40,20,80]);
      setNotif(`🌟 ${m?.name||"Mascot"} → LV${mLvlNow}! ${EVO_PERKS[mLvlNow]}`);
      setTimeout(()=>setNotif(null),3000);
      if(mLvlNow>=10)unlock("mascot_lv10");
      // Auto-equip star at LV5, crown at LV20
      const owned={...(saveRef.current.ownedAccessories||{})};
      const equipped={...(saveRef.current.mascotAccessories||{})};
      if(mLvlNow===5){owned[`${mascotIdNow}:star`]=true;equipped[mascotIdNow]=equipped[mascotIdNow]||"star";}
      if(mLvlNow===20){owned[`${mascotIdNow}:crown`]=true;equipped[mascotIdNow]="crown";}
      saveRef.current.ownedAccessories=owned;
      saveRef.current.mascotAccessories=equipped;
    }
    const _skl=saveRef.current.skills||{};
    const coinSkill=_skl.coin_magnet||0;
    const coinSkillMult=coinSkill===3?1.2:coinSkill===2?1.1:coinSkill===1?1.05:1;
    const coinMult=(mLvlNow>=5?1.05:1)*coinSkillMult;
    saveRef.current.coins=(saveRef.current.coins||0)+Math.max(1,Math.floor(pts*0.09*coinMult));
    saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+Math.max(1,Math.floor(pts*0.09*coinMult));
    gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
    if(hit.rarity.name!=="common")gs.sessionStats.rareHits++;
    if(gs.streak>gs.sessionStats.bestCombo)gs.sessionStats.bestCombo=gs.streak;
    if(isPerfect){gs.sessionStats.perfectTaps=(gs.sessionStats.perfectTaps||0)+1;}

    // Activate streak shield at streak 10
    if(gs.streak===10&&!streakShRef.current){streakShRef.current=true;setStreakShieldActive(true);sfx("lucky");}
    // Mascot mood
    if(gs.streak>=20)setMascotMood("fire");
    else if(gs.streak>=10)setMascotMood("excited");
    else if(gs.streak>=5)setMascotMood("happy");
    else setMascotMood("idle");
    // Mascot bounce on every hit
    mascotBouncePlay();
    // Streak milestone burst celebrations + speech
    {const MILESTONES=[{n:5,label:"🔥 ON FIRE!",color:"#fbbf24"},{n:10,label:"⚡ UNSTOPPABLE!",color:"#f97316"},{n:20,label:"💥 LEGENDARY!",color:"#ef4444"},{n:30,label:"🌈 GODLIKE!!!",color:"#ff00ff"},{n:50,label:"👑 TRANSCENDENT!",color:"#ffd700"}];
    const ms=MILESTONES.find(m=>m.n===gs.streak);
    if(ms){setStreakBurst(ms);setTimeout(()=>setStreakBurst(null),1200);showMascotSpeech("streak");}}

    // Musical pentatonic scale note (most addictive mechanic!) — rising melody as streak grows
    sfx("comboNote", gs.streak);

    // Check personal best mid-game
    if(gs.score>saveRef.current.highScore&&gs.score>200&&!newRecord){
      setNewRecord(true);setTimeout(()=>setNewRecord(false),2000);
    }

    // SFX + particles
    if(hit.rarity.name==="legendary"){
      sfx("legendary");vibrate([30,15,30,15,60,15,90]);spawnParticles(hit.x,hit.y,hit.color,55,"spark");
      spawnParticles(hit.x,hit.y,"#ffffff",20,"dot");
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),650);
      setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),900);
      unlock("legendary");
    } else if(hit.rarity.name==="epic"){
      sfx("epic");vibrate([22,30,22]);spawnParticles(hit.x,hit.y,hit.color,35,"spark");
      spawnParticles(hit.x,hit.y,hit.color+"88",12,"dot");
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),420);unlock("first_epic");
    } else if(hit.rarity.name==="rare"){
      sfx("rare");vibrate([20,20]);spawnParticles(hit.x,hit.y,hit.color,22,"dot");unlock("first_rare");
    } else if(hit.rarity.name==="uncommon"){
      sfx("uncommon");vibrate(14);spawnParticles(hit.x,hit.y,hit.color,12,"dot");
    } else {
      vibrate(8);spawnParticles(hit.x,hit.y,hit.color,8,"dot");
    }
    // ── CHAIN REACTIONS — Rare+ targets can chain-detonate nearby normal targets ──
    const chainChance=hit.rarity.name==="legendary"?1.0:hit.rarity.name==="epic"?0.55:hit.rarity.name==="rare"?0.22:0;
    if(chainChance>0){
      const chainRange=hit.radius*4.2+90;
      const candidates=targetsRef.current.filter(t=>
        t!==hit&&!t.dying&&!t.anticipateMs||(t.anticipateMs&&(performance.now()-t.born)>=t.anticipateMs)
      ).filter(t=>t.type==="normal"&&t.id!==hit.id&&!t.dying);
      let chained=0;
      candidates.forEach(t=>{
        if(chained>=4)return;
        const dist=Math.hypot(t.x-hit.x,t.y-hit.y);
        if(dist>chainRange)return;
        if(Math.random()>chainChance)return;
        chained++;
        // Lightning arc from hit to chained target
        particlesRef.current.push({type:"arc",x:hit.x,y:hit.y,x2:t.x,y2:t.y,
          color:hit.color,size:3,born:performance.now(),duration:280,alpha:1});
        // Detonate
        t.dying=performance.now();
        const chainPts=Math.max(1,Math.floor((t.rarity?.mult||1)*combo*feverMult*0.5*prestigeMult));
        gs.score+=chainPts;
        spawnParticles(t.x,t.y,t.color,14,"dot");
        spawnPopup(t.x,t.y-18,`+${chainPts} CHAIN!`,hit.color,12);
      });
      if(chained>0){
        sfx("chainBonus");vibrate([8,4,8]);
        // Chain count announcement popup
        const chainLabel=chained>=4?"⚡⚡⚡ CHAIN x"+chained+"!":chained>=2?"⚡⚡ CHAIN x"+chained+"!":"⚡ CHAIN!";
        setChainFlash({label:chainLabel,at:Date.now()});
      }
      if(chained>=4)unlock("chain_4");
    }
    if(isPerfect){
      sfx("perfect");vibrate([8,8,8]);spawnPopup(hit.x,hit.y-22,"✨ PERFECT!","#fbbf24",18);
      setPerfectFlash(true);setTimeout(()=>setPerfectFlash(false),350);unlock("perfect_tap");
      // Golden star burst trail for perfect taps
      const trailColors=["#ffd700","#fbbf24","#fffbe6","#f59e0b","#ffffff"];
      const _pnow=performance.now();
      for(let i=0;i<20;i++){
        const ang=Math.random()*Math.PI*2,spd=1.5+Math.random()*3.5;
        particlesRef.current.push({
          type:"trail",x:hit.x,y:hit.y,
          vx:Math.cos(ang)*spd,vy:Math.sin(ang)*spd,
          color:trailColors[i%trailColors.length],
          born:_pnow,duration:380+Math.random()*360,
          size:2+Math.random()*4,alpha:1,
        });
      }
      // Ring shockwave in gold
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,r:1,color:"#ffd700",born:_pnow,duration:500,alpha:0.85});
    } else if(hit.rarity.label){
      spawnPopup(hit.x,hit.y,hit.rarity.label,hit.color,14);
    }
    // Combo label
    const cl=COMBO_LABELS.find(([n])=>gs.streak>=n);
    if(cl){setComboLabel(cl[1]);clearTimeout(window.__clt);window.__clt=setTimeout(()=>setComboLabel(""),1300);}
    // Achievements
    unlock("first_tap");
    if(gs.streak>=5)unlock("streak_5");
    if(gs.streak>=10)unlock("streak_10");if(gs.streak>=25)unlock("streak_25");if(gs.streak>=50)unlock("streak_50");
    if(gs.streak>=15)unlock("combo_15");
    if(gs.score>=2000)unlock("score_2000");
    // Fever
    if(gs.streak>=FEVER_STREAK&&!gs.feverActive){
      const frLvl=(saveRef.current.skills||{}).fever_rush||0;
      const feverMult2=frLvl===3?1.6:frLvl===2?1.4:frLvl===1?1.2:1.0;
      gs.feverActive=true;gs.feverTimeLeft=Math.round(FEVER_DUR*feverMult2);setFeverBorder(true);sfx("feverStart");vibrate([35,20,35,20,65]);
      audioRef.current?.setBgMusicFever?.(true);
      spawnPopup(hit.x,hit.y-45,"🌡 FEVER!","#fbbf24",21);unlock("fever_mode");setMascotMood("fever");showMascotSpeech("fever");
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
  const startGame=useCallback((levelId,shopCart=[],infCfg=null)=>{
    const baseCfg=infCfg||getLevelConfig(levelId);
    // Apply speed mode multiplier
    const speedMult=saveRef.current.speedMode||1.0;
    const cfg={...baseCfg,
      spawnInterval:Math.round(baseCfg.spawnInterval/speedMult),
      targetLifetime:Math.round(baseCfg.targetLifetime/speedMult),
    };
    levelCfgRef.current=cfg;
    // Sync module-level flags
    _hapticOn=saveRef.current.hapticEnabled!==false;
    _colorblindOn=!!saveRef.current.colorblindMode;
    initMissions();
    initBgParts(cfg.world);
    targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];ripplesRef.current=[];
    spawnTimer.current=0;pausedRef.current=false;setPaused(false);
    streakShRef.current=false;setStreakShieldActive(false);setNewRecord(false);setCloseBanner(false);
    luckyRef.current=null;if(luckyTimer.current)clearTimeout(luckyTimer.current);
    // Schedule first lucky event 45-70 seconds in
    luckyTimer.current=setTimeout(()=>triggerLucky(),45000+Math.random()*25000);

    const extraLife=shopCart.includes("extra_life");
    const headStart=shopCart.includes("head_start");
    const shieldStart=shopCart.includes("shield_start");
    const powerPack=shopCart.includes("power_pack");
    const feverPotion=shopCart.includes("fever_potion");
    const xpBomb=shopCart.includes("xp_bomb");
    const streakSaver=shopCart.includes("streak_saver");

    const isRescue=rescuedRef.current;rescuedRef.current=false;
    tensionRef.current=0;setTensionLevel(0);setBonusRound(false);setMysteryReveal(null);
    setStreakDecaying(false);if(decayTimerRef.current){clearInterval(decayTimerRef.current);decayTimerRef.current=null;}
    // Mascot level bonuses
    const mascotId=saveRef.current.mascotId||"dragon";
    const mascotXP=saveRef.current.mascotXP||{};
    const mLevel=Math.min(20,Math.floor((mascotXP[mascotId]||0)/500));
    const hasStreakShield=mLevel>=10;
    const headStartBonus=(mLevel>=15?100:0)+(headStart?300:0);
    const frLvl2=(saveRef.current.skills||{}).fever_rush||0;
    const feverMult2=frLvl2===3?1.6:frLvl2===2?1.4:frLvl2===1?1.2:1.0;
    gsRef.current={
      score:isRescue?400:headStartBonus>0?headStartBonus:0,
      lives:isRescue?MAX_LIVES:Math.min(MAX_LIVES,cfg.lives+(extraLife?1:0)),
      streak:feverPotion?FEVER_STREAK:0,
      feverActive:!!feverPotion, feverTimeLeft:feverPotion?Math.round(FEVER_DUR*feverMult2*1.5):0,
      startTime:Date.now(), lastTapTime:Date.now(),
      sessionStats:{tapsTotal:0,rareHits:0,bestCombo:0,score:0,feverCount:feverPotion?1:0,powerupCollected:0,bossKills:0,perfectTaps:0,missedTargets:0},
      _hitLog:[], // [{t:timestamp, hit:bool}] for adaptive difficulty
      _adaptNextEval:Date.now()+4000, // first eval after 4 seconds
      _adaptMult:1.0, // current adaptive multiplier (0.7-1.3)
      _xpBombActive:!!xpBomb, // doubles XP at level end
      _streakSaverActive:!!streakSaver, // saves streak once on miss
    };
    if(hasStreakShield&&!isRescue){streakShRef.current=true;setStreakShieldActive(true);}
    if(shieldStart)activePwrRef.current=[{type:"SHIELD",endsAt:Date.now()+25000}];
    if(powerPack){const pt=["SLOW","DOUBLE","SHIELD","FREEZE"];const ty=pt[Math.floor(Math.random()*pt.length)];if(!activePwrRef.current.find(p=>p.type===ty))activePwrRef.current.push({type:ty,endsAt:Date.now()+12000});}
    if(feverPotion){setFeverBorder(true);sfx("feverStart");}
    setActivePwrDisp([...activePwrRef.current]);
    setHud({score:headStart?300:0,lives:gsRef.current.lives,streak:0,fever:false,coins:saveRef.current.coins,timeLeft:null,modGoal:cfg.modifier?.desc||null});
    setLevelCompleteData(null);setGameOverData(null);setEpicFlash(false);setFeverBorder(false);setComboLabel("");
    setCartItems([]);setScreen("playing");setMascotMood("idle");setMascotSpeech(null);setMascotBounce(false);
    if(soundOn&&audioRef.current?.startBgMusic)audioRef.current.startBgMusic(cfg.world);
    // 11B — Boss warning on levels ending in 9 (boss next)
    if(!cfg.isInfinity&&!cfg.isZen&&typeof levelId==="number"&&levelId%10===9){
      const nextWld=WORLDS[Math.floor(levelId/10)%10];
      setTimeout(()=>setNotif(`👑 Next level: ${nextWld?.emoji||""} BOSS BATTLE!`),2200);
    }
    runCountdown(()=>{lastTickRef.current=performance.now();rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));});
  },[initMissions,initBgParts,runCountdown,soundOn]); // eslint-disable-line

  // Lucky golden event — all targets turn legendary for 7 seconds
  const triggerLucky=useCallback(()=>{
    if(!gsRef.current||pausedRef.current)return;
    luckyRef.current="active";setLuckyMode(true);
    sfx("lucky");
    spawnPopup(window.innerWidth/2,window.innerHeight/2-60,"⭐ LUCKY STARS! ⭐","#ffd700",24);
    setTimeout(()=>{luckyRef.current=null;setLuckyMode(false);
      // Schedule next lucky event 50-80s later
      luckyTimer.current=setTimeout(()=>triggerLucky(),50000+Math.random()*30000);
    },7000);
  },[sfx,spawnPopup]);// eslint-disable-line

  // Pause
  const togglePause=useCallback(()=>{
    if(!gsRef.current)return;
    const next=!pausedRef.current;pausedRef.current=next;setPaused(next);
    if(!next){lastTickRef.current=performance.now();rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));}
  },[]);// eslint-disable-line

  useEffect(()=>()=>{if(rafRef.current)cancelAnimationFrame(rafRef.current);},[]);

  // Menu canvas loop
  useEffect(()=>{
    if(screen!=="menu"&&screen!=="levelmap"&&screen!=="shop"&&screen!=="levelcomplete"&&screen!=="gameover"&&screen!=="spinwheel"&&screen!=="missions"&&screen!=="achievements"&&screen!=="leaderboard"&&screen!=="settings"&&screen!=="infinity"&&screen!=="gauntlet"&&screen!=="mascotcollection"&&screen!=="weekly"&&screen!=="tournament"&&screen!=="skilltree"&&screen!=="zen")return;
    let raf;
    const loop=(ts)=>{
      const canvas=canvasRef.current;if(!canvas)return;
      const ctx=canvas.getContext("2d");
      const th=THEMES.find(t=>t.id===(saveRef.current.themeId||"neon"))||THEMES[0];
      drawBg(ctx,canvas.width,canvas.height,th.accent,th.grid,ts,false);
      drawBgParticles(ctx,bgPartsRef.current,th.accent,false);
      drawVignette(ctx,canvas.width,canvas.height,th.accent);
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

    drawBg(ctx,w,h,accentColor,gridColor,ts,fever,cfg?cfg.world:0);
    drawBgParticles(ctx,bgPartsRef.current,accentColor,fever,cfg?cfg.world:0);
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
    // Restore anchor-frozen target velocities when freeze expires
    const anchorFreezeActive=gsRef.current&&gsRef.current._anchorFreezeUntil&&gsRef.current._anchorFreezeUntil>now;
    if(!anchorFreezeActive){
      targetsRef.current.forEach(t=>{
        if(t._frozenUntil&&t._frozenUntil<=now){
          t.vx=t._anchorFrozenVx||0;t.vy=t._anchorFrozenVy||0;
          delete t._anchorFrozenVx;delete t._anchorFrozenVy;delete t._frozenUntil;
        }
      });
    }
    targetsRef.current=targetsRef.current.filter(t=>{
      // Move (skip if anchor-frozen)
      if(t._frozenUntil&&t._frozenUntil>now){drawTarget(ctx,t,ts);return true;}
      if(t.moving&&!activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>now)){
        if(t.type==="boss"&&t.bossPattern!=null){
          // Boss-specific movement patterns, scaled by phase speed
          const phaseSpeed=t.bossPhase===3?1.8:t.bossPhase===2?1.35:1.0;
          const margin=t.radius+5;
          if(t.bossPattern===0){
            // Orbit around spawn anchor
            const orbR=Math.min(80,Math.min(w,h)*0.18);
            const omega=0.0011*phaseSpeed;
            t.bossAngle=(t.bossAngle||0)+omega*dt;
            t.x=(t.cx||t.x)+Math.cos(t.bossAngle)*orbR;
            t.y=(t.cy||t.y)+Math.sin(t.bossAngle)*orbR*0.7;
          } else if(t.bossPattern===1){
            // Bounce (default)
            t.x+=t.vx*dt*0.056*phaseSpeed;t.y+=t.vy*dt*0.056*phaseSpeed;
            if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
            if(t.y<t.radius+95||t.y>h-margin){t.vy*=-1;t.y=Math.max(t.radius+95,Math.min(h-margin,t.y));}
          } else if(t.bossPattern===2){
            // Vertical wave drift
            t.x+=t.vx*dt*0.056*phaseSpeed;
            t.y=(t.cy||t.y)+Math.sin((performance.now()-t.born)*0.0025*phaseSpeed)*45;
            if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
          } else {
            // Zigzag — sudden direction change every ~700ms
            t.bossZigT=(t.bossZigT||0)+dt;
            if(t.bossZigT>700/phaseSpeed){
              const a=Math.random()*Math.PI*2;const sp=1.2*phaseSpeed;
              t.vx=Math.cos(a)*sp;t.vy=Math.sin(a)*sp;t.bossZigT=0;
            }
            t.x+=t.vx*dt*0.056;t.y+=t.vy*dt*0.056;
            if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
            if(t.y<t.radius+95||t.y>h-margin){t.vy*=-1;t.y=Math.max(t.radius+95,Math.min(h-margin,t.y));}
          }
        } else {
          t.x+=t.vx*dt*0.056;t.y+=t.vy*dt*0.056;
          const margin=t.radius+5;
          if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
          if(t.y<t.radius+95||t.y>h-margin){t.vy*=-1;t.y=Math.max(t.radius+95,Math.min(h-margin,t.y));}
        }
        if(t.trail){t.trail.push({x:t.x,y:t.y});if(t.trail.length>12)t.trail.shift();}
      }
      // Squish (dying) animation — plays for 120ms then removes
      if(t.dying){
        const age=pnow-t.dying;
        if(age>=120)return false;
        const p=age/120;
        const sx=1+Math.sin(p*Math.PI)*0.55;
        const sy=1-Math.sin(p*Math.PI)*0.42;
        ctx.save();ctx.translate(t.x,t.y);ctx.scale(sx,sy);ctx.translate(-t.x,-t.y);
        ctx.globalAlpha=1-p*0.8;
        drawTarget(ctx,t,ts);
        ctx.restore();ctx.globalAlpha=1;
        return true;
      }
      // Expiry
      if((now-t.spawnedAt)>=t.lifetime){
        if(t.type==="powerup"||t.type==="bomb"||t.type==="boss"||t.type==="treasure")return false;
        if(t.type==="normal"&&!t._isShard)gs.sessionStats.missedTargets=(gs.sessionStats.missedTargets||0)+1;
        const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
        if(hasShield){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
        else if(streakShRef.current){
          // Streak Shield — absorbs one miss, preserves streak!
          streakShRef.current=false;setStreakShieldActive(false);sfx("shieldBreak");vibrate([8,12,8]);
        } else if(gs._streakSaverActive&&(gs.streak||0)>0){
          // Streak Saver shop item — save streak on first miss
          gs._streakSaverActive=false;gs.lives--;lostLife=true;
          sfx("shieldBreak");vibrate([8,5,8]);
          spawnParticles(t.x,t.y,"#fbbf24",6,"spark");
          spawnPopup(t.x,t.y-18,"💛 STREAK SAVED!","#fbbf24",14);
        } else{
          gs.lives--;sfx("miss");vibrate(42);lostLife=true;
          // Skill: combo_guard — absorb N misses before clearing streak
          const cgLvl=(saveRef.current.skills||{}).combo_guard||0;
          gs._comboGuardCount=gs._comboGuardCount||0;
          if(cgLvl>0&&gs.streak>0&&gs._comboGuardCount<cgLvl){
            gs._comboGuardCount++;
            spawnParticles(t.x,t.y,"#fbbf24",6,"spark");
          } else {
            gs._comboGuardCount=0;
            gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);setMascotMood("sad");
            showMascotSpeech("miss");
            setTimeout(()=>setMascotMood("idle"),1200);
          }
          // Screen shake on miss
          setScreenShake(true);setTimeout(()=>setScreenShake(false),280);
          // Red flash at target position
          spawnParticles(t.x,t.y,"#ef4444",8,"spark");
          // Log miss for adaptive difficulty
          if(gs._hitLog){gs._hitLog.push({t:Date.now(),hit:false});if(gs._hitLog.length>80)gs._hitLog.shift();}
          // no_miss modifier: instant fail
          if(cfg?.modifier?.type==="no_miss"){endLevel(false);return false;}
        }
        return false;
      }
      drawTarget(ctx,t,ts);return true;
    });

    // World foreground silhouettes + depth vignette (on top of targets)
    drawWorldForeground(ctx,w,h,cfg?cfg.world:0,ts);
    drawVignette(ctx,w,h,accentColor);

    if(lostLife){if(gs.lives<=0){endLevel(false);return;}}

    // Expire power-ups
    const pl=activePwrRef.current.length;
    activePwrRef.current=activePwrRef.current.filter(p=>p.endsAt>now);
    if(activePwrRef.current.length!==pl)setActivePwrDisp([...activePwrRef.current]);

    // Fever
    if(gs.feverActive){gs.feverTimeLeft-=dt;if(gs.feverTimeLeft<=0){gs.feverActive=false;setFeverBorder(false);sfx("feverEnd");audioRef.current?.setBgMusicFever?.(false);setMascotMood("idle");}}

    // Adaptive difficulty — every 4s, adjust spawnInterval and targetLifetime
    if(saveRef.current.adaptiveDifficulty&&gs._hitLog&&gs._adaptNextEval&&now>=gs._adaptNextEval){
      gs._adaptNextEval=now+4000;
      const windowMs=12000;
      const recent=gs._hitLog.filter(e=>now-e.t<windowMs);
      if(recent.length>=6){
        const hitRate=recent.filter(e=>e.hit).length/recent.length;
        // Target ~72% hit rate as "just right"
        let newMult=gs._adaptMult||1.0;
        if(hitRate>0.88)newMult=Math.min(1.35,newMult+0.07); // too easy → harder
        else if(hitRate>0.78)newMult=Math.min(1.35,newMult+0.03);
        else if(hitRate<0.45)newMult=Math.max(0.65,newMult-0.10); // too hard → easier
        else if(hitRate<0.60)newMult=Math.max(0.65,newMult-0.05);
        if(Math.abs(newMult-(gs._adaptMult||1.0))>0.01){
          gs._adaptMult=newMult;
          const base=getLevelConfig(cfg.id||1);
          const sm=saveRef.current.speedMode||1.0;
          levelCfgRef.current.spawnInterval=Math.max(200,Math.round(base.spawnInterval/sm/newMult));
          levelCfgRef.current.targetLifetime=Math.max(600,Math.round(base.targetLifetime/sm/newMult));
        }
      }
    }

    // Spawn — rage boss speeds up spawn
    const rageSpawn=cfg._rageSpawn&&targetsRef.current.some(t=>t.rage);
    spawnTimer.current+=dt;
    if(spawnTimer.current>=(rageSpawn?cfg.spawnInterval*0.5:cfg.spawnInterval)){spawnTimer.current=0;spawnTarget();}

    // World modifier: Dragon's Lair (W1) — small ground tremors every ~7-10s
    if(cfg.world===1){
      gs.lairTremorAt=gs.lairTremorAt||(Date.now()+8000+Math.random()*3000);
      if(Date.now()>=gs.lairTremorAt){
        setScreenShake(true);setTimeout(()=>setScreenShake(false),250);
        try{navigator.vibrate?.([20]);}catch{}
        gs.lairTremorAt=Date.now()+7000+Math.random()*4000;
      }
    }
    // World modifier: Haunted Castle (W7) — periodic 'ghost wave' makes targets fade
    if(cfg.world===7){
      gs.ghostWaveAt=gs.ghostWaveAt||(Date.now()+5000);
      gs.ghostWaveEnd=gs.ghostWaveEnd||0;
      if(Date.now()>=gs.ghostWaveAt&&Date.now()>gs.ghostWaveEnd){
        gs.ghostWaveEnd=Date.now()+1400;
        gs.ghostWaveAt=Date.now()+5500+Math.random()*2000;
        // Mark all current normal targets as wave-ghosted
        targetsRef.current.forEach(t=>{if(t.type==="normal")t.waveGhost=Date.now()+1400;});
      }
    }

    // Combo decay — reduce streak after 2.5s of inactivity (1.5s in Viking Fjords frost)
    const decayMs=cfg.world===5?1500:2500; // Viking Fjords: combo slips through frost faster
    if(gs.streak>0&&gs.lastTapTime&&(Date.now()-gs.lastTapTime)>decayMs){
      gs.streak=Math.max(0,gs.streak-1);
      gs.lastTapTime=Date.now()-decayMs;
      setStreakDecaying(gs.streak>0);
    }

    // HUD update 20fps
    if(ts-hudRef.current>50){
      hudRef.current=ts;
      const decayMs2=cfg?.world===5?1500:2500;
      const decayPct=gs.streak>0&&gs.lastTapTime?Math.max(0,1-(Date.now()-gs.lastTapTime)/decayMs2):1;
      const bossT=targetsRef.current.find(t=>t.type==="boss"&&!t.dying);
      // Zen mode: countdown timer
      let zenTimeLeft=null;
      if(cfg?.isZen){
        zenTimeLeft=Math.max(0,Math.ceil((cfg.zenDuration-(Date.now()-gs.startTime))/1000));
        if(zenTimeLeft<=0){endLevel(true);return;}
      }
      setHud({score:gs.score,lives:gs.lives,streak:gs.streak,fever:gs.feverActive,coins:saveRef.current.coins,
        timeLeft:zenTimeLeft,modGoal:cfg?.isZen?null:cfg?.modifier?.desc||null,decayPct,
        boss:bossT?{hp:bossT.hitsLeft,max:bossT.maxHits,phase:bossT.bossPhase||1,rage:!!bossT.rage}:null});
    }

    rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));
  },[sfx,spawnTarget,endLevel]);// eslint-disable-line

  const sv=saveRef.current,lvl=getLvl(sv.xp);
  const unlockedMascots=sv.unlockedMascots||(sv.unlockedMascots=["dragon","fox"]);
  const currentMascot=MASCOTS.find(m=>m.id===(sv.mascotId||"dragon")&&unlockedMascots.includes(m.id))||MASCOTS[0];

  // Show mascot speech bubble for 2.5s
  const showSpeech=useCallback((text)=>{
    clearTimeout(speechTimerRef.current);
    setMascotSpeech(text);
    speechTimerRef.current=setTimeout(()=>setMascotSpeech(null),2500);
  },[]);

  // Show mood-specific speech from the current mascot's personality pool
  const showMascotSpeech=useCallback((moodKey)=>{
    const pool=currentMascot.speeches?.[moodKey];
    if(!pool?.length)return;
    const text=pool[Math.floor(Math.random()*pool.length)];
    clearTimeout(speechTimerRef.current);
    setMascotSpeech(text);
    speechTimerRef.current=setTimeout(()=>setMascotSpeech(null),2500);
  },[currentMascot]);

  // Check + apply mascot unlock conditions from current save state
  const checkMascotUnlocks=useCallback(()=>{
    const sv2=saveRef.current;
    const unlocked=sv2.unlockedMascots||(sv2.unlockedMascots=["dragon","fox"]);
    const newlyUnlocked=[];
    for(const m of MASCOTS){
      if(unlocked.includes(m.id)||!m.unlockCond)continue;
      const{type,value}=m.unlockCond;
      let met=false;
      if(type==="level")met=(sv2.unlockedLevel||1)>value; // >value because unlockedLevel updates to next
      else if(type==="streak")met=(sv2.bestStreak||0)>=value;
      else if(type==="threestars"){
        const cnt=Object.values(sv2.levelStars||{}).filter(s=>s>=3).length;
        met=cnt>=value;
      }
      else if(type==="coins")met=(sv2.totalCoins||0)>=value;
      if(met)newlyUnlocked.push(m);
    }
    if(newlyUnlocked.length>0){
      sv2.unlockedMascots=[...unlocked,...newlyUnlocked.map(m=>m.id)];
      return newlyUnlocked;
    }
    return[];
  },[]);

  // Brief mascot bounce on hit
  const mascotBouncePlay=useCallback(()=>{
    clearTimeout(bounceTimerRef.current);
    setMascotBounce(true);
    bounceTimerRef.current=setTimeout(()=>setMascotBounce(false),320);
  },[]);

  // Helper: render the mascot emoji with dance/idle animation
  const MascotEmoji=({mood="idle",dancing=false,size=36,style:sx={}})=>{
    const m=currentMascot;
    const emoji=m.e[mood]||m.e.idle;
    const bounce=mascotBounce&&mood!=="sad"&&mood!=="scared"&&!dancing;
    // Mascot level — drives evolution perks
    const mLvl=Math.min(20,Math.floor(((saveRef.current.mascotXP||{})[m.id]||0)/500));
    // LV15+: faster dance, LV20: even faster
    const danceSpd=mLvl>=20?0.4:mLvl>=15?0.46:0.55;
    const anim=dancing?`${m.dance} ${danceSpd}s ease-in-out infinite`
      :bounce?"mascotBounce 0.32s cubic-bezier(0.34,1.6,0.64,1)"
      :(mood==="excited"||mood==="fire"||mood==="fever")?`${m.dance} ${mLvl>=15?0.9:1.1}s ease-in-out infinite`
      :mood==="sad"?"mascotSad 0.6s ease-in-out 1"
      :mood==="scared"?"mascotShake 0.4s ease-in-out 1"
      :"mascotIdle 2.2s ease-in-out infinite";
    // LV10+: extra glow aura. LV20: rainbow MAX aura
    const auraColor=mLvl>=20?"#ffd700":m.color;
    const auraStrength=mLvl>=20?1.5:mLvl>=10?1.1:1;
    const glow=mood==="fire"||mood==="fever"?`drop-shadow(0 0 ${Math.round(size/2.5*auraStrength)}px ${m.color}) drop-shadow(0 0 ${Math.round(size/1.5)}px #ff6030aa)`
      :mood==="victory"||dancing?`drop-shadow(0 0 ${Math.round(size/2*auraStrength)}px ${auraColor}) drop-shadow(0 0 ${Math.round(size*auraStrength)}px ${auraColor}55)`
      :`drop-shadow(0 0 ${Math.round(size/3*auraStrength)}px ${auraColor})`;
    // Equipped accessory overlay
    const accId=(saveRef.current.mascotAccessories||{})[m.id];
    const acc=accId?MASCOT_ACCESSORIES.find(a=>a.id===accId):null;
    return(
      <span style={{position:"relative",display:"inline-block",...sx}}>
        {/* LV20 MAX rainbow aura ring */}
        {mLvl>=20&&(
          <span style={{
            position:"absolute",inset:`-${size*0.12}px`,borderRadius:"50%",
            background:"conic-gradient(from 0deg,#ff6030,#fbbf24,#34d399,#60a5fa,#f472b6,#a78bfa,#ff6030)",
            filter:`blur(${size/8}px)`,opacity:0.55,
            animation:"slotSpin 3.5s linear infinite",pointerEvents:"none"}}/>
        )}
        {/* LV10+ subtle aura ring */}
        {mLvl>=10&&mLvl<20&&(
          <span style={{
            position:"absolute",inset:`-${size*0.08}px`,borderRadius:"50%",
            background:`radial-gradient(circle,${m.color}55 0%,transparent 70%)`,
            opacity:0.7,pointerEvents:"none",
            animation:"floatGlow 2.4s ease-in-out infinite"}}/>
        )}
        <span style={{fontSize:size,lineHeight:1,display:"inline-block",position:"relative",
          animation:anim,filter:glow}}>
          {emoji}
        </span>
        {acc&&(
          <span style={{
            position:"absolute",top:-size*0.15,left:"50%",transform:"translateX(-50%)",
            fontSize:size*0.5,lineHeight:1,pointerEvents:"none",
            filter:`drop-shadow(0 0 ${Math.round(size/6)}px #ffd70088)`,
            animation:anim}}>
            {acc.emoji}
          </span>
        )}
      </span>
    );
  };

  const streakColor=()=>{
    const s=hud.streak;
    if(s>=35)return"#ff00ff";if(s>=20)return"#ef4444";if(s>=10)return"#f97316";if(s>=5)return"#fbbf24";return"#ffffff";
  };

  // ── Score Tension Ramp — fires whenever score changes ──
  useEffect(()=>{
    if(screen!=="playing")return;
    const cfg=levelCfgRef.current;if(!cfg)return;
    const pct=hud.score/cfg.scoreGoal;
    const newT=pct>=0.99?4:pct>=0.95?3:pct>=0.90?2:pct>=0.75?1:0;
    if(newT!==tensionRef.current){
      tensionRef.current=newT;
      setTensionLevel(newT);
      if(newT===2){sfx("comboNote",9);showMascotSpeech("close");}
      if(newT===3){sfx("comboNote",11);try{navigator.vibrate?.([15,10,15]);}catch{}showMascotSpeech("close");}
      if(newT===4){sfx("comboNote",12);try{navigator.vibrate?.([15,10,15,10,20]);}catch{}showMascotSpeech("close");}
    }
  },[hud.score,screen]);// eslint-disable-line

  // ── Rescue countdown ──
  useEffect(()=>{
    if(rescueSecondsLeft<=0)return;
    const t=setTimeout(()=>setRescueSecondsLeft(s=>Math.max(0,s-1)),1000);
    return()=>clearTimeout(t);
  },[rescueSecondsLeft]);

  // ── Coin/XP payout roll-up ──
  useEffect(()=>{
    if(!levelCompleteData)return;
    const{coinsEarned,xpEarned}=levelCompleteData;
    setDisplayedCoins(0);setDisplayedXP(0);setPayoutDone(false);
    let frame=0;const FRAMES=45;
    const id=setInterval(()=>{
      frame++;
      const ease=1-Math.pow(1-frame/FRAMES,3);
      setDisplayedCoins(Math.floor(ease*coinsEarned));
      setDisplayedXP(Math.floor(ease*xpEarned));
      if(frame%5===0)sfx("comboNote",Math.min(11,Math.floor((frame/FRAMES)*12)));
      if(frame>=FRAMES){clearInterval(id);setPayoutDone(true);}
    },35);
    return()=>clearInterval(id);
  },[levelCompleteData]);// eslint-disable-line

  // ═════════════════════════════════════════════════════════════
  // SCREEN RENDERERS
  // ═════════════════════════════════════════════════════════════

  // ── World Story ──
  const renderWorldStory=()=>{
    if(!storyData)return null;
    const{worldId,type,onDone,bossIntro,panelIndex=0}=storyData;
    // Boss intro panel
    if(type==="boss"&&bossIntro){
      const wld=WORLDS[(worldId||1)-1];
      return(
        <div className="absolute inset-0 z-50 flex flex-col items-center justify-center px-6"
          style={{background:`linear-gradient(160deg,${wld.bg} 0%,rgba(0,0,0,0.92) 100%)`}}>
          <style>{`@keyframes storyFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}} @keyframes bossShake{0%,100%{transform:rotate(-2deg)}50%{transform:rotate(2deg)}}`}</style>
          <div className="w-full max-w-sm flex flex-col items-center gap-5 text-center">
            <div className="text-xs uppercase tracking-widest font-bold" style={{color:wld.color,opacity:0.7}}>⚠️ BOSS STAGE ⚠️</div>
            <div className="text-6xl" style={{animation:"bossShake 0.4s ease-in-out infinite",filter:`drop-shadow(0 0 18px ${wld.color})`}}>{bossIntro.emoji}</div>
            <div className="font-black text-2xl leading-tight" style={{
              color:wld.color,fontFamily:"'Rajdhani','Exo 2',sans-serif",
              textShadow:`0 0 24px ${wld.color}88`}}>{bossIntro.title}</div>
            <div className="rounded-3xl px-6 py-5 text-sm leading-relaxed"
              style={{background:`${wld.color}12`,border:`1px solid ${wld.color}55`,
                backdropFilter:"blur(10px)",color:"#f0f0e8",lineHeight:1.7,fontSize:"1rem"}}>
              {bossIntro.text}
            </div>
            <NeonButton onClick={()=>{
              const bs=saveRef.current.seenBossIntros||[];
              if(!bs.includes(worldId))saveRef.current.seenBossIntros=[...bs,worldId];
              debounceSave();onDone&&onDone();setStoryData(null);
            }} className="w-full py-4 text-lg font-black"
              style={{background:`linear-gradient(135deg,${wld.accent},${wld.color})`,
                boxShadow:`0 0 32px ${wld.color}77`}}>
              🥊 I'm Ready! Let's Go!
            </NeonButton>
          </div>
        </div>
      );
    }
    if(type==="main"){
      const panels=MAIN_STORY.intro.map((text,i)=>({emoji:["🌈","🌩️","🦸"][i]||"✨",text}));
      const idx=panelIndex||0;
      const panel=panels[idx];
      const isLast=idx===panels.length-1;
      return(
        <div className="absolute inset-0 z-50 flex flex-col items-center justify-center px-6"
          style={{background:"linear-gradient(160deg,#060010 0%,#001020 60%,#080800 100%)"}}>
          <style>{`@keyframes storyFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}`}</style>
          {/* Stars bg */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {[...Array(22)].map((_,i)=>(
              <div key={i} style={{position:"absolute",width:2,height:2,borderRadius:"50%",background:"#fff",
                left:`${(i*37+7)%100}%`,top:`${(i*23+5)%100}%`,opacity:0.2+Math.random()*0.4}}/>
            ))}
          </div>
          <div className="relative z-10 w-full max-w-sm flex flex-col items-center gap-6">
            <div className="text-5xl" style={{animation:"storyFloat 3s ease-in-out infinite"}}>{panel.emoji}</div>
            <div className="text-center font-black text-xl leading-tight" style={{
              color:"#ffd700",fontFamily:"'Rajdhani','Exo 2',sans-serif",
              textShadow:"0 0 20px #ffd70088"}}>
              {MAIN_STORY.title}
            </div>
            <div className="rounded-3xl px-6 py-5 text-center text-sm leading-relaxed"
              style={{background:"rgba(255,255,255,0.06)",border:"1px solid rgba(255,215,0,0.25)",
                backdropFilter:"blur(10px)",color:"#f0e8c0",lineHeight:1.7,fontSize:"1rem"}}>
              {panel.text}
            </div>
            {/* Dots */}
            <div className="flex gap-2">
              {panels.map((_,i)=>(
                <div key={i} style={{width:8,height:8,borderRadius:"50%",background:i===idx?"#ffd700":"#ffffff22",
                  boxShadow:i===idx?"0 0 8px #ffd700":"none"}}/>
              ))}
            </div>
            <NeonButton onClick={()=>{
              if(!isLast){setStoryData(d=>({...d,panelIndex:(d.panelIndex||0)+1}));}
              else{saveRef.current.seenMainStory=true;debounceSave();onDone&&onDone();setStoryData(null);}
            }} className="w-full py-4 text-lg font-black"
              style={{background:"linear-gradient(135deg,#b8860b,#ffd700)",boxShadow:"0 0 28px #ffd70066",color:"#000"}}>
              {isLast?"🚀 START THE QUEST!":"Next →"}
            </NeonButton>
            {idx===0&&<button onClick={()=>{saveRef.current.seenMainStory=true;debounceSave();onDone&&onDone();setStoryData(null);}}
              className="text-xs opacity-30 mt-1" style={{color:"#fff",background:"none",border:"none",cursor:"pointer"}}>
              Skip
            </button>}
          </div>
        </div>
      );
    }
    // World story
    const ws=WORLD_STORIES.find(s=>s.worldId===worldId);
    if(!ws)return null;
    const idx=panelIndex||0;
    const panel=ws.panels[idx];
    const isLast=idx===ws.panels.length-1;
    const wld=WORLDS[worldId-1];
    return(
      <div className="absolute inset-0 z-50 flex flex-col items-center justify-center px-6"
        style={{background:`linear-gradient(160deg,${wld.bg} 0%,${wld.color}18 100%)`}}>
        <div className="relative z-10 w-full max-w-sm flex flex-col items-center gap-5">
          {/* World title */}
          <div className="flex items-center gap-2">
            <span style={{fontSize:32}}>{wld.emoji}</span>
            <div className="font-black text-lg" style={{color:wld.color,fontFamily:"'Rajdhani','Exo 2',sans-serif",
              textShadow:`0 0 16px ${wld.color}88`}}>{ws.title}</div>
          </div>
          {/* Panel emoji big */}
          <div className="text-6xl" style={{animation:"storyFloat 3s ease-in-out infinite",filter:`drop-shadow(0 0 12px ${wld.color}88)`}}>{panel.emoji}</div>
          {/* Story text */}
          <div className="rounded-3xl px-6 py-5 text-center text-sm leading-relaxed w-full"
            style={{background:`${wld.color}10`,border:`1px solid ${wld.color}44`,
              backdropFilter:"blur(10px)",color:"#f0f0e8",lineHeight:1.7,fontSize:"0.97rem"}}>
            {panel.text}
          </div>
          {/* Dots */}
          <div className="flex gap-2">
            {ws.panels.map((_,i)=>(
              <div key={i} style={{width:8,height:8,borderRadius:"50%",background:i===idx?wld.color:"#ffffff22",
                boxShadow:i===idx?`0 0 8px ${wld.color}`:"none"}}/>
            ))}
          </div>
          <NeonButton onClick={()=>{
            if(!isLast){setStoryData(d=>({...d,panelIndex:(d.panelIndex||0)+1}));}
            else{
              const seen=saveRef.current.seenWorldStories||[];
              if(!seen.includes(worldId))saveRef.current.seenWorldStories=[...seen,worldId];
              debounceSave();onDone&&onDone();setStoryData(null);
            }
          }} className="w-full py-4 text-lg font-black"
            style={{background:`linear-gradient(135deg,${wld.accent},${wld.color})`,
              boxShadow:`0 0 28px ${wld.color}66`}}>
            {isLast?"▶ Let's Go! 🎮":"Next →"}
          </NeonButton>
          {idx===0&&<button onClick={()=>{
            const seen=saveRef.current.seenWorldStories||[];
            if(!seen.includes(worldId))saveRef.current.seenWorldStories=[...seen,worldId];
            debounceSave();onDone&&onDone();setStoryData(null);
          }} className="text-xs opacity-30 mt-1" style={{color:"#fff",background:"none",border:"none",cursor:"pointer"}}>
            Skip
          </button>}
        </div>
      </div>
    );
  };

  // ── Tutorial ──
  const TUT_STEPS=[
    {emoji:"👆",title:"Tap the targets!",body:"Glowing circles appear on screen. Tap them before they disappear to score points!",cta:"Got it! →",demo:true},
    {emoji:"🔥",title:"Build your streak!",body:"Tap targets one after another without missing. The longer your streak, the bigger your bonus!",cta:"Cool! →"},
    {emoji:"💣",title:"Avoid bombs!",body:"Red bombs will appear — do NOT tap them! They cost you a life. Tap AROUND them!",cta:"Understood! →"},
    {emoji:"🌟",title:"You're ready!",body:"Collect stars, unlock new worlds, and chase the high score. Have fun on your adventure!",cta:"LET'S GO! 🚀"},
  ];
  const renderTutorial=()=>{
    const step=TUT_STEPS[tutStep]||TUT_STEPS[0];
    const isLast=tutStep===TUT_STEPS.length-1;
    return(
      <div className="absolute inset-0 z-50 flex flex-col items-center justify-center px-6"
        style={{background:"linear-gradient(160deg,#05001a 0%,#001020 60%,#050a00 100%)"}}>
        <div className="w-full max-w-sm flex flex-col items-center gap-6 text-center">
          <div className="text-xs uppercase tracking-widest opacity-50" style={{color:theme.accent}}>
            Step {(tutStep||0)+1} / {TUT_STEPS.length}
          </div>
          <div className="text-7xl" style={{animation:"storyFloat 1.8s ease-in-out infinite",filter:`drop-shadow(0 0 24px ${theme.accent})`}}>
            {step.emoji}
          </div>
          {/* Demo fake tap target */}
          {step.demo&&(
            <div onClick={()=>{sfx("tap");spawnParticles&&null;}}
              className="w-16 h-16 rounded-full flex items-center justify-center cursor-pointer"
              style={{background:`radial-gradient(circle at 38% 36%,${theme.accent}cc,${theme.accent}44)`,
                boxShadow:`0 0 32px ${theme.accent}99`,border:`2px solid ${theme.accent}`,
                animation:"floatGlow 1s ease-in-out infinite"}}>
              <span className="text-2xl font-black" style={{color:"#fff"}}>!</span>
            </div>
          )}
          <h2 className="font-black text-2xl" style={{color:theme.accent,fontFamily:"'Rajdhani','Exo 2',sans-serif",textShadow:`0 0 20px ${theme.accent}88`}}>
            {step.title}
          </h2>
          <p className="text-base leading-relaxed opacity-80" style={{color:"#e8e8f0",lineHeight:1.7}}>
            {step.body}
          </p>
          {/* Dot indicators */}
          <div className="flex gap-2">
            {TUT_STEPS.map((_,i)=>(
              <div key={i} style={{width:8,height:8,borderRadius:"50%",background:i===(tutStep||0)?theme.accent:"#ffffff22"}}/>
            ))}
          </div>
          <NeonButton onClick={()=>{
            if(isLast){
              saveRef.current.seenTutorial=true;debounceSave();
              setTutStep(null);
              if(!saveRef.current.seenMainStory){
                setStoryData({type:"main",panelIndex:0,onDone:()=>go("levelmap")});
              } else {setScreen("levelmap");}
            } else {
              setTutStep((tutStep||0)+1);
            }
          }} className="w-full py-4 text-lg font-black"
            style={{background:`linear-gradient(135deg,${theme.secondary||theme.accent},${theme.accent})`,
              boxShadow:`0 0 32px ${theme.accent}77`}}>
            {step.cta}
          </NeonButton>
          <button onClick={()=>{
            saveRef.current.seenTutorial=true;debounceSave();setTutStep(null);go("levelmap");
          }} style={{color:"#ffffff30",background:"none",border:"none",cursor:"pointer",fontSize:"0.75rem"}}>
            Skip tutorial
          </button>
        </div>
      </div>
    );
  };

  // ── Menu ──
  const renderMenu=()=>{
    // Cycle through world emojis for the title decoration
    const worldEmojiRow=WORLDS.map(w=>w.emoji).join(" ");
    return(
    <div className="flex flex-col items-center justify-center h-full gap-4 px-5 relative z-10 pb-6">
      {/* Title block */}
      <div className="text-center">
        <div className="text-base tracking-widest opacity-50 mb-1" style={{color:theme.accent}}>🐉 🌿 ✨ 🔮 ❄️ ⛏️ 👻 🌊 ⛰️ 🌈</div>
        <h1 className="font-black leading-none" style={{
          fontSize:"clamp(2.8rem,11vw,4.2rem)",letterSpacing:"0.1em",
          fontFamily:"'Rajdhani','Exo 2',sans-serif",
          background:`linear-gradient(160deg,${theme.accent} 0%,#ffffff 50%,${theme.accent} 100%)`,
          backgroundSize:"200% auto",
          WebkitBackgroundClip:"text",WebkitTextFillColor:"transparent",
          filter:`drop-shadow(0 0 28px ${theme.accent}aa)`,
          animation:"shimmer 4s linear infinite",
        }}>
          REALM<br/><span style={{fontSize:"0.62em",letterSpacing:"0.22em"}}>QUEST</span>
        </h1>
        <p className="text-xs mt-2 opacity-60 tracking-widest uppercase" style={{color:theme.accent,fontFamily:"'Rajdhani',sans-serif"}}>
          10 Worlds · 100 Levels · Fun for Everyone!
        </p>
        {/* XP bar */}
        <div className="mt-3 flex items-center gap-2 justify-center">
          <span className="text-xs font-bold px-2 py-0.5 rounded-full" style={{background:theme.accent+"22",color:theme.accent}}>LV {lvl}</span>
          <div className="w-28 h-1.5 rounded-full" style={{background:"#ffffff18"}}>
            <div className="h-full rounded-full" style={{width:`${(sv.xp%XP_PER_LVL)/XP_PER_LVL*100}%`,background:theme.accent,boxShadow:`0 0 8px ${theme.accent}`}}/>
          </div>
          <span className="text-xs opacity-35" style={{color:theme.accent}}>{xpToNext(sv.xp)}xp</span>
          {(sv.skillPoints||0)>0&&(
            <button onClick={()=>setScreen("skilltree")}
              className="ml-2 px-2 py-0.5 rounded-lg font-black text-xs"
              style={{background:`${theme.accent}33`,border:`1px solid ${theme.accent}88`,color:theme.accent,animation:"heartbeat 1.5s ease-in-out infinite",outline:"none"}}>
              ✨ {sv.skillPoints}
            </button>
          )}
        </div>
      </div>

      {/* ── Mascot showcase on menu ── */}
      <div className="flex flex-col items-center gap-2" style={{marginTop:-4,marginBottom:-4}}>
        {/* Time-based greeting speech bubble */}
        {(()=>{
          const h=new Date().getHours();
          const streak=sv.loginStreak||0;
          const name=currentMascot.name;
          let greeting;
          if(streak>=7&&Math.random()<0.4) greeting=`Day ${streak} streak! 🔥`;
          else if(h>=5&&h<11) greeting=`Good morning! ☀️`;
          else if(h>=11&&h<17) greeting=`Hey there! 👋`;
          else if(h>=17&&h<22) greeting=`Good evening! 🌙`;
          else greeting=`Up late? Let's play! 🌌`;
          return(
            <div style={{
              fontSize:11,fontWeight:"bold",padding:"5px 12px",borderRadius:14,
              background:`${currentMascot.color}22`,border:`1px solid ${currentMascot.color}55`,
              color:currentMascot.color,
              animation:"speechBubble 0.5s cubic-bezier(0.34,1.5,0.64,1) both",
              marginBottom:4,position:"relative"}}>
              {greeting}
            </div>
          );
        })()}
        <MascotEmoji mood="idle" size={90}/>
        <div className="font-black tracking-widest" style={{
          fontSize:"0.8rem",color:currentMascot.color,
          textShadow:`0 0 14px ${currentMascot.color}`,animation:"floatGlow 2s ease-in-out infinite"}}>
          {currentMascot.name} — your companion! 🌟
        </div>
      </div>

      {/* Quest story teaser */}
      {(sv.unlockedLevel||1)<=3&&(
        <div className="w-full rounded-2xl px-4 py-3 flex items-center gap-3 cursor-pointer"
          style={{background:`${theme.accent}0c`,border:`1px solid ${theme.accent}30`}}
          onClick={()=>setStoryData({type:"main",panelIndex:0,onDone:()=>go("levelmap")})}>
          <span style={{fontSize:28}}>🌈</span>
          <div>
            <div className="text-xs font-bold mb-0.5" style={{color:theme.accent}}>🗺️ Your Quest</div>
            <div className="text-xs opacity-60 leading-snug" style={{color:theme.accent}}>{MAIN_STORY.intro[0].slice(0,70)}…</div>
          </div>
        </div>
      )}

      {/* World progress strip */}
      <div className="flex gap-1 justify-center flex-wrap">
        {WORLDS.map(w=>{
          const wLevels=Array.from({length:10},(_,i)=>(w.id-1)*10+i+1);
          const done=wLevels.filter(l=>(sv.levelStars[l]||0)>0).length;
          return(
            <div key={w.id} className="flex flex-col items-center" style={{opacity:done>0?1:0.3}}>
              <span style={{fontSize:18}}>{w.emoji}</span>
              <div style={{width:20,height:3,borderRadius:2,background:done===10?w.color:`${w.color}44`,boxShadow:done===10?`0 0 6px ${w.color}`:"none"}}/>
            </div>
          );
        })}
      </div>

      {/* Coins + streak */}
      <div className="flex items-center gap-3">
        <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:"#fbbf2415",border:"1px solid #fbbf2430"}}>
          <span>🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>{sv.coins||0}</span>
        </div>
        <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:theme.accent+"15",border:`1px solid ${theme.accent}30`}}>
          <span className="text-xs" style={{color:theme.accent}}>Day {sv.loginStreak||1} 🔥</span>
        </div>
        {sv.highScore>0&&<div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:"#ffffff08",border:"1px solid #ffffff15"}}>
          <span className="text-xs opacity-50">Best {sv.highScore.toLocaleString()}</span>
        </div>}
      </div>

      {/* Play button */}
      <NeonButton onClick={()=>{
        if(!saveRef.current.seenTutorial){
          setTutStep(0);
        } else if(!saveRef.current.seenMainStory){
          setStoryData({type:"main",panelIndex:0,onDone:()=>go("levelmap")});
        } else {
          setScreen("levelmap");
        }
      }} className="w-full py-5 text-2xl"
        style={{background:`linear-gradient(135deg,${theme.secondary},${theme.accent})`,boxShadow:`0 0 36px ${theme.accent}66`,
          fontSize:"1.4rem",letterSpacing:"0.1em"}}>
        🌟 START ADVENTURE!
      </NeonButton>

      {/* Daily Spin */}
      {(()=>{const alreadySpun=sv.lastSpinDate===getTodayKey();return(
        <NeonButton onClick={()=>!alreadySpun&&go("spinwheel")} className="w-full py-3 text-base"
          style={{background:alreadySpun?"#ffffff08":`${theme.accent}22`,border:`1px solid ${alreadySpun?"#ffffff15":theme.accent+"66"}`,
            color:alreadySpun?"#ffffff30":theme.accent,opacity:alreadySpun?0.5:1}}>
          🎡 {alreadySpun?"Daily Spin (come back tomorrow)":"Daily Spin — FREE prize!"}
        </NeonButton>
      );})()}

      {/* Zen Mode — always accessible from level 5+ */}
      {(sv.unlockedLevel||1)>=5&&(
        <NeonButton onClick={()=>go("zen")}
          className="w-full py-3 text-base font-black"
          style={{background:"linear-gradient(135deg,#05966922,#34d39933)",border:"2px solid #34d39966",
            color:"#34d399",boxShadow:"0 0 20px #34d39933",letterSpacing:"0.06em"}}>
          ☯ ZEN MODE {sv.zenBest>0?`• Best: ${sv.zenBest.toLocaleString()}`:""}
        </NeonButton>
      )}
      {/* Infinity Mode — unlocked after level 100 */}
      {(sv.unlockedLevel||1)>100&&(
        <NeonButton onClick={()=>go("infinity")}
          className="w-full py-3 text-base font-black"
          style={{background:"linear-gradient(135deg,#a78bfa22,#6d28d955)",border:"2px solid #a78bfa66",
            color:"#a78bfa",boxShadow:"0 0 24px #a78bfa33",letterSpacing:"0.06em"}}>
          ∞ INFINITY MODE {sv.infinityBest>0?`• Best: ${sv.infinityBest.toLocaleString()}`:""}
        </NeonButton>
      )}
      {/* Daily Boss Gauntlet */}
      {(()=>{
        const alreadyDone=sv.gauntletDate===getTodayKey();
        if((sv.unlockedLevel||1)<11)return null;
        return(
          <NeonButton onClick={()=>{if(!alreadyDone)go("gauntlet");}}
            className="w-full py-3 text-sm font-black"
            style={{background:alreadyDone?"#ffffff08":"#ff6b3522",border:`1px solid ${alreadyDone?"#ffffff15":"#ff6b3566"}`,
              color:alreadyDone?"#ffffff30":"#ff6b35",opacity:alreadyDone?0.5:1}}>
            ⚔️ {alreadyDone?"Daily Gauntlet (done today)":`Daily Boss Gauntlet! ${sv.gauntletBest>0?`• Record: ${sv.gauntletBest} bosses`:""}`}
          </NeonButton>
        );
      })()}
      {/* Weekly Challenge */}
      {(()=>{
        if((sv.unlockedLevel||1)<20)return null;
        const wk=getWeekKey();
        const isThisWeek=sv.weeklyChallengeDate===wk;
        const done=isThisWeek&&sv.weeklyChallengeCompleted;
        const wkLvl=getWeeklyChallengeLevel();
        return(
          <NeonButton onClick={()=>{if(!done)go("weekly");}}
            className="w-full py-3 text-sm font-black"
            style={{background:done?"#ffffff08":"linear-gradient(135deg,#a78bfa22,#7c3aed22)",
              border:`1px solid ${done?"#ffffff15":"#a78bfa66"}`,
              color:done?"#ffffff30":"#a78bfa",opacity:done?0.5:1}}>
            🗓️ {done?"Weekly Done — see you Monday!":`Weekly Challenge: Level ${wkLvl}!`}
          </NeonButton>
        );
      })()}
      {/* Daily Tournament */}
      {(()=>{
        if((sv.unlockedLevel||1)<5)return null;
        const today=getTodayKey();
        const isToday=sv.tournamentDate===today;
        const todayBest=isToday?(sv.tournamentBest||0):0;
        const dailyLvl=getDailyChallengeLevel();
        return(
          <NeonButton onClick={()=>go("tournament")}
            className="w-full py-3 text-sm font-black"
            style={{background:"linear-gradient(135deg,#fbbf2422,#d9770622)",
              border:"1px solid #fbbf2466",color:"#fbbf24"}}>
            🏆 Daily Tournament: Lv {dailyLvl} {todayBest>0?`• Best: ${todayBest.toLocaleString()}`:""}
          </NeonButton>
        );
      })()}
      {/* Quick links */}
      <div className="grid grid-cols-2 gap-3 w-full">
        {[{label:"🎯 Daily Quests",sc:"missions"},{label:"🏆 High Scores",sc:"leaderboard"},{label:"🏅 Trophies",sc:"achievements"},{label:"🌿 Skill Tree",sc:"skilltree"},{label:"⚙️ Settings",sc:"settings"}].map(b=>(
          <NeonButton key={b.sc} onClick={()=>setScreen(b.sc)} className="py-3 text-sm"
            style={{background:"#ffffff0d",border:`1px solid ${theme.accent}30`}}>{b.label}</NeonButton>
        ))}
      </div>
    </div>
  );};

  // ── Daily Spin Wheel ──
  const SPIN_PRIZES=[
    {label:"20 coins",   emoji:"🪙", value:20,  type:"coins", color:"#fbbf24"},
    {label:"50 coins",   emoji:"🪙", value:50,  type:"coins", color:"#f59e0b"},
    {label:"100 coins",  emoji:"💰", value:100, type:"coins", color:"#d97706"},
    {label:"100 XP",     emoji:"⭐", value:100, type:"xp",    color:"#60a5fa"},
    {label:"200 XP",     emoji:"🌟", value:200, type:"xp",    color:"#818cf8"},
    {label:"+1 Life",    emoji:"❤️", value:1,   type:"life",  color:"#f87171"},
    {label:"Lucky Star", emoji:"✨", value:0,   type:"lucky", color:"#ffd700"},
    {label:"Power-Up",   emoji:"⚡", value:0,   type:"powerup",color:"#34d399"},
  ];
  const renderSpinWheel=()=>{
    const sliceAngle=360/SPIN_PRIZES.length;
    const canSpin=!spinState;
    const doSpin=()=>{
      if(!canSpin)return;
      const prizeIdx=Math.floor(Math.random()*SPIN_PRIZES.length);
      const targetDeg=1800+prizeIdx*sliceAngle+(sliceAngle/2-10);
      setSpinState("spinning");setSpinDeg(prev=>prev+targetDeg);
      sfx("jackpot");
      setTimeout(()=>{
        const prize=SPIN_PRIZES[prizeIdx];
        const sv2=saveRef.current;
        if(prize.type==="coins"){sv2.coins=(sv2.coins||0)+prize.value;sv2.totalCoins=(sv2.totalCoins||0)+prize.value;}
        else if(prize.type==="xp"){sv2.xp=(sv2.xp||0)+prize.value;}
        else if(prize.type==="lucky"){/* handled in next session via lucky mode */}
        else if(prize.type==="life"){/* awarded at start of next level */sv2.pendingLife=true;}
        sv2.lastSpinDate=getTodayKey();
        flushSave();
        setSpinResult(prize);setSpinState("done");
        sfx("levelComplete");vibrate([20,30,20,60]);
      },2400);
    };
    return(
      <div className="flex flex-col h-full overflow-y-auto relative z-10 items-center justify-center px-5 gap-6"
        style={{background:"radial-gradient(ellipse at top,#0d0025 0%,#000510 60%)"}}>
        <style>{`@keyframes wheelSpin{to{transform:rotate(var(--wheel-end))}} @keyframes prizeReveal{0%{transform:scale(0.4);opacity:0}70%{transform:scale(1.18)}100%{transform:scale(1);opacity:1}}`}</style>
        <div className="flex items-center gap-3 self-start">
          <NeonButton onClick={()=>{setSpinState(null);setSpinResult(null);go("menu");}} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>🎡 Daily Spin</h2>
        </div>
        {/* Wheel */}
        <div className="relative flex items-center justify-center" style={{width:260,height:260}}>
          {/* Pointer */}
          <div className="absolute z-10" style={{top:-12,left:"50%",transform:"translateX(-50%)",width:0,height:0,
            borderLeft:"10px solid transparent",borderRight:"10px solid transparent",
            borderTop:`22px solid ${theme.accent}`,filter:`drop-shadow(0 0 8px ${theme.accent})`}}/>
          {/* Wheel SVG */}
          <div style={{width:260,height:260,borderRadius:"50%",overflow:"hidden",
            transform:`rotate(${spinDeg}deg)`,
            transition:spinState==="spinning"?"transform 2.4s cubic-bezier(0.17,0.67,0.24,1)":"none",
            boxShadow:`0 0 40px ${theme.accent}55`,border:`3px solid ${theme.accent}66`}}>
            <svg width="260" height="260" viewBox="0 0 260 260">
              {SPIN_PRIZES.map((p,i)=>{
                const startAngle=(i*sliceAngle-90)*Math.PI/180;
                const endAngle=((i+1)*sliceAngle-90)*Math.PI/180;
                const x1=130+120*Math.cos(startAngle),y1=130+120*Math.sin(startAngle);
                const x2=130+120*Math.cos(endAngle),y2=130+120*Math.sin(endAngle);
                const mx=130+75*Math.cos((startAngle+endAngle)/2),my=130+75*Math.sin((startAngle+endAngle)/2);
                return(
                  <g key={i}>
                    <path d={`M130,130 L${x1},${y1} A120,120 0 0,1 ${x2},${y2} Z`} fill={p.color} opacity={0.85}/>
                    <text x={mx} y={my} textAnchor="middle" dominantBaseline="middle"
                      fontSize="18" style={{userSelect:"none"}}>{p.emoji}</text>
                  </g>
                );
              })}
              <circle cx="130" cy="130" r="18" fill="#1a1a2e" stroke={theme.accent} strokeWidth="2"/>
            </svg>
          </div>
        </div>
        {/* Prize reveal */}
        {spinState==="done"&&spinResult&&(
          <div className="flex flex-col items-center gap-3 text-center" style={{animation:"prizeReveal 0.6s ease-out"}}>
            <div style={{fontSize:56,filter:`drop-shadow(0 0 20px ${spinResult.color})`}}>{spinResult.emoji}</div>
            <div className="font-black text-2xl" style={{color:spinResult.color,fontFamily:"'Rajdhani',sans-serif",
              textShadow:`0 0 20px ${spinResult.color}`}}>
              YOU WON: {spinResult.label.toUpperCase()}!
            </div>
            <NeonButton onClick={()=>{setSpinState(null);setSpinResult(null);go("menu");}} className="px-8 py-3 text-base"
              style={{background:`linear-gradient(135deg,${theme.secondary||theme.accent},${theme.accent})`}}>
              🎉 Awesome! Collect
            </NeonButton>
          </div>
        )}
        {/* Spin button */}
        {!spinState&&(
          <NeonButton onClick={doSpin} className="px-12 py-4 text-xl font-black"
            style={{background:`linear-gradient(135deg,${theme.secondary||theme.accent},${theme.accent})`,
              boxShadow:`0 0 40px ${theme.accent}88`,fontSize:"1.3rem",letterSpacing:"0.08em"}}>
            🎡 SPIN!
          </NeonButton>
        )}
        {spinState==="spinning"&&(
          <div className="font-black text-lg" style={{color:theme.accent,animation:"shimmer 1s linear infinite"}}>
            ✨ Spinning... ✨
          </div>
        )}
        <p className="text-xs opacity-40 text-center" style={{color:theme.accent}}>One free spin per day — come back tomorrow!</p>
      </div>
    );
  };

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
          <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>🗺️ Adventure Map</h2>
          <span className="ml-auto text-sm font-bold" style={{color:"#fbbf24"}}>🪙 {sv.coins||0}</span>
        </div>
        {/* Scrollable map */}
        <div className="flex-1 overflow-y-auto" style={{WebkitOverflowScrolling:"touch"}}>
          {WORLDS.map(world=>{
            const levelStart=(world.id-1)*10+1;
            const levels=ALL_LEVELS.slice(levelStart-1,levelStart+9);
            const doneLevels=levels.filter(l=>(sv.levelStars[l.id]||0)>0).length;
            const worldFullyDone=doneLevels===10;
            // Total stars in this world (max 30)
            const worldStars=levels.reduce((s,lv)=>s+(sv.levelStars[lv.id]||0),0);
            // Is this the "current" world? (player is unlocking levels here)
            const isCurrentWorld=unlockedTo>=levelStart&&unlockedTo<=levelStart+9;
            return(
              <div key={world.id} className="mb-2">
                {/* World banner — immersive, tappable for story */}
                <div className="flex items-center gap-3 px-4 py-3 mx-2 mt-3 rounded-2xl relative overflow-hidden"
                  onClick={()=>{
                    setStoryData({type:"world",worldId:world.id,panelIndex:0,onDone:()=>{}});
                  }}
                  style={{background:`${world.color}15`,border:`1px solid ${world.color}${isCurrentWorld?"99":"55"}`,backdropFilter:"blur(6px)",
                    boxShadow:worldFullyDone?`0 0 24px ${world.color}66`:isCurrentWorld?`0 0 16px ${world.color}55`:"none",
                    cursor:"pointer"}}>
                  {/* World-color gradient bg */}
                  <div style={{position:"absolute",inset:0,background:`linear-gradient(120deg,${world.color}18 0%,transparent 65%)`,pointerEvents:"none"}}/>
                  {/* Shimmer sweep — only for fully-done worlds */}
                  {worldFullyDone&&(
                    <div style={{position:"absolute",inset:0,pointerEvents:"none",
                      background:`linear-gradient(120deg,transparent 35%,${world.color}33 50%,transparent 65%)`,
                      backgroundSize:"200% 100%",animation:"shimmer 4s linear infinite"}}/>
                  )}
                  <span style={{fontSize:32,lineHeight:1,zIndex:1,
                    filter:`drop-shadow(0 0 ${worldFullyDone?12:6}px ${world.color})`,
                    animation:isCurrentWorld?"floatGlow 2.4s ease-in-out infinite":"none"}}>{world.emoji}</span>
                  <div style={{zIndex:1,flex:1}}>
                    <div className="font-black text-base leading-tight" style={{color:world.color}}>{world.name}</div>
                    <div className="text-xs opacity-60 flex items-center gap-2" style={{color:world.color}}>
                      <span>World {world.id}</span>
                      <span style={{opacity:0.5}}>·</span>
                      <span>⭐ {worldStars}/30</span>
                      <span style={{opacity:0.5}}>·</span>
                      <span>📖 Story</span>
                    </div>
                  </div>
                  {worldFullyDone&&<div className="ml-auto flex flex-col items-center gap-0.5" style={{zIndex:1}}>
                    <span style={{fontSize:22,animation:"heartbeat 1.6s ease-in-out infinite",
                      filter:`drop-shadow(0 0 8px ${world.color})`}}>🏆</span>
                    {worldStars>=30
                      ?<span style={{fontSize:8,fontWeight:"black",letterSpacing:"0.06em",
                          color:"#ffd700",background:"#ffd70022",padding:"1px 6px",borderRadius:6,
                          border:"1px solid #ffd70066",animation:"shimmer 2s linear infinite",whiteSpace:"nowrap"}}>⭐ PERFECT</span>
                      :<span style={{fontSize:8,color:world.color,opacity:0.7}}>⭐ {worldStars}/30</span>
                    }
                  </div>}
                  {!worldFullyDone&&<div className="ml-auto flex flex-col items-end gap-0.5" style={{zIndex:1}}>
                    {isCurrentWorld&&<span style={{fontSize:8,fontWeight:"black",letterSpacing:"0.06em",
                      color:world.color,background:`${world.color}22`,padding:"1px 5px",borderRadius:6,
                      border:`1px solid ${world.color}66`}}>📍 HERE</span>}
                    <div className="flex gap-0.5">
                      {Array.from({length:10},(_,i)=>(
                        <div key={i} style={{width:5,height:14,borderRadius:2,
                          background:i<doneLevels?world.color:`${world.color}25`,
                          boxShadow:i<doneLevels?`0 0 4px ${world.color}`:"none"}}/>
                      ))}
                    </div>
                  </div>}
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
                      return<line key={i} x1={x1} y1={y1} x2={x2} y2={y2} stroke={unlocked?world.color+"77":"#ffffff15"} strokeWidth={unlocked?3:1.5} strokeDasharray={unlocked?"none":"6,4"}/>;
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
                    const nodeR=lv.isBoss?38:30;
                    const nodeLabel=locked?"🔒":lv.isBoss?(stars>0?"👑":world.emoji):lv.id;
                    return(
                      <div key={lv.id}
                        className="absolute flex flex-col items-center"
                        style={{left:x,top:y,transform:"translate(-50%,-50%)",width:90,cursor:locked?"default":"pointer"}}
                        onClick={()=>{if(!locked){
                          if(stars>0&&lv.id<(sv.unlockedLevel||1)){setReplayModal(lv.id);}
                          else{setSelectedLevel(lv.id);go("shop");}
                        }}}
                        onTouchEnd={e=>{e.preventDefault();if(!locked){
                          if(stars>0&&lv.id<(sv.unlockedLevel||1)){setReplayModal(lv.id);}
                          else{setSelectedLevel(lv.id);go("shop");}
                        }}}
                      >
                        {/* Node circle */}
                        <div className="flex items-center justify-center rounded-full font-black transition-all"
                          style={{
                            width:nodeR*2,height:nodeR*2,
                            background:locked?"#111118":stars>0?`${world.color}44`:`${world.color}1a`,
                            border:`${isCurrent||isAvailable?3:2}px solid ${locked?"#2a2a3a":world.color}`,
                            boxShadow:isAvailable?`0 0 24px ${world.color}99,0 0 48px ${world.color}33`:
                                       stars===3?`0 0 16px ${world.color}77`:
                                       lv.isBoss&&!locked?`0 0 12px ${world.color}55`:"none",
                            color:locked?"#333":world.color,
                            animation:isAvailable?"levelPulse 1.5s ease-in-out infinite":"none",
                            fontSize:lv.isBoss?22:13,
                          }}>
                          {nodeLabel}
                        </div>
                        {/* Stars */}
                        <div className="flex gap-0.5 mt-1">
                          {[1,2,3].map(s=>(
                            <span key={s} style={{fontSize:10,opacity:stars>=s?1:0.15,color:"#fbbf24",
                              filter:stars>=s?"drop-shadow(0 0 4px #fbbf24)":"none"}}>★</span>
                          ))}
                        </div>
                        {/* Name shown for available + boss levels */}
                        {(!locked&&(isAvailable||isCurrent||lv.isBoss))&&(
                          <div className="text-center mt-0.5" style={{fontSize:9,color:world.color,opacity:0.85,maxWidth:82,lineHeight:1.2,fontWeight:"bold"}}>
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
      {/* Replay modal — absolute overlay inside the levelmap container */}
      {replayModal&&(()=>{
        const rlv=getLevelConfig(replayModal);
        const rstars=sv.levelStars[replayModal]||0;
        const _s0=sv.scores?.[0];const prevBest=sv.levelScores?.[replayModal]||(typeof _s0==="number"?_s0:_s0?.score)||0;
        return(
          <div className="absolute inset-0 flex items-center justify-center z-50 px-6"
            style={{background:"rgba(0,0,0,0.88)",backdropFilter:"blur(12px)"}}>
            <div className="w-full max-w-sm rounded-3xl p-6 flex flex-col gap-4"
              style={{background:`${rlv.worldColor}14`,border:`2px solid ${rlv.worldColor}55`}}>
              <div className="text-center">
                <div className="font-black text-lg" style={{color:rlv.worldColor}}>Level {rlv.id}: {rlv.name}</div>
                <div className="flex justify-center gap-1 mt-1">
                  {[1,2,3].map(s=><span key={s} style={{fontSize:18,opacity:rstars>=s?1:0.2,color:"#fbbf24"}}>★</span>)}
                </div>
                {prevBest>0&&<div className="text-xs mt-1 opacity-60" style={{color:rlv.worldColor}}>Best: {prevBest.toLocaleString()} pts</div>}
              </div>
              <NeonButton onClick={()=>{setReplayModal(null);setSelectedLevel(replayModal);go("shop");}}
                className="w-full py-4 font-black"
                style={{background:`linear-gradient(135deg,${rlv.worldColor}33,${rlv.worldColor}55)`,border:`2px solid ${rlv.worldColor}`,color:rlv.worldColor}}>
                🎮 Play Again
              </NeonButton>
              {rstars>0&&(
                <NeonButton onClick={()=>{
                  // Pick a random challenge modifier (not boss_kill or final_boss)
                  const challengeMods=[
                    {type:"combo_20",desc:"20× combo challenge ⭐"},
                    {type:"no_miss",desc:"Perfect run — no misses! 🎯"},
                    {type:"moving_only",desc:"Moving targets only! 💨"},
                    {type:"ghost_rush",desc:"Find the ghosts! 👻"},
                    {type:"fever_2",desc:"Activate Fever twice! ✨"},
                  ];
                  const mod=challengeMods[Math.floor(Math.random()*challengeMods.length)];
                  const challengeCfg=getLevelConfig(replayModal);
                  // Apply modifier and +50% XP bonus flag
                  challengeCfg.modifier=mod;
                  challengeCfg._challengeBonus=true; // endLevel checks this for +50% XP
                  setReplayModal(null);
                  // Start directly (no shop)
                  startGame(replayModal,[],null);
                  // Override the config after startGame sets it
                  setTimeout(()=>{if(levelCfgRef.current){levelCfgRef.current.modifier=mod;levelCfgRef.current._challengeBonus=true;}},50);
                }}
                  className="w-full py-3 font-black"
                  style={{background:"linear-gradient(135deg,#fbbf2422,#f9780433)",border:"2px solid #fbbf2488",color:"#fbbf24"}}>
                  ⚡ Challenge Mode <span style={{fontSize:10,opacity:0.7}}>+50% XP</span>
                </NeonButton>
              )}
              <NeonButton onClick={()=>setReplayModal(null)}
                className="w-full py-3 text-sm" style={{background:"#ffffff08",border:"1px solid #ffffff15"}}>
                Cancel
              </NeonButton>
            </div>
          </div>
        );
      })()}
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
            <NeonButton onClick={()=>go("levelmap")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Map</NeonButton>
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
        {/* Story teaser card */}
        {(()=>{const ws=WORLD_STORIES.find(s=>s.worldId===cfg.world);if(!ws)return null;
          const snippet=cfg.isBoss?ws.bossIntro?.text:ws.panels[0]?.text;
          if(!snippet)return null;
          const emo=cfg.isBoss?(ws.bossIntro?.emoji||WORLDS[cfg.world-1].emoji):ws.panels[0]?.emoji;
          return(
            <div className="rounded-2xl px-4 py-3 flex items-center gap-3 cursor-pointer"
              style={{background:`${cfg.worldColor}0c`,border:`1px solid ${cfg.worldColor}33`}}
              onClick={()=>{
                if(cfg.isBoss){setStoryData({type:"boss",worldId:cfg.world,bossIntro:ws.bossIntro,onDone:()=>{}});}
                else{setStoryData({type:"world",worldId:cfg.world,panelIndex:0,onDone:()=>{}});}
              }}>
              <span style={{fontSize:26,flexShrink:0}}>{emo}</span>
              <div>
                <div className="text-xs font-bold mb-0.5" style={{color:cfg.worldColor}}>📖 Story</div>
                <div className="text-xs opacity-60 leading-snug" style={{color:cfg.worldColor,overflow:"hidden",display:"-webkit-box",WebkitLineClamp:2,WebkitBoxOrient:"vertical"}}>{snippet}</div>
              </div>
            </div>
          );
        })()}
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
          // The actual start logic, extracted so confirmation can call it
          const doStart=()=>{
            sv.coins-=total;flushSave();
            const isFirstLevelOfWorld=cfg.id%10===1;
            const seenWorlds=saveRef.current.seenWorldStories||[];
            const seenBosses=saveRef.current.seenBossIntros||[];
            if(cfg.isBoss&&!seenBosses.includes(cfg.world)){
              const ws=WORLD_STORIES.find(s=>s.worldId===cfg.world);
              if(ws?.bossIntro){
                setStoryData({type:"boss",worldId:cfg.world,bossIntro:ws.bossIntro,onDone:()=>startGame(selectedLevel,cartItems)});
                return;
              }
            }
            if(isFirstLevelOfWorld&&!seenWorlds.includes(cfg.world)){
              setStoryData({type:"world",worldId:cfg.world,panelIndex:0,onDone:()=>startGame(selectedLevel,cartItems)});
            } else {
              startGame(selectedLevel,cartItems);
            }
          };
          // Confirm if buying anything
          if(total>0){
            setShopConfirm({total,items:[...cartItems],onConfirm:()=>{setShopConfirm(null);doStart();}});
          } else {
            doStart();
          }
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
    const speedMode=sv.speedMode||1.0;
    const speedLabel=speedMode<=0.75?"🐢":speedMode>=1.5?"🔥":speedMode>=1.2?"⚡":speedMode>=1?"":"";
    return(
      <div className="absolute inset-0" onTouchStart={handleTap} onClick={handleTap} style={{touchAction:"none",zIndex:10}}>
        {/* Mode indicators (top corners, non-default modes only) */}
        <div className="absolute top-2 right-2 z-30 flex flex-col gap-1 items-end pointer-events-none">
          {speedMode!==1.0&&(
            <div style={{padding:"3px 8px",borderRadius:8,background:`${wc}33`,border:`1px solid ${wc}66`,
              color:"#fff",fontSize:10,fontWeight:"bold",letterSpacing:"0.04em",boxShadow:`0 0 8px ${wc}44`}}>
              {speedLabel} {speedMode.toFixed(1)}×
            </div>
          )}
          {sv.colorblindMode&&(
            <div style={{padding:"3px 8px",borderRadius:8,background:`${wc}33`,border:`1px solid ${wc}66`,
              color:"#fff",fontSize:10,fontWeight:"bold",letterSpacing:"0.04em"}}>
              ♛ CB
            </div>
          )}
          {sv.adaptiveDifficulty&&(
            <div style={{padding:"3px 8px",borderRadius:8,background:"#06b6d433",border:"1px solid #06b6d466",
              color:"#fff",fontSize:10,fontWeight:"bold",letterSpacing:"0.04em"}}>
              🎯 AUTO
            </div>
          )}
        </div>
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
            {cfg&&<div className="text-xs font-bold px-1.5 py-0.5 rounded-full" style={{background:wc+"22",color:wc}}>{WORLDS[cfg.world-1].emoji} L{cfg.id}</div>}
            {/* Mascot HUD chip — tiny */}
            <span style={{fontSize:16,lineHeight:1}}>{currentMascot.e[mascotMood]||currentMascot.e.idle}</span>
          </div>
          <div className="flex-1 flex flex-col items-center justify-center py-2 px-1">
            <div className="text-xs opacity-35 tracking-widest uppercase" style={{color:wc}}>Streak</div>
            <div className="text-xl font-black tabular-nums"
              style={{
                color:streakDecaying&&hud.streak>0?"#ef4444":streakColor(),
                textShadow:hud.streak>=5?`0 0 14px ${streakDecaying?"#ef4444":streakColor()}`:"none",
                animation:streakDecaying&&hud.streak>0?"heartbeat 0.6s ease-in-out infinite":"none",
              }}>
              {hud.streak}×{streakDecaying&&hud.streak>0?"⚠️":""}
            </div>
            {/* Streak decay bar — only visible when streak > 0 */}
            {hud.streak>0&&(
              <div style={{width:44,height:3,background:"#ffffff18",borderRadius:2,marginTop:2,overflow:"hidden"}}>
                <div style={{
                  width:`${Math.max(0,(hud.decayPct??1))*100}%`,height:"100%",borderRadius:2,
                  background:streakDecaying?"#ef4444":streakColor(),
                  boxShadow:streakDecaying?`0 0 4px #ef4444`:`0 0 4px ${streakColor()}`,
                  transition:"width 0.12s linear",
                }}/>
              </div>
            )}
          </div>
          <button onTouchStart={e=>{e.stopPropagation();togglePause();}} onClick={e=>{e.stopPropagation();togglePause();}}
            className="flex items-center justify-center px-4"
            style={{color:wc,fontSize:18,background:"transparent",border:"none",WebkitTapHighlightColor:"transparent"}}>
            {paused?"▶":"⏸"}
          </button>
        </div>
        {/* Fragment progress chip — shown when boss fragments collected */}
        {(sv.bossFragments||0)>0&&(
          <div className="absolute z-20 pointer-events-none"
            style={{top:78,right:8}}>
            <div className="flex items-center gap-1 px-2 py-0.5 rounded-lg"
              style={{background:"#c084fc22",border:"1px solid #c084fc66",fontSize:9,fontWeight:"bold",color:"#c084fc"}}>
              💎 {sv.bossFragments}/10
              <div style={{width:28,height:4,background:"#ffffff15",borderRadius:2,overflow:"hidden",display:"inline-block",verticalAlign:"middle",marginLeft:2}}>
                <div style={{width:`${(sv.bossFragments/10)*100}%`,height:"100%",background:"#c084fc",boxShadow:"0 0 4px #c084fc"}}/>
              </div>
            </div>
          </div>
        )}
        {/* Boss HP Bar */}
        {hud.boss&&(
          <div className="absolute left-0 right-0 z-20 pointer-events-none flex flex-col items-center gap-0.5" style={{top:76}}>
            <div style={{fontSize:9,fontWeight:"black",letterSpacing:"0.08em",color:hud.boss.rage?"#ff0000":hud.boss.phase===3?"#ef4444":hud.boss.phase===2?"#fbbf24":"#ff6030",
              textTransform:"uppercase",textShadow:hud.boss.rage?"0 0 8px #ff0000":hud.boss.phase===2?"0 0 6px #fbbf24":"none",
              animation:hud.boss.rage?"heartbeat 0.5s ease-in-out infinite":"none"}}>
              {hud.boss.rage?"⚠️ RAGE":"💀 BOSS"} {BOSS_EMOJIS[(cfg?.world||1)-1]}
            </div>
            <div style={{width:160,height:8,background:"#ffffff15",borderRadius:4,overflow:"hidden",
              boxShadow:"0 0 8px rgba(0,0,0,0.5)"}}>
              <div style={{
                width:`${(hud.boss.hp/hud.boss.max)*100}%`,height:"100%",borderRadius:4,
                background:hud.boss.rage?"#ff0000":hud.boss.phase===3?"#ef4444":hud.boss.phase===2?"#fbbf24":"#4ade80",
                boxShadow:hud.boss.rage?"0 0 8px #ff0000":hud.boss.phase===2?"0 0 6px #fbbf24":"0 0 4px #4ade80",
                transition:"width 0.25s ease-out",
              }}/>
            </div>
            <div style={{fontSize:8,color:"#ffffff44",letterSpacing:"0.04em"}}>
              {Array.from({length:hud.boss.max},(_,i)=>(
                <span key={i} style={{marginRight:1,opacity:i<hud.boss.hp?1:0.15}}>♦</span>
              ))}
            </div>
          </div>
        )}
        {/* Modifier goal hint */}
        {hud.modGoal&&(
          <div className="absolute left-0 right-0 flex justify-center z-20" style={{top:hud.boss?120:76}}>
            <div className="px-3 py-1 rounded-xl text-xs font-bold" style={{background:"#fbbf2420",border:"1px solid #fbbf2444",color:"#fbbf24"}}>
              ⚡ {hud.modGoal}
            </div>
          </div>
        )}
        {/* Power-ups */}
        {activePwrDisp.length>0&&(
          <div className="absolute left-0 right-0 flex justify-center gap-2 z-20" style={{top:hud.boss?148:hud.modGoal?108:76}}>
            {activePwrDisp.map(p=>(
              <div key={p.type} className="px-2 py-1 rounded-lg text-xs font-bold flex items-center gap-1"
                style={{background:"#1e3a8acc",border:"1px solid #60a5fa55",color:"#60a5fa"}}>
                {p.type==="SHIELD"?"🛡":p.type==="SLOW"?"🐢":p.type==="DOUBLE"?"×2":p.type==="FREEZE"?"❄️":"❤️"}
                {" "}{p.type}{" "}<span className="opacity-50">{Math.max(0,Math.ceil((p.endsAt-Date.now())/1000))}s</span>
              </div>
            ))}
          </div>
        )}
        {/* Streak Shield indicator */}
        {streakShieldActive&&(
          <div className="absolute right-3 z-25 flex items-center gap-1 px-2 py-1 rounded-xl"
            style={{top:82,background:"#ffd70022",border:"1px solid #ffd70066",animation:"floatGlow 1s ease-in-out infinite"}}>
            <span style={{fontSize:14}}>🛡️</span>
            <span className="text-xs font-black" style={{color:"#ffd700"}}>STREAK SAFE</span>
          </div>
        )}
        {/* Lucky Mode banner */}
        {luckyMode&&(
          <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:140}}>
            <div className="font-black text-lg px-5 py-2 rounded-2xl"
              style={{color:"#ffd700",textShadow:"0 0 24px #ffd700",background:"#ffd70020",border:"2px solid #ffd700aa",
                animation:"legendaryRainbow 1.5s linear infinite"}}>
              ⭐ LUCKY STARS! TAP EVERYTHING! ⭐
            </div>
          </div>
        )}
        {/* New Record banner */}
        {newRecord&&(
          <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:luckyMode?180:140}}>
            <div className="font-black text-sm px-4 py-1.5 rounded-xl"
              style={{color:"#34d399",textShadow:"0 0 16px #34d399",background:"#34d39920",border:"1px solid #34d39966",
                animation:"waveIn 0.4s ease-out"}}>
              🏆 NEW PERSONAL BEST!
            </div>
          </div>
        )}
        {/* Fever */}
        {feverBorder&&<div className="absolute inset-0 pointer-events-none z-10" style={{border:"4px solid #fbbf24",boxShadow:"inset 0 0 60px #fbbf2445,0 0 60px #fbbf2445",animation:"feverPulse 0.6s ease-in-out infinite alternate"}}/>}
        {feverBorder&&<div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:luckyMode||newRecord?184:140}}>
          <span className="font-black text-base px-4 py-1 rounded-full" style={{color:"#fbbf24",textShadow:"0 0 20px #fbbf24",background:"#fbbf2420",animation:"feverPulse 0.5s infinite alternate"}}>✨ MAGIC MODE!</span>
        </div>}
        {epicFlash&&<div className="absolute inset-0 pointer-events-none z-10" style={{background:"#f472b633",animation:"epicFlash 0.5s ease-out forwards"}}/>}
        {perfectFlash&&<div className="absolute inset-0 pointer-events-none z-10" style={{background:"#fbbf2422",animation:"epicFlash 0.35s ease-out forwards"}}/>}
        {comboLabel&&(
          <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:"40%",transform:"translateY(-50%)"}}>
            <div className="font-black px-6 py-2 rounded-2xl"
              style={{fontSize:"clamp(1.4rem,6vw,2.2rem)",color:"#fff",
                textShadow:`0 0 30px ${theme.accent},0 0 60px ${theme.accent}55`,
                background:theme.accent+"22",border:`2px solid ${theme.accent}`,
                animation:"comboAnnounce 0.35s cubic-bezier(0.34,1.5,0.64,1)"}}>
              {comboLabel}
            </div>
          </div>
        )}
        {/* BIG MASCOT COMPANION — right side, cheering you on */}
        <div className="absolute pointer-events-none z-15" style={{bottom:18,right:10,display:"flex",flexDirection:"column",alignItems:"center",gap:4}}>
          {/* Speech bubble */}
          {mascotSpeech&&(
            <div style={{
              background:"rgba(0,0,0,0.88)",border:`2px solid ${currentMascot.color}`,
              borderRadius:14,padding:"6px 10px",maxWidth:130,textAlign:"center",
              fontSize:11,fontWeight:"bold",color:currentMascot.color,lineHeight:1.3,
              boxShadow:`0 0 14px ${currentMascot.color}44`,
              animation:"speechBubble 0.3s cubic-bezier(0.34,1.5,0.64,1)",
              position:"relative"}}>
              {mascotSpeech}
              {/* Triangle pointer */}
              <div style={{
                position:"absolute",bottom:-9,left:"50%",transform:"translateX(-50%)",
                width:0,height:0,borderLeft:"7px solid transparent",
                borderRight:"7px solid transparent",
                borderTop:`9px solid ${currentMascot.color}`}}/>
            </div>
          )}
          <MascotEmoji mood={mascotMood} size={86}/>
          <div style={{fontSize:9,color:currentMascot.color,fontWeight:"bold",opacity:0.75,letterSpacing:"0.05em"}}>
            {currentMascot.name.toUpperCase()}
          </div>
        </div>
        {/* Chain flash popup */}
        {chainFlash&&(Date.now()-chainFlash.at<900)&&(
          <div key={chainFlash.at} className="absolute left-1/2 pointer-events-none z-40"
            style={{top:"45%",transform:"translateX(-50%)",animation:"streakBurstAnim 0.85s cubic-bezier(0.34,1.4,0.64,1) forwards",textAlign:"center",whiteSpace:"nowrap"}}>
            <div className="font-black" style={{fontSize:"clamp(1.2rem,6vw,2rem)",color:"#60a5fa",
              textShadow:"0 0 30px #60a5fa,0 0 60px #60a5fa55",letterSpacing:"0.04em"}}>
              {chainFlash.label}
            </div>
          </div>
        )}
        {/* Streak milestone burst + 50× combo finisher (10C) */}
        {streakBurst&&(
          <div className="absolute left-1/2 pointer-events-none z-40"
            style={{top:"30%",transform:"translateX(-50%)",
              animation:streakBurst.n>=50?"comboFinisher 1.4s cubic-bezier(0.34,1.4,0.64,1) forwards":"streakBurstAnim 1.1s cubic-bezier(0.34,1.4,0.64,1) forwards",
              textAlign:"center",whiteSpace:"nowrap"}}>
            {streakBurst.n>=50&&(
              <div style={{position:"absolute",inset:"-30px",background:"radial-gradient(ellipse at center,#ffd70033 0%,transparent 70%)",animation:"legendaryRainbow 0.8s linear infinite",borderRadius:"50%"}}/>
            )}
            <div className="font-black" style={{fontSize:streakBurst.n>=50?"clamp(2rem,10vw,3.6rem)":"clamp(1.6rem,8vw,2.8rem)",
              color:streakBurst.color,
              textShadow:streakBurst.n>=50?`0 0 60px ${streakBurst.color},0 0 120px ${streakBurst.color}88,0 0 200px #ffd70044`:`0 0 40px ${streakBurst.color},0 0 80px ${streakBurst.color}55`,
              letterSpacing:"0.04em"}}>
              {streakBurst.label}
            </div>
            <div style={{fontSize:"clamp(0.7rem,3vw,1rem)",color:streakBurst.color,opacity:0.8}}>
              {streakBurst.n}× combo!{streakBurst.n>=50?" 🌈 LEGENDARY!":""}
            </div>
          </div>
        )}
        {/* Score Tension Ramp — border glow escalates toward goal */}
        {tensionLevel>=1&&(
          <div className="absolute inset-0 pointer-events-none z-6" style={{
            border:`${tensionLevel+1}px solid`,
            borderColor:["","#fbbf2444","#f9780477","#ff980099","#ffd700cc"][tensionLevel],
            boxShadow:tensionLevel>=3?`inset 0 0 60px #ffd70018`:"none",
            animation:tensionLevel>=3?"feverPulse 0.35s ease-in-out infinite alternate":"none"}}/>
        )}
        {tensionLevel>=3&&(
          <div className="absolute left-0 right-0 pointer-events-none z-27" style={{bottom:76,textAlign:"center"}}>
            <span style={{
              fontWeight:"black",
              color:tensionLevel===4?"#ffd700":"#ff9800",
              fontSize:tensionLevel===4?"clamp(1.2rem,6vw,1.6rem)":"clamp(0.9rem,4.5vw,1.15rem)",
              textShadow:`0 0 28px ${tensionLevel===4?"#ffd700":"#ff9800"}`,
              animation:"floatGlow 0.25s ease-in-out infinite",letterSpacing:"0.04em"
            }}>
              {tensionLevel===4?"⭐ ONE TAP AWAY! ⭐":"🔥 ALMOST THERE!"}
            </span>
          </div>
        )}
        {/* Bonus Round — golden glow + banner */}
        {bonusRound&&(
          <>
            <div className="absolute inset-0 pointer-events-none z-6" style={{
              border:"4px solid #ffd700",
              boxShadow:"inset 0 0 70px #ffd70025,0 0 70px #ffd70025",
              animation:"scorePulse 0.45s ease-in-out infinite alternate"}}/>
            <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:88}}>
              <div style={{
                display:"inline-block",padding:"6px 20px",borderRadius:12,
                background:"linear-gradient(135deg,#b8860b,#ffd700,#b8860b)",
                fontWeight:"black",fontSize:"clamp(0.9rem,4.5vw,1.1rem)",color:"#000",
                animation:"heartbeat 0.55s ease-in-out infinite",
                boxShadow:"0 0 30px #ffd70099",letterSpacing:"0.06em"}}>
                🌟 BONUS ROUND — ALL LEGENDARY! 🌟
              </div>
            </div>
          </>
        )}
        {/* Mystery Box slot-reveal overlay */}
        {mysteryReveal&&(
          <div className="absolute left-1/2 pointer-events-none z-45" style={{
            top:"25%",transform:"translateX(-50%)",
            background:"rgba(0,0,0,0.92)",border:"3px solid #ffd700",
            borderRadius:20,padding:"18px 28px",textAlign:"center",
            boxShadow:"0 0 50px #ffd70055",minWidth:200}}>
            <div style={{color:"#ffd700",fontWeight:"black",fontSize:"1rem",marginBottom:10,letterSpacing:"0.06em"}}>
              🎁 MYSTERY BOX!
            </div>
            <div style={{display:"flex",gap:14,justifyContent:"center",marginBottom:12}}>
              {[0,1,2].map(i=>(
                <div key={i} style={{
                  width:52,height:52,borderRadius:12,
                  border:`2px solid ${mysteryReveal.phase>i?"#ffd700":"#ffffff22"}`,
                  background:mysteryReveal.phase>i?"#ffd70022":"#ffffff08",
                  display:"flex",alignItems:"center",justifyContent:"center",
                  fontSize:28,
                  animation:mysteryReveal.phase<=i?"slotSpin 0.15s linear infinite":"none",
                  boxShadow:mysteryReveal.phase>i?`0 0 18px #ffd700`:"none",
                  transition:"all 0.15s"}}>
                  {mysteryReveal.phase>i
                    ?MYSTERY_PRIZES[mysteryReveal.reels[i]].emoji
                    :"❓"}
                </div>
              ))}
            </div>
            {mysteryReveal.phase===3&&(
              <div style={{color:"#ffd700",fontWeight:"black",fontSize:"1.1rem",
                animation:"victoryBurst 0.4s cubic-bezier(0.34,1.5,0.64,1)"}}>
                {mysteryReveal.prize.label}
              </div>
            )}
          </div>
        )}
        {/* Screen edge world-color glow (intensifies with fever/lucky) */}
        <div className="absolute inset-0 pointer-events-none z-5" style={{
          boxShadow:luckyMode
            ?`inset 0 0 80px #ffd70033,inset 0 0 160px #ffd70018`
            :`inset 0 0 80px ${wc}0a,inset 0 0 160px ${wc}05`,
          border:`1px solid ${luckyMode?"#ffd70033":wc+"0a"}`}}/>
        {/* HEAT METER — streak-powered bar above score bar */}
        {cfg&&(
          <div className="absolute bottom-0 left-0 right-0 z-20" style={{height:10,background:"#00000055"}}>
            {/* Score bar (bottom 5px) */}
            <div style={{position:"absolute",bottom:0,left:0,right:0,height:5,background:"#00000055"}}>
              {(()=>{const pct=Math.min(100,hud.score/cfg.scoreGoal*100);const isClose=pct>=82;return(
                <div className="h-full transition-all duration-300 relative"
                  style={{width:`${pct}%`,
                    background:isClose?`linear-gradient(90deg,${wc}aa,#ffd700)`:
                      `linear-gradient(90deg,${wc}aa,${wc})`,
                    boxShadow:isClose?`0 0 16px #ffd700,0 0 6px #ffd700`:`0 0 12px ${wc},0 0 4px ${wc}`,
                    animation:isClose?"scorePulse 0.4s ease-in-out infinite alternate":"none"}}>
                  <div style={{position:"absolute",right:0,top:-2,width:8,height:9,borderRadius:"50%",background:isClose?"#ffd700":wc,boxShadow:`0 0 10px ${isClose?"#ffd700":wc}`}}/>
                </div>
              );})()}
              {/* SO CLOSE text */}
              {cfg&&hud.score/cfg.scoreGoal>=0.82&&hud.score<cfg.scoreGoal&&(
                <div className="absolute right-2 pointer-events-none" style={{bottom:6}}>
                  <span className="text-xs font-black" style={{color:"#ffd700",textShadow:"0 0 8px #ffd700",
                    animation:"floatGlow 0.5s ease-in-out infinite"}}>SO CLOSE! 🔥</span>
                </div>
              )}
            </div>
            {/* Heat bar (top 5px) — fills with combo */}
            <div style={{position:"absolute",top:0,left:0,right:0,height:5,background:"#00000033"}}>
              {(()=>{const heat=Math.min(100,(hud.streak/FEVER_STREAK)*100);const isHot=heat>=60;return(
                <div style={{width:`${heat}%`,height:"100%",transition:"width 0.15s ease",
                  background:isHot?
                    `linear-gradient(90deg,#ff6030,#ff9800,#ffd700)`:
                    `linear-gradient(90deg,${wc}66,${wc}aa)`,
                  boxShadow:isHot?`0 0 8px #ff9800`:`0 0 4px ${wc}88`}}>
                </div>
              );})()}
              {hud.streak>=3&&<div className="absolute right-1 top-0 flex items-center pointer-events-none" style={{height:5}}>
                <span style={{fontSize:8,color:"#ff9800",fontWeight:"black",lineHeight:1}}>🔥</span>
              </div>}
            </div>
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
            {/* Quick restart — 11A */}
            <NeonButton onClick={()=>{
              const lvId=levelCfgRef.current?.id;
              if(!lvId)return;
              if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}
              gsRef.current=null;targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];
              setActivePwrDisp([]);setFeverBorder(false);setPaused(false);pausedRef.current=false;
              setTimeout(()=>startGame(lvId,[]),50);
            }} className="w-48 py-3 mb-3" style={{background:`${wc}22`,border:`1px solid ${wc}66`,boxShadow:`0 0 12px ${wc}33`}}>
              🔄 RESTART
            </NeonButton>
            <NeonButton onClick={()=>{if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}gsRef.current=null;targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];setActivePwrDisp([]);setFeverBorder(false);setPaused(false);pausedRef.current=false;go("levelmap");}}
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
    const wld=WORLDS[cfg.world-1];
    const isBossLevel=cfg.isBoss;
    const totalAttempted=(sessionStats.tapsTotal||0)+(sessionStats.missedTargets||0);
    const accuracyPct=totalAttempted>0?Math.round((sessionStats.tapsTotal||0)/totalAttempted*100):100;
    const isSniper=accuracyPct>=95&&totalAttempted>=8;
    return(<>
      <div className="flex flex-col items-center h-full overflow-y-auto px-5 py-5 gap-3.5 relative z-10">
        {/* World-themed confetti explosion — 9E */}
        {(()=>{
          // Each world has themed confetti emojis
          const worldConfetti=[
            ["🌿","🍃","✨","💚","🌱"],["🔥","💥","⚡","🌋","🌟"],
            ["❄️","💙","🌊","💎","⛄"],["🌵","🏜️","💛","⭐","🪙"],
            ["🌸","🌺","💜","🌙","✨"],["⚙️","🔩","🤖","⚡","💎"],
            ["🌊","🐠","💙","🐚","✨"],["👻","💜","🕷️","🌟","💀"],
            ["🚀","⭐","🌌","💫","🪐"],["🌈","✨","💎","🌟","🎊"],
          ];
          const wEmoji=worldConfetti[(wld.id-1)%10];
          const count=isBossLevel?30:16;
          return(
            <div className="absolute inset-0 pointer-events-none overflow-hidden z-0">
              {Array.from({length:count},(_,i)=>(
                <div key={i} style={{
                  position:"absolute",
                  top:`${-5-Math.random()*10}%`,
                  left:`${(i*(100/count)+Math.random()*8)%100}%`,
                  fontSize:isBossLevel?`${14+Math.floor(Math.random()*10)}px`:`${12+Math.floor(Math.random()*8)}px`,
                  animation:`coinFall ${1.2+Math.random()*2.2}s ${i*0.09}s ease-in forwards`,
                  opacity:0.9,
                  transform:`rotate(${Math.floor(Math.random()*360)}deg)`,
                }}>
                  {wEmoji[i%wEmoji.length]}
                </div>
              ))}
            </div>
          );
        })()}
        {/* ── BIG DANCING MASCOT — victory celebration ── */}
        <div className="flex flex-col items-center gap-2" style={{animation:"victoryBurst 0.6s cubic-bezier(0.34,1.5,0.64,1)"}}>
          <MascotEmoji mood="victory" dancing={true} size={isBossLevel?118:96}/>
          <div className="font-black tracking-widest" style={{
            fontSize:"clamp(0.7rem,3.5vw,0.9rem)",
            color:currentMascot.color,
            textShadow:`0 0 18px ${currentMascot.color}`,
            animation:"floatGlow 1.2s ease-in-out infinite"}}>
            {isBossLevel?`🎊🎊 ${currentMascot.name.toUpperCase()} IS ABSOLUTELY HYPED! 🎊🎊`:`🎉 ${currentMascot.name.toUpperCase()} IS CHEERING FOR YOU! 🎉`}
          </div>
        </div>
        {/* Cinematic hero banner */}
        <div className="w-full rounded-3xl relative overflow-hidden" style={{
          background:`linear-gradient(160deg,${wld.color}22 0%,${wld.bg} 60%)`,
          border:`1px solid ${wld.color}55`,
          boxShadow:`0 0 40px ${wld.color}33,inset 0 0 30px ${wld.color}0a`,
          padding:"20px 20px 16px",animation:"victoryBurst 0.5s cubic-bezier(0.34,1.4,0.64,1)"}}>
          {/* World label */}
          <div className="flex items-center gap-2 mb-2">
            <span style={{fontSize:22}}>{wld.emoji}</span>
            <div>
              <div className="text-xs uppercase tracking-widest opacity-55 font-bold" style={{color:wld.color}}>{wld.name}</div>
              <div className="text-base font-black leading-tight" style={{color:wld.color}}>{cfg.name}</div>
            </div>
            <div className="ml-auto px-2 py-0.5 rounded-full text-xs font-black"
              style={{background:`${wld.color}22`,color:wld.color,border:`1px solid ${wld.color}44`,letterSpacing:"0.08em"}}>
              {isBossLevel?"👑 BOSS BEATEN!":"⭐ CLEARED!"}
            </div>
          </div>
          {/* Star row */}
          <div className="flex justify-center gap-3 my-2">
            {[1,2,3].map(s=>(
              <span key={s} style={{fontSize:s<=stars?46:30,opacity:s<=stars?1:0.12,
                filter:s<=stars?`drop-shadow(0 0 14px #fbbf24) drop-shadow(0 0 28px #fbbf2488)`:"none",
                animation:s<=stars?`starPop ${0.25+s*0.18}s cubic-bezier(0.34,1.5,0.64,1) both`:"none",
                animationDelay:`${(s-1)*0.12}s`}}>⭐</span>
            ))}
          </div>
          {newStars>stars&&<div className="text-center text-xs" style={{color:"#fbbf24",opacity:0.7}}>Personal best: {newStars}★</div>}
          {/* Score */}
          <div className="text-center mt-2">
            <div className="text-xs uppercase opacity-40 tracking-widest mb-0.5" style={{color:wld.color}}>Score</div>
            <div className="font-black tabular-nums" style={{fontSize:"clamp(2rem,10vw,3rem)",color:wld.color,
              textShadow:`0 0 30px ${wld.color}66`,lineHeight:1}}>{score.toLocaleString()}</div>
          </div>
        </div>

        {/* Rewards row */}
        <div className="flex gap-2.5 w-full">
          <div className="flex-1 rounded-2xl py-3 flex flex-col items-center gap-0.5"
            style={{background:`${wld.color}12`,border:`1px solid ${wld.color}33`,backdropFilter:"blur(8px)"}}>
            <div className="text-lg">✨</div>
            <div className="font-black text-sm" style={{
              color:wld.color,
              animation:payoutDone?"none":"heartbeat 0.35s ease-in-out infinite",
              textShadow:payoutDone?"none":`0 0 12px ${wld.color}`}}>+{displayedXP} XP</div>
          </div>
          {/* 11C — Coins earned with animated pop overlay */}
          <div className="flex-1 rounded-2xl py-3 flex flex-col items-center gap-0.5 relative overflow-visible"
            style={{background:"#fbbf2412",border:"1px solid #fbbf2433",backdropFilter:"blur(8px)"}}>
            <div className="text-lg">🪙</div>
            <div className="font-black text-sm" style={{
              color:"#fbbf24",
              animation:payoutDone?"none":"heartbeat 0.35s ease-in-out infinite",
              textShadow:payoutDone?"none":"0 0 14px #fbbf24"}}>+{displayedCoins}</div>
            {payoutDone&&coinsEarned>0&&(
              <div style={{position:"absolute",top:"-22px",left:"50%",transform:"translateX(-50%)",
                fontSize:11,fontWeight:"black",color:"#ffd700",whiteSpace:"nowrap",
                animation:"coinPop 1.2s ease-out forwards",pointerEvents:"none",
                textShadow:"0 0 8px #ffd700"}}>+🪙{coinsEarned}!</div>
            )}
          </div>
          <div className="flex-1 rounded-2xl py-3 flex flex-col items-center gap-0.5"
            style={{background:"#ffffff08",border:"1px solid #ffffff15",backdropFilter:"blur(8px)"}}>
            <div className="text-lg">⚡</div>
            <div className="font-black text-sm" style={{color:"#fff"}}>×{sv.bestStreak} best</div>
          </div>
        </div>

        {/* Stats grid */}
        <div className="w-full rounded-2xl py-3 px-4 grid grid-cols-3 gap-2"
          style={{background:"rgba(0,0,0,0.35)",border:`1px solid ${wld.color}1a`,backdropFilter:"blur(10px)"}}>
          {[["👆 Taps",sessionStats.tapsTotal],["✨ Magic+",sessionStats.rareHits],["🐉 Bosses",sessionStats.bossKills||0],
            ["🎯 Perfect",sessionStats.perfectTaps||0],["⚡ Magic Mode",sessionStats.feverCount||0],["⏱ Time",sessionStats.timeSurvived+"s"]
          ].map(([l,v])=>(
            <div key={l} className="text-center py-1">
              <div className="text-xs opacity-40 mb-0.5" style={{color:wld.color,letterSpacing:"0.02em"}}>{l}</div>
              <div className="font-black text-sm" style={{color:wld.color}}>{v}</div>
            </div>
          ))}
          {/* Accuracy rating */}
          <div className="col-span-3 flex items-center justify-center gap-2 py-2 rounded-xl mt-1"
            style={{background:isSniper?"#ffd70015":"#ffffff06",border:`1px solid ${isSniper?"#ffd70066":"#ffffff10"}`}}>
            <span style={{fontSize:16}}>{isSniper?"🎯":"📊"}</span>
            <div>
              <div style={{fontSize:10,color:isSniper?"#ffd700":"#ffffff55",fontWeight:"bold",letterSpacing:"0.06em"}}>
                {isSniper?"⭐ SNIPER ACCURACY!":"Accuracy"}
              </div>
              <div style={{fontSize:13,fontWeight:"black",color:isSniper?"#ffd700":wld.color}}>{accuracyPct}%</div>
            </div>
            <div style={{flex:1,height:4,background:"#ffffff10",borderRadius:2,overflow:"hidden",maxWidth:60}}>
              <div style={{width:`${accuracyPct}%`,height:"100%",background:isSniper?"#ffd700":wld.color,boxShadow:`0 0 4px ${wld.color}`}}/>
            </div>
          </div>
        </div>

        {/* Boss victory story */}
        {isBossLevel&&(()=>{const ws=WORLD_STORIES.find(s=>s.worldId===cfg.world);return ws?(
          <div className="w-full rounded-2xl px-4 py-4 text-center text-sm leading-relaxed"
            style={{background:`${wld.color}14`,border:`1px solid ${wld.color}44`,backdropFilter:"blur(8px)",color:"#f0f0d8",lineHeight:1.65}}>
            <div className="text-2xl mb-2">🎉</div>
            <div style={{color:wld.color,fontWeight:"bold",marginBottom:6}}>{wld.name} Conquered!</div>
            {ws.victory}
          </div>
        ):null;})()}

        {/* Teaser for next level / next world */}
        {!isLast&&(()=>{
          const nextId=levelId+1;
          const nextCfg=getLevelConfig(nextId);
          const nextWld=WORLDS[nextCfg.world-1];
          const isNewWorld=nextCfg.world!==cfg.world;
          const isNextBoss=nextCfg.isBoss;
          return(
            <div className="w-full rounded-2xl px-4 py-3 flex items-center gap-3"
              style={{background:`${nextWld.color}14`,border:`1px solid ${nextWld.color}40`,backdropFilter:"blur(8px)"}}>
              <span style={{fontSize:28,animation:isNewWorld?"floatGlow 1.5s ease-in-out infinite":"none"}}>
                {isNewWorld?nextWld.emoji:isNextBoss?"👑":"▶"}
              </span>
              <div className="flex-1 min-w-0">
                <div className="text-xs font-black" style={{color:nextWld.color}}>
                  {isNewWorld?`🌍 NEW WORLD: ${nextWld.name.toUpperCase()}!`:isNextBoss?"👑 BOSS BATTLE INCOMING!":"NEXT STAGE"}
                </div>
                <div className="text-xs opacity-55 truncate" style={{color:nextWld.color}}>
                  {isNewWorld?`Prepare for ${nextWld.name} — new enemies await!`:nextCfg.name}
                </div>
              </div>
              <span className="text-base" style={{color:nextWld.color,opacity:0.6}}>→</span>
            </div>
          );
        })()}
        {/* CTA buttons */}
        {!isLast&&(
          <NeonButton onClick={()=>{setMascotDancing(false);setMascotMood("idle");setSelectedLevel(levelId+1);setCartItems([]);go("shop");}}
            className="w-full py-4 text-lg font-black"
            style={{background:`linear-gradient(135deg,${wld.accent},${wld.color})`,
              boxShadow:`0 0 36px ${wld.color}55,0 4px 20px rgba(0,0,0,0.5)`,letterSpacing:"0.06em"}}>
            🚀 NEXT STAGE →
          </NeonButton>
        )}
        {isLast&&<div className="text-center font-black text-2xl py-2"
          style={{color:"#ffd700",textShadow:"0 0 40px #ffd700,0 0 80px #ffd70044",animation:"floatGlow 2s ease-in-out infinite"}}>
          🌈 YOU ARE THE QUEST MASTER! 🌈
        </div>}
        {/* PRESTIGE button — available after completing level 100 (max 5 times) */}
        {levelCompleteData?.canPrestige&&(
          <NeonButton onClick={()=>{
            if(window.confirm(`PRESTIGE! Reset levels 1-100 and earn +5% permanent score bonus? (Prestige ${(sv.prestigeLevel||0)+1}/5)`)){
              sv.prestigeLevel=(sv.prestigeLevel||0)+1;sv.unlockedLevel=1;
              unlock("prestige_1");
              flushSave();sfx("prestige");vibrate([30,15,30,15,60,15,100]);
              setPrestigeAnim(true);setTimeout(()=>setPrestigeAnim(false),2000);
              setNotif(`👑 PRESTIGE ${sv.prestigeLevel}! +${sv.prestigeLevel*5}% score bonus forever!`);
              setMascotDancing(false);setMascotMood("idle");go("levelmap");
            }
          }} className="w-full py-4 text-base font-black"
            style={{background:"linear-gradient(135deg,#ffd70033,#ffd70066)",border:"2px solid #ffd700",
              boxShadow:"0 0 40px #ffd70066",color:"#ffd700",letterSpacing:"0.07em"}}>
            👑 PRESTIGE! ({(sv.prestigeLevel||0)+1}/5) — +5% Score Forever
          </NeonButton>
        )}
        {/* Score sharing card — 9A */}
        <NeonButton onClick={()=>{
          const mascot=currentMascot;
          const starStr="⭐".repeat(stars)+"☆".repeat(3-stars);
          const accuracyStr=isSniper?` 🎯 ${accuracyPct}% Sniper!`:`📊 ${accuracyPct}% accuracy`;
          const streakStr=sessionStats.bestCombo>0?` | ⚡ ${sessionStats.bestCombo}× combo`:"";
          const txt=[
            `🎮 NexusTap Score Card`,
            `─────────────────────`,
            `${wld.emoji} ${cfg.name} (Level ${levelId})`,
            `🏆 Score: ${score.toLocaleString()} ${starStr}`,
            `${accuracyStr}${streakStr}`,
            `🐾 Mascot: ${mascot.emoji.idle} ${mascot.name}`,
            `─────────────────────`,
            `Can you beat me? 👇`,
          ].join("\n");
          if(navigator.share){navigator.share({title:"NexusTap",text:txt}).catch(()=>{});}
          else if(navigator.clipboard){navigator.clipboard.writeText(txt);setNotif("📋 Score card copied!");}
        }} className="w-full py-3 text-sm"
          style={{background:"rgba(255,255,255,0.06)",border:`1px solid ${wld.color}44`,backdropFilter:"blur(8px)"}}>
          📤 Share Score Card
        </NeonButton>
        <NeonButton onClick={()=>{setMascotDancing(false);setMascotMood("idle");setScrollToLevel(levelId);go("levelmap");}}
          className="w-full py-3 text-sm" style={{background:"rgba(255,255,255,0.06)",border:`1px solid ${wld.color}33`,backdropFilter:"blur(8px)"}}>
          ← Adventure Map
        </NeonButton>
      </div>
      {/* ── MASCOT UNLOCK OVERLAY ── */}
      {mascotUnlockedData&&(
        <div className="absolute inset-0 flex flex-col items-center justify-center z-50 px-6"
          style={{background:"rgba(0,0,0,0.88)",backdropFilter:"blur(12px)"}}>
          {/* Confetti sparkles */}
          <div className="absolute inset-0 pointer-events-none overflow-hidden">
            {[...Array(18)].map((_,i)=>(
              <div key={i} style={{
                position:"absolute",
                left:`${(i*37)%100}%`,
                top:`${(i*53)%80}%`,
                fontSize:14,
                animation:`sparkleFloat ${1.5+i*0.18}s ease-in-out ${i*0.12}s infinite`,
                opacity:0.7}}>
                {["✨","🌟","⭐","💫","🎊","🎉"][i%6]}
              </div>
            ))}
          </div>
          <div className="flex flex-col items-center gap-4 relative z-10"
            style={{animation:"victoryBurst 0.6s cubic-bezier(0.34,1.5,0.64,1)"}}>
            {/* Rarity banner */}
            {(()=>{
              const rs={starter:"#60a5fa",common:"#4ecb71",rare:"#6ec0f5",epic:"#b06de8",legendary:"#ffd700"}[mascotUnlockedData.rarity]||"#60a5fa";
              return(
                <div style={{
                  background:`linear-gradient(135deg,${rs}22,${rs}44)`,
                  border:`2px solid ${rs}`,borderRadius:14,
                  padding:"4px 18px",
                  fontSize:11,fontWeight:"black",color:rs,letterSpacing:"0.1em",
                  boxShadow:`0 0 24px ${rs}55`,
                  animation:`floatGlow 1s ease-in-out infinite`}}>
                  {({starter:"STARTER",common:"COMMON",rare:"RARE ✦",epic:"EPIC ✦✦",legendary:"LEGENDARY ✦✦✦"}[mascotUnlockedData.rarity]||"NEW")} MASCOT UNLOCKED!
                </div>
              );
            })()}
            <div style={{
              fontSize:11,color:"#ffffff88",fontWeight:"bold",letterSpacing:"0.06em"}}>
              🎉 NEW COMPANION! 🎉
            </div>
            {/* Big animated mascot */}
            <div style={{
              fontSize:100,lineHeight:1,
              filter:`drop-shadow(0 0 30px ${mascotUnlockedData.color}) drop-shadow(0 0 60px ${mascotUnlockedData.color}55)`,
              animation:`${mascotUnlockedData.dance} 0.7s ease-in-out infinite`}}>
              {mascotUnlockedData.e.victory}
            </div>
            <div style={{fontWeight:"black",fontSize:"1.8rem",color:mascotUnlockedData.color,
              textShadow:`0 0 30px ${mascotUnlockedData.color}`,letterSpacing:"0.06em"}}>
              {mascotUnlockedData.name}
            </div>
            <div style={{
              fontSize:13,color:"#ffffffaa",textAlign:"center",
              fontStyle:"italic",maxWidth:240,lineHeight:1.4}}>
              "{mascotUnlockedData.catchphrase}"
            </div>
            <div className="flex gap-3 w-full mt-2">
              <NeonButton
                onClick={()=>{saveRef.current.mascotId=mascotUnlockedData.id;debounceSave();setMascotUnlockedData(null);}}
                className="flex-1 py-3 font-black"
                style={{background:`linear-gradient(135deg,${mascotUnlockedData.color}33,${mascotUnlockedData.color}55)`,
                  border:`2px solid ${mascotUnlockedData.color}`,color:mascotUnlockedData.color,
                  boxShadow:`0 0 24px ${mascotUnlockedData.color}44`,fontSize:13}}>
                Choose {mascotUnlockedData.name}! 🌟
              </NeonButton>
              <NeonButton
                onClick={()=>setMascotUnlockedData(null)}
                className="flex-1 py-3 font-black text-sm"
                style={{background:"#ffffff10",color:"#fff"}}>
                Later
              </NeonButton>
            </div>
          </div>
        </div>
      )}
    </>);
  };

  // ── Game Over ──
  const renderGameOver=()=>{
    if(!gameOverData)return null;
    const{score,levelId,levelName,scoreGoal,sessionStats,nearMiss,shortfall}=gameOverData;
    const cfg=getLevelConfig(levelId);
    const pct=Math.min(100,Math.round(score/scoreGoal*100));
    return(
      <div className="flex flex-col items-center h-full overflow-y-auto px-5 py-6 gap-4 relative z-10">
        {/* Near-Miss special header */}
        {/* Sad mascot on game over */}
        <div className="flex flex-col items-center gap-2" style={{animation:"waveIn 0.5s ease-out"}}>
          <MascotEmoji mood="scared" size={88}/>
          <div className="font-bold text-center" style={{
            fontSize:"0.85rem",color:currentMascot.color,
            textShadow:`0 0 12px ${currentMascot.color}55`,maxWidth:200}}>
            {nearMiss
              ?"Nooo!! So close! I believe in you!! 💪"
              :"Awww! Let's try again together! 🌈"}
          </div>
        </div>
        {nearMiss?(
          <div className="w-full text-center rounded-3xl px-4 py-4" style={{
            background:`linear-gradient(160deg,#ff980014,rgba(0,0,0,0.3))`,
            border:"1px solid #ff980055",backdropFilter:"blur(10px)",animation:"waveIn 0.5s ease-out"}}>
            <div className="font-black text-xl mb-1" style={{color:"#ff9800",textShadow:"0 0 20px #ff980077"}}>SO CLOSE!</div>
            <div className="text-sm opacity-80" style={{color:"#ffc87a"}}>
              Only <span className="font-black" style={{color:"#ffd700"}}>{shortfall?.toLocaleString()}</span> more points needed!
            </div>
            <div className="text-xs opacity-50 mt-1" style={{color:"#ff9800"}}>You reached {pct}% of the goal 🎯</div>
          </div>
        ):(
          <div className="text-center">
            <div className="text-sm uppercase tracking-widest opacity-50 mb-1" style={{color:cfg.worldColor}}>{WORLDS[cfg.world-1].emoji} {WORLDS[cfg.world-1].name}</div>
            <div className="text-xs uppercase tracking-widest font-bold opacity-60 mb-1" style={{color:"#ef4444"}}>— Almost there! Try again! —</div>
            <div className="text-xl font-black" style={{color:cfg.worldColor}}>{levelName}</div>
          </div>
        )}
        {/* Score + progress */}
        <div className="w-full rounded-3xl p-4" style={{
          background:`linear-gradient(160deg,${cfg.worldColor}14 0%,rgba(0,0,0,0.4) 100%)`,
          border:`1px solid ${cfg.worldColor}44`,backdropFilter:"blur(10px)"}}>
          <div className="text-center mb-3">
            <div className="text-xs uppercase tracking-widest opacity-40 mb-1" style={{color:cfg.worldColor}}>Score</div>
            <div className="font-black tabular-nums" style={{fontSize:"clamp(1.8rem,9vw,2.8rem)",color:cfg.worldColor,
              textShadow:`0 0 24px ${cfg.worldColor}55`}}>{score.toLocaleString()}</div>
          </div>
          <div className="flex justify-between text-xs mb-1.5 opacity-55" style={{color:cfg.worldColor}}>
            <span>Quest progress</span><span>{pct}%</span>
          </div>
          <div className="h-3 rounded-full relative" style={{background:"#ffffff12"}}>
            <div className="h-full rounded-full transition-all" style={{width:`${pct}%`,
              background:nearMiss?`linear-gradient(90deg,${cfg.worldColor}88,#ff9800)`:
                `linear-gradient(90deg,${cfg.worldColor}88,${cfg.worldColor})`,
              boxShadow:nearMiss?`0 0 16px #ff980088`:`0 0 12px ${cfg.worldColor}88`}}/>
            {/* Near-miss gap indicator */}
            {nearMiss&&<div style={{position:"absolute",right:0,top:-2,height:18,width:2,background:"#ff9800",
              boxShadow:"0 0 8px #ff9800",borderRadius:2}}/>}
          </div>
          {nearMiss&&<div className="text-xs text-center mt-2 font-bold" style={{color:"#ff9800"}}>⬅ This close to winning!</div>}
        </div>
        <div className="w-full rounded-2xl p-3 grid grid-cols-3 gap-2"
          style={{background:"rgba(0,0,0,0.3)",border:`1px solid ${cfg.worldColor}1a`,backdropFilter:"blur(8px)"}}>
          {[["👆 Taps",sessionStats.tapsTotal],["✨ Magic+",sessionStats.rareHits],["🔥 Streak",sessionStats.bestCombo+"×"],
            ["🐉 Bosses",sessionStats.bossKills||0],["🎯 Perfect",sessionStats.perfectTaps||0],["⏱ Time",sessionStats.timeSurvived+"s"]
          ].map(([l,v])=>(
            <div key={l} className="text-center py-1">
              <div className="text-xs opacity-40 mb-0.5" style={{color:cfg.worldColor}}>{l}</div>
              <div className="font-black text-sm" style={{color:cfg.worldColor}}>{v}</div>
            </div>
          ))}
        </div>
        {/* ── RESCUE GAMBLE ── */}
        {nearMiss&&rescueSecondsLeft>0&&sv.coins>=50&&(
          <div className="w-full rounded-2xl overflow-hidden" style={{
            background:"linear-gradient(135deg,#7c2d12,#c2410c,#7c2d12)",
            border:"3px solid #ff6030",
            boxShadow:"0 0 40px #ff603055",
            animation:"rescuePulse 0.6s ease-in-out infinite alternate"}}>
            <div className="flex flex-col items-center gap-2 px-4 py-4">
              <div style={{fontSize:42,animation:"mascotShake 0.4s ease-in-out infinite"}}>
                {currentMascot.e.scared}
              </div>
              <div style={{color:"#ffd700",fontWeight:"black",fontSize:"1.3rem",letterSpacing:"0.05em",textShadow:"0 0 20px #ffd700"}}>
                🚨 LAST CHANCE!
              </div>
              <div style={{color:"#ffc87a",fontSize:"0.85rem",textAlign:"center"}}>
                Restart with <span style={{color:"#ffd700",fontWeight:"bold"}}>FULL LIVES + 400 BONUS</span>
              </div>
              <div style={{color:"#ff9800",fontWeight:"black",fontSize:"1.5rem",textShadow:"0 0 16px #ff9800"}}>
                {rescueSecondsLeft}s
              </div>
              <NeonButton
                onClick={()=>{
                  saveRef.current.coins-=50;flushSave();
                  setRescueSecondsLeft(0);rescuedRef.current=true;
                  startGame(levelId,[]);
                }}
                className="w-full py-4 text-xl font-black"
                style={{background:"linear-gradient(135deg,#fbbf24,#f59e0b)",color:"#000",
                  boxShadow:"0 0 30px #fbbf2488",letterSpacing:"0.08em"}}>
                RESCUE ME! (50🪙)
              </NeonButton>
              <div style={{color:"#ff9800",fontSize:"0.75rem",opacity:0.7}}>
                You have {sv.coins}🪙
              </div>
            </div>
          </div>
        )}
        <NeonButton onClick={()=>{setRescueSecondsLeft(0);setSelectedLevel(levelId);setCartItems([]);go("shop");}}
          className="w-full py-4 text-lg font-black"
          style={{background:nearMiss?`linear-gradient(135deg,#b45309,#ff9800)`:
            `linear-gradient(135deg,${cfg.worldColor}99,${cfg.worldColor})`,
            boxShadow:nearMiss?`0 0 36px #ff980066,0 4px 20px rgba(0,0,0,0.5)`:
              `0 0 32px ${cfg.worldColor}55,0 4px 20px rgba(0,0,0,0.5)`,
            letterSpacing:"0.06em",fontSize:nearMiss?"1.2rem":"1rem"}}>
          {nearMiss?"🔥 SO CLOSE — TRY AGAIN!":"🌟 TRY AGAIN!"}
        </NeonButton>
        <NeonButton onClick={()=>go("levelmap")} className="w-full py-3 text-sm"
          style={{background:"rgba(255,255,255,0.06)",border:`1px solid ${cfg.worldColor}33`,backdropFilter:"blur(8px)"}}>
          ← Adventure Map
        </NeonButton>
      </div>
    );
  };

  // ── Missions ──
  const renderMissions=()=>{
    const missions=getDailyMissions(),prog=sv.missionProgress||{};
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
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

  // ── Skill Tree ──
  const renderSkillTree=()=>{
    const skills=sv.skills||{};
    const pts=sv.skillPoints||0;
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
            <h2 className="text-xl font-black" style={{color:theme.accent}}>Skill Tree</h2>
          </div>
          <div className="px-3 py-1.5 rounded-xl font-black text-sm" style={{background:`${theme.accent}22`,border:`1px solid ${theme.accent}66`,color:theme.accent}}>
            ✨ {pts} pt{pts!==1?"s":""}
          </div>
        </div>
        <p className="text-xs opacity-40 -mt-2">Earn skill points by leveling up. Permanent bonuses for all future runs.</p>
        <div className="flex flex-col gap-3">
          {SKILL_TREE.map(skill=>{
            const lvl=skills[skill.id]||0;
            const maxed=lvl>=3;
            const cost=maxed?0:skill.cost[lvl];
            const canAfford=pts>=cost&&!maxed;
            return(
              <div key={skill.id} className="rounded-2xl p-4" style={{background:"#ffffff07",border:`1px solid ${maxed?"#ffd70066":theme.accent+"22"}`}}>
                <div className="flex items-center justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <span style={{fontSize:22}}>{skill.icon}</span>
                    <div>
                      <div className="font-black text-sm" style={{color:maxed?"#ffd700":theme.accent}}>{skill.name}{maxed?" ★ MAX":""}</div>
                      <div style={{fontSize:10,color:"#ffffff44"}}>{skill.desc}</div>
                    </div>
                  </div>
                  {!maxed&&(
                    <NeonButton
                      onClick={()=>{
                        if(!canAfford)return;
                        sv.skills={...skills,[skill.id]:lvl+1};
                        sv.skillPoints=pts-cost;
                        flushSave();
                        setNotif(`${skill.icon} ${skill.name} → Lv ${lvl+1}!`);
                      }}
                      className="px-4 py-2 text-xs font-black"
                      disabled={!canAfford}
                      style={{
                        background:canAfford?`${theme.accent}25`:"#ffffff08",
                        border:`1px solid ${canAfford?theme.accent+"88":"#ffffff15"}`,
                        color:canAfford?theme.accent:"#666",
                        opacity:canAfford?1:0.5,
                      }}>
                      ✨{cost} → Lv{lvl+1}
                    </NeonButton>
                  )}
                </div>
                {/* Level pips */}
                <div className="flex gap-1.5 mb-1.5">
                  {[0,1,2].map(i=>(
                    <div key={i} className="h-2 flex-1 rounded-full" style={{
                      background:i<lvl?theme.accent:(i===lvl&&!maxed?"#ffffff18":"#ffffff0a"),
                      boxShadow:i<lvl?`0 0 6px ${theme.accent}88`:"none",
                    }}/>
                  ))}
                </div>
                {/* Current effect label */}
                <div style={{fontSize:11,color:lvl>0?theme.accent:"#ffffff33"}}>
                  {lvl>0?`Active: ${skill.levels[lvl-1]}`:`Inactive — upgrade to unlock`}
                  {!maxed&&<span style={{color:"#ffffff33",marginLeft:6}}>Next: {skill.levels[lvl]}</span>}
                </div>
              </div>
            );
          })}
        </div>
        <div className="text-center text-xs opacity-30 pb-4">Skill points earned by leveling up (every {XP_PER_LVL} XP)</div>
      </div>
    );
  };

  // ── Achievements ──
  // Achievement tab state — "all" | "gameplay" | "progression" | "social"
  const [achTab, setAchTab] = React.useState("all");
  const ACH_CATS = {
    gameplay:    ["first_tap","combo_10","boss_1","fever_1","perfect_5","combo_15","chain_4","mimic_hit","shielded_hit"],
    progression: ["level_10","level_50","level_100","prestige_1","three_stars_5","mascot_lv10"],
    social:      ["missions_all","daily_7","score_2000"],
  };
  const renderAchievements=()=>{
    const filtered=achTab==="all"?ACHIEVEMENTS:ACHIEVEMENTS.filter(a=>ACH_CATS[achTab]?.includes(a.id));
    const unlockedCount=sv.unlockedAchievements.length;
    return(
    <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{color:theme.accent}}>Medals</h2>
        <span className="text-xs opacity-40" style={{color:theme.accent}}>{unlockedCount}/{ACHIEVEMENTS.length}</span>
      </div>
      {/* Tab bar */}
      <div className="flex gap-1.5 rounded-xl p-1" style={{background:"rgba(0,0,0,0.3)"}}>
        {[["all","All"],["gameplay","🎮"],["progression","📈"],["social","🤝"]].map(([t,label])=>(
          <button key={t} onClick={()=>setAchTab(t)}
            className="flex-1 py-1.5 rounded-lg text-xs font-black transition-all"
            style={{background:achTab===t?theme.accent+"33":"transparent",color:achTab===t?theme.accent:"#ffffff55",
              border:achTab===t?`1px solid ${theme.accent}66`:"1px solid transparent"}}>
            {label}
          </button>
        ))}
      </div>
      {/* Overall XP from achievements */}
      {achTab==="all"&&(
        <div className="rounded-xl px-3 py-2 flex items-center gap-2" style={{background:`${theme.accent}12`,border:`1px solid ${theme.accent}33`}}>
          <span style={{fontSize:18}}>⚡</span>
          <div className="text-xs" style={{color:theme.accent}}>
            Total achievement XP: <span className="font-black">{ACHIEVEMENTS.filter(a=>sv.unlockedAchievements.includes(a.id)).reduce((s,a)=>s+(a.xp||0),0)}</span>
          </div>
          <div className="ml-auto text-xs font-black" style={{color:theme.accent}}>{Math.round(unlockedCount/ACHIEVEMENTS.length*100)}%</div>
        </div>
      )}
      <div className="grid grid-cols-2 gap-3">
        {filtered.map(a=>{
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
  };

  // ── Leaderboard ──
  const renderLeaderboard=()=>{
    const todayKey=getTodayKey(),weekKey=getWeekKey();
    // Normalise scores — entries may be numbers (legacy) or {score,date,week}
    const normScores=(sv.scores||[]).map(e=>typeof e==="number"?{score:e,date:"2000-0-0",week:"2000-W0"}:e);
    const todayScores=normScores.filter(e=>e.date===todayKey).sort((a,b)=>b.score-a.score).slice(0,10);
    const weekScores=normScores.filter(e=>e.week===weekKey).sort((a,b)=>b.score-a.score).slice(0,10);
    const allScores=normScores.sort((a,b)=>b.score-a.score).slice(0,10);
    const activeScores=lbTab==="today"?todayScores:lbTab==="week"?weekScores:allScores;
    const infAll=[...(sv.infinityScores||[])].sort((a,b)=>b-a).slice(0,5);
    const hasInfinity=(sv.unlockedLevel||1)>100||(sv.infinityScores||[]).length>0;
    // Compute world-by-world star progress
    const worldStars=WORLDS.map(w=>{
      const lvls=Array.from({length:10},(_,i)=>w.id===10?91+i:(w.id-1)*10+i+1);
      const stars=lvls.reduce((s,l)=>s+(sv.levelStars?.[l]||0),0);
      return{world:w,stars,max:30,pct:Math.round((stars/30)*100)};
    });
    const totalStars=worldStars.reduce((s,w)=>s+w.stars,0);
    const achPct=Math.round(((sv.unlockedAchievements||[]).length/ACHIEVEMENTS.length)*100);
    return(
      <div className="flex flex-col h-full px-4 py-5 gap-4 overflow-y-auto relative z-10">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <h2 className="text-xl font-black" style={{color:theme.accent}}>Best Scores</h2>
          {(()=>{const pt=PRESTIGE_TIERS[Math.min(5,sv.prestigeLevel||0)];return pt?.badge?(
            <span style={{fontSize:12,color:pt.color,background:`${pt.color}18`,border:`1px solid ${pt.color}66`,borderRadius:8,padding:"2px 10px",fontWeight:"black",
              textShadow:`0 0 10px ${pt.color}88`,boxShadow:`0 0 8px ${pt.color}33`}}>
              {pt.badge} {pt.title} Ⅰ×{sv.prestigeLevel}
            </span>
          ):null;})()}
        </div>
        {/* ── PERSONAL STATS SUMMARY ── */}
        <div className="grid grid-cols-2 gap-2">
          <div className="p-3 rounded-2xl" style={{background:`${theme.accent}10`,border:`1px solid ${theme.accent}33`}}>
            <div className="text-xs opacity-50 uppercase tracking-widest" style={{color:theme.accent}}>High Score</div>
            <div className="text-xl font-black tabular-nums" style={{color:theme.accent}}>{(sv.highScore||0).toLocaleString()}</div>
          </div>
          <div className="p-3 rounded-2xl" style={{background:"#fbbf2410",border:"1px solid #fbbf2433"}}>
            <div className="text-xs opacity-50 uppercase tracking-widest" style={{color:"#fbbf24"}}>Best Streak</div>
            <div className="text-xl font-black tabular-nums" style={{color:"#fbbf24"}}>{sv.bestStreak||0}×</div>
          </div>
          <div className="p-3 rounded-2xl" style={{background:"#34d39910",border:"1px solid #34d39933"}}>
            <div className="text-xs opacity-50 uppercase tracking-widest" style={{color:"#34d399"}}>Total Coins</div>
            <div className="text-xl font-black tabular-nums" style={{color:"#34d399"}}>🪙 {(sv.totalCoins||0).toLocaleString()}</div>
          </div>
          <div className="p-3 rounded-2xl" style={{background:"#a78bfa10",border:"1px solid #a78bfa33"}}>
            <div className="text-xs opacity-50 uppercase tracking-widest" style={{color:"#a78bfa"}}>Stars Total</div>
            <div className="text-xl font-black tabular-nums" style={{color:"#a78bfa"}}>⭐ {totalStars}<span className="text-xs opacity-50">/300</span></div>
          </div>
        </div>
        {/* ── PRESTIGE COSMETICS PANEL — 12A ── */}
        {(sv.prestigeLevel||0)>0&&(()=>{
          const pt=PRESTIGE_TIERS[Math.min(5,sv.prestigeLevel||0)];
          const next=sv.prestigeLevel<5?PRESTIGE_TIERS[sv.prestigeLevel+1]:null;
          return(
            <div className="rounded-2xl p-4" style={{background:`linear-gradient(135deg,${pt.color}15 0%,#0a0218 80%)`,border:`1px solid ${pt.color}55`,boxShadow:`0 0 24px ${pt.color}22`}}>
              <div className="flex items-center gap-3 mb-2">
                <span style={{fontSize:28,filter:`drop-shadow(0 0 8px ${pt.color})`}}>{pt.badge}</span>
                <div>
                  <div className="font-black" style={{color:pt.color,letterSpacing:"0.06em",fontSize:13}}>{pt.title}</div>
                  <div className="text-xs opacity-60" style={{color:pt.color}}>{pt.desc}</div>
                </div>
              </div>
              {/* Prestige progress pips */}
              <div className="flex gap-2 mt-2">
                {PRESTIGE_TIERS.slice(1).map(t=>(
                  <div key={t.level} className="flex-1 h-2 rounded-full overflow-hidden" style={{background:"#ffffff10"}}>
                    <div style={{width:(sv.prestigeLevel||0)>=t.level?"100%":"0%",height:"100%",background:t.color,transition:"width 0.6s",boxShadow:`0 0 4px ${t.color}`}}/>
                  </div>
                ))}
              </div>
              {next&&<div className="text-xs mt-2 opacity-50" style={{color:pt.color}}>Next: {next.badge} {next.title} (Prestige {next.level})</div>}
              {!next&&<div className="text-xs mt-2 text-center font-black" style={{color:"#ffd700",textShadow:"0 0 10px #ffd700",animation:"floatGlow 2s ease-in-out infinite"}}>🌟 MAXIMUM PRESTIGE ACHIEVED 🌟</div>}
            </div>
          );
        })()}
        {/* ── WORLD PROGRESS RIBBON ── */}
        <div className="rounded-2xl p-3" style={{background:"#ffffff05",border:"1px solid #ffffff10"}}>
          <div className="text-xs font-bold opacity-50 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>World Progress</div>
          <div className="space-y-1.5">
            {worldStars.map(w=>(
              <div key={w.world.id} className="flex items-center gap-2">
                <span style={{fontSize:16,minWidth:22}}>{w.world.emoji}</span>
                <div className="flex-1">
                  <div className="flex justify-between items-baseline">
                    <span style={{fontSize:10,color:w.world.color,fontWeight:"bold",letterSpacing:"0.04em"}}>{w.world.name}</span>
                    <span style={{fontSize:9,color:w.world.color,opacity:0.7}}>{w.stars}/30 ⭐</span>
                  </div>
                  <div style={{height:4,background:"#ffffff10",borderRadius:2,overflow:"hidden",marginTop:1}}>
                    <div style={{width:`${w.pct}%`,height:"100%",background:w.world.color,boxShadow:`0 0 4px ${w.world.color}`,transition:"width 0.5s"}}/>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        {/* ── WORLD RECORDS HALL — 12B ── */}
        {Object.keys(sv.worldBest||{}).length>0&&(
          <div className="rounded-2xl p-3" style={{background:"#ffffff05",border:"1px solid #ffffff10"}}>
            <div className="text-xs font-bold opacity-50 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>🌍 World Records</div>
            <div className="grid grid-cols-2 gap-1.5">
              {WORLDS.map(w=>{
                const best=(sv.worldBest||{})[w.id];
                if(!best)return null;
                return(
                  <div key={w.id} className="flex items-center gap-1.5 rounded-xl px-2 py-1.5"
                    style={{background:`${w.color}0e`,border:`1px solid ${w.color}33`}}>
                    <span style={{fontSize:14}}>{w.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <div style={{fontSize:9,color:w.color,opacity:0.7,letterSpacing:"0.04em",fontWeight:"bold"}}>{w.name}</div>
                      <div style={{fontSize:12,color:w.color,fontWeight:"black",tabularNums:true}}>{best.toLocaleString()}</div>
                    </div>
                  </div>
                );
              }).filter(Boolean)}
            </div>
          </div>
        )}
        {/* ── TIME-TABBED SCORES ── */}
        <div>
          {/* Tab row */}
          <div className="flex gap-1 mb-3 rounded-2xl p-1" style={{background:"#ffffff08"}}>
            {[["today","Today","📅"],["week","This Week","📆"],["all","All Time","🏆"]].map(([key,label,icon])=>(
              <button key={key} onClick={()=>setLbTab(key)}
                className="flex-1 text-xs font-bold py-2 rounded-xl transition-all"
                style={{
                  background:lbTab===key?`${theme.accent}28`:"transparent",
                  border:`1px solid ${lbTab===key?theme.accent+"88":"transparent"}`,
                  color:lbTab===key?theme.accent:"#888",
                  outline:"none",letterSpacing:"0.03em",
                }}>
                {icon} {label}
              </button>
            ))}
          </div>
          {/* Score list for active tab */}
          {activeScores.length===0
            ?<p className="text-center opacity-40 text-sm py-4" style={{color:theme.accent}}>
                {lbTab==="today"?"No runs today yet!":lbTab==="week"?"No runs this week yet!":"No scores yet!"}
              </p>
            :activeScores.map((e,i)=>(
              <div key={i} className="flex items-center justify-between px-4 py-3 mb-1.5 rounded-2xl"
                style={{background:i===0?`${theme.accent}18`:"#ffffff05",border:`1px solid ${i<3?theme.accent+"44":"#ffffff0d"}`}}>
                <span className="font-black text-xl" style={{color:i===0?"#fbbf24":i===1?"#d1d5db":i===2?"#d97706":theme.accent,minWidth:32}}>
                  {i===0?"🥇":i===1?"🥈":i===2?"🥉":`#${i+1}`}
                </span>
                <span className="font-bold text-xl tabular-nums" style={{color:theme.accent}}>{(e.score||e).toLocaleString()}</span>
                {lbTab!=="all"&&<span style={{fontSize:9,color:"#ffffff33"}}>{e.date||""}</span>}
              </div>
            ))
          }
        </div>
        {hasInfinity&&<>
          <div className="text-xs font-bold opacity-40 uppercase tracking-widest mt-2" style={{color:"#a78bfa"}}>∞ Infinity Mode</div>
          {infAll.length===0
            ?<p className="text-center opacity-40 text-sm" style={{color:"#a78bfa"}}>No infinity runs yet</p>
            :infAll.map((s,i)=>(
              <div key={i} className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{background:i===0?"#a78bfa18":"#ffffff05",border:`1px solid ${i===0?"#a78bfa44":"#ffffff0d"}`}}>
                <span className="font-black" style={{color:"#a78bfa",minWidth:32}}>{i===0?"∞🥇":`∞#${i+1}`}</span>
                <span className="font-bold tabular-nums" style={{color:"#a78bfa"}}>{s.toLocaleString()}</span>
              </div>
            ))
          }
        </>}
        {/* ── COMPLETION CARDS ── */}
        <div className="grid grid-cols-2 gap-2 mt-2">
          <div className="p-3 rounded-2xl text-center" style={{background:"#ffffff06",border:`1px solid ${theme.accent}22`}}>
            <div className="text-xs opacity-40 mb-1" style={{color:theme.accent}}>Levels Unlocked</div>
            <div className="text-2xl font-black" style={{color:theme.accent}}>{Math.min(100,sv.unlockedLevel||1)}<span className="text-sm opacity-50">/100</span></div>
          </div>
          <div className="p-3 rounded-2xl text-center" style={{background:"#ffffff06",border:"1px solid #fbbf2422"}}>
            <div className="text-xs opacity-40 mb-1" style={{color:"#fbbf24"}}>Achievements</div>
            <div className="text-2xl font-black" style={{color:"#fbbf24"}}>{(sv.unlockedAchievements||[]).length}<span className="text-sm opacity-50">/{ACHIEVEMENTS.length}</span></div>
            <div className="text-xs opacity-50 mt-0.5" style={{color:"#fbbf24"}}>{achPct}% complete</div>
          </div>
        </div>
      </div>
    );
  };

  // ── Mascot Collection ──
  const renderMascotCollection=()=>{
    const sv2=saveRef.current;
    const unlocked=sv2.unlockedMascots||["dragon","fox"];
    const RARITY_STYLE={
      starter:{border:"#60a5fa",bg:"#60a5fa",label:"STARTER"},
      common: {border:"#4ecb71",bg:"#4ecb71",label:"COMMON"},
      rare:   {border:"#6ec0f5",bg:"#6ec0f5",label:"RARE"},
      epic:   {border:"#b06de8",bg:"#b06de8",label:"EPIC"},
      legendary:{border:"#ffd700",bg:"#ffd700",label:"LEGENDARY"},
    };
    return(
      <div className="flex flex-col h-full bg-transparent relative z-10">
        {/* Header */}
        <div className="flex items-center gap-3 px-4 pt-5 pb-3" style={{flexShrink:0}}>
          <NeonButton onClick={()=>go("settings")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <div>
            <h2 className="text-xl font-black" style={{color:theme.accent}}>🐾 Mascot Collection</h2>
            <p className="text-xs opacity-50" style={{color:"#fff"}}>{unlocked.length} / {MASCOTS.length} unlocked</p>
          </div>
        </div>
        {/* Grid */}
        <div className="overflow-y-auto flex-1 px-3 pb-6" style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:12,alignContent:"start"}}>
          {MASCOTS.map(m=>{
            const isUnlocked=unlocked.includes(m.id);
            const isActive=sv2.mascotId===m.id;
            const rs=RARITY_STYLE[m.rarity]||RARITY_STYLE.common;
            const newlyUnlocked=isUnlocked&&!isActive;
            return(
              <button key={m.id} disabled={!isUnlocked}
                onClick={()=>{if(isUnlocked){sv2.mascotId=m.id;debounceSave();go("mascotcollection");}}}
                style={{
                  position:"relative",display:"flex",flexDirection:"column",alignItems:"center",
                  gap:6,padding:"18px 10px 14px",borderRadius:20,
                  border:`2px solid ${isActive?rs.border:isUnlocked?"#ffffff22":"#ffffff10"}`,
                  background:isActive?`${rs.bg}18`:isUnlocked?"#ffffff08":"#00000040",
                  boxShadow:isActive?`0 0 24px ${rs.border}55`:"none",
                  cursor:isUnlocked?"pointer":"default",
                  WebkitTapHighlightColor:"transparent",transition:"all 0.18s",
                  opacity:isUnlocked?1:0.55}}>
                {/* Rarity top stripe */}
                <div style={{
                  position:"absolute",top:0,left:0,right:0,height:4,
                  borderRadius:"18px 18px 0 0",
                  background:isUnlocked?`linear-gradient(90deg,${rs.border},${rs.border}88,${rs.border})`:"#333"}}/>
                {/* Rarity badge */}
                <div style={{
                  position:"absolute",top:8,right:8,
                  background:isUnlocked?rs.bg:"#555",
                  color:isUnlocked?"#000":"#888",
                  fontSize:7,fontWeight:"black",padding:"2px 6px",borderRadius:6,
                  letterSpacing:"0.06em"}}>
                  {rs.label}
                </div>
                {/* ACTIVE badge */}
                {isActive&&(
                  <div style={{
                    position:"absolute",top:8,left:8,
                    background:"#ffd700",color:"#000",
                    fontSize:7,fontWeight:"black",padding:"2px 6px",borderRadius:6,
                    letterSpacing:"0.04em",boxShadow:"0 0 8px #ffd70066"}}>
                    ✓ ACTIVE
                  </div>
                )}
                {/* Mascot emoji */}
                <div style={{position:"relative",marginTop:8}}>
                  {isUnlocked?(
                    <span style={{
                      fontSize:52,lineHeight:1,display:"block",
                      filter:`drop-shadow(0 0 ${isActive?16:6}px ${rs.border})`,
                      animation:isActive?`${m.dance} 0.9s ease-in-out infinite`:"mascotIdle 2.8s ease-in-out infinite"}}>
                      {m.e.idle}
                    </span>
                  ):(
                    <div style={{
                      width:52,height:52,borderRadius:"50%",background:"#222",
                      display:"flex",alignItems:"center",justifyContent:"center",
                      border:"2px solid #ffffff15",fontSize:26}}>
                      🔒
                    </div>
                  )}
                </div>
                {/* Name */}
                <div style={{
                  fontWeight:"black",fontSize:13,letterSpacing:"0.04em",
                  color:isActive?rs.border:isUnlocked?"#fff":"#555"}}>
                  {m.name}
                </div>
                {/* Catchphrase or unlock hint */}
                <div style={{
                  fontSize:9,textAlign:"center",lineHeight:1.35,
                  color:isUnlocked?"#ffffff66":"#ffffff33",maxWidth:110}}>
                  {isUnlocked?m.catchphrase:`🔒 ${m.unlockHint||"Coming soon"}`}
                </div>
                {/* Mascot XP bar */}
                {isUnlocked&&(()=>{
                  const mxp=(sv2.mascotXP||{})[m.id]||0;
                  const mlvl=Math.min(20,Math.floor(mxp/500));
                  const pct=mlvl>=20?100:((mxp%500)/500)*100;
                  return(
                    <div style={{width:"100%",marginTop:2}}>
                      <div style={{display:"flex",justifyContent:"space-between",fontSize:8,opacity:0.6,marginBottom:2,color:rs.border}}>
                        <span>LV {mlvl}</span><span>{mlvl>=20?"MAX":Math.floor(pct)+"%"}</span>
                      </div>
                      <div style={{width:"100%",height:4,borderRadius:2,background:"#ffffff18"}}>
                        <div style={{width:`${pct}%`,height:"100%",borderRadius:2,background:rs.border,boxShadow:`0 0 4px ${rs.border}`}}/>
                      </div>
                      {mlvl>=5&&<div style={{fontSize:7,marginTop:2,color:rs.border,opacity:0.8}}>
                        {[mlvl>=5?"💰+5%coin":null,mlvl>=10?"🛡️shield":null,mlvl>=15?"⭐+100pts":null,mlvl>=20?"👑legendary":null].filter(Boolean).join(" ")}
                      </div>}
                    </div>
                  );
                })()}
                {/* SELECT button for unlocked-but-not-active */}
                {isUnlocked&&!isActive&&(
                  <div style={{
                    marginTop:4,padding:"4px 14px",borderRadius:10,
                    background:`${rs.bg}22`,border:`1px solid ${rs.border}66`,
                    fontSize:10,fontWeight:"bold",color:rs.border,letterSpacing:"0.05em"}}>
                    SELECT
                  </div>
                )}
              </button>
            );
          })}
        </div>
        {/* ── Accessory shop for active mascot ── */}
        {(()=>{
          const activeId=sv2.mascotId||"dragon";
          const activeM=MASCOTS.find(m=>m.id===activeId)||MASCOTS[0];
          const owned=sv2.ownedAccessories||{};
          const equipped=(sv2.mascotAccessories||{})[activeId];
          return(
            <div style={{padding:"12px 16px 24px",borderTop:"1px solid #ffffff15",flexShrink:0}}>
              <div className="flex items-center justify-between mb-3">
                <div>
                  <div className="text-sm font-black" style={{color:activeM.color,letterSpacing:"0.05em"}}>
                    🎩 {activeM.name}'s Accessories
                  </div>
                  <div className="text-xs opacity-50" style={{color:"#fff"}}>Coins: 🪙 {sv2.coins||0}</div>
                </div>
                {equipped&&(
                  <button onClick={()=>{
                    const ma={...(sv2.mascotAccessories||{})};delete ma[activeId];sv2.mascotAccessories=ma;
                    flushSave();setNotif("Accessory removed");setTimeout(()=>setNotif(null),1500);
                  }} className="text-xs px-3 py-1 rounded-lg font-bold"
                    style={{background:"#ffffff10",color:"#ffffff90",border:"1px solid #ffffff20"}}>
                    Remove
                  </button>
                )}
              </div>
              <div style={{display:"grid",gridTemplateColumns:"repeat(3,1fr)",gap:8}}>
                {MASCOT_ACCESSORIES.map(a=>{
                  const ownKey=`${activeId}:${a.id}`;
                  const isOwned=!!owned[ownKey];
                  const isEquipped=equipped===a.id;
                  const canBuy=(sv2.coins||0)>=a.cost;
                  return(
                    <button key={a.id} onClick={()=>{
                      if(isOwned){
                        // toggle equip
                        sv2.mascotAccessories={...(sv2.mascotAccessories||{}),[activeId]:isEquipped?null:a.id};
                        if(isEquipped){delete sv2.mascotAccessories[activeId];}
                        flushSave();sfx("tap");
                      }else if(canBuy){
                        sv2.coins-=a.cost;
                        sv2.ownedAccessories={...(sv2.ownedAccessories||{}),[ownKey]:true};
                        sv2.mascotAccessories={...(sv2.mascotAccessories||{}),[activeId]:a.id};
                        flushSave();sfx("coin");vibrate([20]);
                        setNotif(`✨ ${a.name} equipped!`);setTimeout(()=>setNotif(null),1800);
                      }
                    }} disabled={!isOwned&&!canBuy}
                      style={{
                        position:"relative",padding:"10px 4px 8px",borderRadius:14,
                        border:`2px solid ${isEquipped?"#ffd700":isOwned?activeM.color+"66":canBuy?"#ffffff22":"#ffffff08"}`,
                        background:isEquipped?"#ffd70015":isOwned?activeM.color+"10":canBuy?"#ffffff05":"#00000040",
                        cursor:(isOwned||canBuy)?"pointer":"not-allowed",
                        opacity:(!isOwned&&!canBuy)?0.5:1,
                        boxShadow:isEquipped?`0 0 12px #ffd70055`:"none",
                        WebkitTapHighlightColor:"transparent"
                      }}>
                      {isEquipped&&<div style={{position:"absolute",top:4,right:4,fontSize:9,padding:"1px 5px",background:"#ffd700",color:"#000",borderRadius:5,fontWeight:"black"}}>ON</div>}
                      <div style={{fontSize:30,lineHeight:1,marginBottom:4}}>{a.emoji}</div>
                      <div style={{fontSize:10,fontWeight:"bold",color:"#fff",lineHeight:1.1}}>{a.name}</div>
                      <div style={{fontSize:9,marginTop:3,color:isOwned?"#34d399":canBuy?"#fbbf24":"#ffffff40",fontWeight:"bold"}}>
                        {isOwned?(isEquipped?"✓ Equipped":"Tap to wear"):`🪙 ${a.cost}`}
                      </div>
                    </button>
                  );
                })}
              </div>
            </div>
          );
        })()}
      </div>
    );
  };

  // ── Settings ──
  const renderSettings=()=>{
    const SPEED_MODES=[{v:0.7,label:"Easy 🐢",desc:"Slower, longer"},{v:1.0,label:"Normal ⚖️",desc:"Standard"},{v:1.3,label:"Hard ⚡",desc:"Faster, shorter"},{v:1.6,label:"Expert 🔥",desc:"Maximum speed"}];
    return(
    <div className="flex flex-col h-full px-4 py-5 gap-5 overflow-y-auto relative z-10">
      <div className="flex items-center gap-3">
        <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <h2 className="text-xl font-black" style={{color:theme.accent}}>Settings</h2>
      </div>
      {/* Sound on/off */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Sound</p>
        <NeonButton onClick={()=>{const n=!soundOn;setSoundOn(n);sv.soundEnabled=n;debounceSave();}}
          className="px-6 py-3"
          style={{background:soundOn?`${theme.accent}22`:"#ffffff0a",border:`1px solid ${soundOn?theme.accent:"#ffffff22"}`,color:soundOn?theme.accent:"#888"}}>
          {soundOn?"🔊  Sound ON":"🔇  Sound OFF"}
        </NeonButton>
      </div>
      {/* Volume sliders */}
      {soundOn&&<div>
        <p className="text-xs font-bold opacity-40 mb-3 uppercase tracking-widest" style={{color:theme.accent}}>Volume</p>
        <div className="flex flex-col gap-3">
          <div className="flex items-center gap-3">
            <span className="text-xs w-14" style={{color:theme.accent}}>🎵 Music</span>
            <input type="range" min={0} max={100} value={sv.musicVol??80}
              onChange={e=>{const v=parseInt(e.target.value);sv.musicVol=v;debounceSave();bgMusicCtl?.setVol?.(v*0.00032);}}
              style={{flex:1,accentColor:theme.accent}}/>
            <span className="text-xs w-8 text-right opacity-50" style={{color:theme.accent}}>{sv.musicVol??80}</span>
          </div>
          <div className="flex items-center gap-3">
            <span className="text-xs w-14" style={{color:theme.accent}}>🔔 SFX</span>
            <input type="range" min={0} max={100} value={sv.sfxVol??80}
              onChange={e=>{const v=parseInt(e.target.value);sv.sfxVol=v;debounceSave();}}
              style={{flex:1,accentColor:theme.accent}}/>
            <span className="text-xs w-8 text-right opacity-50" style={{color:theme.accent}}>{sv.sfxVol??80}</span>
          </div>
        </div>
      </div>}
      {/* Haptic toggle */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Haptic Feedback</p>
        <NeonButton onClick={()=>{const n=sv.hapticEnabled===false;sv.hapticEnabled=n;_hapticOn=n;debounceSave();}}
          className="px-6 py-3"
          style={{background:(sv.hapticEnabled!==false)?`${theme.accent}22`:"#ffffff0a",
            border:`1px solid ${(sv.hapticEnabled!==false)?theme.accent:"#ffffff22"}`,
            color:(sv.hapticEnabled!==false)?theme.accent:"#888"}}>
          {(sv.hapticEnabled!==false)?"📳  Vibration ON":"📴  Vibration OFF"}
        </NeonButton>
      </div>
      {/* Colorblind mode */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Accessibility</p>
        <NeonButton onClick={()=>{const n=!sv.colorblindMode;sv.colorblindMode=n;_colorblindOn=n;debounceSave();}}
          className="px-6 py-3"
          style={{background:sv.colorblindMode?`${theme.accent}22`:"#ffffff0a",
            border:`1px solid ${sv.colorblindMode?theme.accent:"#ffffff22"}`,
            color:sv.colorblindMode?theme.accent:"#888"}}>
          {sv.colorblindMode?"♛  Colorblind Symbols ON":"♛  Colorblind Symbols OFF"}
        </NeonButton>
      </div>
      {/* Adaptive difficulty */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Adaptive Difficulty</p>
        <NeonButton onClick={()=>{sv.adaptiveDifficulty=!sv.adaptiveDifficulty;debounceSave();}}
          className="px-6 py-3"
          style={{background:sv.adaptiveDifficulty?`${theme.accent}22`:"#ffffff0a",
            border:`1px solid ${sv.adaptiveDifficulty?theme.accent:"#ffffff22"}`,
            color:sv.adaptiveDifficulty?theme.accent:"#888"}}>
          {sv.adaptiveDifficulty?"🎯  Auto-Adjust ON  — speed adapts to your skill":"🎯  Auto-Adjust OFF — fixed speed mode"}
        </NeonButton>
      </div>
      {/* Speed mode */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:theme.accent}}>Game Speed</p>
        <div className="flex flex-col gap-2">
          {SPEED_MODES.map(sm=>(
            <NeonButton key={sm.v} onClick={()=>{sv.speedMode=sm.v;debounceSave();}}
              className="flex items-center justify-between px-4 py-3 rounded-2xl"
              style={{background:(sv.speedMode||1)===sm.v?`${theme.accent}20`:"#ffffff06",
                border:`1px solid ${(sv.speedMode||1)===sm.v?theme.accent:"#ffffff10"}`}}>
              <div className="flex flex-col items-start">
                <span style={{color:(sv.speedMode||1)===sm.v?theme.accent:"#aaa",fontWeight:"bold"}}>{sm.label}</span>
                <span style={{fontSize:10,color:"#ffffff44"}}>{sm.desc}</span>
              </div>
              {(sv.speedMode||1)===sm.v&&<span style={{color:theme.accent}}>✓</span>}
            </NeonButton>
          ))}
        </div>
      </div>
      <div>
        <div className="flex justify-between items-baseline mb-2">
          <p className="text-xs font-bold opacity-40 uppercase tracking-widest" style={{color:theme.accent}}>Theme</p>
          <p className="text-xs opacity-50" style={{color:theme.accent}}>Your Level: <span style={{color:"#fff",fontWeight:"bold"}}>Lv {lvl}</span></p>
        </div>
        <div className="flex flex-col gap-2">
          {THEMES.map(th=>{
            const locked=lvl<th.unlockLevel;
            const levelsAway=th.unlockLevel-lvl;
            return(
              <NeonButton key={th.id} disabled={locked}
                onClick={()=>{setTheme(th);sv.themeId=th.id;debounceSave();}}
                className="flex items-center justify-between px-4 py-3 rounded-2xl"
                style={{background:theme.id===th.id?`${th.accent}20`:"#ffffff06",border:`1px solid ${theme.id===th.id?th.accent:"#ffffff10"}`,opacity:locked?0.55:1}}>
                <div className="flex items-center gap-3 flex-1 min-w-0">
                  <div className="w-4 h-4 rounded-full flex-shrink-0" style={{background:locked?"#444":th.accent,boxShadow:locked?"none":`0 0 8px ${th.accent}`}}/>
                  <div className="flex-1 min-w-0">
                    <div style={{color:locked?"#666":th.accent,fontWeight:"bold"}}>{th.name}</div>
                    {locked&&(
                      <div className="text-xs opacity-60 mt-0.5" style={{color:"#fff"}}>
                        Unlocks at Lv {th.unlockLevel} {levelsAway>0?`· ${levelsAway} to go`:""}
                      </div>
                    )}
                  </div>
                </div>
                {locked?(
                  <span className="text-xs flex items-center gap-1" style={{color:"#888"}}>
                    🔒 Lv{th.unlockLevel}
                  </span>
                ):theme.id===th.id?<span style={{color:th.accent,fontSize:18}}>✓</span>:<span className="text-xs opacity-40" style={{color:th.accent}}>tap to use</span>}
              </NeonButton>
            );
          })}
        </div>
      </div>
      {/* ── Mascot Chooser ── */}
      <div>
        <p className="text-xs font-bold opacity-40 mb-3 uppercase tracking-widest" style={{color:theme.accent}}>Your Companion</p>
        {/* Active mascot preview */}
        <NeonButton onClick={()=>go("mascotcollection")}
          className="w-full flex items-center gap-4 px-4 py-3 rounded-2xl"
          style={{background:`${currentMascot.color}12`,border:`2px solid ${currentMascot.color}44`,
            boxShadow:`0 0 20px ${currentMascot.color}22`}}>
          <span style={{fontSize:46,lineHeight:1,
            filter:`drop-shadow(0 0 12px ${currentMascot.color})`,
            animation:`${currentMascot.dance} 0.9s ease-in-out infinite`}}>
            {currentMascot.e.idle}
          </span>
          <div className="flex flex-col items-start flex-1">
            <span className="font-black text-base" style={{color:currentMascot.color}}>{currentMascot.name}</span>
            <span className="text-xs opacity-60" style={{color:"#fff"}}>
              {({starter:"Starter",common:"Common",rare:"Rare ✦",epic:"Epic ✦✦",legendary:"Legendary ✦✦✦"}[currentMascot.rarity]||"")}
            </span>
            <span className="text-xs mt-1" style={{color:"#ffffff55",fontStyle:"italic"}}>"{currentMascot.catchphrase}"</span>
          </div>
          <div style={{color:`${currentMascot.color}88`,fontSize:12,fontWeight:"bold"}}>
            {(sv.unlockedMascots||["dragon","fox"]).length}/{MASCOTS.length} collected →
          </div>
        </NeonButton>
      </div>
      <div className="border-t border-white border-opacity-10 pt-4">
        <NeonButton onClick={()=>{if(window.confirm("Reset ALL progress? Cannot be undone.")){saveRef.current={...DEFAULT_SAVE};flushSave();setTheme(THEMES[0]);setSoundOn(true);go("menu");}}}
          className="w-full py-3 text-sm" style={{background:"#ef444418",border:"1px solid #ef444455",color:"#ef4444"}}>
          Reset All Progress
        </NeonButton>
      </div>
    </div>
  );};

  // ── Infinity Mode Screen ──
  const renderInfinity=()=>{
    const infBest=sv.infinityBest||0;
    const infRound=infinityRound;
    const cfg=getInfinityLevelConfig(infRound);
    return(
      <div className="flex flex-col h-full px-5 py-6 gap-5 relative z-10 items-center justify-center">
        <NeonButton onClick={()=>go("menu")} className="absolute top-4 left-4 px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <div className="text-center">
          <div className="text-5xl mb-2" style={{animation:"floatGlow 2s ease-in-out infinite",filter:"drop-shadow(0 0 20px #a78bfa)"}}>∞</div>
          <h2 className="font-black text-3xl" style={{color:"#a78bfa",textShadow:"0 0 30px #a78bfaaa",fontFamily:"'Rajdhani',sans-serif",letterSpacing:"0.1em"}}>INFINITY MODE</h2>
          <p className="text-sm opacity-60 mt-1" style={{color:"#a78bfa"}}>No end. No mercy. Pure reflex.</p>
        </div>
        {infBest>0&&(
          <div className="px-6 py-3 rounded-2xl text-center" style={{background:"#a78bfa18",border:"1px solid #a78bfa44"}}>
            <div className="text-xs opacity-50 mb-1" style={{color:"#a78bfa"}}>Personal Best</div>
            <div className="text-2xl font-black" style={{color:"#a78bfa"}}>{infBest.toLocaleString()}</div>
          </div>
        )}
        <div className="w-full rounded-2xl p-4" style={{background:"#ffffff08",border:"1px solid #a78bfa33"}}>
          <div className="text-xs opacity-40 mb-2 uppercase tracking-widest" style={{color:"#a78bfa"}}>Starting Round</div>
          <div className="flex gap-2 justify-center">
            {[1,5,10,20].map(r=>(
              <NeonButton key={r} onClick={()=>setInfinityRound(r)}
                className="flex-1 py-3 text-sm font-black"
                style={{background:infRound===r?"#a78bfa33":"#ffffff08",border:`1px solid ${infRound===r?"#a78bfa":"#ffffff15"}`,color:infRound===r?"#a78bfa":"#888"}}>
                R{r}
              </NeonButton>
            ))}
          </div>
          <div className="text-xs text-center mt-2 opacity-40" style={{color:"#a78bfa"}}>Goal: {cfg.scoreGoal.toLocaleString()} pts · {cfg.lives} lives</div>
        </div>
        <NeonButton onClick={()=>{
          const infCfg=getInfinityLevelConfig(infRound);
          startGame(0,[],infCfg);
        }} className="w-full py-5 text-xl font-black"
          style={{background:"linear-gradient(135deg,#6d28d9,#a78bfa)",boxShadow:"0 0 40px #a78bfa66",letterSpacing:"0.1em"}}>
          ∞ DIVE IN — Round {infRound}
        </NeonButton>
        <p className="text-xs text-center opacity-30" style={{color:"#a78bfa"}}>2× coin rewards · Levels cycle through all 10 worlds</p>
      </div>
    );
  };

  // ── Zen Mode Screen ──
  const renderZen=()=>{

    const zenBest=sv.zenBest||0;
    const worldCfg=getZenConfig(zenWorld);
    return(
      <div className="flex flex-col h-full px-5 py-6 gap-5 relative z-10 items-center justify-center">
        <NeonButton onClick={()=>go("menu")} className="absolute top-4 left-4 px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <div className="text-center">
          <div className="text-5xl mb-2" style={{animation:"floatGlow 2.5s ease-in-out infinite",filter:"drop-shadow(0 0 20px #34d399)"}}>☯</div>
          <h2 className="font-black text-3xl" style={{color:"#34d399",textShadow:"0 0 30px #34d399aa",fontFamily:"'Rajdhani',sans-serif",letterSpacing:"0.1em"}}>ZEN MODE</h2>
          <p className="text-sm opacity-60 mt-1" style={{color:"#34d399"}}>90 seconds. No bombs. Pure flow.</p>
        </div>
        {zenBest>0&&(
          <div className="px-6 py-3 rounded-2xl text-center" style={{background:"#34d39918",border:"1px solid #34d39944"}}>
            <div className="text-xs opacity-50 mb-1" style={{color:"#34d399"}}>Personal Best</div>
            <div className="text-2xl font-black" style={{color:"#34d399"}}>{zenBest.toLocaleString()}</div>
            <div className="text-xs opacity-40" style={{color:"#34d399"}}>World {sv.zenBestWorld}: {WORLDS[(sv.zenBestWorld||1)-1].name}</div>
          </div>
        )}
        {/* World selector */}
        <div className="w-full rounded-2xl p-3" style={{background:"#ffffff08",border:"1px solid #34d39933"}}>
          <div className="text-xs opacity-40 mb-2 uppercase tracking-widest text-center" style={{color:"#34d399"}}>Choose World</div>
          <div className="grid grid-cols-5 gap-1.5">
            {WORLDS.map(w=>(
              <NeonButton key={w.id} onClick={()=>setZenWorld(w.id)}
                className="py-2 text-center text-lg rounded-xl"
                style={{background:zenWorld===w.id?`${w.color}33`:"#ffffff06",
                  border:`1px solid ${zenWorld===w.id?w.color:"#ffffff10"}`,
                  boxShadow:zenWorld===w.id?`0 0 8px ${w.color}66`:"none"}}>
                {w.emoji}
              </NeonButton>
            ))}
          </div>
          <div className="text-center mt-2 text-xs font-bold" style={{color:WORLDS[zenWorld-1].color}}>{WORLDS[zenWorld-1].name}</div>
        </div>
        <NeonButton onClick={()=>startGame(0,[],worldCfg)}
          className="w-full py-5 text-xl font-black"
          style={{background:"linear-gradient(135deg,#059669,#34d399)",boxShadow:"0 0 40px #34d39966",letterSpacing:"0.1em"}}>
          ☯ BEGIN ZEN
        </NeonButton>
        <p className="text-xs text-center opacity-30" style={{color:"#34d399"}}>Unlimited lives · No bombs · 90 second countdown</p>
      </div>
    );
  };

  // ── Weekly Challenge Screen ──
  const renderWeekly=()=>{
    const wk=getWeekKey();
    const wkLvl=getWeeklyChallengeLevel();
    const cfg=getLevelConfig(wkLvl);
    const wld=WORLDS[cfg.world-1];
    const isThisWeek=sv.weeklyChallengeDate===wk;
    const completed=isThisWeek&&sv.weeklyChallengeCompleted;
    const best=isThisWeek?(sv.weeklyChallengeBest||0):0;
    return(
      <div className="flex flex-col h-full px-5 py-6 gap-5 relative z-10 items-center justify-center">
        <NeonButton onClick={()=>go("menu")} className="absolute top-4 left-4 px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <div className="text-center">
          <div className="text-5xl mb-2" style={{animation:"floatGlow 2s ease-in-out infinite",filter:"drop-shadow(0 0 20px #a78bfa)"}}>🗓️</div>
          <h2 className="font-black text-3xl" style={{color:"#a78bfa",textShadow:"0 0 30px #a78bfaaa",letterSpacing:"0.08em"}}>WEEKLY CHALLENGE</h2>
          <p className="text-sm opacity-60 mt-1" style={{color:"#a78bfa"}}>Resets every Monday · 3× coin reward</p>
        </div>
        <div className="w-full rounded-2xl p-5" style={{background:`linear-gradient(160deg,${wld.color}22 0%,${wld.bg} 60%)`,border:`1px solid ${wld.color}55`,boxShadow:`0 0 30px ${wld.color}33`}}>
          <div className="flex items-center gap-3 mb-3">
            <span style={{fontSize:36}}>{wld.emoji}</span>
            <div>
              <div className="text-xs uppercase tracking-widest opacity-55 font-bold" style={{color:wld.color}}>{wld.name}</div>
              <div className="text-lg font-black" style={{color:wld.color}}>Level {wkLvl}: {cfg.name}</div>
            </div>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <div className="p-2 rounded-lg" style={{background:"#ffffff08"}}>
              <div className="opacity-50" style={{color:wld.color}}>Goal</div>
              <div className="font-bold" style={{color:"#fff"}}>{cfg.scoreGoal.toLocaleString()} pts</div>
            </div>
            <div className="p-2 rounded-lg" style={{background:"#ffffff08"}}>
              <div className="opacity-50" style={{color:wld.color}}>Lives</div>
              <div className="font-bold" style={{color:"#fff"}}>{cfg.lives}</div>
            </div>
          </div>
          {best>0&&(
            <div className="mt-3 p-2 rounded-lg text-center" style={{background:"#a78bfa18",border:"1px solid #a78bfa44"}}>
              <div className="text-xs opacity-60" style={{color:"#a78bfa"}}>Your best this week</div>
              <div className="text-xl font-black" style={{color:"#a78bfa"}}>{best.toLocaleString()}</div>
            </div>
          )}
        </div>
        <div className="w-full rounded-xl p-3 text-center" style={{background:"#fbbf2418",border:"1px solid #fbbf2444"}}>
          <div className="text-xs opacity-70" style={{color:"#fbbf24"}}>🏆 Reward for clearing</div>
          <div className="font-black text-base" style={{color:"#fbbf24"}}>+500 🪙 · +200 XP · Unique badge</div>
        </div>
        <NeonButton onClick={()=>{
          if(completed)return;
          setSelectedLevel(wkLvl);
          sv.weeklyChallengeDate=wk;
          if(!isThisWeek){sv.weeklyChallengeBest=0;sv.weeklyChallengeCompleted=false;}
          flushSave();
          go("shop");
        }} disabled={completed}
          className="w-full py-5 text-xl font-black"
          style={{background:completed?"#ffffff10":"linear-gradient(135deg,#6d28d9,#a78bfa)",
            boxShadow:completed?"none":"0 0 40px #a78bfa66",
            color:completed?"#ffffff40":"#fff",letterSpacing:"0.06em",
            opacity:completed?0.5:1}}>
          {completed?"✓ Done! See you Monday":"🗓️ BEGIN WEEKLY CHALLENGE"}
        </NeonButton>
      </div>
    );
  };

  // ── Daily Tournament Screen ──
  const renderTournament=()=>{
    const today=getTodayKey();
    const dailyLvl=getDailyChallengeLevel();
    const cfg=getLevelConfig(dailyLvl);
    const wld=WORLDS[cfg.world-1];
    const isToday=sv.tournamentDate===today;
    const todayBest=isToday?(sv.tournamentBest||0):0;
    // Estimate rank from score — heuristic: higher score = better rank
    // Rough mapping: score / scoreGoal ratio → percentile
    const ratio=todayBest/(cfg.scoreGoal||1);
    const estRank=todayBest===0?"—":ratio>=3?"Top 5%":ratio>=2.2?"Top 15%":ratio>=1.5?"Top 35%":ratio>=1?"Top 60%":"Bottom 40%";
    const history=(sv.tournamentHistory||[]).slice(0,7);
    return(
      <div className="flex flex-col h-full px-5 py-6 gap-4 relative z-10 overflow-y-auto">
        <NeonButton onClick={()=>go("menu")} className="absolute top-4 left-4 px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <div className="text-center pt-8">
          <div className="text-5xl mb-2" style={{animation:"floatGlow 2s ease-in-out infinite",filter:"drop-shadow(0 0 20px #fbbf24)"}}>🏆</div>
          <h2 className="font-black text-3xl" style={{color:"#fbbf24",textShadow:"0 0 30px #fbbf24aa",letterSpacing:"0.08em"}}>DAILY TOURNAMENT</h2>
          <p className="text-sm opacity-60 mt-1" style={{color:"#fbbf24"}}>Same level for all players today · 2× coin reward</p>
        </div>
        <div className="w-full rounded-2xl p-5" style={{background:`linear-gradient(160deg,${wld.color}22 0%,${wld.bg} 60%)`,border:`1px solid ${wld.color}55`,boxShadow:`0 0 30px ${wld.color}33`}}>
          <div className="flex items-center gap-3 mb-3">
            <span style={{fontSize:36}}>{wld.emoji}</span>
            <div>
              <div className="text-xs uppercase tracking-widest opacity-55 font-bold" style={{color:wld.color}}>{wld.name}</div>
              <div className="text-lg font-black" style={{color:wld.color}}>Level {dailyLvl}: {cfg.name}</div>
            </div>
          </div>
          {todayBest>0?(
            <div className="mt-3 grid grid-cols-2 gap-2 text-center">
              <div className="p-2 rounded-lg" style={{background:"#fbbf2418",border:"1px solid #fbbf2444"}}>
                <div className="text-xs opacity-60" style={{color:"#fbbf24"}}>Today's Best</div>
                <div className="text-xl font-black" style={{color:"#fbbf24"}}>{todayBest.toLocaleString()}</div>
              </div>
              <div className="p-2 rounded-lg" style={{background:"#a78bfa18",border:"1px solid #a78bfa44"}}>
                <div className="text-xs opacity-60" style={{color:"#a78bfa"}}>Estimated Rank</div>
                <div className="text-xl font-black" style={{color:"#a78bfa"}}>{estRank}</div>
              </div>
            </div>
          ):(
            <div className="text-sm text-center opacity-50 mt-2" style={{color:"#fff"}}>No attempt yet — go for the high score!</div>
          )}
        </div>
        {/* 7-day history */}
        {history.length>0&&(
          <div className="w-full rounded-xl p-3" style={{background:"#ffffff05",border:"1px solid #ffffff10"}}>
            <div className="text-xs uppercase tracking-widest opacity-50 mb-2" style={{color:"#fbbf24"}}>Last 7 Tournaments</div>
            <div className="space-y-1">
              {history.map((h,i)=>(
                <div key={i} className="flex justify-between text-xs" style={{color:"#ffffff80"}}>
                  <span>{h.date}</span>
                  <span style={{color:"#fbbf24",fontWeight:"bold"}}>{h.score.toLocaleString()} · {h.rank}</span>
                </div>
              ))}
            </div>
          </div>
        )}
        <NeonButton onClick={()=>{setSelectedLevel(dailyLvl);go("shop");}}
          className="w-full py-5 text-xl font-black"
          style={{background:"linear-gradient(135deg,#b45309,#fbbf24)",
            boxShadow:"0 0 40px #fbbf2466",letterSpacing:"0.06em"}}>
          🏆 ENTER TOURNAMENT
        </NeonButton>
        <p className="text-xs text-center opacity-30" style={{color:"#fbbf24"}}>Coins from this run are doubled</p>
      </div>
    );
  };

  // ── Daily Boss Gauntlet Screen ──
  const renderGauntlet=()=>{
    const alreadyDone=sv.gauntletDate===getTodayKey();
    const bossWorlds=WORLDS.slice(0,10);
    return(
      <div className="flex flex-col h-full px-5 py-5 gap-4 relative z-10 overflow-y-auto">
        <div className="flex items-center gap-3">
          <NeonButton onClick={()=>go("menu")} className="px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
          <div>
            <h2 className="text-xl font-black" style={{color:"#ff6b35"}}>⚔️ Daily Gauntlet</h2>
            <p className="text-xs opacity-50" style={{color:"#ff6b35"}}>Defeat all 10 world bosses in a row!</p>
          </div>
        </div>
        {alreadyDone&&(
          <div className="rounded-2xl px-4 py-3 text-center" style={{background:"#ff6b3518",border:"1px solid #ff6b3544"}}>
            <div style={{color:"#ff6b35",fontWeight:"bold",fontSize:14}}>✓ Completed today!</div>
            <div className="text-xs opacity-60 mt-1" style={{color:"#ff6b35"}}>Come back tomorrow for another run.</div>
            {(sv.gauntletBest||0)>0&&<div className="text-xs mt-1" style={{color:"#ff6b35"}}>Record: {sv.gauntletBest} bosses defeated</div>}
          </div>
        )}
        <div className="rounded-2xl p-4" style={{background:"#ffffff08",border:"1px solid #ff6b3533"}}>
          <div className="text-xs opacity-40 mb-3 uppercase tracking-widest" style={{color:"#ff6b35"}}>Boss Lineup</div>
          <div className="grid grid-cols-5 gap-2">
            {bossWorlds.map((w,i)=>(
              <div key={w.id} className="flex flex-col items-center gap-1 p-2 rounded-xl"
                style={{background:`${w.color}15`,border:`1px solid ${w.color}33`}}>
                <span style={{fontSize:22}}>{w.emoji}</span>
                <span style={{fontSize:8,color:w.color,opacity:0.8,textAlign:"center",lineHeight:1.2}}>{w.name.split(" ")[0]}</span>
              </div>
            ))}
          </div>
        </div>
        <div className="rounded-2xl px-4 py-3" style={{background:"#ffd70018",border:"1px solid #ffd70044"}}>
          <div className="text-sm font-bold" style={{color:"#ffd700"}}>🏆 Reward: 500🪙 + Boss Slayer achievement</div>
          <div className="text-xs opacity-60 mt-1" style={{color:"#ffd700"}}>5 lives total — no recharge between bosses</div>
        </div>
        <NeonButton onClick={()=>{
          if(alreadyDone)return;
          // Start gauntlet as a special boss-only level (world 1 boss first)
          setGauntletState({bossIndex:0,lives:5,score:0});
          const gauntletCfg={
            id:"gauntlet0",world:1,worldName:WORLDS[0].name,worldColor:WORLDS[0].color,
            worldBg:WORLDS[0].bg,worldGrid:WORLDS[0].grid,
            name:"Gauntlet: "+WORLDS[0].name,scoreGoal:1,lives:5,spawnInterval:2000,
            targetLifetime:30000,bombRate:0,movingRate:0,ghostRate:0,
            bossEnabled:true,bossRate:1.0,modifier:null,rarityBonus:0,
            isBoss:true,isLast:false,isGauntlet:true,gauntletBossIndex:0,
          };
          startGame(10,[],gauntletCfg); // level 10 cfg as base but override with gauntletCfg
        }} disabled={alreadyDone}
          className="w-full py-5 text-xl font-black"
          style={{background:alreadyDone?"#ffffff08":"linear-gradient(135deg,#b45309,#ff6b35)",
            boxShadow:alreadyDone?"none":"0 0 36px #ff6b3555",
            color:alreadyDone?"#ffffff30":"#fff",letterSpacing:"0.06em",opacity:alreadyDone?0.5:1}}>
          {alreadyDone?"⚔️ See you tomorrow!":"⚔️ BEGIN GAUNTLET!"}
        </NeonButton>
      </div>
    );
  };

  // ═════════════════════════════════════════════════════════════
  // MAIN RENDER
  // ═════════════════════════════════════════════════════════════
  const activeWorldColor = levelCfgRef.current ? WORLDS[levelCfgRef.current.world-1].color : theme.accent;
  return(
    <div className="relative w-full h-screen overflow-hidden select-none"
      style={{background:theme.bg,fontFamily:"'Exo 2','Rajdhani','Segoe UI',system-ui,sans-serif",
        transform:screenShake?`translate(${(Math.random()>0.5?1:-1)*5}px,${(Math.random()>0.5?1:-1)*3}px)`:"none",
        transition:screenShake?"none":"transform 0.04s ease"}}>

      <style>{`
        @keyframes feverPulse{0%{box-shadow:inset 0 0 40px #fbbf2430,0 0 40px #fbbf2430}100%{box-shadow:inset 0 0 80px #fbbf2455,0 0 80px #fbbf2455}}
        @keyframes epicFlash{0%{opacity:1}100%{opacity:0}}
        @keyframes legendaryRainbow{0%{opacity:1;filter:hue-rotate(0deg) brightness(1.6)}40%{opacity:0.9;filter:hue-rotate(180deg) brightness(1.4)}100%{opacity:0;filter:hue-rotate(360deg) brightness(1)}}
        @keyframes comboAnnounce{0%{transform:scale(.4) translateY(20px);opacity:0}55%{transform:scale(1.18) translateY(-4px)}75%{transform:scale(0.96)}100%{transform:scale(1) translateY(0);opacity:1}}
        @keyframes countAnim{0%{transform:scale(2.2);opacity:0}40%{transform:scale(0.95);opacity:1}80%{transform:scale(1);opacity:1}100%{transform:scale(.75);opacity:0}}
        @keyframes levelPulse{0%,100%{box-shadow:0 0 14px var(--wc,#a78bfa),0 0 0 2px var(--wc,#a78bfa)33}50%{box-shadow:0 0 34px var(--wc,#a78bfa),0 0 0 4px var(--wc,#a78bfa)55}}
        @keyframes starPop{0%{transform:scale(0) rotate(-40deg);opacity:0}60%{transform:scale(1.4) rotate(10deg)}85%{transform:scale(0.92)}100%{transform:scale(1) rotate(0);opacity:1}}
        @keyframes waveIn{0%{transform:scale(.55) translateY(-28px);opacity:0}65%{transform:scale(1.06)}85%{transform:scale(0.97)}100%{transform:scale(1);opacity:1}}
        @keyframes shimmer{0%{background-position:200% center}100%{background-position:-200% center}}
        @keyframes floatGlow{0%,100%{transform:translateY(0);filter:brightness(1)}50%{transform:translateY(-4px);filter:brightness(1.15)}}
        @keyframes bannerSlide{0%{transform:translateX(-20px);opacity:0}100%{transform:translateX(0);opacity:1}}
        @keyframes victoryBurst{0%{transform:scale(0.5);opacity:0}60%{transform:scale(1.08)}100%{transform:scale(1);opacity:1}}
        @keyframes coinFall{0%{transform:translateY(0) rotate(0deg);opacity:0.9}100%{transform:translateY(110vh) rotate(720deg);opacity:0}}
        @keyframes scorePulse{0%{box-shadow:0 0 12px #ffd700,0 0 4px #ffd700}100%{box-shadow:0 0 24px #ffd700,0 0 10px #ffd700}}
        @keyframes heartbeat{0%,100%{transform:scale(1)}15%{transform:scale(1.18)}30%{transform:scale(1)}45%{transform:scale(1.1)}60%{transform:scale(1)}}
        @keyframes perfectPop{0%{transform:scale(0.6) rotate(-8deg);opacity:0}50%{transform:scale(1.15) rotate(3deg)}100%{transform:scale(1) rotate(0);opacity:1}}
        @keyframes notifSlide{0%{transform:translateX(-50%) translateY(-24px);opacity:0}15%{transform:translateX(-50%) translateY(0);opacity:1}80%{transform:translateX(-50%) translateY(0);opacity:1}100%{transform:translateX(-50%) translateY(-12px);opacity:0}}
        @keyframes sparkleFloat{0%{transform:translateY(0) rotate(0deg);opacity:0.7}50%{transform:translateY(-18px) rotate(180deg);opacity:1}100%{transform:translateY(0) rotate(360deg);opacity:0.7}}
        @keyframes mascotIdle{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-7px) scale(1.05)}}
        @keyframes mascotBounce{0%{transform:scale(1) translateY(0)}30%{transform:scale(0.85,1.2) translateY(0)}60%{transform:scale(1.15,0.88) translateY(-22px)}85%{transform:scale(0.95,1.06) translateY(0)}100%{transform:scale(1) translateY(0)}}
        @keyframes mascotSad{0%,100%{transform:rotate(0) translateY(0)}25%{transform:rotate(-8deg) translateY(4px)}75%{transform:rotate(8deg) translateY(4px)}}
        @keyframes mascotShake{0%,100%{transform:translateX(0)}20%{transform:translateX(-6px)}40%{transform:translateX(6px)}60%{transform:translateX(-4px)}80%{transform:translateX(4px)}}
        @keyframes slotSpin{0%{transform:translateY(-8px)}50%{transform:translateY(8px)}100%{transform:translateY(-8px)}}
        @keyframes speechBubble{0%{transform:scale(0.5) translateY(8px);opacity:0}60%{transform:scale(1.06) translateY(-2px)}100%{transform:scale(1) translateY(0);opacity:1}}
        @keyframes rescuePulse{0%{box-shadow:0 0 30px #ff603044}100%{box-shadow:0 0 60px #ff6030aa,0 0 100px #ff603033}}
        @keyframes danceDragon{0%,100%{transform:scale(1) rotate(-8deg)}25%{transform:scale(1.25) rotate(14deg) translateY(-10px)}50%{transform:scale(1.1) rotate(-6deg) translateY(-5px)}75%{transform:scale(1.2) rotate(10deg) translateY(-8px)}}
        @keyframes danceFox{0%{transform:rotate(0) scale(1)}30%{transform:rotate(-180deg) scale(1.2) translateY(-8px)}60%{transform:rotate(-360deg) scale(1)}80%{transform:rotate(-360deg) scale(1.15) translateY(-6px)}100%{transform:rotate(-360deg) scale(1)}}
        @keyframes danceCat{0%,100%{transform:translateY(0) rotate(-10deg)}33%{transform:translateY(-20px) rotate(12deg)}66%{transform:translateY(-10px) rotate(-5deg)}}
        @keyframes danceFrog{0%,100%{transform:scaleY(1) scaleX(1) translateY(0)}30%{transform:scaleX(0.85) scaleY(1.15) translateY(-24px)}55%{transform:scaleX(0.9) scaleY(1.1) translateY(-18px)}75%{transform:scaleX(1.15) scaleY(0.88) translateY(2px)}}
        @keyframes danceLion{0%,100%{transform:scale(1) rotate(0)}20%{transform:scale(1.22) rotate(-8deg)}40%{transform:scale(1.18) rotate(8deg)}60%{transform:scale(1.25) rotate(-6deg)}80%{transform:scale(1.2) rotate(6deg)}}
        @keyframes dancePanda{0%,100%{transform:translateX(0) rotate(0)}25%{transform:translateX(-14px) rotate(-15deg)}75%{transform:translateX(14px) rotate(15deg)}}
        @keyframes dancePenguin{0%,100%{transform:translateX(0) rotate(0) translateY(0)}30%{transform:translateX(-10px) rotate(-12deg) translateY(-4px)}70%{transform:translateX(10px) rotate(12deg) translateY(-4px)}}
        @keyframes danceOctopus{0%{transform:rotate(0) scale(1)}15%{transform:rotate(-40deg) scale(1.15)}35%{transform:rotate(35deg) scale(0.9)}55%{transform:rotate(-25deg) scale(1.2)}75%{transform:rotate(30deg) scale(0.95)}100%{transform:rotate(0) scale(1)}}
        @keyframes danceButterfly{0%,100%{transform:translateY(0) rotate(-12deg) scale(1)}25%{transform:translateY(-18px) rotate(14deg) scale(1.15)}50%{transform:translateY(-8px) rotate(-8deg) scale(0.92)}75%{transform:translateY(-14px) rotate(10deg) scale(1.1)}}
        @keyframes danceUnicorn{0%,100%{transform:translateY(0) scaleX(1)}20%{transform:translateY(-14px) scaleX(0.92) rotate(-5deg)}40%{transform:translateY(-8px) scaleX(1.08) rotate(4deg)}60%{transform:translateY(-18px) scaleX(0.95) rotate(-4deg)}80%{transform:translateY(-6px) scaleX(1.05) rotate(3deg)}}
        @keyframes streakBurstAnim{0%{transform:translateX(-50%) scale(0.4);opacity:0}20%{transform:translateX(-50%) scale(1.25);opacity:1}70%{transform:translateX(-50%) scale(1);opacity:1}90%{transform:translateX(-50%) scale(0.95);opacity:0.6}100%{transform:translateX(-50%) scale(0.8);opacity:0}}
        @keyframes comboFinisher{0%{transform:translateX(-50%) scale(0.2) rotate(-8deg);opacity:0}15%{transform:translateX(-50%) scale(1.5) rotate(4deg);opacity:1}35%{transform:translateX(-50%) scale(1.1) rotate(-2deg);opacity:1}60%{transform:translateX(-50%) scale(1.2) rotate(0);opacity:1}85%{transform:translateX(-50%) scale(1.05);opacity:0.9}100%{transform:translateX(-50%) scale(0.7);opacity:0}}
        @keyframes coinPop{0%{transform:translateX(-50%) translateY(0) scale(0.6);opacity:0}20%{transform:translateX(-50%) translateY(-8px) scale(1.2);opacity:1}60%{transform:translateX(-50%) translateY(-18px) scale(1);opacity:1}100%{transform:translateX(-50%) translateY(-30px) scale(0.8);opacity:0}}
        @keyframes mascotIdle{0%,100%{transform:translateY(0) scale(1)}50%{transform:translateY(-5px) scale(1.04)}}
        @keyframes bossRagePulse{0%,100%{box-shadow:0 0 0 0 #ff000044}50%{box-shadow:0 0 0 12px #ff000022}}
        @keyframes prestigePop{0%{transform:scale(0.3) rotate(-20deg);opacity:0}50%{transform:scale(1.3) rotate(5deg)}75%{transform:scale(0.95) rotate(-2deg)}100%{transform:scale(1) rotate(0);opacity:1}}
        @keyframes infinityPulse{0%,100%{text-shadow:0 0 20px #a78bfa,0 0 40px #a78bfa55}50%{text-shadow:0 0 40px #a78bfa,0 0 80px #a78bfaaa}}
        @keyframes vtScreenIn{0%{opacity:0;transform:translateY(14px)}100%{opacity:1;transform:translateY(0)}}
        @keyframes vtScreenOut{0%{opacity:1;transform:translateY(0)}100%{opacity:0;transform:translateY(-10px)}}
        ::view-transition-old(root){animation:vtScreenOut 0.18s ease-in both}
        ::view-transition-new(root){animation:vtScreenIn 0.22s ease-out both}
        *{-webkit-tap-highlight-color:transparent;box-sizing:border-box}
        ::-webkit-scrollbar{width:0}
        .shine-btn{position:relative;overflow:hidden}
        .shine-btn::after{content:'';position:absolute;top:-50%;left:-75%;width:50%;height:200%;background:linear-gradient(to right,transparent,rgba(255,255,255,0.12),transparent);transform:skewX(-20deg);transition:left 0.4s}
        .shine-btn:active::after{left:125%}
      `}</style>

      <canvas ref={canvasRef} className="absolute inset-0 z-0" style={{width:"100%",height:"100%",pointerEvents:"none"}}/>

      {legendaryFlash&&(
        <div className="absolute inset-0 pointer-events-none z-40"
          style={{background:"linear-gradient(135deg,rgba(255,0,80,0.18),rgba(255,160,0,0.15),rgba(255,230,0,0.12),rgba(0,200,80,0.12),rgba(0,140,255,0.15),rgba(160,0,255,0.18))",
            animation:"legendaryRainbow 0.9s ease-out forwards"}}/>
      )}

      {notif&&(
        <div className="absolute top-4 left-1/2 z-50 px-4 py-2.5 rounded-2xl text-sm font-bold pointer-events-none"
          style={{transform:"translateX(-50%)",background:"rgba(0,0,0,0.92)",border:`1px solid ${activeWorldColor}`,color:activeWorldColor,
            boxShadow:`0 0 28px ${activeWorldColor}55,0 4px 24px rgba(0,0,0,0.6)`,maxWidth:"85vw",whiteSpace:"nowrap",textAlign:"center",
            backdropFilter:"blur(12px)",animation:"notifSlide 2.6s ease-in-out forwards",letterSpacing:"0.04em"}}>
          {notif}
        </div>
      )}
      {/* Mid-game achievement popup — richer display with icon + XP */}
      {achPopup&&(
        <div className="absolute z-50 pointer-events-none"
          style={{bottom:"22%",left:"50%",transform:"translateX(-50%)",animation:"perfectPop 2.2s cubic-bezier(0.34,1.4,0.64,1) forwards",textAlign:"center",whiteSpace:"nowrap"}}>
          <div className="flex items-center gap-2 px-4 py-3 rounded-2xl"
            style={{background:"rgba(0,0,0,0.92)",border:"1px solid #ffd70088",
              boxShadow:"0 0 32px #ffd70044,0 4px 20px rgba(0,0,0,0.6)",backdropFilter:"blur(12px)"}}>
            <span style={{fontSize:28}}>{achPopup.icon}</span>
            <div className="flex flex-col items-start">
              <div style={{fontSize:11,color:"#ffd700",fontWeight:"black",letterSpacing:"0.08em",textTransform:"uppercase"}}>Achievement!</div>
              <div style={{fontSize:13,color:"#fff",fontWeight:"bold"}}>{achPopup.label}</div>
              <div style={{fontSize:10,color:"#fbbf24",opacity:0.8}}>+{achPopup.xp} XP</div>
            </div>
          </div>
        </div>
      )}

      <div className="screen-root" style={{position:"absolute",inset:0}}>
      {screen==="menu"          &&renderMenu()}
      {screen==="levelmap"      &&renderLevelMap()}
      {screen==="shop"          &&renderShop()}
      {screen==="playing"       &&renderPlaying()}
      {screen==="levelcomplete" &&renderLevelComplete()}
      {screen==="gameover"      &&renderGameOver()}
      {screen==="missions"      &&renderMissions()}
      {screen==="achievements"  &&renderAchievements()}
      {screen==="leaderboard"   &&renderLeaderboard()}
      {screen==="skilltree"     &&renderSkillTree()}
      {screen==="settings"         &&renderSettings()}
      {screen==="mascotcollection" &&renderMascotCollection()}
      {screen==="spinwheel"     &&renderSpinWheel()}
      {screen==="infinity"      &&renderInfinity()}
      {screen==="zen"           &&renderZen()}
      {screen==="gauntlet"      &&renderGauntlet()}
      {screen==="weekly"        &&renderWeekly()}
      {screen==="tournament"    &&renderTournament()}
      </div>
      {storyData&&renderWorldStory()}
      {tutStep!==null&&renderTutorial()}
      {/* ── SHOP PURCHASE CONFIRMATION ── */}
      {shopConfirm&&(
        <div className="absolute inset-0 flex items-center justify-center z-50 px-5"
          style={{background:"rgba(0,0,0,0.82)",backdropFilter:"blur(10px)",animation:"vtScreenIn 0.18s ease-out"}}
          onClick={(e)=>{if(e.target===e.currentTarget)setShopConfirm(null);}}>
          <div className="w-full max-w-sm rounded-3xl p-5"
            style={{background:"linear-gradient(160deg,#fbbf2422 0%,#180400 70%)",
              border:"1px solid #fbbf2455",boxShadow:"0 0 50px #fbbf2466",
              animation:"victoryBurst 0.36s cubic-bezier(0.34,1.4,0.64,1)"}}>
            <div className="text-center mb-3">
              <div className="text-3xl mb-1">🛒</div>
              <h3 className="font-black text-lg" style={{color:"#fbbf24"}}>Confirm Purchase</h3>
              <p className="text-xs opacity-60" style={{color:"#fff"}}>Coins are spent at start — no refunds</p>
            </div>
            {/* Items list */}
            <div className="space-y-1 mb-3 max-h-44 overflow-y-auto">
              {shopConfirm.items.map(id=>{const item=SHOP_ITEMS.find(i=>i.id===id);return item?(
                <div key={id} className="flex items-center justify-between px-3 py-2 rounded-xl"
                  style={{background:"#ffffff08",border:"1px solid #ffffff15"}}>
                  <div className="flex items-center gap-2">
                    <span style={{fontSize:20}}>{item.icon}</span>
                    <div>
                      <div className="text-sm font-bold" style={{color:"#fff"}}>{item.name}</div>
                      <div className="text-xs opacity-50" style={{color:"#fff"}}>{item.desc}</div>
                    </div>
                  </div>
                  <div className="text-sm font-black" style={{color:"#fbbf24"}}>🪙 {item.cost}</div>
                </div>
              ):null;})}
            </div>
            {/* Total + balance */}
            <div className="rounded-xl p-3 mb-4" style={{background:"#fbbf2410",border:"1px solid #fbbf2433"}}>
              <div className="flex justify-between text-sm mb-1">
                <span className="opacity-60" style={{color:"#fff"}}>Total cost</span>
                <span className="font-black" style={{color:"#fbbf24"}}>🪙 {shopConfirm.total}</span>
              </div>
              <div className="flex justify-between text-sm mb-1">
                <span className="opacity-60" style={{color:"#fff"}}>Your coins</span>
                <span style={{color:"#fff"}}>🪙 {(sv.coins||0).toLocaleString()}</span>
              </div>
              <div className="border-t border-white border-opacity-10 my-1.5"></div>
              <div className="flex justify-between text-sm">
                <span className="opacity-60" style={{color:"#fff"}}>After purchase</span>
                <span className="font-black" style={{color:"#34d399"}}>🪙 {((sv.coins||0)-shopConfirm.total).toLocaleString()}</span>
              </div>
            </div>
            <div className="flex gap-3">
              <NeonButton onClick={()=>setShopConfirm(null)}
                className="flex-1 py-3 text-sm font-bold"
                style={{background:"#ffffff10",border:"1px solid #ffffff20",color:"#ffffff90"}}>
                Cancel
              </NeonButton>
              <NeonButton onClick={()=>{sfx("coin");shopConfirm.onConfirm();}}
                className="flex-1 py-3 text-sm font-black"
                style={{background:"linear-gradient(135deg,#b45309,#fbbf24)",boxShadow:"0 0 24px #fbbf2455",color:"#fff",letterSpacing:"0.04em"}}>
                ✓ Confirm
              </NeonButton>
            </div>
          </div>
        </div>
      )}
      {/* ── DAILY LOGIN BONUS POPUP ── */}
      {dailyBonusData&&(
        <div className="absolute inset-0 flex flex-col items-center justify-center z-50 px-5"
          style={{background:"rgba(0,0,0,0.86)",backdropFilter:"blur(14px)",animation:"vtScreenIn 0.3s ease-out"}}
          onClick={(e)=>{if(e.target===e.currentTarget)setDailyBonusData(null);}}>
          <div className="w-full max-w-sm rounded-3xl p-6 text-center"
            style={{
              background:dailyBonusData.isJackpot?"linear-gradient(160deg,#fbbf2422 0%,#180400 70%)":"linear-gradient(160deg,#a78bfa22 0%,#0a0218 70%)",
              border:`1px solid ${dailyBonusData.isJackpot?"#fbbf24":"#a78bfa"}55`,
              boxShadow:`0 0 60px ${dailyBonusData.isJackpot?"#fbbf24":"#a78bfa"}55`,
              animation:"victoryBurst 0.5s cubic-bezier(0.34,1.4,0.64,1)"}}>
            <div className="text-5xl mb-2" style={{
              animation:"floatGlow 1.6s ease-in-out infinite",
              filter:`drop-shadow(0 0 24px ${dailyBonusData.isJackpot?"#fbbf24":"#a78bfa"})`}}>
              {dailyBonusData.isJackpot?"🎁":"🌞"}
            </div>
            <h2 className="text-xl font-black mb-1" style={{color:dailyBonusData.isJackpot?"#fbbf24":"#a78bfa"}}>
              {dailyBonusData.isJackpot?"WEEKLY JACKPOT!":"Daily Login Bonus!"}
            </h2>
            <p className="text-xs opacity-60 mb-4" style={{color:"#fff"}}>
              Day {dailyBonusData.streak} · {dailyBonusData.isJackpot?"You did it! 🎉":"Welcome back!"}
            </p>
            {/* 7-day calendar */}
            <div className="grid grid-cols-7 gap-1.5 mb-4">
              {[1,2,3,4,5,6,7].map(d=>{
                const isToday=d===dailyBonusData.day;
                const isPast=d<dailyBonusData.day;
                const COIN=[40,60,80,120,160,220,400];
                return(
                  <div key={d} className="flex flex-col items-center" style={{
                    padding:"6px 2px",borderRadius:9,
                    background:isToday?(d===7?"#fbbf2433":"#a78bfa33"):isPast?"#ffffff10":"#ffffff05",
                    border:`1px solid ${isToday?(d===7?"#fbbf24":"#a78bfa"):isPast?"#ffffff20":"#ffffff10"}`,
                    boxShadow:isToday?`0 0 12px ${d===7?"#fbbf24":"#a78bfa"}66`:"none"}}>
                    <div style={{fontSize:9,opacity:0.6,color:isToday?(d===7?"#fbbf24":"#a78bfa"):"#fff"}}>D{d}</div>
                    <div style={{fontSize:14,marginTop:1}}>{isPast?"✓":d===7?"🎁":"🪙"}</div>
                    <div style={{fontSize:8,marginTop:1,opacity:0.7,color:isToday?(d===7?"#fbbf24":"#a78bfa"):"#fff"}}>{COIN[d-1]}</div>
                  </div>
                );
              })}
            </div>
            <div className="flex gap-3 justify-center mb-4">
              <div className="px-3 py-2 rounded-xl flex-1" style={{background:"#fbbf2418",border:"1px solid #fbbf2444"}}>
                <div className="text-xs opacity-50" style={{color:"#fbbf24"}}>Coins</div>
                <div className="text-lg font-black" style={{color:"#fbbf24"}}>+🪙 {dailyBonusData.coins}</div>
              </div>
              <div className="px-3 py-2 rounded-xl flex-1" style={{background:"#a78bfa18",border:"1px solid #a78bfa44"}}>
                <div className="text-xs opacity-50" style={{color:"#a78bfa"}}>XP</div>
                <div className="text-lg font-black" style={{color:"#a78bfa"}}>+{dailyBonusData.xp}</div>
              </div>
            </div>
            <NeonButton onClick={()=>{sfx("coin");setDailyBonusData(null);}}
              className="w-full py-3 text-base font-black"
              style={{background:dailyBonusData.isJackpot?"linear-gradient(135deg,#b45309,#fbbf24)":"linear-gradient(135deg,#6d28d9,#a78bfa)",
                boxShadow:`0 0 30px ${dailyBonusData.isJackpot?"#fbbf24":"#a78bfa"}66`,letterSpacing:"0.05em"}}>
              {dailyBonusData.isJackpot?"🎉 CLAIM JACKPOT":"✨ Awesome!"}
            </NeonButton>
          </div>
        </div>
      )}

      {/* Offline coins overlay */}
      {offlineCoinsData&&(
        <div className="fixed inset-0 z-[120] flex items-center justify-center" style={{background:"rgba(0,0,0,0.72)"}}>
          <div className="relative rounded-2xl p-6 flex flex-col items-center gap-3 text-center"
            style={{background:"linear-gradient(160deg,#14532d22 0%,#0a0218 70%)",border:"1px solid #4ade8055",
              boxShadow:"0 0 60px #4ade8055",maxWidth:320,width:"90%"}}>
            <div className="text-5xl mb-1" style={{filter:"drop-shadow(0 0 16px #4ade80)"}}>🌙</div>
            <h2 className="text-xl font-black" style={{color:"#4ade80"}}>Welcome Back!</h2>
            <p className="text-sm" style={{color:"#86efac"}}>Your coins kept rolling while you were away.</p>
            <div className="rounded-xl px-5 py-3 mt-1" style={{background:"#4ade8018",border:"1px solid #4ade8044"}}>
              <div className="text-4xl font-black" style={{color:"#4ade80"}}>+🪙 {offlineCoinsData.coins}</div>
              <div className="text-xs mt-1" style={{color:"#86efac"}}>
                {offlineCoinsData.hours>=3.9?"4h (max)":offlineCoinsData.hours>=1?`${offlineCoinsData.hours.toFixed(1)}h away`:"~1h away"}
              </div>
            </div>
            <p className="text-xs" style={{color:"#4ade8066"}}>Earn up to 1 coin/10s · max 4 hours</p>
            <NeonButton onClick={()=>setOfflineCoinsData(null)}
              style={{background:"linear-gradient(135deg,#15803d,#4ade80)",boxShadow:"0 0 20px #4ade8066",letterSpacing:"0.05em"}}>
              ✅ Sweet!
            </NeonButton>
          </div>
        </div>
      )}

      {/* Weekly recap overlay — 12C, shown on Sunday */}
      {weeklyRecapData&&(
        <div className="fixed inset-0 z-[120] flex items-center justify-center" style={{background:"rgba(0,0,0,0.80)"}}>
          <div className="relative rounded-2xl p-6 flex flex-col items-center gap-4 text-center"
            style={{background:"linear-gradient(160deg,#1e1b4b22 0%,#0a0218 70%)",border:"1px solid #6366f155",
              boxShadow:"0 0 60px #6366f133",maxWidth:340,width:"90%"}}>
            {/* Sparkles */}
            <div className="absolute inset-0 pointer-events-none overflow-hidden rounded-2xl">
              {[...Array(10)].map((_,i)=>(
                <div key={i} style={{position:"absolute",left:`${(i*31)%100}%`,top:`${(i*47)%80}%`,
                  fontSize:12,animation:`sparkleFloat ${1.5+i*0.2}s ease-in-out ${i*0.1}s infinite`,opacity:0.6}}>
                  {["⭐","💫","✨","🌟"][i%4]}
                </div>
              ))}
            </div>
            <div className="text-5xl relative z-10" style={{filter:"drop-shadow(0 0 20px #6366f1)"}}>📊</div>
            <h2 className="text-xl font-black relative z-10" style={{color:"#818cf8"}}>Weekly Recap</h2>
            <p className="text-xs relative z-10" style={{color:"#a5b4fc"}}>Here's how your week went, adventurer!</p>
            <div className="w-full grid grid-cols-3 gap-2 relative z-10">
              <div className="rounded-xl py-3 flex flex-col items-center gap-1" style={{background:"#6366f115",border:"1px solid #6366f133"}}>
                <div style={{fontSize:20}}>🎮</div>
                <div className="font-black text-lg" style={{color:"#818cf8"}}>{weeklyRecapData.levelsPlayed}</div>
                <div className="text-xs opacity-50" style={{color:"#818cf8"}}>Levels</div>
              </div>
              <div className="rounded-xl py-3 flex flex-col items-center gap-1" style={{background:"#fbbf2415",border:"1px solid #fbbf2433"}}>
                <div style={{fontSize:20}}>🏆</div>
                <div className="font-black text-base" style={{color:"#fbbf24"}}>{weeklyRecapData.bestScore.toLocaleString()}</div>
                <div className="text-xs opacity-50" style={{color:"#fbbf24"}}>Best Score</div>
              </div>
              <div className="rounded-xl py-3 flex flex-col items-center gap-1" style={{background:"#4ade8015",border:"1px solid #4ade8033"}}>
                <div style={{fontSize:20}}>🪙</div>
                <div className="font-black text-lg" style={{color:"#4ade80"}}>~{weeklyRecapData.coinsEarned.toLocaleString()}</div>
                <div className="text-xs opacity-50" style={{color:"#4ade80"}}>Coins</div>
              </div>
            </div>
            <p className="text-xs opacity-40 relative z-10" style={{color:"#818cf8"}}>New week starts tomorrow — keep going!</p>
            <NeonButton onClick={()=>setWeeklyRecapData(null)} className="relative z-10"
              style={{background:"linear-gradient(135deg,#4338ca,#6366f1)",boxShadow:"0 0 20px #6366f155",letterSpacing:"0.05em"}}>
              🚀 Let's go!
            </NeonButton>
          </div>
        </div>
      )}
    </div>
  );
}
