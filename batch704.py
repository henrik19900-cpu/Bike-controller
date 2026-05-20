#!/usr/bin/env python3
"""Batch 704: LIGHT_GLOW42+DARK_GLOW42 + ThaumasiteFox9e+ThoriteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"teschemacherite_orb9e_peak", label:"Teschemacherite Orb Peak", desc:"Reach peak with Teschemacherite Orb", icon:"🟣", xp:120 },'
A1_NEW = (
    '{ id:"teschemacherite_orb9e_peak", label:"Teschemacherite Orb Peak", desc:"Reach peak with Teschemacherite Orb", icon:"🟣", xp:120 },\n'
    '  { id:"light_glow42_use", label:"Light Glow 42", desc:"Activate LIGHT_GLOW42 power-up", icon:"💡", xp:60 },\n'
    '  { id:"light_glow42_max", label:"Light Glower 42", desc:"Reach max with LIGHT_GLOW42 active", icon:"💡", xp:120 },\n'
    '  { id:"dark_glow42_use", label:"Dark Glow 42", desc:"Activate DARK_GLOW42 power-up", icon:"🌑", xp:60 },\n'
    '  { id:"dark_glow42_max", label:"Dark Glower 42", desc:"Reach max with DARK_GLOW42 active", icon:"🌑", xp:120 },\n'
    '  { id:"thaumasite_fox9e_tap", label:"Thaumasite Fox", desc:"Tap a Thaumasite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"thaumasite_fox9e_peak", label:"Thaumasite Fox Peak", desc:"Reach peak with Thaumasite Fox", icon:"🌿", xp:120 },\n'
    '  { id:"thorite_orb9e_tap", label:"Thorite Orb", desc:"Tap a Thorite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"thorite_orb9e_peak", label:"Thorite Orb Peak", desc:"Reach peak with Thorite Orb", icon:"🟡", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="WIND_GLOW42"){\n'
          '        gs.score+=2276;showPopup(cx,cy-1986,"+2276 💨",theme.accent,26);spawnShockwave(cx,cy,"#a3e635",2148);if(gs.score>=bonusTotal)unlock("wind_glow42_max");')
A3_NEW = ('  } else if(ptype==="LIGHT_GLOW42"){\n'
          '        gs.score+=2280;showPopup(cx,cy-1990,"+2280 💡",theme.accent,26);spawnShockwave(cx,cy,"#fde047",2152);if(gs.score>=bonusTotal)unlock("light_glow42_max");\n'
          '      } else if(ptype==="DARK_GLOW42"){\n'
          '        gs.score+=2282;showPopup(cx,cy-1992,"+2282 🌑",theme.accent,26);spawnShockwave(cx,cy,"#1e1b4b",2154);if(gs.score>=bonusTotal)unlock("dark_glow42_max");\n'
          '      } else if(ptype==="WIND_GLOW42"){\n'
          '        gs.score+=2276;showPopup(cx,cy-1986,"+2276 💨",theme.accent,26);spawnShockwave(cx,cy,"#a3e635",2148);if(gs.score>=bonusTotal)unlock("wind_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // WIND_GLOW42 — +2276 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW42"){sfx("powerUp",1939);unlock("wind_glow42_use");}')
A4_NEW = ('  // LIGHT_GLOW42 — +2280 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW42"){sfx("powerUp",1943);unlock("light_glow42_use");}\n'
          '  // DARK_GLOW42 — +2282 dark glow bonus\n'
          '      if(ptype==="DARK_GLOW42"){sfx("powerUp",1945);unlock("dark_glow42_use");}\n'
          '  // WIND_GLOW42 — +2276 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW42"){sfx("powerUp",1939);unlock("wind_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawTephroiteFox9e('
A5_NEW = (
    'function drawThaumasiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3965)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d1fae5");g.addColorStop(0.45+sp*0.35,"#059669");g.addColorStop(1,"#064e3b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(5,150,105,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#064e3b":"#d1fae5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌿":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawThoriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3969);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+tp*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(234,179,8,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(234,179,8,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#eab308":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟡":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTephroiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="tephroite_fox9e"){'
A6_NEW = (
    'else if(t.type==="thaumasite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2126);\n'
    '    drawThaumasiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="thorite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2128);\n'
    '    drawThoriteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="tephroite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="tephroite_fox9e"){'
A7_NEW = (
    'if(hit.type==="thaumasite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2126);\n'
    '      const pts=Math.round(392*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#059669",2126);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌿","#d1fae5",22);\n'
    '      unlock("thaumasite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("thaumasite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="thorite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2128);\n'
    '      const pts=Math.round(387*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#eab308",2128);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🟡","#fef9c3",22);\n'
    '      unlock("thorite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("thorite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tephroite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="tephroite_fox9e";color="#a855f7";glow="#f5d0fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="teschemacherite_orb9e"')
A8_NEW = ('      type="thaumasite_fox9e";color="#059669";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="thorite_orb9e";color="#eab308";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tephroite_fox9e";color="#a855f7";glow="#f5d0fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="teschemacherite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="tephroite_fox9e"?BASE_R*1.48:type==="teschemacherite_orb9e"?BASE_R*1.47:'
A9_NEW = 'type==="thaumasite_fox9e"?BASE_R*1.49:type==="thorite_orb9e"?BASE_R*1.48:type==="tephroite_fox9e"?BASE_R*1.48:type==="teschemacherite_orb9e"?BASE_R*1.47:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 704 done! +{len(code)-ORIG} bytes")
