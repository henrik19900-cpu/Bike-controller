#!/usr/bin/env python3
"""Batch 775: OCEAN_GLOW44+BAY_GLOW44 + KoechliniteFox9e+KottigiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4349"
SW = "2344"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.20"
ORB_R = f"{BASE_R}*2.19"
FOXSC = 534
ORBSC = 529
PW1SC = 2564
PW2SC = 2566

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"kesterite_fox9e_tap", label:"Kesterite Fox Tap"'
A1_NEW = (
    '  { id:"koechlinite_fox9e_tap", label:"Koechlinite Fox Tap", desc:"Tap Koechlinite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"koechlinite_fox9e_peak", label:"Koechlinite Fox Peak", desc:"Tap Koechlinite Fox at peak", icon:"🟠", xp:88 },\n'
    '  { id:"kottigite_orb9e_tap", label:"Kottigite Orb Tap", desc:"Tap Kottigite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"kottigite_orb9e_peak", label:"Kottigite Orb Peak", desc:"Tap Kottigite Orb at peak", icon:"🟣", xp:88 },\n'
    '  { id:"ocean_glow44_use", label:"Ocean Glow Use", desc:"Activate Ocean Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"ocean_glow44_max", label:"Ocean Glow Max", desc:"Activate Ocean Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"bay_glow44_use", label:"Bay Glow Use", desc:"Activate Bay Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"bay_glow44_max", label:"Bay Glow Max", desc:"Activate Bay Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"kesterite_fox9e_tap", label:"Kesterite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"LAKE_GLOW44","RIVER_GLOW44","SPRING_GLOW44"'
A2_NEW = '"OCEAN_GLOW44","BAY_GLOW44","LAKE_GLOW44","RIVER_GLOW44","SPRING_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="LAKE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="OCEAN_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} OCEAN GLOW",cx,cy,"#38bdf8");\n'
    '        spawnShockwave(cx,cy,"#0c4a6e");sfx("powerUp");\n'
    '        unlock("ocean_glow44_use");if(gs.streak>=20)unlock("ocean_glow44_max");\n'
    '      } else if(ptype==="BAY_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} BAY GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#075985");sfx("powerUp");\n'
    '        unlock("bay_glow44_use");if(gs.streak>=20)unlock("bay_glow44_max");\n'
    '      } else if(ptype==="LAKE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// LAKE_GLOW44 — +2560 lake glow bonus'
A4_NEW = (
    f'// OCEAN_GLOW44 — +{PW1SC} ocean glow bonus\n'
    f'        // BAY_GLOW44 — +{PW2SC} bay glow bonus\n'
    '        // LAKE_GLOW44 — +2560 lake glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawKesteriteFox9e('
A5_NEW = (
    f'function drawKoechliniteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fed7aa");g.addColorStop(0.45+sp*0.35,"#ea580c");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,215,170,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#7c2d12":"#fed7aa";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟠":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawKottigiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e9d5ff");g.addColorStop(0.35+tp*0.35,"#7e22ce");g.addColorStop(1,"#3b0764");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(233,213,255,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(126,34,206,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#7e22ce":"#e9d5ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟣":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawKesteriteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="kesterite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="koechlinite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp775a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawKoechliniteFox9e(ctx,t.radius,ts,sp775a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="kottigite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp775b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawKottigiteOrb9e(ctx,t.radius,ts,tp775b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="kesterite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="kesterite_fox9e"){'
A7_NEW = (
    'if(hit.type==="koechlinite_fox9e"){\n'
    f'          const sp775c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts775a=Math.round({FOXSC}*(1+sp775c));\n'
    '          gs.score+=pts775a;gs.streak++;addPopup("+"+pts775a+(sp775c>0.88?" 🟠 PEAK!":""),hit.x,hit.y,"#fed7aa");\n'
    '          spawnShockwave(hit.x,hit.y,"#ea580c");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp775c>0.88){sfx("legendary");unlock("koechlinite_fox9e_peak");}else unlock("koechlinite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="kottigite_orb9e"){\n'
    f'          const tp775d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts775b=Math.round({ORBSC}*(1+tp775d));\n'
    '          gs.score+=pts775b;gs.streak++;addPopup("+"+pts775b+(tp775d>0.88?" 🟣 PEAK!":""),hit.x,hit.y,"#e9d5ff");\n'
    '          spawnShockwave(hit.x,hit.y,"#7e22ce");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp775d>0.88){sfx("legendary");unlock("kottigite_orb9e_peak");}else unlock("kottigite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="kesterite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="kesterite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="kilchoanite_orb9e"')
A8_NEW = (
    '      type="koechlinite_fox9e";color="#ea580c";glow="#fed7aa";\n'
    '    } else if('+COND100F+'){\n'
    '      type="kottigite_orb9e";color="#7e22ce";glow="#e9d5ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="kesterite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="kilchoanite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="kesterite_fox9e"?BASE_R*2.19:type==="kilchoanite_orb9e"?BASE_R*2.18:'
A9_NEW = f'type==="koechlinite_fox9e"?{FOX_R}:type==="kottigite_orb9e"?{ORB_R}:type==="kesterite_fox9e"?BASE_R*2.19:type==="kilchoanite_orb9e"?BASE_R*2.18:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'LAKE_GLOW44:"🏔️✨",RIVER_GLOW44:"🌊✨",SPRING_GLOW44:"🌱✨"'
A10_NEW = 'OCEAN_GLOW44:"🌊✨",BAY_GLOW44:"⚓✨",LAKE_GLOW44:"🏔️✨",RIVER_GLOW44:"🌊✨",SPRING_GLOW44:"🌱✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 775 done! +{len(src)-orig_len} bytes")
