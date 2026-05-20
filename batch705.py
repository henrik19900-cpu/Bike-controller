#!/usr/bin/env python3
"""Batch 705: SOLAR_GLOW42+LUNAR_GLOW42 + ThuliteFox9e+TripliteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"thorite_orb9e_peak", label:"Thorite Orb Peak", desc:"Reach peak with Thorite Orb", icon:"🟡", xp:120 },'
A1_NEW = (
    '{ id:"thorite_orb9e_peak", label:"Thorite Orb Peak", desc:"Reach peak with Thorite Orb", icon:"🟡", xp:120 },\n'
    '  { id:"solar_glow42_use", label:"Solar Glow 42", desc:"Activate SOLAR_GLOW42 power-up", icon:"☀️", xp:60 },\n'
    '  { id:"solar_glow42_max", label:"Solar Glower 42", desc:"Reach max with SOLAR_GLOW42 active", icon:"☀️", xp:120 },\n'
    '  { id:"lunar_glow42_use", label:"Lunar Glow 42", desc:"Activate LUNAR_GLOW42 power-up", icon:"🌕", xp:60 },\n'
    '  { id:"lunar_glow42_max", label:"Lunar Glower 42", desc:"Reach max with LUNAR_GLOW42 active", icon:"🌕", xp:120 },\n'
    '  { id:"thulite_fox9e_tap", label:"Thulite Fox", desc:"Tap a Thulite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"thulite_fox9e_peak", label:"Thulite Fox Peak", desc:"Reach peak with Thulite Fox", icon:"🌹", xp:120 },\n'
    '  { id:"triplite_orb9e_tap", label:"Triplite Orb", desc:"Tap a Triplite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"triplite_orb9e_peak", label:"Triplite Orb Peak", desc:"Reach peak with Triplite Orb", icon:"🍊", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="LIGHT_GLOW42"){\n'
          '        gs.score+=2280;showPopup(cx,cy-1990,"+2280 💡",theme.accent,26);spawnShockwave(cx,cy,"#fde047",2152);if(gs.score>=bonusTotal)unlock("light_glow42_max");')
A3_NEW = ('  } else if(ptype==="SOLAR_GLOW42"){\n'
          '        gs.score+=2284;showPopup(cx,cy-1994,"+2284 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#f59e0b",2156);if(gs.score>=bonusTotal)unlock("solar_glow42_max");\n'
          '      } else if(ptype==="LUNAR_GLOW42"){\n'
          '        gs.score+=2286;showPopup(cx,cy-1996,"+2286 🌕",theme.accent,26);spawnShockwave(cx,cy,"#d1d5db",2158);if(gs.score>=bonusTotal)unlock("lunar_glow42_max");\n'
          '      } else if(ptype==="LIGHT_GLOW42"){\n'
          '        gs.score+=2280;showPopup(cx,cy-1990,"+2280 💡",theme.accent,26);spawnShockwave(cx,cy,"#fde047",2152);if(gs.score>=bonusTotal)unlock("light_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // LIGHT_GLOW42 — +2280 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW42"){sfx("powerUp",1943);unlock("light_glow42_use");}')
A4_NEW = ('  // SOLAR_GLOW42 — +2284 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW42"){sfx("powerUp",1947);unlock("solar_glow42_use");}\n'
          '  // LUNAR_GLOW42 — +2286 lunar glow bonus\n'
          '      if(ptype==="LUNAR_GLOW42"){sfx("powerUp",1949);unlock("lunar_glow42_use");}\n'
          '  // LIGHT_GLOW42 — +2280 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW42"){sfx("powerUp",1943);unlock("light_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawThaumasiteFox9e('
A5_NEW = (
    'function drawThuliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3972)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fce7f3");g.addColorStop(0.45+sp*0.35,"#ec4899");g.addColorStop(1,"#831843");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(236,72,153,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#831843":"#fce7f3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌹":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTripliteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3976);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffedd5");g.addColorStop(0.35+tp*0.35,"#f97316");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(249,115,22,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(249,115,22,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#f97316":"#ffedd5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🍊":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawThaumasiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="thaumasite_fox9e"){'
A6_NEW = (
    'else if(t.type==="thulite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2130);\n'
    '    drawThuliteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="triplite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2132);\n'
    '    drawTripliteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="thaumasite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="thaumasite_fox9e"){'
A7_NEW = (
    'if(hit.type==="thulite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2130);\n'
    '      const pts=Math.round(394*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#ec4899",2130);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌹","#fce7f3",22);\n'
    '      unlock("thulite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("thulite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="triplite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2132);\n'
    '      const pts=Math.round(389*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#f97316",2132);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🍊","#ffedd5",22);\n'
    '      unlock("triplite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("triplite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="thaumasite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="thaumasite_fox9e";color="#059669";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="thorite_orb9e"')
A8_NEW = ('      type="thulite_fox9e";color="#ec4899";glow="#fce7f3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="triplite_orb9e";color="#f97316";glow="#ffedd5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="thaumasite_fox9e";color="#059669";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="thorite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="thaumasite_fox9e"?BASE_R*1.49:type==="thorite_orb9e"?BASE_R*1.48:'
A9_NEW = 'type==="thulite_fox9e"?BASE_R*1.50:type==="triplite_orb9e"?BASE_R*1.49:type==="thaumasite_fox9e"?BASE_R*1.49:type==="thorite_orb9e"?BASE_R*1.48:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 705 done! +{len(code)-ORIG} bytes")
