#!/usr/bin/env python3
"""Batch 783: LOCH_GLOW44+FORD_GLOW44 + MatilditeFox9e+MawsoniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4381"
SW = "2360"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.28"
ORB_R = f"{BASE_R}*2.27"
FOXSC = 550
ORBSC = 545
PW1SC = 2596
PW2SC = 2598

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"margarite_fox9e_tap", label:"Margarite Fox Tap"'
A1_NEW = (
    '  { id:"matildite_fox9e_tap", label:"Matildite Fox Tap", desc:"Tap Matildite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"matildite_fox9e_peak", label:"Matildite Fox Peak", desc:"Tap Matildite Fox at peak", icon:"💎", xp:88 },\n'
    '  { id:"mawsonite_orb9e_tap", label:"Mawsonite Orb Tap", desc:"Tap Mawsonite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"mawsonite_orb9e_peak", label:"Mawsonite Orb Peak", desc:"Tap Mawsonite Orb at peak", icon:"🟨", xp:88 },\n'
    '  { id:"loch_glow44_use", label:"Loch Glow Use", desc:"Activate Loch Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"loch_glow44_max", label:"Loch Glow Max", desc:"Activate Loch Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"ford_glow44_use", label:"Ford Glow Use", desc:"Activate Ford Glow power-up", icon:"🌿", xp:50 },\n'
    '  { id:"ford_glow44_max", label:"Ford Glow Max", desc:"Activate Ford Glow at max streak", icon:"🌿", xp:75 },\n'
    '  { id:"margarite_fox9e_tap", label:"Margarite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"WHARF_GLOW44","QUAY_GLOW44","DOCK_GLOW44"'
A2_NEW = '"LOCH_GLOW44","FORD_GLOW44","WHARF_GLOW44","QUAY_GLOW44","DOCK_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="WHARF_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="LOCH_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} LOCH GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0284c7");sfx("powerUp");\n'
    '        unlock("loch_glow44_use");if(gs.streak>=20)unlock("loch_glow44_max");\n'
    '      } else if(ptype==="FORD_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} FORD GLOW",cx,cy,"#86efac");\n'
    '        spawnShockwave(cx,cy,"#15803d");sfx("powerUp");\n'
    '        unlock("ford_glow44_use");if(gs.streak>=20)unlock("ford_glow44_max");\n'
    '      } else if(ptype==="WHARF_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// WHARF_GLOW44 — +2592 wharf glow bonus'
A4_NEW = (
    f'// LOCH_GLOW44 — +{PW1SC} loch glow bonus\n'
    f'        // FORD_GLOW44 — +{PW2SC} ford glow bonus\n'
    '        // WHARF_GLOW44 — +2592 wharf glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMargariteFox9e('
A5_NEW = (
    f'function drawMatilditeFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.45+sp*0.35,"#0284c7");g.addColorStop(1,"#0c4a6e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(224,242,254,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0c4a6e":"#e0f2fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"💎":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMawsoniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+tp*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,252,232,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(202,138,4,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#ca8a04":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟨":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMargariteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="margarite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="matildite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp783a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMatilditeFox9e(ctx,t.radius,ts,sp783a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="mawsonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp783b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMawsoniteOrb9e(ctx,t.radius,ts,tp783b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="margarite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="margarite_fox9e"){'
A7_NEW = (
    'if(hit.type==="matildite_fox9e"){\n'
    f'          const sp783c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts783a=Math.round({FOXSC}*(1+sp783c));\n'
    '          gs.score+=pts783a;gs.streak++;addPopup("+"+pts783a+(sp783c>0.88?" 💎 PEAK!":""),hit.x,hit.y,"#e0f2fe");\n'
    '          spawnShockwave(hit.x,hit.y,"#0284c7");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp783c>0.88){sfx("legendary");unlock("matildite_fox9e_peak");}else unlock("matildite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="mawsonite_orb9e"){\n'
    f'          const tp783d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts783b=Math.round({ORBSC}*(1+tp783d));\n'
    '          gs.score+=pts783b;gs.streak++;addPopup("+"+pts783b+(tp783d>0.88?" 🟨 PEAK!":""),hit.x,hit.y,"#fefce8");\n'
    '          spawnShockwave(hit.x,hit.y,"#ca8a04");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp783d>0.88){sfx("legendary");unlock("mawsonite_orb9e_peak");}else unlock("mawsonite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="margarite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="margarite_fox9e";color="#be185d";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="masuyite_orb9e"')
A8_NEW = (
    '      type="matildite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mawsonite_orb9e";color="#ca8a04";glow="#fefce8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="margarite_fox9e";color="#be185d";glow="#fdf2f8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="masuyite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="margarite_fox9e"?BASE_R*2.27:type==="masuyite_orb9e"?BASE_R*2.26:'
A9_NEW = f'type==="matildite_fox9e"?{FOX_R}:type==="mawsonite_orb9e"?{ORB_R}:type==="margarite_fox9e"?BASE_R*2.27:type==="masuyite_orb9e"?BASE_R*2.26:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'WHARF_GLOW44:"⚓✨",QUAY_GLOW44:"🌊✨",DOCK_GLOW44:"⚓✨"'
A10_NEW = 'LOCH_GLOW44:"🌊✨",FORD_GLOW44:"🌿✨",WHARF_GLOW44:"⚓✨",QUAY_GLOW44:"🌊✨",DOCK_GLOW44:"⚓✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 783 done! +{len(src)-orig_len} bytes")
