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

function getTimeAttackConfig(worldId=1) {
  const w=WORLDS[(worldId-1)%10];
  return {
    id:`timeattack${worldId}`, world:worldId, worldName:w.name, worldColor:w.color, worldBg:w.bg, worldGrid:w.grid,
    name:`⚡ Time Attack — ${w.name}`, scoreGoal:99999, lives:3, spawnInterval:450,
    targetLifetime:2200, bombRate:0.04, movingRate:0.45, ghostRate:0.12,
    bossEnabled:false, bossRate:0, modifier:{type:"time_attack",desc:"45s sprint! Max score wins!"},
    rarityBonus:0.12, isBoss:false, isLast:false, isZen:true, zenDuration:45000, isTimeAttack:true,
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
  { id:"offline_earn",    label:"Passive Earner",    desc:"Earn coins while offline",          icon:"🌙", xp:20  },
  { id:"all_worlds",      label:"World Traveler",    desc:"Play in all 10 worlds",             icon:"🌍", xp:100 },
  { id:"friday_fever",    label:"Friday Fever",      desc:"Play on a Friday for 2× XP",       icon:"🔥", xp:25  },
  { id:"weekend_warrior", label:"Weekend Warrior",   desc:"Play on a weekend for bonus coins", icon:"🎉", xp:25  },
  { id:"speed_demon",     label:"Speed Demon",       desc:"Complete a level with a speed bonus", icon:"⚡", xp:30 },
  { id:"phantom_catch",   label:"Ghost Hunter",      desc:"Catch a Phantom target",              icon:"👻", xp:40 },
  { id:"volatile_defuse", label:"Bomb Squad",        desc:"Defuse a Volatile target",            icon:"💣", xp:35 },
  { id:"healer_catch",    label:"First Aid",         desc:"Tap a Healer to restore a life",      icon:"❤️", xp:25 },
  { id:"overkill_5x",    label:"OVERKILL",          desc:"Score 5× the level goal",             icon:"🌟", xp:80 },
  { id:"twin_hit",        label:"Dynamic Duo",       desc:"Tap a Twin target pair",              icon:"✦", xp:30  },
  { id:"rainbow_catch",   label:"Color Catcher",     desc:"Tap a Rainbow target",                icon:"🌈", xp:20  },
  { id:"rainbow_legendary",label:"Perfect Rainbow",  desc:"Tap a Rainbow at Legendary tier",     icon:"🌟", xp:60  },
  { id:"frozen_catch",    label:"Ice Breaker",       desc:"Tap a Frozen target's small zone",    icon:"❄️", xp:45  },
  { id:"bouncy_catch",    label:"Reflex Master",     desc:"Catch a fast Bouncy target",          icon:"⚡", xp:30  },
  { id:"ninja_catch",     label:"Ninja Hunter",      desc:"Catch a Ninja target when it appears",icon:"🥷", xp:75  },
  { id:"loot_chest",     label:"Treasure Hunter",   desc:"Tap a Loot Chest for coin drops",     icon:"🪙", xp:35  },
  { id:"first_tap_fever",label:"Hot Start",          desc:"Get First Tap Fever on a rare+ target",icon:"🔥", xp:40  },
  { id:"bounty_hit",     label:"Bounty Hunter",      desc:"Tap a crowned Bounty target",          icon:"👑", xp:30  },
  { id:"tornado_catch",  label:"Eye of the Storm",   desc:"Tap a Tornado target",                 icon:"🌀", xp:45  },
  { id:"bubble_pop",     label:"Pop Star",           desc:"Pop a soap Bubble target",             icon:"🫧", xp:15  },
  { id:"bomb_defuse",    label:"Bomb Squad",         desc:"Double-tap a bomb to defuse it!",      icon:"💚", xp:50  },
  { id:"echo_tap",       label:"Resonance",          desc:"Tap an Echo target",                   icon:"◎",  xp:25  },
  { id:"echo_bonus",     label:"Double Echo",        desc:"Catch the Echo ghost for bonus points",icon:"🔮", xp:55  },
  { id:"gold_rush",      label:"Gold Rush!",          desc:"Trigger a Gold Rush Mode",             icon:"🥇", xp:40  },
  { id:"crystal_shatter",label:"Gem Hunter",         desc:"Shatter a Crystal target",             icon:"💎", xp:30  },
  { id:"crystal_chain",  label:"Full Crystal",       desc:"Tap all 3 crystal shards after shattering",icon:"💠",xp:80 },
  { id:"chain_lightning_hit",label:"Lightning Rod",  desc:"Use the Chain Lightning power-up",     icon:"⚡", xp:45  },
  { id:"rage_tap",           label:"Anger Manager",  desc:"Tap a Rage target",                    icon:"😠", xp:30  },
  { id:"rage_max",           label:"Rage Quit",      desc:"Tap a Rage target at maximum rage",    icon:"😡", xp:75  },
  { id:"divider_tap",        label:"Cell Division",  desc:"Tap a Divider to split it",            icon:"÷",  xp:25  },
  { id:"vanishing_tap",      label:"Ghost Buster",   desc:"Tap a Vanishing target",               icon:"👻", xp:30  },
  { id:"vanishing_blind",    label:"Sixth Sense",    desc:"Tap a Vanishing target while invisible",icon:"🎯", xp:90  },
  { id:"tap_frenzy",         label:"Tap Frenzy",     desc:"Hit 5 targets in 2 seconds",           icon:"⚡", xp:35  },
  { id:"homing_tap",         label:"Target Acquired", desc:"Tap a Homing target",                  icon:"🎯", xp:20  },
  { id:"homing_center",      label:"Bullseye",        desc:"Tap a Homing target near screen center",icon:"🎯", xp:60  },
  { id:"world_complete",     label:"World Conqueror", desc:"Complete all levels in any world",      icon:"🌍", xp:100 },
  { id:"gemstone_tap",       label:"Gem Collector",   desc:"Find and tap a Gemstone",              icon:"💎", xp:120 },
  { id:"poison_tap",         label:"Antidote",        desc:"Neutralize a Poison target",           icon:"☣️", xp:30  },
  { id:"morph_tap",          label:"Shape Shifter",   desc:"Tap a Morph target",                   icon:"🔄", xp:25  },
  { id:"morph_legendary",    label:"Perfect Morph",   desc:"Catch a Morph at Legendary tier",      icon:"🌟", xp:120 },
  { id:"time_warp_use",      label:"Time Lord",       desc:"Use the Time Warp power-up",           icon:"⏱️", xp:40  },
  { id:"conductor_tap",      label:"Music Maestro",   desc:"Tap a Conductor target",               icon:"♪",  xp:30  },
  { id:"siphon_tap",         label:"Danger Seeker",   desc:"Block a Siphon before it drains life", icon:"⚠️", xp:65  },
  { id:"glitch_tap",         label:"Bug Hunter",      desc:"Tap a Glitch target",                  icon:"🟢", xp:25  },
  { id:"glitch_perfect",     label:"Mid-Glitch!",     desc:"Tap a Glitch target mid-teleport",     icon:"⚡", xp:90  },
  { id:"prism_tap",          label:"Prism Hunter",    desc:"Tap a Prism target",                   icon:"🔮", xp:35  },
  { id:"lucky_streak",       label:"Lucky Seven",     desc:"Hit 7 targets in a row for lucky coins",icon:"🍀", xp:30  },
  { id:"score_boost_use",    label:"Rocket Launch",   desc:"Use the Score Boost power-up",         icon:"🚀", xp:25  },
  { id:"comet_tap",          label:"Star Gazer",      desc:"Tap a Comet target",                   icon:"🌠", xp:30  },
  { id:"comet_early",        label:"Shooting Star",   desc:"Catch a Comet in the first half of its flight",icon:"⭐",xp:75 },
  { id:"mirrorball_tap",     label:"Disco King",      desc:"Tap a Mirror Ball target",             icon:"🪩", xp:35  },
  { id:"nexus_tap",          label:"NEXUS!",           desc:"Find and tap the legendary Nexus",     icon:"🌟", xp:500 },
  { id:"phoenix_tap",        label:"Fire Tamer",       desc:"Tap a Phoenix target",                 icon:"🔥", xp:25  },
  { id:"phoenix_risen",      label:"Born Again",       desc:"Tap a Phoenix in its risen Legendary form",icon:"🦋",xp:80 },
  { id:"icecomet_tap",       label:"Frost Strike",     desc:"Tap an Ice Comet and freeze nearby targets",icon:"❄️",xp:40 },
  { id:"voltage_tap",        label:"Lightning Tapper", desc:"Tap a Voltage target and trigger a chain zap",icon:"⚡",xp:35 },
  { id:"void_tap",           label:"Into the Void",    desc:"Tap a Void target",                        icon:"🌀",xp:45 },
  { id:"void_master",        label:"Black Hole",       desc:"Absorb 3+ targets with a single Void tap", icon:"🕳️",xp:120 },
  { id:"clover_tap",         label:"Lucky Tap",        desc:"Tap a Lucky Clover target",                icon:"🍀",xp:30 },
  { id:"clover_jackpot",     label:"Four-Leaf Fortune",desc:"Roll the maximum ×10 on a Lucky Clover",  icon:"🌟",xp:150 },
  { id:"ricochet_tap",       label:"Billiard Shot",    desc:"Tap a Ricochet target",                   icon:"🎯",xp:30 },
  { id:"ricochet_double",    label:"Bank Shot",        desc:"Ricochet kills 2 targets at once",         icon:"💫",xp:75 },
  { id:"aurora_tap",         label:"Borealis Bop",     desc:"Tap an Aurora target",                    icon:"🌌",xp:35 },
  { id:"aurora_perfect",     label:"Perfect Rhythm",   desc:"Tap Aurora with perfect timing rhythm",   icon:"✨",xp:100 },
  { id:"fury_mode",          label:"Fury Mode",        desc:"Reach a 35× streak — unleash the fury!",  icon:"🌑",xp:90 },
  { id:"score_10k",          label:"Ten Thousand",     desc:"Score 10,000 points in a single session", icon:"💎",xp:100 },
  { id:"portal_tap",         label:"Warp Tapper",      desc:"Tap a Portal target",                     icon:"🌀",xp:40 },
  { id:"portal_chaos",       label:"Chaos Agent",      desc:"Teleport 5+ targets with one Portal tap", icon:"🎲",xp:90 },
  { id:"particlebomb_tap",   label:"Boom!",            desc:"Tap a Particle Bomb target",              icon:"💥",xp:35 },
  { id:"beacon_tap",         label:"Signal Boost",     desc:"Tap a Beacon target",                     icon:"🔆",xp:30 },
  { id:"beacon_surge",       label:"Beacon Surge",     desc:"Tap Beacon with 4+ nearby targets",       icon:"⚡",xp:80 },
  { id:"shadow_tap",         label:"Shadow Boxer",     desc:"Tap a Shadow target",                     icon:"🕶️",xp:30 },
  { id:"shadow_clone_catch", label:"Clone Catcher",    desc:"Catch a Shadow clone for bonus pts",      icon:"👤",xp:70 },
  { id:"spectral_tap",       label:"Ghost Buster",     desc:"Tap a Spectral target",                   icon:"👻",xp:35 },
  { id:"spectral_perfect",   label:"Perfect Apparition",desc:"Catch Spectral in its visible phase",   icon:"💛",xp:90 },
  { id:"heart_tap",          label:"Heartbreaker",     desc:"Tap a Heart target",                      icon:"❤️",xp:25 },
  { id:"nova_tap",           label:"Supernova!",       desc:"Tap a Nova target to freeze all enemies", icon:"💫",xp:60 },
  { id:"firefly_tap",        label:"Firefly Catcher",  desc:"Tap a Firefly target",                   icon:"✨",xp:25 },
  { id:"firefly_swift",      label:"Swift Fingers",    desc:"Catch a Firefly within 0.8s of spawn",   icon:"⚡",xp:80 },
  { id:"geode_crack",        label:"Rock Breaker",     desc:"Crack open a Geode target",              icon:"🪨",xp:20 },
  { id:"geode_gem",          label:"Gem Collector",    desc:"Collect the gem from a cracked Geode",   icon:"💎",xp:75 },
  { id:"timebomb_defuse",    label:"Bomb Squad",       desc:"Defuse a Time Bomb before detonation",   icon:"💣",xp:40 },
  { id:"timebomb_clutch",    label:"Clutch Defuse",    desc:"Defuse a Time Bomb in the last 0.4s",    icon:"🔥",xp:120 },
  { id:"thunderbolt_tap",    label:"Lightning Reflexes",desc:"Tap a Thunderbolt target",              icon:"⚡",xp:30 },
  { id:"thunderbolt_clutch", label:"Cliff Hanger",     desc:"Catch Thunderbolt in the bottom quarter", icon:"🌩️",xp:100 },
  { id:"gravityorb_tap",     label:"Gravity Surfer",   desc:"Tap a Gravity Orb target",               icon:"🌐",xp:35 },
  { id:"gravityorb_cluster", label:"Black Hole Master",desc:"Tap Gravity Orb with 4+ pulled targets", icon:"🕳️",xp:110 },
  { id:"crystalball_tap",    label:"Fortune Teller",   desc:"Tap a Crystal Ball to see the future",   icon:"🔮",xp:45 },
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
  { id:"time_warp_start",name:"Time Warp ⏱️",  desc:"Start with Time Warp active (6s slow)", cost:110, icon:"⏱️" },
  { id:"double_spawn", name:"Target Rush 🌊",   desc:"2× target spawn rate from the start",  cost:85,  icon:"🌊" },
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

const BOSS_TAUNTS = {
  phase2: ["You dare challenge me?!","Is that all you've got?","My power grows stronger!","You can't stop me now!","Feel my wrath, tapper!"],
  phase3: ["IMPOSSIBLE! I'm invincible!","You'll regret this!!!","MAXIMUM POWER UNLEASHED!","I won't go down easily!","THIS IS MY FINAL FORM!!!"],
  dying:  ["No... this can't be...","You're... stronger than I thought...","Take the crystal... you earned it...","I'll be back... stronger...","Well played, young tapper..."],
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
  hapticIntensity:70,    // vibration scale 10-100
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
  taBest:0,                // best score in time attack mode
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
let _hapticIntensity = 70; // 10-100, scales vibration duration
function vibrate(p){
  try{
    if(!_hapticOn||!navigator.vibrate)return;
    const scale=(_hapticIntensity??70)/70; // 1.0 = default
    const scaled=Array.isArray(p)?p.map(v=>Math.round(v*scale)):Math.round(p*scale);
    navigator.vibrate(scaled);
  }catch{}
}

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
  const icons={SHIELD:"🛡",SLOW:"🐢",DOUBLE:"×2",LIFE:"❤️",FREEZE:"❄️",LUCKY:"⭐",MIRROR:"🪞",MULTIPLIER:"×3",COMBO_FREEZE:"🧊",GRAVITY:"🌐",CHAIN_LIGHTNING:"⚡",TIME_WARP:"⏱️",SCORE_BOOST:"×5",LIFE_SURGE:"❤️+2",MAGNET_FIELD:"🧲",OVERCLOCK:"⚡",SHIELD_WALL:"🏰"};
  if(pwrType==="LUCKY"){ctx.shadowColor="#ffd700";ctx.shadowBlur=r*(1.2+pulse*0.8);}
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

// ── Poison target — avoid it; if it expires, next target gives 50% score ──
function drawPoison(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.009);
  const drip=Math.sin(ts*0.015)*2;
  ctx.save();
  // Toxic aura
  ctx.globalAlpha=0.18+pulse*0.18;ctx.fillStyle="#4ade80";ctx.shadowColor="#16a34a";ctx.shadowBlur=22+pulse*14;
  ctx.beginPath();ctx.arc(0,0,r*1.28,0,Math.PI*2);ctx.fill();
  // Core — sickly green
  ctx.globalAlpha=1;
  const pg=ctx.createRadialGradient(0,0,0,0,0,r);
  pg.addColorStop(0,"rgba(187,247,208,0.92)");pg.addColorStop(0.5,"rgba(74,222,128,0.88)");pg.addColorStop(1,"rgba(22,101,52,0.82)");
  ctx.fillStyle=pg;ctx.shadowColor="#22c55e";ctx.shadowBlur=14;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Biohazard-ish symbol (3 arcs)
  ctx.globalAlpha=0.6+pulse*0.2;ctx.strokeStyle="#14532d";ctx.lineWidth=2.5;ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(0,0,r*0.28,0,Math.PI*2);ctx.stroke();
  [0,Math.PI*2/3,Math.PI*4/3].forEach(a=>{
    ctx.beginPath();ctx.arc(Math.cos(a)*r*0.45,Math.sin(a)*r*0.45,r*0.22,a-0.3,a+Math.PI*0.65);ctx.stroke();
  });
  // Drip at bottom
  ctx.globalAlpha=0.7+pulse*0.2;ctx.translate(0,drip);
  ctx.fillStyle="#bbf7d0";
  ctx.beginPath();ctx.arc(0,r*0.68,r*0.1,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(r*0.3,r*0.62,r*0.07,0,Math.PI*2);ctx.fill();
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

// ── Divider target — large orb with crack; splits into 2 medium targets ──
function drawDivider(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  const crackShift=Math.sin(ts*0.015)*1.2; // crack vibrates
  ctx.save();
  // Outer halo
  ctx.globalAlpha=0.18+pulse*0.14;ctx.fillStyle="#fb923c";ctx.shadowColor="#ea580c";ctx.shadowBlur=28;
  ctx.beginPath();ctx.arc(0,0,r*1.28,0,Math.PI*2);ctx.fill();
  // Main body
  ctx.globalAlpha=1;
  const dg=ctx.createRadialGradient(0,0,0,0,0,r);
  dg.addColorStop(0,"rgba(253,186,116,0.95)");dg.addColorStop(0.55,"rgba(251,146,60,0.9)");dg.addColorStop(1,"rgba(234,88,12,0.85)");
  ctx.fillStyle=dg;ctx.shadowColor="#f97316";ctx.shadowBlur=16;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Crack line through center
  ctx.globalAlpha=0.85+pulse*0.12;ctx.strokeStyle="#fef3c7";ctx.lineWidth=2.5;
  ctx.shadowColor="#fbbf24";ctx.shadowBlur=8;
  ctx.beginPath();
  ctx.moveTo(-r*0.05+crackShift,-r*0.85);
  ctx.lineTo(r*0.12+crackShift,-r*0.25);
  ctx.lineTo(-r*0.08+crackShift,r*0.15);
  ctx.lineTo(r*0.1+crackShift,r*0.82);
  ctx.stroke();
  // ÷ symbol hint
  ctx.globalAlpha=0.65+pulse*0.2;ctx.fillStyle="#fff7ed";ctx.shadowBlur=4;
  ctx.font=`bold ${Math.round(r*0.5)}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("÷",-r*0.2,0);
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

// ── Magnet target — pulls nearby targets toward it ──
function drawMagnet(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.006);
  const spin=ts*0.0018;
  ctx.save();
  // Outer magnetic field rings
  for(let i=1;i<=3;i++){
    ctx.save();
    ctx.globalAlpha=(0.12+pulse*0.08)/i;
    ctx.strokeStyle="#ec4899";ctx.lineWidth=1.5;
    ctx.setLineDash([4+i*2,4+i*2]);ctx.lineDashOffset=ts*0.03*i;
    ctx.beginPath();ctx.arc(0,0,r*(1.4+i*0.35),0,Math.PI*2);ctx.stroke();
    ctx.setLineDash([]);ctx.restore();
  }
  // Glow
  const grd=ctx.createRadialGradient(0,0,r*0.2,0,0,r*2);
  grd.addColorStop(0,"#ec489944");grd.addColorStop(0.6,"#ec489911");grd.addColorStop(1,"transparent");
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*2,0,Math.PI*2);ctx.fill();
  // Body — hot pink
  ctx.shadowColor="#ec4899";ctx.shadowBlur=r*(0.8+pulse*0.4);
  const body=ctx.createRadialGradient(-r*0.3,-r*0.3,0,0,0,r);
  body.addColorStop(0,"#fce7f3");body.addColorStop(0.5,"#ec4899");body.addColorStop(1,"#9d174d");
  ctx.fillStyle=body;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Horseshoe magnet U shape
  ctx.save();ctx.rotate(spin*0.5);
  ctx.strokeStyle="rgba(255,255,255,0.9)";ctx.lineWidth=r*0.14;ctx.lineCap="round";
  ctx.shadowColor="#fff";ctx.shadowBlur=6;
  ctx.beginPath();ctx.arc(0,0,r*0.45,Math.PI,0,false);ctx.stroke();
  ctx.beginPath();ctx.moveTo(-r*0.45,-0.1);ctx.lineTo(-r*0.45,r*0.22);ctx.stroke();
  ctx.beginPath();ctx.moveTo(r*0.45,-0.1);ctx.lineTo(r*0.45,r*0.22);ctx.stroke();
  ctx.restore();
  ctx.restore();
}

// ── Ice Comet target — frozen streaker; freezes nearby targets on expiry ──
function drawIceComet(ctx, r, ts, trail) {
  const pulse=0.7+0.3*Math.sin(ts*0.01);
  // Icy trail
  if(trail&&trail.length>1){
    for(let i=1;i<trail.length;i++){
      const alpha=(i/trail.length)*0.4*pulse;
      const sz=r*(i/trail.length)*0.6;
      ctx.save();
      ctx.globalAlpha=alpha;
      ctx.fillStyle=`hsl(${195+i*4},100%,${75-i*2}%)`;
      ctx.translate(trail[i].x-trail[trail.length-1].x,trail[i].y-trail[trail.length-1].y);
      ctx.beginPath();ctx.arc(0,0,sz,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
  }
  // Ice crystals around head
  ctx.save();
  for(let i=0;i<6;i++){
    const a=(i/6)*Math.PI*2+ts*0.001;
    ctx.fillStyle="#bae6fd";ctx.globalAlpha=0.5*pulse;
    const px=Math.cos(a)*(r+6),py=Math.sin(a)*(r+6);
    ctx.beginPath();ctx.moveTo(px,py);ctx.lineTo(px+3,py-4);ctx.lineTo(px-3,py-4);ctx.closePath();ctx.fill();
  }
  // Core
  ctx.globalAlpha=1;
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#ffffff");grad.addColorStop(0.3,"#bae6fd");grad.addColorStop(0.7,"#0ea5e9");grad.addColorStop(1,"#075985");
  ctx.fillStyle=grad;ctx.shadowColor="#38bdf8";ctx.shadowBlur=20+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.font=`${Math.floor(r*0.9)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("❄️",0,1);
  ctx.restore();
}

// ── Phoenix target — fiery bird; when expired it respawns once as Epic ──
function drawPhoenix(ctx, r, ts, isRisen) {
  const pulse=0.6+0.4*Math.sin(ts*0.012);
  const spin=ts*0.0005;
  const col1=isRisen?"#c084fc":"#f97316";
  const col2=isRisen?"#7c3aed":"#dc2626";
  // Flame aura
  const grad=ctx.createRadialGradient(0,0,r*0.2,0,0,r*1.6);
  grad.addColorStop(0,col1+"cc");grad.addColorStop(0.5,col1+"44");grad.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=0.55*pulse;ctx.fillStyle=grad;
  ctx.beginPath();ctx.arc(0,0,r*1.6,0,Math.PI*2);ctx.fill();
  // Flickering flames (5 spikes radiating up)
  ctx.globalAlpha=0.75*pulse;ctx.fillStyle=col1;
  for(let i=0;i<5;i++){
    const a=-Math.PI/2+(i-2)*0.3+Math.sin(ts*0.018+i)*0.15;
    const fl=r*(0.8+Math.random()*0.4);
    ctx.save();ctx.rotate(a);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(-4,-fl);ctx.lineTo(4,-fl);ctx.closePath();ctx.fill();
    ctx.restore();
  }
  // Body
  ctx.globalAlpha=1;ctx.rotate(spin);
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#fff5f5");bg.addColorStop(0.35,col1);bg.addColorStop(1,col2);
  ctx.fillStyle=bg;ctx.shadowColor=col1;ctx.shadowBlur=14+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Bird emoji or phoenix emoji
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.font=`${Math.floor(r*1.0)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText(isRisen?"🦋":"🔥",0,1);
  ctx.restore();
}

// ── Nexus target — ultra-rare cosmic core; 2000+ pts; orbiting planets ──
function drawNexus(ctx, r, ts) {
  const pulse=0.65+0.35*Math.sin(ts*0.006);
  const spin=ts*0.0007;
  // Outer galaxy nebula
  const neb=ctx.createRadialGradient(0,0,r*0.3,0,0,r*2.5);
  neb.addColorStop(0,"#ffd70055");neb.addColorStop(0.4,"#a78bfa33");neb.addColorStop(0.7,"#60a5fa18");neb.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=0.7*pulse;ctx.fillStyle=neb;
  ctx.beginPath();ctx.arc(0,0,r*2.5,0,Math.PI*2);ctx.fill();
  // Orbiting planets
  const planets=[{r2:r*1.5,sz:r*0.22,col:"#60a5fa",spd:0.0014},{r2:r*2.0,sz:r*0.16,col:"#f472b6",spd:-0.0009},{r2:r*1.2,sz:r*0.14,col:"#34d399",spd:0.002}];
  planets.forEach(p=>{
    const ang=spin*p.spd/0.0007+ts*p.spd;
    ctx.globalAlpha=0.9;ctx.fillStyle=p.col;ctx.shadowColor=p.col;ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(Math.cos(ang)*p.r2,Math.sin(ang)*p.r2,p.sz,0,Math.PI*2);ctx.fill();
  });
  // Inner core — layered gradients
  ctx.globalAlpha=1;ctx.rotate(spin*2);
  const core=ctx.createRadialGradient(0,0,0,0,0,r);
  core.addColorStop(0,"#ffffff");core.addColorStop(0.2,"#fde68a");core.addColorStop(0.5,"#ffd700");core.addColorStop(0.8,"#b45309");core.addColorStop(1,"#78350f");
  ctx.fillStyle=core;ctx.shadowColor="#ffd700";ctx.shadowBlur=28+pulse*20;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Star burst rays
  ctx.strokeStyle="#fde68a";ctx.lineWidth=1.5;ctx.globalAlpha=0.5*pulse;
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    ctx.beginPath();ctx.moveTo(Math.cos(a)*r*0.8,Math.sin(a)*r*0.8);ctx.lineTo(Math.cos(a)*r*1.6,Math.sin(a)*r*1.6);ctx.stroke();
  }
  // "N" logo in center
  ctx.globalAlpha=1;ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.font=`black ${Math.floor(r*0.9)}px 'Exo 2',sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("N",0,0);
  ctx.restore();
}

// ── Mirror Ball target — disco ball; tapping spawns 3 mini copies ──
function drawMirrorBall(ctx, r, ts) {
  const spin=ts*0.002;
  const pulse=0.6+0.4*Math.sin(ts*0.01);
  ctx.save();ctx.rotate(spin);
  // Outer shimmer
  const numFacets=12;
  for(let i=0;i<numFacets;i++){
    const angle=(i/numFacets)*Math.PI*2;
    const fx=Math.cos(angle)*r*0.75;const fy=Math.sin(angle)*r*0.75;
    const hue=(i/numFacets)*360+(ts*0.05)%360;
    const sz=r*0.22;
    ctx.fillStyle=`hsl(${hue},100%,70%)`;
    ctx.globalAlpha=(0.5+0.5*Math.sin(angle*3+ts*0.008))*0.85;
    ctx.beginPath();ctx.arc(fx,fy,sz,0,Math.PI*2);ctx.fill();
  }
  // Main silvery body
  ctx.globalAlpha=1;
  const grad=ctx.createRadialGradient(-r*0.25,-r*0.25,0,0,0,r);
  grad.addColorStop(0,"#ffffff");grad.addColorStop(0.3,"#e2e8f0");grad.addColorStop(0.7,"#94a3b8");grad.addColorStop(1,"#1e293b");
  ctx.fillStyle=grad;ctx.shadowColor="#ffffff";ctx.shadowBlur=14+pulse*10;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Grid lines
  ctx.strokeStyle="#ffffff33";ctx.lineWidth=0.8;ctx.shadowBlur=0;
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    ctx.beginPath();ctx.moveTo(-r,Math.cos(a)*r*0.7);ctx.lineTo(r,Math.cos(a)*r*0.7);ctx.stroke();
  }
  for(let i=0;i<8;i++){
    const a=i*Math.PI/4;
    ctx.beginPath();ctx.moveTo(Math.cos(a)*r*0.7,-r);ctx.lineTo(Math.cos(a)*r*0.7,r);ctx.stroke();
  }
  ctx.restore();
}

// ── Comet target — streaks across the screen in a straight line; short lifetime ──
function drawComet(ctx, r, ts, trail) {
  const pulse=0.7+0.3*Math.sin(ts*0.015);
  // Draw trail history
  if(trail&&trail.length>1){
    for(let i=1;i<trail.length;i++){
      const alpha=(i/trail.length)*0.55*pulse;
      const size=r*(i/trail.length)*0.7;
      const dx=trail[i].x-trail[i-1].x;const dy=trail[i].y-trail[i-1].y;
      ctx.save();
      ctx.globalAlpha=alpha;
      ctx.fillStyle=`hsl(${45+i*8},100%,${65+i*2}%)`;
      ctx.translate(trail[i].x-trail[trail.length-1].x,trail[i].y-trail[trail.length-1].y);
      ctx.beginPath();ctx.arc(0,0,size,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
  }
  // Head — bright white-gold core
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#ffffff");grad.addColorStop(0.3,"#fde68a");grad.addColorStop(0.7,"#f59e0b");grad.addColorStop(1,"#92400e");
  ctx.save();ctx.fillStyle=grad;ctx.shadowColor="#fde68a";ctx.shadowBlur=18+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Star symbol ★
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.font=`bold ${Math.floor(r*0.9)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("★",0,1);
  ctx.restore();
}

// ── Prism target — refracts light into 3 rainbow beams when tapped ──
function drawPrism(ctx, r, ts) {
  const spin=ts*0.0009;
  const pulse=0.7+0.3*Math.sin(ts*0.008);
  // Rainbow shimmer aura
  const hue1=(ts*0.04)%360;
  const aura=ctx.createRadialGradient(0,0,r*0.3,0,0,r*1.6);
  aura.addColorStop(0,`hsla(${hue1},100%,75%,0.5)`);
  aura.addColorStop(0.5,`hsla(${(hue1+120)%360},100%,60%,0.25)`);
  aura.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=0.55*pulse;ctx.fillStyle=aura;
  ctx.beginPath();ctx.arc(0,0,r*1.6,0,Math.PI*2);ctx.fill();
  // Main prism body — elongated diamond shape
  ctx.globalAlpha=1;
  ctx.rotate(spin);
  const pts3=[[0,-r*1.1],[r*0.65,0],[0,r*1.1],[-r*0.65,0]];
  const prismGrad=ctx.createLinearGradient(-r,0,r,0);
  for(let i=0;i<7;i++) prismGrad.addColorStop(i/6,`hsl(${(hue1+i*52)%360},100%,65%)`);
  ctx.fillStyle=prismGrad;ctx.shadowColor="#ffffff";ctx.shadowBlur=12+pulse*10;
  ctx.beginPath();pts3.forEach(([px,py],i)=>i===0?ctx.moveTo(px,py):ctx.lineTo(px,py));ctx.closePath();ctx.fill();
  // Inner facet lines
  ctx.strokeStyle="#ffffff88";ctx.lineWidth=1;ctx.shadowBlur=0;
  ctx.beginPath();ctx.moveTo(-r*0.65,0);ctx.lineTo(0,-r*1.1);ctx.lineTo(r*0.65,0);ctx.lineTo(0,r*1.1);ctx.stroke();
  ctx.restore();
}

// ── Glitch target — corrupted pixel art; teleports every 0.9s; catch mid-teleport for bonus ──
function drawGlitch(ctx, r, ts) {
  const blinkRate=300;const blink=Math.floor(ts/blinkRate)%2===0;
  const jitter=blink?0:Math.random()*3-1.5; // position jitter when "glitching"
  ctx.save();ctx.translate(jitter,jitter*0.6);
  // Digital corruption bars
  const numBars=5;
  for(let i=0;i<numBars;i++){
    const barY=-r+i*(r*2/numBars);
    const barH=r*2/numBars*0.8;
    const shift=Math.sin(ts*0.02+i*1.4)*r*0.4*(blink?1:0.2);
    const hue=(i*72+ts*0.1)%360;
    ctx.fillStyle=`hsl(${hue},100%,60%)`;
    ctx.globalAlpha=0.75;
    ctx.fillRect(-r+shift,barY,r*2,barH);
  }
  // Main body — dark with scanlines
  ctx.globalAlpha=0.92;
  const grad=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  grad.addColorStop(0,"#0f172a");grad.addColorStop(0.7,"#1e293b");grad.addColorStop(1,"#334155");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Scanlines
  ctx.globalAlpha=0.2;ctx.strokeStyle="#ffffff";ctx.lineWidth=0.8;
  for(let y=-r;y<r;y+=4){
    ctx.beginPath();ctx.moveTo(-Math.sqrt(Math.max(0,r*r-y*y)),y);
    ctx.lineTo(Math.sqrt(Math.max(0,r*r-y*y)),y);ctx.stroke();
  }
  // Glitch text
  ctx.globalAlpha=blink?1:0.4;
  ctx.fillStyle=blink?"#00ff88":"#ff0080";
  ctx.font=`bold ${Math.floor(r*0.75)}px monospace`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.shadowColor=blink?"#00ff88":"#ff0080";ctx.shadowBlur=10;
  ctx.fillText("ERR",0,0);
  ctx.restore();
}

// ── Siphon target — dark vortex that drains 1 life on expiry; tap it for huge reward ──
function drawSiphon(ctx, r, ts, lifeLeft) {
  const pulse=0.6+0.4*Math.sin(ts*0.014);
  const dangerpct=1-lifeLeft;
  const warnCol=dangerpct>0.6?"#ef4444":"#dc2626";
  // Outer vortex ring
  const spin=-ts*0.006; // counter-clockwise, sinister
  ctx.save();
  ctx.rotate(spin);
  // Pulsing dark aura
  const aura=ctx.createRadialGradient(0,0,r*0.4,0,0,r*1.6);
  aura.addColorStop(0,"#7f1d1d88");aura.addColorStop(0.55,warnCol+"44");aura.addColorStop(1,"transparent");
  ctx.globalAlpha=0.6*pulse;ctx.fillStyle=aura;
  ctx.beginPath();ctx.arc(0,0,r*1.6,0,Math.PI*2);ctx.fill();
  // Dark spiral arms (vortex look)
  ctx.globalAlpha=0.8;
  for(let i=0;i<3;i++){
    const armA=(i*(Math.PI*2/3));
    ctx.strokeStyle=warnCol;ctx.lineWidth=2;
    ctx.shadowColor=warnCol;ctx.shadowBlur=8;
    ctx.beginPath();
    for(let s=0;s<12;s++){
      const ang=armA+s*0.22;
      const rad=r*(0.2+s*0.065);
      s===0?ctx.moveTo(Math.cos(ang)*rad,Math.sin(ang)*rad):ctx.lineTo(Math.cos(ang)*rad,Math.sin(ang)*rad);
    }
    ctx.stroke();
  }
  ctx.restore();
  // Body
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#450a0a");bg.addColorStop(0.5,"#991b1b");bg.addColorStop(1,"#450a0a");
  ctx.save();ctx.fillStyle=bg;ctx.shadowColor=warnCol;ctx.shadowBlur=14+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Warning symbol
  ctx.fillStyle="#fff";ctx.shadowBlur=0;
  ctx.font=`bold ${Math.floor(r*1.1)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.globalAlpha=0.7+0.3*pulse;
  ctx.fillText("⚠",0,1);
  ctx.restore();
}

// ── Conductor target — musical note theme; when tapped boosts spawn for 5s ──
function drawConductor(ctx, r, ts) {
  const pulse=0.7+0.3*Math.sin(ts*0.009);
  const beat=0.5+0.5*Math.sin(ts*0.016); // faster "heartbeat" to music
  // Outer resonance ring
  const grad=ctx.createRadialGradient(0,0,r*0.2,0,0,r*1.5);
  grad.addColorStop(0,"#fb923c99");grad.addColorStop(0.5,"#f9780433");grad.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=0.5*pulse;ctx.fillStyle=grad;
  ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.fill();
  // Body
  ctx.globalAlpha=1;
  const bg=ctx.createRadialGradient(-r*0.2,-r*0.2,0,0,0,r);
  bg.addColorStop(0,"#fed7aa");bg.addColorStop(0.45,"#f97316");bg.addColorStop(1,"#7c2d12");
  ctx.fillStyle=bg;ctx.shadowColor="#f97316";ctx.shadowBlur=12+beat*10;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Musical note symbol ♪
  ctx.fillStyle="#fff";ctx.shadowBlur=0;ctx.shadowColor="transparent";
  ctx.font=`bold ${Math.floor(r*1.1)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("♪",0,0);
  // Orbiting music dots
  for(let i=0;i<3;i++){
    const angle=ts*0.003+i*(Math.PI*2/3);
    const ox=Math.cos(angle)*(r+7);const oy=Math.sin(angle)*(r+7);
    ctx.globalAlpha=0.7*pulse;ctx.fillStyle=["#fde68a","#fca5a5","#86efac"][i];
    ctx.beginPath();ctx.arc(ox,oy,3,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

// ── Vanishing target — blinks in/out of visibility every ~0.8s ──
function drawVanishing(ctx, r, ts) {
  // Blink cycle: visible for 40% of cycle, invisible for 60%
  const cycleLen=800; // ms
  const phase=(ts%cycleLen)/cycleLen;
  const visible=phase<0.4; // visible 40% of the time
  const fadeFrac=visible?(phase<0.05?phase/0.05:(0.4-phase<0.05?(0.4-phase)/0.05:1)):0;
  if(fadeFrac<=0)return; // fully invisible — still hittable though!
  const pulse=0.5+0.5*Math.sin(ts*0.008);
  ctx.save();
  ctx.globalAlpha=fadeFrac*(0.7+pulse*0.2);
  // Ghostly white/cyan body
  const vg=ctx.createRadialGradient(0,0,0,0,0,r);
  vg.addColorStop(0,"rgba(240,255,255,0.92)");vg.addColorStop(0.5,"rgba(103,232,249,0.8)");vg.addColorStop(1,"rgba(14,165,233,0.6)");
  ctx.fillStyle=vg;ctx.shadowColor="#67e8f9";ctx.shadowBlur=20+pulse*14;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Blink ring
  ctx.globalAlpha=fadeFrac*0.7;ctx.strokeStyle="#bae6fd";ctx.lineWidth=2.5;ctx.shadowBlur=8;
  ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);ctx.stroke();
  // ? symbol — what is it?
  ctx.globalAlpha=fadeFrac*(0.7+pulse*0.25);ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.font=`bold ${Math.round(r*0.65)}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("?",0,0);
  ctx.restore();
}

// ── Ninja target — nearly invisible, materializes in last 20% of lifetime ──
function drawNinja(ctx, r, ts, lifeRatio) {
  // Only fully visible in last 20%; faint shimmer hint for 80-40%; invisible for 40-20%
  let alpha;
  if(lifeRatio>0.6) alpha=0.04+0.06*Math.sin(ts*0.004); // barely visible shimmer hint
  else if(lifeRatio>0.2) alpha=0.0; // completely invisible
  else alpha=Math.pow(1-lifeRatio/0.2,2)*0.95; // materializes rapidly in final 20%
  if(alpha<=0.01) return; // skip draw
  ctx.save();ctx.globalAlpha=alpha;
  // Dark smoke body
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#9ca3af");bg.addColorStop(0.5,"#6b7280");bg.addColorStop(1,"#111827");
  ctx.fillStyle=bg;ctx.shadowColor="#374151";ctx.shadowBlur=12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Ninja mask eyes
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(-r*0.25,-r*0.1,r*0.13,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.arc(r*0.25,-r*0.1,r*0.13,0,Math.PI*2);ctx.fill();
  // Shuriken star shape
  if(lifeRatio<0.2){
    const spin=ts*0.012;ctx.strokeStyle="#e2e8f0";ctx.lineWidth=1.5;
    for(let i=0;i<4;i++){
      const a=i*Math.PI/2+spin;
      ctx.beginPath();ctx.moveTo(Math.cos(a)*r*0.6,Math.sin(a)*r*0.6);
      ctx.lineTo(Math.cos(a+Math.PI/4)*r*0.25,Math.sin(a+Math.PI/4)*r*0.25);
      ctx.stroke();
    }
  }
  ctx.restore();
}

// ── Homing target — drifts toward screen center; arrows show direction ──
function drawHoming(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  const spin=ts*0.0022;
  ctx.save();
  // Outer orbit ring with arrow markers
  ctx.globalAlpha=0.22+pulse*0.18;ctx.strokeStyle="#34d399";ctx.lineWidth=2.5;
  ctx.shadowColor="#059669";ctx.shadowBlur=18+pulse*12;
  ctx.setLineDash([6,5]);ctx.lineDashOffset=-spin*80;
  ctx.beginPath();ctx.arc(0,0,r*1.38,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);
  // Direction arrows on orbit ring (pointing inward = target moves to center)
  ctx.globalAlpha=0.6+pulse*0.25;ctx.fillStyle="#4ade80";ctx.shadowBlur=6;
  [0,Math.PI*0.66,Math.PI*1.32].forEach(a=>{
    const rx=Math.cos(a+spin)*r*1.38,ry=Math.sin(a+spin)*r*1.38;
    ctx.save();ctx.translate(rx,ry);ctx.rotate(a+spin+Math.PI); // pointing inward
    ctx.beginPath();ctx.moveTo(0,-4.5);ctx.lineTo(3.5,3);ctx.lineTo(-3.5,3);ctx.closePath();ctx.fill();
    ctx.restore();
  });
  ctx.globalAlpha=1;
  // Core — green gradient
  const hg=ctx.createRadialGradient(0,0,0,0,0,r);
  hg.addColorStop(0,"rgba(134,239,172,0.95)");hg.addColorStop(0.6,"rgba(52,211,153,0.88)");hg.addColorStop(1,"rgba(5,150,105,0.8)");
  ctx.fillStyle=hg;ctx.shadowColor="#10b981";ctx.shadowBlur=14;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Target crosshair
  ctx.globalAlpha=0.7+pulse*0.2;ctx.strokeStyle="#d1fae5";ctx.lineWidth=1.5;ctx.shadowBlur=4;
  ctx.beginPath();ctx.moveTo(-r*0.55,0);ctx.lineTo(r*0.55,0);ctx.stroke();
  ctx.beginPath();ctx.moveTo(0,-r*0.55);ctx.lineTo(0,r*0.55);ctx.stroke();
  ctx.beginPath();ctx.arc(0,0,r*0.3,0,Math.PI*2);ctx.stroke();
  ctx.restore();
}

// ── Bouncy target — fast-moving elastic ball with squish trails ──
function drawBouncy(ctx, r, ts) {
  const bounce=0.5+0.5*Math.sin(ts*0.014);
  const squish=1+bounce*0.12;
  ctx.save();
  // Elastic squish transform
  ctx.scale(squish,1/squish);
  // Outer glow
  ctx.globalAlpha=0.4+bounce*0.3;
  ctx.fillStyle="#fef08a";ctx.shadowColor="#eab308";ctx.shadowBlur=20+bounce*10;
  ctx.beginPath();ctx.arc(0,0,r*1.4,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;
  // Gradient body
  const bg=ctx.createRadialGradient(-r*0.28,-r*0.3,0,0,0,r);
  bg.addColorStop(0,"#fef9c3");bg.addColorStop(0.4,"#fde047");bg.addColorStop(0.8,"#eab308");bg.addColorStop(1,"#a16207");
  ctx.fillStyle=bg;ctx.shadowColor="#eab308";ctx.shadowBlur=12+bounce*6;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Shine highlight
  ctx.fillStyle="#fffbeb66";
  ctx.beginPath();ctx.ellipse(-r*0.22,-r*0.3,r*0.3,r*0.18,Math.PI*0.3,0,Math.PI*2);ctx.fill();
  // Speed lines (3 arcs)
  ctx.globalAlpha=0.45;ctx.strokeStyle="#fbbf24";ctx.lineWidth=1.5;
  for(let i=0;i<3;i++){
    ctx.beginPath();ctx.arc(0,0,r*(1.1+i*0.12),Math.PI*0.6,Math.PI*1.4);ctx.stroke();
  }
  ctx.restore();
}

// ── Frozen target — smaller tap zone, 3× points, crystalline ice ──
function drawFrozen(ctx, r, ts) {
  const sparkle=0.5+0.5*Math.sin(ts*0.012);
  const spin=ts*0.0008;
  ctx.save();
  // Ice crystal outer ring with snowflake spokes
  ctx.globalAlpha=0.5+sparkle*0.3;ctx.strokeStyle="#e0f2fe";ctx.lineWidth=1.5;ctx.shadowColor="#93c5fd";ctx.shadowBlur=18;
  for(let i=0;i<6;i++){
    const a=i*Math.PI/3+spin;
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*r*1.35,Math.sin(a)*r*1.35);ctx.stroke();
    // Small crossbar
    const mx=Math.cos(a)*r*0.8,my=Math.sin(a)*r*0.8;
    const bx=Math.cos(a+Math.PI/2)*5,by=Math.sin(a+Math.PI/2)*5;
    ctx.beginPath();ctx.moveTo(mx-bx,my-by);ctx.lineTo(mx+bx,my+by);ctx.stroke();
  }
  // Icy body
  ctx.globalAlpha=1;
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#f0f9ff");bg.addColorStop(0.4,"#bfdbfe");bg.addColorStop(0.75,"#60a5fa");bg.addColorStop(1,"#2563eb");
  ctx.fillStyle=bg;ctx.shadowColor="#93c5fd";ctx.shadowBlur=14+sparkle*8;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // ×3 label
  ctx.fillStyle="#ffffff";ctx.font=`black ${r*0.6}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=0;
  ctx.fillText("×3",0,0);
  // Reduce effective tap radius visual indicator (dotted inner circle at 70%)
  ctx.globalAlpha=0.35;ctx.setLineDash([3,3]);ctx.strokeStyle="#ff0000";ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(0,0,r*0.7,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}

// ── Rainbow target — cycles rarity every ~2s, score based on current tier ──
const RAINBOW_CYCLE=[
  {color:"#a0a0a0",glow:"#c0c0c0",name:"common",mult:1},
  {color:"#4ecb71",glow:"#22c55e",name:"uncommon",mult:2},
  {color:"#60a5fa",glow:"#3b82f6",name:"rare",mult:3},
  {color:"#b06de8",glow:"#9333ea",name:"epic",mult:5},
  {color:"#ffd700",glow:"#f59e0b",name:"legendary",mult:10},
];
function getRainbowTier(ts){return RAINBOW_CYCLE[Math.floor(ts/2000)%RAINBOW_CYCLE.length];}
function drawRainbow(ctx, r, ts) {
  const tier=getRainbowTier(ts);
  const frac=(ts%2000)/2000; // 0→1 within current cycle
  const pulse=0.5+0.5*Math.sin(ts*0.01);
  const spin=ts*0.001;
  ctx.save();
  // Rainbow ring that rotates with hue shift
  ctx.globalAlpha=0.6;ctx.lineWidth=3;ctx.shadowColor=tier.glow;ctx.shadowBlur=18;
  const grad=ctx.createConicalGradient?.(0,0,0)||null;
  ctx.strokeStyle=tier.color;
  ctx.beginPath();ctx.arc(0,0,r*1.4,0,Math.PI*2);ctx.stroke();
  // Body with current tier color
  ctx.globalAlpha=1;
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#ffffff88");bg.addColorStop(0.4,tier.color);bg.addColorStop(1,tier.glow);
  ctx.fillStyle=bg;ctx.shadowColor=tier.glow;ctx.shadowBlur=16+pulse*10;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Tier label in center
  ctx.fillStyle="#fff";ctx.font=`bold ${r*0.5}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=0;
  ctx.fillText(["C","U","R","E","L"][RAINBOW_CYCLE.indexOf(tier)]||"?",0,0);
  // Progress arc for next cycle
  ctx.globalAlpha=0.45;ctx.strokeStyle="#fff";ctx.lineWidth=2;
  ctx.beginPath();ctx.arc(0,0,r+4,-Math.PI/2,-Math.PI/2+frac*Math.PI*2);ctx.stroke();
  ctx.restore();
}

// ── Twin target — golden amber, tapping one scores both ──
function drawTwin(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.006);
  const spin=ts*0.0012;
  ctx.save();
  // Outer glow
  ctx.globalAlpha=0.3+pulse*0.2;
  ctx.strokeStyle="#f59e0b";ctx.lineWidth=3;ctx.shadowColor="#fbbf24";ctx.shadowBlur=20;
  ctx.setLineDash([6,4]);ctx.lineDashOffset=spin*50;
  ctx.beginPath();ctx.arc(0,0,r*1.45,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.globalAlpha=1;
  // Body
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#fde68a");bg.addColorStop(0.5,"#f59e0b");bg.addColorStop(1,"#b45309");
  ctx.fillStyle=bg;ctx.shadowColor="#f59e0b";ctx.shadowBlur=14+pulse*8;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // ∞ or ✦ symbol
  ctx.fillStyle="#ffffff";ctx.font=`bold ${r*0.8}px serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=0;
  ctx.fillText("✦",0,0);
  // Two small orbiting dots
  for(let i=0;i<2;i++){
    const a=spin*3+i*Math.PI;const d=r*1.25;
    ctx.fillStyle="#fde68a";ctx.globalAlpha=0.8;
    ctx.beginPath();ctx.arc(Math.cos(a)*d,Math.sin(a)*d,3.5,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

// ── Morph target — cycles through rarity tiers; catch at legendary for jackpot ──
const MORPH_CYCLE=[
  {color:"#4ade80",glow:"#16a34a",label:"C"},  // common  0-1.4s
  {color:"#60a5fa",glow:"#2563eb",label:"U"},  // uncommon
  {color:"#f472b6",glow:"#db2777",label:"R"},  // rare
  {color:"#c084fc",glow:"#7c3aed",label:"E"},  // epic
  {color:"#ffd700",glow:"#b8860b",label:"L"},  // legendary
];
function drawMorph(ctx, r, ts, spawnedAt) {
  const cycleMs=1400;
  const elapsed=Date.now()-spawnedAt;
  const phase=Math.floor((elapsed/cycleMs)%MORPH_CYCLE.length);
  const phasePct=(elapsed%cycleMs)/cycleMs;
  const tier=MORPH_CYCLE[phase];
  const nextTier=MORPH_CYCLE[(phase+1)%MORPH_CYCLE.length];
  // Blend color between phases
  const pulse=0.75+0.25*Math.sin(ts*0.012);
  const spin=ts*0.0014;
  // Outer morphing aura
  const grad=ctx.createRadialGradient(0,0,r*0.1,0,0,r*1.4);
  grad.addColorStop(0,tier.color+"cc");
  grad.addColorStop(0.6,tier.color+"55");
  grad.addColorStop(1,"transparent");
  ctx.save();
  ctx.globalAlpha=0.45*pulse;
  ctx.fillStyle=grad;
  ctx.beginPath();ctx.arc(0,0,r*1.4,0,Math.PI*2);ctx.fill();
  // Inner body — star with 5 points
  ctx.globalAlpha=1;
  ctx.rotate(spin);
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#ffffff");
  bg.addColorStop(0.35,tier.color);
  bg.addColorStop(1,tier.glow+"aa");
  ctx.fillStyle=bg;
  ctx.beginPath();
  const pts=5,outer=r,inner=r*0.48;
  for(let i=0;i<pts*2;i++){
    const rad=i%2===0?outer:inner;
    const ang=(i*Math.PI/pts)-Math.PI/2;
    i===0?ctx.moveTo(Math.cos(ang)*rad,Math.sin(ang)*rad):ctx.lineTo(Math.cos(ang)*rad,Math.sin(ang)*rad);
  }
  ctx.closePath();ctx.fill();
  ctx.strokeStyle=tier.color;ctx.lineWidth=1.5;ctx.shadowColor=tier.glow;ctx.shadowBlur=10+pulse*10;ctx.stroke();
  ctx.restore();
  // Tier label
  ctx.save();
  ctx.font=`bold ${Math.floor(r*0.7)}px 'Exo 2',sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillStyle="#ffffff";ctx.shadowColor=tier.glow;ctx.shadowBlur=8;
  ctx.fillText(tier.label,0,0);
  // Phase progress ring
  ctx.restore();
  ctx.save();
  const ringR=r+3.5,circ=2*Math.PI*ringR;
  ctx.strokeStyle=nextTier.color;ctx.lineWidth=2;ctx.globalAlpha=0.6;
  ctx.shadowColor=nextTier.glow;ctx.shadowBlur=6;
  ctx.beginPath();ctx.arc(0,0,ringR,-Math.PI/2,-Math.PI/2+phasePct*Math.PI*2);ctx.stroke();
  ctx.restore();
}

// ── Gemstone target — prismatic gem with rainbow light refraction ──
function drawGemstone(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.006);
  const spin=ts*0.0008;
  // Rainbow color cycling
  const hue=(ts*0.05)%360;
  const hue2=(hue+120)%360;
  const hue3=(hue+240)%360;
  ctx.save();
  // Outer rainbow aura
  ctx.globalAlpha=0.2+pulse*0.2;
  const ag=ctx.createConicalGradient?null:null; // fallback — use simple glow
  ctx.strokeStyle=`hsl(${hue},100%,70%)`;ctx.lineWidth=4.5;
  ctx.shadowColor=`hsl(${hue},100%,60%)`;ctx.shadowBlur=28+pulse*18;
  ctx.beginPath();ctx.arc(0,0,r*1.3,0,Math.PI*2);ctx.stroke();
  // Diamond octagon shape
  ctx.globalAlpha=1;
  const sides=8;
  const gg=ctx.createLinearGradient(-r,-r,r,r);
  gg.addColorStop(0,`hsl(${hue},90%,75%)`);gg.addColorStop(0.33,`hsl(${hue2},90%,70%)`);
  gg.addColorStop(0.66,`hsl(${hue3},90%,75%)`);gg.addColorStop(1,`hsl(${hue},90%,80%)`);
  ctx.fillStyle=gg;ctx.shadowColor=`hsl(${hue2},100%,65%)`;ctx.shadowBlur=18;
  ctx.beginPath();
  for(let i=0;i<sides;i++){
    const a=spin+i*(Math.PI*2/sides);const scaledR=r*(i%2===0?1.0:0.72);
    if(i===0)ctx.moveTo(Math.cos(a)*scaledR,Math.sin(a)*scaledR);
    else ctx.lineTo(Math.cos(a)*scaledR,Math.sin(a)*scaledR);
  }
  ctx.closePath();ctx.fill();
  // Inner facet lines
  ctx.globalAlpha=0.45+pulse*0.2;ctx.strokeStyle="#ffffff";ctx.lineWidth=1;ctx.shadowBlur=0;
  for(let i=0;i<4;i++){
    const a=spin+i*(Math.PI/2);
    ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*r*0.75,Math.sin(a)*r*0.75);ctx.stroke();
  }
  // Bright center glint
  ctx.globalAlpha=0.85+pulse*0.12;ctx.fillStyle="#ffffff";ctx.shadowColor="#fff";ctx.shadowBlur=12;
  ctx.beginPath();ctx.arc(-r*0.2,-r*0.25,r*0.12,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

// ── Loot Chest — golden chest with coin sparkles, drops 3-5 coins ──
function drawLootChest(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  const shake=Math.sin(ts*0.022)*1.5;
  ctx.save();
  ctx.translate(shake,0);
  // Outer golden glow
  ctx.globalAlpha=0.35+pulse*0.3;
  ctx.fillStyle="#ffd700";ctx.shadowColor="#ffd700";ctx.shadowBlur=22+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r*1.45,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;
  // Chest body (rounded rect)
  const bw=r*1.4,bh=r*1.0;
  ctx.shadowColor="#b45309";ctx.shadowBlur=8;
  const bg=ctx.createLinearGradient(0,-bh/2,0,bh/2);
  bg.addColorStop(0,"#fde68a");bg.addColorStop(0.45,"#f59e0b");bg.addColorStop(1,"#92400e");
  ctx.fillStyle=bg;
  ctx.beginPath();ctx.roundRect(-bw/2,-bh/2,bw,bh,4);ctx.fill();
  // Lid
  const lidGrad=ctx.createLinearGradient(0,-bh/2,0,-bh/2+bh*0.35);
  lidGrad.addColorStop(0,"#fef3c7");lidGrad.addColorStop(1,"#d97706");
  ctx.fillStyle=lidGrad;ctx.beginPath();ctx.roundRect(-bw/2,-bh/2,bw,bh*0.35,4);ctx.fill();
  // Lid line
  ctx.strokeStyle="#7c2d12";ctx.lineWidth=1.5;ctx.shadowBlur=0;
  ctx.beginPath();ctx.moveTo(-bw/2,-bh*0.15);ctx.lineTo(bw/2,-bh*0.15);ctx.stroke();
  // Lock clasp
  ctx.fillStyle="#ffd700";ctx.shadowColor="#ffd700";ctx.shadowBlur=6+pulse*4;
  ctx.beginPath();ctx.arc(0,-bh*0.13,4,0,Math.PI*2);ctx.fill();
  ctx.strokeStyle="#b45309";ctx.lineWidth=1.5;ctx.shadowBlur=0;
  ctx.beginPath();ctx.arc(0,-bh*0.13,4,0,Math.PI*2);ctx.stroke();
  // Coin sparkles
  const coinAngles=[0,Math.PI*0.6,Math.PI*1.4];
  coinAngles.forEach((a,i)=>{
    const oa=a+ts*0.002+i*0.8;
    const od=r*(0.9+0.3*Math.sin(ts*0.006+i));
    const px=Math.cos(oa)*od,py=Math.sin(oa)*od;
    ctx.globalAlpha=(0.5+0.5*Math.sin(ts*0.008+i))*0.8;
    ctx.fillStyle="#ffd700";ctx.shadowColor="#ffd700";ctx.shadowBlur=8;
    ctx.font=`bold ${r*0.38}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🪙",px,py);
  });
  ctx.restore();
}

// ── Bubble target — large translucent soap bubble, generous hit zone ──
function drawBubble(ctx, r, ts) {
  const shimmer=0.5+0.5*Math.sin(ts*0.006);
  const drift=Math.sin(ts*0.0045)*2;
  ctx.save();
  ctx.translate(0,drift);
  // Outer translucent bubble
  ctx.globalAlpha=0.12+shimmer*0.08;
  ctx.fillStyle="#e0f7ff";ctx.shadowColor="#67e8f9";ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(0,0,r*1.25,0,Math.PI*2);ctx.fill();
  // Iridescent rim ring
  ctx.globalAlpha=0.5+shimmer*0.3;
  const rimGrad=ctx.createLinearGradient(-r,-r,r,r);
  rimGrad.addColorStop(0,"#f472b6");rimGrad.addColorStop(0.25,"#67e8f9");
  rimGrad.addColorStop(0.5,"#c084fc");rimGrad.addColorStop(0.75,"#4ade80");rimGrad.addColorStop(1,"#fbbf24");
  ctx.strokeStyle=rimGrad;ctx.lineWidth=3.5;ctx.shadowColor="#60a5fa";ctx.shadowBlur=10;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.stroke();
  // Inner sheen (half-moon highlight)
  ctx.globalAlpha=0.35+shimmer*0.2;
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  ctx.beginPath();ctx.ellipse(-r*0.28,-r*0.32,r*0.38,r*0.22,Math.PI*0.35,0,Math.PI*2);ctx.fill();
  // Small secondary highlight
  ctx.globalAlpha=0.25;
  ctx.beginPath();ctx.ellipse(r*0.2,r*0.3,r*0.12,r*0.07,Math.PI*0.1,0,Math.PI*2);ctx.fill();
  ctx.restore();
}

// ── Rage target — grows angrier (red, faster) the longer it lives ──
function drawRage(ctx, r, ts, rageLevel) {
  const rl=Math.min(1,rageLevel||0); // 0=calm, 1=max rage
  const pulse=0.5+0.5*Math.sin(ts*0.01*(1+rl*3));
  const shake=rl>0.5?Math.sin(ts*0.04)*2.5*rl:0;
  ctx.save();ctx.translate(shake,0);
  // Outer aura — grows redder with rage
  ctx.globalAlpha=0.2+rl*0.35;
  const auraColor=rl<0.5?`rgba(251,146,60,${0.5+pulse*0.3})`:`rgba(239,68,68,${0.5+pulse*0.3})`;
  ctx.fillStyle=auraColor;ctx.shadowColor=rl<0.5?"#fb923c":"#ef4444";ctx.shadowBlur=20+rl*28;
  ctx.beginPath();ctx.arc(0,0,r*(1.2+rl*0.35),0,Math.PI*2);ctx.fill();
  // Core body — orange to red gradient
  ctx.globalAlpha=1;
  const cg=ctx.createRadialGradient(0,0,0,0,0,r);
  const innerColor=rl<0.5?`rgba(251,113,133,${0.9+pulse*0.08})`:`rgba(220,38,38,${0.9+pulse*0.08})`;
  const outerColor=rl<0.5?"rgba(239,68,68,0.85)":"rgba(127,29,29,0.85)";
  cg.addColorStop(0,innerColor);cg.addColorStop(1,outerColor);
  ctx.fillStyle=cg;ctx.shadowColor=rl<0.5?"#f97316":"#dc2626";ctx.shadowBlur=12+rl*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Rage veins (jagged lines radiating out)
  if(rl>0.3){
    ctx.globalAlpha=(rl-0.3)*0.8+0.1;ctx.strokeStyle="#fca5a5";ctx.lineWidth=1.2;ctx.shadowBlur=4;
    for(let i=0;i<Math.floor(3+rl*5);i++){
      const angle=(i/8)*Math.PI*2+ts*0.002;
      const inner=r*0.45;const outer=r*0.82;
      ctx.beginPath();ctx.moveTo(Math.cos(angle)*inner,Math.sin(angle)*inner);
      ctx.lineTo(Math.cos(angle+0.25)*outer,Math.sin(angle+0.25)*outer);ctx.stroke();
    }
  }
  // Rage face (👿 emoji approximation)
  ctx.globalAlpha=0.85+rl*0.1;ctx.fillStyle="#fff";ctx.shadowBlur=0;
  ctx.font=`bold ${Math.round(r*0.7)}px sans-serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText(rl>0.6?"😡":rl>0.3?"😠":"😤",0,0);
  ctx.restore();
}

// ── Crystal target — hexagonal gem that shatters into 3 scoreable shards ──
function drawCrystalTarget(ctx, r, ts) {
  const spin=ts*0.0012;const pulse=0.5+0.5*Math.sin(ts*0.006);
  ctx.save();
  // Outer glow halo
  ctx.globalAlpha=0.2+pulse*0.18;ctx.shadowColor="#60a5fa";ctx.shadowBlur=28+pulse*18;
  ctx.strokeStyle="#93c5fd";ctx.lineWidth=3.5;
  ctx.beginPath();for(let i=0;i<6;i++){const a=spin+i*Math.PI/3;const x2=Math.cos(a)*(r*1.35),y2=Math.sin(a)*(r*1.35);i===0?ctx.moveTo(x2,y2):ctx.lineTo(x2,y2);}ctx.closePath();ctx.stroke();
  // Crystal body hexagon
  ctx.globalAlpha=1;
  const hexGrad=ctx.createLinearGradient(-r,-r,r,r);
  hexGrad.addColorStop(0,"rgba(191,219,254,0.95)");hexGrad.addColorStop(0.4,"rgba(96,165,250,0.85)");hexGrad.addColorStop(1,"rgba(37,99,235,0.8)");
  ctx.fillStyle=hexGrad;ctx.shadowColor="#60a5fa";ctx.shadowBlur=16;
  ctx.beginPath();for(let i=0;i<6;i++){const a=spin+i*Math.PI/3;const x2=Math.cos(a)*r*1.0,y2=Math.sin(a)*r*1.0;i===0?ctx.moveTo(x2,y2):ctx.lineTo(x2,y2);}ctx.closePath();ctx.fill();
  // Facet lines — inner reflections
  ctx.globalAlpha=0.35+pulse*0.2;ctx.strokeStyle="#dbeafe";ctx.lineWidth=1;ctx.shadowBlur=0;
  for(let i=0;i<6;i++){const a=spin+i*Math.PI/3;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*r*0.85,Math.sin(a)*r*0.85);ctx.stroke();}
  // Bright glint
  ctx.globalAlpha=0.7+pulse*0.25;ctx.fillStyle="#eff6ff";ctx.shadowColor="#ffffff";ctx.shadowBlur=8;
  ctx.beginPath();ctx.arc(-r*0.25,-r*0.3,r*0.15,0,Math.PI*2);ctx.fill();
  ctx.restore();
}
function drawCrystalShard(ctx, r, ts, bornAt) {
  const age=performance.now()-(bornAt||performance.now());
  const life=Math.max(0,1-age/2000);if(life<=0)return;
  const spin=ts*0.004;
  ctx.save();ctx.globalAlpha=life*0.9;
  const sg=ctx.createLinearGradient(-r,-r,r,r);
  sg.addColorStop(0,"rgba(219,234,254,0.95)");sg.addColorStop(1,"rgba(96,165,250,0.8)");
  ctx.fillStyle=sg;ctx.shadowColor="#60a5fa";ctx.shadowBlur=10*life;
  ctx.beginPath();ctx.moveTo(0,-r);ctx.lineTo(r*0.6,r*0.6);ctx.lineTo(-r*0.6,r*0.6);ctx.closePath();ctx.fill();
  ctx.globalAlpha=life*0.55;ctx.strokeStyle="#bfdbfe";ctx.lineWidth=1.2;ctx.stroke();
  ctx.restore();
}

// ── Echo target — leaves a ghost echo on tap; tap the echo for bonus ──
function drawEcho(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.008);
  const spin=ts*0.0018;
  ctx.save();
  // Outer echo rings
  for(let ring=0;ring<3;ring++){
    const rr=r*(0.6+ring*0.35);
    const phase=ring*(Math.PI*2/3)+spin;
    ctx.globalAlpha=(0.18+pulse*0.14)*(1-ring*0.25);
    ctx.strokeStyle="#a78bfa";ctx.lineWidth=2.5-ring*0.5;ctx.shadowColor="#7c3aed";ctx.shadowBlur=12;
    ctx.setLineDash([Math.PI*rr/4,Math.PI*rr/4]);ctx.lineDashOffset=phase*rr;
    ctx.beginPath();ctx.arc(0,0,rr,0,Math.PI*2);ctx.stroke();
  }
  ctx.setLineDash([]);ctx.globalAlpha=1;
  // Core — translucent violet orb
  const cg=ctx.createRadialGradient(0,0,0,0,0,r*0.52);
  cg.addColorStop(0,`rgba(196,181,253,${0.85+pulse*0.12})`);
  cg.addColorStop(0.6,`rgba(139,92,246,${0.7+pulse*0.1})`);
  cg.addColorStop(1,"rgba(91,33,182,0.55)");
  ctx.fillStyle=cg;ctx.shadowColor="#7c3aed";ctx.shadowBlur=22+pulse*14;
  ctx.beginPath();ctx.arc(0,0,r*0.52,0,Math.PI*2);ctx.fill();
  // Echo symbol — two overlapping circles
  ctx.globalAlpha=0.55+pulse*0.25;ctx.strokeStyle="#e9d5ff";ctx.lineWidth=1.5;ctx.shadowBlur=4;
  ctx.beginPath();ctx.arc(-r*0.14,0,r*0.22,0,Math.PI*2);ctx.stroke();
  ctx.beginPath();ctx.arc(r*0.14,0,r*0.22,0,Math.PI*2);ctx.stroke();
  ctx.restore();
}
// ── Echo Ghost — fading afterimage of an echo tap ──
function drawEchoGhost(ctx, r, ts, bornAt) {
  const age=ts-(bornAt||ts);
  const life=Math.max(0,1-age/1500);
  if(life<=0)return;
  ctx.save();
  ctx.globalAlpha=life*0.55;
  ctx.strokeStyle="#c4b5fd";ctx.lineWidth=3;ctx.shadowColor="#7c3aed";ctx.shadowBlur=18*life;
  ctx.setLineDash([8,6]);
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);
  ctx.globalAlpha=life*0.3;
  ctx.fillStyle="#a78bfa";
  ctx.beginPath();ctx.arc(0,0,r*0.5,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=life*0.75;ctx.fillStyle="#e9d5ff";ctx.font=`bold ${Math.round(r*0.55)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("◎",0,0);
  ctx.restore();
}

// ── Tornado target — blue spinning vortex, scrambles nearby target positions ──
function drawTornado(ctx, r, ts) {
  const spin=ts*0.003;
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  ctx.save();
  // Outer wind halo
  ctx.globalAlpha=0.22+pulse*0.2;
  ctx.strokeStyle="#67e8f9";ctx.lineWidth=4;ctx.shadowColor="#06b6d4";ctx.shadowBlur=22+pulse*14;
  ctx.beginPath();ctx.arc(0,0,r*1.55,0,Math.PI*2);ctx.stroke();
  ctx.globalAlpha=1;
  // Spiral arms (3)
  for(let arm=0;arm<3;arm++){
    const armAngle=spin+arm*(Math.PI*2/3);
    ctx.globalAlpha=0.7;ctx.strokeStyle="#67e8f9";ctx.lineWidth=2;
    ctx.shadowColor="#06b6d4";ctx.shadowBlur=10;
    ctx.beginPath();
    for(let i=0;i<24;i++){
      const t2=i/23;
      const a=armAngle+t2*Math.PI*1.8;
      const rd=r*0.12+t2*r*0.82;
      if(i===0)ctx.moveTo(Math.cos(a)*rd,Math.sin(a)*rd);
      else ctx.lineTo(Math.cos(a)*rd,Math.sin(a)*rd);
    }
    ctx.stroke();
  }
  ctx.globalAlpha=1;
  // Core
  const cg=ctx.createRadialGradient(0,0,0,0,0,r*0.55);
  cg.addColorStop(0,"#e0f7ff");cg.addColorStop(0.4,"#67e8f9");cg.addColorStop(1,"#0891b2");
  ctx.fillStyle=cg;ctx.shadowColor="#06b6d4";ctx.shadowBlur=14;
  ctx.beginPath();ctx.arc(0,0,r*0.55,0,Math.PI*2);ctx.fill();
  // Eye symbol
  ctx.fillStyle="#ffffff";ctx.font=`bold ${r*0.55}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.shadowBlur=0;ctx.globalAlpha=0.85;
  ctx.fillText("🌀",0,1);
  ctx.restore();
}

// ── Healer target — glowing green cross, restores 1 life when tapped ──
function drawHealer(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.005);
  ctx.save();
  // Outer healing glow
  const grad=ctx.createRadialGradient(0,0,r*0.4,0,0,r*1.6);
  grad.addColorStop(0,"#34d39944");grad.addColorStop(1,"transparent");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r*1.6,0,Math.PI*2);ctx.fill();
  // Body
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#6ee7b7");bg.addColorStop(0.55,"#34d399");bg.addColorStop(1,"#059669");
  ctx.fillStyle=bg;ctx.shadowColor="#34d399";ctx.shadowBlur=18+pulse*10;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Cross symbol
  ctx.fillStyle="#ffffff";ctx.shadowBlur=0;
  const arm=r*0.45,thick=r*0.22;
  ctx.beginPath();ctx.roundRect(-thick/2,-arm,thick,arm*2,thick/4);ctx.fill();
  ctx.beginPath();ctx.roundRect(-arm,-thick/2,arm*2,thick,thick/4);ctx.fill();
  // Sparkle particles around it
  for(let i=0;i<4;i++){
    const a=(i/4)*Math.PI*2+ts*0.002;const d=r*1.2;
    ctx.fillStyle="#a7f3d0";ctx.globalAlpha=0.6+0.4*Math.sin(ts*0.008+i);
    ctx.beginPath();ctx.arc(Math.cos(a)*d,Math.sin(a)*d,2.5,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
}

// ── Volatile target — pulsing bomb-like, explodes on expiry ──
function drawVolatile(ctx, r, ts, lifeRatio) {
  const urgency=1-lifeRatio; // 0=fresh, 1=about to explode
  const pulse=0.5+0.5*Math.sin(ts*0.008*(1+urgency*4));
  const sz=r*(1+urgency*0.25+pulse*0.08);
  ctx.save();
  // Outer explosive ring
  ctx.globalAlpha=0.4+urgency*0.4;
  ctx.strokeStyle=`hsl(${20-urgency*20},100%,50%)`;
  ctx.lineWidth=2+urgency*2;ctx.shadowColor="#ff4500";ctx.shadowBlur=18+urgency*20;
  ctx.beginPath();ctx.arc(0,0,sz*1.4,0,Math.PI*2);ctx.stroke();
  // Body gradient
  ctx.globalAlpha=1;
  const bg=ctx.createRadialGradient(0,0,0,0,0,sz);
  const hue=20-urgency*20;
  bg.addColorStop(0,`hsl(${hue+30},100%,70%)`);
  bg.addColorStop(0.5,`hsl(${hue},100%,50%)`);
  bg.addColorStop(1,`hsl(${hue-15},100%,30%)`);
  ctx.fillStyle=bg;ctx.shadowColor=`hsl(${hue},100%,50%)`;ctx.shadowBlur=16+urgency*12;
  ctx.beginPath();ctx.arc(0,0,sz,0,Math.PI*2);ctx.fill();
  // ⚠ warning icon
  ctx.fillStyle="#fff";ctx.font=`bold ${sz*0.85}px serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("💣",0,0);
  // Timer ring
  ctx.globalAlpha=0.7;ctx.strokeStyle="#ffffff";ctx.lineWidth=2.5;
  ctx.shadowBlur=0;ctx.beginPath();
  ctx.arc(0,0,sz+4,-Math.PI/2,-Math.PI/2+lifeRatio*Math.PI*2);ctx.stroke();
  ctx.restore();
}

// ── Phantom target — ultra-short lifetime, huge points, ghostly flicker ──
function drawPhantom(ctx, r, ts, lifeRatio) {
  // Flicker faster as time runs out
  const flicker=lifeRatio>0.4?1:0.4+0.6*Math.abs(Math.sin(ts*0.04*(1-lifeRatio+0.5)));
  const pulse=0.4+0.6*Math.sin(ts*0.009);
  ctx.save();
  ctx.globalAlpha=flicker*0.85*(0.5+0.5*lifeRatio);
  // Outer glow ring
  const grad=ctx.createRadialGradient(0,0,r*0.3,0,0,r*1.5);
  grad.addColorStop(0,"#e879f988");grad.addColorStop(1,"transparent");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.fill();
  // Body
  const bg=ctx.createRadialGradient(0,0,0,0,0,r);
  bg.addColorStop(0,"#f0abfc");bg.addColorStop(0.6,"#e879f9");bg.addColorStop(1,"#a21caf");
  ctx.fillStyle=bg;
  ctx.shadowColor="#e879f9";ctx.shadowBlur=20+pulse*12;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Ghost symbol (∞)
  ctx.globalAlpha*=0.9;ctx.fillStyle="#ffffff";ctx.font=`bold ${r*0.8}px serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText("👻",0,0);
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

// ── Voltage target — electric orb; chain-zaps 3 nearby targets when tapped ──
function drawVoltage(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.009);
  // Outer electric field
  const outerGrd=ctx.createRadialGradient(0,0,r*0.4,0,0,r*1.6);
  outerGrd.addColorStop(0,"#facc1544");outerGrd.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=0.5*pulse;ctx.fillStyle=outerGrd;
  ctx.beginPath();ctx.arc(0,0,r*1.6,0,Math.PI*2);ctx.fill();ctx.restore();
  // Lightning arcs around border
  for(let i=0;i<6;i++){
    const a=(i/6)*Math.PI*2+ts*0.003;
    const jitter=(Math.sin(ts*0.04+i*1.7)*0.25);
    const x1=Math.cos(a)*r*0.7,y1=Math.sin(a)*r*0.7;
    const x2=Math.cos(a+jitter)*r*1.1,y2=Math.sin(a+jitter)*r*1.1;
    ctx.save();ctx.strokeStyle="#facc15";ctx.lineWidth=1.5;ctx.globalAlpha=0.7*pulse;
    ctx.shadowColor="#fbbf24";ctx.shadowBlur=8;
    ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();ctx.restore();
  }
  // Core gradient
  const grd=ctx.createRadialGradient(0,0,0,0,0,r);
  grd.addColorStop(0,"#fef08a");grd.addColorStop(0.5,"#fbbf24");grd.addColorStop(1,"#b45309");
  ctx.save();ctx.shadowColor="#fbbf24";ctx.shadowBlur=18+10*pulse;
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // ⚡ symbol
  ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(r*0.9)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.95;
  ctx.fillText("⚡",0,1);ctx.restore();
}

// ── Lucky Clover — 4-leaf clover; gives random 1-10× score multiplier on tap ──
function drawLuckyClover(ctx, r, ts) {
  const pulse=0.8+0.2*Math.sin(ts*0.008);
  // Glow aura
  const auraGrd=ctx.createRadialGradient(0,0,r*0.3,0,0,r*1.5);
  auraGrd.addColorStop(0,"#4ade8033");auraGrd.addColorStop(1,"transparent");
  ctx.save();ctx.globalAlpha=pulse;ctx.fillStyle=auraGrd;
  ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.fill();ctx.restore();
  // 4 leaf circles
  const leafColors=["#22c55e","#16a34a","#4ade80","#15803d"];
  const angles=[0,Math.PI/2,Math.PI,3*Math.PI/2];
  const leafR=r*0.48;const leafOff=r*0.38;
  angles.forEach((a,i)=>{
    const lx=Math.cos(a)*leafOff,ly=Math.sin(a)*leafOff;
    ctx.save();ctx.translate(lx,ly);
    const grd=ctx.createRadialGradient(0,0,0,0,0,leafR);
    grd.addColorStop(0,"#86efac");grd.addColorStop(1,leafColors[i]);
    ctx.fillStyle=grd;ctx.shadowColor="#22c55e";ctx.shadowBlur=8*pulse;
    ctx.beginPath();ctx.arc(0,0,leafR,0,Math.PI*2);ctx.fill();
    ctx.restore();
  });
  // Center hub
  ctx.save();ctx.fillStyle="#166534";ctx.shadowColor="#15803d";ctx.shadowBlur=6;
  ctx.beginPath();ctx.arc(0,0,r*0.18,0,Math.PI*2);ctx.fill();
  // Lucky sparkles
  for(let i=0;i<3;i++){
    const sa=(i/3)*Math.PI*2+ts*0.005;
    const sd=r*(0.9+0.15*Math.sin(ts*0.012+i));
    ctx.fillStyle=`hsl(${140+i*20},90%,70%)`;ctx.globalAlpha=0.7*pulse;
    ctx.beginPath();ctx.arc(Math.cos(sa)*sd,Math.sin(sa)*sd,2.5,0,Math.PI*2);ctx.fill();
  }
  ctx.restore();
  ctx.save();ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(r*0.55)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.9;
  ctx.shadowColor="#22c55e";ctx.shadowBlur=6;
  ctx.fillText("🍀",0,1);ctx.restore();
}

// ── Void target — swirling dark orb; absorbs nearby targets for bonus pts ──
function drawVoid(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  // Gravity distortion rings
  for(let i=3;i>0;i--){
    ctx.save();ctx.strokeStyle=`hsl(${270+i*10},80%,${30+i*8}%)`;
    ctx.lineWidth=1;ctx.globalAlpha=(0.1+i*0.07)*pulse;
    ctx.beginPath();ctx.arc(0,0,r*(0.9+i*0.35),0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  // Swirling spiral arms
  for(let arm=0;arm<3;arm++){
    ctx.save();ctx.strokeStyle=`hsl(${280+arm*30},90%,70%)`;
    ctx.lineWidth=2;ctx.globalAlpha=0.5*pulse;ctx.shadowColor="#a855f7";ctx.shadowBlur=8;
    ctx.beginPath();
    for(let s=0;s<40;s++){
      const angle=(s/40)*Math.PI*2*1.8+(arm/3)*Math.PI*2-ts*0.005;
      const rad=(s/40)*r*0.85;
      if(s===0)ctx.moveTo(Math.cos(angle)*rad,Math.sin(angle)*rad);
      else ctx.lineTo(Math.cos(angle)*rad,Math.sin(angle)*rad);
    }
    ctx.stroke();ctx.restore();
  }
  // Dark core
  const grd=ctx.createRadialGradient(0,0,0,0,0,r);
  grd.addColorStop(0,"#1e1b4b");grd.addColorStop(0.6,"#4c1d95");grd.addColorStop(1,"#7c3aed88");
  ctx.save();ctx.shadowColor="#a855f7";ctx.shadowBlur=20+8*pulse;
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // ◈ eye symbol
  ctx.fillStyle="#e9d5ff";ctx.font=`bold ${Math.round(r*0.85)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.9;
  ctx.fillText("🌀",0,1);ctx.restore();
}

// ── Thunderbolt — lightning bolt falling from top; tap fast or lose a life ──
function drawThunderbolt(ctx,r,ts){
  const pulse=0.7+0.3*Math.abs(Math.sin(ts*0.02));
  ctx.save();
  ctx.shadowBlur=20*pulse;ctx.shadowColor="#facc15";
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#fef08a");grad.addColorStop(0.5,"#facc15");grad.addColorStop(1,"#78350f");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Lightning bolt shape
  ctx.strokeStyle="#ffffff";ctx.lineWidth=2;ctx.globalAlpha=0.9*pulse;
  ctx.beginPath();
  ctx.moveTo(r*0.15,-r*0.6);ctx.lineTo(-r*0.1,-r*0.05);ctx.lineTo(r*0.25,-r*0.05);
  ctx.lineTo(-r*0.15,r*0.6);ctx.lineTo(r*0.05,r*0.1);ctx.lineTo(-r*0.2,r*0.1);
  ctx.closePath();ctx.fillStyle="#fef9c3";ctx.fill();
  ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.78)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("⚡",0,0);ctx.restore();
}
// ── Gravity Orb — pulls normal targets; tap to score + release them ──
function drawGravityOrb(ctx,r,ts){
  const spin=ts*0.0015;
  ctx.save();
  ctx.shadowBlur=24;ctx.shadowColor="#7c3aed";
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#a78bfa");grad.addColorStop(0.6,"#6d28d9");grad.addColorStop(1,"#1e1b4b");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Orbiting rings
  for(let i=0;i<2;i++){
    ctx.save();ctx.rotate(spin+(i*Math.PI));
    ctx.strokeStyle=`rgba(167,139,250,${0.35+i*0.1})`;ctx.lineWidth=1.5;
    ctx.beginPath();ctx.ellipse(0,0,r*0.92,r*0.3,0,0,Math.PI*2);ctx.stroke();
    ctx.restore();
  }
  // Gravity waves
  ctx.globalAlpha=0.25;ctx.strokeStyle="#a78bfa";ctx.lineWidth=1;
  for(let i=1;i<=3;i++){ctx.beginPath();ctx.arc(0,0,r*(0.6+i*0.22),0,Math.PI*2);ctx.stroke();}
  ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.88)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("🌐",0,0);ctx.restore();
}
// ── Crystal Ball — predicts next target rarity; guaranteed lucky spawn after tap ──
function drawCrystalBall(ctx,r,ts){
  const glow=0.5+0.5*Math.sin(ts*0.005);
  const hue=(ts*0.04)%360;
  ctx.save();
  ctx.shadowBlur=20+10*glow;ctx.shadowColor=`hsl(${hue},100%,70%)`;
  const grad=ctx.createRadialGradient(-r*0.25,-r*0.25,r*0.05,0,0,r);
  grad.addColorStop(0,"rgba(255,255,255,0.9)");
  grad.addColorStop(0.3,`hsla(${hue},80%,70%,0.6)`);
  grad.addColorStop(0.7,`hsla(${(hue+60)%360},100%,40%,0.7)`);
  grad.addColorStop(1,`hsla(${(hue+120)%360},100%,20%,0.8)`);
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Swirling inner mist
  ctx.save();ctx.rotate(ts*0.0008);
  ctx.globalAlpha=0.3*glow;ctx.strokeStyle=`hsl(${hue},100%,90%)`;ctx.lineWidth=1.5;
  ctx.beginPath();ctx.arc(0,0,r*0.45,0,Math.PI*1.5);ctx.stroke();
  ctx.restore();
  // Stand base
  ctx.globalAlpha=0.5;ctx.fillStyle="#4a3728";
  ctx.beginPath();ctx.ellipse(0,r*0.85,r*0.5,r*0.12,0,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.82)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("🔮",0,0);ctx.restore();
}
// ── Firefly — tiny, fast, flickering; hard to hit, big points ──
function drawFirefly(ctx,r,ts){
  const flicker=0.65+0.35*Math.sin(ts*0.012);
  ctx.save();
  ctx.shadowBlur=18*flicker;ctx.shadowColor="#84ef63";
  const grad=ctx.createRadialGradient(0,0,0,0,0,r);
  grad.addColorStop(0,"#ffffff");grad.addColorStop(0.3,"#bbf7d0");grad.addColorStop(1,"#22c55e00");
  ctx.globalAlpha=flicker;ctx.fillStyle=grad;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  const wf=Math.sin(ts*0.018)*0.35;
  ctx.globalAlpha=0.35*flicker;ctx.fillStyle="#bbf7d0";
  ctx.beginPath();ctx.ellipse(-r*0.55,-r*0.1,r*0.65,r*0.25+wf*r*0.15,-0.4,0,Math.PI*2);ctx.fill();
  ctx.beginPath();ctx.ellipse(r*0.55,-r*0.1,r*0.65,r*0.25+wf*r*0.15,0.4,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.88)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("✨",0,0);ctx.restore();
}
// ── Geode — rocky shell; first tap cracks open, second collects the gem ──
function drawGeode(ctx,r,ts,cracked){
  ctx.save();
  if(!cracked){
    ctx.shadowBlur=8;ctx.shadowColor="#94a3b8";ctx.fillStyle="#475569";
    ctx.beginPath();
    const sides=7;
    for(let i=0;i<sides;i++){
      const a=(i/sides)*Math.PI*2;const j=0.78+0.22*Math.sin(i*3.7+ts*0.001);
      const px=Math.cos(a)*r*j,py=Math.sin(a)*r*j;
      i===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
    }
    ctx.closePath();ctx.fill();
    ctx.strokeStyle="#94a3b8";ctx.lineWidth=1.5;ctx.globalAlpha=0.6;
    ctx.beginPath();ctx.moveTo(-r*0.3,-r*0.5);ctx.lineTo(r*0.1,r*0.2);ctx.lineTo(-r*0.1,r*0.6);ctx.stroke();
    ctx.beginPath();ctx.moveTo(r*0.2,-r*0.4);ctx.lineTo(-r*0.1,r*0.1);ctx.stroke();
    ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.78)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("🪨",0,0);
  } else {
    const hue=(ts*0.08)%360;
    ctx.shadowBlur=22;ctx.shadowColor=`hsl(${hue},100%,70%)`;
    const grad=ctx.createRadialGradient(0,0,0,0,0,r);
    grad.addColorStop(0,"#ffffff");grad.addColorStop(0.4,`hsl(${hue},100%,75%)`);
    grad.addColorStop(1,`hsl(${(hue+120)%360},100%,40%)`);
    ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
    ctx.strokeStyle="#ffffff";ctx.lineWidth=1;ctx.globalAlpha=0.45;
    for(let i=0;i<6;i++){const a=(i/6)*Math.PI*2;ctx.beginPath();ctx.moveTo(0,0);ctx.lineTo(Math.cos(a)*r,Math.sin(a)*r);ctx.stroke();}
    ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.88)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
    ctx.fillText("💎",0,0);
  }
  ctx.restore();
}
// ── Time Bomb — ticking target; tap to defuse or it detonates (−2 lives) ──
function drawTimeBomb(ctx,r,ts,secondsLeft){
  const urgency=secondsLeft!==undefined?Math.max(0,Math.min(1,1-secondsLeft/3)):0.5;
  const pulse=0.85+0.15*Math.sin(ts*(0.008+urgency*0.025));
  ctx.save();
  ctx.shadowBlur=12+urgency*22;ctx.shadowColor=urgency>0.6?"#ef4444":"#f97316";
  const grad=ctx.createRadialGradient(0,0,0,0,0,r*pulse);
  grad.addColorStop(0,urgency>0.6?"#fca5a5":"#fed7aa");
  grad.addColorStop(0.5,urgency>0.6?"#ef4444":"#f97316");
  grad.addColorStop(1,"#111111");
  ctx.fillStyle=grad;ctx.beginPath();ctx.arc(0,0,r*pulse,0,Math.PI*2);ctx.fill();
  const segs=Math.max(1,Math.round(secondsLeft!==undefined?secondsLeft*3:8));
  ctx.strokeStyle=urgency>0.6?"#ef4444":"#fbbf24";ctx.lineWidth=2.5;ctx.globalAlpha=0.8;
  for(let i=0;i<segs;i++){
    const a=(i/9)*Math.PI*2-Math.PI/2;const a2=((i+0.72)/9)*Math.PI*2-Math.PI/2;
    ctx.beginPath();ctx.arc(0,0,r*0.82,a,a2);ctx.stroke();
  }
  ctx.globalAlpha=1;ctx.font=`${Math.round(r*0.88)}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("💣",0,0);ctx.restore();
}
// ── Motion trail + ghost afterimages for moving targets ──
// ── Spectral target — phasing ghost orb; massive pts if caught while visible ──
function drawSpectral(ctx, r, ts) {
  const cycle=1600;const phase=(ts%cycle)/cycle; // 0→1 fade in, then 0 fade out
  const vis=phase<0.5?phase*2:2-phase*2; // triangle wave: 0→1→0
  const pulse=0.5+0.5*Math.sin(ts*0.008);
  // Spectral shimmer aura
  ctx.save();ctx.globalAlpha=vis*0.3*pulse;
  ctx.fillStyle="#e0e7ff";ctx.shadowColor="#818cf8";ctx.shadowBlur=20;
  ctx.beginPath();ctx.arc(0,0,r*1.5,0,Math.PI*2);ctx.fill();
  // Body — fades in and out
  const grd=ctx.createRadialGradient(0,0,0,0,0,r);
  grd.addColorStop(0,"#e0e7ff");grd.addColorStop(0.4,"#a5b4fc");grd.addColorStop(1,"#3730a3");
  ctx.globalAlpha=vis*0.9;ctx.fillStyle=grd;ctx.shadowColor="#818cf8";ctx.shadowBlur=14+8*pulse;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Visible indicator ring (full opacity ring shows when visible)
  if(vis>0.6){
    ctx.globalAlpha=(vis-0.6)*2.5*pulse;ctx.strokeStyle="#fbbf24";ctx.lineWidth=2;
    ctx.shadowColor="#fbbf24";ctx.shadowBlur=10;
    ctx.beginPath();ctx.arc(0,0,r*1.2,0,Math.PI*2);ctx.stroke();
  }
  ctx.fillStyle="#c7d2fe";ctx.font=`bold ${Math.round(r*0.75)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=vis*0.9;
  ctx.fillText("👻",0,1);ctx.restore();
}

// ── Heart target — beats like a heart; tap for +1 life AND coin bonus ──
function drawHeart(ctx, r, ts) {
  const beat=0.5+0.5*Math.sin(ts*0.012);
  const sz=r*(1+beat*0.12);
  ctx.save();ctx.shadowColor="#f43f5e";ctx.shadowBlur=16+10*beat;
  ctx.fillStyle=`hsl(${350+beat*5},90%,${55+beat*5}%)`;
  // Heart shape using bezier curves
  ctx.beginPath();
  ctx.moveTo(0,-sz*0.55);
  ctx.bezierCurveTo(sz*0.55,-sz*0.95,sz*1.1,-sz*0.3,0,sz*0.55);
  ctx.bezierCurveTo(-sz*1.1,-sz*0.3,-sz*0.55,-sz*0.95,0,-sz*0.55);
  ctx.fill();
  // Highlight
  ctx.fillStyle="#ffffff44";ctx.beginPath();
  ctx.ellipse(-sz*0.3,-sz*0.55,sz*0.22,sz*0.15,Math.PI*0.4,0,Math.PI*2);ctx.fill();
  // Label
  ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(sz*0.55)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.9;
  ctx.fillText("+1",0,sz*0.1);ctx.restore();
}

// ── Nova target — pulsing supernova; tap to freeze ALL targets for 2s ──
function drawNova(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.009);
  const boom=0.7+0.3*Math.sin(ts*0.006);
  // Outer corona
  const coronaColors=["#fde68a","#fbbf24","#f59e0b","#d97706"];
  for(let i=3;i>=0;i--){
    const cr=r*(1.2+i*0.35)*boom;
    ctx.save();ctx.globalAlpha=(0.06+i*0.04)*pulse;
    ctx.fillStyle=coronaColors[i]||"#fbbf24";ctx.shadowColor="#fbbf24";ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(0,0,cr,0,Math.PI*2);ctx.fill();ctx.restore();
  }
  // Star burst rays
  for(let i=0;i<8;i++){
    const a=(i/8)*Math.PI*2+ts*0.003;
    const rl=r*(0.85+0.2*Math.sin(ts*0.007+i));
    ctx.save();ctx.strokeStyle="#fde68a";ctx.lineWidth=2;ctx.globalAlpha=0.6*pulse;
    ctx.shadowColor="#fbbf24";ctx.shadowBlur=10;
    ctx.beginPath();ctx.moveTo(Math.cos(a)*r*0.6,Math.sin(a)*r*0.6);
    ctx.lineTo(Math.cos(a)*rl,Math.sin(a)*rl);ctx.stroke();ctx.restore();
  }
  // Core
  const grd=ctx.createRadialGradient(0,0,0,0,0,r*0.85);
  grd.addColorStop(0,"#fef9c3");grd.addColorStop(0.4,"#fbbf24");grd.addColorStop(1,"#92400e");
  ctx.save();ctx.fillStyle=grd;ctx.shadowColor="#fbbf24";ctx.shadowBlur=20+10*pulse;
  ctx.beginPath();ctx.arc(0,0,r*0.85,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(r*0.8)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.95;
  ctx.fillText("💫",0,1);ctx.restore();
}

// ── Beacon target — stationary golden lighthouse; nearby taps score double while it lives ──
function drawBeacon(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  // Radiating rings (influence area indicator)
  for(let i=3;i>0;i--){
    ctx.save();ctx.strokeStyle="#fbbf24";ctx.lineWidth=1;ctx.globalAlpha=(0.06+i*0.03)*pulse;
    ctx.shadowColor="#fbbf24";ctx.shadowBlur=4;
    ctx.beginPath();ctx.arc(0,0,r*(1.5+i*0.6),0,Math.PI*2);ctx.stroke();ctx.restore();
  }
  // Core golden orb
  const grd=ctx.createRadialGradient(-r*0.2,-r*0.2,0,0,0,r);
  grd.addColorStop(0,"#fef9c3");grd.addColorStop(0.4,"#fbbf24");grd.addColorStop(1,"#b45309");
  ctx.save();ctx.fillStyle=grd;ctx.shadowColor="#fbbf24";ctx.shadowBlur=18+8*pulse;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Beacon beam upward
  const beamH=r*2.5;
  const beamGrd=ctx.createLinearGradient(0,-r,0,-r-beamH);
  beamGrd.addColorStop(0,"#fbbf2488");beamGrd.addColorStop(1,"transparent");
  ctx.globalAlpha=0.4+0.3*pulse;ctx.fillStyle=beamGrd;
  ctx.beginPath();ctx.moveTo(-r*0.3,-r);ctx.lineTo(r*0.3,-r);
  ctx.lineTo(r*0.6,-r-beamH);ctx.lineTo(-r*0.6,-r-beamH);ctx.closePath();ctx.fill();
  ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(r*0.8)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.95;
  ctx.fillText("🔆",0,1);ctx.restore();
}

// ── Shadow target — leaves a clone shadow on tap; tap shadow for bonus pts ──
function drawShadow(ctx, r, ts, isShadowClone) {
  const pulse=0.5+0.5*Math.sin(ts*0.009);
  if(isShadowClone){
    // Shadow clone: ghostly dark silhouette
    ctx.save();ctx.globalAlpha=0.45*pulse;
    ctx.fillStyle="#1e1b4b";ctx.shadowColor="#818cf8";ctx.shadowBlur=12;
    ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
    ctx.fillStyle="#818cf8";ctx.font=`bold ${Math.round(r*0.7)}px sans-serif`;
    ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.7*pulse;
    ctx.fillText("👤",0,1);ctx.restore();
    return;
  }
  // Main shadow target: deep indigo with mirror effect
  const grd=ctx.createRadialGradient(0,0,0,0,0,r);
  grd.addColorStop(0,"#4338ca");grd.addColorStop(0.5,"#3730a3");grd.addColorStop(1,"#1e1b4b");
  ctx.save();ctx.fillStyle=grd;ctx.shadowColor="#6366f1";ctx.shadowBlur=16+6*pulse;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Dark shimmer waves
  for(let i=0;i<3;i++){
    const a=(i/3)*Math.PI*2+ts*0.004;
    ctx.strokeStyle="#818cf8";ctx.lineWidth=1;ctx.globalAlpha=0.3*pulse;
    ctx.beginPath();ctx.arc(Math.cos(a)*r*0.3,Math.sin(a)*r*0.3,r*0.4,0,Math.PI*2);ctx.stroke();
  }
  ctx.fillStyle="#c7d2fe";ctx.font=`bold ${Math.round(r*0.8)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.95;
  ctx.fillText("🕶️",0,1);ctx.restore();
}

// ── Portal target — swirling warp gate; teleports all targets when tapped ──
function drawPortal(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.008);
  // Outer ring of portal energy
  for(let ring=3;ring>0;ring--){
    const ringR=r*(0.7+ring*0.22);
    const hue=(ts*0.06+ring*60)%360;
    ctx.save();ctx.globalAlpha=(0.1+ring*0.08)*pulse;
    ctx.strokeStyle=`hsl(${hue},85%,65%)`;ctx.lineWidth=3-ring*0.5;
    ctx.shadowColor=`hsl(${hue},85%,65%)`;ctx.shadowBlur=10;
    ctx.setLineDash([5,4]);ctx.beginPath();ctx.arc(0,0,ringR,0,Math.PI*2);ctx.stroke();
    ctx.setLineDash([]);ctx.restore();
  }
  // Spinning inner warp ring
  const spinAngle=ts*0.005;
  for(let i=0;i<8;i++){
    const a=spinAngle+(i/8)*Math.PI*2;
    const hue2=(i*45+ts*0.08)%360;
    ctx.save();ctx.globalAlpha=0.7*pulse;
    ctx.fillStyle=`hsl(${hue2},90%,65%)`;ctx.shadowColor=`hsl(${hue2},90%,65%)`;ctx.shadowBlur=8;
    ctx.beginPath();ctx.arc(Math.cos(a)*r*0.58,Math.sin(a)*r*0.58,3,0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
  // Dark core with ∞ symbol
  const coreGrd=ctx.createRadialGradient(0,0,0,0,0,r*0.7);
  coreGrd.addColorStop(0,"#0f0f2a");coreGrd.addColorStop(0.6,"#1e1b4b");coreGrd.addColorStop(1,"#312e81cc");
  ctx.save();ctx.fillStyle=coreGrd;ctx.shadowColor="#818cf8";ctx.shadowBlur=16*pulse;
  ctx.beginPath();ctx.arc(0,0,r*0.7,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#818cf8";ctx.font=`bold ${Math.round(r*0.7)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.9;
  ctx.fillText("🌀",0,1);ctx.restore();
}

// ── Particle Bomb target — explodes into scoreable spark particles on tap ──
function drawParticleBomb(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.009);
  // Pulsing danger ring
  ctx.save();ctx.strokeStyle="#ff4500";ctx.lineWidth=2.5+pulse;ctx.globalAlpha=0.5+0.4*pulse;
  ctx.shadowColor="#ff4500";ctx.shadowBlur=18;
  ctx.beginPath();ctx.arc(0,0,r*1.3+pulse*4,0,Math.PI*2);ctx.stroke();
  // Core orange-red gradient
  const grd=ctx.createRadialGradient(0,0,0,0,0,r);
  grd.addColorStop(0,"#ffed4a");grd.addColorStop(0.4,"#ff8c00");grd.addColorStop(0.8,"#ff4500");grd.addColorStop(1,"#dc2626");
  ctx.globalAlpha=1;ctx.fillStyle=grd;ctx.shadowColor="#ff4500";ctx.shadowBlur=20+pulse*8;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Particle sparks orbiting
  for(let i=0;i<5;i++){
    const a=(i/5)*Math.PI*2+ts*0.006;
    const osc=r*(1.0+0.15*Math.sin(ts*0.012+i));
    ctx.fillStyle=i%2===0?"#ffed4a":"#ff8c00";ctx.globalAlpha=0.8*pulse;
    ctx.beginPath();ctx.arc(Math.cos(a)*osc,Math.sin(a)*osc,3,0,Math.PI*2);ctx.fill();
  }
  ctx.fillStyle="#fff";ctx.font=`bold ${Math.round(r*0.8)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.95;
  ctx.fillText("💥",0,1);ctx.restore();
}

// ── Ricochet target — bouncing silver orb; tap to ricochet-kill 2 nearby targets ──
function drawRicochet(ctx, r, ts) {
  const pulse=0.7+0.3*Math.sin(ts*0.01);
  // Outer bounce ring
  ctx.save();ctx.strokeStyle="#e2e8f0";ctx.lineWidth=2;ctx.globalAlpha=0.5*pulse;
  ctx.shadowColor="#94a3b8";ctx.shadowBlur=10;
  ctx.setLineDash([6,4]);ctx.beginPath();ctx.arc(0,0,r*1.3,0,Math.PI*2);ctx.stroke();
  ctx.setLineDash([]);ctx.restore();
  // Core silver body
  const grd=ctx.createRadialGradient(-r*0.25,-r*0.25,0,0,0,r);
  grd.addColorStop(0,"#f8fafc");grd.addColorStop(0.5,"#94a3b8");grd.addColorStop(1,"#475569");
  ctx.save();ctx.shadowColor="#cbd5e1";ctx.shadowBlur=14+6*pulse;
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fill();
  // Reflection highlight
  ctx.fillStyle="#ffffff66";ctx.beginPath();ctx.arc(-r*0.28,-r*0.3,r*0.28,0,Math.PI*2);ctx.fill();
  // Bounce arrows indicating ricochet
  const arrowAngs=[Math.PI*0.2,Math.PI*0.7,Math.PI*1.2];
  arrowAngs.forEach(a=>{
    const ax=Math.cos(a)*r*0.55,ay=Math.sin(a)*r*0.55;
    ctx.save();ctx.translate(ax,ay);ctx.rotate(a+Math.PI/2);
    ctx.strokeStyle="#fff";ctx.lineWidth=1.5;ctx.globalAlpha=0.7*pulse;
    ctx.beginPath();ctx.moveTo(0,-4);ctx.lineTo(0,4);ctx.lineTo(-3,1);ctx.moveTo(0,4);ctx.lineTo(3,1);
    ctx.stroke();ctx.restore();
  });
  ctx.restore();
}

// ── Aurora target — shimmering northern lights; rhythm-based tap multiplier ──
function drawAurora(ctx, r, ts) {
  const pulse=0.5+0.5*Math.sin(ts*0.007);
  // Aurora wave bands
  const bands=5;
  for(let i=0;i<bands;i++){
    const hue=(i/bands)*120+180+ts*0.04; // shifting blue-green-purple
    const wave=Math.sin(ts*0.006+i*1.2)*r*0.3;
    const bandR=r*(0.6+i*0.18);
    ctx.save();ctx.globalAlpha=(0.12+i*0.04)*pulse;
    ctx.strokeStyle=`hsl(${hue},90%,65%)`;ctx.lineWidth=6-i;
    ctx.shadowColor=`hsl(${hue},90%,65%)`;ctx.shadowBlur=12;
    ctx.beginPath();
    for(let a=0;a<=Math.PI*2;a+=0.1){
      const wr=bandR+wave*Math.sin(a*3+ts*0.003);
      const px=Math.cos(a)*wr,py=Math.sin(a)*wr;
      a===0?ctx.moveTo(px,py):ctx.lineTo(px,py);
    }
    ctx.closePath();ctx.stroke();ctx.restore();
  }
  // Core gem
  const grd=ctx.createRadialGradient(0,0,0,0,0,r*0.85);
  grd.addColorStop(0,"#e0f2fe");grd.addColorStop(0.4,"#38bdf8");grd.addColorStop(0.8,"#0284c7");grd.addColorStop(1,"#0c4a6e");
  ctx.save();ctx.shadowColor="#38bdf8";ctx.shadowBlur=20+10*pulse;
  ctx.fillStyle=grd;ctx.beginPath();ctx.arc(0,0,r*0.85,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#ffffff88";ctx.beginPath();ctx.arc(-r*0.22,-r*0.25,r*0.22,0,Math.PI*2);ctx.fill();
  ctx.fillStyle="#e0f2fe";ctx.font=`bold ${Math.round(r*0.7)}px sans-serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.globalAlpha=0.9;
  ctx.fillText("🌌",0,1);ctx.restore();
}

function drawTrail(ctx, t) {
  if(!t.trail||t.trail.length<2) return;
  // Ghost afterimages every 3 frames
  const step=Math.max(1,Math.floor(t.trail.length/4));
  for(let i=0;i<t.trail.length-step;i+=step){
    const tp=t.trail[i];
    const af=i/t.trail.length;
    ctx.save();ctx.globalAlpha=af*0.18;
    ctx.fillStyle=t.color;ctx.shadowColor=t.glow||t.color;ctx.shadowBlur=t.radius*af;
    ctx.beginPath();ctx.arc(tp.x,tp.y,t.radius*(0.4+af*0.5),0,Math.PI*2);ctx.fill();
    ctx.restore();
  }
  // Line trail
  for(let i=1;i<t.trail.length;i++){
    const a=i/t.trail.length;
    ctx.save(); ctx.globalAlpha=a*0.25;
    ctx.strokeStyle=t.color; ctx.lineWidth=t.radius*1.4*a; ctx.lineCap="round";
    ctx.shadowColor=t.color; ctx.shadowBlur=t.radius*a*0.7;
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
  else if(t.type==="magnet")   drawMagnet(ctx,t.radius,ts);
  else if(t.type==="phantom")  drawPhantom(ctx,t.radius,ts,timeLeft);
  else if(t.type==="volatile") drawVolatile(ctx,t.radius,ts,timeLeft);
  else if(t.type==="healer")   drawHealer(ctx,t.radius,ts);
  else if(t.type==="twin")     drawTwin(ctx,t.radius,ts);
  else if(t.type==="rainbow")  drawRainbow(ctx,t.radius,ts);
  else if(t.type==="frozen")   drawFrozen(ctx,t.radius,ts);
  else if(t.type==="bouncy")   drawBouncy(ctx,t.radius,ts);
  else if(t.type==="ninja")    drawNinja(ctx,t.radius,ts,timeLeft);
  else if(t.type==="lootchest") drawLootChest(ctx,t.radius,ts);
  else if(t.type==="tornado")  drawTornado(ctx,t.radius,ts);
  else if(t.type==="bubble")   drawBubble(ctx,t.radius,ts);
  else if(t.type==="echo")     drawEcho(ctx,t.radius,ts);
  else if(t.type==="echo_ghost") drawEchoGhost(ctx,t.radius,ts,t._ghostBorn);
  else if(t.type==="crystal")  drawCrystalTarget(ctx,t.radius,ts);
  else if(t.type==="crystal_shard") drawCrystalShard(ctx,t.radius,ts,t._shardBorn);
  else if(t.type==="rage")     {const rl=Math.min(1,(now-t.spawnedAt)/(t.lifetime*0.9));drawRage(ctx,t.radius,ts,rl);}
  else if(t.type==="divider")  drawDivider(ctx,t.radius,ts);
  else if(t.type==="vanishing") drawVanishing(ctx,t.radius,ts);
  else if(t.type==="homing")   drawHoming(ctx,t.radius,ts);
  else if(t.type==="gemstone") drawGemstone(ctx,t.radius,ts);
  else if(t.type==="poison")   drawPoison(ctx,t.radius,ts);
  else if(t.type==="morph")      drawMorph(ctx,t.radius,ts,t.spawnedAt);
  else if(t.type==="conductor")  drawConductor(ctx,t.radius,ts);
  else if(t.type==="siphon")     drawSiphon(ctx,t.radius,ts,1-(now-t.spawnedAt)/t.lifetime);
  else if(t.type==="glitch")     drawGlitch(ctx,t.radius,ts);
  else if(t.type==="prism")      drawPrism(ctx,t.radius,ts);
  else if(t.type==="comet")      drawComet(ctx,t.radius,ts,t.trail);
  else if(t.type==="mirrorball") drawMirrorBall(ctx,t.radius,ts);
  else if(t.type==="nexus")      drawNexus(ctx,t.radius,ts);
  else if(t.type==="icecomet")   drawIceComet(ctx,t.radius,ts,t.trail);
  else if(t.type==="phoenix")    drawPhoenix(ctx,t.radius,ts,false);
  else if(t.type==="phoenix2")   drawPhoenix(ctx,t.radius,ts,true);
  else if(t.type==="voltage")    drawVoltage(ctx,t.radius,ts);
  else if(t.type==="void")       drawVoid(ctx,t.radius,ts);
  else if(t.type==="clover")     drawLuckyClover(ctx,t.radius,ts);
  else if(t.type==="ricochet")   drawRicochet(ctx,t.radius,ts);
  else if(t.type==="aurora")     drawAurora(ctx,t.radius,ts);
  else if(t.type==="portal")     drawPortal(ctx,t.radius,ts);
  else if(t.type==="particlebomb") drawParticleBomb(ctx,t.radius,ts);
  else if(t.type==="beacon")     drawBeacon(ctx,t.radius,ts);
  else if(t.type==="shadow")     drawShadow(ctx,t.radius,ts,false);
  else if(t.type==="shadow_clone") drawShadow(ctx,t.radius,ts,true);
  else if(t.type==="spectral")   drawSpectral(ctx,t.radius,ts);
  else if(t.type==="heart")      drawHeart(ctx,t.radius,ts);
  else if(t.type==="nova")       drawNova(ctx,t.radius,ts);
  else if(t.type==="firefly")    drawFirefly(ctx,t.radius,ts);
  else if(t.type==="geode")      drawGeode(ctx,t.radius,ts,t._geodeCracked);
  else if(t.type==="timebomb"){const secsLeft=Math.max(0,(t.spawnedAt+t.lifetime-Date.now())/1000);drawTimeBomb(ctx,t.radius,ts,secsLeft);}
  else if(t.type==="thunderbolt") drawThunderbolt(ctx,t.radius,ts);
  else if(t.type==="gravityorb")  drawGravityOrb(ctx,t.radius,ts);
  else if(t.type==="crystalball") drawCrystalBall(ctx,t.radius,ts);
  else{
    const nm=t.rarity?.name;
    if     (nm==="common")    drawCommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="uncommon")  drawUncommon(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="rare")      drawRare(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="epic")      drawEpic(ctx,t.radius,t.color,t.glow,ts,timeLeft);
    else if(nm==="legendary") drawLegendary(ctx,t.radius,t.color,t.glow,ts,timeLeft);
  }
  // Perfect zone sweet-spot dot — subtle center glow on normal targets
  if(t.type==="normal"&&t.rarity&&t.rarity.name!=="common"){
    const tlNow=Math.max(0,1-(Date.now()-t.spawnedAt)/t.lifetime);
    const inPZ=tlNow>0.36&&tlNow<0.67;
    if(inPZ){
      ctx.save();ctx.globalAlpha=0.45+0.3*Math.abs(Math.sin(ts/90));
      ctx.fillStyle="#ffffff";ctx.shadowColor="#ffd700";ctx.shadowBlur=8;
      ctx.beginPath();ctx.arc(0,0,t.radius*0.22,0,Math.PI*2);ctx.fill();
      ctx.restore();
    }
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

// ── World Weather Particles (deterministic, no state needed) ──
function drawWeatherParticles(ctx,w,h,worldId,ts){
  if(!worldId)return;
  const N=26;const gr=2.39996;
  ctx.save();
  if(worldId===1){
    // Dragon's Lair: fire embers rising
    for(let i=0;i<N;i++){
      const spd=0.000038+(i%5)*0.000014;
      const t=((ts*spd+i*0.14)%1+1)%1;
      const x=((Math.sin(i*gr)*0.5+0.5)*w*0.88+w*0.06+Math.sin(ts*0.0008+i*0.7)*20)%w;
      const y=h-(t*(h*1.08))-20;
      const fade=t<0.18?t/0.18:t>0.82?(1-t)/0.18:1;
      const flicker=0.55+0.45*Math.sin(ts*0.013+i*1.3);
      ctx.globalAlpha=fade*0.52*flicker;
      ctx.fillStyle=i%3===0?"#ff6600":i%3===1?"#ffaa00":"#ff3300";
      ctx.shadowColor=ctx.fillStyle;ctx.shadowBlur=7;
      ctx.beginPath();ctx.arc(x,y,1.4+(i%4)*0.6,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===2){
    // Troll Forest: leaves + fireflies
    for(let i=0;i<N;i++){
      const isFirefly=i%7===0;
      if(isFirefly){
        const fx=(Math.sin(i*gr+ts*0.00028)*0.45+0.5)*w;
        const fy=(Math.cos(i*gr*1.3+ts*0.00022)*0.38+0.5)*h;
        const glow=0.4+0.6*Math.sin(ts*0.005+i*2.1);
        ctx.globalAlpha=glow*0.55;ctx.fillStyle="#ccff44";
        ctx.shadowColor="#88ff00";ctx.shadowBlur=10;
        ctx.beginPath();ctx.arc(fx,fy,1.4,0,Math.PI*2);ctx.fill();
      } else {
        const spd=0.000017+(i%6)*0.0000055;
        const t=((ts*spd+i*0.13)%1+1)%1;
        const x=((Math.sin(i*gr*2)*0.5+0.5)*w+Math.sin(ts*0.0006+i*0.9)*28)%w;
        const y=t*(h+18)-9;
        const fade=t<0.1?t*10:t>0.9?(1-t)*10:0.7;
        ctx.globalAlpha=fade*0.48;ctx.shadowBlur=0;
        ctx.save();ctx.translate(x,y);ctx.rotate(ts*0.002+i*0.8);
        ctx.fillStyle=i%3===0?"#2d5a1b":i%3===1?"#1a3d0e":"#3a6e22";
        ctx.beginPath();ctx.ellipse(0,0,3.5,1.5,0,0,Math.PI*2);ctx.fill();
        ctx.restore();
      }
    }
  } else if(worldId===3){
    // Elven Kingdom: golden sparkle dust drifting up
    for(let i=0;i<N;i++){
      const spd=0.000028+(i%4)*0.00001;
      const t=((ts*spd+i*0.11)%1+1)%1;
      const x=(Math.sin(i*gr+ts*0.00018)*0.45+0.5)*w+Math.sin(ts*0.0009+i*0.6)*14;
      const y=h-(t*h*1.04)+Math.sin(ts*0.0009+i*0.55)*13;
      const sparkle=0.5+0.5*Math.sin(ts*0.009+i*1.7);
      const fade=t<0.15?t/0.15:t>0.85?(1-t)/0.15:1;
      ctx.globalAlpha=fade*sparkle*0.55;
      ctx.fillStyle=i%2===0?"#ffd700":"#ffe44d";
      ctx.shadowColor="#ffd700";ctx.shadowBlur=8;
      ctx.beginPath();ctx.arc(x,y,0.9+sparkle*1.4,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===4){
    // Dark Wizard Tower: purple shadow wisps drifting
    for(let i=0;i<20;i++){
      const ox=(Math.sin(i*gr)*0.5+0.5)*w;
      const oy=(Math.cos(i*gr*1.4)*0.5+0.5)*h;
      const wx=ox+Math.sin(ts*0.00035+i*0.8)*44;
      const wy=oy+Math.cos(ts*0.00028+i*1.1)*32;
      const pulse=0.5+0.5*Math.sin(ts*0.003+i*2.2);
      ctx.globalAlpha=pulse*0.17;
      ctx.fillStyle=i%3===0?"#9b59b6":i%3===1?"#6c3483":"#7d3c98";
      ctx.shadowColor="#9b59b6";ctx.shadowBlur=14;
      ctx.beginPath();ctx.arc(wx,wy,5+pulse*8,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===5){
    // Viking Fjords: snowflakes drifting down
    for(let i=0;i<N;i++){
      const spd=0.000023+(i%5)*0.00001;
      const t=((ts*spd+i*0.12)%1+1)%1;
      const drift=Math.sin(ts*0.0005+i*0.7)*22;
      const x=((Math.sin(i*gr*2.1)*0.5+0.5)*w+drift)%w;
      const y=t*(h+14)-7;
      const fade=t<0.07?t/0.07:t>0.93?(1-t)/0.07:1;
      ctx.globalAlpha=fade*0.42;
      ctx.fillStyle="#c8e6ff";ctx.shadowColor="#a8c8ff";ctx.shadowBlur=4;
      ctx.beginPath();ctx.arc(x,y,0.9+(i%3)*0.7,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===6){
    // Goblin Mines: coal dust + gold sparks
    for(let i=0;i<N;i++){
      const spd=0.000028+(i%6)*0.000011;
      const t=((ts*spd+i*0.1)%1+1)%1;
      const x=((Math.sin(i*gr)*0.5+0.5)*w+Math.sin(ts*0.001+i*0.5)*11)%w;
      const y=t*(h+10)-5;
      const isSpark=i%6===0;
      const fade=t<0.1?t*10:t>0.9?(1-t)*10:0.6;
      if(isSpark){
        ctx.globalAlpha=fade*Math.abs(Math.sin(ts*0.018+i*3));
        ctx.fillStyle="#ffd700";ctx.shadowColor="#ff8800";ctx.shadowBlur=8;
        ctx.beginPath();ctx.arc(x,y,1.2,0,Math.PI*2);ctx.fill();
      } else {
        ctx.globalAlpha=fade*0.32;ctx.shadowBlur=0;
        ctx.fillStyle="#443322";
        ctx.beginPath();ctx.arc(x,y,1.4+(i%3)*0.5,0,Math.PI*2);ctx.fill();
      }
    }
  } else if(worldId===7){
    // Undead Catacombs: ghostly orbs drifting sideways
    for(let i=0;i<18;i++){
      const ox=(Math.sin(i*gr*1.5)*0.5+0.5)*w;
      const oy=60+(Math.cos(i*gr)*0.5+0.5)*(h-130);
      const gx=(ox+ts*0.024*(i%2?1:-1)+i*44)%(w+44)-22;
      const gy=oy+Math.sin(ts*0.0008+i*0.9)*20;
      const glow=0.4+0.6*Math.sin(ts*0.0045+i*1.5);
      ctx.globalAlpha=glow*0.2;
      ctx.fillStyle=i%3===0?"#88bb88":"#aaddaa";
      ctx.shadowColor="#66aa66";ctx.shadowBlur=16;
      ctx.beginPath();ctx.arc(gx,gy,5+glow*7,0,Math.PI*2);ctx.fill();
    }
  } else if(worldId===8){
    // Sea Serpent's Deep: bubbles rising
    for(let i=0;i<N;i++){
      const spd=0.00002+(i%5)*0.000009;
      const t=((ts*spd+i*0.115)%1+1)%1;
      const x=((Math.sin(i*gr*1.8)*0.5+0.5)*w*0.88+w*0.06+Math.sin(ts*0.0007+i*0.6)*14);
      const y=h-(t*(h+18))-9;
      const fade=t<0.09?t/0.09:t>0.91?(1-t)/0.09:0.5;
      const r=1.4+(i%4)*0.75;
      ctx.globalAlpha=fade*0.38;
      ctx.strokeStyle="#1abc9c";ctx.lineWidth=0.75;ctx.shadowColor="#1abc9c";ctx.shadowBlur=4;
      ctx.fillStyle="rgba(26,188,156,0.08)";
      ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.fill();ctx.stroke();
    }
  } else if(worldId===9){
    // Giant's Peak: sleet streaks at sharp angle
    for(let i=0;i<N;i++){
      const spd=0.000038+(i%4)*0.000014;
      const t=((ts*spd+i*0.12)%1+1)%1;
      const x=((Math.sin(i*gr*1.9)*0.5+0.5)*w+t*w*0.32)%w;
      const y=t*(h+20)-10;
      const fade=t<0.06?t/0.06:t>0.94?(1-t)/0.06:0.6;
      ctx.globalAlpha=fade*0.48;ctx.shadowBlur=0;
      ctx.strokeStyle="#dce8ff";ctx.lineWidth=0.9;
      ctx.beginPath();ctx.moveTo(x,y);ctx.lineTo(x+4,y+8);ctx.stroke();
    }
  } else if(worldId===10){
    // Ancient Dragon God: divine golden motes rising with cross-sparkle
    for(let i=0;i<N;i++){
      const spd=0.000024+(i%5)*0.0000095;
      const t=((ts*spd+i*0.11)%1+1)%1;
      const x=(Math.sin(i*gr+ts*0.00014)*0.45+0.5)*w+Math.sin(ts*0.0006+i*0.8)*18;
      const y=h-(t*h*1.04);
      const glow=0.5+0.5*Math.sin(ts*0.007+i*2.1);
      const fade=(t<0.09?t/0.09:t>0.91?(1-t)/0.09:1)*glow*0.52;
      ctx.globalAlpha=fade;
      ctx.fillStyle=i%2===0?"#ffd700":"#ffcc00";
      ctx.shadowColor="#ffaa00";ctx.shadowBlur=10;
      ctx.beginPath();ctx.arc(x,y,0.9+glow*1.7,0,Math.PI*2);ctx.fill();
      if(glow>0.85){
        // Tiny cross sparkle at peak brightness
        ctx.globalAlpha=fade*0.6;ctx.strokeStyle="#fff8cc";ctx.lineWidth=0.7;
        ctx.beginPath();ctx.moveTo(x-3,y);ctx.lineTo(x+3,y);ctx.stroke();
        ctx.beginPath();ctx.moveTo(x,y-3);ctx.lineTo(x,y+3);ctx.stroke();
      }
    }
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

function drawTapTrail(ctx,trail,themeAccent,streak){
  const now=performance.now();
  // Combo intensity: higher streak = thicker, brighter, longer trail
  const comboLevel=Math.min(10,Math.floor((streak||0)/5));
  const trailDur=350+comboLevel*40; // up to 750ms at max combo
  const baseAlpha=0.45+comboLevel*0.04;
  const baseSz=2.5+comboLevel*0.5;
  for(let i=trail.length-1;i>=0;i--){
    const p=trail[i];
    const age=now-p.ts;
    if(age>trailDur){trail.splice(i,1);continue;}
    const ratio=1-age/trailDur;
    const alpha=ratio*baseAlpha;
    const sz=baseSz*ratio;
    ctx.save();ctx.globalAlpha=alpha;
    // Fever/high combo: rainbow trail
    const trailColor=streak>=20?`hsl(${(now*0.18+i*15)%360},100%,70%)`:themeAccent||"#a78bfa";
    ctx.fillStyle=trailColor;
    ctx.shadowColor=trailColor;ctx.shadowBlur=6+comboLevel*2;
    ctx.beginPath();ctx.arc(p.x,p.y,sz,0,Math.PI*2);ctx.fill();
    ctx.restore();
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
  const [damageFlash,   setDamageFlash]   = useState(false); // red vignette on life loss
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
  const [rushMode,          setRushMode]          = useState(false);
  const [goldRushMode,      setGoldRushMode]      = useState(false); // Gold Rush — all coin rewards × 3
  const [bossTaunt,         setBossTaunt]         = useState(null); // {text, phase}
  const [closeBanner,       setCloseBanner]       = useState(false); // "SO CLOSE!" banner
  const luckyRef    = useRef(null);   // null | "active" | "countdown"
  const luckyTimer  = useRef(null);
  const triggerLuckyRef = useRef(null); // ref to triggerLucky for forward-reference calls
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
  const [taWorld,        setTaWorld]        = useState(1);    // world selector for time attack
  // Bounty Board — rotating wanted rarity for bonus pts
  const [bountyData,     setBountyData]     = useState(null); // {rarity,icon,mult,expiresAt}
  const bountyRef        = useRef(null);
  const bountyTimerRef   = useRef(null);

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
  const tapTrailRef  = useRef([]); // finger trail {x,y,ts,alpha}
  const missionProg  = useRef({});
  const pausedRef    = useRef(false);
  const levelCfgRef  = useRef(null); // current level config
  const mascotHappyRef = useRef(0);  // 9B — session tap happiness counter (resets per level)

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
    } else if(ptype==="LUCKY"){
      // LUCKY power-up — triggers 7s all-legendary mode
      triggerLuckyRef.current?.();
      spawnPopup(x,y,"⭐ LUCKY STARS!","#ffd700",18);
    } else if(ptype==="COMBO_FREEZE"){
      // COMBO_FREEZE — combo streak is protected for 10s (misses don't reset streak)
      const dur=10000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="COMBO_FREEZE");
      activePwrRef.current.push({type:"COMBO_FREEZE",endsAt:Date.now()+dur});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"🧊 COMBO LOCK!","#67e8f9",18);
    } else if(ptype==="MIRROR"){
      // MIRROR — flip all current target positions horizontally for 5s chaos
      const canvas=canvasRef.current;
      const cw=canvas?canvas.width:390;
      targetsRef.current.forEach(t=>{if(t.type!=="boss"&&!t.dying)t.x=cw-t.x;});
      setScreenShake(true);setTimeout(()=>setScreenShake(false),300);
      spawnPopup(x,y,"🪞 MIRROR!","#c084fc",18);
      setNotif("🪞 MIRROR! All targets flipped!");
    } else if(ptype==="MULTIPLIER"){
      // MULTIPLIER — 3× score for 8 seconds
      const dur=8000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!==ptype);
      activePwrRef.current.push({type:ptype,endsAt:Date.now()+dur});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"×3 MULTIPLIER!","#f43f5e",18);
    } else if(ptype==="GRAVITY"){
      // GRAVITY — pulls all targets toward screen center instantly
      const canvas=canvasRef.current;
      const gcx=canvas?canvas.width/2:195,gcy=canvas?canvas.height/2:350;
      targetsRef.current.forEach(t=>{
        if(t.dying||t.type==="boss")return;
        const dx=gcx-t.x,dy=gcy-t.y,dist=Math.hypot(dx,dy);
        if(dist>0){t.x+=dx*0.55;t.y+=dy*0.55;} // pull 55% of the way to center
      });
      spawnPopup(gcx,gcy,"🌐 GRAVITY PULL!","#a78bfa",20);
      spawnParticles(gcx,gcy,"#a78bfa",20,"spark");
      sfx("chainBonus");vibrate([15,8,25]);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),350);
      setNotif("🌐 GRAVITY! All targets pulled to center!");
    } else if(ptype==="CHAIN_LIGHTNING"){
      // CHAIN LIGHTNING — auto-scores up to 4 random non-boss targets instantly
      const eligible=targetsRef.current.filter(t=>!t.dying&&t.type!=="boss"&&t.type!=="bomb"&&t.type!=="volatile");
      const toZap=eligible.sort(()=>Math.random()-0.5).slice(0,4);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      let totalPts=0;
      toZap.forEach((t,i)=>{
        setTimeout(()=>{
          if(!t.dying){
            t.dying=performance.now();
            const pts=Math.round(60*combo*feverMult);
            gs.score+=pts;gs.sessionStats.score=gs.score;totalPts+=pts;
            spawnParticles(t.x,t.y,"#fbbf24",8,"spark");
            spawnPopup(t.x,t.y-22,`⚡ +${pts}`,"#fbbf24",13);
            sfx("comboNote",Math.min(12,gs.streak+i));
          }
        },i*150);
      });
      spawnPopup(x,y,"⚡ CHAIN LIGHTNING!","#fbbf24",20);
      vibrate([10,8,10,8,25]);sfx("chainBonus");
      unlock("chain_lightning_hit");
      setNotif(`⚡ CHAIN LIGHTNING! Zapping ${toZap.length} targets!`);
    } else if(ptype==="LIFE_SURGE"){
      // LIFE SURGE — instant +2 lives (max cap: starting lives + 2)
      const maxLives=(levelCfgRef.current?.lives||3)+2;
      const gained=Math.min(2,maxLives-gs.lives);
      gs.lives+=gained;
      spawnPopup(x,y,`❤️ +${gained} LIVES!`,"#4ade80",20);
      spawnParticles(x,y,"#4ade80",16,"spark");
      sfx("starEarn");vibrate([15,8,15,8,25]);
      setNotif(`❤️ Life Surge! +${gained} lives!`);
    } else if(ptype==="SCORE_BOOST"){
      // SCORE BOOST — next 3 taps score 5× normal
      gs._scoreBoostTaps=3;
      spawnPopup(x,y,"×5 SCORE BOOST!","#f43f5e",22);
      spawnParticles(x,y,"#f43f5e",16,"spark");
      sfx("powerUp");vibrate([10,6,10,6,25]);
      setNotif("×5 SCORE BOOST! Next 3 taps × 5!");
      unlock("score_boost_use");
    } else if(ptype==="TIME_WARP"){
      // TIME WARP — drastically slows all targets for 6 seconds
      gs._timeWarpEndsAt=Date.now()+6000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="TIME_WARP");
      activePwrRef.current.push({type:"TIME_WARP",endsAt:Date.now()+6000});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"⏱️ TIME WARP!","#818cf8",20);
      spawnParticles(x,y,"#818cf8",18,"spark");
      sfx("powerUp");vibrate([12,8,12,8,30]);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),300);
      setNotif("⏱️ TIME Warp! Everything slowed to 20%!");
      unlock("time_warp_use");
    } else if(ptype==="MAGNET_FIELD"){
      // MAGNET FIELD — all targets drift toward your last tap for 5s
      gs._magnetFieldEndsAt=Date.now()+5000;
      gs._magnetFieldX=x;gs._magnetFieldY=y;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="MAGNET_FIELD");
      activePwrRef.current.push({type:"MAGNET_FIELD",endsAt:Date.now()+5000});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"🧲 MAGNET FIELD!","#ec4899",20);
      spawnParticles(x,y,"#ec4899",18,"spark");
      sfx("powerUp");vibrate([12,8,20,8,12]);
      setNotif("🧲 Magnet Field! Targets pulled toward you!");
    } else if(ptype==="OVERCLOCK"){
      // OVERCLOCK — all points ×2 for 10s (stacks with fever and other multipliers)
      gs._overclockEndsAt=Date.now()+10000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="OVERCLOCK");
      activePwrRef.current.push({type:"OVERCLOCK",endsAt:Date.now()+10000});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"⚡ OVERCLOCK! ×2 PTS!","#fbbf24",22);
      spawnParticles(x,y,"#fbbf24",20,"spark");spawnParticles(x,y,"#ffffff",8,"dot");
      sfx("feverStart");vibrate([15,8,15,8,20]);
      setNotif("⚡ Overclock! All points ×2 for 10 seconds!");
    } else if(ptype==="SHIELD_WALL"){
      // SHIELD_WALL — absorbs up to 3 hits (bombs, misses, siphons) before breaking
      gs._shieldWallHits=3;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD_WALL");
      activePwrRef.current.push({type:"SHIELD_WALL",endsAt:Date.now()+30000,hitsLeft:3});
      setActivePwrDisp([...activePwrRef.current]);
      spawnPopup(x,y,"🏰 SHIELD WALL! ×3","#a78bfa",20);
      spawnParticles(x,y,"#a78bfa",18,"spark");
      sfx("lucky");vibrate([12,8,12,8,12]);
      setNotif("🏰 Shield Wall! Absorbs 3 hits!");
    } else {
      const dur=ptype==="SLOW"?7000:ptype==="FREEZE"?5000:9000;
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!==ptype);
      activePwrRef.current.push({type:ptype,endsAt:Date.now()+dur});
      setActivePwrDisp([...activePwrRef.current]);
      const pLabels={SHIELD:"🛡 SHIELD",SLOW:"🐢 SLOW",DOUBLE:"×2 DOUBLE",FREEZE:"❄️ FREEZE"};
      spawnPopup(x,y,pLabels[ptype]||`+${ptype}`,"#60a5fa",15);
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
      const pt=["SHIELD","SLOW","DOUBLE","LIFE","FREEZE","LUCKY","MIRROR","MULTIPLIER","COMBO_FREEZE","GRAVITY","CHAIN_LIGHTNING","TIME_WARP","SCORE_BOOST","LIFE_SURGE","MAGNET_FIELD","OVERCLOCK","SHIELD_WALL"];
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
    } else if((cfg.id||0)>=14&&Math.random()<0.025&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.5% Magnet — pulls nearby targets toward it
      type="magnet";color="#ec4899";glow="#9d174d";
    } else if((cfg.id||0)>=20&&Math.random()<0.022&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.2% Phantom — ultra-short lifetime (1.1s), huge points, ghostly appearance
      type="phantom";color="#e879f9";glow="#a21caf";
    } else if((cfg.id||0)>=35&&Math.random()<0.012&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.2% Ninja — invisible 80% of lifetime, visible only last 20%; huge score reward
      type="ninja";color="#6b7280";glow="#374151";
    } else if((cfg.id||0)>=16&&Math.random()<0.025&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.5% Bouncy — fast bouncing target, higher points for catching something hard to hit
      type="bouncy";color="#fde047";glow="#eab308";
      moving=true;const boa=Math.random()*Math.PI*2,bsp=2.8+Math.random()*1.8;
      vx=Math.cos(boa)*bsp;vy=Math.sin(boa)*bsp;
    } else if((cfg.id||0)>=28&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Frozen — smaller hit radius (70%), but 3× points
      type="frozen";color="#bfdbfe";glow="#93c5fd";
    } else if((cfg.id||0)>=30&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Rainbow — cycles through rarity tiers every 2s; score based on current tier when tapped
      type="rainbow";color="#ff6030";glow="#ff4400";
    } else if((cfg.id||0)>=22&&Math.random()<0.02&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2% Twin — spawns as a pair; tapping one scores both (bonus points for efficiency)
      type="twin";color="#f59e0b";glow="#d97706";
      // Spawn a matching partner at a nearby position
      const partnerPos=pickPos(BASE_R*1.1);
      const twinId=Math.random().toString(36).slice(2);
      const twinId2=Math.random().toString(36).slice(2);
      // We'll link them by sharing a twinGroupId; handled in tap handler
      gs._pendingTwin={id:twinId2,pos:partnerPos,groupId:twinId,lt:lifetime};
    } else if((cfg.id||0)>=18&&Math.random()<0.015&&gs.lives<cfg.lives&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.5% Healer — only spawns if player has lost lives; restores 1 life when tapped
      type="healer";color="#34d399";glow="#059669";
    } else if((cfg.id||0)>=25&&Math.random()<0.018&&!gs.bonusRoundActive&&effBomb>0&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Volatile — tap to defuse (scores 250pts), or it explodes on expiry (costs a life)
      type="volatile";color="#ff4500";glow="#dc2626";
    } else if((cfg.id||0)>=5&&Math.random()<0.028&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.8% Bubble — large hit zone (1.8× radius), pops for points (easy/fun target for beginners)
      type="bubble";color="#e0f7ff";glow="#67e8f9";
    } else if((cfg.id||0)>=20&&Math.random()<0.022&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.2% Echo — tap it to score, then a ghost echo appears for a bonus second tap
      type="echo";color="#a78bfa";glow="#7c3aed";
    } else if((cfg.id||0)>=30&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Crystal — hexagonal gem; shatters into 3 scoreable shards on tap
      type="crystal";color="#bfdbfe";glow="#3b82f6";
    } else if((cfg.id||0)>=24&&Math.random()<0.012&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.2% Tornado — scrambles nearby target positions in a vortex effect
      type="tornado";color="#67e8f9";glow="#06b6d4";
    } else if((cfg.id||0)>=8&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Loot Chest — big golden chest, drops 3-5 coins on tap
      type="lootchest";color="#ffd700";glow="#b45309";
    } else if((cfg.id||0)>=25&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Rage — starts calm, grows angry/faster over lifetime; worth more points when tapped at high rage
      type="rage";color="#ef4444";glow="#dc2626";moving=true;
    } else if((cfg.id||0)>=15&&Math.random()<0.02&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2% Divider — large orange orb; splits into 2 medium targets when tapped
      type="divider";color="#fb923c";glow="#ea580c";
    } else if((cfg.id||0)>=22&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Vanishing — blinks in/out of visibility; big reward for blind timing
      type="vanishing";color="#67e8f9";glow="#0ea5e9";
    } else if((cfg.id||0)>=12&&Math.random()<0.02&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2% Homing — slowly drifts toward screen center; strategic since it comes to you
      type="homing";color="#34d399";glow="#059669";moving=true;
    } else if((cfg.id||0)>=15&&Math.random()<0.022&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.2% Morph — cycles through rarity tiers every 1.4s; catch during legendary = jackpot
      type="morph";color="#ffffff";glow="#ffffff";moving=Math.random()<0.3;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.5+Math.random()*0.8;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=50&&Math.random()<0.004&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 0.4% Nexus — ultra-rare cosmic core; 2000+ pts; once per session check
      type="nexus";color="#ffd700";glow="#b8860b";
    } else if((cfg.id||0)>=18&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Ice Comet — streaks across screen freezing nearby targets on impact
      type="icecomet";color="#38bdf8";glow="#0ea5e9";moving=true;
      const angle=(Math.PI*0.2+Math.random()*Math.PI*0.6);
      const speed=2.0+Math.random()*1.0;
      vx=Math.cos(angle)*speed;vy=Math.sin(angle)*speed;
    } else if((cfg.id||0)>=12&&Math.random()<0.02&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2% Phoenix — fiery bird; respawns once as epic when expired
      type="phoenix";color="#f97316";glow="#dc2626";moving=Math.random()<0.35;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.5+Math.random()*0.7;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=30&&Math.random()<0.012&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.2% Mirror Ball — disco sphere; tap to spawn 3 mini copies
      type="mirrorball";color="#e2e8f0";glow="#94a3b8";
    } else if((cfg.id||0)>=20&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Comet — streaks across the screen, 3.5s lifetime; trail particles
      type="comet";color="#fde68a";glow="#f59e0b";moving=true;
      // Start from a random edge and fly to the opposite side
      const fromSide=Math.floor(Math.random()*2); // 0=top, 1=left
      // We'll set position via pickPos override below, vx/vy set here
      const speed=2.2+Math.random()*1.2;
      const angle=fromSide===0
        ?(Math.PI*0.3+Math.random()*Math.PI*0.4) // top → down-ish
        :(Math.random()*Math.PI*0.6-Math.PI*0.3); // left → right-ish
      vx=Math.cos(angle)*speed;vy=Math.sin(angle)*speed;
    } else if((cfg.id||0)>=25&&Math.random()<0.013&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.3% Prism — beautiful rainbow diamond; splits score into 3 rainbow beams
      type="prism";color="#f0abfc";glow="#a21caf";
    } else if((cfg.id||0)>=22&&Math.random()<0.015&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.5% Glitch — teleports randomly every 0.9s; premium points
      type="glitch";color="#00ff88";glow="#00cc66";moving=true;
      const a=Math.random()*Math.PI*2;vx=Math.cos(a)*0.6;vy=Math.sin(a)*0.6;
    } else if((cfg.id||0)>=18&&!cfg.isZen&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Siphon — drains 1 life on expiry; tapping it rewards 1000+ pts
      type="siphon";color="#dc2626";glow="#7f1d1d";moving=Math.random()<0.4;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.5+Math.random()*0.7;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=8&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!gs._conductorActive&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Conductor — when tapped boosts spawn rate for 5s and gives staccato combo bonus
      type="conductor";color="#f97316";glow="#c2410c";
    } else if((cfg.id||0)>=40&&Math.random()<0.01&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1% Gemstone — rare prismatic gem; scores 500+ base pts (like legendary rarity)
      type="gemstone";color="#e879f9";glow="#9333ea";
    } else if((cfg.id||0)>=20&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&effBomb>0&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Poison — DON'T tap it (or tap to neutralize); expires = next target 50% score
      type="poison";color="#4ade80";glow="#16a34a";
      const homingAngle=Math.random()*Math.PI*2;
      vx=Math.cos(homingAngle)*0.4;vy=Math.sin(homingAngle)*0.4;
      const initSpd=0.6+Math.random()*0.4;const angle=Math.random()*Math.PI*2;
      vx=Math.cos(angle)*initSpd;vy=Math.sin(angle)*initSpd;
    } else if((cfg.id||0)>=25&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Spectral — phases in/out; 800pts if caught visible, normal pts if invisible
      type="spectral";color="#a5b4fc";glow="#6366f1";moving=Math.random()<0.25;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.3+Math.random()*0.5;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=6&&Math.random()<0.016&&gs.lives<(levelCfgRef.current?.lives||3)+1&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Heart — gives +1 life; only spawns when player has lost lives
      type="heart";color="#f43f5e";glow="#be123c";
    } else if((cfg.id||0)>=30&&Math.random()<0.012&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.2% Nova — freezes all targets for 2s + base score
      type="nova";color="#fbbf24";glow="#b45309";
    } else if((cfg.id||0)>=14&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Beacon — stationary; doubles nearby tap scores while alive
      type="beacon";color="#fbbf24";glow="#b45309";moving=false;
    } else if((cfg.id||0)>=18&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Shadow — leaves clone on tap; tap clone for bonus
      type="shadow";color="#4338ca";glow="#6366f1";moving=Math.random()<0.35;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.4+Math.random()*0.6;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=20&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Portal — teleports all targets to new positions on tap
      type="portal";color="#818cf8";glow="#4f46e5";
    } else if((cfg.id||0)>=15&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&effBomb>0&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Particle Bomb — explodes into scoreable sparks when tapped
      type="particlebomb";color="#ff8c00";glow="#ff4500";
    } else if((cfg.id||0)>=12&&Math.random()<0.019&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.9% Ricochet — tap to ricochet-kill 2 nearby targets
      type="ricochet";color="#94a3b8";glow="#cbd5e1";moving=Math.random()<0.4;
      if(moving){const a=Math.random()*Math.PI*2,sp=1.0+Math.random()*1.0;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=28&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Aurora — rhythm-based tap multiplier (1-5×)
      type="aurora";color="#38bdf8";glow="#0284c7";
    } else if((cfg.id||0)>=10&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Lucky Clover — random 1-10× multiplier on tap
      type="clover";color="#22c55e";glow="#16a34a";
    } else if((cfg.id||0)>=15&&Math.random()<0.02&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2% Voltage — zaps 3 nearby targets in a chain when tapped
      type="voltage";color="#fbbf24";glow="#f59e0b";moving=Math.random()<0.3;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.4+Math.random()*0.6;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
    } else if((cfg.id||0)>=35&&Math.random()<0.01&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1% Void — absorbs up to 5 nearby targets for massive bonus score
      type="void";color="#7c3aed";glow="#4c1d95";
    } else if((cfg.id||0)>=22&&!cfg.isZen&&Math.random()<0.016&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.6% Thunderbolt — fast falling target; defuse for 700pts or it exits and costs a life
      type="thunderbolt";color="#facc15";glow="#fef08a";moving=true;
      vx=0;vy=2.8+Math.random()*1.4; // falls straight down
    } else if((cfg.id||0)>=25&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Gravity Orb — pulls normal targets toward it; tap to score and release them
      type="gravityorb";color="#7c3aed";glow="#a78bfa";
    } else if((cfg.id||0)>=30&&Math.random()<0.01&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1% Crystal Ball — guarantees lucky spawn after tapped
      type="crystalball";color="#c084fc";glow="#e879f9";
    } else if((cfg.id||0)>=18&&Math.random()<0.022&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 2.2% Firefly — tiny fast flickering target; hard to hit, 500+ pts
      type="firefly";color="#22c55e";glow="#84ef63";moving=true;
      const fa=Math.random()*Math.PI*2;const fsp=2.6+Math.random()*1.8;
      vx=Math.cos(fa)*fsp;vy=Math.sin(fa)*fsp;
    } else if((cfg.id||0)>=20&&Math.random()<0.018&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.8% Geode — 2-tap rock; first tap cracks it, second awards gem + coins
      type="geode";color="#64748b";glow="#94a3b8";hitsLeft=2;maxHits=2;
    } else if((cfg.id||0)>=28&&!cfg.isZen&&Math.random()<0.014&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){
      // 1.4% Time Bomb — tap to defuse (+800 pts) or it detonates (−2 lives) after 3s
      type="timebomb";color="#f97316";glow="#dc2626";moving=Math.random()<0.3;
      if(moving){const a=Math.random()*Math.PI*2,sp=0.4+Math.random()*0.5;vx=Math.cos(a)*sp;vy=Math.sin(a)*sp;}
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
    const baseR=type==="boss"?BASE_R*2.4:type==="treasure"?BASE_R*1.7:type==="mystery"?BASE_R*1.5:type==="mimic"?BASE_R*1.35:type==="anchor"?BASE_R*1.3:type==="splitter"?BASE_R*1.4:type==="shielded"?BASE_R*1.25:type==="magnet"?BASE_R*1.3:type==="phantom"?BASE_R*1.4:type==="volatile"?BASE_R*1.45:type==="healer"?BASE_R*1.2:type==="twin"?BASE_R*1.1:type==="rainbow"?BASE_R*1.35:type==="frozen"?BASE_R*1.3:type==="bouncy"?BASE_R*1.0:type==="ninja"?BASE_R*1.2:type==="lootchest"?BASE_R*1.55:type==="tornado"?BASE_R*1.4:type==="bubble"?BASE_R*1.8:type==="echo"?BASE_R*1.25:type==="echo_ghost"?BASE_R*1.15:type==="crystal"?BASE_R*1.3:type==="crystal_shard"?BASE_R*0.65:type==="rage"?BASE_R*1.15:type==="divider"?BASE_R*1.65:type==="vanishing"?BASE_R*1.1:type==="homing"?BASE_R*1.2:type==="gemstone"?BASE_R*1.1:type==="poison"?BASE_R*1.15:type==="morph"?BASE_R*1.2:type==="conductor"?BASE_R*1.25:type==="siphon"?BASE_R*1.3:type==="glitch"?BASE_R*1.1:type==="prism"?BASE_R*1.2:type==="comet"?BASE_R*1.15:type==="mirrorball"?BASE_R*1.45:type==="nexus"?BASE_R*1.8:type==="phoenix"?BASE_R*1.25:type==="phoenix2"?BASE_R*1.4:type==="icecomet"?BASE_R*1.2:type==="voltage"?BASE_R*1.2:type==="void"?BASE_R*1.5:type==="clover"?BASE_R*1.1:type==="ricochet"?BASE_R*1.15:type==="aurora"?BASE_R*1.35:type==="portal"?BASE_R*1.4:type==="particlebomb"?BASE_R*1.25:type==="beacon"?BASE_R*1.3:type==="shadow"?BASE_R*1.1:type==="shadow_clone"?BASE_R*0.9:type==="spectral"?BASE_R*1.1:type==="heart"?BASE_R*1.2:type==="nova"?BASE_R*1.4:type==="firefly"?BASE_R*0.78:type==="geode"?BASE_R*1.3:type==="timebomb"?BASE_R*1.25:type==="thunderbolt"?BASE_R*1.1:type==="gravityorb"?BASE_R*1.5:type==="crystalball"?BASE_R*1.35:type==="normal"?BASE_R*(rarity?.size||1):BASE_R;
    const pos=pickPos(baseR);
    let lifetime=cfg.targetLifetime;
    // World modifiers: Ocean Deep (8) — slower targets (calmer waters), longer lifetimes
    if(cfg.world===8)lifetime*=1.15;
    // World modifiers: Goblin Mines (6) — slightly faster targets (more chaotic) — short lifetimes
    if(cfg.world===6)lifetime*=0.92;
    if(activePwrRef.current.some(p=>p.type==="SLOW"&&p.endsAt>Date.now()))lifetime*=1.6;
    if(activePwrRef.current.some(p=>p.type==="FREEZE"&&p.endsAt>Date.now())){vx=0;vy=0;}
    // Phantom targets: very short lifetime (1100ms fixed) — catch it or lose it!
    if(type==="phantom")lifetime=1100;
    // Volatile targets: medium-short lifetime (2200ms) — defuse or explode
    if(type==="volatile")lifetime=2200;
    // Ninja targets: longer lifetime (3500ms) so visible window is still ~700ms
    if(type==="ninja")lifetime=3500;
    // Comet targets: very short lifetime (2800ms) — it flies across fast!
    if(type==="comet")lifetime=2800;
    // Ice Comet: similar short lifetime
    if(type==="icecomet")lifetime=3000;
    // Time Bomb: fixed 3s detonation fuse
    if(type==="timebomb")lifetime=3000;
    // Firefly: shorter lifetime (they dart away fast)
    if(type==="firefly")lifetime=Math.min(lifetime,2200);
    // Geode: slightly longer (2-tap mechanic)
    if(type==="geode")lifetime=Math.max(lifetime,3400);
    // Thunderbolt: very short (2s) — it falls fast
    if(type==="thunderbolt")lifetime=Math.min(lifetime,2000);
    // Gravity Orb: medium lifetime (allows it to pull targets for a while)
    if(type==="gravityorb")lifetime=Math.max(lifetime,3200);
    // Crystal Ball: medium-long (gives time to plan the tap)
    if(type==="crystalball")lifetime=Math.max(lifetime,3800);
    // Skill: target_sense — extra lifetime
    const tsk=(saveRef.current.skills||{}).target_sense||0;
    if(tsk>=1)lifetime+=500;if(tsk>=2)lifetime+=500;if(tsk>=3)lifetime+=1000;
    // Normal targets telegraph their position 260ms before becoming active
    const anticipateMs=type==="normal"?260:0;
    // Size scaling: normal targets shrink by up to 20% at level 100 (0.8 at L100, 1.0 at L1)
    const finalR=type==="normal"?Math.round(baseR*(1-Math.min(0.20,(cfg.id||1)/100*0.20))):baseR;
    // Boss pattern: 4 patterns based on worldId, advances phases as HP drops
    const bossPattern=type==="boss"?(cfg.world%4):null;
    const mainId=Math.random().toString(36).slice(2);
    const twinGroupId=type==="twin"?mainId:undefined;
    const pendingTwin=type==="twin"?gs._pendingTwin:null;
    if(type==="twin"&&gs._pendingTwin)delete gs._pendingTwin;
    targetsRef.current.push({
      id:mainId,type,rarity:type==="normal"?rarity:null,
      x:pos.x,y:pos.y,radius:finalR,color,glow,lifetime,
      spawnedAt:Date.now()+anticipateMs, // lifetime starts after anticipation
      born:performance.now(),anticipateMs,
      moving,ghost,vx,vy,pwrType,hitsLeft,maxHits,trail:moving?[]:null,
      worldId:cfg.world, worldColor:cfg.worldColor,
      bossPattern, bossPhase:1, // phase 1 = full HP, 2 = mid, 3 = rage
      cx:pos.x, cy:pos.y, // anchor for orbit patterns
      twinGroupId,
    });
    // Spawn twin partner immediately
    if(type==="twin"&&pendingTwin){
      targetsRef.current.push({
        id:pendingTwin.id,type:"twin",rarity:null,
        x:pendingTwin.pos.x,y:pendingTwin.pos.y,radius:baseR,color,glow,lifetime,
        spawnedAt:Date.now(),born:performance.now(),anticipateMs:0,
        moving:false,ghost:false,vx:0,vy:0,pwrType:null,hitsLeft:1,maxHits:1,trail:null,
        worldId:cfg.world,worldColor:cfg.worldColor,bossPattern:null,bossPhase:1,
        cx:pendingTwin.pos.x,cy:pendingTwin.pos.y,twinGroupId:mainId,
      });
    }
  },[sfx,pickPos]);

  // Level complete / game over
  const endLevel=useCallback((won)=>{
    const gs=gsRef.current;if(!gs)return;
    if(rafRef.current){cancelAnimationFrame(rafRef.current);rafRef.current=null;}
    if(luckyTimer.current){clearTimeout(luckyTimer.current);luckyTimer.current=null;}
    if(bountyTimerRef.current){clearTimeout(bountyTimerRef.current);bountyTimerRef.current=null;}
    bountyRef.current=null;setBountyData(null);
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
      // 11B — Boss incoming notification on level X9 (next level is a boss)
      if(cfg.id%10===9){const nextLvl=cfg.id+1;const bossWorld=WORLDS[Math.floor((nextLvl-1)/10)];setTimeout(()=>setNotif(`⚠️ BOSS INCOMING on Level ${nextLvl}! ${bossWorld?.emoji||"👹"} Prepare yourself!`),1500);}
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
      // 5× Score Goal OVERKILL bonus — legendary achievement, extra coins
      if(!cfg.isInfinity&&!cfg.isZen&&cfg.scoreGoal&&score>=cfg.scoreGoal*5){
        const overkillBonus=Math.floor(coinsEarned*0.75);
        coinsEarned+=overkillBonus;
        setTimeout(()=>setNotif(`🌟 OVERKILL × 5! +${overkillBonus}🪙 LEGENDARY!`),1000);
        unlock("overkill_5x");
      }
      // Day-of-week bonuses
      const dayOfWeek=new Date().getDay();
      if(dayOfWeek===5&&!cfg.isZen){ // Friday — double XP (Friday Fever)
        xpEarned=Math.ceil(xpEarned*2);
        setTimeout(()=>setNotif(`🔥 FRIDAY FEVER! 2× XP: +${xpEarned}xp`),900);
        unlock("friday_fever");
      }
      if((dayOfWeek===0||dayOfWeek===6)&&!cfg.isZen){ // Weekend — +50% coins (Weekend Warrior)
        const weekendBonus=Math.floor(coinsEarned*0.5);
        coinsEarned+=weekendBonus;
        setTimeout(()=>setNotif(`🎉 WEEKEND WARRIOR! +${weekendBonus}🪙 bonus!`),900);
        unlock("weekend_warrior");
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
        if(cfg.isTimeAttack&&score>(sv.taBest||0)){sv.taBest=score;sv.taBestWorld=cfg.world;}
        coinsEarned+=Math.floor(score*0.08); // bonus coins for zen
        unlock("zen_master");
      }
      // Phase 10A achievement checks
      if(gs.streak>=50||sv.bestStreak>=50)unlock("streak_50");
      if((sv.totalCoins||0)>=500)unlock("coins_500");
      // Track world visits — all_worlds achievement
      const visitedWorlds=new Set(Object.keys(sv.levelStars||{}).map(id=>getLevelConfig(Number(id)).world));
      if(visitedWorlds.size>=10)unlock("all_worlds");
      // World completion — all 10 levels in a world with at least 1 star
      const worldId=cfg.world;
      const worldLevels=Array.from({length:10},(_,i)=>((worldId-1)*10+i+1));
      const worldDone=worldLevels.every(lid=>(sv.levelStars[lid]||0)>=1);
      if(worldDone){unlock(`world_${worldId}_complete`);unlock("world_complete");}
      // Perfect world — all 10 levels with 3 stars
      const worldPerfect=worldLevels.every(lid=>(sv.levelStars[lid]||0)>=3);
      if(worldPerfect)unlock(`world_${worldId}_perfect`);
      // Perfect run bonus — no misses AND lives unchanged → triple coins
      const missedCount=gs.sessionStats.missedTargets||0;
      const startLives=cfg.lives+(gs._extraLifeUsed?-1:0);
      const isPerfectRun=missedCount===0&&gs.lives>=startLives&&(gs.sessionStats.tapsTotal||0)>=5&&!cfg.isInfinity;
      if(isPerfectRun&&!cfg.isZen){
        const perfectBonus=Math.floor(coinsEarned*2);
        coinsEarned+=perfectBonus;
        sv.coins=(sv.coins||0)+perfectBonus;
        sv.totalCoins=(sv.totalCoins||0)+perfectBonus;
        sfx("flawless");
        setTimeout(()=>setNotif(`🎯 PERFECT LEVEL! +${perfectBonus}🪙 bonus!`),800);
      }
      // Speed bonus — finish a level quickly relative to expected time
      if(!cfg.isInfinity&&!cfg.isZen&&!cfg.isGauntlet&&won){
        const expectedTime=Math.max(15,(cfg.spawnInterval||800)*6/1000); // rough expected seconds
        if(timeSurvived>0&&timeSurvived<expectedTime*0.7){ // finished in top 70% of expected time
          const speedBonus=Math.floor(coinsEarned*0.3);
          if(speedBonus>0){
            coinsEarned+=speedBonus;
            setTimeout(()=>setNotif(`⚡ SPEED BONUS! +${speedBonus}🪙`),1200);
            unlock("speed_demon");
          }
        }
      }
      flushSave();
      const canPrestige=cfg.id===100&&(sv.prestigeLevel||0)<5;
      setLevelCompleteData({score,stars,newStars,xpEarned,coinsEarned,levelId:cfg.id,isLast:cfg.isLast,
        bestStreak:sv.bestStreak,sessionStats:{...gs.sessionStats,timeSurvived},canPrestige,isPerfectRun});
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
      // Frozen targets have 70% smaller effective hit zone (precision challenge)
      const effectiveR=t.type==="frozen"?t.radius*0.70*1.35:t.type==="bubble"?t.radius*1.8:t.radius*1.35;
      if(d<effectiveR&&d<hitDist){hit=t;hitDist=d;}
    }
    ripplesRef.current.push({x:tx,y:ty,r:12,alpha:0.7,color:hit?(hit.color||"#a78bfa"):"#ffffff44"});
    if(!hit)return;

    // MAGNET — collect all targets currently in range (area-of-effect)
    if(hit.type==="magnet"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const MAGNET_R=100;
      const pulled=targetsRef.current.filter(t=>!t.dying&&t.type==="normal"&&Math.hypot(t.x-hit.x,t.y-hit.y)<MAGNET_R);
      let totalPts=0;
      pulled.forEach(t=>{
        const combo=Math.min(10,1+Math.floor(gs.streak/5));
        const feverMult=gs.feverActive?2:1;
        const ptsMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
        const rarityMult=t.rarity?.mult||1;
        const tpts=Math.round(rarityMult*combo*feverMult*ptsMult);
        totalPts+=tpts;
        t.dying=performance.now();
        spawnParticles(t.x,t.y,"#ec4899",10,"spark");
      });
      const basePts=Math.round(150*(gs.feverActive?2:1));
      gs.score+=basePts+totalPts;
      gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("powerUp");vibrate([15,8,30]);
      spawnParticles(hit.x,hit.y,"#ec4899",24,"spark");
      spawnParticles(hit.x,hit.y,"#fce7f3",10,"dot");
      spawnPopup(hit.x,hit.y-26,`🧲 PULLED ${pulled.length}! +${basePts+totalPts}`,"#ec4899",19);
      if(pulled.length>=2)setEpicFlash(true),setTimeout(()=>setEpicFlash(false),600);
      sfx("comboNote",gs.streak);
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

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

    // RAINBOW — score based on current color tier when tapped
    if(hit.type==="rainbow"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const tier=getRainbowTier(performance.now()); // use current time for tier
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierR=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(tier.mult*80*combo*feverMult*prestigeMult*(isMultiplierR?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      if(tier.name!=="common")gs.sessionStats.rareHits++;
      hit.dying=performance.now();
      const tierIcons={common:"⚪",uncommon:"🟢",rare:"🔵",epic:"🟣",legendary:"🌟"};
      sfx(tier.name==="legendary"?"legendary":tier.name==="epic"?"epic":tier.name==="rare"?"rare":"tap");
      vibrate([12,8,12]);
      spawnParticles(hit.x,hit.y,tier.color,20+(tier.mult*3),"spark");
      spawnPopup(hit.x,hit.y-30,`${tierIcons[tier.name]||""} ${tier.name.toUpperCase()}! +${pts}`,"#ffffff",18);
      if(tier.name==="legendary"){setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),600);}
      else if(tier.name==="epic"){setEpicFlash(true);setTimeout(()=>setEpicFlash(false),400);}
      if(tier.name==="legendary")unlock("rainbow_legendary");
      unlock("rainbow_catch");mascotHappyRef.current++;
      const cfg3=levelCfgRef.current;
      if(cfg3){if(gs.score>=cfg3.scoreGoal&&(!cfg3.modifier||checkModGoal(cfg3.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // TWIN — tapping one scores both twins for bonus points
    if(hit.type==="twin"){
      const partner=targetsRef.current.find(t=>t!==hit&&t.type==="twin"&&t.twinGroupId===hit.twinGroupId&&!t.dying);
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierT=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const basePts=120*combo*feverMult*prestigeMult*(isMultiplierT?3:1);
      let totalPts=Math.round(basePts);
      if(partner){
        partner.dying=performance.now();
        totalPts=Math.round(basePts*2.2); // bonus for finding both
        spawnParticles(partner.x,partner.y,"#f59e0b",15,"spark");
        spawnParticles(partner.x,partner.y,"#fbbf24",6,"dot");
        spawnPopup(partner.x,partner.y-22,"✦ TWIN!","#f59e0b",15);
      }
      gs.score+=totalPts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("coin");vibrate([10,8,10,8,20]);
      spawnParticles(hit.x,hit.y,"#f59e0b",20,"spark");
      spawnPopup(hit.x,hit.y-30,partner?`✦×2 +${totalPts}`:`✦ TWIN +${totalPts}`,"#fbbf24",18);
      if(partner)setEpicFlash(true),setTimeout(()=>setEpicFlash(false),400);
      unlock("twin_hit");mascotHappyRef.current++;
      const cfg2=levelCfgRef.current;
      if(cfg2){if(gs.score>=cfg2.scoreGoal&&(!cfg2.modifier||checkModGoal(cfg2.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // FROZEN — smaller hit zone but 3× points reward
    if(hit.type==="frozen"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierFz=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(180*3*combo*feverMult*prestigeMult*(isMultiplierFz?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      hit.dying=performance.now();
      sfx("rare");vibrate([15,8,15,8,25]);
      spawnParticles(hit.x,hit.y,"#bfdbfe",25,"spark");
      spawnParticles(hit.x,hit.y,"#60a5fa",10,"dot");
      spawnPopup(hit.x,hit.y-32,`❄️ FROZEN! ×3 +${pts}`,"#60a5fa",20);
      unlock("frozen_catch");mascotHappyRef.current++;
      const cfgFz=levelCfgRef.current;
      if(cfgFz){if(gs.score>=cfgFz.scoreGoal&&(!cfgFz.modifier||checkModGoal(cfgFz.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // NINJA — nearly invisible, materializes last 20%; enormous point reward
    if(hit.type==="ninja"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const timeLeftNinja=1-(Date.now()-hit.spawnedAt)/hit.lifetime;
      if(timeLeftNinja>0.2){
        // Tapped while still invisible — counts as a miss (can't game it)
        sfx("miss");vibrate(20);
        spawnPopup(hit.x,hit.y-22,"👁️ WHERE IS IT?","#9ca3af",14);
        return;
      }
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierNj=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(600*combo*feverMult*prestigeMult*(isMultiplierNj?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      hit.dying=performance.now();
      sfx("legendary");vibrate([20,8,20,8,40]);
      spawnParticles(hit.x,hit.y,"#9ca3af",30,"spark");spawnParticles(hit.x,hit.y,"#ffffff",12,"dot");
      spawnPopup(hit.x,hit.y-32,`🥷 NINJA! +${pts}`,"#e2e8f0",22);
      setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),700);
      unlock("ninja_catch");mascotHappyRef.current++;
      const cfgNj=levelCfgRef.current;
      if(cfgNj){if(gs.score>=cfgNj.scoreGoal&&(!cfgNj.modifier||checkModGoal(cfgNj.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // BOUNCY — fast-moving elastic ball, 1.8× points
    if(hit.type==="bouncy"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierBo=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(100*1.8*combo*feverMult*prestigeMult*(isMultiplierBo?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      hit.dying=performance.now();
      sfx("rare");vibrate([12,6,12]);
      spawnParticles(hit.x,hit.y,"#fde047",18,"spark");
      spawnParticles(hit.x,hit.y,"#fbbf24",6,"dot");
      spawnPopup(hit.x,hit.y-28,`⚡ BOUNCY! +${pts}`,"#fde047",17);
      unlock("bouncy_catch");mascotHappyRef.current++;
      const cfgBo=levelCfgRef.current;
      if(cfgBo){if(gs.score>=cfgBo.scoreGoal&&(!cfgBo.modifier||checkModGoal(cfgBo.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // HEALER — restores 1 life when tapped
    if(hit.type==="healer"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const cfg=levelCfgRef.current;
      const maxLvs=cfg?cfg.lives:5;
      if(gs.lives<maxLvs){
        gs.lives++;
        spawnParticles(hit.x,hit.y,"#34d399",20,"spark");
        spawnParticles(hit.x,hit.y,"#6ee7b7",8,"dot");
        spawnPopup(hit.x,hit.y-30,"+1 ❤️ HEALED!","#34d399",20);
        sfx("coin");vibrate([12,6,12,6,24]);
        setEpicFlash(true);setTimeout(()=>setEpicFlash(false),400);
        unlock("healer_catch");
      } else {
        // Already full HP — convert to bonus coins
        const coinGift=20;
        saveRef.current.coins=(saveRef.current.coins||0)+coinGift;
        saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinGift;
        spawnPopup(hit.x,hit.y-28,`✨ Full HP! +${coinGift}🪙`,"#34d399",16);
        sfx("coin");
      }
      gs.streak++;gs.lastTapTime=Date.now();gs.sessionStats.tapsTotal++;mascotHappyRef.current++;
      return;
    }

    // VOLATILE — defuse for 250pts, or it explodes costing a life
    if(hit.type==="volatile"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierV=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(250*combo*feverMult*prestigeMult*(isMultiplierV?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("bossHit");vibrate([15,8,15]);
      spawnParticles(hit.x,hit.y,"#ff4500",20,"spark");
      spawnPopup(hit.x,hit.y-28,`💣 DEFUSED! +${pts}`,"#ff8c00",18);
      unlock("volatile_defuse");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // PHANTOM — ultra-short lifetime, huge score reward for catching it
    if(hit.type==="phantom"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplier2=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(500*combo*feverMult*prestigeMult*(isMultiplier2?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      hit.dying=performance.now();
      sfx("legendary");vibrate([20,10,20,10,40]);
      spawnParticles(hit.x,hit.y,"#e879f9",30,"spark");
      spawnParticles(hit.x,hit.y,"#f0abfc",12,"dot");
      spawnPopup(hit.x,hit.y-32,`👻 PHANTOM! +${pts}`,"#e879f9",22);
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
      unlock("phantom_catch");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // BUBBLE — large hit zone, pops with a satisfying burst; decent points
    if(hit.type==="bubble"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierBub=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(60*combo*feverMult*prestigeMult*(isMultiplierBub?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      hit.dying=performance.now();
      sfx("rare");vibrate(10);
      // Pop burst — rainbow iridescent particles
      const bubColors=["#f472b6","#67e8f9","#c084fc","#4ade80","#fbbf24"];
      bubColors.forEach((c,i)=>setTimeout(()=>spawnParticles(hit.x,hit.y,c,8,"dot"),i*20));
      spawnPopup(hit.x,hit.y-26,`🫧 POP! +${pts}`,"#67e8f9",16);
      unlock("bubble_pop");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // ECHO — scores points, then spawns a ghost echo at nearby position for bonus tap
    if(hit.type==="echo"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(90*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("comboNote",gs.streak);vibrate([10,5,15]);
      spawnParticles(hit.x,hit.y,"#a78bfa",10,"spark");
      spawnPopup(hit.x,hit.y-28,`◎ ECHO +${pts}`,"#c4b5fd",15);
      // Spawn ghost echo nearby — tap it for bonus
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      const angle=Math.random()*Math.PI*2;
      const dist=45+Math.random()*60;
      const ghostX=Math.max(hit.radius+22,Math.min(cw-hit.radius-22,hit.x+Math.cos(angle)*dist));
      const ghostY=Math.max(hit.radius+100,Math.min(ch-hit.radius-22,hit.y+Math.sin(angle)*dist));
      const ghostId=Math.random().toString(36).slice(2);
      const ghostBorn=performance.now();
      targetsRef.current.push({
        id:ghostId,type:"echo_ghost",x:ghostX,y:ghostY,
        radius:hit.radius*0.9,color:"#c4b5fd",glow:"#7c3aed",
        rarity:hit.rarity,lifetime:1500,spawnedAt:Date.now(),born:ghostBorn,
        moving:false,ghost:false,vx:0,vy:0,trail:[],
        hitsLeft:1,maxHits:1,dying:null,_ghostBorn:ghostBorn,_echoPts:Math.round(pts*1.5),
      });
      mascotHappyRef.current++;
      unlock("echo_tap");
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // ECHO GHOST — bonus tap after an echo
    if(hit.type==="echo_ghost"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round((hit._echoPts||135)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("lucky");vibrate([10,5,10,5,20]);
      spawnParticles(hit.x,hit.y,"#e9d5ff",14,"spark");
      spawnParticles(hit.x,hit.y,"#7c3aed",6,"dot");
      spawnPopup(hit.x,hit.y-32,`✨ ECHO BONUS! +${pts}`,"#e9d5ff",18);
      unlock("echo_bonus");
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // POISON — tapping neutralizes it (small reward); missing applies poison debuff
    if(hit.type==="poison"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const pts=Math.round(50*combo*feverMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("comboNote",gs.streak);vibrate([8,4,8]);
      spawnParticles(hit.x,hit.y,"#4ade80",10,"spark");
      spawnPopup(hit.x,hit.y-24,`☣️ NEUTRALIZED +${pts}`,"#86efac",14);
      unlock("poison_tap");
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // GEMSTONE — rare prismatic gem; massive score reward
    if(hit.type==="gemstone"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(500*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      gs.sessionStats.rareHits++;
      sfx("legendary");vibrate([25,12,25,12,50]);
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      const rainbowColors=["#ff6030","#ffd700","#34d399","#60a5fa","#f472b6","#a78bfa","#ffffff"];
      rainbowColors.forEach((c,i)=>setTimeout(()=>spawnParticles(hit.x,hit.y,c,10,"spark"),i*40));
      spawnPopup(hit.x,hit.y-40,`💎 GEMSTONE! +${pts}`,"#e879f9",22);
      setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);
      unlock("gemstone_tap");
      mascotHappyRef.current+=5;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // MORPH — score depends on which rarity phase it was caught in
    if(hit.type==="morph"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const cycleMs=1400;
      const elapsed=Date.now()-hit.spawnedAt;
      const phase=Math.floor((elapsed/cycleMs)%MORPH_CYCLE.length); // 0=common .. 4=legendary
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=[30,60,120,220,500][phase]; // scales with tier
      const pts=Math.round(basePts*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      const tier=MORPH_CYCLE[phase];
      if(phase>=3)gs.sessionStats.rareHits++;
      const flashLabels=["✨ COMMON","🌊 UNCOMMON","💜 RARE!","🌟 EPIC!!","🏆 LEGENDARY!!!"][phase];
      spawnParticles(hit.x,hit.y,tier.color,phase>=4?20:8+phase*3,"spark");
      spawnPopup(hit.x,hit.y-36,`${flashLabels} +${pts}`,tier.color,phase>=4?24:18);
      if(phase===4){sfx("legendary");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);vibrate([20,10,20,10,40]);unlock("morph_legendary");}
      else if(phase>=3){sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),600);vibrate([15,8,15]);}
      else{sfx("tap");vibrate([8]);}
      unlock("morph_tap");
      mascotHappyRef.current+=phase>=4?5:1;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // ICE COMET — streaks across screen; freezes nearby targets when tapped
    if(hit.type==="icecomet"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(220*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Freeze nearby targets (80px radius) for 2s
      const FREEZE_R=80;
      targetsRef.current.forEach(t=>{
        if(t!==hit&&!t.dying&&t.type==="normal"&&Math.hypot(t.x-hit.x,t.y-hit.y)<FREEZE_R){
          const origVx=t.vx,origVy=t.vy;
          t.vx=0;t.vy=0;t.moving=false;t._frozen=true;
          spawnParticles(t.x,t.y,"#38bdf8",6,"spark");
          setTimeout(()=>{if(t._frozen){t.vx=origVx;t.vy=origVy;t.moving=origVx!==0||origVy!==0;t._frozen=false;}},2000);
        }
      });
      spawnParticles(hit.x,hit.y,"#38bdf8",20,"spark");
      spawnParticles(hit.x,hit.y,"#bae6fd",10,"dot");
      spawnPopup(hit.x,hit.y-40,`❄️ ICE COMET! +${pts}`,"#38bdf8",22);
      sfx("tap");vibrate([10,6,10]);
      unlock("icecomet_tap");
      mascotHappyRef.current+=2;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // PHOENIX — fiery bird; base pts; expires → phoenix2 (epic risen form)
    if(hit.type==="phoenix"||hit.type==="phoenix2"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const isRisen=hit.type==="phoenix2";
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round((isRisen?350:150)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      if(isRisen)gs.sessionStats.rareHits++;
      const col=isRisen?"#c084fc":"#f97316";
      spawnParticles(hit.x,hit.y,col,isRisen?18:10,"spark");
      spawnPopup(hit.x,hit.y-38,isRisen?`🦋 RISEN! +${pts}`:`🔥 PHOENIX! +${pts}`,col,isRisen?22:18);
      if(isRisen){sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);vibrate([15,8,15]);}
      else sfx("tap");
      unlock("phoenix_tap");
      if(isRisen)unlock("phoenix_risen");
      mascotHappyRef.current+=isRisen?4:1;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // NEXUS — ultra-rare cosmic target; massive score + legendary flash
    if(hit.type==="nexus"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(2000*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak+=5; // instant +5 combo!
      gs.lastTapTime=Date.now();gs.sessionStats.tapsTotal++;
      gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      // Epic particle explosion
      const colors=["#ffd700","#ffffff","#60a5fa","#f472b6","#34d399","#a78bfa"];
      colors.forEach((c,i)=>{
        setTimeout(()=>{spawnParticles(hit.x,hit.y,c,16,"spark");},i*60);
      });
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#ffd700",size:hit.radius*2.5,born:performance.now(),duration:900,alpha:0.85});
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#ffffff",size:hit.radius*1.5,born:performance.now(),duration:600,alpha:0.6});
      spawnPopup(hit.x,hit.y-56,`🌟 NEXUS! +${pts}!`,"#ffd700",28);
      sfx("jackpot");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1200);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),600);
      vibrate([30,15,30,15,60,15,30]);
      unlock("nexus_tap");
      mascotHappyRef.current+=10;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // MIRROR BALL — spawns 3 mini normal targets on tap; rainbow particles
    if(hit.type==="mirrorball"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(100*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Spawn 3 mini disco copies
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      const minicols=["#ff6060","#60ff60","#6060ff"];
      for(let i=0;i<3;i++){
        const angle=(i/3)*Math.PI*2;
        const spx=Math.max(35,Math.min(cw-35,hit.x+Math.cos(angle)*55));
        const spy=Math.max(100,Math.min(ch-35,hit.y+Math.sin(angle)*55));
        targetsRef.current.push({
          id:Math.random().toString(36).slice(2),type:"normal",
          x:spx,y:spy,radius:BASE_R*0.65,color:minicols[i],glow:minicols[i],
          rarity:RARITY.RARE,lifetime:2200,spawnedAt:Date.now(),born:performance.now(),
          moving:false,ghost:false,vx:0,vy:0,trail:[],hitsLeft:1,maxHits:1,dying:null,_isMini:true
        });
      }
      // Rainbow particle burst in 6 directions
      for(let i=0;i<6;i++){
        const hue=i*60;spawnParticles(hit.x,hit.y,`hsl(${hue},100%,65%)`,8,"spark");
      }
      spawnPopup(hit.x,hit.y-40,`🪩 MIRROR BALL! +${pts}`,"#e2e8f0",20);
      sfx("chainBonus");vibrate([12,6,12,6,20]);
      unlock("mirrorball_tap");
      mascotHappyRef.current+=2;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // COMET — streaks across screen; tap mid-flight for bonus
    if(hit.type==="comet"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Early-flight bonus: more points if caught in first 50% of lifetime
      const lifeLeft=Math.max(0,1-(Date.now()-hit.spawnedAt)/hit.lifetime);
      const earlyBonus=lifeLeft>0.5?Math.round(lifeLeft*300):0;
      const pts=Math.round((300+earlyBonus)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      // Gold comet burst
      ["#ffd700","#fde68a","#ffffff","#f59e0b"].forEach((c,i)=>
        setTimeout(()=>spawnParticles(hit.x,hit.y,c,8,"spark"),i*35));
      const label=earlyBonus>0?`🌠 COMET! +${pts} EARLY BONUS!`:`🌠 COMET! +${pts}`;
      spawnPopup(hit.x,hit.y-40,label,"#fde68a",earlyBonus>0?22:18);
      sfx(earlyBonus>0?"legendary":"epic");
      if(earlyBonus>0){setEpicFlash(true);setTimeout(()=>setEpicFlash(false),600);}
      vibrate([12,8,12,8,20]);
      unlock("comet_tap");
      if(earlyBonus>150)unlock("comet_early");
      mascotHappyRef.current+=earlyBonus>0?4:2;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // PRISM — splits score into 3 rainbow beam particle streams
    if(hit.type==="prism"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(280*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      // Spawn 3 rainbow beam particle waves
      const beamColors=["#ff6060","#60ff60","#6060ff"];
      beamColors.forEach((c,i)=>{
        const angle=-Math.PI/2+(i-1)*(Math.PI/5);
        for(let j=0;j<10;j++){
          particlesRef.current.push({
            type:"dot",x:hit.x,y:hit.y,
            vx:Math.cos(angle+j*0.15)*3,vy:Math.sin(angle+j*0.15)*3,
            color:c,alpha:1,scale:1,born:performance.now(),duration:700+j*40
          });
        }
      });
      spawnPopup(hit.x,hit.y-40,`🔮 PRISM! +${pts}`,"#f0abfc",22);
      sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),600);
      vibrate([15,8,15,8,25]);
      unlock("prism_tap");
      mascotHappyRef.current+=3;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // GLITCH — rewards based on how recently it teleported (mid-teleport = bonus)
    if(hit.type==="glitch"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Bonus if caught within 0.3s of last teleport (mid-glitch)
      const timeSinceGlitch=now-(hit._lastGlitch||0);
      const midGlitch=timeSinceGlitch<300;
      const pts=Math.round((midGlitch?400:150)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      const col=midGlitch?"#00ff88":"#ffffff";
      spawnParticles(hit.x,hit.y,col,14,"spark");
      spawnPopup(hit.x,hit.y-36,midGlitch?`🟢 GLITCH PERFECT! +${pts}`:`⬜ GLITCH! +${pts}`,col,midGlitch?22:18);
      if(midGlitch){sfx("legendary");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);vibrate([15,8,15,8,30]);}
      else{sfx("tap");vibrate([8]);}
      unlock("glitch_tap");
      if(midGlitch)unlock("glitch_perfect");
      mascotHappyRef.current+=midGlitch?4:1;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // SIPHON — drains 1 life if not tapped; massive reward for catching it
    if(hit.type==="siphon"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Bonus scales with how much life was left (catching early = more points)
      const lifeLeft=Math.max(0,1-(Date.now()-hit.spawnedAt)/hit.lifetime);
      const urgencyBonus=Math.round(lifeLeft*400); // up to 400 bonus pts for catching early
      const pts=Math.round((600+urgencyBonus)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      spawnParticles(hit.x,hit.y,"#ef4444",16,"spark");
      spawnParticles(hit.x,hit.y,"#fbbf24",8,"dot");
      spawnPopup(hit.x,hit.y-42,`⚠️ SIPHON BLOCKED! +${pts}`,"#ef4444",22);
      sfx("bossKill");vibrate([20,10,20,10,40]);
      setNotif("🛡 Siphon neutralized — danger averted!");
      unlock("siphon_tap");
      mascotHappyRef.current+=3;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // CONDUCTOR — boosts spawn rate for 5s, gives staccato combo notes
    if(hit.type==="conductor"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      gs._conductorActive=true;
      gs._conductorEndsAt=Date.now()+5000;
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(180*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      spawnParticles(hit.x,hit.y,"#f97316",16,"spark");
      spawnPopup(hit.x,hit.y-38,`♪ CONDUCTOR! +${pts}`,"#f97316",20);
      sfx("chainBonus");vibrate([10,6,10,6,20]);
      setNotif("♪ Conductor! Spawn rate boosted for 5s!");
      unlock("conductor_tap");
      mascotHappyRef.current+=2;
      setTimeout(()=>{if(gsRef.current){gsRef.current._conductorActive=false;gsRef.current._conductorEndsAt=null;}},5000);
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // LUCKY CLOVER — random 1-10× score multiplier reveal on tap
    if(hit.type==="clover"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Weighted random: 1-3× common, 4-6× uncommon, 7-9× rare, 10× legendary
      const roll=Math.random();
      const mult=roll<0.45?1+Math.floor(Math.random()*3):roll<0.75?4+Math.floor(Math.random()*3):roll<0.92?7+Math.floor(Math.random()*3):10;
      const basePts=Math.round(80*mult*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      const isJackpot=mult>=10;
      const isGreat=mult>=7;
      const cloverColors=["#22c55e","#4ade80","#86efac","#bbf7d0"];
      cloverColors.forEach((c,i)=>setTimeout(()=>spawnParticles(hit.x,hit.y,c,isJackpot?14:8,"spark"),i*40));
      if(isJackpot){
        particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#22c55e",size:hit.radius*3,born:performance.now(),duration:700,alpha:0.9});
        spawnPopup(hit.x,hit.y-50,`🍀 JACKPOT! ×${mult} = +${basePts}`,"#22c55e",26);
        sfx("jackpot");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);
        setScreenShake(true);setTimeout(()=>setScreenShake(false),400);
        vibrate([25,10,25,10,50]);
      } else if(isGreat){
        spawnPopup(hit.x,hit.y-42,`🍀 LUCKY ×${mult}! +${basePts}`,"#4ade80",22);
        sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
        vibrate([15,8,20]);
      } else {
        spawnPopup(hit.x,hit.y-36,`🍀 ×${mult}! +${basePts}`,"#22c55e",18);
        sfx("rare");vibrate([10,5,10]);
      }
      unlock("clover_tap");
      if(mult>=10)unlock("clover_jackpot");
      mascotHappyRef.current+=mult>=7?4:1;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // RICOCHET — kills 2 nearest normal targets in addition to base score
    if(hit.type==="ricochet"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=Math.round(100*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      spawnParticles(hit.x,hit.y,"#cbd5e1",12,"spark");
      // Find 2 nearest normal targets and ricochet to them
      const ricTargets=targetsRef.current
        .filter(t=>!t.dying&&(t.type==="normal"||t.type==="phantom"))
        .sort((a,b)=>Math.hypot(a.x-hit.x,a.y-hit.y)-Math.hypot(b.x-hit.x,b.y-hit.y))
        .slice(0,2);
      let ricPts=basePts;
      ricTargets.forEach((rt,i)=>{
        setTimeout(()=>{
          if(!rt.dying){
            rt.dying=performance.now();
            const rpts=Math.round(60*combo*feverMult*prestigeMult);
            gs.score+=rpts;ricPts+=rpts;gs.sessionStats.score=gs.score;
            // Draw arc line from hit to target
            particlesRef.current.push({type:"arc",x:hit.x,y:hit.y,x2:rt.x,y2:rt.y,
              color:"#e2e8f0",alpha:1,born:performance.now(),duration:300});
            spawnParticles(rt.x,rt.y,"#94a3b8",8,"spark");
            spawnPopup(rt.x,rt.y-24,`🎯 RICO! +${rpts}`,"#e2e8f0",13);
            sfx("comboNote",gs.streak+i);
          }
        },i*100);
      });
      spawnPopup(hit.x,hit.y-36,`🎯 RICOCHET! +${basePts}`,"#e2e8f0",20);
      sfx("chainBonus");vibrate([12,6,12,6,18]);
      if(ricTargets.length>0)setNotif(`🎯 Ricochet! Killed ${ricTargets.length} nearby!`);
      unlock("ricochet_tap");
      if(ricTargets.length>=2)unlock("ricochet_double");
      mascotHappyRef.current+=1+ricTargets.length;
      const cfgR=levelCfgRef.current;
      if(cfgR){if(gs.score>=cfgR.scoreGoal&&(!cfgR.modifier||checkModGoal(cfgR.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // AURORA — scores based on tap rhythm consistency (taps at even intervals = bonus)
    if(hit.type==="aurora"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Rhythm bonus: consistency of last 3 inter-tap intervals
      const times=gs._recentTaps||[];
      let rhythmMult=1;
      if(times.length>=3){
        const intervals=[];
        for(let i=1;i<Math.min(times.length,4);i++)intervals.push(times[i]-times[i-1]);
        if(intervals.length>=2){
          const avg=intervals.reduce((a,b)=>a+b,0)/intervals.length;
          const variance=intervals.reduce((a,b)=>a+(b-avg)**2,0)/intervals.length;
          const cv=Math.sqrt(variance)/Math.max(avg,1); // coefficient of variation (0=perfect)
          rhythmMult=cv<0.1?5:cv<0.2?4:cv<0.35?3:cv<0.5?2:1;
        }
      }
      const pts=Math.round(160*rhythmMult*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      const rhythmColors=["#94a3b8","#34d399","#60a5fa","#c084fc","#ffd700"];
      const rc=rhythmColors[rhythmMult-1]||"#38bdf8";
      spawnParticles(hit.x,hit.y,rc,12+(rhythmMult*3),"spark");
      const rhythmLabels=["GOOD","GOOD","NICE","GREAT","PERFECT"];
      spawnPopup(hit.x,hit.y-44,`🌌 AURORA ×${rhythmMult} ${rhythmLabels[rhythmMult-1]}! +${pts}`,rc,rhythmMult>=4?24:20);
      if(rhythmMult>=4){sfx("legendary");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);}
      else{sfx("epic");}
      vibrate(rhythmMult>=4?[20,8,20,8,35]:[12,6,16]);
      unlock("aurora_tap");
      if(rhythmMult>=5)unlock("aurora_perfect");
      mascotHappyRef.current+=rhythmMult;
      const cfgA=levelCfgRef.current;
      if(cfgA){if(gs.score>=cfgA.scoreGoal&&(!cfgA.modifier||checkModGoal(cfgA.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // SPECTRAL — phasing ghost; massive pts if caught while visible
    if(hit.type==="spectral"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      // Determine visibility at moment of tap
      const cycle=1600;const phase=(performance.now()%cycle)/cycle;
      const vis=phase<0.5?phase*2:2-phase*2;
      const isVisible=vis>0.4; // must be in visible half of cycle for bonus
      const basePts=Math.round((isVisible?800:120)*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      if(isVisible)gs.sessionStats.rareHits++;
      const col=isVisible?"#fbbf24":"#a5b4fc";
      spawnParticles(hit.x,hit.y,col,isVisible?20:8,"spark");
      spawnPopup(hit.x,hit.y-44,isVisible?`👻 SPECTRAL PERFECT! +${basePts}`:`👻 SPECTRAL +${basePts}`,col,isVisible?26:18);
      if(isVisible){sfx("legendary");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);vibrate([20,10,20,10,50]);}
      else{sfx("rare");vibrate([10,5,10]);}
      unlock("spectral_tap");
      if(isVisible)unlock("spectral_perfect");
      mascotHappyRef.current+=isVisible?6:1;
      const cfgSp=levelCfgRef.current;
      if(cfgSp){if(gs.score>=cfgSp.scoreGoal&&(!cfgSp.modifier||checkModGoal(cfgSp.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // HEART — gives +1 life + coin bonus when tapped
    if(hit.type==="heart"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const maxLives=(levelCfgRef.current?.lives||3)+2;
      const lifeGained=gs.lives<maxLives?1:0;
      const coinBonus=15+Math.floor(Math.random()*10);
      const pts=Math.round(80*combo*feverMult*prestigeMult);
      gs.score+=pts;if(lifeGained>0)gs.lives++;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      saveRef.current.coins=(saveRef.current.coins||0)+coinBonus;
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinBonus;
      debounceSave();
      spawnParticles(hit.x,hit.y,"#f43f5e",14,"spark");
      if(lifeGained>0){
        spawnPopup(hit.x,hit.y-44,`❤️ +1 LIFE! +${coinBonus}🪙 +${pts}`,"#f43f5e",22);
        sfx("starEarn");setScreenShake(false);vibrate([15,8,15,8,30]);
      } else {
        spawnPopup(hit.x,hit.y-36,`💕 LOVE! +${coinBonus}🪙 +${pts}`,"#f43f5e",20);
        sfx("rare");vibrate([12,6,12]);
      }
      unlock("heart_tap");
      mascotHappyRef.current+=3;
      const cfgHt=levelCfgRef.current;
      if(cfgHt){if(gs.score>=cfgHt.scoreGoal&&(!cfgHt.modifier||checkModGoal(cfgHt.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // NOVA — freezes all targets for 2s + good base score
    if(hit.type==="nova"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(200*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      // Nova freeze — store frozen state on targets + use FREEZE power-up
      activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="FREEZE");
      activePwrRef.current.push({type:"FREEZE",endsAt:Date.now()+2000});
      setActivePwrDisp([...activePwrRef.current]);
      // Freeze all existing targets
      targetsRef.current.forEach(t=>{
        if(!t.dying&&t.type!=="boss"){
          const ov=t.vx,oY=t.vy;t.vx=0;t.vy=0;t.moving=false;t._frozenByNova=true;
          setTimeout(()=>{if(t._frozenByNova){t.vx=ov;t.vy=oY;t.moving=ov!==0||oY!==0;t._frozenByNova=false;}},2000);
        }
      });
      // Supernova particle explosion
      const blastColors=["#fde68a","#fbbf24","#ffffff","#f59e0b","#fed7aa"];
      blastColors.forEach((c,i)=>setTimeout(()=>{
        spawnParticles(cw/2,ch/2,c,10,"spark");
      },i*60));
      particlesRef.current.push({type:"shockwave",x:cw/2,y:ch/2,color:"#fbbf24",size:Math.max(cw,ch)*0.5,born:performance.now(),duration:900,alpha:0.7});
      spawnPopup(hit.x,hit.y-50,`💫 NOVA! ALL FROZEN! +${pts}`,"#fbbf24",24);
      sfx("legendary");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),500);
      vibrate([25,10,25,10,60]);
      setNotif("💫 NOVA BLAST! All targets frozen for 2s!");
      unlock("nova_tap");
      mascotHappyRef.current+=5;
      const cfgNv=levelCfgRef.current;
      if(cfgNv){if(gs.score>=cfgNv.scoreGoal&&(!cfgNv.modifier||checkModGoal(cfgNv.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // THUNDERBOLT — tap to catch lightning; big pts; clutch bonus if nearly off-screen
    if(hit.type==="thunderbolt"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const canvas=canvasRef.current;const ch=canvas?.height||700;
      const nearBottom=hit.y>(ch*0.75);// caught it near the bottom = clutch
      const pts=Math.round((nearBottom?1200:700)*combo*feverMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      const label=nearBottom?`⚡ CLUTCH! +${pts}`:`⚡ LIGHTNING! +${pts}`;
      const col=nearBottom?"#fef08a":"#facc15";
      spawnPopup(hit.x,hit.y-30,label,col,nearBottom?22:17);
      spawnParticles(hit.x,hit.y,col,16,"spark");
      if(nearBottom){sfx("chainBonus");vibrate([15,8,20]);setScreenShake(true);setTimeout(()=>setScreenShake(false),220);}
      else{sfx("tap");vibrate(10);}
      unlock("thunderbolt_tap");
      if(nearBottom)unlock("thunderbolt_clutch");
      mascotHappyRef.current+=2;
      updateMissions(gs.sessionStats);
      const cfgTbolt=levelCfgRef.current;
      if(cfgTbolt){if(gs.score>=cfgTbolt.scoreGoal&&(!cfgTbolt.modifier||checkModGoal(cfgTbolt.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // GRAVITY ORB — tap to score + release all pulled targets; bonus per pulled target
    if(hit.type==="gravityorb"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      // Count how many targets are near the orb (they were being pulled)
      const nearby=targetsRef.current.filter(t=>!t.dying&&t.type!=="boss"&&Math.hypot(t.x-hit.x,t.y-hit.y)<180).length;
      const pullBonus=nearby*80;
      const basePts=500+pullBonus;
      const pts=Math.round(basePts*combo*feverMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      // Release pulled targets: push them away from orb center
      targetsRef.current.forEach(t=>{
        if(!t.dying&&t.type!=="boss"&&Math.hypot(t.x-hit.x,t.y-hit.y)<220){
          const dx=t.x-hit.x,dy=t.y-hit.y;const dist=Math.hypot(dx,dy)||1;
          t.vx=(dx/dist)*1.5+(Math.random()-0.5)*0.5;t.vy=(dy/dist)*1.5+(Math.random()-0.5)*0.5;
        }
      });
      const label=nearby>0?`🌐 GRAVITY! +${pts} (${nearby} pulled)`:`🌐 GRAVITY ORB! +${pts}`;
      spawnPopup(hit.x,hit.y-34,label,"#a78bfa",nearby>3?22:18);
      spawnParticles(hit.x,hit.y,"#7c3aed",20,"spark");
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#7c3aed",size:220,born:performance.now(),duration:800,alpha:0.6});
      sfx(nearby>3?"legendary":"bossKill");vibrate([12,8,16]);
      unlock("gravityorb_tap");
      if(nearby>=4)unlock("gravityorb_cluster");
      mascotHappyRef.current+=3;
      updateMissions(gs.sessionStats);
      const cfgGO=levelCfgRef.current;
      if(cfgGO){if(gs.score>=cfgGO.scoreGoal&&(!cfgGO.modifier||checkModGoal(cfgGO.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // CRYSTAL BALL — guarantees legendary rarity on next 2 spawns; scores base pts
    if(hit.type==="crystalball"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const pts=Math.round(400*combo*feverMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs._luckyTaps=2; // next 2 spawns will be legendary (reuses lucky spawn logic if available)
      luckyRef.current="active"; // briefly activate lucky mode for 2 spawns
      setTimeout(()=>{
        if(gsRef.current&&!gsRef.current._crystalBallUsed)gsRef.current._crystalBallUsed=false;
        if(luckyRef.current==="active"){luckyRef.current=null;setLuckyMode(false);}
      },4000);
      setLuckyMode(true);
      spawnPopup(hit.x,hit.y-34,`🔮 CRYSTAL! +${pts} Legendary incoming!`,"#c084fc",20);
      spawnParticles(hit.x,hit.y,"#e879f9",18,"spark");spawnParticles(hit.x,hit.y,"#ffd700",8,"dot");
      sfx("lucky");vibrate([12,8,12,8,20]);
      unlock("crystalball_tap");
      mascotHappyRef.current+=4;
      updateMissions(gs.sessionStats);
      const cfgCB=levelCfgRef.current;
      if(cfgCB){if(gs.score>=cfgCB.scoreGoal&&(!cfgCB.modifier||checkModGoal(cfgCB.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // FIREFLY — tiny fast; 500 base pts, bonus if caught within 0.8s of spawn
    if(hit.type==="firefly"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(12,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const ageMs=Date.now()-hit.spawnedAt;
      const freshBonus=ageMs<800?2:1; // double pts if caught fast
      const pts=Math.round(500*combo*feverMult*freshBonus);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      const label=freshBonus===2?"✨ SWIFT CATCH! +"+pts:"✨ Firefly! +"+pts;
      spawnPopup(hit.x,hit.y-30,label,"#84ef63",freshBonus===2?20:16);
      spawnParticles(hit.x,hit.y,"#bbf7d0",14,"spark");spawnParticles(hit.x,hit.y,"#ffffff",6,"dot");
      sfx("tap");if(freshBonus===2){sfx("chainBonus");vibrate([10,5,15]);}else vibrate(8);
      unlock("firefly_tap");
      if(freshBonus===2&&(gs._swiftCatches||0)===0){gs._swiftCatches=1;unlock("firefly_swift");}
      else if(freshBonus===2)gs._swiftCatches=(gs._swiftCatches||0)+1;
      mascotHappyRef.current+=2;
      updateMissions(gs.sessionStats);
      const cfgFf=levelCfgRef.current;
      if(cfgFf){if(gs.score>=cfgFf.scoreGoal&&(!cfgFf.modifier||checkModGoal(cfgFf.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // GEODE — 2-tap rock; first crack reveals gem, second awards big score + coins
    if(hit.type==="geode"){
      if(hit.hitsLeft===2){
        // First tap — crack the shell
        hit.hitsLeft=1;hit._geodeCracked=true;
        hit.color="#a855f7";hit.glow="#7c3aed";
        spawnParticles(hit.x,hit.y,"#94a3b8",12,"spark");
        spawnPopup(hit.x,hit.y-26,"🪨 CRACKED! Tap again!","#94a3b8",15);
        sfx("tap");vibrate([8,12,8]);
      } else {
        // Second tap — collect the gem
        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
        const combo=Math.min(10,1+Math.floor(gs.streak/5));
        const feverMult=gs.feverActive?2:1;
        const pts=Math.round(650*combo*feverMult);
        const coinReward=3+Math.floor(Math.random()*4);
        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
        saveRef.current.coins=(saveRef.current.coins||0)+coinReward;
        saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinReward;
        spawnPopup(hit.x,hit.y-30,`💎 GEM! +${pts} +${coinReward}🪙`,"#c084fc",22);
        spawnParticles(hit.x,hit.y,"#c084fc",18,"spark");spawnParticles(hit.x,hit.y,"#ffd700",10,"dot");
        sfx("legendary");vibrate([12,8,20]);
        unlock("geode_gem");
        mascotHappyRef.current+=4;
        updateMissions(gs.sessionStats);
        const cfgGd=levelCfgRef.current;
        if(cfgGd){if(gs.score>=cfgGd.scoreGoal&&(!cfgGd.modifier||checkModGoal(cfgGd.modifier,gs))){endLevel(true);return;}}
      }
      unlock("geode_crack");
      return;
    }
    // TIME BOMB — tap to defuse; 800 pts base; clutch bonus if < 0.4s left
    if(hit.type==="timebomb"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const timeLeftMs=Math.max(0,(hit.spawnedAt+hit.lifetime)-Date.now());
      const clutch=timeLeftMs<400;
      const basePts=clutch?1400:800;
      const pts=Math.round(basePts*combo*feverMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      const label=clutch?`💣 CLUTCH DEFUSE! +${pts}`:`💣 DEFUSED! +${pts}`;
      const col=clutch?"#fbbf24":"#f97316";
      spawnPopup(hit.x,hit.y-32,label,col,clutch?22:18);
      spawnParticles(hit.x,hit.y,col,16,"spark");
      if(clutch){spawnParticles(hit.x,hit.y,"#ffffff",8,"dot");sfx("legendary");vibrate([15,8,20]);setScreenShake(true);setTimeout(()=>setScreenShake(false),250);}
      else{sfx("bossKill");vibrate([10,6,12]);}
      unlock("timebomb_defuse");
      if(clutch)unlock("timebomb_clutch");
      mascotHappyRef.current+=3;
      updateMissions(gs.sessionStats);
      const cfgTb=levelCfgRef.current;
      if(cfgTb){if(gs.score>=cfgTb.scoreGoal&&(!cfgTb.modifier||checkModGoal(cfgTb.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // BEACON — stationary amplifier; tap to collect and score nearby bonus
    if(hit.type==="beacon"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const BEACON_R=110;
      const nearbyCount=targetsRef.current.filter(t=>!t.dying&&t.type!=="bomb"&&Math.hypot(t.x-hit.x,t.y-hit.y)<BEACON_R).length;
      const basePts=Math.round((150+nearbyCount*60)*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Remove beacon boost flag from nearby targets
      targetsRef.current.forEach(t=>{if(t._beaconBoost)t._beaconBoost=false;});
      spawnParticles(hit.x,hit.y,"#fbbf24",16,"spark");
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#fbbf24",size:BEACON_R*1.5,born:performance.now(),duration:600,alpha:0.5});
      spawnPopup(hit.x,hit.y-44,`🔆 BEACON! ×${nearbyCount} nearby +${basePts}`,"#fbbf24",nearbyCount>3?24:20);
      sfx(nearbyCount>3?"legendary":"epic");
      if(nearbyCount>3){setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);}
      vibrate([15,8,20,8,25]);
      unlock("beacon_tap");
      if(nearbyCount>=4)unlock("beacon_surge");
      mascotHappyRef.current+=2+nearbyCount;
      const cfgBn=levelCfgRef.current;
      if(cfgBn){if(gs.score>=cfgBn.scoreGoal&&(!cfgBn.modifier||checkModGoal(cfgBn.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // SHADOW — tap leaves a shadow_clone at same position; clone gives bonus if caught
    if(hit.type==="shadow"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=Math.round(100*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Spawn shadow clone at same position — 1.5s window
      targetsRef.current.push({
        id:Math.random().toString(36).slice(2),type:"shadow_clone",
        x:hit.x,y:hit.y,radius:BASE_R*0.9,color:"#4338ca",glow:"#6366f1",
        rarity:RARITY.RARE,lifetime:1500,spawnedAt:Date.now(),born:performance.now(),
        moving:false,ghost:false,vx:0,vy:0,trail:[],hitsLeft:1,maxHits:1,dying:null
      });
      spawnParticles(hit.x,hit.y,"#6366f1",12,"spark");
      spawnPopup(hit.x,hit.y-36,`🕶️ SHADOW! +${basePts} — catch clone!`,"#818cf8",20);
      sfx("rare");vibrate([12,6,12]);
      unlock("shadow_tap");
      mascotHappyRef.current+=2;
      const cfgSh=levelCfgRef.current;
      if(cfgSh){if(gs.score>=cfgSh.scoreGoal&&(!cfgSh.modifier||checkModGoal(cfgSh.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // SHADOW CLONE — bonus tap after a shadow target; short window
    if(hit.type==="shadow_clone"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const cloneBonus=Math.round(300*combo*feverMult*prestigeMult);
      gs.score+=cloneBonus;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      spawnParticles(hit.x,hit.y,"#c7d2fe",14,"spark");
      spawnPopup(hit.x,hit.y-40,`👤 CLONE CAUGHT! +${cloneBonus}`,"#c7d2fe",22);
      sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
      vibrate([15,8,25]);
      unlock("shadow_clone_catch");
      mascotHappyRef.current+=4;
      const cfgSc=levelCfgRef.current;
      if(cfgSc){if(gs.score>=cfgSc.scoreGoal&&(!cfgSc.modifier||checkModGoal(cfgSc.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // PORTAL — teleports all targets to random new positions; base score + chaos bonus
    if(hit.type==="portal"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      const teleported=targetsRef.current.filter(t=>!t.dying&&t.type!=="boss"&&t.type!=="bomb").length;
      const basePts=Math.round((100+teleported*30)*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      // Teleport all non-boss targets
      targetsRef.current.forEach(t=>{
        if(t.dying||t.type==="boss"||t.type==="bomb")return;
        const newX=t.radius+Math.random()*(cw-t.radius*2);
        const newY=t.radius+95+Math.random()*(ch-t.radius-100);
        spawnParticles(t.x,t.y,"#818cf8",6,"spark");
        t.x=newX;t.y=newY;
        if(t.trail)t.trail=[];
      });
      spawnParticles(hit.x,hit.y,"#818cf8",20,"spark");
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#818cf8",size:hit.radius*3.5,born:performance.now(),duration:800,alpha:0.7});
      spawnPopup(hit.x,hit.y-48,`🌀 PORTAL! ×${teleported} teleported! +${basePts}`,"#818cf8",teleported>5?24:20);
      sfx("legendary");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
      setScreenShake(true);setTimeout(()=>setScreenShake(false),350);
      vibrate([18,8,18,8,35]);
      unlock("portal_tap");
      if(teleported>=5)unlock("portal_chaos");
      mascotHappyRef.current+=2+Math.floor(teleported/2);
      const cfgP=levelCfgRef.current;
      if(cfgP){if(gs.score>=cfgP.scoreGoal&&(!cfgP.modifier||checkModGoal(cfgP.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // PARTICLE BOMB — explodes into 12 scoreable spark particles on tap
    if(hit.type==="particlebomb"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=Math.round(80*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      // Explosion of spark particles that fly outward and give points when they expire
      const BOMB_SPARKS=12;
      let sparkPts=0;
      for(let i=0;i<BOMB_SPARKS;i++){
        const angle=(i/BOMB_SPARKS)*Math.PI*2+Math.random()*0.3;
        const speed=2+Math.random()*3;
        const sparkColor=i%3===0?"#ffed4a":i%3===1?"#ff8c00":"#f43f5e";
        const travelTime=600+Math.random()*400;
        const landX=Math.max(30,Math.min(cw-30,hit.x+Math.cos(angle)*speed*travelTime*0.05));
        const landY=Math.max(100,Math.min(ch-30,hit.y+Math.sin(angle)*speed*travelTime*0.05));
        particlesRef.current.push({
          type:"dot",x:hit.x,y:hit.y,
          vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
          color:sparkColor,alpha:1,scale:1.5,born:performance.now(),duration:travelTime
        });
        setTimeout(()=>{
          const spts=Math.round(20*combo*feverMult*prestigeMult);
          sparkPts+=spts;gs.score+=spts;gs.sessionStats.score=gs.score;
          spawnParticles(landX,landY,sparkColor,4,"spark");
          spawnPopup(landX,landY-16,`+${spts}`,"#ff8c00",10);
        },travelTime);
      }
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#ff4500",size:hit.radius*2.5,born:performance.now(),duration:600,alpha:0.8});
      spawnParticles(hit.x,hit.y,"#ffed4a",16,"spark");
      spawnPopup(hit.x,hit.y-42,`💥 BOMB! +${basePts} +sparks!`,"#ff8c00",20);
      sfx("bossKill");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
      vibrate([20,8,20,8,40]);
      unlock("particlebomb_tap");
      mascotHappyRef.current+=3;
      const cfgBomb=levelCfgRef.current;
      if(cfgBomb){if(gs.score>=cfgBomb.scoreGoal&&(!cfgBomb.modifier||checkModGoal(cfgBomb.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // VOLTAGE — chain-zaps up to 3 nearby normal targets when tapped
    if(hit.type==="voltage"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=Math.round(120*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      spawnParticles(hit.x,hit.y,"#fbbf24",14,"spark");
      spawnPopup(hit.x,hit.y-36,`⚡ VOLTAGE! +${basePts}`,"#fbbf24",20);
      sfx("chainBonus");vibrate([10,5,20,5,10]);
      // Chain-zap up to 3 nearby targets within 100px
      const CHAIN_R=100;
      const nearby=targetsRef.current
        .filter(t=>!t.dying&&(t.type==="normal"||t.type==="phantom")&&Math.hypot(t.x-hit.x,t.y-hit.y)<CHAIN_R)
        .slice(0,3);
      nearby.forEach((zt,i)=>{
        setTimeout(()=>{
          if(!zt.dying){
            zt.dying=performance.now();
            const zpts=Math.round(60*combo*feverMult*prestigeMult);
            gs.score+=zpts;gs.sessionStats.score=gs.score;
            spawnParticles(zt.x,zt.y,"#facc15",8,"spark");
            spawnPopup(zt.x,zt.y-20,`⚡+${zpts}`,"#fbbf24",12);
            sfx("comboNote",gs.streak+i);
          }
        },i*120);
      });
      if(nearby.length>0)setNotif(`⚡ Chain zap! ×${nearby.length} targets!`);
      unlock("voltage_tap");
      mascotHappyRef.current+=1+nearby.length;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // VOID — absorbs up to 5 nearby targets for massive bonus score
    if(hit.type==="void"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const canvas=canvasRef.current;
      const VOID_R=120;
      const absorbed=targetsRef.current.filter(
        t=>!t.dying&&t.type!=="boss"&&t.type!=="bomb"&&t.type!=="siphon"&&Math.hypot(t.x-hit.x,t.y-hit.y)<VOID_R
      ).slice(0,5);
      // Remove absorbed targets
      const absorbedIds=new Set(absorbed.map(t=>t.id));
      targetsRef.current=targetsRef.current.filter(t=>!absorbedIds.has(t.id));
      const absorbBonus=absorbed.length*150;
      const basePts=Math.round((300+absorbBonus)*combo*feverMult*prestigeMult);
      gs.score+=basePts;gs.streak+=Math.min(3,absorbed.length);gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;gs.sessionStats.rareHits++;
      // Implosion particle effect
      absorbed.forEach(t=>{
        spawnParticles(t.x,t.y,"#a855f7",8,"spark");
      });
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#7c3aed",size:hit.radius*3,born:performance.now(),duration:700,alpha:0.8});
      spawnParticles(hit.x,hit.y,"#c084fc",18,"spark");
      spawnPopup(hit.x,hit.y-46,absorbed.length>0?`🌀 VOID! +${basePts} (×${absorbed.length+1} abs!)`:`🌀 VOID! +${basePts}`,"#c084fc",absorbed.length>2?26:22);
      if(absorbed.length>=3){sfx("legendary");setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),800);setScreenShake(true);setTimeout(()=>setScreenShake(false),400);}
      else{sfx("epic");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);}
      vibrate([20,8,20,8,40]);
      unlock("void_tap");
      if(absorbed.length>=3)unlock("void_master");
      mascotHappyRef.current+=2+absorbed.length;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // HOMING — scores based on how close it is to center when tapped
    if(hit.type==="homing"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      const centerDist=Math.hypot(hit.x-cw/2,hit.y-ch/2);
      const maxDist=Math.hypot(cw/2,ch/2);
      const proximityBonus=Math.max(0,1-centerDist/maxDist); // 0=edge, 1=center
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round((60+proximityBonus*140)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("comboNote",gs.streak);vibrate([10,5,10]);
      spawnParticles(hit.x,hit.y,"#34d399",12,"spark");
      const prxLabel=proximityBonus>0.8?"🎯 BULLSEYE!":proximityBonus>0.5?"✅ CLOSE!":"🟡 NEAR";
      spawnPopup(hit.x,hit.y-28,`${prxLabel} +${pts}`,"#4ade80",15+Math.floor(proximityBonus*6));
      if(proximityBonus>0.85)unlock("homing_center");
      unlock("homing_tap");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // VANISHING — bonus points if hit while invisible (blind timing)
    if(hit.type==="vanishing"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const cycleLen=800;
      const phase=(performance.now()%cycleLen)/cycleLen;
      const isVisible=phase<0.4;
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const basePts=isVisible?70:200; // blind hit = 200 base pts!
      const pts=Math.round(basePts*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx(isVisible?"comboNote":"legendary");vibrate(isVisible?[10,6,10]:[20,10,20,10,40]);
      spawnParticles(hit.x,hit.y,"#67e8f9",isVisible?8:16,"spark");
      const label=isVisible?`👻 VANISH! +${pts}`:`🎯 BLIND HIT! +${pts}`;
      const color=isVisible?"#bae6fd":"#ffd700";
      spawnPopup(hit.x,hit.y-30,label,color,isVisible?14:20);
      if(!isVisible){sfx("jackpot");unlock("vanishing_blind");}
      unlock("vanishing_tap");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // DIVIDER — scores points then splits into 2 medium moving targets
    if(hit.type==="divider"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(70*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("rare");vibrate([12,6,12]);
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      spawnParticles(hit.x,hit.y,"#fb923c",12,"spark");
      spawnPopup(hit.x,hit.y-28,`÷ SPLIT! +${pts}`,"#fdba74",15);
      // Spawn 2 medium sub-targets flying outward
      [0,1].forEach(si=>{
        const angle=(si===0?-0.4:0.4)+Math.random()*0.3-0.15;
        const speed=1.8+Math.random()*1.2;
        const subX=Math.max(hit.radius+20,Math.min(cw-hit.radius-20,hit.x));
        const subY=Math.max(hit.radius+100,Math.min(ch-hit.radius-20,hit.y));
        const subRar=RARITY.find(r=>r.name==="common");
        targetsRef.current.push({
          id:Math.random().toString(36).slice(2),type:"normal",
          x:subX,y:subY,radius:Math.round(hit.radius*0.62),
          color:"#fdba74",glow:"#f97316",rarity:subRar||RARITY[0],
          lifetime:2800,spawnedAt:Date.now(),born:performance.now(),
          moving:true,ghost:false,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,
          trail:[],hitsLeft:1,maxHits:1,dying:null,_isShard:true,
        });
      });
      unlock("divider_tap");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // RAGE — scores more points the more enraged (higher rageLevel) it is
    if(hit.type==="rage"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const rageLevel=Math.min(1,(Date.now()-hit.spawnedAt)/(hit.lifetime*0.9));
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round((80+rageLevel*220)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      const rageColor=rageLevel>0.7?"#dc2626":rageLevel>0.4?"#f97316":"#fbbf24";
      sfx("bossKill");vibrate([20,10,20]);
      spawnParticles(hit.x,hit.y,rageColor,14,"spark");
      spawnParticles(hit.x,hit.y,"#fca5a5",6,"dot");
      const rageLabel=rageLevel>0.8?"😡 MAX RAGE!":rageLevel>0.5?"😠 ENRAGED!":"😤 ANGRY!";
      spawnPopup(hit.x,hit.y-30,`${rageLabel} +${pts}`,rageColor,16+Math.floor(rageLevel*6));
      if(rageLevel>=0.8)unlock("rage_max");
      else unlock("rage_tap");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // CRYSTAL — shatters into 3 scoreable shards flying outward
    if(hit.type==="crystal"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(80*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("epic");vibrate([15,8,15]);
      const canvas=canvasRef.current;const cw=canvas?.width||390,ch=canvas?.height||700;
      spawnParticles(hit.x,hit.y,"#bfdbfe",12,"spark");
      spawnParticles(hit.x,hit.y,"#60a5fa",6,"dot");
      spawnPopup(hit.x,hit.y-30,`💎 CRYSTAL +${pts}`,"#93c5fd",16);
      // Spawn 3 shards flying outward
      const shardBorn=performance.now();
      const groupId=Math.random().toString(36).slice(2);
      [0,1,2].forEach(si=>{
        const angle=(si/3)*Math.PI*2+Math.random()*0.5;
        const flyDist=55+Math.random()*45;
        const sx=Math.max(hit.radius+20,Math.min(cw-hit.radius-20,hit.x+Math.cos(angle)*flyDist));
        const sy=Math.max(hit.radius+100,Math.min(ch-hit.radius-20,hit.y+Math.sin(angle)*flyDist));
        targetsRef.current.push({
          id:Math.random().toString(36).slice(2),type:"crystal_shard",
          x:sx,y:sy,radius:18,color:"#93c5fd",glow:"#3b82f6",
          rarity:hit.rarity,lifetime:2000,spawnedAt:Date.now(),born:shardBorn,
          moving:false,ghost:false,vx:0,vy:0,trail:[],
          hitsLeft:1,maxHits:1,dying:null,_shardBorn:shardBorn,_shardGroup:groupId,
        });
      });
      gs._crystalGroupId=groupId;gs._crystalShardsHit=0;
      unlock("crystal_shatter");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }
    // CRYSTAL SHARD — bonus score after crystal shatter
    if(hit.type==="crystal_shard"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round(45*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      sfx("comboNote",gs.streak);vibrate(8);
      spawnParticles(hit.x,hit.y,"#bfdbfe",7,"spark");
      spawnPopup(hit.x,hit.y-24,`✨ SHARD +${pts}`,"#bfdbfe",13);
      // Check if this is the third shard in the group
      if(hit._shardGroup&&gs._crystalGroupId===hit._shardGroup){
        gs._crystalShardsHit=(gs._crystalShardsHit||0)+1;
        if(gs._crystalShardsHit>=3){
          const bonus=Math.round(200*combo*feverMult*prestigeMult);
          gs.score+=bonus;
          spawnPopup(hit.x,hit.y-50,`💠 FULL CRYSTAL! +${bonus}`,"#60a5fa",20);
          sfx("legendary");vibrate([20,10,20,10,40]);
          unlock("crystal_chain");
        }
      }
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // TORNADO — scrambles nearby target positions in a vortex, then scores
    if(hit.type==="tornado"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const VORTEX_R=120;
      let vortexCount=0;
      targetsRef.current.forEach(t=>{
        if(t.dying||t.type==="boss")return;
        const dx=t.x-hit.x,dy=t.y-hit.y;
        const dist=Math.hypot(dx,dy);
        if(dist<VORTEX_R&&dist>0){
          const angle=Math.atan2(dy,dx)+Math.PI/2; // perpendicular (tangential kick)
          const force=((VORTEX_R-dist)/VORTEX_R)*40;
          t.x=Math.max(t.radius+10,Math.min(canvasRef.current?.width||390-t.radius-10,t.x+Math.cos(angle)*force));
          t.y=Math.max(t.radius+100,Math.min(canvasRef.current?.height||700-t.radius-10,t.y+Math.sin(angle)*force));
          vortexCount++;
        }
      });
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const pts=Math.round((150+vortexCount*30)*combo*feverMult*prestigeMult);
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      hit.dying=performance.now();
      sfx("chainBonus");vibrate([10,5,15,5,10]);
      spawnParticles(hit.x,hit.y,"#67e8f9",25,"spark");
      spawnPopup(hit.x,hit.y-30,`🌀 VORTEX! +${pts}`,"#67e8f9",18);
      if(vortexCount>=3)spawnPopup(hit.x,hit.y-52,`×${vortexCount} SCATTER!`,"#06b6d4",13);
      setEpicFlash(true);setTimeout(()=>setEpicFlash(false),400);
      unlock("tornado_catch");
      mascotHappyRef.current++;
      const cfg=levelCfgRef.current;
      if(cfg){if(gs.score>=cfg.scoreGoal&&(!cfg.modifier||checkModGoal(cfg.modifier,gs))){endLevel(true);return;}}
      return;
    }

    // LOOT CHEST — drops 3-5 coins and bonus points on tap
    if(hit.type==="lootchest"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const coinDrop=3+Math.floor(Math.random()*3); // 3-5 coins
      const combo=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult=gs.feverActive?2:1;
      const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const isMultiplierL=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
      const pts=Math.round(80*combo*feverMult*prestigeMult*(isMultiplierL?3:1));
      gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();
      gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
      saveRef.current.coins=(saveRef.current.coins||0)+coinDrop;
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+coinDrop;
      hit.dying=performance.now();
      sfx("coin");sfx("treasure");vibrate([10,5,20,5,30]);
      spawnParticles(hit.x,hit.y,"#ffd700",25,"spark");
      spawnParticles(hit.x,hit.y,"#fef3c7",10,"dot");
      spawnPopup(hit.x,hit.y-28,`🪙 ×${coinDrop} +${pts}`,"#ffd700",20);
      // Cascade: 3 coin popups raining down
      for(let i=0;i<coinDrop;i++){
        const ox=(Math.random()-0.5)*60,oy=-(20+i*18);
        setTimeout(()=>spawnPopup(hit.x+ox,hit.y+oy,"🪙","#ffd700",14),i*80);
      }
      unlock("loot_chest");
      mascotHappyRef.current+=2;
      debounceSave();
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
      // Double-tap defuse: tapping same bomb twice within 200ms defuses it for 25pts
      const nowBomb=Date.now();
      if(hit._firstTap&&(nowBomb-hit._firstTap)<200){
        // Defuse! Remove without penalty
        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
        sfx("rare");vibrate([10,5,10]);
        spawnParticles(hit.x,hit.y,"#4ade80",14,"spark");
        spawnPopup(hit.x,hit.y-22,"💚 DEFUSED! +25","#4ade80",16);
        gs.score+=25;gs.sessionStats.score=gs.score;
        unlock("bomb_defuse");
        return;
      }
      hit._firstTap=nowBomb;
      setTimeout(()=>{if(hit._firstTap===nowBomb)hit._firstTap=null;},200);
      // Normal bomb hit
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
        const taunt2=BOSS_TAUNTS.phase2[Math.floor(Math.random()*BOSS_TAUNTS.phase2.length)];
        setBossTaunt({text:taunt2,phase:2});setTimeout(()=>setBossTaunt(null),3500);
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
        const taunt3=BOSS_TAUNTS.phase3[Math.floor(Math.random()*BOSS_TAUNTS.phase3.length)];
        setBossTaunt({text:taunt3,phase:3});setTimeout(()=>setBossTaunt(null),4000);
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
        const dyingTaunt=BOSS_TAUNTS.dying[Math.floor(Math.random()*BOSS_TAUNTS.dying.length)];
        setBossTaunt({text:dyingTaunt,phase:"dying"});setTimeout(()=>setBossTaunt(null),3000);
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
    const isMultiplier=activePwrRef.current.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
    const feverMult=gs.feverActive?2:1;
    const timeLeft=1-(Date.now()-hit.spawnedAt)/hit.lifetime;
    const ceLevel=(saveRef.current.skills||{}).critical_eye||0;
    const perfectZone=0.38*(ceLevel===3?1.35:ceLevel===2?1.20:ceLevel===1?1.10:1.0);
    const isPerfect=hitDist<hit.radius*perfectZone&&timeLeft>0.36&&timeLeft<0.67;
    const isLastBreath=timeLeft<0.08&&hit.type==="normal"; // caught in last 8% of life
    // Prestige score multiplier (+5% per prestige level, max 5 prestiges = +25%)
    const prestigeMult=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
    const shardMult=hit._isShard?0.5:1; // splitter shards award half points
    const poisonMult=gs._poisonedUntil&&Date.now()<gs._poisonedUntil?0.5:1; // poison debuff
    if(poisonMult<1)gs._poisonedUntil=null; // consume debuff after one hit
    const scoreBoostMult=(gs._scoreBoostTaps||0)>0?5:1;
    if(scoreBoostMult>1){gs._scoreBoostTaps--;if(gs._scoreBoostTaps<=0)setNotif("×5 boost ended!");}
    // Beacon bonus: if any active beacon within 110px, target scores 2×
    const BEACON_RANGE=110;
    const beaconActive=targetsRef.current.some(t=>t.type==="beacon"&&!t.dying&&Math.hypot(t.x-hit.x,t.y-hit.y)<BEACON_RANGE);
    const beaconMult=beaconActive?2:1;
    const overclockMult=(gs._overclockEndsAt&&Date.now()<gs._overclockEndsAt)?2:1;
    // Bounty Board bonus: matching rarity gives 2-5× extra points
    const bounty=bountyRef.current;
    const bountyHit=bounty&&bounty.expiresAt>Date.now()&&hit.rarity?.name===bounty.rarity;
    const bountyMult=bountyHit?bounty.mult:1;
    const pts=Math.round(hit.rarity.mult*combo*feverMult*(isDouble?2:1)*(isMultiplier?3:1)*(isPerfect?1.5:1)*(isLastBreath?1.5:1)*prestigeMult*shardMult*poisonMult*scoreBoostMult*beaconMult*overclockMult*bountyMult);
    gs.score+=pts;
    if(bountyHit){
      spawnPopup(hit.x,hit.y-38,`🎯 BOUNTY! ×${bounty.mult} +${pts}`,bounty.color,22);
      spawnParticles(hit.x,hit.y,bounty.color,16,"spark");
      sfx("chainBonus");vibrate([12,6,18]);
      gs._bountyHits=(gs._bountyHits||0)+1;
      if(gs._bountyHits>=3)unlock("bounty_hit");
      // Reset bounty after hit — next one in 8s
      bountyRef.current=null;setBountyData(null);
      if(bountyTimerRef.current)clearTimeout(bountyTimerRef.current);
      bountyTimerRef.current=setTimeout(()=>{
        if(!gsRef.current||gsRef.current.lives<=0)return;
        const BOUNTY_POOL2=[{rarity:"UNCOMMON",icon:"⚪",mult:2,color:"#94a3b8"},{rarity:"RARE",icon:"🔵",mult:3,color:"#60a5fa"},{rarity:"EPIC",icon:"🟣",mult:4,color:"#c084fc"},{rarity:"LEGENDARY",icon:"🟡",mult:5,color:"#ffd700"}];
        const b=BOUNTY_POOL2[Math.floor(Math.random()*BOUNTY_POOL2.length)];
        const bd={...b,expiresAt:Date.now()+35000};bountyRef.current=bd;setBountyData(bd);
        bountyTimerRef.current=setTimeout(()=>{bountyRef.current=null;setBountyData(null);},35000);
      },8000);
    }
    if(scoreBoostMult>1){spawnParticles(hit.x,hit.y,"#f43f5e",8,"spark");}
    // Prestige aura — golden shockwave on each tap when prestige ≥ 1
    if((saveRef.current.prestigeLevel||0)>=1){
      particlesRef.current.push({type:"shockwave",x:hit.x,y:hit.y,color:"#ffd700",
        size:hit.radius*1.2,born:performance.now(),duration:500,alpha:0.55+(saveRef.current.prestigeLevel||0)*0.06});
    }
    // Proximity chain bonus — if tapped within 300ms AND within 80px of last tap
    const nowMs=Date.now();
    if(gs._lastTapX!==undefined&&gs._lastTapY!==undefined&&gs._lastTapMs&&
       (nowMs-gs._lastTapMs)<300&&Math.hypot(hit.x-gs._lastTapX,hit.y-gs._lastTapY)<80){
      const chainPts=Math.round(pts*0.4);
      if(chainPts>0){
        gs.score+=chainPts;
        spawnPopup(hit.x,hit.y-42,`🔗 CHAIN +${chainPts}`,"#a78bfa",13);
      }
    }
    gs._lastTapX=hit.x;gs._lastTapY=hit.y;gs._lastTapMs=nowMs;
    if(gs._magnetFieldEndsAt&&Date.now()<gs._magnetFieldEndsAt){gs._magnetFieldX=hit.x;gs._magnetFieldY=hit.y;}
    // Tap Frenzy — 5 hits within 2s triggers bonus
    if(!gs._recentTaps)gs._recentTaps=[];
    gs._recentTaps.push(nowMs);
    gs._recentTaps=gs._recentTaps.filter(t=>nowMs-t<2000);
    if(gs._recentTaps.length>=5&&!gs._frenzyAt){
      gs._frenzyAt=nowMs;
      const frenzyBonus=Math.round(150*(gs.feverActive?2:1)*(1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05)));
      gs.score+=frenzyBonus;
      const canvas=canvasRef.current;
      spawnPopup(canvas?.width/2||195,(canvas?.height||700)*0.38,`⚡ TAP FRENZY! +${frenzyBonus}`,"#f97316",22);
      sfx("chainBonus");vibrate([15,8,15,8,30]);
      setTimeout(()=>{if(gsRef.current)gsRef.current._frenzyAt=null;},2000);
      unlock("tap_frenzy");
    }
    // Lucky Streak — 7 consecutive hits without any miss gives coin jackpot
    gs._luckyTaps=(gs._luckyTaps||0)+1;
    if(gs._luckyTaps===7){
      gs._luckyTaps=0;
      const luckyCoins=10+Math.floor(Math.random()*15);
      saveRef.current.coins=(saveRef.current.coins||0)+luckyCoins;
      saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+luckyCoins;
      debounceSave();
      const canvas=canvasRef.current;
      spawnPopup(canvas?.width/2||195,(canvas?.height||700)*0.32,`🍀 LUCKY STREAK! +${luckyCoins}🪙`,"#ffd700",20);
      sfx("coin");vibrate([8,6,8,6,15]);
      unlock("lucky_streak");
    }
    // Track last rarity for Mimic targets
    gs.lastRarityMult=hit.rarity.mult;
    gs.lastRarityColor=hit.color;
    gs.lastRarityName=hit.rarity.name;
    // 9B — Mascot happiness — session tap milestone triggers dialogue + bonus
    mascotHappyRef.current=(mascotHappyRef.current||0)+1;
    const happyCount=mascotHappyRef.current;
    if(happyCount===25||happyCount===50||happyCount===75){
      const happyMascot=MASCOTS.find(m=>m.id===(saveRef.current.mascotId||"dragon"));
      const msgs=happyMascot?.speeches?.happy||["Great job!"];
      showMascotSpeech("happy");
      if(happyCount===50){
        // 50-tap milestone: +50 score bonus
        gs.score+=50;
        spawnPopup(hit.x,hit.y-55,`${happyMascot?.emoji?.happy||"🌟"} HAPPY BOOST! +50`,"#fbbf24",16);
      }
      if(happyCount===75){
        // 75-tap milestone: instant 3× score multiplier for 5s (handled via feverMult override)
        spawnPopup(hit.x,hit.y-55,"🌈 MASCOT FEVER! +100","#ff00ff",18);
        gs.score+=100;sfx("mascotNote",25,440,"sine");vibrate([20,10,20,10,40]);
      }
    }
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
    const goldRushActive=gs._goldRushEndsAt&&Date.now()<gs._goldRushEndsAt;
    const coinMult=(mLvlNow>=5?1.05:1)*coinSkillMult*(goldRushActive?3:1);
    const baseCoin=Math.max(1,Math.floor(pts*0.09*coinMult));
    const bountyCoin=hit._isBounty?baseCoin*2:0; // Bounty target gives 3× coins (base + 2× bonus)
    saveRef.current.coins=(saveRef.current.coins||0)+baseCoin+bountyCoin;
    saveRef.current.totalCoins=(saveRef.current.totalCoins||0)+baseCoin+bountyCoin;
    if(bountyCoin>0){spawnPopup(hit.x,hit.y-44,`👑 BOUNTY! +${bountyCoin}🪙`,"#ffd700",15);sfx("coin");unlock("bounty_hit");}
    if(goldRushActive&&baseCoin>0&&Math.random()<0.25){spawnPopup(hit.x,hit.y-50,`🥇 ×3 GOLD!`,"#ffd700",13);}
    // Trigger Gold Rush — rare chance on legendary or loot chest hit
    if(!goldRushActive&&!gs._goldRushEndsAt&&(hit.rarity?.name==="legendary"||hit.type==="lootchest")&&Math.random()<0.12){
      gs._goldRushEndsAt=Date.now()+9000;
      setGoldRushMode(true);setTimeout(()=>setGoldRushMode(false),9000);
      sfx("jackpot");vibrate([30,15,30,15,60]);
      const canvas=canvasRef.current;
      spawnPopup(canvas?.width/2||195,canvas?.height/3||230,"🥇 GOLD RUSH! 3× COINS","#ffd700",22);
      unlock("gold_rush");
    }

    gs.sessionStats.tapsTotal++;gs.sessionStats.score=gs.score;
    if(hit.rarity.name!=="common")gs.sessionStats.rareHits++;
    if(gs.streak>gs.sessionStats.bestCombo)gs.sessionStats.bestCombo=gs.streak;
    if(isPerfect){gs.sessionStats.perfectTaps=(gs.sessionStats.perfectTaps||0)+1;}

    // First-tap fever: if very first tap of a level hits rare+, grant 3s mini-fever
    if(gs.sessionStats.tapsTotal===1&&!gs.feverActive&&(hit.rarity.name==="rare"||hit.rarity.name==="epic"||hit.rarity.name==="legendary")){
      gs.feverActive=true;gs.feverTimeLeft=3000;
      setFeverBorder(true);sfx("feverStart");vibrate([25,12,25]);
      spawnPopup(hit.x,hit.y-40,"🔥 FIRST TAP FEVER!","#f97316",20);
      unlock("first_tap_fever");
    }

    // New personal best streak notification
    if(gs.streak>5&&gs.streak>(saveRef.current.bestStreak||0)&&!gs._streakPBNotified){
      gs._streakPBNotified=gs.streak;
      spawnPopup(hit.x,hit.y-58,`🏆 NEW STREAK PB: ${gs.streak}×!`,"#34d399",15);
      saveRef.current.bestStreak=gs.streak;
    }
    // Activate streak shield at streak 10
    if(gs.streak===10&&!streakShRef.current){streakShRef.current=true;setStreakShieldActive(true);sfx("lucky");}
    // Combo Shield auto-recharge at streak 15 (if shield was lost)
    if(gs.streak===15&&!streakShRef.current){
      streakShRef.current=true;setStreakShieldActive(true);sfx("lucky");
      const canvas3=canvasRef.current;
      spawnPopup(canvas3?.width/2||195,(canvas3?.height||700)*0.28,"🛡 SHIELD RECHARGED!","#fbbf24",18);
      vibrate([15,8,15]);
    }
    // Fury Mode: streak ≥35 triggers a purple border effect + bonus
    if(gs.streak===35){
      const canvas3=canvasRef.current;const cw35=canvas3?.width||390;const ch35=canvas3?.height||700;
      const furyColors=["#a855f7","#7c3aed","#f97316","#ffd700"];
      furyColors.forEach((c,i)=>setTimeout(()=>spawnParticles(cw35/2,ch35/2,c,14,"spark"),i*65));
      sfx("legendary");vibrate([25,10,25,10,50]);
      spawnPopup(cw35/2,ch35*0.22,"🌑 FURY MODE!","#a855f7",24);
      unlock("fury_mode");
    }
    // Mascot mood
    if(gs.streak>=35)setMascotMood("fire");
    else if(gs.streak>=20)setMascotMood("fire");
    else if(gs.streak>=10)setMascotMood("excited");
    else if(gs.streak>=5)setMascotMood("happy");
    else setMascotMood("idle");
    // Mascot bounce on every hit
    mascotBouncePlay();
    // Streak milestone burst celebrations + speech
    {const MILESTONES=[{n:5,label:"🔥 ON FIRE!",color:"#fbbf24"},{n:10,label:"⚡ UNSTOPPABLE!",color:"#f97316"},{n:20,label:"💥 LEGENDARY!",color:"#ef4444"},{n:25,label:"🌟 SUPERSTAR!",color:"#c084fc"},{n:30,label:"🌈 GODLIKE!!!",color:"#ff00ff"},{n:50,label:"👑 TRANSCENDENT!",color:"#ffd700"}];
    const ms=MILESTONES.find(m=>m.n===gs.streak);
    if(ms){
      setStreakBurst(ms);setTimeout(()=>setStreakBurst(null),ms.n>=50?1800:1200);showMascotSpeech("streak");
      // 25x: shockwave ring explosion
      if(ms.n===25){
        const canvas=canvasRef.current;const cw2=canvas?canvas.width:390;const ch2=canvas?canvas.height:700;
        const cols=["#c084fc","#a78bfa","#60a5fa","#fbbf24"];
        cols.forEach((c,i)=>setTimeout(()=>spawnParticles(cw2/2,ch2/2,c,12,"spark"),i*55));
        spawnParticles(cw2/2,ch2/2,"#fff",8,"shockwave");
        sfx("chainBonus");vibrate([20,10,20,10,45]);
        setEpicFlash(true);setTimeout(()=>setEpicFlash(false),500);
      }
      // 50x: rainbow explosion across the whole canvas
      if(ms.n>=50){
        const canvas=canvasRef.current;const cw2=canvas?canvas.width:390;const ch2=canvas?canvas.height:700;
        const colors=["#ff6030","#ffd700","#34d399","#60a5fa","#f472b6","#a78bfa","#ff6b35"];
        colors.forEach((c,i)=>setTimeout(()=>spawnParticles(cw2/2,ch2/2,c,15,"spark"),i*80));
        sfx("jackpot");vibrate([30,10,30,10,30,10,80]);
        setLegendaryFlash(true);setTimeout(()=>setLegendaryFlash(false),1000);
      }
    }}

    // Musical pentatonic scale note (most addictive mechanic!) — rising melody as streak grows
    sfx("comboNote", gs.streak);

    // Check personal best mid-game — firework burst when record is broken
    if(gs.score>saveRef.current.highScore&&gs.score>200&&!newRecord){
      setNewRecord(true);setTimeout(()=>setNewRecord(false),2000);
      const canvas=canvasRef.current;const cw3=canvas?canvas.width:390;const ch3=canvas?canvas.height:700;
      const fwColors=["#ffd700","#ff6b35","#34d399","#60a5fa","#f472b6","#a78bfa"];
      // 3 firework bursts at different positions
      [[cw3*0.25,ch3*0.3],[cw3*0.75,ch3*0.25],[cw3*0.5,ch3*0.2]].forEach(([fx,fy],i)=>{
        setTimeout(()=>spawnParticles(fx,fy,fwColors[i*2]||"#ffd700",22,"spark"),i*180);
      });
      sfx("jackpot");vibrate([20,10,20,10,20]);
    }

    // Score milestones — mini celebration at key point thresholds
    {const SCORE_MILESTONES=[1000,2500,5000,10000,20000,50000];
    const prevScore=gs.score-pts;
    const crossed=SCORE_MILESTONES.find(m=>prevScore<m&&gs.score>=m);
    if(crossed&&!cfg?.isZen){
      const canvas2=canvasRef.current;const cw4=canvas2?.width||390,ch4=canvas2?.height||700;
      const isEpic=crossed>=10000;
      const milestoneColor=isEpic?"#ffd700":crossed>=5000?"#c084fc":crossed>=2500?"#f97316":"#34d399";
      spawnPopup(cw4/2,ch4*0.28,`🏅 ${crossed.toLocaleString()} PTS!`,milestoneColor,isEpic?24:20);
      spawnParticles(cw4/2,ch4*0.3,milestoneColor,isEpic?20:12,"spark");
      if(isEpic){sfx("legendary");setEpicFlash(true);setTimeout(()=>setEpicFlash(false),400);unlock("score_10k");}
      else sfx("chainBonus");
      vibrate(isEpic?[15,8,15,8,25]:[10,5,15]);
    }}

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
    // Last-Breath bonus visual
    if(isLastBreath){
      spawnPopup(hit.x,hit.y-38,"⏰ LAST BREATH! ×1.5","#fb923c",15);
      sfx("nearMiss"); // distinctive sound for near-miss catch
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
    // Score milestone celebration — every 500 points
    const prevM=Math.floor((gs.score-pts)/500);
    const newM=Math.floor(gs.score/500);
    if(newM>prevM&&newM>0){
      const milestoneScore=newM*500;
      spawnParticles(hit.x,hit.y,"#ffd700",20,"spark");
      spawnPopup(hit.x,hit.y-50,`🏅 ${milestoneScore.toLocaleString()}!`,"#ffd700",17);
    }
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
    _hapticIntensity=saveRef.current.hapticIntensity??70;
    initMissions();
    initBgParts(cfg.world);
    targetsRef.current=[];particlesRef.current=[];activePwrRef.current=[];ripplesRef.current=[];tapTrailRef.current=[];
    spawnTimer.current=0;pausedRef.current=false;setPaused(false);
    mascotHappyRef.current=0; // reset session happiness
    streakShRef.current=false;setStreakShieldActive(false);setNewRecord(false);setCloseBanner(false);setRushMode(false);setBossTaunt(null);setGoldRushMode(false);
    luckyRef.current=null;if(luckyTimer.current)clearTimeout(luckyTimer.current);
    // Schedule first lucky event 45-70 seconds in
    luckyTimer.current=setTimeout(()=>triggerLucky(),45000+Math.random()*25000);
    // Bounty Board — first bounty after 12 seconds, then every 35s
    bountyRef.current=null;setBountyData(null);
    if(bountyTimerRef.current)clearTimeout(bountyTimerRef.current);
    const BOUNTY_POOL=[
      {rarity:"UNCOMMON",icon:"⚪",mult:2,color:"#94a3b8"},
      {rarity:"RARE",icon:"🔵",mult:3,color:"#60a5fa"},
      {rarity:"EPIC",icon:"🟣",mult:4,color:"#c084fc"},
      {rarity:"LEGENDARY",icon:"🟡",mult:5,color:"#ffd700"},
    ];
    const pickBounty=()=>{
      if(!gsRef.current||gsRef.current.lives<=0)return;
      const b=BOUNTY_POOL[Math.floor(Math.random()*BOUNTY_POOL.length)];
      const bd={...b,expiresAt:Date.now()+35000};
      bountyRef.current=bd;setBountyData(bd);
      bountyTimerRef.current=setTimeout(()=>{bountyRef.current=null;setBountyData(null);bountyTimerRef.current=setTimeout(pickBounty,5000);},35000);
    };
    bountyTimerRef.current=setTimeout(pickBounty,12000);

    const extraLife=shopCart.includes("extra_life");
    const headStart=shopCart.includes("head_start");
    const shieldStart=shopCart.includes("shield_start");
    const powerPack=shopCart.includes("power_pack");
    const feverPotion=shopCart.includes("fever_potion");
    const xpBomb=shopCart.includes("xp_bomb");
    const streakSaver=shopCart.includes("streak_saver");
    const timeWarpStart=shopCart.includes("time_warp_start");
    const doubleSpawn=shopCart.includes("double_spawn");

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
      _timeWarpEndsAt:timeWarpStart?Date.now()+6000:null,
      _doubleSpawnActive:!!doubleSpawn,
    };
    if(hasStreakShield&&!isRescue){streakShRef.current=true;setStreakShieldActive(true);}
    if(shieldStart)activePwrRef.current=[{type:"SHIELD",endsAt:Date.now()+25000}];
    if(powerPack){const pt=["SLOW","DOUBLE","SHIELD","FREEZE"];const ty=pt[Math.floor(Math.random()*pt.length)];if(!activePwrRef.current.find(p=>p.type===ty))activePwrRef.current.push({type:ty,endsAt:Date.now()+12000});}
    if(feverPotion){setFeverBorder(true);sfx("feverStart");}
    if(timeWarpStart){activePwrRef.current.push({type:"TIME_WARP",endsAt:Date.now()+6000});setTimeout(()=>setNotif("⏱️ Time Warp active!"),600);}
    if(doubleSpawn){setTimeout(()=>setNotif("🌊 Target Rush! 2× spawns!"),600);}
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
  // Keep ref in sync for forward-reference calls from activatePowerUp
  React.useEffect(()=>{triggerLuckyRef.current=triggerLucky;},[triggerLucky]);

  // Pause
  const togglePause=useCallback(()=>{
    if(!gsRef.current)return;
    const next=!pausedRef.current;pausedRef.current=next;setPaused(next);
    if(!next){lastTickRef.current=performance.now();rafRef.current=requestAnimationFrame(gl=>gameLoopFn(gl));}
  },[]);// eslint-disable-line

  useEffect(()=>()=>{if(rafRef.current)cancelAnimationFrame(rafRef.current);},[]);

  // Menu canvas loop
  useEffect(()=>{
    if(screen!=="menu"&&screen!=="levelmap"&&screen!=="shop"&&screen!=="levelcomplete"&&screen!=="gameover"&&screen!=="spinwheel"&&screen!=="missions"&&screen!=="achievements"&&screen!=="leaderboard"&&screen!=="settings"&&screen!=="infinity"&&screen!=="gauntlet"&&screen!=="mascotcollection"&&screen!=="weekly"&&screen!=="tournament"&&screen!=="skilltree"&&screen!=="zen"&&screen!=="timeattack")return;
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
    drawTapTrail(ctx,tapTrailRef.current,accentColor,gsRef.current?.streak||0);

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
          const timeWarpMult=gs._timeWarpEndsAt&&Date.now()<gs._timeWarpEndsAt?0.2:1;
          // Comet and Ice Comet fly straight without bouncing
          if(t.type==="comet"||t.type==="icecomet"){
            t.x+=t.vx*dt*0.072*timeWarpMult;t.y+=t.vy*dt*0.072*timeWarpMult;
            // Off-screen removal (handled by expiry)
          } else
          // Rage target accelerates over its lifetime
          if(t.type==="rage"){
            const rl=Math.min(1,(now-t.spawnedAt)/(t.lifetime*0.9));
            const speedScale=0.056*(1+rl*3.5)*timeWarpMult; // up to 4.5× faster at max rage
            t.x+=t.vx*dt*speedScale;t.y+=t.vy*dt*speedScale;
          } else if(t.type==="homing"){
            // Homing: gently steers toward screen center
            const cx2=w/2,cy2=Math.min(h*0.52,h-80);
            const dx2=cx2-t.x,dy2=cy2-t.y;
            const dist2=Math.hypot(dx2,dy2)||1;
            const steer=0.018*timeWarpMult;
            t.vx+=dx2/dist2*steer;t.vy+=dy2/dist2*steer;
            const spd=Math.hypot(t.vx,t.vy);if(spd>1.4){t.vx=t.vx/spd*1.4;t.vy=t.vy/spd*1.4;}
            t.x+=t.vx*dt*0.056*timeWarpMult;t.y+=t.vy*dt*0.056*timeWarpMult;
          } else {
            t.x+=t.vx*dt*0.056*timeWarpMult;t.y+=t.vy*dt*0.056*timeWarpMult;
          }
          // MAGNET FIELD — all non-boss targets drift toward last tap position
          if(gs._magnetFieldEndsAt&&Date.now()<gs._magnetFieldEndsAt&&t.type!=="boss"&&t.type!=="bomb"&&t.type!=="siphon"){
            const mfx=gs._magnetFieldX||w/2,mfy=gs._magnetFieldY||h/2;
            const mdx=mfx-t.x,mdy=mfy-t.y;
            const mDist=Math.hypot(mdx,mdy)||1;
            if(mDist>30){
              const pull=0.012;
              t.vx+=mdx/mDist*pull;t.vy+=mdy/mDist*pull;
              const spd=Math.hypot(t.vx,t.vy);if(spd>1.8){t.vx=t.vx/spd*1.8;t.vy=t.vy/spd*1.8;}
            }
          }
          const margin=t.radius+5;
          if(t.x<margin||t.x>w-margin){t.vx*=-1;t.x=Math.max(margin,Math.min(w-margin,t.x));}
          if(t.y<t.radius+95||t.y>h-margin){t.vy*=-1;t.y=Math.max(t.radius+95,Math.min(h-margin,t.y));}
        }
        if(t.trail){t.trail.push({x:t.x,y:t.y});if(t.trail.length>12)t.trail.shift();}
      }
      // Glitch teleport — jumps to a random valid position every 0.9s
      if(t.type==="glitch"&&!t.dying){
        if(!t._lastGlitch)t._lastGlitch=now;
        if(now-t._lastGlitch>=900){
          t._lastGlitch=now;
          const margin=t.radius+10;
          t.x=margin+Math.random()*(w-margin*2);
          t.y=(t.radius+100)+Math.random()*(h-(t.radius+100)-margin);
          spawnParticles(t.x,t.y,"#00ff88",5,"spark");
        }
      }
      // Edge Danger Zone — stationary normal targets within 20px of screen edges flash and explode after 1.5s
      if(!t.moving&&!t.dying&&t.type==="normal"&&!t._isShard&&!cfg?.isZen){
        const EDGE=22;
        const nearEdge=t.x<EDGE||t.x>w-EDGE||t.y<t.radius+95+EDGE||t.y>h-EDGE;
        if(nearEdge){
          if(!t._edgeWarnAt)t._edgeWarnAt=now;
          const edgeAge=now-t._edgeWarnAt;
          if(edgeAge>=1500){
            // Explode! Cost a life if no shield
            spawnParticles(t.x,t.y,"#ef4444",18,"spark");
            spawnPopup(t.x,t.y-24,"⚠️ EDGE!","#ef4444",16);
            sfx("miss");vibrate([20,10,20]);
            const hasShieldE=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
            if(hasShieldE){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
            else if(streakShRef.current){streakShRef.current=false;setStreakShieldActive(false);sfx("shieldBreak");}
            else{gs.lives--;gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);setMascotMood("sad");lostLife=true;}
            return false;
          }
        } else {
          t._edgeWarnAt=null;
        }
      }
      // Gravity Orb — pulls ALL non-bomb targets toward its center
      if(t.type==="gravityorb"&&!t.dying){
        const GORB_R=160,GORB_STR=0.022;
        targetsRef.current.forEach(other=>{
          if(other===t||other.dying||other.type==="boss"||other.type==="bomb"||other.type==="timebomb")return;
          const dx=t.x-other.x,dy=t.y-other.y;
          const dist=Math.hypot(dx,dy);
          if(dist>0&&dist<GORB_R){
            const force=GORB_STR*(1-dist/GORB_R)*dt;
            if(!other._gravLocked){other.vx=(other.vx||0)+(dx/dist)*force*2;other.vy=(other.vy||0)+(dy/dist)*force*2;other.moving=true;}
          }
        });
      }
      // 10B — Magnet pull: attract nearby normal targets toward this magnet
      if(t.type==="magnet"&&!t.dying){
        const PULL_R=110,PULL_STR=0.018;
        targetsRef.current.forEach(other=>{
          if(other===t||other.dying||other.type!=="normal")return;
          const dx=t.x-other.x,dy=t.y-other.y;
          const dist=Math.hypot(dx,dy);
          if(dist>0&&dist<PULL_R){
            const force=PULL_STR*(1-dist/PULL_R)*dt;
            other.x+=dx/dist*force*2;
            other.y+=dy/dist*force*2;
          }
        });
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
        // PHOENIX expired — respawns once as phoenix2 (risen form)
        if(t.type==="phoenix"&&!t._hasRisen){
          spawnParticles(t.x,t.y,"#f97316",12,"spark");
          targetsRef.current.push({
            id:Math.random().toString(36).slice(2),type:"phoenix2",
            x:t.x,y:t.y,radius:BASE_R*1.4,color:"#c084fc",glow:"#7c3aed",
            rarity:RARITY.EPIC,lifetime:3000,spawnedAt:Date.now(),born:performance.now(),
            moving:t.moving,ghost:false,vx:t.vx*-0.5,vy:t.vy*-0.5,trail:[],
            hitsLeft:1,maxHits:1,dying:null,_hasRisen:true
          });
          return false; // remove original
        }
        // THUNDERBOLT exits screen — costs 1 life (it "struck" without being caught)
        if(t.type==="thunderbolt"){
          spawnParticles(t.x,Math.min(h-20,t.y),"#facc15",14,"spark");
          spawnPopup(t.x,Math.min(h-40,t.y-20),"⚡ MISSED! -1 LIFE","#facc15",16);
          sfx("miss");vibrate([20,10,20]);
          const hasShTb=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now)||activePwrRef.current.find(p=>p.type==="SHIELD_WALL"&&p.endsAt>now);
          if(hasShTb&&typeof hasShTb==="object"){
            const sw=hasShTb;sw.hitsLeft=(sw.hitsLeft||1)-1;
            if(sw.hitsLeft<=0){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD_WALL");setActivePwrDisp([...activePwrRef.current]);}
          } else if(typeof hasShTb==="boolean"&&hasShTb){
            activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);
          } else{gs.lives=Math.max(0,gs.lives-1);gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);lostLife=true;}
          return false;
        }
        // TIME BOMB detonation — costs 2 lives, removes nearby targets, screen shake
        if(t.type==="timebomb"){
          const BLAST_R=120;
          const blasted=targetsRef.current.filter(o=>o!==t&&!o.dying&&Math.hypot(o.x-t.x,o.y-t.y)<BLAST_R&&o.type!=="boss");
          blasted.forEach(o=>{o.dying=performance.now();spawnParticles(o.x,o.y,"#f97316",6,"spark");});
          spawnParticles(t.x,t.y,"#f97316",35,"spark");spawnParticles(t.x,t.y,"#ef4444",20,"dot");
          particlesRef.current.push({type:"shockwave",x:t.x,y:t.y,color:"#f97316",size:BLAST_R*1.4,born:performance.now(),duration:700,alpha:0.85});
          spawnPopup(t.x,t.y-32,"💣 BOOM! −2 LIVES","#ef4444",20);
          sfx("miss");vibrate([30,15,30,15,40]);setScreenShake(true);setTimeout(()=>setScreenShake(false),500);
          const hasShTB=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
          if(hasShTB){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
          else{gs.lives=Math.max(0,gs.lives-2);gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);lostLife=true;}
          if(gs.lives<=0){endLevel(false);return false;}
          return false;
        }
        // SIPHON expired — drains 1 life (unless shielded)
        if(t.type==="siphon"){
          spawnParticles(t.x,t.y,"#dc2626",20,"spark");
          spawnPopup(t.x,t.y-30,"⚠️ SIPHON! -1 LIFE","#ef4444",18);
          sfx("miss");vibrate([20,10,20,10,30]);
          const hasShS=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
          if(hasShS){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
          else{gs.lives--;gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);lostLife=true;}
          return false;
        }
        // POISON expired — apply poison debuff (next target gives 50% pts)
        if(t.type==="poison"){
          gs._poisonedUntil=Date.now()+4000;
          spawnParticles(t.x,t.y,"#4ade80",14,"dot");
          spawnPopup(t.x,t.y-26,"☣️ POISONED! -50%","#4ade80",16);
          sfx("miss");vibrate([15,8,15]);
          return false;
        }
        // VOLATILE explosion on expiry — costs a life, removes nearby targets
        if(t.type==="volatile"){
          const BLAST_R=90;
          const blasted=targetsRef.current.filter(o=>o!==t&&!o.dying&&o.type==="normal"&&Math.hypot(o.x-t.x,o.y-t.y)<BLAST_R);
          blasted.forEach(o=>{o.dying=performance.now();spawnParticles(o.x,o.y,"#ff4500",6,"spark");});
          spawnParticles(t.x,t.y,"#ff4500",30,"spark");spawnParticles(t.x,t.y,"#ffd700",15,"dot");
          spawnPopup(t.x,t.y-30,"💥 BOOM! -1 LIFE","#ef4444",18);
          sfx("miss");vibrate([30,15,30]);setScreenShake(true);setTimeout(()=>setScreenShake(false),400);
          const hasShieldV=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
          if(!hasShieldV){gs.lives--;gs.streak=0;streakShRef.current=false;setStreakShieldActive(false);}
          else{activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
          return false;
        }
        if(t.type==="normal"&&!t._isShard){gs.sessionStats.missedTargets=(gs.sessionStats.missedTargets||0)+1;gs._luckyTaps=0;}
        const hasShield=activePwrRef.current.some(p=>p.type==="SHIELD"&&p.endsAt>now);
        const shieldWall=activePwrRef.current.find(p=>p.type==="SHIELD_WALL"&&p.endsAt>now);
        if(hasShield){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD");setActivePwrDisp([...activePwrRef.current]);}
        else if(shieldWall){
          shieldWall.hitsLeft=(shieldWall.hitsLeft||1)-1;
          spawnParticles(t.x,t.y,"#a78bfa",8,"spark");
          spawnPopup(t.x,t.y-16,`🏰 WALL: ${shieldWall.hitsLeft} left`,"#a78bfa",12);
          if(shieldWall.hitsLeft<=0){activePwrRef.current=activePwrRef.current.filter(p=>p.type!=="SHIELD_WALL");setActivePwrDisp([...activePwrRef.current]);sfx("shieldBreak");}
          else setActivePwrDisp([...activePwrRef.current]);
        } else if(streakShRef.current){
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
          } else if(activePwrRef.current.some(p=>p.type==="COMBO_FREEZE"&&p.endsAt>now)){
            // COMBO_FREEZE active — protect streak, just flash blue
            spawnParticles(t.x,t.y,"#67e8f9",8,"spark");
            spawnPopup(t.x,t.y-18,"🧊 COMBO SAVED!","#67e8f9",13);
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
      // Bomb danger zone — subtle pulsing red ring around bombs showing tap-exclusion zone
      if(t.type==="bomb"&&!t.dying){
        const bdPulse=0.4+0.4*Math.abs(Math.sin(ts*0.006));
        ctx.save();ctx.globalAlpha=bdPulse*0.18;
        ctx.fillStyle="#ef4444";ctx.shadowColor="#ef4444";ctx.shadowBlur=0;
        ctx.beginPath();ctx.arc(t.x,t.y,t.radius*2.2,0,Math.PI*2);ctx.fill();
        ctx.globalAlpha=bdPulse*0.5;
        ctx.strokeStyle="#ef4444";ctx.lineWidth=1.5;
        ctx.setLineDash([5,4]);
        ctx.beginPath();ctx.arc(t.x,t.y,t.radius*2.2,0,Math.PI*2);ctx.stroke();
        ctx.setLineDash([]);
        ctx.restore();
      }
      // Bounty target indicator — golden crown + pulsing ring above the target
      if(t._isBounty&&!t.dying){
        const bpulse=0.5+0.5*Math.sin(ts*0.009);
        ctx.save();
        ctx.globalAlpha=0.55+bpulse*0.35;
        ctx.strokeStyle="#ffd700";ctx.lineWidth=2.5;ctx.shadowColor="#ffd700";ctx.shadowBlur=12+bpulse*8;
        ctx.setLineDash([5,3]);ctx.lineDashOffset=-ts*0.05;
        ctx.beginPath();ctx.arc(t.x,t.y,t.radius+8,0,Math.PI*2);ctx.stroke();
        ctx.setLineDash([]);ctx.globalAlpha=0.9;
        ctx.font=`${Math.round(t.radius*0.7)}px sans-serif`;
        ctx.textAlign="center";ctx.textBaseline="bottom";ctx.shadowBlur=6;
        ctx.fillText("👑",t.x,t.y-t.radius-2);
        ctx.restore();
      }
      // Edge warning flash overlay
      if(t._edgeWarnAt){
        const edgeFrac=Math.min(1,(now-t._edgeWarnAt)/1500);
        const flashAlpha=0.35+0.45*Math.sin(ts*0.025)*(0.5+edgeFrac*0.5);
        ctx.save();ctx.globalAlpha=flashAlpha;
        ctx.strokeStyle="#ef4444";ctx.lineWidth=3+edgeFrac*3;
        ctx.shadowColor="#ef4444";ctx.shadowBlur=12+edgeFrac*10;
        ctx.beginPath();ctx.arc(t.x,t.y,t.radius+4,0,Math.PI*2);ctx.stroke();
        ctx.restore();
      }
      // Near-expiry warning — target flashes orange when < 20% lifetime remains
      if(t.type==="normal"&&!t.dying&&!t._edgeWarnAt&&t.lifetime>0){
        const lifeLeft=(t.spawnedAt+t.lifetime-now)/t.lifetime;
        if(lifeLeft<0.2&&lifeLeft>0){
          const urgency=1-lifeLeft/0.2;
          const expAlpha=(0.3+0.5*urgency)*Math.abs(Math.sin(ts*0.03*(1+urgency*2)));
          ctx.save();ctx.globalAlpha=expAlpha;
          ctx.strokeStyle=lifeLeft<0.08?"#ef4444":"#f97316";
          ctx.lineWidth=2.5;ctx.shadowColor=lifeLeft<0.08?"#ef4444":"#f97316";ctx.shadowBlur=8+urgency*8;
          ctx.beginPath();ctx.arc(t.x,t.y,t.radius+3,0,Math.PI*2);ctx.stroke();
          ctx.restore();
        }
      }
      drawTarget(ctx,t,ts);return true;
    });

    // World foreground silhouettes + weather + depth vignette (on top of targets)
    drawWorldForeground(ctx,w,h,cfg?cfg.world:0,ts);
    drawWeatherParticles(ctx,w,h,cfg?cfg.world:0,ts);
    drawVignette(ctx,w,h,accentColor);

    if(lostLife){
      if(gs.lives<=0){endLevel(false);return;}
      setDamageFlash(true);setTimeout(()=>setDamageFlash(false),500);
    }

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

    // Lightning Storm — triggered by hitting streak 25+ milestone (max once per level)
    if(!cfg.isBoss&&gs.streak>=25&&!gs._stormTriggered&&!gs._stormEndsAt){
      gs._stormTriggered=true;gs._stormEndsAt=now+4000;
      spawnPopup(cw/2,ch*0.3,"⚡ LIGHTNING STORM!","#fbbf24",22);
      setNotif("⚡ LIGHTNING STORM! All targets get zapped!");
      sfx("chainBonus");vibrate([15,8,15,8,25]);
      // Zap all current normal targets for free
      const eligible=targetsRef.current.filter(t=>!t.dying&&t.type==="normal"&&!t._isShard);
      const combo=Math.min(10,1+Math.floor(gs.streak/5));const feverMult=gs.feverActive?2:1;
      eligible.slice(0,5).forEach((t,i)=>{setTimeout(()=>{
        if(!t.dying){t.dying=performance.now();
          const pts=Math.round(40*combo*feverMult);gs.score+=pts;gs.sessionStats.score=gs.score;
          spawnParticles(t.x,t.y,"#fbbf24",10,"spark");spawnPopup(t.x,t.y-20,`⚡+${pts}`,"#fbbf24",13);
          sfx("comboNote",i+2);
        }
      },i*120);});
    }

    // Target Rush — when score hits 90% of goal, spawn at 1.5× rate for 8s
    if(!cfg.isBoss&&!cfg.isZen&&cfg.scoreGoal&&gs.score>=cfg.scoreGoal*0.9&&!gs._rushStarted){
      gs._rushStarted=true;gs._rushEndsAt=now+8000;
      spawnPopup(cw/2,ch/3,"⚡ RUSH! GET IT!","#f97316",20);sfx("feverStart");vibrate([15,8,15]);
      setRushMode(true);setTimeout(()=>setRushMode(false),8000);
    }
    const isRush=gs._rushEndsAt&&now<gs._rushEndsAt;

    // Spawn — rage boss speeds up spawn
    const rageSpawn=cfg._rageSpawn&&targetsRef.current.some(t=>t.rage);
    spawnTimer.current+=dt;
    const rushSpawnMult=isRush?0.65:1;
    const conductorMult=(gs._conductorEndsAt&&Date.now()<gs._conductorEndsAt)?0.45:1;
    const doubleSpawnMult=gs._doubleSpawnActive?0.5:1;
    if(spawnTimer.current>=(rageSpawn?cfg.spawnInterval*0.5:cfg.spawnInterval*rushSpawnMult*conductorMult*doubleSpawnMult)){spawnTimer.current=0;spawnTarget();}

    // Bounty Target — once per level, designate one normal target as a bounty (3× coins)
    if(!cfg.isBoss&&!cfg.isZen&&!cfg.isGauntlet&&!gs.bountySet){
      gs.bountySet=true;
      // After 4 targets have been tapped, flag the next newly-spawned normal target
      gs._bountyArmed=true;
    }
    if(gs._bountyArmed&&targetsRef.current.length>0){
      const candidate=targetsRef.current.find(t=>t.type==="normal"&&!t._isBounty&&!t.dying&&!t.ghost);
      if(candidate){
        candidate._isBounty=true;
        gs._bountyArmed=false;
      }
    }

    // Wave Surge — every 18-24s, spawn 3-5 targets at once (not in boss/zen/bonus rounds)
    if(!cfg.isBoss&&!cfg.isZen&&!gs.bonusRoundActive&&!cfg.isGauntlet){
      if(!gs.waveAt) gs.waveAt=Date.now()+18000+Math.random()*6000;
      if(Date.now()>=gs.waveAt){
        const waveCount=3+Math.floor(Math.random()*3);
        for(let i=0;i<waveCount;i++) setTimeout(()=>spawnTarget(),i*60);
        spawnPopup(cw/2,ch/3,`🌊 WAVE × ${waveCount}`,"#60a5fa",16);
        sfx("chainBonus");
        gs.waveAt=Date.now()+18000+Math.random()*8000;
      }
    }

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

    // Score milestone popups — HALFWAY / SO CLOSE (shown once per level)
    if(cfg.scoreGoal&&!cfg.isInfinity&&!cfg.isZen){
      const scorePct=gs.score/cfg.scoreGoal;
      if(scorePct>=0.5&&!gs._shownHalfway){
        gs._shownHalfway=true;
        spawnPopup(cw/2,ch*0.42,"🎯 HALFWAY THERE!","#4ade80",18);sfx("tap");
      }
      if(scorePct>=0.9&&!gs._shownClose){
        gs._shownClose=true;
        spawnPopup(cw/2,ch*0.38,"🔥 SO CLOSE! PUSH IT!","#f97316",20);sfx("lucky");vibrate([15,8,15]);
      }
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
      const totalAttempted=(gs.sessionStats.tapsTotal||0)+(gs.sessionStats.missedTargets||0);
      const liveAccuracy=totalAttempted>=5?Math.round((gs.sessionStats.tapsTotal||0)/totalAttempted*100):null;
      // Next-tap score estimate (based on current combo + fever + prestige; uses RARE rarity mult)
      const estCombo=Math.min(10,1+Math.floor(gs.streak/5));
      const estFever=gs.feverActive?2:1;
      const estPrestige=1+(Math.min(5,saveRef.current.prestigeLevel||0)*0.05);
      const estScoreBoost=(gs._scoreBoostTaps||0)>0?5:1;
      const estNextPts=Math.round(2*estCombo*estFever*estPrestige*estScoreBoost); // using rare mult ~2
      setHud({score:gs.score,lives:gs.lives,streak:gs.streak,fever:gs.feverActive,coins:saveRef.current.coins,
        timeLeft:zenTimeLeft,modGoal:cfg?.isZen?null:cfg?.modifier?.desc||null,decayPct,
        boss:bossT?{hp:bossT.hitsLeft,max:bossT.maxHits,phase:bossT.bossPhase||1,rage:!!bossT.rage}:null,
        accuracy:liveAccuracy,nextPts:gs.streak>=5?estNextPts:null});
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

      {/* Stats strip */}
      <div className="flex items-center gap-2 flex-wrap justify-center">
        <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:"#fbbf2415",border:"1px solid #fbbf2430"}}>
          <span>🪙</span><span className="font-bold text-sm" style={{color:"#fbbf24"}}>{sv.coins||0}</span>
        </div>
        {/* 7-day login streak calendar */}
        <div className="flex items-center gap-1 px-2.5 py-1.5 rounded-xl" style={{background:theme.accent+"12",border:`1px solid ${theme.accent}28`}}>
          {Array.from({length:7},(_,i)=>{
            const dayPos=i+1;
            const streak=sv.loginStreak||0;
            const dayInCycle=((streak-1)%7)+1;
            const filled=streak>=7?true:dayPos<=dayInCycle;
            const isToday=dayPos===dayInCycle;
            return(
              <div key={i} style={{
                width:16,height:16,borderRadius:4,
                background:filled?"#fbbf24":"#ffffff12",
                border:isToday?`2px solid ${theme.accent}`:`1px solid ${filled?"#fbbf2444":"#ffffff10"}`,
                display:"flex",alignItems:"center",justifyContent:"center",fontSize:8,
                boxShadow:filled?"0 0 6px #fbbf2455":"none",
              }}>
                {filled?"✓":""}
              </div>
            );
          })}
          <span style={{fontSize:10,color:theme.accent,fontWeight:"bold",marginLeft:3}}>🔥 {sv.loginStreak||1}</span>
        </div>
        {(sv.unlockedAchievements||[]).length>0&&(
          <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl" style={{background:"#ffffff08",border:"1px solid #ffffff15"}}>
            <span className="text-xs opacity-60">🏆 {sv.unlockedAchievements.length}/{ACHIEVEMENTS.length}</span>
          </div>
        )}
        {(sv.prestigeLevel||0)>0&&(()=>{
          const pt=PRESTIGE_TIERS[sv.prestigeLevel];
          return pt?.badge?(
            <div className="flex items-center gap-1 px-3 py-1.5 rounded-xl"
              style={{background:`${pt.color}18`,border:`1px solid ${pt.color}55`}}>
              <span style={{fontSize:13}}>{pt.badge}</span>
              <span className="text-xs font-bold" style={{color:pt.color}}>{pt.title}</span>
            </div>
          ):null;
        })()}
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
      {/* Time Attack Mode — unlocked after level 3 */}
      {(sv.unlockedLevel||1)>=3&&(
        <NeonButton onClick={()=>go("timeattack")}
          className="w-full py-3 text-base font-black"
          style={{background:"linear-gradient(135deg,#ea580c22,#f9731633)",border:"2px solid #f9731666",
            color:"#f97316",boxShadow:"0 0 20px #f9731633",letterSpacing:"0.06em"}}>
          ⚡ TIME ATTACK {sv.taBest>0?`• Best: ${sv.taBest.toLocaleString()}`:""}
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
        {/* 10D — Bonus spin for login streak >= 7 */}
        {(sv.loginStreak||0)>=7&&(()=>{
          const bonusSpinKey=`bonusSpin_${getTodayKey()}`;
          const alreadyBonused=sv[bonusSpinKey];
          return!alreadyBonused?(
            <div className="w-full rounded-2xl p-4 text-center" style={{background:"#ffd70015",border:"2px solid #ffd70066",boxShadow:"0 0 24px #ffd70033"}}>
              <div className="font-black text-sm mb-1" style={{color:"#ffd700",letterSpacing:"0.06em"}}>🔥 7-DAY STREAK BONUS!</div>
              <div className="text-xs opacity-60 mb-3" style={{color:"#fbbf24"}}>You get an extra bonus spin today!</div>
              <NeonButton onClick={()=>{
                if(spinState==="spinning")return;
                const sv2=saveRef.current;
                sv2[bonusSpinKey]=true;
                // Bonus spin always gives double rewards
                const prizeIdx=Math.floor(Math.random()*SPIN_PRIZES.length);
                const prize=SPIN_PRIZES[prizeIdx];
                if(prize.type==="coins"){const b=prize.value*2;sv2.coins=(sv2.coins||0)+b;sv2.totalCoins=(sv2.totalCoins||0)+b;}
                else if(prize.type==="xp"){sv2.xp=(sv2.xp||0)+prize.value*2;}
                flushSave();
                sfx("jackpot");vibrate([30,15,30,15,60]);
                setNotif(`🎁 BONUS SPIN: ${prize.emoji} ${prize.label} ×2! 🔥`);
                setTimeout(()=>setNotif(null),3000);
              }} style={{background:"linear-gradient(135deg,#b45309,#fbbf24)",boxShadow:"0 0 20px #ffd70066",letterSpacing:"0.05em"}}>
                🎡 CLAIM BONUS SPIN
              </NeonButton>
            </div>
          ):null;
        })()}
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
            <div className="flex items-center gap-2">
              {/* Difficulty rating D1-D5 */}
              {(()=>{
                const diff=Math.min(5,Math.ceil((cfg.id||1)/20));
                const diffColors=["","#4ade80","#fbbf24","#f97316","#ef4444","#a855f7"];
                const diffLabels=["","Easy","Medium","Hard","Expert","Legendary"];
                return(
                  <span className="text-xs font-black px-1.5 py-0.5 rounded"
                    style={{background:diffColors[diff]+"22",color:diffColors[diff],border:`1px solid ${diffColors[diff]}55`}}>
                    D{diff} {diffLabels[diff]}
                  </span>
                );
              })()}
              <div className="flex gap-0.5">{[1,2,3].map(s=><span key={s} style={{fontSize:12,opacity:(sv.levelStars[cfg.id]||0)>=s?1:0.2,color:"#fbbf24"}}>★</span>)}</div>
            </div>
          </div>
          <div className="flex gap-4 text-xs opacity-60" style={{color:cfg.worldColor}}>
            <span>❤️ {cfg.lives} lives</span>
            {cfg.modifier&&<span className="font-bold" style={{color:"#fbbf24"}}>⚡ {cfg.modifier.desc}</span>}
          </div>
        </div>
        {/* Target type preview — show which special targets may appear in this level */}
        {(()=>{
          const id=cfg.id||1;
          const previews=[];
          if(id>=1) previews.push({icon:"🟣",label:"Normal",desc:"Standard tap target"});
          if(id>=1) previews.push({icon:"💣",label:"Bomb",desc:"DON'T tap! Costs a life"});
          if(id>=3) previews.push({icon:"⚡",label:"Power-up",desc:"Special abilities"});
          if(id>=5) previews.push({icon:"🫧",label:"Bubble",desc:"Easy pop, wide zone"});
          if(id>=5) previews.push({icon:"❓",label:"Mystery",desc:"Spin for surprise!"});
          if(id>=8) previews.push({icon:"🪙",label:"Chest",desc:"Drops 3-5 coins"});
          if(id>=10) previews.push({icon:"🔮",label:"Treasure",desc:"Jackpot score bonus"});
          if(id>=12) previews.push({icon:"🎭",label:"Mimic",desc:"Copies last rarity"});
          if(id>=14) previews.push({icon:"🧲",label:"Magnet",desc:"Pulls nearby targets"});
          if(id>=16) previews.push({icon:"🌀",label:"Anchor",desc:"Freezes all movers"});
          if(id>=18) previews.push({icon:"💚",label:"Healer",desc:"Restore 1 life"});
          if(id>=16) previews.push({icon:"⚡",label:"Bouncy",desc:"Fast! Bounces around"});
          if(id>=20) previews.push({icon:"👻",label:"Phantom",desc:"Ultra-short 1.1s life"});
          if(id>=22) previews.push({icon:"✦",label:"Twin",desc:"Tap one, score two!"});
          if(id>=24) previews.push({icon:"❄️",label:"Frozen",desc:"Tiny hitbox, 3× pts"});
          if(id>=24) previews.push({icon:"🌀",label:"Tornado",desc:"Scatters all targets"});
          if(id>=25) previews.push({icon:"💥",label:"Volatile",desc:"Defuse it before boom!"});
          if(id>=28) previews.push({icon:"🟣",label:"Shielded",desc:"Needs 2 taps"});
          if(id>=30) previews.push({icon:"🌈",label:"Rainbow",desc:"Cycling rarity tiers"});
          if(id>=35) previews.push({icon:"🥷",label:"Ninja",desc:"Invisible mostly!"});
          if(id>=40) previews.push({icon:"💥",label:"Splitter",desc:"Splits into 3!"});
          if(id>=10) previews.push({icon:"🍀",label:"Clover",desc:"Random ×1-10 multiplier!"});
          if(id>=12) previews.push({icon:"🎯",label:"Ricochet",desc:"Kills 2 nearby targets!"});
          if(id>=15) previews.push({icon:"⚡",label:"Voltage",desc:"Chain zaps 3 targets!"});
          if(id>=15) previews.push({icon:"💥",label:"Particle Bomb",desc:"Explodes into sparks!"});
          if(id>=20) previews.push({icon:"🌀",label:"Portal",desc:"Teleports all targets!"});
          if(id>=28) previews.push({icon:"🌌",label:"Aurora",desc:"Rhythm tap multiplier"});
          if(id>=35) previews.push({icon:"🌀",label:"Void",desc:"Absorbs nearby targets"});
          if(cfg.isBoss) previews.push({icon:WORLDS[cfg.world-1].emoji,label:"BOSS",desc:"Multi-hit epic fight!"});
          const show=previews.slice(-8); // Show last 8 relevant types for this level
          return(
            <div className="rounded-2xl px-4 py-3" style={{background:`${cfg.worldColor}08`,border:`1px solid ${cfg.worldColor}22`}}>
              <div className="text-xs font-bold opacity-40 mb-2 uppercase tracking-widest" style={{color:cfg.worldColor}}>🎯 Targets in this level</div>
              <div className="flex flex-wrap gap-1.5">
                {show.map((t,i)=>(
                  <div key={i} className="flex items-center gap-1 px-2 py-1 rounded-lg"
                    style={{background:`${cfg.worldColor}12`,border:`1px solid ${cfg.worldColor}25`}}>
                    <span style={{fontSize:12}}>{t.icon}</span>
                    <span className="text-xs font-bold" style={{color:cfg.worldColor,opacity:0.8}}>{t.label}</span>
                  </div>
                ))}
              </div>
            </div>
          );
        })()}

        {/* Boss incoming warning — level X9 means next level is a boss */}
        {cfg.id%10===9&&!cfg.isBoss&&(
          <div className="rounded-2xl px-4 py-3 flex items-center gap-3"
            style={{background:"#ff000012",border:"1px solid #ff000044",
              animation:"heartbeat 1.2s ease-in-out infinite"}}>
            <span style={{fontSize:24}}>⚠️</span>
            <div>
              <div className="font-black text-sm" style={{color:"#ff6b35"}}>BOSS INCOMING!</div>
              <div className="text-xs opacity-70" style={{color:"#ff9f80"}}>
                Level {cfg.id+1} features a powerful boss. Consider buying a Shield or Extra Life!
              </div>
            </div>
          </div>
        )}
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
      <div className="absolute inset-0" onTouchStart={handleTap} onClick={handleTap}
        onTouchMove={e=>{const r=e.currentTarget.getBoundingClientRect();const t=e.touches[0];if(t)tapTrailRef.current.push({x:t.clientX-r.left,y:t.clientY-r.top,ts:performance.now()});}}
        onMouseMove={e=>{const r=e.currentTarget.getBoundingClientRect();tapTrailRef.current.push({x:e.clientX-r.left,y:e.clientY-r.top,ts:performance.now()});}}
        style={{touchAction:"none",zIndex:10}}>
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
          <div className="flex-1 flex flex-col items-center justify-center py-2 px-1" style={{position:"relative"}}>
            {cfg&&!cfg.isInfinity&&!cfg.isZen&&(()=>{
              const pct=Math.min(1,hud.score/cfg.scoreGoal);
              const r=29,s=3,cx=31,cy=31;
              const circ=2*Math.PI*r;
              const dash=pct*circ;
              const clr=pct>=0.85?"#f97316":pct>=0.6?"#fbbf24":"#4ade80";
              return(
                <svg width={62} height={62} style={{position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",pointerEvents:"none",overflow:"visible",zIndex:0}}>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke="#ffffff08" strokeWidth={s}/>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke={clr} strokeWidth={s}
                    strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
                    transform={`rotate(-90 ${cx} ${cy})`}
                    style={{transition:"stroke-dasharray 0.35s ease-out",filter:`drop-shadow(0 0 4px ${clr})`}}/>
                </svg>
              );
            })()}
            {cfg?.isZen&&hud.timeLeft!=null&&(()=>{
              const totalSec=Math.ceil((cfg.zenDuration||90000)/1000);
              const pct=hud.timeLeft/totalSec;
              const r=29,s=3.5,cx=31,cy=31;
              const circ=2*Math.PI*r;
              const dash=pct*circ;
              const clr=pct<0.2?"#ef4444":pct<0.45?"#f97316":pct<0.7?"#fbbf24":"#34d399";
              return(
                <svg width={62} height={62} style={{position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",pointerEvents:"none",overflow:"visible",zIndex:0}}>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke="#ffffff06" strokeWidth={s}/>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke={clr} strokeWidth={s}
                    strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
                    transform={`rotate(-90 ${cx} ${cy})`}
                    style={{transition:"stroke-dasharray 0.9s linear",filter:`drop-shadow(0 0 5px ${clr})`,
                      animation:pct<0.2?"heartbeat 0.7s ease-in-out infinite":"none"}}/>
                </svg>
              );
            })()}
            <div className="text-xs opacity-35 tracking-widest uppercase" style={{color:wc,position:"relative",zIndex:1}}>
              {cfg?.isZen?"TIME":"Score"}
            </div>
            <div className="text-xl font-black tabular-nums" style={{color:wc,position:"relative",zIndex:1}}>{hud.score.toLocaleString()}</div>
            {cfg?.isZen&&hud.timeLeft!=null
              ?<div className="text-xs font-bold tabular-nums" style={{color:hud.timeLeft<=15?"#ef4444":hud.timeLeft<=30?"#f97316":"#34d399",position:"relative",zIndex:1,textShadow:hud.timeLeft<=15?"0 0 8px #ef4444":"none"}}>
                  {hud.timeLeft}s ☯
                </div>
              :<>{cfg&&!cfg.isZen&&<div className="text-xs opacity-40 tabular-nums" style={{color:wc,position:"relative",zIndex:1}}>/{cfg.scoreGoal.toLocaleString()}</div>}</>
            }
          </div>
          <div className="flex flex-col items-center justify-center px-2 py-1.5 gap-1">
            <div className="flex gap-0.5">{Array.from({length:MAX_LIVES},(_,i)=><span key={i} style={{fontSize:13,opacity:i<hud.lives?1:0.18}}>{i<hud.lives?"❤️":"🖤"}</span>)}</div>
            {cfg&&<div className="text-xs font-bold px-1.5 py-0.5 rounded-full" style={{background:wc+"22",color:wc}}>{WORLDS[cfg.world-1].emoji} L{cfg.id}</div>}
            {/* Mascot HUD chip — tiny */}
            <span style={{fontSize:16,lineHeight:1}}>{currentMascot.e[mascotMood]||currentMascot.e.idle}</span>
          </div>
          <div className="flex-1 flex flex-col items-center justify-center py-2 px-1" style={{position:"relative"}}>
            {hud.streak>0&&(()=>{
              const dp=Math.max(0,hud.decayPct??1);
              const r=29,s=3,cx=31,cy=31;
              const circ=2*Math.PI*r;
              const dash=dp*circ;
              const clr=streakDecaying?"#ef4444":streakColor();
              return(
                <svg width={62} height={62} style={{position:"absolute",top:"50%",left:"50%",transform:"translate(-50%,-50%)",pointerEvents:"none",overflow:"visible",zIndex:0}}>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke="#ffffff06" strokeWidth={s}/>
                  <circle cx={cx} cy={cy} r={r} fill="none" stroke={clr} strokeWidth={s}
                    strokeDasharray={`${dash} ${circ}`} strokeLinecap="round"
                    transform={`rotate(-90 ${cx} ${cy})`}
                    style={{transition:"stroke-dasharray 0.12s linear",filter:`drop-shadow(0 0 4px ${clr})`}}/>
                </svg>
              );
            })()}
            <div className="text-xs opacity-35 tracking-widest uppercase" style={{color:wc,position:"relative",zIndex:1}}>Streak</div>
            <div className="text-xl font-black tabular-nums"
              style={{
                color:streakDecaying&&hud.streak>0?"#ef4444":streakColor(),
                textShadow:hud.streak>=5?`0 0 14px ${streakDecaying?"#ef4444":streakColor()}`:"none",
                animation:streakDecaying&&hud.streak>0?"heartbeat 0.6s ease-in-out infinite":"none",
                position:"relative",zIndex:1,
              }}>
              {hud.streak}×{streakDecaying&&hud.streak>0?"⚠️":""}
            </div>
            {hud.streak>=5&&<div style={{fontSize:9,fontWeight:"black",color:streakColor(),opacity:0.8,letterSpacing:"0.04em",position:"relative",zIndex:1}}>
              ×{Math.min(10,1+Math.floor(hud.streak/5))} MULT
            </div>}
            {hud.nextPts!=null&&hud.streak>=5&&<div style={{fontSize:7,color:"#fbbf24",opacity:0.65,letterSpacing:"0.02em",position:"relative",zIndex:1}}>
              ~{hud.nextPts}pts
            </div>}
            {hud.accuracy!=null&&hud.streak===0&&<div style={{fontSize:8,color:hud.accuracy>=95?"#4ade80":hud.accuracy>=80?"#fbbf24":"#f87171",opacity:0.75,letterSpacing:"0.03em",position:"relative",zIndex:1}}>
              {hud.accuracy}% ACC
            </div>}
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
        {/* Mission mini-tracker — compact 3-dot indicator showing daily quest progress */}
        {!hud.boss&&!sv.missionCompleted&&(()=>{
          const missions=getDailyMissions();
          const prog=sv.missionProgress||{};
          const dots=missions.map(m=>({done:(prog[m.id]||0)>=m.goal,pct:Math.min(1,(prog[m.id]||0)/m.goal)}));
          const anyProgress=dots.some(d=>d.pct>0);
          if(!anyProgress)return null;
          return(
            <div className="absolute z-20 pointer-events-none flex items-center gap-1"
              style={{top:76,left:"50%",transform:"translateX(-50%)",background:"rgba(0,0,0,0.5)",
                borderRadius:12,padding:"3px 8px",border:"1px solid #ffffff10"}}>
              {dots.map((d,i)=>(
                <div key={i} style={{width:22,height:4,borderRadius:2,background:"#ffffff18",overflow:"hidden"}}>
                  <div style={{width:`${d.pct*100}%`,height:"100%",borderRadius:2,
                    background:d.done?"#34d399":"#fbbf24",boxShadow:d.done?"0 0 4px #34d399":"none",
                    transition:"width 0.3s ease"}}/>
                </div>
              ))}
              <span style={{fontSize:8,color:"#fbbf24",fontWeight:"bold"}}>{dots.filter(d=>d.done).length}/3</span>
            </div>
          );
        })()}
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
        {/* Boss Speech Bubble — shows during phase transitions */}
        {bossTaunt&&hud.boss&&(
          <div className="absolute left-0 right-0 flex justify-center z-30 pointer-events-none" style={{top:130}}>
            <div className="relative px-4 py-2 rounded-2xl max-w-xs text-center"
              style={{
                background:bossTaunt.phase===3?"#ff000022":bossTaunt.phase===2?"#fbbf2418":"#2a2a3a",
                border:`1px solid ${bossTaunt.phase===3?"#ff0000":bossTaunt.phase===2?"#fbbf24":"#666666"}88`,
                color:bossTaunt.phase===3?"#ff4444":bossTaunt.phase===2?"#fbbf24":"#aaaaaa",
                fontSize:13,fontWeight:"bold",
                animation:"speechBubble 0.3s cubic-bezier(0.34,1.5,0.64,1) both",
                boxShadow:`0 0 20px ${bossTaunt.phase===3?"#ff000066":bossTaunt.phase===2?"#fbbf2444":"#44444444"}`,
              }}>
              {bossTaunt.phase==="dying"?"💀":bossTaunt.phase===3?"😡":"😤"} "{bossTaunt.text}"
              {/* Speech bubble tail */}
              <div style={{position:"absolute",top:-7,left:"50%",transform:"translateX(-50%)",
                width:0,height:0,
                borderLeft:"8px solid transparent",borderRight:"8px solid transparent",
                borderBottom:`8px solid ${bossTaunt.phase===3?"#ff000044":bossTaunt.phase===2?"#fbbf2430":"#44444444"}`}}/>
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
        {/* Stacked multiplier banner — show when DOUBLE + MULTIPLIER both active */}
        {(()=>{
          const hasDouble=activePwrDisp.some(p=>p.type==="DOUBLE"&&p.endsAt>Date.now());
          const hasMultiplier=activePwrDisp.some(p=>p.type==="MULTIPLIER"&&p.endsAt>Date.now());
          const hasFever=hud.fever;
          const totalMult=(hasDouble?2:1)*(hasMultiplier?3:1)*(hasFever?2:1);
          if(totalMult<=1)return null;
          return(
            <div className="absolute z-30 pointer-events-none" style={{top:72,left:"50%",transform:"translateX(-50%)",
              background:"linear-gradient(90deg,#f43f5e,#f97316)",borderRadius:20,padding:"2px 10px",
              fontSize:11,fontWeight:"black",color:"#fff",letterSpacing:"0.08em",
              boxShadow:"0 0 16px #f43f5e66",animation:"heartbeat 0.8s ease-in-out infinite",whiteSpace:"nowrap"}}>
              ×{totalMult} SUPER MULT!
            </div>
          );
        })()}
        {/* Power-ups */}
        {/* 9D — Power-up queue visual with time bars */}
        {activePwrDisp.length>0&&(
          <div className="absolute left-0 right-0 flex justify-center gap-1.5 z-20" style={{top:hud.boss?148:hud.modGoal?108:76}}>
            {activePwrDisp.map(p=>{
              const secsLeft=Math.max(0,Math.ceil((p.endsAt-Date.now())/1000));
              const totalSecs=p.type==="SHIELD"?25:p.type==="SLOW"?8:p.type==="DOUBLE"?10:p.type==="FREEZE"?4:p.type==="MULTIPLIER"?8:p.type==="COMBO_FREEZE"?10:p.type==="TIME_WARP"?6:12;
              const pct=Math.min(100,Math.round(secsLeft/totalSecs*100));
              const isExpiring=secsLeft<=2&&secsLeft>0;
              const colors={SHIELD:"#fbbf24",SLOW:"#60a5fa",DOUBLE:"#f97316",FREEZE:"#06b6d4",LIFE:"#4ade80",LUCKY:"#ffd700",MIRROR:"#c084fc",MULTIPLIER:"#f43f5e",COMBO_FREEZE:"#67e8f9",GRAVITY:"#a78bfa",TIME_WARP:"#818cf8",SCORE_BOOST:"#f43f5e",LIFE_SURGE:"#4ade80",MAGNET_FIELD:"#ec4899",OVERCLOCK:"#fbbf24",SHIELD_WALL:"#a78bfa"};
              const icons={SHIELD:"🛡",SLOW:"🐢",DOUBLE:"×2",FREEZE:"❄️",LIFE:"❤️",LUCKY:"⭐",MIRROR:"🪞",MULTIPLIER:"×3",COMBO_FREEZE:"🧊",GRAVITY:"🌐",TIME_WARP:"⏱️",SCORE_BOOST:"×5",LIFE_SURGE:"💚",MAGNET_FIELD:"🧲",OVERCLOCK:"⚡",SHIELD_WALL:"🏰"};
              const c=colors[p.type]||"#60a5fa";
              return(
                <div key={p.type} className="flex flex-col items-center gap-0.5"
                  style={{background:"#0a0a1acc",borderRadius:8,padding:"3px 6px",border:`1px solid ${c}${isExpiring?"cc":"44"}`,minWidth:36,
                    animation:isExpiring?"heartbeat 0.4s ease-in-out infinite":"none",
                    boxShadow:isExpiring?`0 0 8px ${c}88`:"none"}}>
                  <div className="text-xs font-black" style={{color:c,fontSize:11}}>{icons[p.type]||"⚡"}</div>
                  <div className="text-xs font-bold tabular-nums" style={{color:isExpiring?"#ef4444":c,fontSize:9,lineHeight:1,fontWeight:isExpiring?"black":"bold"}}>{secsLeft}s</div>
                  <div style={{width:28,height:3,background:"#ffffff15",borderRadius:2,overflow:"hidden"}}>
                    <div style={{width:`${pct}%`,height:"100%",background:isExpiring?"#ef4444":c,borderRadius:2,
                      boxShadow:`0 0 4px ${isExpiring?"#ef4444":c}`,transition:"width 0.5s linear"}}/>
                  </div>
                </div>
              );
            })}
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
        {rushMode&&!feverBorder&&<div className="absolute inset-0 pointer-events-none z-10" style={{border:"3px solid #f97316",boxShadow:"inset 0 0 40px #f9731633,0 0 40px #f9731633",animation:"feverPulse 0.45s ease-in-out infinite alternate"}}/>}
        {rushMode&&<div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:luckyMode||newRecord?184:feverBorder?166:140}}>
          <span className="font-black text-sm px-3 py-1 rounded-full" style={{color:"#f97316",textShadow:"0 0 16px #f97316",background:"#f9731620",border:"1px solid #f9731666",animation:"heartbeat 0.55s ease-in-out infinite"}}>⚡ RUSH MODE!</span>
        </div>}
        {goldRushMode&&<div className="absolute inset-0 pointer-events-none z-10" style={{border:"3px solid #ffd700",boxShadow:"inset 0 0 50px #ffd70028,0 0 50px #ffd70028",animation:"feverPulse 0.5s ease-in-out infinite alternate"}}/>}
        {goldRushMode&&<div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:feverBorder?178:rushMode?158:140}}>
          <span className="font-black text-sm px-3 py-1 rounded-full" style={{color:"#ffd700",textShadow:"0 0 18px #ffd700",background:"#ffd70018",border:"1px solid #ffd70066",animation:"heartbeat 0.6s ease-in-out infinite"}}>🥇 GOLD RUSH! 3× COINS!</span>
        </div>}
        {/* Score Boost — rose border + tap counter */}
        {(gsRef.current?._scoreBoostTaps||0)>0&&(
          <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-29" style={{top:feverBorder?200:goldRushMode?178:158}}>
            <span className="font-black text-xs px-3 py-1 rounded-full" style={{color:"#f43f5e",textShadow:"0 0 12px #f43f5e",background:"#f43f5e18",border:"1px solid #f43f5e66",letterSpacing:"0.06em",animation:"heartbeat 0.5s ease-in-out infinite"}}>
              ×5 SCORE BOOST — {gsRef.current._scoreBoostTaps} tap{gsRef.current._scoreBoostTaps!==1?"s":""} left!
            </span>
          </div>
        )}
        {/* Lightning Storm visual — yellow border flash */}
        {gsRef.current?._stormEndsAt&&Date.now()<gsRef.current._stormEndsAt&&(
          <div className="absolute inset-0 pointer-events-none z-10" style={{
            border:"3px solid #fbbf24",
            boxShadow:"inset 0 0 60px #fbbf2428,0 0 60px #fbbf2428",
            animation:"feverPulse 0.25s ease-in-out infinite alternate"}}/>
        )}
        {/* Time Warp — deep purple slowdown border + banner */}
        {activePwrDisp.some(p=>p.type==="TIME_WARP"&&p.endsAt>Date.now())&&(
          <>
            <div className="absolute inset-0 pointer-events-none z-10" style={{
              border:"3px solid #818cf8",
              boxShadow:"inset 0 0 60px #818cf822,0 0 60px #818cf822",
              animation:"feverPulse 1.2s ease-in-out infinite alternate"}}/>
            <div className="absolute left-0 right-0 flex justify-center pointer-events-none z-29" style={{top:feverBorder?200:goldRushMode?178:158}}>
              <span className="font-black text-xs px-3 py-1 rounded-full" style={{color:"#818cf8",textShadow:"0 0 12px #818cf8",background:"#818cf818",border:"1px solid #818cf866",letterSpacing:"0.06em"}}>⏱️ TIME WARP ACTIVE</span>
            </div>
          </>
        )}
        {feverBorder&&<div className="absolute inset-0 pointer-events-none z-10" style={{border:"4px solid #fbbf24",boxShadow:"inset 0 0 60px #fbbf2445,0 0 60px #fbbf2445",animation:"feverPulse 0.6s ease-in-out infinite alternate"}}/>}
        {feverBorder&&<div className="absolute left-0 right-0 flex justify-center pointer-events-none z-30" style={{top:luckyMode||newRecord?184:140}}>
          <span className="font-black text-base px-4 py-1 rounded-full" style={{color:"#fbbf24",textShadow:"0 0 20px #fbbf24",background:"#fbbf2420",animation:"feverPulse 0.5s infinite alternate"}}>✨ MAGIC MODE!</span>
        </div>}
        {damageFlash&&<div className="absolute inset-0 pointer-events-none z-10" style={{background:"#ef444428",boxShadow:"inset 0 0 80px #ef444466",animation:"epicFlash 0.5s ease-out forwards"}}/>}
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
        {/* Bounty Board — wanted rarity chip */}
        {bountyData&&!hud.fever&&(()=>{
          const secsLeft=Math.max(0,Math.round((bountyData.expiresAt-Date.now())/1000));
          const urgent=secsLeft<=8;
          return(
            <div className="absolute pointer-events-none z-20" style={{top:88,left:"50%",transform:"translateX(-50%)"}}>
              <div style={{
                display:"flex",alignItems:"center",gap:5,
                background:"#0a0a1aee",border:`1.5px solid ${bountyData.color}`,
                borderRadius:16,padding:"3px 10px",
                boxShadow:`0 0 10px ${bountyData.color}44`,
                animation:urgent?"heartbeat 0.5s ease-in-out infinite":"none"
              }}>
                <span style={{fontSize:11}}>🎯</span>
                <span style={{fontSize:9,color:bountyData.color,fontWeight:"bold",letterSpacing:"0.06em"}}>WANTED: {bountyData.icon} {bountyData.rarity}</span>
                <span style={{fontSize:9,color:urgent?"#ef4444":"#6b7280",fontWeight:"bold"}}>×{bountyData.mult} {secsLeft}s</span>
              </div>
            </div>
          );
        })()}
        {/* Combo milestone progress bar — shows distance to next milestone */}
        {hud.streak>0&&(()=>{
          const COMBO_MILESTONES=[5,10,20,25,30,35,50];
          const streak=hud.streak;
          const nextMs=COMBO_MILESTONES.find(m=>m>streak)||55;
          const prevMs=COMBO_MILESTONES.filter(m=>m<=streak).pop()||0;
          const pct=Math.min(100,((streak-prevMs)/(nextMs-prevMs))*100);
          const comboColor=streak>=35?"#a855f7":streak>=20?"#ef4444":streak>=10?"#f97316":streak>=5?"#fbbf24":"#34d399";
          return(
            <div className="absolute left-4 right-4 pointer-events-none z-20" style={{bottom:6}}>
              <div style={{display:"flex",alignItems:"center",gap:4,marginBottom:1}}>
                <span style={{fontSize:7,color:comboColor,opacity:0.7,letterSpacing:"0.05em"}}>{streak}×</span>
                <div style={{flex:1,height:2.5,background:"#ffffff10",borderRadius:2,overflow:"hidden"}}>
                  <div style={{width:`${pct}%`,height:"100%",background:comboColor,borderRadius:2,
                    boxShadow:`0 0 5px ${comboColor}`,transition:"width 0.15s ease-out"}}/>
                </div>
                <span style={{fontSize:7,color:comboColor,opacity:0.5}}>→{nextMs}×</span>
              </div>
            </div>
          );
        })()}
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
          {/* 9B — Happiness bar */}
          {(()=>{
            const happy=mascotHappyRef.current||0;
            const maxHappy=75;
            const pct=Math.min(100,Math.round((happy%75)/75*100));
            const milestone=happy<25?"😐":happy<50?"😊":happy<75?"😄":"🌟";
            return(
              <div style={{width:50}}>
                <div style={{width:"100%",height:3,background:"#ffffff15",borderRadius:2,overflow:"hidden"}}>
                  <div style={{width:`${pct}%`,height:"100%",background:currentMascot.color,borderRadius:2,
                    boxShadow:`0 0 3px ${currentMascot.color}`,transition:"width 0.3s"}}/>
                </div>
                <div style={{textAlign:"center",fontSize:7,color:currentMascot.color,opacity:0.6,marginTop:1}}>{milestone} {happy}</div>
              </div>
            );
          })()}
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
        {/* Last-life danger border — persistent red pulse when 1 life remaining */}
        {hud.lives===1&&!cfg?.isZen&&(
          <div className="absolute inset-0 pointer-events-none z-5" style={{
            border:"3px solid #ef4444",
            boxShadow:"inset 0 0 50px #ef444428,0 0 30px #ef444422",
            animation:"heartbeat 0.7s ease-in-out infinite"}}/>
        )}
        {hud.lives===1&&!cfg?.isZen&&(
          <div className="absolute left-0 right-0 top-16 flex justify-center pointer-events-none z-25">
            <span style={{fontSize:9,fontWeight:"black",color:"#ef4444",letterSpacing:"0.15em",
              textShadow:"0 0 8px #ef4444",animation:"heartbeat 0.7s ease-in-out infinite"}}>⚠️ LAST LIFE</span>
          </div>
        )}
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
            {/* Falling coin rain during bonus round */}
            <div className="absolute inset-0 pointer-events-none z-7 overflow-hidden">
              {[...Array(14)].map((_,i)=>(
                <div key={i} style={{
                  position:"absolute",top:-20,
                  left:`${(i*7+3)%100}%`,
                  fontSize:12+Math.floor(i%3)*4,
                  animation:`coinFall ${1.8+i*0.22}s ${i*0.18}s linear infinite`,
                  opacity:0.75,pointerEvents:"none"}}>
                  🪙
                </div>
              ))}
            </div>
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
          <div className="absolute inset-0 flex flex-col items-center justify-center z-50 pointer-events-none" style={{background:"rgba(0,0,0,0.55)"}}>
            <div className="font-black text-9xl" key={countdownVal}
              style={{color:countdownVal==="GO!"?"#34d399":wc,textShadow:`0 0 70px ${countdownVal==="GO!"?"#34d399":wc}`,animation:"countAnim 0.5s ease-out"}}>
              {countdownVal}
            </div>
            {countdownVal!=="GO!"&&(()=>{
              const tips=["Tap targets before they vanish! ⚡","🛡 Shielded targets need 2 taps!","Build streaks for fever mode! 🔥","🧲 Magnet targets pull others!","Rare targets = more points! ✨","Perfect timing = Perfect tap bonus! 🎯"];
              const tip=tips[Math.floor((Date.now()/1000)%tips.length)];
              return <div style={{fontSize:12,color:"#ffffff66",marginTop:16,textAlign:"center",maxWidth:220,padding:"0 20px"}}>{currentMascot.e.idle} {tip}</div>;
            })()}
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
    const{score,stars,newStars,xpEarned,coinsEarned,levelId,isLast,sessionStats,isPerfectRun}=levelCompleteData;
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
          {isPerfectRun&&<div className="text-center text-xs font-black mt-1" style={{color:"#4ade80",textShadow:"0 0 12px #4ade80",animation:"floatGlow 1s ease-in-out infinite",letterSpacing:"0.06em"}}>🎯 PERFECT RUN! 3× COIN BONUS!</div>}
          {/* Letter grade rank */}
          {(()=>{
            const ratio=score/(cfg.scoreGoal||1);
            const rank=ratio>=3.5?"S+":ratio>=2.8?"S":ratio>=2?"A+":ratio>=1.5?"A":ratio>=1.2?"B+":ratio>=1?"B":"C";
            const rColors={"S+":"#ffd700","S":"#ffd700","A+":"#f97316","A":"#f97316","B+":"#60a5fa","B":"#60a5fa","C":"#94a3b8"};
            const rColor=rColors[rank]||"#94a3b8";
            return(
              <div className="absolute top-3 right-3 flex flex-col items-center">
                <div style={{fontSize:28,fontWeight:"black",color:rColor,
                  textShadow:`0 0 16px ${rColor}`,lineHeight:1,
                  animation:rank.startsWith("S")?"legendaryRainbow 1.5s linear infinite":"none"}}>
                  {rank}
                </div>
                <div style={{fontSize:8,color:rColor,opacity:0.7,letterSpacing:"0.05em"}}>RANK</div>
              </div>
            );
          })()}
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

        {/* 11C — Animated coins earned overlay */}
        {coinsEarned>0&&(
          <div className="w-full rounded-2xl px-4 py-3 flex items-center justify-between gap-3"
            style={{background:"#ffd70014",border:"1px solid #ffd70044",backdropFilter:"blur(8px)"}}>
            <div className="flex items-center gap-2">
              <span style={{fontSize:22,animation:"coinFall 0.6s ease-out both,floatGlow 1.2s ease-in-out 0.6s infinite"}}>🪙</span>
              <div>
                <div className="text-xs opacity-55 font-bold tracking-widest uppercase" style={{color:"#ffd700"}}>Coins Earned</div>
                <div className="text-2xl font-black tabular-nums" style={{color:"#ffd700",
                  textShadow:"0 0 16px #ffd700",animation:"scorePulse 0.5s cubic-bezier(0.34,1.5,0.64,1) both"}}>
                  +{coinsEarned}
                </div>
              </div>
            </div>
            <div className="flex flex-col items-end gap-1">
              <div className="text-xs opacity-40" style={{color:"#ffd700"}}>Balance</div>
              <div className="text-sm font-black" style={{color:"#ffd700"}}>🪙 {(sv.coins||0).toLocaleString()}</div>
            </div>
          </div>
        )}

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
        <div className="w-full rounded-3xl p-4 relative" style={{
          background:`linear-gradient(160deg,${cfg.worldColor}14 0%,rgba(0,0,0,0.4) 100%)`,
          border:`1px solid ${cfg.worldColor}44`,backdropFilter:"blur(10px)"}}>
          {/* Letter grade on game over */}
          {(()=>{
            const grade=pct>=90?"A":pct>=70?"B":pct>=50?"C":"D";
            const gc=pct>=90?"#fbbf24":pct>=70?"#60a5fa":pct>=50?"#94a3b8":"#ef4444";
            return <div style={{position:"absolute",top:8,right:10,fontSize:24,fontWeight:"black",color:gc,textShadow:`0 0 12px ${gc}`}}>{grade}</div>;
          })()}
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
    gameplay:    ["first_tap","combo_10","boss_1","fever_1","perfect_5","combo_15","chain_4","mimic_hit","shielded_hit","speed_demon","phantom_catch","volatile_defuse","frozen_catch","bouncy_catch","ninja_catch","loot_chest","tornado_catch","bubble_pop","bomb_defuse","echo_tap","echo_bonus","crystal_shatter","crystal_chain","rage_tap","rage_max","divider_tap","chain_lightning_hit","gold_rush","first_tap_fever","bounty_hit","vanishing_tap","vanishing_blind","tap_frenzy","homing_tap","homing_center","gemstone_tap","morph_tap","morph_legendary","time_warp_use","conductor_tap","siphon_tap","glitch_tap","glitch_perfect","prism_tap","comet_tap","comet_early","mirrorball_tap","nexus_tap","phoenix_tap","phoenix_risen","icecomet_tap","voltage_tap","void_tap","void_master","clover_tap","clover_jackpot","ricochet_tap","ricochet_double","aurora_tap","aurora_perfect","fury_mode","score_10k","portal_tap","portal_chaos","particlebomb_tap","beacon_tap","beacon_surge","shadow_tap","shadow_clone_catch","spectral_tap","spectral_perfect","heart_tap","nova_tap","firefly_tap","firefly_swift","geode_crack","geode_gem","timebomb_defuse","timebomb_clutch","thunderbolt_tap","thunderbolt_clutch","gravityorb_tap","gravityorb_cluster","crystalball_tap"],
    progression: ["level_10","level_50","level_100","prestige_1","three_stars_5","mascot_lv10","streak_25","streak_50","streak_10","streak_5","score_2000","world_complete"],
    social:      ["missions_all","daily_7","friday_fever","weekend_warrior","all_worlds","streak_saver","loot_chest"],
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
            <div className="flex items-center justify-between mb-2">
              <div className="text-xs font-bold opacity-50 uppercase tracking-widest" style={{color:theme.accent}}>🌍 World Records</div>
              <div className="text-xs opacity-40">{Object.keys(sv.worldBest||{}).length}/{WORLDS.length} worlds</div>
            </div>
            <div className="grid grid-cols-2 gap-1.5">
              {WORLDS.map(w=>{
                const best=(sv.worldBest||{})[w.id];
                if(!best)return null;
                const worldLvl=getLevelConfig(w.id*10);
                const ratio=best/(worldLvl.scoreGoal||1);
                const rank=ratio>=3?"S+":ratio>=2.2?"S":ratio>=1.5?"A":ratio>=1?"B":"C";
                const rankColor={"S+":"#ffd700","S":"#f97316","A":"#a78bfa","B":"#60a5fa","C":"#94a3b8"}[rank]||"#fff";
                return(
                  <div key={w.id} className="flex items-center gap-1.5 rounded-xl px-2 py-1.5"
                    style={{background:`${w.color}0e`,border:`1px solid ${w.color}33`}}>
                    <span style={{fontSize:14}}>{w.emoji}</span>
                    <div className="flex-1 min-w-0">
                      <div style={{fontSize:9,color:w.color,opacity:0.7,letterSpacing:"0.04em",fontWeight:"bold"}}>{w.name}</div>
                      <div style={{fontSize:12,color:w.color,fontWeight:"black",tabularNums:true}}>{best.toLocaleString()}</div>
                    </div>
                    <div style={{fontSize:13,fontWeight:"black",color:rankColor,
                      textShadow:`0 0 8px ${rankColor}88`,minWidth:22,textAlign:"center"}}>{rank}</div>
                  </div>
                );
              }).filter(Boolean)}
            </div>
            {Object.keys(sv.worldBest||{}).length===WORLDS.length&&(
              <div className="mt-2 text-center text-xs font-bold" style={{color:"#ffd700",
                textShadow:"0 0 12px #ffd70088"}}>🌟 All worlds conquered! 🌟</div>
            )}
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
                {/* Personal best with this mascot */}
                {isUnlocked&&(()=>{
                  const mBest=(sv2.mascotScores||{})[m.id]||0;
                  return mBest>0?(
                    <div style={{fontSize:8,color:rs.border,opacity:0.75,letterSpacing:"0.03em"}}>
                      🏆 {mBest.toLocaleString()} pts
                    </div>
                  ):null;
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
      {/* Haptic intensity slider */}
      {(sv.hapticEnabled!==false)&&<div>
        <p className="text-xs font-bold opacity-40 mb-3 uppercase tracking-widest" style={{color:theme.accent}}>Haptic Intensity</p>
        <div className="flex items-center gap-3">
          <span className="text-xs" style={{color:theme.accent}}>📳</span>
          <input type="range" min={10} max={100} step={10} value={sv.hapticIntensity??70}
            onChange={e=>{const v=parseInt(e.target.value);sv.hapticIntensity=v;_hapticIntensity=v;debounceSave();vibrate([v]);}}
            style={{flex:1,accentColor:theme.accent}}/>
          <span className="text-xs w-10 text-right opacity-50" style={{color:theme.accent}}>{sv.hapticIntensity??70}%</span>
        </div>
        <p className="text-xs opacity-30 mt-1" style={{color:"#fff"}}>Higher = stronger vibrations</p>
      </div>}
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
      {/* Data management */}
      <div className="border-t border-white border-opacity-10 pt-4 flex flex-col gap-2">
        <p className="text-xs font-bold opacity-40 uppercase tracking-widest mb-1" style={{color:theme.accent}}>Data</p>
        <NeonButton onClick={()=>{
          const data=JSON.stringify(saveRef.current,null,2);
          const blob=new Blob([data],{type:"application/json"});
          const url=URL.createObjectURL(blob);
          const a=document.createElement("a");a.href=url;a.download="nexustap_save.json";a.click();
          URL.revokeObjectURL(url);
          setNotif("💾 Save exported!");
        }} className="w-full py-3 text-sm" style={{background:"#3b82f618",border:"1px solid #3b82f655",color:"#60a5fa"}}>
          💾 Export Save Data
        </NeonButton>
        <NeonButton onClick={()=>{
          const inp=document.createElement("input");inp.type="file";inp.accept=".json";
          inp.onchange=e=>{
            const file=e.target.files[0];if(!file)return;
            const reader=new FileReader();
            reader.onload=ev=>{
              try{
                const imported=JSON.parse(ev.target.result);
                if(imported.highScore!==undefined&&imported.coins!==undefined){
                  Object.assign(saveRef.current,imported);flushSave();
                  setNotif("✅ Save imported!");go("menu");
                } else setNotif("❌ Invalid save file");
              } catch{setNotif("❌ Could not read file");}
            };reader.readAsText(file);
          };inp.click();
        }} className="w-full py-3 text-sm" style={{background:"#8b5cf618",border:"1px solid #8b5cf655",color:"#a78bfa"}}>
          📂 Import Save Data
        </NeonButton>
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

  // ── Time Attack Mode ──
  const renderTimeAttack=()=>{
    const taBest=sv.taBest||0;
    const worldCfg=getTimeAttackConfig(taWorld);
    const taWorld_=WORLDS[taWorld-1];
    return(
      <div className="flex flex-col h-full px-5 py-6 gap-5 relative z-10 items-center justify-center">
        <NeonButton onClick={()=>go("menu")} className="absolute top-4 left-4 px-3 py-2 text-sm" style={{background:"#ffffff10"}}>← Back</NeonButton>
        <div className="text-center">
          <div className="text-5xl mb-2" style={{animation:"heartbeat 0.8s ease-in-out infinite",filter:"drop-shadow(0 0 20px #f97316)"}}>⚡</div>
          <h2 className="font-black text-3xl" style={{color:"#f97316",textShadow:"0 0 30px #f97316aa",fontFamily:"'Rajdhani',sans-serif",letterSpacing:"0.1em"}}>TIME ATTACK</h2>
          <p className="text-sm opacity-60 mt-1" style={{color:"#f97316"}}>45 seconds. Max score wins. No mercy.</p>
        </div>
        {taBest>0&&(
          <div className="px-6 py-3 rounded-2xl text-center" style={{background:"#f9731618",border:"1px solid #f9731644"}}>
            <div className="text-xs opacity-50 mb-1" style={{color:"#f97316"}}>Personal Best</div>
            <div className="text-2xl font-black" style={{color:"#f97316"}}>{taBest.toLocaleString()}</div>
            {sv.taBestWorld&&<div className="text-xs opacity-40" style={{color:"#f97316"}}>World {sv.taBestWorld}: {WORLDS[(sv.taBestWorld||1)-1].name}</div>}
          </div>
        )}
        {/* World selector */}
        <div className="w-full rounded-2xl p-3" style={{background:"#ffffff08",border:"1px solid #f9731633"}}>
          <div className="text-xs opacity-40 mb-2 uppercase tracking-widest text-center" style={{color:"#f97316"}}>Choose World</div>
          <div className="grid grid-cols-5 gap-1.5">
            {WORLDS.map(w=>(
              <NeonButton key={w.id} onClick={()=>setTaWorld(w.id)}
                className="py-2 text-center text-lg rounded-xl"
                style={{background:taWorld===w.id?`${w.color}33`:"#ffffff06",
                  border:`1px solid ${taWorld===w.id?w.color:"#ffffff10"}`,
                  boxShadow:taWorld===w.id?`0 0 8px ${w.color}66`:"none"}}>
                {w.emoji}
              </NeonButton>
            ))}
          </div>
          <div className="text-center mt-2 text-xs font-bold" style={{color:taWorld_.color}}>{taWorld_.name}</div>
        </div>
        {/* Rules */}
        <div className="w-full rounded-xl px-4 py-3 text-xs" style={{background:"#ffffff06",border:"1px solid #f9731622",color:"#aaa",lineHeight:1.7}}>
          ⏱ <strong style={{color:"#f97316"}}>45 seconds</strong> — tap everything you can<br/>
          💣 <strong style={{color:"#ef4444"}}>Bombs</strong> are present — watch out!<br/>
          🌈 <strong style={{color:"#a78bfa"}}>All rarities</strong> spawn rapidly — chain them!<br/>
          🏆 Score is saved to your personal best
        </div>
        <NeonButton onClick={()=>startGame(0,[],worldCfg)}
          className="w-full py-5 text-xl font-black"
          style={{background:"linear-gradient(135deg,#ea580c,#f97316)",boxShadow:"0 0 40px #f9731666",letterSpacing:"0.1em"}}>
          ⚡ START ATTACK!
        </NeonButton>
        <p className="text-xs text-center opacity-30" style={{color:"#f97316"}}>3 lives · Bombs active · Ultra-fast spawn rate</p>
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
        <>
          {/* Background flash for high-XP achievements */}
          {achPopup.xp>=60&&<div className="absolute inset-0 z-49 pointer-events-none"
            style={{background:"radial-gradient(circle at 50% 78%,#ffd70033 0%,transparent 70%)",
              animation:"epicFlash 0.6s ease-out forwards"}}/>}
          <div className="absolute z-50 pointer-events-none"
            style={{bottom:"22%",left:"50%",transform:"translateX(-50%)",animation:"perfectPop 2.2s cubic-bezier(0.34,1.4,0.64,1) forwards",textAlign:"center",whiteSpace:"nowrap"}}>
            <div className="flex items-center gap-2 px-4 py-3 rounded-2xl"
              style={{background:"rgba(0,0,0,0.92)",
                border:`2px solid ${achPopup.xp>=75?"#ffd700":achPopup.xp>=50?"#f97316":"#ffd70066"}`,
                boxShadow:`0 0 ${achPopup.xp>=75?"48px #ffd700aa":"28px #ffd70044"},0 4px 20px rgba(0,0,0,0.6)`,
                backdropFilter:"blur(12px)",
                animation:achPopup.xp>=75?"perfectPop 2.2s cubic-bezier(0.34,1.4,0.64,1) forwards,legendaryRainbow 1.5s linear infinite":"perfectPop 2.2s cubic-bezier(0.34,1.4,0.64,1) forwards",
              }}>
              <span style={{fontSize:32,filter:achPopup.xp>=75?"drop-shadow(0 0 12px #ffd700)":"none"}}>{achPopup.icon}</span>
              <div className="flex flex-col items-start">
                <div style={{fontSize:11,color:achPopup.xp>=75?"#ffd700":"#ffd700",fontWeight:"black",letterSpacing:"0.08em",textTransform:"uppercase"}}>
                  {achPopup.xp>=75?"⭐ EPIC ACHIEVEMENT!":achPopup.xp>=50?"🏆 ACHIEVEMENT!":"Achievement!"}
                </div>
                <div style={{fontSize:14,color:"#fff",fontWeight:"bold"}}>{achPopup.label}</div>
                <div style={{fontSize:10,color:"#fbbf24",opacity:0.9}}>+{achPopup.xp} XP ✨</div>
              </div>
            </div>
          </div>
        </>
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
      {screen==="timeattack"    &&renderTimeAttack()}
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
