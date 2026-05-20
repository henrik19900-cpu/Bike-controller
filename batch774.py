#!/usr/bin/env python3
"""Batch 774: LAKE_GLOW44+RIVER_GLOW44 + KesteriteFox9e+KilchoaniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4345"
SW = "2342"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.19"
ORB_R = f"{BASE_R}*2.18"
FOXSC = 532
ORBSC = 527
PW1SC = 2560
PW2SC = 2562

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"jungeite_fox9e_tap", label:"Jungeite Fox Tap"'
A1_NEW = (
    '  { id:"kesterite_fox9e_tap", label:"Kesterite Fox Tap", desc:"Tap Kesterite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"kesterite_fox9e_peak", label:"Kesterite Fox Peak", desc:"Tap Kesterite Fox at peak", icon:"🟡", xp:88 },\n'
    '  { id:"kilchoanite_orb9e_tap", label:"Kilchoanite Orb Tap", desc:"Tap Kilchoanite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"kilchoanite_orb9e_peak", label:"Kilchoanite Orb Peak", desc:"Tap Kilchoanite Orb at peak", icon:"🌿", xp:88 },\n'
    '  { id:"lake_glow44_use", label:"Lake Glow Use", desc:"Activate Lake Glow power-up", icon:"🏔️", xp:50 },\n'
    '  { id:"lake_glow44_max", label:"Lake Glow Max", desc:"Activate Lake Glow at max streak", icon:"🏔️", xp:75 },\n'
    '  { id:"river_glow44_use", label:"River Glow Use", desc:"Activate River Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"river_glow44_max", label:"River Glow Max", desc:"Activate River Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"jungeite_fox9e_tap", label:"Jungeite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"SPRING_GLOW44","POND_GLOW44","STREAM_GLOW44"'
A2_NEW = '"LAKE_GLOW44","RIVER_GLOW44","SPRING_GLOW44","POND_GLOW44","STREAM_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="SPRING_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="LAKE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} LAKE GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0284c7");sfx("powerUp");\n'
    '        unlock("lake_glow44_use");if(gs.streak>=20)unlock("lake_glow44_max");\n'
    '      } else if(ptype==="RIVER_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} RIVER GLOW",cx,cy,"#38bdf8");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("river_glow44_use");if(gs.streak>=20)unlock("river_glow44_max");\n'
    '      } else if(ptype==="SPRING_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// SPRING_GLOW44 — +2556 spring glow bonus'
A4_NEW = (
    f'// LAKE_GLOW44 — +{PW1SC} lake glow bonus\n'
    f'        // RIVER_GLOW44 — +{PW2SC} river glow bonus\n'
    '        // SPRING_GLOW44 — +2556 spring glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawJungeite773Fox9e('
A5_NEW = (
    f'function drawKesteriteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.45+sp*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,249,195,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#713f12":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟡":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawKilchoaniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.35+tp*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(220,252,231,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,163,74,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#16a34a":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌿":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawJungeite773Fox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="jungeite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="kesterite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp774a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawKesteriteFox9e(ctx,t.radius,ts,sp774a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="kilchoanite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp774b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawKilchoaniteOrb9e(ctx,t.radius,ts,tp774b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="jungeite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="jungeite_fox9e"){'
A7_NEW = (
    'if(hit.type==="kesterite_fox9e"){\n'
    f'          const sp774c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts774a=Math.round({FOXSC}*(1+sp774c));\n'
    '          gs.score+=pts774a;gs.streak++;addPopup("+"+pts774a+(sp774c>0.88?" 🟡 PEAK!":""),hit.x,hit.y,"#fef9c3");\n'
    '          spawnShockwave(hit.x,hit.y,"#ca8a04");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp774c>0.88){sfx("legendary");unlock("kesterite_fox9e_peak");}else unlock("kesterite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="kilchoanite_orb9e"){\n'
    f'          const tp774d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts774b=Math.round({ORBSC}*(1+tp774d));\n'
    '          gs.score+=pts774b;gs.streak++;addPopup("+"+pts774b+(tp774d>0.88?" 🌿 PEAK!":""),hit.x,hit.y,"#dcfce7");\n'
    '          spawnShockwave(hit.x,hit.y,"#16a34a");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp774d>0.88){sfx("legendary");unlock("kilchoanite_orb9e_peak");}else unlock("kilchoanite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="jungeite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="jungeite_fox9e";color="#b45309";glow="#fde68a";\n'
          '    } else if('+COND100F+'){\n'
          '      type="jennite_orb9e"')
A8_NEW = (
    '      type="kesterite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="kilchoanite_orb9e";color="#16a34a";glow="#dcfce7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="jungeite_fox9e";color="#b45309";glow="#fde68a";\n'
    '    } else if('+COND100F+'){\n'
    '      type="jennite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="jungeite_fox9e"?BASE_R*2.18:type==="jennite_orb9e"?BASE_R*2.17:'
A9_NEW = f'type==="kesterite_fox9e"?{FOX_R}:type==="kilchoanite_orb9e"?{ORB_R}:type==="jungeite_fox9e"?BASE_R*2.18:type==="jennite_orb9e"?BASE_R*2.17:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'SPRING_GLOW44:"🌱✨",POND_GLOW44:"🐸✨",STREAM_GLOW44:"🌊✨"'
A10_NEW = 'LAKE_GLOW44:"🏔️✨",RIVER_GLOW44:"🌊✨",SPRING_GLOW44:"🌱✨",POND_GLOW44:"🐸✨",STREAM_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 774 done! +{len(src)-orig_len} bytes")
