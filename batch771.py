#!/usr/bin/env python3
"""Batch 771: RAVINE_GLOW44+BROOK_GLOW44 + HyperstheneFox9e+HisingeriteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4333"
SW = "2336"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.16"
ORB_R = f"{BASE_R}*2.15"
FOXSC = 526
ORBSC = 521
PW1SC = 2548
PW2SC = 2550

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"huebnerite_fox9e_tap", label:"Huebnerite Fox Tap"'
A1_NEW = (
    '  { id:"hypersthene_fox9e_tap", label:"Hypersthene Fox Tap", desc:"Tap Hypersthene Fox", icon:"🦊", xp:62 },\n'
    '  { id:"hypersthene_fox9e_peak", label:"Hypersthene Fox Peak", desc:"Tap Hypersthene Fox at peak", icon:"🌌", xp:88 },\n'
    '  { id:"hisingerite_orb9e_tap", label:"Hisingerite Orb Tap", desc:"Tap Hisingerite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"hisingerite_orb9e_peak", label:"Hisingerite Orb Peak", desc:"Tap Hisingerite Orb at peak", icon:"🟤", xp:88 },\n'
    '  { id:"ravine_glow44_use", label:"Ravine Glow Use", desc:"Activate Ravine Glow power-up", icon:"🏔️", xp:50 },\n'
    '  { id:"ravine_glow44_max", label:"Ravine Glow Max", desc:"Activate Ravine Glow at max streak", icon:"🏔️", xp:75 },\n'
    '  { id:"brook_glow44_use", label:"Brook Glow Use", desc:"Activate Brook Glow power-up", icon:"💧", xp:50 },\n'
    '  { id:"brook_glow44_max", label:"Brook Glow Max", desc:"Activate Brook Glow at max streak", icon:"💧", xp:75 },\n'
    '  { id:"huebnerite_fox9e_tap", label:"Huebnerite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"CLIFF_GLOW44","GORGE_GLOW44","PEAK_GLOW44"'
A2_NEW = '"RAVINE_GLOW44","BROOK_GLOW44","CLIFF_GLOW44","GORGE_GLOW44","PEAK_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="CLIFF_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="RAVINE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} RAVINE GLOW",cx,cy,"#c4b5fd");\n'
    '        spawnShockwave(cx,cy,"#5b21b6");sfx("powerUp");\n'
    '        unlock("ravine_glow44_use");if(gs.streak>=20)unlock("ravine_glow44_max");\n'
    '      } else if(ptype==="BROOK_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} BROOK GLOW",cx,cy,"#93c5fd");\n'
    '        spawnShockwave(cx,cy,"#1d4ed8");sfx("powerUp");\n'
    '        unlock("brook_glow44_use");if(gs.streak>=20)unlock("brook_glow44_max");\n'
    '      } else if(ptype==="CLIFF_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// CLIFF_GLOW44 — +2544 cliff glow bonus'
A4_NEW = (
    f'// RAVINE_GLOW44 — +{PW1SC} ravine glow bonus\n'
    f'        // BROOK_GLOW44 — +{PW2SC} brook glow bonus\n'
    '        // CLIFF_GLOW44 — +2544 cliff glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHuebneriteFox9e('
A5_NEW = (
    f'function drawHyperstheneFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ddd6fe");g.addColorStop(0.45+sp*0.35,"#5b21b6");g.addColorStop(1,"#2e1065");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(221,214,254,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#2e1065":"#ddd6fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌌":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawHisingeriteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d97706");g.addColorStop(0.35+tp*0.35,"#78350f");g.addColorStop(1,"#1c0a00");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(120,53,15,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#78350f":"#d97706";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟤":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawHuebneriteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="huebnerite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="hypersthene_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp771a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHyperstheneFox9e(ctx,t.radius,ts,sp771a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hisingerite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp771b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHisingeriteOrb9e(ctx,t.radius,ts,tp771b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="huebnerite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="huebnerite_fox9e"){'
A7_NEW = (
    'if(hit.type==="hypersthene_fox9e"){\n'
    f'          const sp771c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts771a=Math.round({FOXSC}*(1+sp771c));\n'
    '          gs.score+=pts771a;gs.streak++;addPopup("+"+pts771a+(sp771c>0.88?" 🌌 PEAK!":""),hit.x,hit.y,"#ddd6fe");\n'
    '          spawnShockwave(hit.x,hit.y,"#5b21b6");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp771c>0.88){sfx("legendary");unlock("hypersthene_fox9e_peak");}else unlock("hypersthene_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hisingerite_orb9e"){\n'
    f'          const tp771d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts771b=Math.round({ORBSC}*(1+tp771d));\n'
    '          gs.score+=pts771b;gs.streak++;addPopup("+"+pts771b+(tp771d>0.88?" 🟤 PEAK!":""),hit.x,hit.y,"#d97706");\n'
    '          spawnShockwave(hit.x,hit.y,"#78350f");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp771d>0.88){sfx("legendary");unlock("hisingerite_orb9e_peak");}else unlock("hisingerite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="huebnerite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="huebnerite_fox9e";color="#991b1b";glow="#fecaca";\n'
          '    } else if('+COND100F+'){\n'
          '      type="huntite_orb9e"')
A8_NEW = (
    '      type="hypersthene_fox9e";color="#5b21b6";glow="#ddd6fe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hisingerite_orb9e";color="#78350f";glow="#d97706";\n'
    '    } else if('+COND100F+'){\n'
    '      type="huebnerite_fox9e";color="#991b1b";glow="#fecaca";\n'
    '    } else if('+COND100F+'){\n'
    '      type="huntite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="huebnerite_fox9e"?BASE_R*2.15:type==="huntite_orb9e"?BASE_R*2.14:'
A9_NEW = f'type==="hypersthene_fox9e"?{FOX_R}:type==="hisingerite_orb9e"?{ORB_R}:type==="huebnerite_fox9e"?BASE_R*2.15:type==="huntite_orb9e"?BASE_R*2.14:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'CLIFF_GLOW44:"🪨✨",GORGE_GLOW44:"🌊✨",PEAK_GLOW44:"⛰️✨"'
A10_NEW = 'RAVINE_GLOW44:"🏔️✨",BROOK_GLOW44:"💧✨",CLIFF_GLOW44:"🪨✨",GORGE_GLOW44:"🌊✨",PEAK_GLOW44:"⛰️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 771 done! +{len(src)-orig_len} bytes")
