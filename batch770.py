#!/usr/bin/env python3
"""Batch 770: CLIFF_GLOW44+GORGE_GLOW44 + HuebneriteFox9e+HuntiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4329"
SW = "2334"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.15"
ORB_R = f"{BASE_R}*2.14"
FOXSC = 524
ORBSC = 519
PW1SC = 2544
PW2SC = 2546

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"hollandite_fox9e_tap", label:"Hollandite Fox Tap"'
A1_NEW = (
    '  { id:"huebnerite_fox9e_tap", label:"Huebnerite Fox Tap", desc:"Tap Huebnerite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"huebnerite_fox9e_peak", label:"Huebnerite Fox Peak", desc:"Tap Huebnerite Fox at peak", icon:"🔴", xp:88 },\n'
    '  { id:"huntite_orb9e_tap", label:"Huntite Orb Tap", desc:"Tap Huntite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"huntite_orb9e_peak", label:"Huntite Orb Peak", desc:"Tap Huntite Orb at peak", icon:"⚪", xp:88 },\n'
    '  { id:"cliff_glow44_use", label:"Cliff Glow Use", desc:"Activate Cliff Glow power-up", icon:"🪨", xp:50 },\n'
    '  { id:"cliff_glow44_max", label:"Cliff Glow Max", desc:"Activate Cliff Glow at max streak", icon:"🪨", xp:75 },\n'
    '  { id:"gorge_glow44_use", label:"Gorge Glow Use", desc:"Activate Gorge Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"gorge_glow44_max", label:"Gorge Glow Max", desc:"Activate Gorge Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"hollandite_fox9e_tap", label:"Hollandite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"PEAK_GLOW44","VALE_GLOW44","SLOPE_GLOW44"'
A2_NEW = '"CLIFF_GLOW44","GORGE_GLOW44","PEAK_GLOW44","VALE_GLOW44","SLOPE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="PEAK_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="CLIFF_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} CLIFF GLOW",cx,cy,"#f1f5f9");\n'
    '        spawnShockwave(cx,cy,"#64748b");sfx("powerUp");\n'
    '        unlock("cliff_glow44_use");if(gs.streak>=20)unlock("cliff_glow44_max");\n'
    '      } else if(ptype==="GORGE_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} GORGE GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0c4a6e");sfx("powerUp");\n'
    '        unlock("gorge_glow44_use");if(gs.streak>=20)unlock("gorge_glow44_max");\n'
    '      } else if(ptype==="PEAK_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// PEAK_GLOW44 — +2540 peak glow bonus'
A4_NEW = (
    f'// CLIFF_GLOW44 — +{PW1SC} cliff glow bonus\n'
    f'        // GORGE_GLOW44 — +{PW2SC} gorge glow bonus\n'
    '        // PEAK_GLOW44 — +2540 peak glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHollanditeFox9e('
A5_NEW = (
    f'function drawHuebneriteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fecaca");g.addColorStop(0.45+sp*0.35,"#991b1b");g.addColorStop(1,"#450a0a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,202,202,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#450a0a":"#fecaca";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🔴":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawHuntiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffffff");g.addColorStop(0.35+tp*0.35,"#d1d5db");g.addColorStop(1,"#374151");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(255,255,255,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(209,213,219,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#d1d5db":"#ffffff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"⚪":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawHollanditeFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="hollandite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="huebnerite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp770a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHuebneriteFox9e(ctx,t.radius,ts,sp770a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="huntite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp770b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHuntiteOrb9e(ctx,t.radius,ts,tp770b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hollandite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="hollandite_fox9e"){'
A7_NEW = (
    'if(hit.type==="huebnerite_fox9e"){\n'
    f'          const sp770c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts770a=Math.round({FOXSC}*(1+sp770c));\n'
    '          gs.score+=pts770a;gs.streak++;addPopup("+"+pts770a+(sp770c>0.88?" 🔴 PEAK!":""),hit.x,hit.y,"#fecaca");\n'
    '          spawnShockwave(hit.x,hit.y,"#991b1b");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp770c>0.88){sfx("legendary");unlock("huebnerite_fox9e_peak");}else unlock("huebnerite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="huntite_orb9e"){\n'
    f'          const tp770d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts770b=Math.round({ORBSC}*(1+tp770d));\n'
    '          gs.score+=pts770b;gs.streak++;addPopup("+"+pts770b+(tp770d>0.88?" ⚪ PEAK!":""),hit.x,hit.y,"#ffffff");\n'
    '          spawnShockwave(hit.x,hit.y,"#d1d5db");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp770d>0.88){sfx("legendary");unlock("huntite_orb9e_peak");}else unlock("huntite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hollandite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="hollandite_fox9e";color="#334155";glow="#e2e8f0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="howlite_orb9e"')
A8_NEW = (
    '      type="huebnerite_fox9e";color="#991b1b";glow="#fecaca";\n'
    '    } else if('+COND100F+'){\n'
    '      type="huntite_orb9e";color="#d1d5db";glow="#ffffff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hollandite_fox9e";color="#334155";glow="#e2e8f0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="howlite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="hollandite_fox9e"?BASE_R*2.14:type==="howlite_orb9e"?BASE_R*2.13:'
A9_NEW = f'type==="huebnerite_fox9e"?{FOX_R}:type==="huntite_orb9e"?{ORB_R}:type==="hollandite_fox9e"?BASE_R*2.14:type==="howlite_orb9e"?BASE_R*2.13:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'PEAK_GLOW44:"⛰️✨",VALE_GLOW44:"🌿✨",SLOPE_GLOW44:"🏔️✨"'
A10_NEW = 'CLIFF_GLOW44:"🪨✨",GORGE_GLOW44:"🌊✨",PEAK_GLOW44:"⛰️✨",VALE_GLOW44:"🌿✨",SLOPE_GLOW44:"🏔️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 770 done! +{len(src)-orig_len} bytes")
