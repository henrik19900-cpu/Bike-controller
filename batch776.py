#!/usr/bin/env python3
"""Batch 776: HARBOR_GLOW44+COVE_GLOW44 + KrausiteFox9e+LanthaniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4353"
SW = "2346"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.21"
ORB_R = f"{BASE_R}*2.20"
FOXSC = 536
ORBSC = 531
PW1SC = 2568
PW2SC = 2570

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"koechlinite_fox9e_tap", label:"Koechlinite Fox Tap"'
A1_NEW = (
    '  { id:"krausite_fox9e_tap", label:"Krausite Fox Tap", desc:"Tap Krausite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"krausite_fox9e_peak", label:"Krausite Fox Peak", desc:"Tap Krausite Fox at peak", icon:"💚", xp:88 },\n'
    '  { id:"lanthanite_orb9e_tap", label:"Lanthanite Orb Tap", desc:"Tap Lanthanite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"lanthanite_orb9e_peak", label:"Lanthanite Orb Peak", desc:"Tap Lanthanite Orb at peak", icon:"🩵", xp:88 },\n'
    '  { id:"harbor_glow44_use", label:"Harbor Glow Use", desc:"Activate Harbor Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"harbor_glow44_max", label:"Harbor Glow Max", desc:"Activate Harbor Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"cove_glow44_use", label:"Cove Glow Use", desc:"Activate Cove Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"cove_glow44_max", label:"Cove Glow Max", desc:"Activate Cove Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"koechlinite_fox9e_tap", label:"Koechlinite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"OCEAN_GLOW44","BAY_GLOW44","LAKE_GLOW44"'
A2_NEW = '"HARBOR_GLOW44","COVE_GLOW44","OCEAN_GLOW44","BAY_GLOW44","LAKE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="OCEAN_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="HARBOR_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} HARBOR GLOW",cx,cy,"#93c5fd");\n'
    '        spawnShockwave(cx,cy,"#1e40af");sfx("powerUp");\n'
    '        unlock("harbor_glow44_use");if(gs.streak>=20)unlock("harbor_glow44_max");\n'
    '      } else if(ptype==="COVE_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} COVE GLOW",cx,cy,"#67e8f9");\n'
    '        spawnShockwave(cx,cy,"#0e7490");sfx("powerUp");\n'
    '        unlock("cove_glow44_use");if(gs.streak>=20)unlock("cove_glow44_max");\n'
    '      } else if(ptype==="OCEAN_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// OCEAN_GLOW44 — +2564 ocean glow bonus'
A4_NEW = (
    f'// HARBOR_GLOW44 — +{PW1SC} harbor glow bonus\n'
    f'        // COVE_GLOW44 — +{PW2SC} cove glow bonus\n'
    '        // OCEAN_GLOW44 — +2564 ocean glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawKoechliniteFox9e('
A5_NEW = (
    f'function drawKrausiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bbf7d0");g.addColorStop(0.45+sp*0.35,"#15803d");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(187,247,208,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#14532d":"#bbf7d0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"💚":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawLanthaniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#cffafe");g.addColorStop(0.35+tp*0.35,"#0891b2");g.addColorStop(1,"#164e63");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(207,250,254,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(8,145,178,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#0891b2":"#cffafe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🩵":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawKoechliniteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="koechlinite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="krausite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp776a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawKrausiteFox9e(ctx,t.radius,ts,sp776a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="lanthanite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp776b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLanthaniteOrb9e(ctx,t.radius,ts,tp776b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="koechlinite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="koechlinite_fox9e"){'
A7_NEW = (
    'if(hit.type==="krausite_fox9e"){\n'
    f'          const sp776c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts776a=Math.round({FOXSC}*(1+sp776c));\n'
    '          gs.score+=pts776a;gs.streak++;addPopup("+"+pts776a+(sp776c>0.88?" 💚 PEAK!":""),hit.x,hit.y,"#bbf7d0");\n'
    '          spawnShockwave(hit.x,hit.y,"#15803d");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp776c>0.88){sfx("legendary");unlock("krausite_fox9e_peak");}else unlock("krausite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="lanthanite_orb9e"){\n'
    f'          const tp776d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts776b=Math.round({ORBSC}*(1+tp776d));\n'
    '          gs.score+=pts776b;gs.streak++;addPopup("+"+pts776b+(tp776d>0.88?" 🩵 PEAK!":""),hit.x,hit.y,"#cffafe");\n'
    '          spawnShockwave(hit.x,hit.y,"#0891b2");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp776d>0.88){sfx("legendary");unlock("lanthanite_orb9e_peak");}else unlock("lanthanite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="koechlinite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="koechlinite_fox9e";color="#ea580c";glow="#fed7aa";\n'
          '    } else if('+COND100F+'){\n'
          '      type="kottigite_orb9e"')
A8_NEW = (
    '      type="krausite_fox9e";color="#15803d";glow="#bbf7d0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="lanthanite_orb9e";color="#0891b2";glow="#cffafe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="koechlinite_fox9e";color="#ea580c";glow="#fed7aa";\n'
    '    } else if('+COND100F+'){\n'
    '      type="kottigite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="koechlinite_fox9e"?BASE_R*2.20:type==="kottigite_orb9e"?BASE_R*2.19:'
A9_NEW = f'type==="krausite_fox9e"?{FOX_R}:type==="lanthanite_orb9e"?{ORB_R}:type==="koechlinite_fox9e"?BASE_R*2.20:type==="kottigite_orb9e"?BASE_R*2.19:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'OCEAN_GLOW44:"🌊✨",BAY_GLOW44:"⚓✨",LAKE_GLOW44:"🏔️✨"'
A10_NEW = 'HARBOR_GLOW44:"⚓✨",COVE_GLOW44:"🌊✨",OCEAN_GLOW44:"🌊✨",BAY_GLOW44:"⚓✨",LAKE_GLOW44:"🏔️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 776 done! +{len(src)-orig_len} bytes")
