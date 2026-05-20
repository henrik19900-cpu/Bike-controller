#!/usr/bin/env python3
"""Batch 780: MAST_GLOW44+BEACON_GLOW44 + LithargeFox9e+LudwigiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4369"
SW = "2354"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.25"
ORB_R = f"{BASE_R}*2.24"
FOXSC = 544
ORBSC = 539
PW1SC = 2584
PW2SC = 2586

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"lindgrenite_fox9e_tap", label:"Lindgrenite Fox Tap"'
A1_NEW = (
    '  { id:"litharge_fox9e_tap", label:"Litharge Fox Tap", desc:"Tap Litharge Fox", icon:"🦊", xp:62 },\n'
    '  { id:"litharge_fox9e_peak", label:"Litharge Fox Peak", desc:"Tap Litharge Fox at peak", icon:"🟡", xp:88 },\n'
    '  { id:"ludwigite_orb9e_tap", label:"Ludwigite Orb Tap", desc:"Tap Ludwigite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"ludwigite_orb9e_peak", label:"Ludwigite Orb Peak", desc:"Tap Ludwigite Orb at peak", icon:"🌑", xp:88 },\n'
    '  { id:"mast_glow44_use", label:"Mast Glow Use", desc:"Activate Mast Glow power-up", icon:"⛵", xp:50 },\n'
    '  { id:"mast_glow44_max", label:"Mast Glow Max", desc:"Activate Mast Glow at max streak", icon:"⛵", xp:75 },\n'
    '  { id:"beacon_glow44_use", label:"Beacon Glow Use", desc:"Activate Beacon Glow power-up", icon:"🔦", xp:50 },\n'
    '  { id:"beacon_glow44_max", label:"Beacon Glow Max", desc:"Activate Beacon Glow at max streak", icon:"🔦", xp:75 },\n'
    '  { id:"lindgrenite_fox9e_tap", label:"Lindgrenite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"CRAG_GLOW44","HELM_GLOW44","CAPE_GLOW44"'
A2_NEW = '"MAST_GLOW44","BEACON_GLOW44","CRAG_GLOW44","HELM_GLOW44","CAPE_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="CRAG_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="MAST_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} MAST GLOW",cx,cy,"#bae6fd");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("mast_glow44_use");if(gs.streak>=20)unlock("mast_glow44_max");\n'
    '      } else if(ptype==="BEACON_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} BEACON GLOW",cx,cy,"#fde68a");\n'
    '        spawnShockwave(cx,cy,"#d97706");sfx("powerUp");\n'
    '        unlock("beacon_glow44_use");if(gs.streak>=20)unlock("beacon_glow44_max");\n'
    '      } else if(ptype==="CRAG_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// CRAG_GLOW44 — +2580 crag glow bonus'
A4_NEW = (
    f'// MAST_GLOW44 — +{PW1SC} mast glow bonus\n'
    f'        // BEACON_GLOW44 — +{PW2SC} beacon glow bonus\n'
    '        // CRAG_GLOW44 — +2580 crag glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawLindgreniteFox9e('
A5_NEW = (
    f'function drawLithargeFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.45+sp*0.35,"#f59e0b");g.addColorStop(1,"#78350f");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,243,199,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#78350f":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟡":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawLudwigiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e2e8f0");g.addColorStop(0.35+tp*0.35,"#1e293b");g.addColorStop(1,"#0f172a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(226,232,240,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(30,41,59,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#1e293b":"#e2e8f0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌑":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawLindgreniteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="lindgrenite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="litharge_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp780a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLithargeFox9e(ctx,t.radius,ts,sp780a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="ludwigite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp780b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawLudwigiteOrb9e(ctx,t.radius,ts,tp780b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="lindgrenite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="lindgrenite_fox9e"){'
A7_NEW = (
    'if(hit.type==="litharge_fox9e"){\n'
    f'          const sp780c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts780a=Math.round({FOXSC}*(1+sp780c));\n'
    '          gs.score+=pts780a;gs.streak++;addPopup("+"+pts780a+(sp780c>0.88?" 🟡 PEAK!":""),hit.x,hit.y,"#fef3c7");\n'
    '          spawnShockwave(hit.x,hit.y,"#f59e0b");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp780c>0.88){sfx("legendary");unlock("litharge_fox9e_peak");}else unlock("litharge_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="ludwigite_orb9e"){\n'
    f'          const tp780d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts780b=Math.round({ORBSC}*(1+tp780d));\n'
    '          gs.score+=pts780b;gs.streak++;addPopup("+"+pts780b+(tp780d>0.88?" 🌑 PEAK!":""),hit.x,hit.y,"#e2e8f0");\n'
    '          spawnShockwave(hit.x,hit.y,"#1e293b");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp780d>0.88){sfx("legendary");unlock("ludwigite_orb9e_peak");}else unlock("ludwigite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="lindgrenite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="lindgrenite_fox9e";color="#059669";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="liskeardite_orb9e"')
A8_NEW = (
    '      type="litharge_fox9e";color="#f59e0b";glow="#fef3c7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ludwigite_orb9e";color="#1e293b";glow="#e2e8f0";\n'
    '    } else if('+COND100F+'){\n'
    '      type="lindgrenite_fox9e";color="#059669";glow="#d1fae5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="liskeardite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="lindgrenite_fox9e"?BASE_R*2.24:type==="liskeardite_orb9e"?BASE_R*2.23:'
A9_NEW = f'type==="litharge_fox9e"?{FOX_R}:type==="ludwigite_orb9e"?{ORB_R}:type==="lindgrenite_fox9e"?BASE_R*2.24:type==="liskeardite_orb9e"?BASE_R*2.23:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'CRAG_GLOW44:"🪨✨",HELM_GLOW44:"⚓✨",CAPE_GLOW44:"🌊✨"'
A10_NEW = 'MAST_GLOW44:"⛵✨",BEACON_GLOW44:"🔦✨",CRAG_GLOW44:"🪨✨",HELM_GLOW44:"⚓✨",CAPE_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 780 done! +{len(src)-orig_len} bytes")
