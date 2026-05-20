#!/usr/bin/env python3
"""Batch 709: NOVA_GLOW43+ECHO_GLOW43 + VilliaumiteFox9e+VoltaiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"vesuvianite_orb9e_peak", label:"Vesuvianite Orb Peak", desc:"Reach peak with Vesuvianite Orb", icon:"🫐", xp:120 },'
A1_NEW = (
    '{ id:"vesuvianite_orb9e_peak", label:"Vesuvianite Orb Peak", desc:"Reach peak with Vesuvianite Orb", icon:"🫐", xp:120 },\n'
    '  { id:"nova_glow43_use", label:"Nova Glow 43", desc:"Activate NOVA_GLOW43 power-up", icon:"💥", xp:60 },\n'
    '  { id:"nova_glow43_max", label:"Nova Glower 43", desc:"Reach max with NOVA_GLOW43 active", icon:"💥", xp:120 },\n'
    '  { id:"echo_glow43_use", label:"Echo Glow 43", desc:"Activate ECHO_GLOW43 power-up", icon:"📡", xp:60 },\n'
    '  { id:"echo_glow43_max", label:"Echo Glower 43", desc:"Reach max with ECHO_GLOW43 active", icon:"📡", xp:120 },\n'
    '  { id:"villiaumite_fox9e_tap", label:"Villiaumite Fox", desc:"Tap a Villiaumite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"villiaumite_fox9e_peak", label:"Villiaumite Fox Peak", desc:"Reach peak with Villiaumite Fox", icon:"🍒", xp:120 },\n'
    '  { id:"voltaite_orb9e_tap", label:"Voltaite Orb", desc:"Tap a Voltaite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"voltaite_orb9e_peak", label:"Voltaite Orb Peak", desc:"Reach peak with Voltaite Orb", icon:"🖤", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"PRISM_GLOW43","CRYSTAL_GLOW43","NEBULA_GLOW42","AURORA_GLOW42"'
A2_NEW = '"NOVA_GLOW43","ECHO_GLOW43","PRISM_GLOW43","CRYSTAL_GLOW43","NEBULA_GLOW42","AURORA_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="PRISM_GLOW43"){\n'
          '        gs.score+=2296;showPopup(cx,cy-2006,"+2296 🔷",theme.accent,26);spawnShockwave(cx,cy,"#2563eb",2168);if(gs.score>=bonusTotal)unlock("prism_glow43_max");')
A3_NEW = ('  } else if(ptype==="NOVA_GLOW43"){\n'
          '        gs.score+=2300;showPopup(cx,cy-2010,"+2300 💥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2172);if(gs.score>=bonusTotal)unlock("nova_glow43_max");\n'
          '      } else if(ptype==="ECHO_GLOW43"){\n'
          '        gs.score+=2302;showPopup(cx,cy-2012,"+2302 📡",theme.accent,26);spawnShockwave(cx,cy,"#0369a1",2174);if(gs.score>=bonusTotal)unlock("echo_glow43_max");\n'
          '      } else if(ptype==="PRISM_GLOW43"){\n'
          '        gs.score+=2296;showPopup(cx,cy-2006,"+2296 🔷",theme.accent,26);spawnShockwave(cx,cy,"#2563eb",2168);if(gs.score>=bonusTotal)unlock("prism_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // PRISM_GLOW43 — +2296 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW43"){sfx("powerUp",1959);unlock("prism_glow43_use");}')
A4_NEW = ('  // NOVA_GLOW43 — +2300 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW43"){sfx("powerUp",1963);unlock("nova_glow43_use");}\n'
          '  // ECHO_GLOW43 — +2302 echo glow bonus\n'
          '      if(ptype==="ECHO_GLOW43"){sfx("powerUp",1965);unlock("echo_glow43_use");}\n'
          '  // PRISM_GLOW43 — +2296 prism glow bonus\n'
          '      if(ptype==="PRISM_GLOW43"){sfx("powerUp",1959);unlock("prism_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawVarisciteFox9e('
A5_NEW = (
    'function drawVilliaumiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4000)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffe4e6");g.addColorStop(0.45+sp*0.35,"#e11d48");g.addColorStop(1,"#881337");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(225,29,72,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#881337":"#ffe4e6";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🍒":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVoltaiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4004);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e2e8f0");g.addColorStop(0.35+tp*0.35,"#1e293b");g.addColorStop(1,"#020617");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(30,41,59,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(30,41,59,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#1e293b":"#e2e8f0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🖤":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawVarisciteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="variscite_fox9e"){'
A6_NEW = (
    'else if(t.type==="villiaumite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2146);\n'
    '    drawVilliaumiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="voltaite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2148);\n'
    '    drawVoltaiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="variscite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="variscite_fox9e"){'
A7_NEW = (
    'if(hit.type==="villiaumite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2146);\n'
    '      const pts=Math.round(402*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#e11d48",2146);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🍒","#ffe4e6",22);\n'
    '      unlock("villiaumite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("villiaumite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="voltaite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2148);\n'
    '      const pts=Math.round(397*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#1e293b",2148);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🖤","#e2e8f0",22);\n'
    '      unlock("voltaite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("voltaite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="variscite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="variscite_fox9e";color="#34d399";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vesuvianite_orb9e"')
A8_NEW = ('      type="villiaumite_fox9e";color="#e11d48";glow="#ffe4e6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="voltaite_orb9e";color="#1e293b";glow="#e2e8f0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="variscite_fox9e";color="#34d399";glow="#d1fae5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vesuvianite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="variscite_fox9e"?BASE_R*1.53:type==="vesuvianite_orb9e"?BASE_R*1.52:'
A9_NEW = 'type==="villiaumite_fox9e"?BASE_R*1.54:type==="voltaite_orb9e"?BASE_R*1.53:type==="variscite_fox9e"?BASE_R*1.53:type==="vesuvianite_orb9e"?BASE_R*1.52:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'PRISM_GLOW43:"🔷✨",CRYSTAL_GLOW43:"💎✨",NEBULA_GLOW42:"🌠✨"'
A10_NEW = 'NOVA_GLOW43:"💥✨",ECHO_GLOW43:"📡✨",PRISM_GLOW43:"🔷✨",CRYSTAL_GLOW43:"💎✨",NEBULA_GLOW42:"🌠✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 709 done! +{len(code)-ORIG} bytes")
