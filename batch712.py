#!/usr/bin/env python3
"""Batch 712: FIRE_GLOW43+ICE_GLOW43 + WaveliteFox9e+WebsteriteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"wagnerite_orb9e_peak", label:"Wagnerite Orb Peak", desc:"Reach peak with Wagnerite Orb", icon:"🍑", xp:120 },'
A1_NEW = (
    '{ id:"wagnerite_orb9e_peak", label:"Wagnerite Orb Peak", desc:"Reach peak with Wagnerite Orb", icon:"🍑", xp:120 },\n'
    '  { id:"fire_glow43_use", label:"Fire Glow 43", desc:"Activate FIRE_GLOW43 power-up", icon:"🔥", xp:60 },\n'
    '  { id:"fire_glow43_max", label:"Fire Glower 43", desc:"Reach max with FIRE_GLOW43 active", icon:"🔥", xp:120 },\n'
    '  { id:"ice_glow43_use", label:"Ice Glow 43", desc:"Activate ICE_GLOW43 power-up", icon:"❄️", xp:60 },\n'
    '  { id:"ice_glow43_max", label:"Ice Glower 43", desc:"Reach max with ICE_GLOW43 active", icon:"❄️", xp:120 },\n'
    '  { id:"wavelite_fox9e_tap", label:"Wavelite Fox", desc:"Tap a Wavelite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"wavelite_fox9e_peak", label:"Wavelite Fox Peak", desc:"Reach peak with Wavelite Fox", icon:"🌊", xp:120 },\n'
    '  { id:"websterite_orb9e_tap", label:"Websterite Orb", desc:"Tap a Websterite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"websterite_orb9e_peak", label:"Websterite Orb Peak", desc:"Reach peak with Websterite Orb", icon:"🩵", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"DAWN_GLOW43","DUSK_GLOW43","STAR_GLOW43","MOON_GLOW43"'
A2_NEW = '"FIRE_GLOW43","ICE_GLOW43","DAWN_GLOW43","DUSK_GLOW43","STAR_GLOW43","MOON_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="DAWN_GLOW43"){\n'
          '        gs.score+=2308;showPopup(cx,cy-2018,"+2308 🌅",theme.accent,26);spawnShockwave(cx,cy,"#ea580c",2180);if(gs.score>=bonusTotal)unlock("dawn_glow43_max");')
A3_NEW = ('  } else if(ptype==="FIRE_GLOW43"){\n'
          '        gs.score+=2312;showPopup(cx,cy-2022,"+2312 🔥",theme.accent,26);spawnShockwave(cx,cy,"#b91c1c",2184);if(gs.score>=bonusTotal)unlock("fire_glow43_max");\n'
          '      } else if(ptype==="ICE_GLOW43"){\n'
          '        gs.score+=2314;showPopup(cx,cy-2024,"+2314 ❄️",theme.accent,26);spawnShockwave(cx,cy,"#0891b2",2186);if(gs.score>=bonusTotal)unlock("ice_glow43_max");\n'
          '      } else if(ptype==="DAWN_GLOW43"){\n'
          '        gs.score+=2308;showPopup(cx,cy-2018,"+2308 🌅",theme.accent,26);spawnShockwave(cx,cy,"#ea580c",2180);if(gs.score>=bonusTotal)unlock("dawn_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // DAWN_GLOW43 — +2308 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW43"){sfx("powerUp",1971);unlock("dawn_glow43_use");}')
A4_NEW = ('  // FIRE_GLOW43 — +2312 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW43"){sfx("powerUp",1975);unlock("fire_glow43_use");}\n'
          '  // ICE_GLOW43 — +2314 ice glow bonus\n'
          '      if(ptype==="ICE_GLOW43"){sfx("powerUp",1977);unlock("ice_glow43_use");}\n'
          '  // DAWN_GLOW43 — +2308 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW43"){sfx("powerUp",1971);unlock("dawn_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawVrbaiteFox9e('
A5_NEW = (
    'function drawWaveliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4021)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.45+sp*0.35,"#0284c7");g.addColorStop(1,"#0c4a6e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(2,132,199,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0c4a6e":"#e0f2fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌊":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawWebsteriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4025);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.35+tp*0.35,"#38bdf8");g.addColorStop(1,"#0369a1");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(56,189,248,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(56,189,248,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#38bdf8":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🩵":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVrbaiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="vrbaite_fox9e"){'
A6_NEW = (
    'else if(t.type==="wavelite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2158);\n'
    '    drawWaveliteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="websterite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2160);\n'
    '    drawWebsteriteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="vrbaite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="vrbaite_fox9e"){'
A7_NEW = (
    'if(hit.type==="wavelite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2158);\n'
    '      const pts=Math.round(408*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#0284c7",2158);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌊","#e0f2fe",22);\n'
    '      unlock("wavelite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("wavelite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="websterite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2160);\n'
    '      const pts=Math.round(403*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#38bdf8",2160);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🩵","#f0f9ff",22);\n'
    '      unlock("websterite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("websterite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="vrbaite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="vrbaite_fox9e";color="#db2777";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wagnerite_orb9e"')
A8_NEW = ('      type="wavelite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="websterite_orb9e";color="#38bdf8";glow="#f0f9ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vrbaite_fox9e";color="#db2777";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wagnerite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="vrbaite_fox9e"?BASE_R*1.56:type==="wagnerite_orb9e"?BASE_R*1.55:'
A9_NEW = 'type==="wavelite_fox9e"?BASE_R*1.57:type==="websterite_orb9e"?BASE_R*1.56:type==="vrbaite_fox9e"?BASE_R*1.56:type==="wagnerite_orb9e"?BASE_R*1.55:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'DAWN_GLOW43:"🌅✨",DUSK_GLOW43:"🌇✨",STAR_GLOW43:"⭐✨"'
A10_NEW = 'FIRE_GLOW43:"🔥✨",ICE_GLOW43:"❄️✨",DAWN_GLOW43:"🌅✨",DUSK_GLOW43:"🌇✨",STAR_GLOW43:"⭐✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 712 done! +{len(code)-ORIG} bytes")
