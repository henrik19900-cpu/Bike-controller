import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"cubanite_orb9e_peak", label:"Cubanite Orb Peak", desc:"Reach peak with Cubanite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"pulsar_pulse41_use", label:"Pulsar Pulse", desc:"Activate PULSAR_PULSE41 power-up", icon:"💫", xp:60 },\n'
'  { id:"pulsar_pulse41_max", label:"Pulsar Pulser", desc:"Reach max with PULSAR_PULSE41 active", icon:"💫", xp:120 },\n'
'  { id:"quasar_pulse41_use", label:"Quasar Pulse", desc:"Activate QUASAR_PULSE41 power-up", icon:"🌀", xp:60 },\n'
'  { id:"quasar_pulse41_max", label:"Quasar Pulser", desc:"Reach max with QUASAR_PULSE41 active", icon:"🌀", xp:120 },\n'
'  { id:"cronstedtite_fox9e_tap", label:"Cronstedtite Fox", desc:"Tap a Cronstedtite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"cronstedtite_fox9e_peak", label:"Cronstedtite Fox Peak", desc:"Reach peak with Cronstedtite Fox", icon:"🦊", xp:120 },\n'
'  { id:"colemanite_orb9e_tap", label:"Colemanite Orb", desc:"Tap a Colemanite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"colemanite_orb9e_peak", label:"Colemanite Orb Peak", desc:"Reach peak with Colemanite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"NOVA_PULSE41","COMET_PULSE41","PRISM_PULSE41"'
A2_NEW = '"NOVA_PULSE41","COMET_PULSE41","PULSAR_PULSE41","QUASAR_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="NOVA_PULSE41"){'
A3_NEW = (
'} else if(ptype==="PULSAR_PULSE41"){\n'
'        gs.score+=2024;showPopup(cx,cy-1734,"+2024 💫",theme.accent,26);spawnShockwave(cx,cy,"#0a03a8",1896);if(gs.score>=bonusTotal)unlock("pulsar_pulse41_max");\n'
'      } else if(ptype==="QUASAR_PULSE41"){\n'
'        gs.score+=2026;showPopup(cx,cy-1736,"+2026 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a087c",1898);if(gs.score>=bonusTotal)unlock("quasar_pulse41_max");\n'
'      } else if(ptype==="NOVA_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// NOVA_PULSE41 — +2020 nova bonus'
A4_NEW = ('// PULSAR_PULSE41 — +2024 pulsar bonus\n'
'      if(ptype==="PULSAR_PULSE41"){sfx("powerUp",1687);unlock("pulsar_pulse41_use");}\n'
'      // QUASAR_PULSE41 — +2026 quasar bonus\n'
'      if(ptype==="QUASAR_PULSE41"){sfx("powerUp",1689);unlock("quasar_pulse41_use");}\n'
'      // NOVA_PULSE41 — +2020 nova bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawCordieriteFox9e('
A5_NEW = (
'function drawCronstedtiteFox9e(ctx,r,ts,cronPct){\n'
'  const bob=Math.sin(ts*0.3458)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+cronPct*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(cronPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(22,101,52,"+(cronPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=cronPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(cronPct>0.88?"🌑":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawColemaniteOrb9e(ctx,r,ts,colmPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3462);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+colmPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+colmPct*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+colmPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(202,138,4,"+(0.45+colmPct*0.55)+")";ctx.lineWidth=3.5+colmPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(colmPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(253,224,71,"+(colmPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=colmPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(colmPct>0.88?"💛":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawCordieriteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="cordierite_fox9e"){'
A6_NEW = (
'else if(t.type==="cronstedtite_fox9e"){\n'
'      const cronPct=Math.min(1,(ts-t.born)/2800);t._cronPct=cronPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawCronstedtiteFox9e(ctx,t.radius,ts,cronPct);ctx.restore();\n'
'    } else if(t.type==="colemanite_orb9e"){\n'
'      const colmPct=Math.min(1,(ts-t.born)/2800);t._colmPct=colmPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawColemaniteOrb9e(ctx,t.radius,ts,colmPct);ctx.restore();\n'
'    } else if(t.type==="cordierite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="cordierite_fox9e"){'
A7_NEW = (
'if(hit.type==="cronstedtite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(264*(hit._cronPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#166534",1870);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("cronstedtite_fox9e_tap");\n'
'        if((hit._cronPct||0)>0.88)unlock("cronstedtite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="colemanite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(259*(hit._colmPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#ca8a04",1872);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("colemanite_orb9e_tap");\n'
'        if((hit._colmPct||0)>0.88)unlock("colemanite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="cordierite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="cordierite_fox9e";color="#6d28d9";glow="#faf5ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="cubanite_orb9e"')
A8_NEW = ('      type="cronstedtite_fox9e";color="#166534";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="colemanite_orb9e";color="#ca8a04";glow="#fefce8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="cordierite_fox9e";color="#6d28d9";glow="#faf5ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="cubanite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="cordierite_fox9e"?BASE_R*1.22:type==="cubanite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="cronstedtite_fox9e"?BASE_R*1.22:type==="colemanite_orb9e"?BASE_R*1.21:type==="cordierite_fox9e"?BASE_R*1.22:type==="cubanite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'NOVA_PULSE41:"🌟💠",COMET_PULSE41:"☄️💠",'
A10_NEW = 'NOVA_PULSE41:"🌟💠",COMET_PULSE41:"☄️💠",PULSAR_PULSE41:"💫💠",QUASAR_PULSE41:"🌀💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 640 done! +{len(src)-original_len} bytes")
