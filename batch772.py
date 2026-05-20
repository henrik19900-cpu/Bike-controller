#!/usr/bin/env python3
"""Batch 772: STREAM_GLOW44+FALLS_GLOW44 + IxioliteFox9e+JacobsiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4337"
SW = "2338"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.17"
ORB_R = f"{BASE_R}*2.16"
FOXSC = 528
ORBSC = 523
PW1SC = 2552
PW2SC = 2554

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"hypersthene_fox9e_tap", label:"Hypersthene Fox Tap"'
A1_NEW = (
    '  { id:"ixiolite_fox9e_tap", label:"Ixiolite Fox Tap", desc:"Tap Ixiolite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"ixiolite_fox9e_peak", label:"Ixiolite Fox Peak", desc:"Tap Ixiolite Fox at peak", icon:"🌊", xp:88 },\n'
    '  { id:"jacobsite_orb9e_tap", label:"Jacobsite Orb Tap", desc:"Tap Jacobsite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"jacobsite_orb9e_peak", label:"Jacobsite Orb Peak", desc:"Tap Jacobsite Orb at peak", icon:"⚫", xp:88 },\n'
    '  { id:"stream_glow44_use", label:"Stream Glow Use", desc:"Activate Stream Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"stream_glow44_max", label:"Stream Glow Max", desc:"Activate Stream Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"falls_glow44_use", label:"Falls Glow Use", desc:"Activate Falls Glow power-up", icon:"💦", xp:50 },\n'
    '  { id:"falls_glow44_max", label:"Falls Glow Max", desc:"Activate Falls Glow at max streak", icon:"💦", xp:75 },\n'
    '  { id:"hypersthene_fox9e_tap", label:"Hypersthene Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"RAVINE_GLOW44","BROOK_GLOW44","CLIFF_GLOW44"'
A2_NEW = '"STREAM_GLOW44","FALLS_GLOW44","RAVINE_GLOW44","BROOK_GLOW44","CLIFF_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="RAVINE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="STREAM_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} STREAM GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("stream_glow44_use");if(gs.streak>=20)unlock("stream_glow44_max");\n'
    '      } else if(ptype==="FALLS_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} FALLS GLOW",cx,cy,"#bae6fd");\n'
    '        spawnShockwave(cx,cy,"#0c4a6e");sfx("powerUp");\n'
    '        unlock("falls_glow44_use");if(gs.streak>=20)unlock("falls_glow44_max");\n'
    '      } else if(ptype==="RAVINE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// RAVINE_GLOW44 — +2548 ravine glow bonus'
A4_NEW = (
    f'// STREAM_GLOW44 — +{PW1SC} stream glow bonus\n'
    f'        // FALLS_GLOW44 — +{PW2SC} falls glow bonus\n'
    '        // RAVINE_GLOW44 — +2548 ravine glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHyperstheneFox9e('
A5_NEW = (
    f'function drawIxioliteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bae6fd");g.addColorStop(0.45+sp*0.35,"#1e3a5f");g.addColorStop(1,"#082f49");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(186,230,253,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#082f49":"#bae6fd";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌊":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawJacobsiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f3f4f6");g.addColorStop(0.35+tp*0.35,"#374151");g.addColorStop(1,"#111827");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(243,244,246,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(55,65,81,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#374151":"#f3f4f6";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"⚫":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawHyperstheneFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="hypersthene_fox9e"){'
A6_NEW = (
    '  else if(t.type==="ixiolite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp772a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawIxioliteFox9e(ctx,t.radius,ts,sp772a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="jacobsite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp772b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawJacobsiteOrb9e(ctx,t.radius,ts,tp772b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hypersthene_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="hypersthene_fox9e"){'
A7_NEW = (
    'if(hit.type==="ixiolite_fox9e"){\n'
    f'          const sp772c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts772a=Math.round({FOXSC}*(1+sp772c));\n'
    '          gs.score+=pts772a;gs.streak++;addPopup("+"+pts772a+(sp772c>0.88?" 🌊 PEAK!":""),hit.x,hit.y,"#bae6fd");\n'
    '          spawnShockwave(hit.x,hit.y,"#1e3a5f");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp772c>0.88){sfx("legendary");unlock("ixiolite_fox9e_peak");}else unlock("ixiolite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="jacobsite_orb9e"){\n'
    f'          const tp772d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts772b=Math.round({ORBSC}*(1+tp772d));\n'
    '          gs.score+=pts772b;gs.streak++;addPopup("+"+pts772b+(tp772d>0.88?" ⚫ PEAK!":""),hit.x,hit.y,"#f3f4f6");\n'
    '          spawnShockwave(hit.x,hit.y,"#374151");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp772d>0.88){sfx("legendary");unlock("jacobsite_orb9e_peak");}else unlock("jacobsite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hypersthene_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="hypersthene_fox9e";color="#5b21b6";glow="#ddd6fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="hisingerite_orb9e"')
A8_NEW = (
    '      type="ixiolite_fox9e";color="#1e3a5f";glow="#bae6fd";\n'
    '    } else if('+COND100F+'){\n'
    '      type="jacobsite_orb9e";color="#374151";glow="#f3f4f6";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hypersthene_fox9e";color="#5b21b6";glow="#ddd6fe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hisingerite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="hypersthene_fox9e"?BASE_R*2.16:type==="hisingerite_orb9e"?BASE_R*2.15:'
A9_NEW = f'type==="ixiolite_fox9e"?{FOX_R}:type==="jacobsite_orb9e"?{ORB_R}:type==="hypersthene_fox9e"?BASE_R*2.16:type==="hisingerite_orb9e"?BASE_R*2.15:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'RAVINE_GLOW44:"🏔️✨",BROOK_GLOW44:"💧✨",CLIFF_GLOW44:"🪨✨"'
A10_NEW = 'STREAM_GLOW44:"🌊✨",FALLS_GLOW44:"💦✨",RAVINE_GLOW44:"🏔️✨",BROOK_GLOW44:"💧✨",CLIFF_GLOW44:"🪨✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 772 done! +{len(src)-orig_len} bytes")
