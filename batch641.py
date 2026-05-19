import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"colemanite_orb9e_peak", label:"Colemanite Orb Peak", desc:"Reach peak with Colemanite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"meteor_pulse41_use", label:"Meteor Pulse", desc:"Activate METEOR_PULSE41 power-up", icon:"🌠", xp:60 },\n'
'  { id:"meteor_pulse41_max", label:"Meteor Pulser", desc:"Reach max with METEOR_PULSE41 active", icon:"🌠", xp:120 },\n'
'  { id:"nebula_pulse41_use", label:"Nebula Pulse", desc:"Activate NEBULA_PULSE41 power-up", icon:"🌌", xp:60 },\n'
'  { id:"nebula_pulse41_max", label:"Nebula Pulser", desc:"Reach max with NEBULA_PULSE41 active", icon:"🌌", xp:120 },\n'
'  { id:"datolite_fox9e_tap", label:"Datolite Fox", desc:"Tap a Datolite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"datolite_fox9e_peak", label:"Datolite Fox Peak", desc:"Reach peak with Datolite Fox", icon:"🦊", xp:120 },\n'
'  { id:"descloizite_orb9e_tap", label:"Descloizite Orb", desc:"Tap a Descloizite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"descloizite_orb9e_peak", label:"Descloizite Orb Peak", desc:"Reach peak with Descloizite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"PULSAR_PULSE41","QUASAR_PULSE41","PRISM_PULSE41"'
A2_NEW = '"PULSAR_PULSE41","QUASAR_PULSE41","METEOR_PULSE41","NEBULA_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="PULSAR_PULSE41"){'
A3_NEW = (
'} else if(ptype==="METEOR_PULSE41"){\n'
'        gs.score+=2028;showPopup(cx,cy-1738,"+2028 🌠",theme.accent,26);spawnShockwave(cx,cy,"#0a03aa",1900);if(gs.score>=bonusTotal)unlock("meteor_pulse41_max");\n'
'      } else if(ptype==="NEBULA_PULSE41"){\n'
'        gs.score+=2030;showPopup(cx,cy-1740,"+2030 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a087e",1902);if(gs.score>=bonusTotal)unlock("nebula_pulse41_max");\n'
'      } else if(ptype==="PULSAR_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// PULSAR_PULSE41 — +2024 pulsar bonus'
A4_NEW = ('// METEOR_PULSE41 — +2028 meteor bonus\n'
'      if(ptype==="METEOR_PULSE41"){sfx("powerUp",1691);unlock("meteor_pulse41_use");}\n'
'      // NEBULA_PULSE41 — +2030 nebula bonus\n'
'      if(ptype==="NEBULA_PULSE41"){sfx("powerUp",1693);unlock("nebula_pulse41_use");}\n'
'      // PULSAR_PULSE41 — +2024 pulsar bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawCronstedtiteFox9e('
A5_NEW = (
'function drawDatoliteFox9e(ctx,r,ts,datPct){\n'
'  const bob=Math.sin(ts*0.3466)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+datPct*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(datPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(22,163,74,"+(datPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=datPct>0.88?"#4ade80":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(datPct>0.88?"💚":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawDescloiziteOrb9e(ctx,r,ts,desPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3470);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+desPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef2f2");g.addColorStop(0.35+desPct*0.35,"#991b1b");g.addColorStop(1,"#450a0a");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+desPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(153,27,27,"+(0.45+desPct*0.55)+")";ctx.lineWidth=3.5+desPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(desPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(252,165,165,"+(desPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=desPct>0.88?"#fca5a5":"#fef2f2";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(desPct>0.88?"❤️":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawCronstedtiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="cronstedtite_fox9e"){'
A6_NEW = (
'else if(t.type==="datolite_fox9e"){\n'
'      const datPct=Math.min(1,(ts-t.born)/2800);t._datPct=datPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawDatoliteFox9e(ctx,t.radius,ts,datPct);ctx.restore();\n'
'    } else if(t.type==="descloizite_orb9e"){\n'
'      const desPct=Math.min(1,(ts-t.born)/2800);t._desPct=desPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawDescloiziteOrb9e(ctx,t.radius,ts,desPct);ctx.restore();\n'
'    } else if(t.type==="cronstedtite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="cronstedtite_fox9e"){'
A7_NEW = (
'if(hit.type==="datolite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(266*(hit._datPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#16a34a",1874);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("datolite_fox9e_tap");\n'
'        if((hit._datPct||0)>0.88)unlock("datolite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="descloizite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(261*(hit._desPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#991b1b",1876);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("descloizite_orb9e_tap");\n'
'        if((hit._desPct||0)>0.88)unlock("descloizite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="cronstedtite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="cronstedtite_fox9e";color="#166534";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="colemanite_orb9e"')
A8_NEW = ('      type="datolite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="descloizite_orb9e";color="#991b1b";glow="#fef2f2";\n'
           '    } else if('+COND100F+'){\n'
           '      type="cronstedtite_fox9e";color="#166534";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="colemanite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="cronstedtite_fox9e"?BASE_R*1.22:type==="colemanite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="datolite_fox9e"?BASE_R*1.22:type==="descloizite_orb9e"?BASE_R*1.21:type==="cronstedtite_fox9e"?BASE_R*1.22:type==="colemanite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'PULSAR_PULSE41:"💫💠",QUASAR_PULSE41:"🌀💠",'
A10_NEW = 'PULSAR_PULSE41:"💫💠",QUASAR_PULSE41:"🌀💠",METEOR_PULSE41:"🌠💠",NEBULA_PULSE41:"🌌💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 641 done! +{len(src)-original_len} bytes")
