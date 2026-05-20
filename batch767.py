#!/usr/bin/env python3
"""Batch 767: RIDGE_GLOW44+STONE_GLOW44 + HastingsiteFox9e+HatchettiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4317"
SW = "2328"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.12"
ORB_R = f"{BASE_R}*2.11"
FOXSC = 518
ORBSC = 513
PW1SC = 2532
PW2SC = 2534

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"gyrolite_fox9e_tap", label:"Gyrolite Fox Tap"'
A1_NEW = (
    '  { id:"hastingsite_fox9e_tap", label:"Hastingsite Fox Tap", desc:"Tap Hastingsite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"hastingsite_fox9e_peak", label:"Hastingsite Fox Peak", desc:"Tap Hastingsite Fox at peak", icon:"🌿", xp:88 },\n'
    '  { id:"hatchettite_orb9e_tap", label:"Hatchettite Orb Tap", desc:"Tap Hatchettite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"hatchettite_orb9e_peak", label:"Hatchettite Orb Peak", desc:"Tap Hatchettite Orb at peak", icon:"🔥", xp:88 },\n'
    '  { id:"ridge_glow44_use", label:"Ridge Glow Use", desc:"Activate Ridge Glow power-up", icon:"⛰️", xp:50 },\n'
    '  { id:"ridge_glow44_max", label:"Ridge Glow Max", desc:"Activate Ridge Glow at max streak", icon:"⛰️", xp:75 },\n'
    '  { id:"stone_glow44_use", label:"Stone Glow Use", desc:"Activate Stone Glow power-up", icon:"🪨", xp:50 },\n'
    '  { id:"stone_glow44_max", label:"Stone Glow Max", desc:"Activate Stone Glow at max streak", icon:"🪨", xp:75 },\n'
    '  { id:"gyrolite_fox9e_tap", label:"Gyrolite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"DEEP_GLOW44","TRENCH_GLOW44","CORAL_GLOW44"'
A2_NEW = '"RIDGE_GLOW44","STONE_GLOW44","DEEP_GLOW44","TRENCH_GLOW44","CORAL_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="DEEP_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="RIDGE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} RIDGE GLOW",cx,cy,"#fbbf24");\n'
    '        spawnShockwave(cx,cy,"#92400e");sfx("powerUp");\n'
    '        unlock("ridge_glow44_use");if(gs.streak>=20)unlock("ridge_glow44_max");\n'
    '      } else if(ptype==="STONE_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} STONE GLOW",cx,cy,"#d6d3d1");\n'
    '        spawnShockwave(cx,cy,"#44403c");sfx("powerUp");\n'
    '        unlock("stone_glow44_use");if(gs.streak>=20)unlock("stone_glow44_max");\n'
    '      } else if(ptype==="DEEP_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// DEEP_GLOW44 — +2528 deep glow bonus'
A4_NEW = (
    f'// RIDGE_GLOW44 — +{PW1SC} ridge glow bonus\n'
    f'        // STONE_GLOW44 — +{PW2SC} stone glow bonus\n'
    '        // DEEP_GLOW44 — +2528 deep glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawGyroliteFox9e('
A5_NEW = (
    f'function drawHastingsiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bbf7d0");g.addColorStop(0.45+sp*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(187,247,208,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#052e16":"#bbf7d0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌿":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawHatchettiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fed7aa");g.addColorStop(0.35+tp*0.35,"#7c2d12");g.addColorStop(1,"#431407");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,215,170,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(124,45,18,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#7c2d12":"#fed7aa";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔥":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawGyroliteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="gyrolite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="hastingsite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp767a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHastingsiteFox9e(ctx,t.radius,ts,sp767a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hatchettite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp767b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHatchettiteOrb9e(ctx,t.radius,ts,tp767b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="gyrolite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="gyrolite_fox9e"){'
A7_NEW = (
    'if(hit.type==="hastingsite_fox9e"){\n'
    f'          const sp767c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts767a=Math.round({FOXSC}*(1+sp767c));\n'
    '          gs.score+=pts767a;gs.streak++;addPopup("+"+pts767a+(sp767c>0.88?" 🌿 PEAK!":""),hit.x,hit.y,"#bbf7d0");\n'
    '          spawnShockwave(hit.x,hit.y,"#166534");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp767c>0.88){sfx("legendary");unlock("hastingsite_fox9e_peak");}else unlock("hastingsite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hatchettite_orb9e"){\n'
    f'          const tp767d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts767b=Math.round({ORBSC}*(1+tp767d));\n'
    '          gs.score+=pts767b;gs.streak++;addPopup("+"+pts767b+(tp767d>0.88?" 🔥 PEAK!":""),hit.x,hit.y,"#fed7aa");\n'
    '          spawnShockwave(hit.x,hit.y,"#7c2d12");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp767d>0.88){sfx("legendary");unlock("hatchettite_orb9e_peak");}else unlock("hatchettite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="gyrolite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="gyrolite_fox9e";color="#0c4a6e";glow="#f0f9ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="hambergite_orb9e"')
A8_NEW = (
    '      type="hastingsite_fox9e";color="#166534";glow="#bbf7d0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hatchettite_orb9e";color="#7c2d12";glow="#fed7aa";\n'
    '    } else if('+COND100F+'){\n'
    '      type="gyrolite_fox9e";color="#0c4a6e";glow="#f0f9ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hambergite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="gyrolite_fox9e"?BASE_R*2.11:type==="hambergite_orb9e"?BASE_R*2.10:'
A9_NEW = f'type==="hastingsite_fox9e"?{FOX_R}:type==="hatchettite_orb9e"?{ORB_R}:type==="gyrolite_fox9e"?BASE_R*2.11:type==="hambergite_orb9e"?BASE_R*2.10:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'DEEP_GLOW44:"🌊✨",TRENCH_GLOW44:"🌌✨",CORAL_GLOW44:"🪸✨"'
A10_NEW = 'RIDGE_GLOW44:"⛰️✨",STONE_GLOW44:"🪨✨",DEEP_GLOW44:"🌊✨",TRENCH_GLOW44:"🌌✨",CORAL_GLOW44:"🪸✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 767 done! +{len(src)-orig_len} bytes")
