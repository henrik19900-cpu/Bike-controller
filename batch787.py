#!/usr/bin/env python3
"""Batch 787: ISLE_GLOW44+SHOAL_GLOW44 + MurdochiteFox9e+MurmaniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4397"
SW = "2368"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.32"
ORB_R = f"{BASE_R}*2.31"
FOXSC = 558
ORBSC = 553
PW1SC = 2612
PW2SC = 2614

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"molybdenite_fox9e_tap", label:"Molybdenite Fox Tap"'
A1_NEW = (
    '  { id:"murdochite_fox9e_tap", label:"Murdochite Fox Tap", desc:"Tap Murdochite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"murdochite_fox9e_peak", label:"Murdochite Fox Peak", desc:"Tap Murdochite Fox at peak", icon:"🌿", xp:88 },\n'
    '  { id:"murmanite_orb9e_tap", label:"Murmanite Orb Tap", desc:"Tap Murmanite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"murmanite_orb9e_peak", label:"Murmanite Orb Peak", desc:"Tap Murmanite Orb at peak", icon:"🔴", xp:88 },\n'
    '  { id:"isle_glow44_use", label:"Isle Glow Use", desc:"Activate Isle Glow power-up", icon:"🏝️", xp:50 },\n'
    '  { id:"isle_glow44_max", label:"Isle Glow Max", desc:"Activate Isle Glow at max streak", icon:"🏝️", xp:75 },\n'
    '  { id:"shoal_glow44_use", label:"Shoal Glow Use", desc:"Activate Shoal Glow power-up", icon:"🐟", xp:50 },\n'
    '  { id:"shoal_glow44_max", label:"Shoal Glow Max", desc:"Activate Shoal Glow at max streak", icon:"🐟", xp:75 },\n'
    '  { id:"molybdenite_fox9e_tap", label:"Molybdenite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"GULF_GLOW44","FJORD_GLOW44","CHANNEL_GLOW44"'
A2_NEW = '"ISLE_GLOW44","SHOAL_GLOW44","GULF_GLOW44","FJORD_GLOW44","CHANNEL_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="GULF_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="ISLE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} ISLE GLOW",cx,cy,"#bbf7d0");\n'
    '        spawnShockwave(cx,cy,"#15803d");sfx("powerUp");\n'
    '        unlock("isle_glow44_use");if(gs.streak>=20)unlock("isle_glow44_max");\n'
    '      } else if(ptype==="SHOAL_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} SHOAL GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0284c7");sfx("powerUp");\n'
    '        unlock("shoal_glow44_use");if(gs.streak>=20)unlock("shoal_glow44_max");\n'
    '      } else if(ptype==="GULF_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// GULF_GLOW44 — +2608 gulf glow bonus'
A4_NEW = (
    f'// ISLE_GLOW44 — +{PW1SC} isle glow bonus\n'
    f'        // SHOAL_GLOW44 — +{PW2SC} shoal glow bonus\n'
    '        // GULF_GLOW44 — +2608 gulf glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMolybdeniteFox9e('
A5_NEW = (
    f'function drawMurdochiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d1fae5");g.addColorStop(0.45+sp*0.35,"#047857");g.addColorStop(1,"#022c22");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(209,250,229,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#022c22":"#d1fae5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌿":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMurmaniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fecaca");g.addColorStop(0.35+tp*0.35,"#b91c1c");g.addColorStop(1,"#450a0a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,202,202,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(185,28,28,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#b91c1c":"#fecaca";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔴":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMolybdeniteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="molybdenite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="murdochite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp787a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMurdochiteFox9e(ctx,t.radius,ts,sp787a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="murmanite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp787b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMurmaniteOrb9e(ctx,t.radius,ts,tp787b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="molybdenite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="molybdenite_fox9e"){'
A7_NEW = (
    'if(hit.type==="murdochite_fox9e"){\n'
    f'          const sp787c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts787a=Math.round({FOXSC}*(1+sp787c));\n'
    '          gs.score+=pts787a;gs.streak++;addPopup("+"+pts787a+(sp787c>0.88?" 🌿 PEAK!":""),hit.x,hit.y,"#d1fae5");\n'
    '          spawnShockwave(hit.x,hit.y,"#047857");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp787c>0.88){sfx("legendary");unlock("murdochite_fox9e_peak");}else unlock("murdochite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="murmanite_orb9e"){\n'
    f'          const tp787d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts787b=Math.round({ORBSC}*(1+tp787d));\n'
    '          gs.score+=pts787b;gs.streak++;addPopup("+"+pts787b+(tp787d>0.88?" 🔴 PEAK!":""),hit.x,hit.y,"#fecaca");\n'
    '          spawnShockwave(hit.x,hit.y,"#b91c1c");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp787d>0.88){sfx("legendary");unlock("murmanite_orb9e_peak");}else unlock("murmanite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="molybdenite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="molybdenite_fox9e";color="#27272a";glow="#d4d4d8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="mosandrite_orb9e"')
A8_NEW = (
    '      type="murdochite_fox9e";color="#047857";glow="#d1fae5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="murmanite_orb9e";color="#b91c1c";glow="#fecaca";\n'
    '    } else if('+COND100F+'){\n'
    '      type="molybdenite_fox9e";color="#27272a";glow="#d4d4d8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mosandrite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="molybdenite_fox9e"?BASE_R*2.31:type==="mosandrite_orb9e"?BASE_R*2.30:'
A9_NEW = f'type==="murdochite_fox9e"?{FOX_R}:type==="murmanite_orb9e"?{ORB_R}:type==="molybdenite_fox9e"?BASE_R*2.31:type==="mosandrite_orb9e"?BASE_R*2.30:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'GULF_GLOW44:"🌊✨",FJORD_GLOW44:"🏔️✨",CHANNEL_GLOW44:"🌊✨"'
A10_NEW = 'ISLE_GLOW44:"🏝️✨",SHOAL_GLOW44:"🐟✨",GULF_GLOW44:"🌊✨",FJORD_GLOW44:"🏔️✨",CHANNEL_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 787 done! +{len(src)-orig_len} bytes")
