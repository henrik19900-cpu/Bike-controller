#!/usr/bin/env python3
"""Batch 720: STAR_GLOW44+MOON_GLOW44 + AheyliteFox9e+AikiniteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"aguilarite_orb9e_peak", label:"Aguilarite Orb Peak", desc:"Reach peak with Aguilarite Orb", icon:"🩶", xp:120 },'
A1_NEW = (
    '{ id:"aguilarite_orb9e_peak", label:"Aguilarite Orb Peak", desc:"Reach peak with Aguilarite Orb", icon:"🩶", xp:120 },\n'
    '  { id:"star_glow44_use", label:"Star Glow 44", desc:"Activate STAR_GLOW44 power-up", icon:"⭐", xp:60 },\n'
    '  { id:"star_glow44_max", label:"Star Glower 44", desc:"Reach max with STAR_GLOW44 active", icon:"⭐", xp:120 },\n'
    '  { id:"moon_glow44_use", label:"Moon Glow 44", desc:"Activate MOON_GLOW44 power-up", icon:"🌙", xp:60 },\n'
    '  { id:"moon_glow44_max", label:"Moon Glower 44", desc:"Reach max with MOON_GLOW44 active", icon:"🌙", xp:120 },\n'
    '  { id:"aheylite_fox9e_tap", label:"Aheylite Fox", desc:"Tap an Aheylite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"aheylite_fox9e_peak", label:"Aheylite Fox Peak", desc:"Reach peak with Aheylite Fox", icon:"🩷", xp:120 },\n'
    '  { id:"aikinite_orb9e_tap", label:"Aikinite Orb", desc:"Tap an Aikinite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"aikinite_orb9e_peak", label:"Aikinite Orb Peak", desc:"Reach peak with Aikinite Orb", icon:"🟤", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"NOVA_GLOW44","ECHO_GLOW44","PRISM_GLOW44","CRYSTAL_GLOW44"'
A2_NEW = '"STAR_GLOW44","MOON_GLOW44","NOVA_GLOW44","ECHO_GLOW44","PRISM_GLOW44","CRYSTAL_GLOW44"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="NOVA_GLOW44"){\n'
          '        gs.score+=2340;showPopup(cx,cy-2050,"+2340 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2212);if(gs.score>=bonusTotal)unlock("nova_glow44_max");')
A3_NEW = ('  } else if(ptype==="STAR_GLOW44"){\n'
          '        gs.score+=2344;showPopup(cx,cy-2054,"+2344 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#ca8a04",2216);if(gs.score>=bonusTotal)unlock("star_glow44_max");\n'
          '      } else if(ptype==="MOON_GLOW44"){\n'
          '        gs.score+=2346;showPopup(cx,cy-2056,"+2346 🌙",theme.accent,26);spawnShockwave(cx,cy,"#4338ca",2218);if(gs.score>=bonusTotal)unlock("moon_glow44_max");\n'
          '      } else if(ptype==="NOVA_GLOW44"){\n'
          '        gs.score+=2340;showPopup(cx,cy-2050,"+2340 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2212);if(gs.score>=bonusTotal)unlock("nova_glow44_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // NOVA_GLOW44 — +2340 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW44"){sfx("powerUp",2003);unlock("nova_glow44_use");}')
A4_NEW = ('  // STAR_GLOW44 — +2344 star glow bonus\n'
          '      if(ptype==="STAR_GLOW44"){sfx("powerUp",2007);unlock("star_glow44_use");}\n'
          '  // MOON_GLOW44 — +2346 moon glow bonus\n'
          '      if(ptype==="MOON_GLOW44"){sfx("powerUp",2009);unlock("moon_glow44_use");}\n'
          '  // NOVA_GLOW44 — +2340 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW44"){sfx("powerUp",2003);unlock("nova_glow44_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawAfghaniteFox9e('
A5_NEW = (
    'function drawAheyliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4077)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+sp*0.35,"#f472b6");g.addColorStop(1,"#9d174d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(244,114,182,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#9d174d":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🩷":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAikiniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4081);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+tp*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(180,83,9,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(180,83,9,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#b45309":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟤":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAfghaniteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="afghanite_fox9e"){'
A6_NEW = (
    'else if(t.type==="aheylite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2190);\n'
    '    drawAheyliteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="aikinite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2192);\n'
    '    drawAikiniteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="afghanite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="afghanite_fox9e"){'
A7_NEW = (
    'if(hit.type==="aheylite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2190);\n'
    '      const pts=Math.round(424*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#f472b6",2190);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🩷","#fdf2f8",22);\n'
    '      unlock("aheylite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("aheylite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="aikinite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2192);\n'
    '      const pts=Math.round(419*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#b45309",2192);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fef3c7",22);\n'
    '      unlock("aikinite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("aikinite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="afghanite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="afghanite_fox9e";color="#3b82f6";glow="#dbeafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aguilarite_orb9e"')
A8_NEW = ('      type="aheylite_fox9e";color="#f472b6";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aikinite_orb9e";color="#b45309";glow="#fef3c7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="afghanite_fox9e";color="#3b82f6";glow="#dbeafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aguilarite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="afghanite_fox9e"?BASE_R*1.64:type==="aguilarite_orb9e"?BASE_R*1.63:'
A9_NEW = 'type==="aheylite_fox9e"?BASE_R*1.65:type==="aikinite_orb9e"?BASE_R*1.64:type==="afghanite_fox9e"?BASE_R*1.64:type==="aguilarite_orb9e"?BASE_R*1.63:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'NOVA_GLOW44:"💥✨",ECHO_GLOW44:"📡✨",PRISM_GLOW44:"🔷✨"'
A10_NEW = 'STAR_GLOW44:"⭐✨",MOON_GLOW44:"🌙✨",NOVA_GLOW44:"💥✨",ECHO_GLOW44:"📡✨",PRISM_GLOW44:"🔷✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 720 done! +{len(code)-ORIG} bytes")
