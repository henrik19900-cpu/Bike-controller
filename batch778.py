#!/usr/bin/env python3
"""Batch 778: CAPE_GLOW44+BLUFF_GLOW44 + LevyneFox9e+LibetheniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4361"
SW = "2350"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.23"
ORB_R = f"{BASE_R}*2.22"
FOXSC = 540
ORBSC = 535
PW1SC = 2576
PW2SC = 2578

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"laumontite_fox9e_tap", label:"Laumontite Fox Tap"'
A1_NEW = (
    '  { id:"levyne_fox9e_tap", label:"Levyne Fox Tap", desc:"Tap Levyne Fox", icon:"🦊", xp:62 },\n'
    '  { id:"levyne_fox9e_peak", label:"Levyne Fox Peak", desc:"Tap Levyne Fox at peak", icon:"🌺", xp:88 },\n'
    '  { id:"libethenite_orb9e_tap", label:"Libethenite Orb Tap", desc:"Tap Libethenite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"libethenite_orb9e_peak", label:"Libethenite Orb Peak", desc:"Tap Libethenite Orb at peak", icon:"💜", xp:88 },\n'
    '  { id:"cape_glow44_use", label:"Cape Glow Use", desc:"Activate Cape Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"cape_glow44_max", label:"Cape Glow Max", desc:"Activate Cape Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"bluff_glow44_use", label:"Bluff Glow Use", desc:"Activate Bluff Glow power-up", icon:"🪨", xp:50 },\n'
    '  { id:"bluff_glow44_max", label:"Bluff Glow Max", desc:"Activate Bluff Glow at max streak", icon:"🪨", xp:75 },\n'
    '  { id:"laumontite_fox9e_tap", label:"Laumontite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"SHORE_GLOW44","INLET_GLOW44","HARBOR_GLOW44"'
A2_NEW = '"CAPE_GLOW44","BLUFF_GLOW44","SHORE_GLOW44","INLET_GLOW44","HARBOR_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="SHORE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="CAPE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} CAPE GLOW",cx,cy,"#a5f3fc");\n'
    '        spawnShockwave(cx,cy,"#0891b2");sfx("powerUp");\n'
    '        unlock("cape_glow44_use");if(gs.streak>=20)unlock("cape_glow44_max");\n'
    '      } else if(ptype==="BLUFF_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} BLUFF GLOW",cx,cy,"#d6d3d1");\n'
    '        spawnShockwave(cx,cy,"#57534e");sfx("powerUp");\n'
    '        unlock("bluff_glow44_use");if(gs.streak>=20)unlock("bluff_glow44_max");\n'
    '      } else if(ptype==="SHORE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// SHORE_GLOW44 — +2572 shore glow bonus'
A4_NEW = (
    f'// CAPE_GLOW44 — +{PW1SC} cape glow bonus\n'
    f'        // BLUFF_GLOW44 — +{PW2SC} bluff glow bonus\n'
    '        // SHORE_GLOW44 — +2572 shore glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawLaumontiteFox9e('
A5_NEW = (
    f'function drawLevyneFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffe4e6");g.addColorStop(0.45+sp*0.35,"#e11d48");g.addColorStop(1,"#881337");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(255,228,230,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#881337":"#ffe4e6";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌺":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawLibetheniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fae8ff");g.addColorStop(0.35+tp*0.35,"#a21caf");g.addColorStop(1,"#4a044e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(250,232,255,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(162,28,175,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#a21caf":"#fae8ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💜":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawLaumontiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="laumontite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="levyne_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp778a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLevyneFox9e(ctx,t.radius,ts,sp778a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="libethenite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp778b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLibetheniteOrb9e(ctx,t.radius,ts,tp778b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="laumontite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="laumontite_fox9e"){'
A7_NEW = (
    'if(hit.type==="levyne_fox9e"){\n'
    f'          const sp778c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts778a=Math.round({FOXSC}*(1+sp778c));\n'
    '          gs.score+=pts778a;gs.streak++;addPopup("+"+pts778a+(sp778c>0.88?" 🌺 PEAK!":""),hit.x,hit.y,"#ffe4e6");\n'
    '          spawnShockwave(hit.x,hit.y,"#e11d48");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp778c>0.88){sfx("legendary");unlock("levyne_fox9e_peak");}else unlock("levyne_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="libethenite_orb9e"){\n'
    f'          const tp778d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts778b=Math.round({ORBSC}*(1+tp778d));\n'
    '          gs.score+=pts778b;gs.streak++;addPopup("+"+pts778b+(tp778d>0.88?" 💜 PEAK!":""),hit.x,hit.y,"#fae8ff");\n'
    '          spawnShockwave(hit.x,hit.y,"#a21caf");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp778d>0.88){sfx("legendary");unlock("libethenite_orb9e_peak");}else unlock("libethenite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="laumontite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="laumontite_fox9e";color="#db2777";glow="#fce7f3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="leonite_orb9e"')
A8_NEW = (
    '      type="levyne_fox9e";color="#e11d48";glow="#ffe4e6";\n'
    '    } else if('+COND100F+'){\n'
    '      type="libethenite_orb9e";color="#a21caf";glow="#fae8ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="laumontite_fox9e";color="#db2777";glow="#fce7f3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="leonite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="laumontite_fox9e"?BASE_R*2.22:type==="leonite_orb9e"?BASE_R*2.21:'
A9_NEW = f'type==="levyne_fox9e"?{FOX_R}:type==="libethenite_orb9e"?{ORB_R}:type==="laumontite_fox9e"?BASE_R*2.22:type==="leonite_orb9e"?BASE_R*2.21:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'SHORE_GLOW44:"🏖️✨",INLET_GLOW44:"🌊✨",HARBOR_GLOW44:"⚓✨"'
A10_NEW = 'CAPE_GLOW44:"🌊✨",BLUFF_GLOW44:"🪨✨",SHORE_GLOW44:"🏖️✨",INLET_GLOW44:"🌊✨",HARBOR_GLOW44:"⚓✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 778 done! +{len(src)-orig_len} bytes")
