#!/usr/bin/env python3
"""Batch 715: SOLAR_GLOW43+LUNAR_GLOW43 + ZinkeniteFox9e+ZippeiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"zeunerite_orb9e_peak", label:"Zeunerite Orb Peak", desc:"Reach peak with Zeunerite Orb", icon:"💚", xp:120 },'
A1_NEW = (
    '{ id:"zeunerite_orb9e_peak", label:"Zeunerite Orb Peak", desc:"Reach peak with Zeunerite Orb", icon:"💚", xp:120 },\n'
    '  { id:"solar_glow43_use", label:"Solar Glow 43", desc:"Activate SOLAR_GLOW43 power-up", icon:"☀️", xp:60 },\n'
    '  { id:"solar_glow43_max", label:"Solar Glower 43", desc:"Reach max with SOLAR_GLOW43 active", icon:"☀️", xp:120 },\n'
    '  { id:"lunar_glow43_use", label:"Lunar Glow 43", desc:"Activate LUNAR_GLOW43 power-up", icon:"🌕", xp:60 },\n'
    '  { id:"lunar_glow43_max", label:"Lunar Glower 43", desc:"Reach max with LUNAR_GLOW43 active", icon:"🌕", xp:120 },\n'
    '  { id:"zinkenite_fox9e_tap", label:"Zinkenite Fox", desc:"Tap a Zinkenite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"zinkenite_fox9e_peak", label:"Zinkenite Fox Peak", desc:"Reach peak with Zinkenite Fox", icon:"🫧", xp:120 },\n'
    '  { id:"zippeite_orb9e_tap", label:"Zippeite Orb", desc:"Tap a Zippeite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"zippeite_orb9e_peak", label:"Zippeite Orb Peak", desc:"Reach peak with Zippeite Orb", icon:"🧡", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"LIGHT_GLOW43","DARK_GLOW43","WIND_GLOW43","STORM_GLOW43"'
A2_NEW = '"SOLAR_GLOW43","LUNAR_GLOW43","LIGHT_GLOW43","DARK_GLOW43","WIND_GLOW43","STORM_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="LIGHT_GLOW43"){\n'
          '        gs.score+=2320;showPopup(cx,cy-2030,"+2320 💡",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2192);if(gs.score>=bonusTotal)unlock("light_glow43_max");')
A3_NEW = ('  } else if(ptype==="SOLAR_GLOW43"){\n'
          '        gs.score+=2324;showPopup(cx,cy-2034,"+2324 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#d97706",2196);if(gs.score>=bonusTotal)unlock("solar_glow43_max");\n'
          '      } else if(ptype==="LUNAR_GLOW43"){\n'
          '        gs.score+=2326;showPopup(cx,cy-2036,"+2326 🌕",theme.accent,26);spawnShockwave(cx,cy,"#94a3b8",2198);if(gs.score>=bonusTotal)unlock("lunar_glow43_max");\n'
          '      } else if(ptype==="LIGHT_GLOW43"){\n'
          '        gs.score+=2320;showPopup(cx,cy-2030,"+2320 💡",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2192);if(gs.score>=bonusTotal)unlock("light_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // LIGHT_GLOW43 — +2320 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW43"){sfx("powerUp",1983);unlock("light_glow43_use");}')
A4_NEW = ('  // SOLAR_GLOW43 — +2324 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW43"){sfx("powerUp",1987);unlock("solar_glow43_use");}\n'
          '  // LUNAR_GLOW43 — +2326 lunar glow bonus\n'
          '      if(ptype==="LUNAR_GLOW43"){sfx("powerUp",1989);unlock("lunar_glow43_use");}\n'
          '  // LIGHT_GLOW43 — +2320 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW43"){sfx("powerUp",1983);unlock("light_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawXonotliteFox9e('
A5_NEW = (
    'function drawZinkeniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4042)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.45+sp*0.35,"#7dd3fc");g.addColorStop(1,"#0c4a6e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(125,211,252,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0c4a6e":"#e0f2fe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🫧":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawZippeiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4046);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+tp*0.35,"#fb923c");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(251,146,60,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(251,146,60,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#fb923c":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🧡":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawXonotliteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="xonotlite_fox9e"){'
A6_NEW = (
    'else if(t.type==="zinkenite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2170);\n'
    '    drawZinkeniteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="zippeite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2172);\n'
    '    drawZippeiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="xonotlite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="xonotlite_fox9e"){'
A7_NEW = (
    'if(hit.type==="zinkenite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2170);\n'
    '      const pts=Math.round(414*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#7dd3fc",2170);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🫧","#e0f2fe",22);\n'
    '      unlock("zinkenite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("zinkenite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="zippeite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2172);\n'
    '      const pts=Math.round(409*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#fb923c",2172);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🧡","#fff7ed",22);\n'
    '      unlock("zippeite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("zippeite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="xonotlite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="xonotlite_fox9e";color="#fb7185";glow="#fff1f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zeunerite_orb9e"')
A8_NEW = ('      type="zinkenite_fox9e";color="#7dd3fc";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zippeite_orb9e";color="#fb923c";glow="#fff7ed";\n'
          '    } else if('+COND100F+'){\n'
          '      type="xonotlite_fox9e";color="#fb7185";glow="#fff1f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zeunerite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="xonotlite_fox9e"?BASE_R*1.59:type==="zeunerite_orb9e"?BASE_R*1.58:'
A9_NEW = 'type==="zinkenite_fox9e"?BASE_R*1.60:type==="zippeite_orb9e"?BASE_R*1.59:type==="xonotlite_fox9e"?BASE_R*1.59:type==="zeunerite_orb9e"?BASE_R*1.58:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'LIGHT_GLOW43:"💡✨",DARK_GLOW43:"🌑✨",WIND_GLOW43:"💨✨"'
A10_NEW = 'SOLAR_GLOW43:"☀️✨",LUNAR_GLOW43:"🌕✨",LIGHT_GLOW43:"💡✨",DARK_GLOW43:"🌑✨",WIND_GLOW43:"💨✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 715 done! +{len(code)-ORIG} bytes")
