#!/usr/bin/env python3
"""Batch 789: BANK_GLOW44+BIGHT_GLOW44 + NatrophiliteFox9e+NaujakasiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4405"
SW = "2372"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.34"
ORB_R = f"{BASE_R}*2.33"
FOXSC = 562
ORBSC = 557
PW1SC = 2620
PW2SC = 2622

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"nagyagite_fox9e_tap", label:"Nagyagite Fox Tap"'
A1_NEW = (
    '  { id:"natrophilite_fox9e_tap", label:"Natrophilite Fox Tap", desc:"Tap Natrophilite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"natrophilite_fox9e_peak", label:"Natrophilite Fox Peak", desc:"Tap Natrophilite Fox at peak", icon:"🌀", xp:88 },\n'
    '  { id:"naujakasite_orb9e_tap", label:"Naujakasite Orb Tap", desc:"Tap Naujakasite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"naujakasite_orb9e_peak", label:"Naujakasite Orb Peak", desc:"Tap Naujakasite Orb at peak", icon:"💫", xp:88 },\n'
    '  { id:"bank_glow44_use", label:"Bank Glow Use", desc:"Activate Bank Glow power-up", icon:"💰", xp:50 },\n'
    '  { id:"bank_glow44_max", label:"Bank Glow Max", desc:"Activate Bank Glow at max streak", icon:"💰", xp:75 },\n'
    '  { id:"bight_glow44_use", label:"Bight Glow Use", desc:"Activate Bight Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"bight_glow44_max", label:"Bight Glow Max", desc:"Activate Bight Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"nagyagite_fox9e_tap", label:"Nagyagite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"LEDGE_GLOW44","SKERRY_GLOW44","ISLE_GLOW44"'
A2_NEW = '"BANK_GLOW44","BIGHT_GLOW44","LEDGE_GLOW44","SKERRY_GLOW44","ISLE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="LEDGE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="BANK_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} BANK GLOW",cx,cy,"#fef08a");\n'
    '        spawnShockwave(cx,cy,"#ca8a04");sfx("powerUp");\n'
    '        unlock("bank_glow44_use");if(gs.streak>=20)unlock("bank_glow44_max");\n'
    '      } else if(ptype==="BIGHT_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} BIGHT GLOW",cx,cy,"#67e8f9");\n'
    '        spawnShockwave(cx,cy,"#0e7490");sfx("powerUp");\n'
    '        unlock("bight_glow44_use");if(gs.streak>=20)unlock("bight_glow44_max");\n'
    '      } else if(ptype==="LEDGE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// LEDGE_GLOW44 — +2616 ledge glow bonus'
A4_NEW = (
    f'// BANK_GLOW44 — +{PW1SC} bank glow bonus\n'
    f'        // BIGHT_GLOW44 — +{PW2SC} bight glow bonus\n'
    '        // LEDGE_GLOW44 — +2616 ledge glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawNagyagiteFox9e('
A5_NEW = (
    f'function drawNatrophiliteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#cffafe");g.addColorStop(0.45+sp*0.35,"#06b6d4");g.addColorStop(1,"#083344");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(207,250,254,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#083344":"#cffafe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌀":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawNaujakasiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.35+tp*0.35,"#c026d3");g.addColorStop(1,"#4a044e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(253,244,255,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(192,38,211,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#c026d3":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💫":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawNagyagiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="nagyagite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="natrophilite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp789a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawNatrophiliteFox9e(ctx,t.radius,ts,sp789a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="naujakasite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp789b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawNaujakasiteOrb9e(ctx,t.radius,ts,tp789b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="nagyagite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="nagyagite_fox9e"){'
A7_NEW = (
    'if(hit.type==="natrophilite_fox9e"){\n'
    f'          const sp789c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts789a=Math.round({FOXSC}*(1+sp789c));\n'
    '          gs.score+=pts789a;gs.streak++;addPopup("+"+pts789a+(sp789c>0.88?" 🌀 PEAK!":""),hit.x,hit.y,"#cffafe");\n'
    '          spawnShockwave(hit.x,hit.y,"#06b6d4");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp789c>0.88){sfx("legendary");unlock("natrophilite_fox9e_peak");}else unlock("natrophilite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="naujakasite_orb9e"){\n'
    f'          const tp789d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts789b=Math.round({ORBSC}*(1+tp789d));\n'
    '          gs.score+=pts789b;gs.streak++;addPopup("+"+pts789b+(tp789d>0.88?" 💫 PEAK!":""),hit.x,hit.y,"#fdf4ff");\n'
    '          spawnShockwave(hit.x,hit.y,"#c026d3");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp789d>0.88){sfx("legendary");unlock("naujakasite_orb9e_peak");}else unlock("naujakasite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="nagyagite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="nagyagite_fox9e";color="#4338ca";glow="#e0e7ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="nantokite_orb9e"')
A8_NEW = (
    '      type="natrophilite_fox9e";color="#06b6d4";glow="#cffafe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="naujakasite_orb9e";color="#c026d3";glow="#fdf4ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="nagyagite_fox9e";color="#4338ca";glow="#e0e7ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="nantokite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="nagyagite_fox9e"?BASE_R*2.33:type==="nantokite_orb9e"?BASE_R*2.32:'
A9_NEW = f'type==="natrophilite_fox9e"?{FOX_R}:type==="naujakasite_orb9e"?{ORB_R}:type==="nagyagite_fox9e"?BASE_R*2.33:type==="nantokite_orb9e"?BASE_R*2.32:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'LEDGE_GLOW44:"🪨✨",SKERRY_GLOW44:"🌊✨",ISLE_GLOW44:"🏝️✨"'
A10_NEW = 'BANK_GLOW44:"💰✨",BIGHT_GLOW44:"🌊✨",LEDGE_GLOW44:"🪨✨",SKERRY_GLOW44:"🌊✨",ISLE_GLOW44:"🏝️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 789 done! +{len(src)-orig_len} bytes")
