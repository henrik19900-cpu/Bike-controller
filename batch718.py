#!/usr/bin/env python3
"""Batch 718: PRISM_GLOW44+CRYSTAL_GLOW44 + AegireineFox9e+AenigmatiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"adularia_orb9e_peak", label:"Adularia Orb Peak", desc:"Reach peak with Adularia Orb", icon:"🌙", xp:120 },'
A1_NEW = (
    '{ id:"adularia_orb9e_peak", label:"Adularia Orb Peak", desc:"Reach peak with Adularia Orb", icon:"🌙", xp:120 },\n'
    '  { id:"prism_glow44_use", label:"Prism Glow 44", desc:"Activate PRISM_GLOW44 power-up", icon:"🔷", xp:60 },\n'
    '  { id:"prism_glow44_max", label:"Prism Glower 44", desc:"Reach max with PRISM_GLOW44 active", icon:"🔷", xp:120 },\n'
    '  { id:"crystal_glow44_use", label:"Crystal Glow 44", desc:"Activate CRYSTAL_GLOW44 power-up", icon:"💎", xp:60 },\n'
    '  { id:"crystal_glow44_max", label:"Crystal Glower 44", desc:"Reach max with CRYSTAL_GLOW44 active", icon:"💎", xp:120 },\n'
    '  { id:"aegirine_fox9e_tap", label:"Aegirine Fox", desc:"Tap an Aegirine Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"aegirine_fox9e_peak", label:"Aegirine Fox Peak", desc:"Reach peak with Aegirine Fox", icon:"🌲", xp:120 },\n'
    '  { id:"aenigmatite_orb9e_tap", label:"Aenigmatite Orb", desc:"Tap an Aenigmatite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"aenigmatite_orb9e_peak", label:"Aenigmatite Orb Peak", desc:"Reach peak with Aenigmatite Orb", icon:"🔴", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"NEBULA_GLOW43","AURORA_GLOW43","COSMIC_GLOW43","VOID_GLOW43"'
A2_NEW = '"PRISM_GLOW44","CRYSTAL_GLOW44","NEBULA_GLOW43","AURORA_GLOW43","COSMIC_GLOW43","VOID_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="NEBULA_GLOW43"){\n'
          '        gs.score+=2332;showPopup(cx,cy-2042,"+2332 🌠",theme.accent,26);spawnShockwave(cx,cy,"#5b21b6",2204);if(gs.score>=bonusTotal)unlock("nebula_glow43_max");')
A3_NEW = ('  } else if(ptype==="PRISM_GLOW44"){\n'
          '        gs.score+=2336;showPopup(cx,cy-2046,"+2336 🔷",theme.accent,26);spawnShockwave(cx,cy,"#1d4ed8",2208);if(gs.score>=bonusTotal)unlock("prism_glow44_max");\n'
          '      } else if(ptype==="CRYSTAL_GLOW44"){\n'
          '        gs.score+=2338;showPopup(cx,cy-2048,"+2338 💎",theme.accent,26);spawnShockwave(cx,cy,"#0369a1",2210);if(gs.score>=bonusTotal)unlock("crystal_glow44_max");\n'
          '      } else if(ptype==="NEBULA_GLOW43"){\n'
          '        gs.score+=2332;showPopup(cx,cy-2042,"+2332 🌠",theme.accent,26);spawnShockwave(cx,cy,"#5b21b6",2204);if(gs.score>=bonusTotal)unlock("nebula_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // NEBULA_GLOW43 — +2332 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW43"){sfx("powerUp",1995);unlock("nebula_glow43_use");}')
A4_NEW = ('  // PRISM_GLOW44 — +2336 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW44"){sfx("powerUp",1999);unlock("prism_glow44_use");}\n'
          '  // CRYSTAL_GLOW44 — +2338 crystal glow bonus\n'
          '      if(ptype==="CRYSTAL_GLOW44"){sfx("powerUp",2001);unlock("crystal_glow44_use");}\n'
          '  // NEBULA_GLOW43 — +2332 nebula glow bonus\n'
          '      if(ptype==="NEBULA_GLOW43"){sfx("powerUp",1995);unlock("nebula_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawActinoliteFox9e('
A5_NEW = (
    'function drawAegireineFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4063)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.45+sp*0.35,"#16a34a");g.addColorStop(1,"#052e16");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,163,74,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#052e16":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌲":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAenigmatiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4067);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fff1f2");g.addColorStop(0.35+tp*0.35,"#f43f5e");g.addColorStop(1,"#4c0519");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(244,63,94,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(244,63,94,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#f43f5e":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔴":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawActinoliteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="actinolite_fox9e"){'
A6_NEW = (
    'else if(t.type==="aegirine_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2182);\n'
    '    drawAegireineFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="aenigmatite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2184);\n'
    '    drawAenigmatiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="actinolite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="actinolite_fox9e"){'
A7_NEW = (
    'if(hit.type==="aegirine_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2182);\n'
    '      const pts=Math.round(420*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#16a34a",2182);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌲","#dcfce7",22);\n'
    '      unlock("aegirine_fox9e_tap");\n'
    '      if(rp>0.88)unlock("aegirine_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="aenigmatite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2184);\n'
    '      const pts=Math.round(415*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#f43f5e",2184);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🔴","#fff1f2",22);\n'
    '      unlock("aenigmatite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("aenigmatite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="actinolite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="actinolite_fox9e";color="#86efac";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="adularia_orb9e"')
A8_NEW = ('      type="aegirine_fox9e";color="#16a34a";glow="#dcfce7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aenigmatite_orb9e";color="#f43f5e";glow="#fff1f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="actinolite_fox9e";color="#86efac";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="adularia_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="actinolite_fox9e"?BASE_R*1.62:type==="adularia_orb9e"?BASE_R*1.61:'
A9_NEW = 'type==="aegirine_fox9e"?BASE_R*1.63:type==="aenigmatite_orb9e"?BASE_R*1.62:type==="actinolite_fox9e"?BASE_R*1.62:type==="adularia_orb9e"?BASE_R*1.61:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'NEBULA_GLOW43:"🌠✨",AURORA_GLOW43:"🌌✨",COSMIC_GLOW43:"🌌✨"'
A10_NEW = 'PRISM_GLOW44:"🔷✨",CRYSTAL_GLOW44:"💎✨",NEBULA_GLOW43:"🌠✨",AURORA_GLOW43:"🌌✨",COSMIC_GLOW43:"🌌✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 718 done! +{len(code)-ORIG} bytes")
