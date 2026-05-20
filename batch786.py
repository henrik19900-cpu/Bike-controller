#!/usr/bin/env python3
"""Batch 786: GULF_GLOW44+FJORD_GLOW44 + MolybdeniteFox9e+MosandriteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4393"
SW = "2366"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.31"
ORB_R = f"{BASE_R}*2.30"
FOXSC = 556
ORBSC = 551
PW1SC = 2608
PW2SC = 2610

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"miargyrite_fox9e_tap", label:"Miargyrite Fox Tap"'
A1_NEW = (
    '  { id:"molybdenite_fox9e_tap", label:"Molybdenite Fox Tap", desc:"Tap Molybdenite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"molybdenite_fox9e_peak", label:"Molybdenite Fox Peak", desc:"Tap Molybdenite Fox at peak", icon:"⚫", xp:88 },\n'
    '  { id:"mosandrite_orb9e_tap", label:"Mosandrite Orb Tap", desc:"Tap Mosandrite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"mosandrite_orb9e_peak", label:"Mosandrite Orb Peak", desc:"Tap Mosandrite Orb at peak", icon:"🌟", xp:88 },\n'
    '  { id:"gulf_glow44_use", label:"Gulf Glow Use", desc:"Activate Gulf Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"gulf_glow44_max", label:"Gulf Glow Max", desc:"Activate Gulf Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"fjord_glow44_use", label:"Fjord Glow Use", desc:"Activate Fjord Glow power-up", icon:"🏔️", xp:50 },\n'
    '  { id:"fjord_glow44_max", label:"Fjord Glow Max", desc:"Activate Fjord Glow at max streak", icon:"🏔️", xp:75 },\n'
    '  { id:"miargyrite_fox9e_tap", label:"Miargyrite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"CHANNEL_GLOW44","STRAIT_GLOW44","FIRTH_GLOW44"'
A2_NEW = '"GULF_GLOW44","FJORD_GLOW44","CHANNEL_GLOW44","STRAIT_GLOW44","FIRTH_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="CHANNEL_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="GULF_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} GULF GLOW",cx,cy,"#38bdf8");\n'
    '        spawnShockwave(cx,cy,"#0c4a6e");sfx("powerUp");\n'
    '        unlock("gulf_glow44_use");if(gs.streak>=20)unlock("gulf_glow44_max");\n'
    '      } else if(ptype==="FJORD_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} FJORD GLOW",cx,cy,"#e2e8f0");\n'
    '        spawnShockwave(cx,cy,"#475569");sfx("powerUp");\n'
    '        unlock("fjord_glow44_use");if(gs.streak>=20)unlock("fjord_glow44_max");\n'
    '      } else if(ptype==="CHANNEL_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// CHANNEL_GLOW44 — +2604 channel glow bonus'
A4_NEW = (
    f'// GULF_GLOW44 — +{PW1SC} gulf glow bonus\n'
    f'        // FJORD_GLOW44 — +{PW2SC} fjord glow bonus\n'
    '        // CHANNEL_GLOW44 — +2604 channel glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMiargyriteFox9e('
A5_NEW = (
    f'function drawMolybdeniteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d4d4d8");g.addColorStop(0.45+sp*0.35,"#27272a");g.addColorStop(1,"#09090b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(212,212,216,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#09090b":"#d4d4d8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"⚫":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMosandriteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+tp*0.35,"#facc15");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,249,195,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(250,204,21,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#facc15":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌟":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMiargyriteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="miargyrite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="molybdenite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp786a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMolybdeniteFox9e(ctx,t.radius,ts,sp786a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="mosandrite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp786b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMosandriteOrb9e(ctx,t.radius,ts,tp786b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="miargyrite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="miargyrite_fox9e"){'
A7_NEW = (
    'if(hit.type==="molybdenite_fox9e"){\n'
    f'          const sp786c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts786a=Math.round({FOXSC}*(1+sp786c));\n'
    '          gs.score+=pts786a;gs.streak++;addPopup("+"+pts786a+(sp786c>0.88?" ⚫ PEAK!":""),hit.x,hit.y,"#d4d4d8");\n'
    '          spawnShockwave(hit.x,hit.y,"#27272a");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp786c>0.88){sfx("legendary");unlock("molybdenite_fox9e_peak");}else unlock("molybdenite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="mosandrite_orb9e"){\n'
    f'          const tp786d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts786b=Math.round({ORBSC}*(1+tp786d));\n'
    '          gs.score+=pts786b;gs.streak++;addPopup("+"+pts786b+(tp786d>0.88?" 🌟 PEAK!":""),hit.x,hit.y,"#fef9c3");\n'
    '          spawnShockwave(hit.x,hit.y,"#facc15");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp786d>0.88){sfx("legendary");unlock("mosandrite_orb9e_peak");}else unlock("mosandrite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="miargyrite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="miargyrite_fox9e";color="#d97706";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="mimetesite_orb9e"')
A8_NEW = (
    '      type="molybdenite_fox9e";color="#27272a";glow="#d4d4d8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mosandrite_orb9e";color="#facc15";glow="#fef9c3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="miargyrite_fox9e";color="#d97706";glow="#fef9c3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mimetesite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="miargyrite_fox9e"?BASE_R*2.30:type==="mimetesite_orb9e"?BASE_R*2.29:'
A9_NEW = f'type==="molybdenite_fox9e"?{FOX_R}:type==="mosandrite_orb9e"?{ORB_R}:type==="miargyrite_fox9e"?BASE_R*2.30:type==="mimetesite_orb9e"?BASE_R*2.29:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'CHANNEL_GLOW44:"🌊✨",STRAIT_GLOW44:"⚓✨",FIRTH_GLOW44:"🌊✨"'
A10_NEW = 'GULF_GLOW44:"🌊✨",FJORD_GLOW44:"🏔️✨",CHANNEL_GLOW44:"🌊✨",STRAIT_GLOW44:"⚓✨",FIRTH_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 786 done! +{len(src)-orig_len} bytes")
