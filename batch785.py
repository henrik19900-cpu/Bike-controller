#!/usr/bin/env python3
"""Batch 785: CHANNEL_GLOW44+STRAIT_GLOW44 + MiargyriteFox9e+MimetesiteOrb9e + 8 achievements"""
import re, sys

F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

OSC = "0.4389"
SW = "2364"
BASE_R = "BASE_R"
FOX_R = f"{BASE_R}*2.30"
ORB_R = f"{BASE_R}*2.29"
FOXSC = 554
ORBSC = 549
PW1SC = 2604
PW2SC = 2606

# ── STEP 1: achievements ──────────────────────────────────────────────────────
A1_OLD = '  { id:"melonite_fox9e_tap", label:"Melonite Fox Tap"'
A1_NEW = (
    '  { id:"miargyrite_fox9e_tap", label:"Miargyrite Fox Tap", desc:"Tap Miargyrite Fox", icon:"🦊", xp:62 },\n'
    '  { id:"miargyrite_fox9e_peak", label:"Miargyrite Fox Peak", desc:"Tap Miargyrite Fox at peak", icon:"🪙", xp:88 },\n'
    '  { id:"mimetesite_orb9e_tap", label:"Mimetesite Orb Tap", desc:"Tap Mimetesite Orb", icon:"🔮", xp:62 },\n'
    '  { id:"mimetesite_orb9e_peak", label:"Mimetesite Orb Peak", desc:"Tap Mimetesite Orb at peak", icon:"🌼", xp:88 },\n'
    '  { id:"channel_glow44_use", label:"Channel Glow Use", desc:"Activate Channel Glow power-up", icon:"🌊", xp:50 },\n'
    '  { id:"channel_glow44_max", label:"Channel Glow Max", desc:"Activate Channel Glow at max streak", icon:"🌊", xp:75 },\n'
    '  { id:"strait_glow44_use", label:"Strait Glow Use", desc:"Activate Strait Glow power-up", icon:"⚓", xp:50 },\n'
    '  { id:"strait_glow44_max", label:"Strait Glow Max", desc:"Activate Strait Glow at max streak", icon:"⚓", xp:75 },\n'
    '  { id:"melonite_fox9e_tap", label:"Melonite Fox Tap"'
)
assert src.count(A1_OLD) == 1, f"S1 anchor count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# ── STEP 2: power-up ID list ──────────────────────────────────────────────────
A2_OLD = '"FIRTH_GLOW44","SOUND_GLOW44","LOCH_GLOW44"'
A2_NEW = '"CHANNEL_GLOW44","STRAIT_GLOW44","FIRTH_GLOW44","SOUND_GLOW44","LOCH_GLOW44"'
assert src.count(A2_OLD) == 1, f"S2 anchor count={src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)

