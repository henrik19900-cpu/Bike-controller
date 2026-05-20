#!/usr/bin/env python3
"""Batch 713: WIND_GLOW43+STORM_GLOW43 + WitheriteFox9e+XanthiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"websterite_orb9e_peak", label:"Websterite Orb Peak", desc:"Reach peak with Websterite Orb", icon:"🩵", xp:120 },'
A1_NEW = (
    '{ id:"websterite_orb9e_peak", label:"Websterite Orb Peak", desc:"Reach peak with Websterite Orb", icon:"🩵", xp:120 },\n'
    '  { id:"wind_glow43_use", label:"Wind Glow 43", desc:"Activate WIND_GLOW43 power-up", icon:"💨", xp:60 },\n'
    '  { id:"wind_glow43_max", label:"Wind Glower 43", desc:"Reach max with WIND_GLOW43 active", icon:"💨", xp:120 },\n'
    '  { id:"storm_glow43_use", label:"Storm Glow 43", desc:"Activate STORM_GLOW43 power-up", icon:"⛈️", xp:60 },\n'
    '  { id:"storm_glow43_max", label:"Storm Glower 43", desc:"Reach max with STORM_GLOW43 active", icon:"⛈️", xp:120 },\n'
    '  { id:"witherite_fox9e_tap", label:"Witherite Fox", desc:"Tap a Witherite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"witherite_fox9e_peak", label:"Witherite Fox Peak", desc:"Reach peak with Witherite Fox", icon:"🌨️", xp:120 },\n'
    '  { id:"xanthite_orb9e_tap", label:"Xanthite Orb", desc:"Tap a Xanthite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"xanthite_orb9e_peak", label:"Xanthite Orb Peak", desc:"Reach peak with Xanthite Orb", icon:"🌼", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"FIRE_GLOW43","ICE_GLOW43","DAWN_GLOW43","DUSK_GLOW43"'
A2_NEW = '"WIND_GLOW43","STORM_GLOW43","FIRE_GLOW43","ICE_GLOW43","DAWN_GLOW43","DUSK_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="FIRE_GLOW43"){\n'
          '        gs.score+=2312;showPopup(cx,cy-2022,"+2312 🔥",theme.accent,26);spawnShockwave(cx,cy,"#b91c1c",2184);if(gs.score>=bonusTotal)unlock("fire_glow43_max");')
A3_NEW = ('  } else if(ptype==="WIND_GLOW43"){\n'
          '        gs.score+=2316;showPopup(cx,cy-2026,"+2316 💨",theme.accent,26);spawnShockwave(cx,cy,"#84cc16",2188);if(gs.score>=bonusTotal)unlock("wind_glow43_max");\n'
          '      } else if(ptype==="STORM_GLOW43"){\n'
          '        gs.score+=2318;showPopup(cx,cy-2028,"+2318 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#4f46e5",2190);if(gs.score>=bonusTotal)unlock("storm_glow43_max");\n'
          '      } else if(ptype==="FIRE_GLOW43"){\n'
          '        gs.score+=2312;showPopup(cx,cy-2022,"+2312 🔥",theme.accent,26);spawnShockwave(cx,cy,"#b91c1c",2184);if(gs.score>=bonusTotal)unlock("fire_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // FIRE_GLOW43 — +2312 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW43"){sfx("powerUp",1975);unlock("fire_glow43_use");}')
A4_NEW = ('  // WIND_GLOW43 — +2316 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW43"){sfx("powerUp",1979);unlock("wind_glow43_use");}\n'
          '  // STORM_GLOW43 — +2318 storm glow bonus\n'
          '      if(ptype==="STORM_GLOW43"){sfx("powerUp",1981);unlock("storm_glow43_use");}\n'
          '  // FIRE_GLOW43 — +2312 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW43"){sfx("powerUp",1975);unlock("fire_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawWaveliteFox9e('
A5_NEW = (
    'function drawWitheriteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4028)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+sp*0.35,"#94a3b8");g.addColorStop(1,"#1e293b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#1e293b":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌨️":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawXanthiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4032);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+tp*0.35,"#facc15");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(250,204,21,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(250,204,21,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#facc15":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌼":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawWaveliteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="wavelite_fox9e"){'
A6_NEW = (
    'else if(t.type==="witherite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2162);\n'
    '    drawWitheriteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="xanthite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2164);\n'
    '    drawXanthiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="wavelite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="wavelite_fox9e"){'
A7_NEW = (
    'if(hit.type==="witherite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2162);\n'
    '      const pts=Math.round(410*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#94a3b8",2162);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌨️","#f8fafc",22);\n'
    '      unlock("witherite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("witherite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="xanthite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2164);\n'
    '      const pts=Math.round(405*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#facc15",2164);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌼","#fefce8",22);\n'
    '      unlock("xanthite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("xanthite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="wavelite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="wavelite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="websterite_orb9e"')
A8_NEW = ('      type="witherite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="xanthite_orb9e";color="#facc15";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wavelite_fox9e";color="#0284c7";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="websterite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="wavelite_fox9e"?BASE_R*1.57:type==="websterite_orb9e"?BASE_R*1.56:'
A9_NEW = 'type==="witherite_fox9e"?BASE_R*1.58:type==="xanthite_orb9e"?BASE_R*1.57:type==="wavelite_fox9e"?BASE_R*1.57:type==="websterite_orb9e"?BASE_R*1.56:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'FIRE_GLOW43:"🔥✨",ICE_GLOW43:"❄️✨",DAWN_GLOW43:"🌅✨"'
A10_NEW = 'WIND_GLOW43:"💨✨",STORM_GLOW43:"⛈️✨",FIRE_GLOW43:"🔥✨",ICE_GLOW43:"❄️✨",DAWN_GLOW43:"🌅✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 713 done! +{len(code)-ORIG} bytes")
