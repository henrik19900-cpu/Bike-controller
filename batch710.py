#!/usr/bin/env python3
"""Batch 710: STAR_GLOW43+MOON_GLOW43 + VolborthiteFox9e+VonseniteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"voltaite_orb9e_peak", label:"Voltaite Orb Peak", desc:"Reach peak with Voltaite Orb", icon:"🖤", xp:120 },'
A1_NEW = (
    '{ id:"voltaite_orb9e_peak", label:"Voltaite Orb Peak", desc:"Reach peak with Voltaite Orb", icon:"🖤", xp:120 },\n'
    '  { id:"star_glow43_use", label:"Star Glow 43", desc:"Activate STAR_GLOW43 power-up", icon:"⭐", xp:60 },\n'
    '  { id:"star_glow43_max", label:"Star Glower 43", desc:"Reach max with STAR_GLOW43 active", icon:"⭐", xp:120 },\n'
    '  { id:"moon_glow43_use", label:"Moon Glow 43", desc:"Activate MOON_GLOW43 power-up", icon:"🌙", xp:60 },\n'
    '  { id:"moon_glow43_max", label:"Moon Glower 43", desc:"Reach max with MOON_GLOW43 active", icon:"🌙", xp:120 },\n'
    '  { id:"volborthite_fox9e_tap", label:"Volborthite Fox", desc:"Tap a Volborthite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"volborthite_fox9e_peak", label:"Volborthite Fox Peak", desc:"Reach peak with Volborthite Fox", icon:"🫒", xp:120 },\n'
    '  { id:"vonsenite_orb9e_tap", label:"Vonsenite Orb", desc:"Tap a Vonsenite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"vonsenite_orb9e_peak", label:"Vonsenite Orb Peak", desc:"Reach peak with Vonsenite Orb", icon:"🌑", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"NOVA_GLOW43","ECHO_GLOW43","PRISM_GLOW43","CRYSTAL_GLOW43"'
A2_NEW = '"STAR_GLOW43","MOON_GLOW43","NOVA_GLOW43","ECHO_GLOW43","PRISM_GLOW43","CRYSTAL_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="NOVA_GLOW43"){\n'
          '        gs.score+=2300;showPopup(cx,cy-2010,"+2300 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2172);if(gs.score>=bonusTotal)unlock("nova_glow43_max");')
A3_NEW = ('  } else if(ptype==="STAR_GLOW43"){\n'
          '        gs.score+=2304;showPopup(cx,cy-2014,"+2304 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#ca8a04",2176);if(gs.score>=bonusTotal)unlock("star_glow43_max");\n'
          '      } else if(ptype==="MOON_GLOW43"){\n'
          '        gs.score+=2306;showPopup(cx,cy-2016,"+2306 🌙",theme.accent,26);spawnShockwave(cx,cy,"#4338ca",2178);if(gs.score>=bonusTotal)unlock("moon_glow43_max");\n'
          '      } else if(ptype==="NOVA_GLOW43"){\n'
          '        gs.score+=2300;showPopup(cx,cy-2010,"+2300 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2172);if(gs.score>=bonusTotal)unlock("nova_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // NOVA_GLOW43 — +2300 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW43"){sfx("powerUp",1963);unlock("nova_glow43_use");}')
A4_NEW = ('  // STAR_GLOW43 — +2304 star glow bonus\n'
          '      if(ptype==="STAR_GLOW43"){sfx("powerUp",1967);unlock("star_glow43_use");}\n'
          '  // MOON_GLOW43 — +2306 moon glow bonus\n'
          '      if(ptype==="MOON_GLOW43"){sfx("powerUp",1969);unlock("moon_glow43_use");}\n'
          '  // NOVA_GLOW43 — +2300 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW43"){sfx("powerUp",1963);unlock("nova_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawVilliaumiteFox9e('
A5_NEW = (
    'function drawVolborthiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4007)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ecfccb");g.addColorStop(0.45+sp*0.35,"#65a30d");g.addColorStop(1,"#365314");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(101,163,13,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#365314":"#ecfccb";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🫒":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVonseniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4011);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+tp*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(22,101,52,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,101,52,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#166534":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌑":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVilliaumiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="villiaumite_fox9e"){'
A6_NEW = (
    'else if(t.type==="volborthite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2150);\n'
    '    drawVolborthiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="vonsenite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2152);\n'
    '    drawVonseniteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="villiaumite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="villiaumite_fox9e"){'
A7_NEW = (
    'if(hit.type==="volborthite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2150);\n'
    '      const pts=Math.round(404*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#65a30d",2150);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🫒","#ecfccb",22);\n'
    '      unlock("volborthite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("volborthite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="vonsenite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2152);\n'
    '      const pts=Math.round(399*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#166534",2152);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌑","#f0fdf4",22);\n'
    '      unlock("vonsenite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("vonsenite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="villiaumite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="villiaumite_fox9e";color="#e11d48";glow="#ffe4e6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="voltaite_orb9e"')
A8_NEW = ('      type="volborthite_fox9e";color="#65a30d";glow="#ecfccb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vonsenite_orb9e";color="#166534";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="villiaumite_fox9e";color="#e11d48";glow="#ffe4e6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="voltaite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="villiaumite_fox9e"?BASE_R*1.54:type==="voltaite_orb9e"?BASE_R*1.53:'
A9_NEW = 'type==="volborthite_fox9e"?BASE_R*1.55:type==="vonsenite_orb9e"?BASE_R*1.54:type==="villiaumite_fox9e"?BASE_R*1.54:type==="voltaite_orb9e"?BASE_R*1.53:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'NOVA_GLOW43:"💥✨",ECHO_GLOW43:"📡✨",PRISM_GLOW43:"🔷✨"'
A10_NEW = 'STAR_GLOW43:"⭐✨",MOON_GLOW43:"🌙✨",NOVA_GLOW43:"💥✨",ECHO_GLOW43:"📡✨",PRISM_GLOW43:"🔷✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 710 done! +{len(code)-ORIG} bytes")
