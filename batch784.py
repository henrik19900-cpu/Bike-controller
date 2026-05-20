#!/usr/bin/env python3
"""Batch 784: FIRTH_GLOW44+SOUND_GLOW44 + MeloniteFox9e+MerwiniteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4385"
SW = "2362"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.29"
ORB_R = f"{BASE_R}*2.28"
FOXSC = 552
ORBSC = 547
PW1SC = 2600
PW2SC = 2602

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"matildite_fox9e_tap", label:"Matildite Fox Tap"'
A1_NEW = (
    '  { id:"melonite_fox9e_tap", label:"Melonite Fox Tap", desc:"Tap Melonite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"melonite_fox9e_peak", label:"Melonite Fox Peak", desc:"Tap Melonite Fox at peak", icon:"🍈", xp:88 },\n'
    '  { id:"merwinite_orb9e_tap", label:"Merwinite Orb Tap", desc:"Tap Merwinite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"merwinite_orb9e_peak", label:"Merwinite Orb Peak", desc:"Tap Merwinite Orb at peak", icon:"🪩", xp:88 },\n'
    '  { id:"firth_glow44_use", label:"Firth Glow Use", desc:"Activate Firth Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"firth_glow44_max", label:"Firth Glow Max", desc:"Activate Firth Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"sound_glow44_use", label:"Sound Glow Use", desc:"Activate Sound Glow power-up", icon:"🎵", xp:50 },\n'
    '  { id:"sound_glow44_max", label:"Sound Glow Max", desc:"Activate Sound Glow at max streak", icon:"🎵", xp:75 },\n'
    '  { id:"matildite_fox9e_tap", label:"Matildite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"LOCH_GLOW44","FORD_GLOW44","WHARF_GLOW44"'
A2_NEW = '"FIRTH_GLOW44","SOUND_GLOW44","LOCH_GLOW44","FORD_GLOW44","WHARF_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="LOCH_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="FIRTH_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} FIRTH GLOW",cx,cy,"#7dd3fc");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("firth_glow44_use");if(gs.streak>=20)unlock("firth_glow44_max");\n'
    '      } else if(ptype==="SOUND_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} SOUND GLOW",cx,cy,"#c4b5fd");\n'
    '        spawnShockwave(cx,cy,"#6d28d9");sfx("powerUp");\n'
    '        unlock("sound_glow44_use");if(gs.streak>=20)unlock("sound_glow44_max");\n'
    '      } else if(ptype==="LOCH_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// LOCH_GLOW44 — +2596 loch glow bonus'
A4_NEW = (
    f'// FIRTH_GLOW44 — +{PW1SC} firth glow bonus\n'
    f'        // SOUND_GLOW44 — +{PW2SC} sound glow bonus\n'
    '        // LOCH_GLOW44 — +2596 loch glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMatilditeFox9e('
A5_NEW = (
    f'function drawMeloniteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.45+sp*0.35,"#16a34a");g.addColorStop(1,"#052e16");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(220,252,231,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#052e16":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🍈":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMerwiniteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ede9fe");g.addColorStop(0.35+tp*0.35,"#7c3aed");g.addColorStop(1,"#2e1065");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(237,233,254,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(124,58,237,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#7c3aed":"#ede9fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🪩":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMatilditeFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="matildite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="melonite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp784a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMeloniteFox9e(ctx,t.radius,ts,sp784a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="merwinite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp784b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMerwiniteOrb9e(ctx,t.radius,ts,tp784b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="matildite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="matildite_fox9e"){'
A7_NEW = (
    'if(hit.type==="melonite_fox9e"){\n'
    f'          const sp784c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts784a=Math.round({FOXSC}*(1+sp784c));\n'
    '          gs.score+=pts784a;gs.streak++;addPopup("+"+pts784a+(sp784c>0.88?" 🍈 PEAK!":""),hit.x,hit.y,"#dcfce7");\n'
    '          spawnShockwave(hit.x,hit.y,"#16a34a");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp784c>0.88){sfx("legendary");unlock("melonite_fox9e_peak");}else unlock("melonite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="merwinite_orb9e"){\n'
    f'          const tp784d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts784b=Math.round({ORBSC}*(1+tp784d));\n'
    '          gs.score+=pts784b;gs.streak++;addPopup("+"+pts784b+(tp784d>0.88?" 🪩 PEAK!":""),hit.x,hit.y,"#ede9fe");\n'
    '          spawnShockwave(hit.x,hit.y,"#7c3aed");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp784d>0.88){sfx("legendary");unlock("merwinite_orb9e_peak");}else unlock("merwinite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="matildite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="matildite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="mawsonite_orb9e"')
A8_NEW = (
    '      type="melonite_fox9e";color="#16a34a";glow="#dcfce7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="merwinite_orb9e";color="#7c3aed";glow="#ede9fe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="matildite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mawsonite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="matildite_fox9e"?BASE_R*2.28:type==="mawsonite_orb9e"?BASE_R*2.27:'
A9_NEW = f'type==="melonite_fox9e"?{FOX_R}:type==="merwinite_orb9e"?{ORB_R}:type==="matildite_fox9e"?BASE_R*2.28:type==="mawsonite_orb9e"?BASE_R*2.27:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'LOCH_GLOW44:"🌊✨",FORD_GLOW44:"🌿✨",WHARF_GLOW44:"⚓✨"'
A10_NEW = 'FIRTH_GLOW44:"🌊✨",SOUND_GLOW44:"🎵✨",LOCH_GLOW44:"🌊✨",FORD_GLOW44:"🌿✨",WHARF_GLOW44:"⚓✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 784 done! +{len(src)-orig_len} bytes")
