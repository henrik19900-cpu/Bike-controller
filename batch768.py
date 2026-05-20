#!/usr/bin/env python3
"""Batch 768: SLOPE_GLOW44+HILL_GLOW44 + HeliodorFox9e+HedenbergiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4321"
SW = "2330"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.13"
ORB_R = f"{BASE_R}*2.12"
FOXSC = 520
ORBSC = 515
PW1SC = 2536
PW2SC = 2538

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"hastingsite_fox9e_tap", label:"Hastingsite Fox Tap"'
A1_NEW = (
    '  { id:"heliodor_fox9e_tap", label:"Heliodor Fox Tap", desc:"Tap Heliodor Fox", icon:"🦊", xp:62 },\n'
    '  { id:"heliodor_fox9e_peak", label:"Heliodor Fox Peak", desc:"Tap Heliodor Fox at peak", icon:"☀️", xp:88 },\n'
    '  { id:"hedenbergite_orb9e_tap", label:"Hedenbergite Orb Tap", desc:"Tap Hedenbergite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"hedenbergite_orb9e_peak", label:"Hedenbergite Orb Peak", desc:"Tap Hedenbergite Orb at peak", icon:"💧", xp:88 },\n'
    '  { id:"slope_glow44_use", label:"Slope Glow Use", desc:"Activate Slope Glow power-up", icon:"🏔️", xp:50 },\n'
    '  { id:"slope_glow44_max", label:"Slope Glow Max", desc:"Activate Slope Glow at max streak", icon:"🏔️", xp:75 },\n'
    '  { id:"hill_glow44_use", label:"Hill Glow Use", desc:"Activate Hill Glow power-up", icon:"🌄", xp:50 },\n'
    '  { id:"hill_glow44_max", label:"Hill Glow Max", desc:"Activate Hill Glow at max streak", icon:"🌄", xp:75 },\n'
    '  { id:"hastingsite_fox9e_tap", label:"Hastingsite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"RIDGE_GLOW44","STONE_GLOW44","DEEP_GLOW44"'
A2_NEW = '"SLOPE_GLOW44","HILL_GLOW44","RIDGE_GLOW44","STONE_GLOW44","DEEP_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="RIDGE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="SLOPE_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} SLOPE GLOW",cx,cy,"#d6d3d1");\n'
    '        spawnShockwave(cx,cy,"#78716c");sfx("powerUp");\n'
    '        unlock("slope_glow44_use");if(gs.streak>=20)unlock("slope_glow44_max");\n'
    '      } else if(ptype==="HILL_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} HILL GLOW",cx,cy,"#bef264");\n'
    '        spawnShockwave(cx,cy,"#365314");sfx("powerUp");\n'
    '        unlock("hill_glow44_use");if(gs.streak>=20)unlock("hill_glow44_max");\n'
    '      } else if(ptype==="RIDGE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// RIDGE_GLOW44 — +2532 ridge glow bonus'
A4_NEW = (
    f'// SLOPE_GLOW44 — +{PW1SC} slope glow bonus\n'
    f'        // HILL_GLOW44 — +{PW2SC} hill glow bonus\n'
    '        // RIDGE_GLOW44 — +2532 ridge glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHastingsiteFox9e('
A5_NEW = (
    f'function drawHeliodorFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.45+sp*0.35,"#92400e");g.addColorStop(1,"#451a03");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,243,199,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#451a03":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"☀️":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawHedenbergiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ccfbf1");g.addColorStop(0.35+tp*0.35,"#134e4a");g.addColorStop(1,"#042f2e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(204,251,241,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(19,78,74,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#134e4a":"#ccfbf1";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💧":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawHastingsiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="hastingsite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="heliodor_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp768a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHeliodorFox9e(ctx,t.radius,ts,sp768a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hedenbergite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp768b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHedenbergiteOrb9e(ctx,t.radius,ts,tp768b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="hastingsite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="hastingsite_fox9e"){'
A7_NEW = (
    'if(hit.type==="heliodor_fox9e"){\n'
    f'          const sp768c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts768a=Math.round({FOXSC}*(1+sp768c));\n'
    '          gs.score+=pts768a;gs.streak++;addPopup("+"+pts768a+(sp768c>0.88?" ☀️ PEAK!":""),hit.x,hit.y,"#fef3c7");\n'
    '          spawnShockwave(hit.x,hit.y,"#92400e");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp768c>0.88){sfx("legendary");unlock("heliodor_fox9e_peak");}else unlock("heliodor_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hedenbergite_orb9e"){\n'
    f'          const tp768d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts768b=Math.round({ORBSC}*(1+tp768d));\n'
    '          gs.score+=pts768b;gs.streak++;addPopup("+"+pts768b+(tp768d>0.88?" 💧 PEAK!":""),hit.x,hit.y,"#ccfbf1");\n'
    '          spawnShockwave(hit.x,hit.y,"#134e4a");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp768d>0.88){sfx("legendary");unlock("hedenbergite_orb9e_peak");}else unlock("hedenbergite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="hastingsite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="hastingsite_fox9e";color="#166534";glow="#bbf7d0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="hatchettite_orb9e"')
A8_NEW = (
    '      type="heliodor_fox9e";color="#92400e";glow="#fef3c7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hedenbergite_orb9e";color="#134e4a";glow="#ccfbf1";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hastingsite_fox9e";color="#166534";glow="#bbf7d0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hatchettite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="hastingsite_fox9e"?BASE_R*2.12:type==="hatchettite_orb9e"?BASE_R*2.11:'
A9_NEW = f'type==="heliodor_fox9e"?{FOX_R}:type==="hedenbergite_orb9e"?{ORB_R}:type==="hastingsite_fox9e"?BASE_R*2.12:type==="hatchettite_orb9e"?BASE_R*2.11:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'RIDGE_GLOW44:"⛰️✨",STONE_GLOW44:"🪨✨",DEEP_GLOW44:"🌊✨"'
A10_NEW = 'SLOPE_GLOW44:"🏔️✨",HILL_GLOW44:"🌄✨",RIDGE_GLOW44:"⛰️✨",STONE_GLOW44:"🪨✨",DEEP_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 768 done! +{len(src)-orig_len} bytes")
