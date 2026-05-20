#!/usr/bin/env python3
"""Batch 769: PEAK_GLOW44+VALE_GLOW44 + HollanditeFox9e+HowliteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4325"
SW = "2332"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.14"
ORB_R = f"{BASE_R}*2.13"
FOXSC = 522
ORBSC = 517
PW1SC = 2540
PW2SC = 2542

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"heliodor_fox9e_tap", label:"Heliodor Fox Tap"'
A1_NEW = (
    '  { id:"hollandite_fox9e_tap", label:"Hollandite Fox Tap", desc:"Tap Hollandite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"hollandite_fox9e_peak", label:"Hollandite Fox Peak", desc:"Tap Hollandite Fox at peak", icon:"🌑", xp:88 },\n'
    '  { id:"howlite_orb9e_tap", label:"Howlite Orb Tap", desc:"Tap Howlite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"howlite_orb9e_peak", label:"Howlite Orb Peak", desc:"Tap Howlite Orb at peak", icon:"🤍", xp:88 },\n'
    '  { id:"peak_glow44_use", label:"Peak Glow Use", desc:"Activate Peak Glow power-up", icon:"⛰️", xp:50 },\n'
    '  { id:"peak_glow44_max", label:"Peak Glow Max", desc:"Activate Peak Glow at max streak", icon:"⛰️", xp:75 },\n'
    '  { id:"vale_glow44_use", label:"Vale Glow Use", desc:"Activate Vale Glow power-up", icon:"🌿", xp:50 },\n'
    '  { id:"vale_glow44_max", label:"Vale Glow Max", desc:"Activate Vale Glow at max streak", icon:"🌿", xp:75 },\n'
    '  { id:"heliodor_fox9e_tap", label:"Heliodor Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"SLOPE_GLOW44","HILL_GLOW44","RIDGE_GLOW44"'
A2_NEW = '"PEAK_GLOW44","VALE_GLOW44","SLOPE_GLOW44","HILL_GLOW44","RIDGE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="SLOPE_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="PEAK_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} PEAK GLOW",cx,cy,"#e2e8f0");\n'
    '        spawnShockwave(cx,cy,"#475569");sfx("powerUp");\n'
    '        unlock("peak_glow44_use");if(gs.streak>=20)unlock("peak_glow44_max");\n'
    '      } else if(ptype==="VALE_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} VALE GLOW",cx,cy,"#86efac");\n'
    '        spawnShockwave(cx,cy,"#166534");sfx("powerUp");\n'
    '        unlock("vale_glow44_use");if(gs.streak>=20)unlock("vale_glow44_max");\n'
    '      } else if(ptype==="SLOPE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// SLOPE_GLOW44 — +2536 slope glow bonus'
A4_NEW = (
    f'// PEAK_GLOW44 — +{PW1SC} peak glow bonus\n'
    f'        // VALE_GLOW44 — +{PW2SC} vale glow bonus\n'
    '        // SLOPE_GLOW44 — +2536 slope glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHeliodorFox9e('
A5_NEW = (
    f'function drawHollanditeFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e2e8f0");g.addColorStop(0.45+sp*0.35,"#334155");g.addColorStop(1,"#0f172a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(226,232,240,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0f172a":"#e2e8f0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌑":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawHowliteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+tp*0.35,"#94a3b8");g.addColorStop(1,"#1e293b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(248,250,252,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🤍":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawHeliodorFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="heliodor_fox9e"){'
A6_NEW = (
    '  else if(t.type==="hollandite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp769a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHollanditeFox9e(ctx,t.radius,ts,sp769a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="howlite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp769b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawHowliteOrb9e(ctx,t.radius,ts,tp769b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="heliodor_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="heliodor_fox9e"){'
A7_NEW = (
    'if(hit.type==="hollandite_fox9e"){\n'
    f'          const sp769c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts769a=Math.round({FOXSC}*(1+sp769c));\n'
    '          gs.score+=pts769a;gs.streak++;addPopup("+"+pts769a+(sp769c>0.88?" 🌑 PEAK!":""),hit.x,hit.y,"#e2e8f0");\n'
    '          spawnShockwave(hit.x,hit.y,"#334155");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp769c>0.88){sfx("legendary");unlock("hollandite_fox9e_peak");}else unlock("hollandite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="howlite_orb9e"){\n'
    f'          const tp769d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts769b=Math.round({ORBSC}*(1+tp769d));\n'
    '          gs.score+=pts769b;gs.streak++;addPopup("+"+pts769b+(tp769d>0.88?" 🤍 PEAK!":""),hit.x,hit.y,"#f8fafc");\n'
    '          spawnShockwave(hit.x,hit.y,"#94a3b8");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp769d>0.88){sfx("legendary");unlock("howlite_orb9e_peak");}else unlock("howlite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="heliodor_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="heliodor_fox9e";color="#92400e";glow="#fef3c7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="hedenbergite_orb9e"')
A8_NEW = (
    '      type="hollandite_fox9e";color="#334155";glow="#e2e8f0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="howlite_orb9e";color="#94a3b8";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="heliodor_fox9e";color="#92400e";glow="#fef3c7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="hedenbergite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="heliodor_fox9e"?BASE_R*2.13:type==="hedenbergite_orb9e"?BASE_R*2.12:'
A9_NEW = f'type==="hollandite_fox9e"?{FOX_R}:type==="howlite_orb9e"?{ORB_R}:type==="heliodor_fox9e"?BASE_R*2.13:type==="hedenbergite_orb9e"?BASE_R*2.12:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'SLOPE_GLOW44:"🏔️✨",HILL_GLOW44:"🌄✨",RIDGE_GLOW44:"⛰️✨"'
A10_NEW = 'PEAK_GLOW44:"⛰️✨",VALE_GLOW44:"🌿✨",SLOPE_GLOW44:"🏔️✨",HILL_GLOW44:"🌄✨",RIDGE_GLOW44:"⛰️✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 769 done! +{len(src)-orig_len} bytes")
