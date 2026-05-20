#!/usr/bin/env python3
"""Batch 711: DAWN_GLOW43+DUSK_GLOW43 + VrbaiteFox9e+WagneriteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"vonsenite_orb9e_peak", label:"Vonsenite Orb Peak", desc:"Reach peak with Vonsenite Orb", icon:"🌑", xp:120 },'
A1_NEW = (
    '{ id:"vonsenite_orb9e_peak", label:"Vonsenite Orb Peak", desc:"Reach peak with Vonsenite Orb", icon:"🌑", xp:120 },\n'
    '  { id:"dawn_glow43_use", label:"Dawn Glow 43", desc:"Activate DAWN_GLOW43 power-up", icon:"🌅", xp:60 },\n'
    '  { id:"dawn_glow43_max", label:"Dawn Glower 43", desc:"Reach max with DAWN_GLOW43 active", icon:"🌅", xp:120 },\n'
    '  { id:"dusk_glow43_use", label:"Dusk Glow 43", desc:"Activate DUSK_GLOW43 power-up", icon:"🌇", xp:60 },\n'
    '  { id:"dusk_glow43_max", label:"Dusk Glower 43", desc:"Reach max with DUSK_GLOW43 active", icon:"🌇", xp:120 },\n'
    '  { id:"vrbaite_fox9e_tap", label:"Vrbaite Fox", desc:"Tap a Vrbaite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"vrbaite_fox9e_peak", label:"Vrbaite Fox Peak", desc:"Reach peak with Vrbaite Fox", icon:"🌸", xp:120 },\n'
    '  { id:"wagnerite_orb9e_tap", label:"Wagnerite Orb", desc:"Tap a Wagnerite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"wagnerite_orb9e_peak", label:"Wagnerite Orb Peak", desc:"Reach peak with Wagnerite Orb", icon:"🍑", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"STAR_GLOW43","MOON_GLOW43","NOVA_GLOW43","ECHO_GLOW43"'
A2_NEW = '"DAWN_GLOW43","DUSK_GLOW43","STAR_GLOW43","MOON_GLOW43","NOVA_GLOW43","ECHO_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="STAR_GLOW43"){\n'
          '        gs.score+=2304;showPopup(cx,cy-2014,"+2304 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#ca8a04",2176);if(gs.score>=bonusTotal)unlock("star_glow43_max");')
A3_NEW = ('  } else if(ptype==="DAWN_GLOW43"){\n'
          '        gs.score+=2308;showPopup(cx,cy-2018,"+2308 🌅",theme.accent,26);spawnShockwave(cx,cy,"#ea580c",2180);if(gs.score>=bonusTotal)unlock("dawn_glow43_max");\n'
          '      } else if(ptype==="DUSK_GLOW43"){\n'
          '        gs.score+=2310;showPopup(cx,cy-2020,"+2310 🌇",theme.accent,26);spawnShockwave(cx,cy,"#6d28d9",2182);if(gs.score>=bonusTotal)unlock("dusk_glow43_max");\n'
          '      } else if(ptype==="STAR_GLOW43"){\n'
          '        gs.score+=2304;showPopup(cx,cy-2014,"+2304 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#ca8a04",2176);if(gs.score>=bonusTotal)unlock("star_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // STAR_GLOW43 — +2304 star glow bonus\n'
          '      if(ptype==="STAR_GLOW43"){sfx("powerUp",1967);unlock("star_glow43_use");}')
A4_NEW = ('  // DAWN_GLOW43 — +2308 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW43"){sfx("powerUp",1971);unlock("dawn_glow43_use");}\n'
          '  // DUSK_GLOW43 — +2310 dusk glow bonus\n'
          '      if(ptype==="DUSK_GLOW43"){sfx("powerUp",1973);unlock("dusk_glow43_use");}\n'
          '  // STAR_GLOW43 — +2304 star glow bonus\n'
          '      if(ptype==="STAR_GLOW43"){sfx("powerUp",1967);unlock("star_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawVolborthiteFox9e('
A5_NEW = (
    'function drawVrbaiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4014)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+sp*0.35,"#db2777");g.addColorStop(1,"#831843");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(219,39,119,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#831843":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌸":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawWagneriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4018);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+tp*0.35,"#f97316");g.addColorStop(1,"#7c2d12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(249,115,22,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(249,115,22,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#f97316":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🍑":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVolborthiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="volborthite_fox9e"){'
A6_NEW = (
    'else if(t.type==="vrbaite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2154);\n'
    '    drawVrbaiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="wagnerite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2156);\n'
    '    drawWagneriteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="volborthite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="volborthite_fox9e"){'
A7_NEW = (
    'if(hit.type==="vrbaite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2154);\n'
    '      const pts=Math.round(406*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#db2777",2154);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌸","#fdf2f8",22);\n'
    '      unlock("vrbaite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("vrbaite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="wagnerite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2156);\n'
    '      const pts=Math.round(401*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#f97316",2156);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🍑","#fff7ed",22);\n'
    '      unlock("wagnerite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("wagnerite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="volborthite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="volborthite_fox9e";color="#65a30d";glow="#ecfccb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vonsenite_orb9e"')
A8_NEW = ('      type="vrbaite_fox9e";color="#db2777";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wagnerite_orb9e";color="#f97316";glow="#fff7ed";\n'
          '    } else if('+COND100F+'){\n'
          '      type="volborthite_fox9e";color="#65a30d";glow="#ecfccb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vonsenite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="volborthite_fox9e"?BASE_R*1.55:type==="vonsenite_orb9e"?BASE_R*1.54:'
A9_NEW = 'type==="vrbaite_fox9e"?BASE_R*1.56:type==="wagnerite_orb9e"?BASE_R*1.55:type==="volborthite_fox9e"?BASE_R*1.55:type==="vonsenite_orb9e"?BASE_R*1.54:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'STAR_GLOW43:"⭐✨",MOON_GLOW43:"🌙✨",NOVA_GLOW43:"💥✨"'
A10_NEW = 'DAWN_GLOW43:"🌅✨",DUSK_GLOW43:"🌇✨",STAR_GLOW43:"⭐✨",MOON_GLOW43:"🌙✨",NOVA_GLOW43:"💥✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 711 done! +{len(code)-ORIG} bytes")
