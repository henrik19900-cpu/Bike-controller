#!/usr/bin/env python3
"""Batch 788: LEDGE_GLOW44+SKERRY_GLOW44 + NagyagiteFox9e+NantokiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4401"
SW = "2370"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.33"
ORB_R = f"{BASE_R}*2.32"
FOXSC = 560
ORBSC = 555
PW1SC = 2616
PW2SC = 2618

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"murdochite_fox9e_tap", label:"Murdochite Fox Tap"'
A1_NEW = (
    '  { id:"nagyagite_fox9e_tap", label:"Nagyagite Fox Tap", desc:"Tap Nagyagite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"nagyagite_fox9e_peak", label:"Nagyagite Fox Peak", desc:"Tap Nagyagite Fox at peak", icon:"🌙", xp:88 },\n'
    '  { id:"nantokite_orb9e_tap", label:"Nantokite Orb Tap", desc:"Tap Nantokite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"nantokite_orb9e_peak", label:"Nantokite Orb Peak", desc:"Tap Nantokite Orb at peak", icon:"🤍", xp:88 },\n'
    '  { id:"ledge_glow44_use", label:"Ledge Glow Use", desc:"Activate Ledge Glow power-up", icon:"🪨", xp:50 },\n'
    '  { id:"ledge_glow44_max", label:"Ledge Glow Max", desc:"Activate Ledge Glow at max streak", icon:"🪨", xp:75 },\n'
    '  { id:"skerry_glow44_use", label:"Skerry Glow Use", desc:"Activate Skerry Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"skerry_glow44_max", label:"Skerry Glow Max", desc:"Activate Skerry Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"murdochite_fox9e_tap", label:"Murdochite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"ISLE_GLOW44","SHOAL_GLOW44","GULF_GLOW44"'
A2_NEW = '"LEDGE_GLOW44","SKERRY_GLOW44","ISLE_GLOW44","SHOAL_GLOW44","GULF_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="ISLE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="LEDGE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} LEDGE GLOW",cx,cy,"#e7e5e4");\n'
    '        spawnShockwave(cx,cy,"#78716c");sfx("powerUp");\n'
    '        unlock("ledge_glow44_use");if(gs.streak>=20)unlock("ledge_glow44_max");\n'
    '      } else if(ptype==="SKERRY_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} SKERRY GLOW",cx,cy,"#93c5fd");\n'
    '        spawnShockwave(cx,cy,"#1d4ed8");sfx("powerUp");\n'
    '        unlock("skerry_glow44_use");if(gs.streak>=20)unlock("skerry_glow44_max");\n'
    '      } else if(ptype==="ISLE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// ISLE_GLOW44 — +2612 isle glow bonus'
A4_NEW = (
    f'// LEDGE_GLOW44 — +{PW1SC} ledge glow bonus\n'
    f'        // SKERRY_GLOW44 — +{PW2SC} skerry glow bonus\n'
    '        // ISLE_GLOW44 — +2612 isle glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMurdochiteFox9e('
A5_NEW = (
    f'function drawNagyagiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e0e7ff");g.addColorStop(0.45+sp*0.35,"#4338ca");g.addColorStop(1,"#1e1b4b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(224,231,255,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#1e1b4b":"#e0e7ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌙":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawNantokiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.35+tp*0.35,"#94a3b8");g.addColorStop(1,"#0f172a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(241,245,249,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#94a3b8":"#f1f5f9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🤍":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMurdochiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="murdochite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="nagyagite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp788a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawNagyagiteFox9e(ctx,t.radius,ts,sp788a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="nantokite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp788b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawNantokiteOrb9e(ctx,t.radius,ts,tp788b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="murdochite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="murdochite_fox9e"){'
A7_NEW = (
    'if(hit.type==="nagyagite_fox9e"){\n'
    f'          const sp788c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts788a=Math.round({FOXSC}*(1+sp788c));\n'
    '          gs.score+=pts788a;gs.streak++;addPopup("+"+pts788a+(sp788c>0.88?" 🌙 PEAK!":""),hit.x,hit.y,"#e0e7ff");\n'
    '          spawnShockwave(hit.x,hit.y,"#4338ca");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp788c>0.88){sfx("legendary");unlock("nagyagite_fox9e_peak");}else unlock("nagyagite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="nantokite_orb9e"){\n'
    f'          const tp788d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts788b=Math.round({ORBSC}*(1+tp788d));\n'
    '          gs.score+=pts788b;gs.streak++;addPopup("+"+pts788b+(tp788d>0.88?" 🤍 PEAK!":""),hit.x,hit.y,"#f1f5f9");\n'
    '          spawnShockwave(hit.x,hit.y,"#94a3b8");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp788d>0.88){sfx("legendary");unlock("nantokite_orb9e_peak");}else unlock("nantokite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="murdochite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="murdochite_fox9e";color="#047857";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="murmanite_orb9e"')
A8_NEW = (
    '      type="nagyagite_fox9e";color="#4338ca";glow="#e0e7ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="nantokite_orb9e";color="#94a3b8";glow="#f1f5f9";\n'
    '    } else if('+COND100F+'){\n'
    '      type="murdochite_fox9e";color="#047857";glow="#d1fae5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="murmanite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="murdochite_fox9e"?BASE_R*2.32:type==="murmanite_orb9e"?BASE_R*2.31:'
A9_NEW = f'type==="nagyagite_fox9e"?{FOX_R}:type==="nantokite_orb9e"?{ORB_R}:type==="murdochite_fox9e"?BASE_R*2.32:type==="murmanite_orb9e"?BASE_R*2.31:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'ISLE_GLOW44:"🏝️✨",SHOAL_GLOW44:"🐟✨",GULF_GLOW44:"🌊✨"'
A10_NEW = 'LEDGE_GLOW44:"🪨✨",SKERRY_GLOW44:"🌊✨",ISLE_GLOW44:"🏝️✨",SHOAL_GLOW44:"🐟✨",GULF_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 788 done! +{len(src)-orig_len} bytes")
