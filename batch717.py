#!/usr/bin/env python3
"""Batch 717: NEBULA_GLOW43+AURORA_GLOW43 + ActinoliteFox9e+AdulariaOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"achroite_orb9e_peak", label:"Achroite Orb Peak", desc:"Reach peak with Achroite Orb", icon:"🤍", xp:120 },'
A1_NEW = (
    '{ id:"achroite_orb9e_peak", label:"Achroite Orb Peak", desc:"Reach peak with Achroite Orb", icon:"🤍", xp:120 },\n'
    '  { id:"nebula_glow43_use", label:"Nebula Glow 43", desc:"Activate NEBULA_GLOW43 power-up", icon:"🌠", xp:60 },\n'
    '  { id:"nebula_glow43_max", label:"Nebula Glower 43", desc:"Reach max with NEBULA_GLOW43 active", icon:"🌠", xp:120 },\n'
    '  { id:"aurora_glow43_use", label:"Aurora Glow 43", desc:"Activate AURORA_GLOW43 power-up", icon:"🌌", xp:60 },\n'
    '  { id:"aurora_glow43_max", label:"Aurora Glower 43", desc:"Reach max with AURORA_GLOW43 active", icon:"🌌", xp:120 },\n'
    '  { id:"actinolite_fox9e_tap", label:"Actinolite Fox", desc:"Tap an Actinolite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"actinolite_fox9e_peak", label:"Actinolite Fox Peak", desc:"Reach peak with Actinolite Fox", icon:"🍃", xp:120 },\n'
    '  { id:"adularia_orb9e_tap", label:"Adularia Orb", desc:"Tap an Adularia Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"adularia_orb9e_peak", label:"Adularia Orb Peak", desc:"Reach peak with Adularia Orb", icon:"🌙", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"COSMIC_GLOW43","VOID_GLOW43","SOLAR_GLOW43","LUNAR_GLOW43"'
A2_NEW = '"NEBULA_GLOW43","AURORA_GLOW43","COSMIC_GLOW43","VOID_GLOW43","SOLAR_GLOW43","LUNAR_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="COSMIC_GLOW43"){\n'
          '        gs.score+=2328;showPopup(cx,cy-2038,"+2328 🌌",theme.accent,26);spawnShockwave(cx,cy,"#3730a3",2200);if(gs.score>=bonusTotal)unlock("cosmic_glow43_max");')
A3_NEW = ('  } else if(ptype==="NEBULA_GLOW43"){\n'
          '        gs.score+=2332;showPopup(cx,cy-2042,"+2332 🌠",theme.accent,26);spawnShockwave(cx,cy,"#5b21b6",2204);if(gs.score>=bonusTotal)unlock("nebula_glow43_max");\n'
          '      } else if(ptype==="AURORA_GLOW43"){\n'
          '        gs.score+=2334;showPopup(cx,cy-2044,"+2334 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0891b2",2206);if(gs.score>=bonusTotal)unlock("aurora_glow43_max");\n'
          '      } else if(ptype==="COSMIC_GLOW43"){\n'
          '        gs.score+=2328;showPopup(cx,cy-2038,"+2328 🌌",theme.accent,26);spawnShockwave(cx,cy,"#3730a3",2200);if(gs.score>=bonusTotal)unlock("cosmic_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // COSMIC_GLOW43 — +2328 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW43"){sfx("powerUp",1991);unlock("cosmic_glow43_use");}')
A4_NEW = ('  // NEBULA_GLOW43 — +2332 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW43"){sfx("powerUp",1995);unlock("nebula_glow43_use");}\n'
          '  // AURORA_GLOW43 — +2334 aurora glow bonus\n'
          '      if(ptype==="AURORA_GLOW43"){sfx("powerUp",1997);unlock("aurora_glow43_use");}\n'
          '  // COSMIC_GLOW43 — +2328 cosmic glow bonus\n'
          '      if(ptype==="COSMIC_GLOW43"){sfx("powerUp",1991);unlock("cosmic_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawAcanthiteFox9e('
A5_NEW = (
    'function drawActinoliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4056)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+sp*0.35,"#86efac");g.addColorStop(1,"#166534");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(134,239,172,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#166534":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🍃":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAdulariaOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4060);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f5f3ff");g.addColorStop(0.35+tp*0.35,"#c4b5fd");g.addColorStop(1,"#4c1d95");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(196,181,253,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(196,181,253,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#c4b5fd":"#f5f3ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌙":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAcanthiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="acanthite_fox9e"){'
A6_NEW = (
    'else if(t.type==="actinolite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2178);\n'
    '    drawActinoliteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="adularia_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2180);\n'
    '    drawAdulariaOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="acanthite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="acanthite_fox9e"){'
A7_NEW = (
    'if(hit.type==="actinolite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2178);\n'
    '      const pts=Math.round(418*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#86efac",2178);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🍃","#f0fdf4",22);\n'
    '      unlock("actinolite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("actinolite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="adularia_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2180);\n'
    '      const pts=Math.round(413*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#c4b5fd",2180);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌙","#f5f3ff",22);\n'
    '      unlock("adularia_orb9e_tap");\n'
    '      if(rp>0.88)unlock("adularia_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="acanthite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="acanthite_fox9e";color="#94a3b8";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="achroite_orb9e"')
A8_NEW = ('      type="actinolite_fox9e";color="#86efac";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="adularia_orb9e";color="#c4b5fd";glow="#f5f3ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="acanthite_fox9e";color="#94a3b8";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="achroite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="acanthite_fox9e"?BASE_R*1.61:type==="achroite_orb9e"?BASE_R*1.60:'
A9_NEW = 'type==="actinolite_fox9e"?BASE_R*1.62:type==="adularia_orb9e"?BASE_R*1.61:type==="acanthite_fox9e"?BASE_R*1.61:type==="achroite_orb9e"?BASE_R*1.60:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'COSMIC_GLOW43:"🌌✨",VOID_GLOW43:"🕳️✨",SOLAR_GLOW43:"☀️✨"'
A10_NEW = 'NEBULA_GLOW43:"🌠✨",AURORA_GLOW43:"🌌✨",COSMIC_GLOW43:"🌌✨",VOID_GLOW43:"🕳️✨",SOLAR_GLOW43:"☀️✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 717 done! +{len(code)-ORIG} bytes")
