#!/usr/bin/env python3
"""Batch 719: NOVA_GLOW44+ECHO_GLOW44 + AfghaniteFox9e+AguilariteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"aenigmatite_orb9e_peak", label:"Aenigmatite Orb Peak", desc:"Reach peak with Aenigmatite Orb", icon:"🔴", xp:120 },'
A1_NEW = (
    '{ id:"aenigmatite_orb9e_peak", label:"Aenigmatite Orb Peak", desc:"Reach peak with Aenigmatite Orb", icon:"🔴", xp:120 },\n'
    '  { id:"nova_glow44_use", label:"Nova Glow 44", desc:"Activate NOVA_GLOW44 power-up", icon:"💥", xp:60 },\n'
    '  { id:"nova_glow44_max", label:"Nova Glower 44", desc:"Reach max with NOVA_GLOW44 active", icon:"💥", xp:120 },\n'
    '  { id:"echo_glow44_use", label:"Echo Glow 44", desc:"Activate ECHO_GLOW44 power-up", icon:"📡", xp:60 },\n'
    '  { id:"echo_glow44_max", label:"Echo Glower 44", desc:"Reach max with ECHO_GLOW44 active", icon:"📡", xp:120 },\n'
    '  { id:"afghanite_fox9e_tap", label:"Afghanite Fox", desc:"Tap an Afghanite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"afghanite_fox9e_peak", label:"Afghanite Fox Peak", desc:"Reach peak with Afghanite Fox", icon:"💙", xp:120 },\n'
    '  { id:"aguilarite_orb9e_tap", label:"Aguilarite Orb", desc:"Tap an Aguilarite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"aguilarite_orb9e_peak", label:"Aguilarite Orb Peak", desc:"Reach peak with Aguilarite Orb", icon:"🩶", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"PRISM_GLOW44","CRYSTAL_GLOW44","NEBULA_GLOW43","AURORA_GLOW43"'
A2_NEW = '"NOVA_GLOW44","ECHO_GLOW44","PRISM_GLOW44","CRYSTAL_GLOW44","NEBULA_GLOW43","AURORA_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="PRISM_GLOW44"){\n'
          '        gs.score+=2336;showPopup(cx,cy-2046,"+2336 🔷",theme.accent,26);spawnShockwave(cx,cy,"#1d4ed8",2208);if(gs.score>=bonusTotal)unlock("prism_glow44_max");')
A3_NEW = ('  } else if(ptype==="NOVA_GLOW44"){\n'
          '        gs.score+=2340;showPopup(cx,cy-2050,"+2340 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2212);if(gs.score>=bonusTotal)unlock("nova_glow44_max");\n'
          '      } else if(ptype==="ECHO_GLOW44"){\n'
          '        gs.score+=2342;showPopup(cx,cy-2052,"+2342 📡",theme.accent,26);spawnShockwave(cx,cy,"#0369a1",2214);if(gs.score>=bonusTotal)unlock("echo_glow44_max");\n'
          '      } else if(ptype==="PRISM_GLOW44"){\n'
          '        gs.score+=2336;showPopup(cx,cy-2046,"+2336 🔷",theme.accent,26);spawnShockwave(cx,cy,"#1d4ed8",2208);if(gs.score>=bonusTotal)unlock("prism_glow44_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // PRISM_GLOW44 — +2336 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW44"){sfx("powerUp",1999);unlock("prism_glow44_use");}')
A4_NEW = ('  // NOVA_GLOW44 — +2340 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW44"){sfx("powerUp",2003);unlock("nova_glow44_use");}\n'
          '  // ECHO_GLOW44 — +2342 echo glow bonus\n'
          '      if(ptype==="ECHO_GLOW44"){sfx("powerUp",2005);unlock("echo_glow44_use");}\n'
          '  // PRISM_GLOW44 — +2336 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW44"){sfx("powerUp",1999);unlock("prism_glow44_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawAegireineFox9e('
A5_NEW = (
    'function drawAfghaniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4070)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dbeafe");g.addColorStop(0.45+sp*0.35,"#3b82f6");g.addColorStop(1,"#1e3a8a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(59,130,246,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#1e3a8a":"#dbeafe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"💙":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAguilariteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4074);\n'
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
    'function drawAegireineFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="aegirine_fox9e"){'
A6_NEW = (
    'else if(t.type==="afghanite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2186);\n'
    '    drawAfghaniteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="aguilarite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2188);\n'
    '    drawAguilariteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="aegirine_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="aegirine_fox9e"){'
A7_NEW = (
    'if(hit.type==="afghanite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2186);\n'
    '      const pts=Math.round(422*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#3b82f6",2186);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 💙","#dbeafe",22);\n'
    '      unlock("afghanite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("afghanite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="aguilarite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2188);\n'
    '      const pts=Math.round(417*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#64748b",2188);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🩶","#f1f5f9",22);\n'
    '      unlock("aguilarite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("aguilarite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="aegirine_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="aegirine_fox9e";color="#16a34a";glow="#dcfce7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aenigmatite_orb9e"')
A8_NEW = ('      type="afghanite_fox9e";color="#3b82f6";glow="#dbeafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aguilarite_orb9e";color="#64748b";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aegirine_fox9e";color="#16a34a";glow="#dcfce7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aenigmatite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="aegirine_fox9e"?BASE_R*1.63:type==="aenigmatite_orb9e"?BASE_R*1.62:'
A9_NEW = 'type==="afghanite_fox9e"?BASE_R*1.64:type==="aguilarite_orb9e"?BASE_R*1.63:type==="aegirine_fox9e"?BASE_R*1.63:type==="aenigmatite_orb9e"?BASE_R*1.62:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'PRISM_GLOW44:"🔷✨",CRYSTAL_GLOW44:"💎✨",NEBULA_GLOW43:"🌠✨"'
A10_NEW = 'NOVA_GLOW44:"💥✨",ECHO_GLOW44:"📡✨",PRISM_GLOW44:"🔷✨",CRYSTAL_GLOW44:"💎✨",NEBULA_GLOW43:"🌠✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 719 done! +{len(code)-ORIG} bytes")
