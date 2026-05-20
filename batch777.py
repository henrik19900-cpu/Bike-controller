#!/usr/bin/env python3
"""Batch 777: SHORE_GLOW44+INLET_GLOW44 + LaumontiteFox9e+LeoniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4357"
SW = "2348"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.22"
ORB_R = f"{BASE_R}*2.21"
FOXSC = 538
ORBSC = 533
PW1SC = 2572
PW2SC = 2574

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"krausite_fox9e_tap", label:"Krausite Fox Tap"'
A1_NEW = (
    '  { id:"laumontite_fox9e_tap", label:"Laumontite Fox Tap", desc:"Tap Laumontite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"laumontite_fox9e_peak", label:"Laumontite Fox Peak", desc:"Tap Laumontite Fox at peak", icon:"🌸", xp:88 },\n'
    '  { id:"leonite_orb9e_tap", label:"Leonite Orb Tap", desc:"Tap Leonite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"leonite_orb9e_peak", label:"Leonite Orb Peak", desc:"Tap Leonite Orb at peak", icon:"🌙", xp:88 },\n'
    '  { id:"shore_glow44_use", label:"Shore Glow Use", desc:"Activate Shore Glow power-up", icon:"🏖️", xp:50 },\n'
    '  { id:"shore_glow44_max", label:"Shore Glow Max", desc:"Activate Shore Glow at max streak", icon:"🏖️", xp:75 },\n'
    '  { id:"inlet_glow44_use", label:"Inlet Glow Use", desc:"Activate Inlet Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"inlet_glow44_max", label:"Inlet Glow Max", desc:"Activate Inlet Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"krausite_fox9e_tap", label:"Krausite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"HARBOR_GLOW44","COVE_GLOW44","OCEAN_GLOW44"'
A2_NEW = '"SHORE_GLOW44","INLET_GLOW44","HARBOR_GLOW44","COVE_GLOW44","OCEAN_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="HARBOR_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="SHORE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} SHORE GLOW",cx,cy,"#fde68a");\n'
    '        spawnShockwave(cx,cy,"#d97706");sfx("powerUp");\n'
    '        unlock("shore_glow44_use");if(gs.streak>=20)unlock("shore_glow44_max");\n'
    '      } else if(ptype==="INLET_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} INLET GLOW",cx,cy,"#a5f3fc");\n'
    '        spawnShockwave(cx,cy,"#0891b2");sfx("powerUp");\n'
    '        unlock("inlet_glow44_use");if(gs.streak>=20)unlock("inlet_glow44_max");\n'
    '      } else if(ptype==="HARBOR_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// HARBOR_GLOW44 — +2568 harbor glow bonus'
A4_NEW = (
    f'// SHORE_GLOW44 — +{PW1SC} shore glow bonus\n'
    f'        // INLET_GLOW44 — +{PW2SC} inlet glow bonus\n'
    '        // HARBOR_GLOW44 — +2568 harbor glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawKrausiteFox9e('
A5_NEW = (
    f'function drawLaumontiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fce7f3");g.addColorStop(0.45+sp*0.35,"#db2777");g.addColorStop(1,"#831843");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(252,231,243,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#831843":"#fce7f3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌸":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawLeoniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f5f3ff");g.addColorStop(0.35+tp*0.35,"#6d28d9");g.addColorStop(1,"#2e1065");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(245,243,255,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(109,40,217,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#6d28d9":"#f5f3ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌙":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawKrausiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="krausite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="laumontite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp777a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLaumontiteFox9e(ctx,t.radius,ts,sp777a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="leonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp777b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLeoniteOrb9e(ctx,t.radius,ts,tp777b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="krausite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="krausite_fox9e"){'
A7_NEW = (
    'if(hit.type==="laumontite_fox9e"){\n'
    f'          const sp777c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts777a=Math.round({FOXSC}*(1+sp777c));\n'
    '          gs.score+=pts777a;gs.streak++;addPopup("+"+pts777a+(sp777c>0.88?" 🌸 PEAK!":""),hit.x,hit.y,"#fce7f3");\n'
    '          spawnShockwave(hit.x,hit.y,"#db2777");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp777c>0.88){sfx("legendary");unlock("laumontite_fox9e_peak");}else unlock("laumontite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="leonite_orb9e"){\n'
    f'          const tp777d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts777b=Math.round({ORBSC}*(1+tp777d));\n'
    '          gs.score+=pts777b;gs.streak++;addPopup("+"+pts777b+(tp777d>0.88?" 🌙 PEAK!":""),hit.x,hit.y,"#f5f3ff");\n'
    '          spawnShockwave(hit.x,hit.y,"#6d28d9");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp777d>0.88){sfx("legendary");unlock("leonite_orb9e_peak");}else unlock("leonite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="krausite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="krausite_fox9e";color="#15803d";glow="#bbf7d0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="lanthanite_orb9e"')
A8_NEW = (
    '      type="laumontite_fox9e";color="#db2777";glow="#fce7f3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="leonite_orb9e";color="#6d28d9";glow="#f5f3ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="krausite_fox9e";color="#15803d";glow="#bbf7d0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="lanthanite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="krausite_fox9e"?BASE_R*2.21:type==="lanthanite_orb9e"?BASE_R*2.20:'
A9_NEW = f'type==="laumontite_fox9e"?{FOX_R}:type==="leonite_orb9e"?{ORB_R}:type==="krausite_fox9e"?BASE_R*2.21:type==="lanthanite_orb9e"?BASE_R*2.20:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'HARBOR_GLOW44:"⚓✨",COVE_GLOW44:"🌊✨",OCEAN_GLOW44:"🌊✨"'
A10_NEW = 'SHORE_GLOW44:"🏖️✨",INLET_GLOW44:"🌊✨",HARBOR_GLOW44:"⚓✨",COVE_GLOW44:"🌊✨",OCEAN_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 777 done! +{len(src)-orig_len} bytes")