# ── STEP 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = '} else if(ptype==="FIRTH_GLOW44"){'
A3_NEW = (
    '} else if(ptype==="CHANNEL_GLOW44"){\n'
    f'        gs.score+=({PW1SC}+gs.streak*4);addPopup("+{PW1SC} CHANNEL GLOW",cx,cy,"#a5f3fc");\n'
    '        spawnShockwave(cx,cy,"#0891b2");sfx("powerUp");\n'
    '        unlock("channel_glow44_use");if(gs.streak>=20)unlock("channel_glow44_max");\n'
    '      } else if(ptype==="STRAIT_GLOW44"){\n'
    f'        gs.score+=({PW2SC}+gs.streak*4);addPopup("+{PW2SC} STRAIT GLOW",cx,cy,"#bae6fd");\n'
    '        spawnShockwave(cx,cy,"#0369a1");sfx("powerUp");\n'
    '        unlock("strait_glow44_use");if(gs.streak>=20)unlock("strait_glow44_max");\n'
    '      } else if(ptype==="FIRTH_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"S3 anchor count={src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)

# ── STEP 4: sfx/unlock comment block ─────────────────────────────────────────
A4_OLD = '// FIRTH_GLOW44 — +2600 firth glow bonus'
A4_NEW = (
    f'// CHANNEL_GLOW44 — +{PW1SC} channel glow bonus\n'
    f'        // STRAIT_GLOW44 — +{PW2SC} strait glow bonus\n'
    '        // FIRTH_GLOW44 — +2600 firth glow bonus'
)
assert src.count(A4_OLD) == 1, f"S4 anchor count={src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMeloniteFox9e('
A5_NEW = (
    f'function drawMiargyriteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.45+sp*0.35,"#d97706");g.addColorStop(1,"#78350f");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(254,249,195,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#78350f":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🪙":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    f'function drawMimetesiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+tp*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(254,252,232,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(234,179,8,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#eab308":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌼":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawMeloniteFox9e('
)
assert src.count(A5_OLD) == 1, f"S5 anchor count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="melonite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="miargyrite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp785a=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMiargyriteFox9e(ctx,t.radius,ts,sp785a);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="mimetesite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp785b=Math.min(1,(ts-t.born)/{SW});\n'
    '    drawMimetesiteOrb9e(ctx,t.radius,ts,tp785b);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="melonite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"S6 anchor count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="melonite_fox9e"){'
A7_NEW = (
    'if(hit.type==="miargyrite_fox9e"){\n'
    f'          const sp785c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts785a=Math.round({FOXSC}*(1+sp785c));\n'
    '          gs.score+=pts785a;gs.streak++;addPopup("+"+pts785a+(sp785c>0.88?" 🪙 PEAK!":""),hit.x,hit.y,"#fef9c3");\n'
    '          spawnShockwave(hit.x,hit.y,"#d97706");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(sp785c>0.88){sfx("legendary");unlock("miargyrite_fox9e_peak");}else unlock("miargyrite_fox9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="mimetesite_orb9e"){\n'
    f'          const tp785d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts785b=Math.round({ORBSC}*(1+tp785d));\n'
    '          gs.score+=pts785b;gs.streak++;addPopup("+"+pts785b+(tp785d>0.88?" 🌼 PEAK!":""),hit.x,hit.y,"#fefce8");\n'
    '          spawnShockwave(hit.x,hit.y,"#eab308");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    '          sfx("tap");if(tp785d>0.88){sfx("legendary");unlock("mimetesite_orb9e_peak");}else unlock("mimetesite_orb9e_tap");\n'
    '          updateMissions(gs.sessionStats);debounceSave();\n'
    '        } else if(hit.type==="melonite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"S7 anchor count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

# ── STEP 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="melonite_fox9e";color="#16a34a";glow="#dcfce7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="merwinite_orb9e"')
A8_NEW = (
    '      type="miargyrite_fox9e";color="#d97706";glow="#fef9c3";\n'
    '    } else if('+COND100F+'){\n'
    '      type="mimetesite_orb9e";color="#eab308";glow="#fefce8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="melonite_fox9e";color="#16a34a";glow="#dcfce7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="merwinite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"S8 anchor count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# ── STEP 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="melonite_fox9e"?BASE_R*2.29:type==="merwinite_orb9e"?BASE_R*2.28:'
A9_NEW = f'type==="miargyrite_fox9e"?{FOX_R}:type==="mimetesite_orb9e"?{ORB_R}:type==="melonite_fox9e"?BASE_R*2.29:type==="merwinite_orb9e"?BASE_R*2.28:'
assert src.count(A9_OLD) == 1, f"S9 anchor count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

# ── STEP 10: icon map (replace_all, assert count==2) ─────────────────────────
A10_OLD = 'FIRTH_GLOW44:"🌊✨",SOUND_GLOW44:"🎵✨",LOCH_GLOW44:"🌊✨"'
A10_NEW = 'CHANNEL_GLOW44:"🌊✨",STRAIT_GLOW44:"⚓✨",FIRTH_GLOW44:"🌊✨",SOUND_GLOW44:"🎵✨",LOCH_GLOW44:"🌊✨"'
cnt10 = src.count(A10_OLD)
assert cnt10 == 2, f"S10 anchor count={cnt10}"
src = src.replace(A10_OLD, A10_NEW)

# ── Write & report ────────────────────────────────────────────────────────────
open(F, "w", encoding="utf-8").write(src)
print(f"Batch 785 done! +{len(src)-orig_len} bytes")
