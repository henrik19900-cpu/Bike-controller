#!/usr/bin/env python3
"""Batch 779: CRAG_GLOW44+HELM_GLOW44 + LindgreniteFox9e+LiskearditeOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4365"
SW = "2352"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.24"
ORB_R = f"{BASE_R}*2.23"
FOXSC = 542
ORBSC = 537
PW1SC = 2580
PW2SC = 2582

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"levyne_fox9e_tap", label:"Levyne Fox Tap"'
A1_NEW = (
    '  { id:"lindgrenite_fox9e_tap", label:"Lindgrenite Fox Tap", desc:"Tap Lindgrenite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"lindgrenite_fox9e_peak", label:"Lindgrenite Fox Peak", desc:"Tap Lindgrenite Fox at peak", icon:"🟢", xp:88 },\n'
    '  { id:"liskeardite_orb9e_tap", label:"Liskeardite Orb Tap", desc:"Tap Liskeardite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"liskeardite_orb9e_peak", label:"Liskeardite Orb Peak", desc:"Tap Liskeardite Orb at peak", icon:"🔷", xp:88 },\n'
    '  { id:"crag_glow44_use", label:"Crag Glow Use", desc:"Activate Crag Glow power-up", icon:"🪨", xp:50 },\n'
    '  { id:"crag_glow44_max", label:"Crag Glow Max", desc:"Activate Crag Glow at max streak", icon:"🪨", xp:75 },\n'
    '  { id:"helm_glow44_use", label:"Helm Glow Use", desc:"Activate Helm Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"helm_glow44_max", label:"Helm Glow Max", desc:"Activate Helm Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"levyne_fox9e_tap", label:"Levyne Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"CAPE_GLOW44","BLUFF_GLOW44","SHORE_GLOW44"'
A2_NEW = '"CRAG_GLOW44","HELM_GLOW44","CAPE_GLOW44","BLUFF_GLOW44","SHORE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="CAPE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="CRAG_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} CRAG GLOW",cx,cy,"#e7e5e4");\n'
    '        spawnShockwave(cx,cy,"#78716c");sfx("powerUp");\n'
    '        unlock("crag_glow44_use");if(gs.streak>=20)unlock("crag_glow44_max");\n'
    '      } else if(ptype==="HELM_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} HELM GLOW",cx,cy,"#bfdbfe");\n'
    '        spawnShockwave(cx,cy,"#1d4ed8");sfx("powerUp");\n'
    '        unlock("helm_glow44_use");if(gs.streak>=20)unlock("helm_glow44_max");\n'
    '      } else if(ptype==="CAPE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// CAPE_GLOW44 — +2576 cape glow bonus'
A4_NEW = (
    f'// CRAG_GLOW44 — +{PW1SC} crag glow bonus\n'
    f'        // HELM_GLOW44 — +{PW2SC} helm glow bonus\n'
    '        // CAPE_GLOW44 — +2576 cape glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawLevyneFox9e('
A5_NEW = (
    f'function drawLindgreniteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d1fae5");g.addColorStop(0.45+sp*0.35,"#059669");g.addColorStop(1,"#064e3b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(209,250,229,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#064e3b":"#d1fae5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟢":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawLiskearditeOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dbeafe");g.addColorStop(0.35+tp*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(219,234,254,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(37,99,235,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#2563eb":"#dbeafe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔷":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawLevyneFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="levyne_fox9e"){'
A6_NEW = (
    '  else if(t.type==="lindgrenite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp779a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLindgreniteFox9e(ctx,t.radius,ts,sp779a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="liskeardite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp779b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLiskearditeOrb9e(ctx,t.radius,ts,tp779b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="levyne_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="levyne_fox9e"){'
A7_NEW = (
    'if(hit.type==="lindgrenite_fox9e"){\n'
    f'          const sp779c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts779a=Math.round({FOXSC}*(1+sp779c));\n'
    '          gs.score+=pts779a;gs.streak++;addPopup("+"+pts779a+(sp779c>0.88?" 🟢 PEAK!":""),hit.x,hit.y,"#d1fae5");\n'
    '          spawnShockwave(hit.x,hit.y,"#059669");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp779c>0.88){sfx("legendary");unlock("lindgrenite_fox9e_peak");}else unlock("lindgrenite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="liskeardite_orb9e"){\n'
    f'          const tp779d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts779b=Math.round({ORBSC}*(1+tp779d));\n'
    '          gs.score+=pts779b;gs.streak++;addPopup("+"+pts779b+(tp779d>0.88?" 🔷 PEAK!":""),hit.x,hit.y,"#dbeafe");\n'
    '          spawnShockwave(hit.x,hit.y,"#2563eb");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp779d>0.88){sfx("legendary");unlock("liskeardite_orb9e_peak");}else unlock("liskeardite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="levyne_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="levyne_fox9e";color="#e11d48";glow="#ffe4e6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="libethenite_orb9e"')
A8_NEW = (
    '      type="lindgrenite_fox9e";color="#059669";glow="#d1fae5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="liskeardite_orb9e";color="#2563eb";glow="#dbeafe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="levyne_fox9e";color="#e11d48";glow="#ffe4e6";\n'
    '    } else if('+COND100F+'){\n'
    '      type="libethenite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="levyne_fox9e"?BASE_R*2.23:type==="libethenite_orb9e"?BASE_R*2.22:'
A9_NEW = f'type==="lindgrenite_fox9e"?{FOX_R}:type==="liskeardite_orb9e"?{ORB_R}:type==="levyne_fox9e"?BASE_R*2.23:type==="libethenite_orb9e"?BASE_R*2.22:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'CAPE_GLOW44:"🌊✨",BLUFF_GLOW44:"🪨✨",SHORE_GLOW44:"🏖️✨"'
A10_NEW = 'CRAG_GLOW44:"🪨✨",HELM_GLOW44:"⚓✨",CAPE_GLOW44:"🌊✨",BLUFF_GLOW44:"🪨✨",SHORE_GLOW44:"🏖️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 779 done! +{len(src)-orig_len} bytes")
