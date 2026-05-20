#!/usr/bin/env python3
"""Batch 782: WHARF_GLOW44+QUAY_GLOW44 + MargariteFox9e+MasuyiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4377"
SW = "2358"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.27"
ORB_R = f"{BASE_R}*2.26"
FOXSC = 548
ORBSC = 543
PW1SC = 2592
PW2SC = 2594

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"mackinawite_fox9e_tap", label:"Mackinawite Fox Tap"'
A1_NEW = (
    '  { id:"margarite_fox9e_tap", label:"Margarite Fox Tap", desc:"Tap Margarite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"margarite_fox9e_peak", label:"Margarite Fox Peak", desc:"Tap Margarite Fox at peak", icon:"🌹", xp:88 },\n'
    '  { id:"masuyite_orb9e_tap", label:"Masuyite Orb Tap", desc:"Tap Masuyite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"masuyite_orb9e_peak", label:"Masuyite Orb Peak", desc:"Tap Masuyite Orb at peak", icon:"🟠", xp:88 },\n'
    '  { id:"wharf_glow44_use", label:"Wharf Glow Use", desc:"Activate Wharf Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"wharf_glow44_max", label:"Wharf Glow Max", desc:"Activate Wharf Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"quay_glow44_use", label:"Quay Glow Use", desc:"Activate Quay Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"quay_glow44_max", label:"Quay Glow Max", desc:"Activate Quay Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"mackinawite_fox9e_tap", label:"Mackinawite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"DOCK_GLOW44","PIER_GLOW44","MAST_GLOW44"'
A2_NEW = '"WHARF_GLOW44","QUAY_GLOW44","DOCK_GLOW44","PIER_GLOW44","MAST_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="DOCK_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="WHARF_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} WHARF GLOW",cx,cy,"#a5f3fc");\n'
    '        spawnShockwave(cx,cy,"#0e7490");sfx("powerUp");\n'
    '        unlock("wharf_glow44_use");if(gs.streak>=20)unlock("wharf_glow44_max");\n'
    '      } else if(ptype==="QUAY_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} QUAY GLOW",cx,cy,"#bae6fd");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("quay_glow44_use");if(gs.streak>=20)unlock("quay_glow44_max");\n'
    '      } else if(ptype==="DOCK_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// DOCK_GLOW44 — +2588 dock glow bonus'
A4_NEW = (
    f'// WHARF_GLOW44 — +{PW1SC} wharf glow bonus\n'
    f'        // QUAY_GLOW44 — +{PW2SC} quay glow bonus\n'
    '        // DOCK_GLOW44 — +2588 dock glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMackinawiteFox9e('
A5_NEW = (
    f'function drawMargariteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+sp*0.35,"#be185d");g.addColorStop(1,"#500724");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(253,242,248,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#500724":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌹":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMasuyiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffedd5");g.addColorStop(0.35+tp*0.35,"#ea580c");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(255,237,213,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(234,88,12,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#ea580c":"#ffedd5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟠":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMackinawiteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="mackinawite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="margarite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp782a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMargariteFox9e(ctx,t.radius,ts,sp782a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="masuyite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp782b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMasuyiteOrb9e(ctx,t.radius,ts,tp782b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="mackinawite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="mackinawite_fox9e"){'
A7_NEW = (
    'if(hit.type==="margarite_fox9e"){\n'
    f'          const sp782c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts782a=Math.round({FOXSC}*(1+sp782c));\n'
    '          gs.score+=pts782a;gs.streak++;addPopup("+"+pts782a+(sp782c>0.88?" 🌹 PEAK!":""),hit.x,hit.y,"#fdf2f8");\n'
    '          spawnShockwave(hit.x,hit.y,"#be185d");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp782c>0.88){sfx("legendary");unlock("margarite_fox9e_peak");}else unlock("margarite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="masuyite_orb9e"){\n'
    f'          const tp782d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts782b=Math.round({ORBSC}*(1+tp782d));\n'
    '          gs.score+=pts782b;gs.streak++;addPopup("+"+pts782b+(tp782d>0.88?" 🟠 PEAK!":""),hit.x,hit.y,"#ffedd5");\n'
    '          spawnShockwave(hit.x,hit.y,"#ea580c");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp782d>0.88){sfx("legendary");unlock("masuyite_orb9e_peak");}else unlock("masuyite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="mackinawite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="mackinawite_fox9e";color="#c2410c";glow="#ffedd5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="maghemite_orb9e"')
A8_NEW = (
    '      type="margarite_fox9e";color="#be185d";glow="#fdf2f8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="masuyite_orb9e";color="#ea580c";glow="#ffedd5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mackinawite_fox9e";color="#c2410c";glow="#ffedd5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="maghemite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="mackinawite_fox9e"?BASE_R*2.26:type==="maghemite_orb9e"?BASE_R*2.25:'
A9_NEW = f'type==="margarite_fox9e"?{FOX_R}:type==="masuyite_orb9e"?{ORB_R}:type==="mackinawite_fox9e"?BASE_R*2.26:type==="maghemite_orb9e"?BASE_R*2.25:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'DOCK_GLOW44:"⚓✨",PIER_GLOW44:"🌊✨",MAST_GLOW44:"⛵✨"'
A10_NEW = 'WHARF_GLOW44:"⚓✨",QUAY_GLOW44:"🌊✨",DOCK_GLOW44:"⚓✨",PIER_GLOW44:"🌊✨",MAST_GLOW44:"⛵✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 782 done! +{len(src)-orig_len} bytes")
