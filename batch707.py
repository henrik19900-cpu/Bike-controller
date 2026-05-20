#!/usr/bin/env python3
"""Batch 707: NEBULA_GLOW42+AURORA_GLOW42 + TsavoriteFox9e+TugtupiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"troilite_orb9e_peak", label:"Troilite Orb Peak", desc:"Reach peak with Troilite Orb", icon:"🩶", xp:120 },'
A1_NEW = (
    '{ id:"troilite_orb9e_peak", label:"Troilite Orb Peak", desc:"Reach peak with Troilite Orb", icon:"🩶", xp:120 },\n'
    '  { id:"nebula_glow42_use", label:"Nebula Glow 42", desc:"Activate NEBULA_GLOW42 power-up", icon:"🌠", xp:60 },\n'
    '  { id:"nebula_glow42_max", label:"Nebula Glower 42", desc:"Reach max with NEBULA_GLOW42 active", icon:"🌠", xp:120 },\n'
    '  { id:"aurora_glow42_use", label:"Aurora Glow 42", desc:"Activate AURORA_GLOW42 power-up", icon:"🌌", xp:60 },\n'
    '  { id:"aurora_glow42_max", label:"Aurora Glower 42", desc:"Reach max with AURORA_GLOW42 active", icon:"🌌", xp:120 },\n'
    '  { id:"tsavorite_fox9e_tap", label:"Tsavorite Fox", desc:"Tap a Tsavorite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"tsavorite_fox9e_peak", label:"Tsavorite Fox Peak", desc:"Reach peak with Tsavorite Fox", icon:"💚", xp:120 },\n'
    '  { id:"tugtupite_orb9e_tap", label:"Tugtupite Orb", desc:"Tap a Tugtupite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"tugtupite_orb9e_peak", label:"Tugtupite Orb Peak", desc:"Reach peak with Tugtupite Orb", icon:"❤️", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"COSMIC_GLOW42","VOID_GLOW42","SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"NEBULA_GLOW42","AURORA_GLOW42","COSMIC_GLOW42","VOID_GLOW42","SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="COSMIC_GLOW42"){\n'
          '        gs.score+=2288;showPopup(cx,cy-1998,"+2288 🌌",theme.accent,26);spawnShockwave(cx,cy,"#312e81",2160);if(gs.score>=bonusTotal)unlock("cosmic_glow42_max");')
A3_NEW = ('  } else if(ptype==="NEBULA_GLOW42"){\n'
          '        gs.score+=2292;showPopup(cx,cy-2002,"+2292 🌠",theme.accent,26);spawnShockwave(cx,cy,"#4f46e5",2164);if(gs.score>=bonusTotal)unlock("nebula_glow42_max");\n'
          '      } else if(ptype==="AURORA_GLOW42"){\n'
          '        gs.score+=2294;showPopup(cx,cy-2004,"+2294 🌌",theme.accent,26);spawnShockwave(cx,cy,"#06b6d4",2166);if(gs.score>=bonusTotal)unlock("aurora_glow42_max");\n'
          '      } else if(ptype==="COSMIC_GLOW42"){\n'
          '        gs.score+=2288;showPopup(cx,cy-1998,"+2288 🌌",theme.accent,26);spawnShockwave(cx,cy,"#312e81",2160);if(gs.score>=bonusTotal)unlock("cosmic_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // COSMIC_GLOW42 — +2288 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW42"){sfx("powerUp",1951);unlock("cosmic_glow42_use");}')
A4_NEW = ('  // NEBULA_GLOW42 — +2292 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW42"){sfx("powerUp",1955);unlock("nebula_glow42_use");}\n'
          '  // AURORA_GLOW42 — +2294 aurora glow bonus\n'
          '      if(ptype==="AURORA_GLOW42"){sfx("powerUp",1957);unlock("aurora_glow42_use");}\n'
          '  // COSMIC_GLOW42 — +2288 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW42"){sfx("powerUp",1951);unlock("cosmic_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawTorberninteFox9e('
A5_NEW = (
    'function drawTsavoriteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3986)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bbf7d0");g.addColorStop(0.45+sp*0.35,"#22c55e");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(34,197,94,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#14532d":"#bbf7d0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"💚":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTugtupiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3990);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffe4e6");g.addColorStop(0.35+tp*0.35,"#f43f5e");g.addColorStop(1,"#881337");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(244,63,94,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(244,63,94,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#f43f5e":"#ffe4e6";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"❤️":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTorberninteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="torbernite_fox9e"){'
A6_NEW = (
    'else if(t.type==="tsavorite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2138);\n'
    '    drawTsavoriteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="tugtupite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2140);\n'
    '    drawTugtupiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="torbernite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="torbernite_fox9e"){'
A7_NEW = (
    'if(hit.type==="tsavorite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2138);\n'
    '      const pts=Math.round(398*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#22c55e",2138);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 💚","#bbf7d0",22);\n'
    '      unlock("tsavorite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("tsavorite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tugtupite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2140);\n'
    '      const pts=Math.round(393*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#f43f5e",2140);\n'
    '      showPopup(cx,cy-38,"+"+pts+" ❤️","#ffe4e6",22);\n'
    '      unlock("tugtupite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("tugtupite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="torbernite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="torbernite_fox9e";color="#10b981";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="troilite_orb9e"')
A8_NEW = ('      type="tsavorite_fox9e";color="#22c55e";glow="#bbf7d0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tugtupite_orb9e";color="#f43f5e";glow="#ffe4e6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="torbernite_fox9e";color="#10b981";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="troilite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="torbernite_fox9e"?BASE_R*1.51:type==="troilite_orb9e"?BASE_R*1.50:'
A9_NEW = 'type==="tsavorite_fox9e"?BASE_R*1.52:type==="tugtupite_orb9e"?BASE_R*1.51:type==="torbernite_fox9e"?BASE_R*1.51:type==="troilite_orb9e"?BASE_R*1.50:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'COSMIC_GLOW42:"🌌✨",VOID_GLOW42:"🕳️✨",SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'NEBULA_GLOW42:"🌠✨",AURORA_GLOW42:"🌌✨",COSMIC_GLOW42:"🌌✨",VOID_GLOW42:"🕳️✨",SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 707 done! +{len(code)-ORIG} bytes")
