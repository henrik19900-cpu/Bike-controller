#!/usr/bin/env python3
"""Batch 781: DOCK_GLOW44+PIER_GLOW44 + MackinawiteFox9e+MaghemiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4373"
SW = "2356"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.26"
ORB_R = f"{BASE_R}*2.25"
FOXSC = 546
ORBSC = 541
PW1SC = 2588
PW2SC = 2590

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"litharge_fox9e_tap", label:"Litharge Fox Tap"'
A1_NEW = (
    '  { id:"mackinawite_fox9e_tap", label:"Mackinawite Fox Tap", desc:"Tap Mackinawite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"mackinawite_fox9e_peak", label:"Mackinawite Fox Peak", desc:"Tap Mackinawite Fox at peak", icon:"🔶", xp:88 },\n'
    '  { id:"maghemite_orb9e_tap", label:"Maghemite Orb Tap", desc:"Tap Maghemite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"maghemite_orb9e_peak", label:"Maghemite Orb Peak", desc:"Tap Maghemite Orb at peak", icon:"🟥", xp:88 },\n'
    '  { id:"dock_glow44_use", label:"Dock Glow Use", desc:"Activate Dock Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"dock_glow44_max", label:"Dock Glow Max", desc:"Activate Dock Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"pier_glow44_use", label:"Pier Glow Use", desc:"Activate Pier Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"pier_glow44_max", label:"Pier Glow Max", desc:"Activate Pier Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"litharge_fox9e_tap", label:"Litharge Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"MAST_GLOW44","BEACON_GLOW44","CRAG_GLOW44"'
A2_NEW = '"DOCK_GLOW44","PIER_GLOW44","MAST_GLOW44","BEACON_GLOW44","CRAG_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="MAST_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="DOCK_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} DOCK GLOW",cx,cy,"#93c5fd");\n'
    '        spawnShockwave(cx,cy,"#1d4ed8");sfx("powerUp");\n'
    '        unlock("dock_glow44_use");if(gs.streak>=20)unlock("dock_glow44_max");\n'
    '      } else if(ptype==="PIER_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} PIER GLOW",cx,cy,"#67e8f9");\n'
    '        spawnShockwave(cx,cy,"#0e7490");sfx("powerUp");\n'
    '        unlock("pier_glow44_use");if(gs.streak>=20)unlock("pier_glow44_max");\n'
    '      } else if(ptype==="MAST_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// MAST_GLOW44 — +2584 mast glow bonus'
A4_NEW = (
    f'// DOCK_GLOW44 — +{PW1SC} dock glow bonus\n'
    f'        // PIER_GLOW44 — +{PW2SC} pier glow bonus\n'
    '        // MAST_GLOW44 — +2584 mast glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawLithargeFox9e('
A5_NEW = (
    f'function drawMackinawiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffedd5");g.addColorStop(0.45+sp*0.35,"#c2410c");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(255,237,213,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#7c2d12":"#ffedd5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🔶":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMaghemiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fee2e2");g.addColorStop(0.35+tp*0.35,"#dc2626");g.addColorStop(1,"#7f1d1d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,226,226,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(220,38,38,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#dc2626":"#fee2e2";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟥":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawLithargeFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="litharge_fox9e"){'
A6_NEW = (
    '  else if(t.type==="mackinawite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp781a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMackinawiteFox9e(ctx,t.radius,ts,sp781a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="maghemite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp781b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMaghemiteOrb9e(ctx,t.radius,ts,tp781b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="litharge_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="litharge_fox9e"){'
A7_NEW = (
    'if(hit.type==="mackinawite_fox9e"){\n'
    f'          const sp781c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts781a=Math.round({FOXSC}*(1+sp781c));\n'
    '          gs.score+=pts781a;gs.streak++;addPopup("+"+pts781a+(sp781c>0.88?" 🔶 PEAK!":""),hit.x,hit.y,"#ffedd5");\n'
    '          spawnShockwave(hit.x,hit.y,"#c2410c");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp781c>0.88){sfx("legendary");unlock("mackinawite_fox9e_peak");}else unlock("mackinawite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="maghemite_orb9e"){\n'
    f'          const tp781d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts781b=Math.round({ORBSC}*(1+tp781d));\n'
    '          gs.score+=pts781b;gs.streak++;addPopup("+"+pts781b+(tp781d>0.88?" 🟥 PEAK!":""),hit.x,hit.y,"#fee2e2");\n'
    '          spawnShockwave(hit.x,hit.y,"#dc2626");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp781d>0.88){sfx("legendary");unlock("maghemite_orb9e_peak");}else unlock("maghemite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="litharge_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="litharge_fox9e";color="#f59e0b";glow="#fef3c7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="ludwigite_orb9e"')
A8_NEW = (
    '      type="mackinawite_fox9e";color="#c2410c";glow="#ffedd5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="maghemite_orb9e";color="#dc2626";glow="#fee2e2";\n'
    '    } else if('+COND100F+'){\n'
    '      type="litharge_fox9e";color="#f59e0b";glow="#fef3c7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ludwigite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="litharge_fox9e"?BASE_R*2.25:type==="ludwigite_orb9e"?BASE_R*2.24:'
A9_NEW = f'type==="mackinawite_fox9e"?{FOX_R}:type==="maghemite_orb9e"?{ORB_R}:type==="litharge_fox9e"?BASE_R*2.25:type==="ludwigite_orb9e"?BASE_R*2.24:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'MAST_GLOW44:"⛵✨",BEACON_GLOW44:"🔦✨",CRAG_GLOW44:"🪨✨"'
A10_NEW = 'DOCK_GLOW44:"⚓✨",PIER_GLOW44:"🌊✨",MAST_GLOW44:"⛵✨",BEACON_GLOW44:"🔦✨",CRAG_GLOW44:"🪨✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 781 done! +{len(src)-orig_len} bytes")
