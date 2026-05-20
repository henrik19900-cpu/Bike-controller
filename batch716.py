#!/usr/bin/env python3
"""Batch 716: COSMIC_GLOW43+VOID_GLOW43 + AcanthiteFox9e+AchroiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"zippeite_orb9e_peak", label:"Zippeite Orb Peak", desc:"Reach peak with Zippeite Orb", icon:"🧡", xp:120 },'
A1_NEW = (
    '{ id:"zippeite_orb9e_peak", label:"Zippeite Orb Peak", desc:"Reach peak with Zippeite Orb", icon:"🧡", xp:120 },\n'
    '  { id:"cosmic_glow43_use", label:"Cosmic Glow 43", desc:"Activate COSMIC_GLOW43 power-up", icon:"🌌", xp:60 },\n'
    '  { id:"cosmic_glow43_max", label:"Cosmic Glower 43", desc:"Reach max with COSMIC_GLOW43 active", icon:"🌌", xp:120 },\n'
    '  { id:"void_glow43_use", label:"Void Glow 43", desc:"Activate VOID_GLOW43 power-up", icon:"🕳️", xp:60 },\n'
    '  { id:"void_glow43_max", label:"Void Glower 43", desc:"Reach max with VOID_GLOW43 active", icon:"🕳️", xp:120 },\n'
    '  { id:"acanthite_fox9e_tap", label:"Acanthite Fox", desc:"Tap an Acanthite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"acanthite_fox9e_peak", label:"Acanthite Fox Peak", desc:"Reach peak with Acanthite Fox", icon:"🥈", xp:120 },\n'
    '  { id:"achroite_orb9e_tap", label:"Achroite Orb", desc:"Tap an Achroite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"achroite_orb9e_peak", label:"Achroite Orb Peak", desc:"Reach peak with Achroite Orb", icon:"🤍", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"SOLAR_GLOW43","LUNAR_GLOW43","LIGHT_GLOW43","DARK_GLOW43"'
A2_NEW = '"COSMIC_GLOW43","VOID_GLOW43","SOLAR_GLOW43","LUNAR_GLOW43","LIGHT_GLOW43","DARK_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="SOLAR_GLOW43"){\n'
          '        gs.score+=2324;showPopup(cx,cy-2034,"+2324 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#d97706",2196);if(gs.score>=bonusTotal)unlock("solar_glow43_max");')
A3_NEW = ('  } else if(ptype==="COSMIC_GLOW43"){\n'
          '        gs.score+=2328;showPopup(cx,cy-2038,"+2328 🌌",theme.accent,26);spawnShockwave(cx,cy,"#3730a3",2200);if(gs.score>=bonusTotal)unlock("cosmic_glow43_max");\n'
          '      } else if(ptype==="VOID_GLOW43"){\n'
          '        gs.score+=2330;showPopup(cx,cy-2040,"+2330 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0c0a09",2202);if(gs.score>=bonusTotal)unlock("void_glow43_max");\n'
          '      } else if(ptype==="SOLAR_GLOW43"){\n'
          '        gs.score+=2324;showPopup(cx,cy-2034,"+2324 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#d97706",2196);if(gs.score>=bonusTotal)unlock("solar_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // SOLAR_GLOW43 — +2324 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW43"){sfx("powerUp",1987);unlock("solar_glow43_use");}')
A4_NEW = ('  // COSMIC_GLOW43 — +2328 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW43"){sfx("powerUp",1991);unlock("cosmic_glow43_use");}\n'
          '  // VOID_GLOW43 — +2330 void glow bonus\n'
          '      if(ptype==="VOID_GLOW43"){sfx("powerUp",1993);unlock("void_glow43_use");}\n'
          '  // SOLAR_GLOW43 — +2324 solar glow bonus\n'
          '      if(ptype==="SOLAR_GLOW43"){sfx("powerUp",1987);unlock("solar_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawZinkeniteFox9e('
A5_NEW = (
    'function drawAcanthiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4049)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.45+sp*0.35,"#94a3b8");g.addColorStop(1,"#334155");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#334155":"#f1f5f9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🥈":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAchroiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4053);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffffff");g.addColorStop(0.35+tp*0.35,"#e2e8f0");g.addColorStop(1,"#475569");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(226,232,240,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(226,232,240,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#e2e8f0":"#ffffff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🤍":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawZinkeniteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="zinkenite_fox9e"){'
A6_NEW = (
    'else if(t.type==="acanthite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2174);\n'
    '    drawAcanthiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="achroite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2176);\n'
    '    drawAchroiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="zinkenite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="zinkenite_fox9e"){'
A7_NEW = (
    'if(hit.type==="acanthite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2174);\n'
    '      const pts=Math.round(416*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#94a3b8",2174);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🥈","#f1f5f9",22);\n'
    '      unlock("acanthite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("acanthite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="achroite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2176);\n'
    '      const pts=Math.round(411*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#e2e8f0",2176);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🤍","#ffffff",22);\n'
    '      unlock("achroite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("achroite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="zinkenite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="zinkenite_fox9e";color="#7dd3fc";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zippeite_orb9e"')
A8_NEW = ('      type="acanthite_fox9e";color="#94a3b8";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="achroite_orb9e";color="#e2e8f0";glow="#ffffff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zinkenite_fox9e";color="#7dd3fc";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zippeite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="zinkenite_fox9e"?BASE_R*1.60:type==="zippeite_orb9e"?BASE_R*1.59:'
A9_NEW = 'type==="acanthite_fox9e"?BASE_R*1.61:type==="achroite_orb9e"?BASE_R*1.60:type==="zinkenite_fox9e"?BASE_R*1.60:type==="zippeite_orb9e"?BASE_R*1.59:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'SOLAR_GLOW43:"☀️✨",LUNAR_GLOW43:"🌕✨",LIGHT_GLOW43:"💡✨"'
A10_NEW = 'COSMIC_GLOW43:"🌌✨",VOID_GLOW43:"🕳️✨",SOLAR_GLOW43:"☀️✨",LUNAR_GLOW43:"🌕✨",LIGHT_GLOW43:"💡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 716 done! +{len(code)-ORIG} bytes")
