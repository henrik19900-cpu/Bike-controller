#!/usr/bin/env python3
"""Batch 773: SPRING_GLOW44+POND_GLOW44 + JarositeFox9e+JenniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4341"
SW = "2340"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.18"
ORB_R = f"{BASE_R}*2.17"
FOXSC = 530
ORBSC = 525
PW1SC = 2556
PW2SC = 2558

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"ixiolite_fox9e_tap", label:"Ixiolite Fox Tap"'
A1_NEW = (
    '  { id:"jarosite_fox9e_tap", label:"Jarosite Fox Tap", desc:"Tap Jarosite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"jarosite_fox9e_peak", label:"Jarosite Fox Peak", desc:"Tap Jarosite Fox at peak", icon:"🌻", xp:88 },\n'
    '  { id:"jennite_orb9e_tap", label:"Jennite Orb Tap", desc:"Tap Jennite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"jennite_orb9e_peak", label:"Jennite Orb Peak", desc:"Tap Jennite Orb at peak", icon:"🔵", xp:88 },\n'
    '  { id:"spring_glow44_use", label:"Spring Glow Use", desc:"Activate Spring Glow power-up", icon:"🌱", xp:50 },\n'
    '  { id:"spring_glow44_max", label:"Spring Glow Max", desc:"Activate Spring Glow at max streak", icon:"🌱", xp:75 },\n'
    '  { id:"pond_glow44_use", label:"Pond Glow Use", desc:"Activate Pond Glow power-up", icon:"🐸", xp:50 },\n'
    '  { id:"pond_glow44_max", label:"Pond Glow Max", desc:"Activate Pond Glow at max streak", icon:"🐸", xp:75 },\n'
    '  { id:"ixiolite_fox9e_tap", label:"Ixiolite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"STREAM_GLOW44","FALLS_GLOW44","RAVINE_GLOW44"'
A2_NEW = '"SPRING_GLOW44","POND_GLOW44","STREAM_GLOW44","FALLS_GLOW44","RAVINE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="STREAM_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="SPRING_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} SPRING GLOW",cx,cy,"#bbf7d0");\n'
    '        spawnShockwave(cx,cy,"#15803d");sfx("powerUp");\n'
    '        unlock("spring_glow44_use");if(gs.streak>=20)unlock("spring_glow44_max");\n'
    '      } else if(ptype==="POND_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} POND GLOW",cx,cy,"#6ee7b7");\n'
    '        spawnShockwave(cx,cy,"#065f46");sfx("powerUp");\n'
    '        unlock("pond_glow44_use");if(gs.streak>=20)unlock("pond_glow44_max");\n'
    '      } else if(ptype==="STREAM_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// STREAM_GLOW44 — +2552 stream glow bonus'
A4_NEW = (
    f'// SPRING_GLOW44 — +{PW1SC} spring glow bonus\n'
    f'        // POND_GLOW44 — +{PW2SC} pond glow bonus\n'
    '        // STREAM_GLOW44 — +2552 stream glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawIxioliteFox9e('
A5_NEW = (
    f'function drawJarositeFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fde68a");g.addColorStop(0.45+sp*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(253,230,138,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#451a03":"#fde68a";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌻":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawJenniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bfdbfe");g.addColorStop(0.35+tp*0.35,"#1d4ed8");g.addColorStop(1,"#1e3a8a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(191,219,254,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(29,78,216,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#1d4ed8":"#bfdbfe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔵":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawIxioliteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="ixiolite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="jarosite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp773a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawJarositeFox9e(ctx,t.radius,ts,sp773a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="jennite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp773b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawJenniteOrb9e(ctx,t.radius,ts,tp773b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="ixiolite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="ixiolite_fox9e"){'
A7_NEW = (
    'if(hit.type==="jarosite_fox9e"){\n'
    f'          const sp773c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts773a=Math.round({FOXSC}*(1+sp773c));\n'
    '          gs.score+=pts773a;gs.streak++;addPopup("+"+pts773a+(sp773c>0.88?" 🌻 PEAK!":""),hit.x,hit.y,"#fde68a");\n'
    '          spawnShockwave(hit.x,hit.y,"#b45309");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp773c>0.88){sfx("legendary");unlock("jarosite_fox9e_peak");}else unlock("jarosite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="jennite_orb9e"){\n'
    f'          const tp773d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts773b=Math.round({ORBSC}*(1+tp773d));\n'
    '          gs.score+=pts773b;gs.streak++;addPopup("+"+pts773b+(tp773d>0.88?" 🔵 PEAK!":""),hit.x,hit.y,"#bfdbfe");\n'
    '          spawnShockwave(hit.x,hit.y,"#1d4ed8");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp773d>0.88){sfx("legendary");unlock("jennite_orb9e_peak");}else unlock("jennite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="ixiolite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="ixiolite_fox9e";color="#1e3a5f";glow="#bae6fd";\n'
          '    } else if('+COND100F+'){\n'
          '      type="jacobsite_orb9e"')
A8_NEW = (
    '      type="jarosite_fox9e";color="#b45309";glow="#fde68a";\n'
    '    } else if('+COND100F+'){\n'
    '      type="jennite_orb9e";color="#1d4ed8";glow="#bfdbfe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ixiolite_fox9e";color="#1e3a5f";glow="#bae6fd";\n'
    '    } else if('+COND100F+'){\n'
    '      type="jacobsite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="ixiolite_fox9e"?BASE_R*2.17:type==="jacobsite_orb9e"?BASE_R*2.16:'
A9_NEW = f'type==="jarosite_fox9e"?{FOX_R}:type==="jennite_orb9e"?{ORB_R}:type==="ixiolite_fox9e"?BASE_R*2.17:type==="jacobsite_orb9e"?BASE_R*2.16:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'STREAM_GLOW44:"🌊✨",FALLS_GLOW44:"💦✨",RAVINE_GLOW44:"🏔️✨"'
A10_NEW = 'SPRING_GLOW44:"🌱✨",POND_GLOW44:"🐸✨",STREAM_GLOW44:"🌊✨",FALLS_GLOW44:"💦✨",RAVINE_GLOW44:"🏔️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 773 done! +{len(src)-orig_len} bytes")
