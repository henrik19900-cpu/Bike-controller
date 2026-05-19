import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"descloizite_orb9e_peak", label:"Descloizite Orb Peak", desc:"Reach peak with Descloizite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"galaxy_pulse41_use", label:"Galaxy Pulse", desc:"Activate GALAXY_PULSE41 power-up", icon:"🌌", xp:60 },\n'
'  { id:"galaxy_pulse41_max", label:"Galaxy Pulser", desc:"Reach max with GALAXY_PULSE41 active", icon:"🌌", xp:120 },\n'
'  { id:"cosmos_pulse41_use", label:"Cosmos Pulse", desc:"Activate COSMOS_PULSE41 power-up", icon:"🪐", xp:60 },\n'
'  { id:"cosmos_pulse41_max", label:"Cosmos Pulser", desc:"Reach max with COSMOS_PULSE41 active", icon:"🪐", xp:120 },\n'
'  { id:"enarsite_fox9e_tap", label:"Enarsite Fox", desc:"Tap an Enarsite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"enarsite_fox9e_peak", label:"Enarsite Fox Peak", desc:"Reach peak with Enarsite Fox", icon:"🦊", xp:120 },\n'
'  { id:"erythrite_orb9e_tap", label:"Erythrite Orb", desc:"Tap an Erythrite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"erythrite_orb9e_peak", label:"Erythrite Orb Peak", desc:"Reach peak with Erythrite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"METEOR_PULSE41","NEBULA_PULSE41","PRISM_PULSE41"'
A2_NEW = '"METEOR_PULSE41","NEBULA_PULSE41","GALAXY_PULSE41","COSMOS_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="METEOR_PULSE41"){'
A3_NEW = (
'} else if(ptype==="GALAXY_PULSE41"){\n'
'        gs.score+=2032;showPopup(cx,cy-1742,"+2032 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03ac",1904);if(gs.score>=bonusTotal)unlock("galaxy_pulse41_max");\n'
'      } else if(ptype==="COSMOS_PULSE41"){\n'
'        gs.score+=2034;showPopup(cx,cy-1744,"+2034 🪐",theme.accent,26);spawnShockwave(cx,cy,"#0a0880",1906);if(gs.score>=bonusTotal)unlock("cosmos_pulse41_max");\n'
'      } else if(ptype==="METEOR_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// METEOR_PULSE41 — +2028 meteor bonus'
A4_NEW = ('// GALAXY_PULSE41 — +2032 galaxy bonus\n'
'      if(ptype==="GALAXY_PULSE41"){sfx("powerUp",1695);unlock("galaxy_pulse41_use");}\n'
'      // COSMOS_PULSE41 — +2034 cosmos bonus\n'
'      if(ptype==="COSMOS_PULSE41"){sfx("powerUp",1697);unlock("cosmos_pulse41_use");}\n'
'      // METEOR_PULSE41 — +2028 meteor bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawDatoliteFox9e('
A5_NEW = (
'function drawEnarsiteFox9e(ctx,r,ts,enaPct){\n'
'  const bob=Math.sin(ts*0.3474)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f9fafb");g.addColorStop(0.45+enaPct*0.35,"#374151");g.addColorStop(1,"#111827");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(enaPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(55,65,81,"+(enaPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=enaPct>0.88?"#d1d5db":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(enaPct>0.88?"🩶":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawErythriteOrb9e(ctx,r,ts,eryPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3478);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+eryPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.35+eryPct*0.35,"#a21caf");g.addColorStop(1,"#4a044e");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+eryPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(162,28,175,"+(0.45+eryPct*0.55)+")";ctx.lineWidth=3.5+eryPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(eryPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(240,171,252,"+(eryPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=eryPct>0.88?"#f0abfc":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(eryPct>0.88?"💜":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawDatoliteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="datolite_fox9e"){'
A6_NEW = (
'else if(t.type==="enarsite_fox9e"){\n'
'      const enaPct=Math.min(1,(ts-t.born)/2800);t._enaPct=enaPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawEnarsiteFox9e(ctx,t.radius,ts,enaPct);ctx.restore();\n'
'    } else if(t.type==="erythrite_orb9e"){\n'
'      const eryPct=Math.min(1,(ts-t.born)/2800);t._eryPct=eryPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawErythriteOrb9e(ctx,t.radius,ts,eryPct);ctx.restore();\n'
'    } else if(t.type==="datolite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="datolite_fox9e"){'
A7_NEW = (
'if(hit.type==="enarsite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(268*(hit._enaPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#374151",1878);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("enarsite_fox9e_tap");\n'
'        if((hit._enaPct||0)>0.88)unlock("enarsite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="erythrite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(263*(hit._eryPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#a21caf",1880);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("erythrite_orb9e_tap");\n'
'        if((hit._eryPct||0)>0.88)unlock("erythrite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="datolite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="datolite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="descloizite_orb9e"')
A8_NEW = ('      type="enarsite_fox9e";color="#374151";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="erythrite_orb9e";color="#a21caf";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="datolite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="descloizite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="datolite_fox9e"?BASE_R*1.22:type==="descloizite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="enarsite_fox9e"?BASE_R*1.22:type==="erythrite_orb9e"?BASE_R*1.21:type==="datolite_fox9e"?BASE_R*1.22:type==="descloizite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'METEOR_PULSE41:"🌠💠",NEBULA_PULSE41:"🌌💠",'
A10_NEW = 'METEOR_PULSE41:"🌠💠",NEBULA_PULSE41:"🌌💠",GALAXY_PULSE41:"🌌💠",COSMOS_PULSE41:"🪐💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 642 done! +{len(src)-original_len} bytes")
