#!/usr/bin/env python3
"""Batch 703: WIND_GLOW42+STORM_GLOW42 + TephroiteFox9e+TeschemacheriteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"tenorite_orb9e_peak", label:"Tenorite Orb Peak", desc:"Reach peak with Tenorite Orb", icon:"⬛", xp:120 },'
A1_NEW = (
    '{ id:"tenorite_orb9e_peak", label:"Tenorite Orb Peak", desc:"Reach peak with Tenorite Orb", icon:"⬛", xp:120 },\n'
    '  { id:"wind_glow42_use", label:"Wind Glow 42", desc:"Activate WIND_GLOW42 power-up", icon:"💨", xp:60 },\n'
    '  { id:"wind_glow42_max", label:"Wind Glower 42", desc:"Reach max with WIND_GLOW42 active", icon:"💨", xp:120 },\n'
    '  { id:"storm_glow42_use", label:"Storm Glow 42", desc:"Activate STORM_GLOW42 power-up", icon:"⛈️", xp:60 },\n'
    '  { id:"storm_glow42_max", label:"Storm Glower 42", desc:"Reach max with STORM_GLOW42 active", icon:"⛈️", xp:120 },\n'
    '  { id:"tephroite_fox9e_tap", label:"Tephroite Fox", desc:"Tap a Tephroite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"tephroite_fox9e_peak", label:"Tephroite Fox Peak", desc:"Reach peak with Tephroite Fox", icon:"🍇", xp:120 },\n'
    '  { id:"teschemacherite_orb9e_tap", label:"Teschemacherite Orb", desc:"Tap a Teschemacherite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"teschemacherite_orb9e_peak", label:"Teschemacherite Orb Peak", desc:"Reach peak with Teschemacherite Orb", icon:"🟣", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="FIRE_GLOW42"){\n'
          '        gs.score+=2272;showPopup(cx,cy-1982,"+2272 🔥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2144);if(gs.score>=bonusTotal)unlock("fire_glow42_max");')
A3_NEW = ('  } else if(ptype==="WIND_GLOW42"){\n'
          '        gs.score+=2276;showPopup(cx,cy-1986,"+2276 💨",theme.accent,26);spawnShockwave(cx,cy,"#a3e635",2148);if(gs.score>=bonusTotal)unlock("wind_glow42_max");\n'
          '      } else if(ptype==="STORM_GLOW42"){\n'
          '        gs.score+=2278;showPopup(cx,cy-1988,"+2278 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#6366f1",2150);if(gs.score>=bonusTotal)unlock("storm_glow42_max");\n'
          '      } else if(ptype==="FIRE_GLOW42"){\n'
          '        gs.score+=2272;showPopup(cx,cy-1982,"+2272 🔥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2144);if(gs.score>=bonusTotal)unlock("fire_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // FIRE_GLOW42 — +2272 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW42"){sfx("powerUp",1935);unlock("fire_glow42_use");}')
A4_NEW = ('  // WIND_GLOW42 — +2276 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW42"){sfx("powerUp",1939);unlock("wind_glow42_use");}\n'
          '  // STORM_GLOW42 — +2278 storm glow bonus\n'
          '      if(ptype==="STORM_GLOW42"){sfx("powerUp",1941);unlock("storm_glow42_use");}\n'
          '  // FIRE_GLOW42 — +2272 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW42"){sfx("powerUp",1935);unlock("fire_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawTelluriteFox9e('
A5_NEW = (
    'function drawTephroiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3958)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f5d0fe");g.addColorStop(0.45+sp*0.35,"#a855f7");g.addColorStop(1,"#6b21a8");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(168,85,247,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#6b21a8":"#f5d0fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🍇":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTeschemacheriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3962);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ede9fe");g.addColorStop(0.35+tp*0.35,"#7c3aed");g.addColorStop(1,"#4c1d95");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(124,58,237,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(124,58,237,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#7c3aed":"#ede9fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟣":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTelluriteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="tellurite_fox9e"){'
A6_NEW = (
    'else if(t.type==="tephroite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2122);\n'
    '    drawTephroiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="teschemacherite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2124);\n'
    '    drawTeschemacheriteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="tellurite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="tellurite_fox9e"){'
A7_NEW = (
    'if(hit.type==="tephroite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2122);\n'
    '      const pts=Math.round(390*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#a855f7",2122);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🍇","#f5d0fe",22);\n'
    '      unlock("tephroite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("tephroite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="teschemacherite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2124);\n'
    '      const pts=Math.round(385*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#7c3aed",2124);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🟣","#ede9fe",22);\n'
    '      unlock("teschemacherite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("teschemacherite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tellurite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="tellurite_fox9e";color="#475569";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tenorite_orb9e"')
A8_NEW = ('      type="tephroite_fox9e";color="#a855f7";glow="#f5d0fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="teschemacherite_orb9e";color="#7c3aed";glow="#ede9fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tellurite_fox9e";color="#475569";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tenorite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="tellurite_fox9e"?BASE_R*1.47:type==="tenorite_orb9e"?BASE_R*1.46:'
A9_NEW = 'type==="tephroite_fox9e"?BASE_R*1.48:type==="teschemacherite_orb9e"?BASE_R*1.47:type==="tellurite_fox9e"?BASE_R*1.47:type==="tenorite_orb9e"?BASE_R*1.46:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 703 done! +{len(code)-ORIG} bytes")
