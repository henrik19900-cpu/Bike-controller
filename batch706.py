#!/usr/bin/env python3
"""Batch 706: COSMIC_GLOW42+VOID_GLOW42 + TorberninteFox9e+TroiliteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"triplite_orb9e_peak", label:"Triplite Orb Peak", desc:"Reach peak with Triplite Orb", icon:"🍊", xp:120 },'
A1_NEW = (
    '{ id:"triplite_orb9e_peak", label:"Triplite Orb Peak", desc:"Reach peak with Triplite Orb", icon:"🍊", xp:120 },\n'
    '  { id:"cosmic_glow42_use", label:"Cosmic Glow 42", desc:"Activate COSMIC_GLOW42 power-up", icon:"🌌", xp:60 },\n'
    '  { id:"cosmic_glow42_max", label:"Cosmic Glower 42", desc:"Reach max with COSMIC_GLOW42 active", icon:"🌌", xp:120 },\n'
    '  { id:"void_glow42_use", label:"Void Glow 42", desc:"Activate VOID_GLOW42 power-up", icon:"🕳️", xp:60 },\n'
    '  { id:"void_glow42_max", label:"Void Glower 42", desc:"Reach max with VOID_GLOW42 active", icon:"🕳️", xp:120 },\n'
    '  { id:"torbernite_fox9e_tap", label:"Torbernite Fox", desc:"Tap a Torbernite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"torbernite_fox9e_peak", label:"Torbernite Fox Peak", desc:"Reach peak with Torbernite Fox", icon:"☢️", xp:120 },\n'
    '  { id:"troilite_orb9e_tap", label:"Troilite Orb", desc:"Tap a Troilite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"troilite_orb9e_peak", label:"Troilite Orb Peak", desc:"Reach peak with Troilite Orb", icon:"🩶", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"COSMIC_GLOW42","VOID_GLOW42","SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="SOLAR_GLOW42"){\n'
          '        gs.score+=2284;showPopup(cx,cy-1994,"+2284 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#f59e0b",2156);if(gs.score>=bonusTotal)unlock("solar_glow42_max");')
A3_NEW = ('  } else if(ptype==="COSMIC_GLOW42"){\n'
          '        gs.score+=2288;showPopup(cx,cy-1998,"+2288 🌌",theme.accent,26);spawnShockwave(cx,cy,"#312e81",2160);if(gs.score>=bonusTotal)unlock("cosmic_glow42_max");\n'
          '      } else if(ptype==="VOID_GLOW42"){\n'
          '        gs.score+=2290;showPopup(cx,cy-2000,"+2290 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0c0a09",2162);if(gs.score>=bonusTotal)unlock("void_glow42_max");\n'
          '      } else if(ptype==="SOLAR_GLOW42"){\n'
          '        gs.score+=2284;showPopup(cx,cy-1994,"+2284 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#f59e0b",2156);if(gs.score>=bonusTotal)unlock("solar_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // SOLAR_GLOW42 — +2284 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW42"){sfx("powerUp",1947);unlock("solar_glow42_use");}')
A4_NEW = ('  // COSMIC_GLOW42 — +2288 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW42"){sfx("powerUp",1951);unlock("cosmic_glow42_use");}\n'
          '  // VOID_GLOW42 — +2290 void glow bonus\n'
          '      if(ptype==="VOID_GLOW42"){sfx("powerUp",1953);unlock("void_glow42_use");}\n'
          '  // SOLAR_GLOW42 — +2284 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW42"){sfx("powerUp",1947);unlock("solar_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawThuliteFox9e('
A5_NEW = (
    'function drawTorberninteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3979)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d1fae5");g.addColorStop(0.45+sp*0.35,"#10b981");g.addColorStop(1,"#064e3b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(16,185,129,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#064e3b":"#d1fae5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"☢️":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTroiliteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3983);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.35+tp*0.35,"#64748b");g.addColorStop(1,"#0f172a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(100,116,139,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(100,116,139,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#64748b":"#f1f5f9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🩶":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawThuliteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="thulite_fox9e"){'
A6_NEW = (
    'else if(t.type==="torbernite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2134);\n'
    '    drawTorberninteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="troilite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2136);\n'
    '    drawTroiliteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="thulite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="thulite_fox9e"){'
A7_NEW = (
    'if(hit.type==="torbernite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2134);\n'
    '      const pts=Math.round(396*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#10b981",2134);\n'
    '      showPopup(cx,cy-38,"+"+pts+" ☢️","#d1fae5",22);\n'
    '      unlock("torbernite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("torbernite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="troilite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2136);\n'
    '      const pts=Math.round(391*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#64748b",2136);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🩶","#f1f5f9",22);\n'
    '      unlock("troilite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("troilite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="thulite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="thulite_fox9e";color="#ec4899";glow="#fce7f3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="triplite_orb9e"')
A8_NEW = ('      type="torbernite_fox9e";color="#10b981";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="troilite_orb9e";color="#64748b";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="thulite_fox9e";color="#ec4899";glow="#fce7f3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="triplite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="thulite_fox9e"?BASE_R*1.50:type==="triplite_orb9e"?BASE_R*1.49:'
A9_NEW = 'type==="torbernite_fox9e"?BASE_R*1.51:type==="troilite_orb9e"?BASE_R*1.50:type==="thulite_fox9e"?BASE_R*1.50:type==="triplite_orb9e"?BASE_R*1.49:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'COSMIC_GLOW42:"🌌✨",VOID_GLOW42:"🕳️✨",SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 706 done! +{len(code)-ORIG} bytes")
