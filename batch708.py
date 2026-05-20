#!/usr/bin/env python3
"""Batch 708: PRISM_GLOW43+CRYSTAL_GLOW43 + VarisciteFox9e+VesuvianiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"tugtupite_orb9e_peak", label:"Tugtupite Orb Peak", desc:"Reach peak with Tugtupite Orb", icon:"❤️", xp:120 },'
A1_NEW = (
    '{ id:"tugtupite_orb9e_peak", label:"Tugtupite Orb Peak", desc:"Reach peak with Tugtupite Orb", icon:"❤️", xp:120 },\n'
    '  { id:"prism_glow43_use", label:"Prism Glow 43", desc:"Activate PRISM_GLOW43 power-up", icon:"🔷", xp:60 },\n'
    '  { id:"prism_glow43_max", label:"Prism Glower 43", desc:"Reach max with PRISM_GLOW43 active", icon:"🔷", xp:120 },\n'
    '  { id:"crystal_glow43_use", label:"Crystal Glow 43", desc:"Activate CRYSTAL_GLOW43 power-up", icon:"💎", xp:60 },\n'
    '  { id:"crystal_glow43_max", label:"Crystal Glower 43", desc:"Reach max with CRYSTAL_GLOW43 active", icon:"💎", xp:120 },\n'
    '  { id:"variscite_fox9e_tap", label:"Variscite Fox", desc:"Tap a Variscite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"variscite_fox9e_peak", label:"Variscite Fox Peak", desc:"Reach peak with Variscite Fox", icon:"🌱", xp:120 },\n'
    '  { id:"vesuvianite_orb9e_tap", label:"Vesuvianite Orb", desc:"Tap a Vesuvianite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"vesuvianite_orb9e_peak", label:"Vesuvianite Orb Peak", desc:"Reach peak with Vesuvianite Orb", icon:"🫐", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"NEBULA_GLOW42","AURORA_GLOW42","COSMIC_GLOW42","VOID_GLOW42","SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"PRISM_GLOW43","CRYSTAL_GLOW43","NEBULA_GLOW42","AURORA_GLOW42","COSMIC_GLOW42","VOID_GLOW42","SOLAR_GLOW42","LUNAR_GLOW42","LIGHT_GLOW42","DARK_GLOW42","WIND_GLOW42","STORM_GLOW42","FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="NEBULA_GLOW42"){\n'
          '        gs.score+=2292;showPopup(cx,cy-2002,"+2292 🌠",theme.accent,26);spawnShockwave(cx,cy,"#4f46e5",2164);if(gs.score>=bonusTotal)unlock("nebula_glow42_max");')
A3_NEW = ('  } else if(ptype==="PRISM_GLOW43"){\n'
          '        gs.score+=2296;showPopup(cx,cy-2006,"+2296 🔷",theme.accent,26);spawnShockwave(cx,cy,"#2563eb",2168);if(gs.score>=bonusTotal)unlock("prism_glow43_max");\n'
          '      } else if(ptype==="CRYSTAL_GLOW43"){\n'
          '        gs.score+=2298;showPopup(cx,cy-2008,"+2298 💎",theme.accent,26);spawnShockwave(cx,cy,"#0284c7",2170);if(gs.score>=bonusTotal)unlock("crystal_glow43_max");\n'
          '      } else if(ptype==="NEBULA_GLOW42"){\n'
          '        gs.score+=2292;showPopup(cx,cy-2002,"+2292 🌠",theme.accent,26);spawnShockwave(cx,cy,"#4f46e5",2164);if(gs.score>=bonusTotal)unlock("nebula_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // NEBULA_GLOW42 — +2292 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW42"){sfx("powerUp",1955);unlock("nebula_glow42_use");}')
A4_NEW = ('  // PRISM_GLOW43 — +2296 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW43"){sfx("powerUp",1959);unlock("prism_glow43_use");}\n'
          '  // CRYSTAL_GLOW43 — +2298 crystal glow bonus\n'
          '      if(ptype==="CRYSTAL_GLOW43"){sfx("powerUp",1961);unlock("crystal_glow43_use");}\n'
          '  // NEBULA_GLOW42 — +2292 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW42"){sfx("powerUp",1955);unlock("nebula_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawTsavoriteFox9e('
A5_NEW = (
    'function drawVarisciteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3993)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d1fae5");g.addColorStop(0.45+sp*0.35,"#34d399");g.addColorStop(1,"#064e3b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(52,211,153,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#064e3b":"#d1fae5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌱":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVesuvianiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3997);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ede9fe");g.addColorStop(0.35+tp*0.35,"#8b5cf6");g.addColorStop(1,"#3b0764");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(139,92,246,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(139,92,246,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#8b5cf6":"#ede9fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🫐":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTsavoriteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="tsavorite_fox9e"){'
A6_NEW = (
    'else if(t.type==="variscite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2142);\n'
    '    drawVarisciteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="vesuvianite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2144);\n'
    '    drawVesuvianiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="tsavorite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="tsavorite_fox9e"){'
A7_NEW = (
    'if(hit.type==="variscite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2142);\n'
    '      const pts=Math.round(400*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#34d399",2142);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌱","#d1fae5",22);\n'
    '      unlock("variscite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("variscite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="vesuvianite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2144);\n'
    '      const pts=Math.round(395*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#8b5cf6",2144);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🫐","#ede9fe",22);\n'
    '      unlock("vesuvianite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("vesuvianite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tsavorite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="tsavorite_fox9e";color="#22c55e";glow="#bbf7d0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tugtupite_orb9e"')
A8_NEW = ('      type="variscite_fox9e";color="#34d399";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vesuvianite_orb9e";color="#8b5cf6";glow="#ede9fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tsavorite_fox9e";color="#22c55e";glow="#bbf7d0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tugtupite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="tsavorite_fox9e"?BASE_R*1.52:type==="tugtupite_orb9e"?BASE_R*1.51:'
A9_NEW = 'type==="variscite_fox9e"?BASE_R*1.53:type==="vesuvianite_orb9e"?BASE_R*1.52:type==="tsavorite_fox9e"?BASE_R*1.52:type==="tugtupite_orb9e"?BASE_R*1.51:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'NEBULA_GLOW42:"🌠✨",AURORA_GLOW42:"🌌✨",COSMIC_GLOW42:"🌌✨",VOID_GLOW42:"🕳️✨",SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'PRISM_GLOW43:"🔷✨",CRYSTAL_GLOW43:"💎✨",NEBULA_GLOW42:"🌠✨",AURORA_GLOW42:"🌌✨",COSMIC_GLOW42:"🌌✨",VOID_GLOW42:"🕳️✨",SOLAR_GLOW42:"☀️✨",LUNAR_GLOW42:"🌕✨",LIGHT_GLOW42:"💡✨",DARK_GLOW42:"🌑✨",WIND_GLOW42:"💨✨",STORM_GLOW42:"⛈️✨",FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 708 done! +{len(code)-ORIG} bytes")
