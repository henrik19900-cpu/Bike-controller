import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"gypsum_orb9e_peak", label:"Gypsum Orb Peak", desc:"Reach peak with Gypsum Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"photon_wave41_use", label:"Photon Wave", desc:"Activate PHOTON_WAVE41 power-up", icon:"🌟", xp:60 },\n'
'  { id:"photon_wave41_max", label:"Photon Waver", desc:"Reach max with PHOTON_WAVE41 active", icon:"🌟", xp:120 },\n'
'  { id:"quantum_wave41_use", label:"Quantum Wave", desc:"Activate QUANTUM_WAVE41 power-up", icon:"⚛️", xp:60 },\n'
'  { id:"quantum_wave41_max", label:"Quantum Waver", desc:"Reach max with QUANTUM_WAVE41 active", icon:"⚛️", xp:120 },\n'
'  { id:"hauyne_fox9e_tap", label:"Hauyne Fox", desc:"Tap a Hauyne Fox target", icon:"🦊", xp:60 },\n'
'  { id:"hauyne_fox9e_peak", label:"Hauyne Fox Peak", desc:"Reach peak with Hauyne Fox", icon:"🦊", xp:120 },\n'
'  { id:"heazlewoodite_orb9e_tap", label:"Heazlewoodite Orb", desc:"Tap a Heazlewoodite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"heazlewoodite_orb9e_peak", label:"Heazlewoodite Orb Peak", desc:"Reach peak with Heazlewoodite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"PULSE_WAVE41","FLUX_WAVE41","PRISM_PULSE41"'
A2_NEW = '"PULSE_WAVE41","FLUX_WAVE41","PHOTON_WAVE41","QUANTUM_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="PULSE_WAVE41"){'
A3_NEW = (
'} else if(ptype==="PHOTON_WAVE41"){\n'
'        gs.score+=2060;showPopup(cx,cy-1770,"+2060 🌟",theme.accent,26);spawnShockwave(cx,cy,"#0a03ba",1932);if(gs.score>=bonusTotal)unlock("photon_wave41_max");\n'
'      } else if(ptype==="QUANTUM_WAVE41"){\n'
'        gs.score+=2062;showPopup(cx,cy-1772,"+2062 ⚛️",theme.accent,26);spawnShockwave(cx,cy,"#0a088e",1934);if(gs.score>=bonusTotal)unlock("quantum_wave41_max");\n'
'      } else if(ptype==="PULSE_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// PULSE_WAVE41 — +2056 pulse wave bonus'
A4_NEW = ('// PHOTON_WAVE41 — +2060 photon wave bonus\n'
'      if(ptype==="PHOTON_WAVE41"){sfx("powerUp",1723);unlock("photon_wave41_use");}\n'
'      // QUANTUM_WAVE41 — +2062 quantum wave bonus\n'
'      if(ptype==="QUANTUM_WAVE41"){sfx("powerUp",1725);unlock("quantum_wave41_use");}\n'
'      // PULSE_WAVE41 — +2056 pulse wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawGrossularFox9e('
A5_NEW = (
'function drawHayneFox9e(ctx,r,ts,hayPct){\n'
'  const bob=Math.sin(ts*0.3530)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+hayPct*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(hayPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(37,99,235,"+(hayPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=hayPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(hayPct>0.88?"💙":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawHeazlewooditeOrb9e(ctx,r,ts,heaPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3534);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+heaPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+heaPct*0.35,"#d97706");g.addColorStop(1,"#78350f");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+heaPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(217,119,6,"+(0.45+heaPct*0.55)+")";ctx.lineWidth=3.5+heaPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(heaPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(251,191,36,"+(heaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=heaPct>0.88?"#fcd34d":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(heaPct>0.88?"🟤":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGrossularFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="grossular_fox9e"){'
A6_NEW = (
'else if(t.type==="hauyne_fox9e"){\n'
'      const hayPct=Math.min(1,(ts-t.born)/2800);t._hayPct=hayPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawHayneFox9e(ctx,t.radius,ts,hayPct);ctx.restore();\n'
'    } else if(t.type==="heazlewoodite_orb9e"){\n'
'      const heaPct=Math.min(1,(ts-t.born)/2800);t._heaPct=heaPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawHeazlewooditeOrb9e(ctx,t.radius,ts,heaPct);ctx.restore();\n'
'    } else if(t.type==="grossular_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="grossular_fox9e"){'
A7_NEW = (
'if(hit.type==="hauyne_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(282*(hit._hayPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#2563eb",1906);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("hauyne_fox9e_tap");\n'
'        if((hit._hayPct||0)>0.88)unlock("hauyne_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="heazlewoodite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(277*(hit._heaPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#d97706",1908);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("heazlewoodite_orb9e_tap");\n'
'        if((hit._heaPct||0)>0.88)unlock("heazlewoodite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="grossular_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="grossular_fox9e";color="#65a30d";glow="#f7fee7";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gypsum_orb9e"')
A8_NEW = ('      type="hauyne_fox9e";color="#2563eb";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="heazlewoodite_orb9e";color="#d97706";glow="#fefce8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="grossular_fox9e";color="#65a30d";glow="#f7fee7";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gypsum_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="grossular_fox9e"?BASE_R*1.22:type==="gypsum_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="hauyne_fox9e"?BASE_R*1.22:type==="heazlewoodite_orb9e"?BASE_R*1.21:type==="grossular_fox9e"?BASE_R*1.22:type==="gypsum_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'PULSE_WAVE41:"📡💠",FLUX_WAVE41:"🌀💠",'
A10_NEW = 'PULSE_WAVE41:"📡💠",FLUX_WAVE41:"🌀💠",PHOTON_WAVE41:"🌟💠",QUANTUM_WAVE41:"⚛️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 649 done! +{len(src)-original_len} bytes")
