import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"coltan_orb9e_peak", label:"Coltan Orb Peak", desc:"Reach peak with Coltan Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"nova_pulse41_use", label:"Nova Pulse", desc:"Activate NOVA_PULSE41 power-up", icon:"🌟", xp:60 },\n'
'  { id:"nova_pulse41_max", label:"Nova Pulser", desc:"Reach max with NOVA_PULSE41 active", icon:"🌟", xp:120 },\n'
'  { id:"comet_pulse41_use", label:"Comet Pulse", desc:"Activate COMET_PULSE41 power-up", icon:"☄️", xp:60 },\n'
'  { id:"comet_pulse41_max", label:"Comet Pulser", desc:"Reach max with COMET_PULSE41 active", icon:"☄️", xp:120 },\n'
'  { id:"cordierite_fox9e_tap", label:"Cordierite Fox", desc:"Tap a Cordierite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"cordierite_fox9e_peak", label:"Cordierite Fox Peak", desc:"Reach peak with Cordierite Fox", icon:"🦊", xp:120 },\n'
'  { id:"cubanite_orb9e_tap", label:"Cubanite Orb", desc:"Tap a Cubanite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"cubanite_orb9e_peak", label:"Cubanite Orb Peak", desc:"Reach peak with Cubanite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"SOLAR_PULSE41","ECLIPSE_PULSE41","PRISM_PULSE41"'
A2_NEW = '"SOLAR_PULSE41","ECLIPSE_PULSE41","NOVA_PULSE41","COMET_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="SOLAR_PULSE41"){'
A3_NEW = (
'} else if(ptype==="NOVA_PULSE41"){\n'
'        gs.score+=2020;showPopup(cx,cy-1730,"+2020 🌟",theme.accent,26);spawnShockwave(cx,cy,"#0a03a6",1892);if(gs.score>=bonusTotal)unlock("nova_pulse41_max");\n'
'      } else if(ptype==="COMET_PULSE41"){\n'
'        gs.score+=2022;showPopup(cx,cy-1732,"+2022 ☄️",theme.accent,26);spawnShockwave(cx,cy,"#0a087a",1894);if(gs.score>=bonusTotal)unlock("comet_pulse41_max");\n'
'      } else if(ptype==="SOLAR_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// SOLAR_PULSE41 — +2016 solar bonus'
A4_NEW = ('// NOVA_PULSE41 — +2020 nova bonus\n'
'      if(ptype==="NOVA_PULSE41"){sfx("powerUp",1683);unlock("nova_pulse41_use");}\n'
'      // COMET_PULSE41 — +2022 comet bonus\n'
'      if(ptype==="COMET_PULSE41"){sfx("powerUp",1685);unlock("comet_pulse41_use");}\n'
'      // SOLAR_PULSE41 — +2016 solar bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawClinozoisiteFox9e('
A5_NEW = (
'function drawCordieriteFox9e(ctx,r,ts,corPct){\n'
'  const bob=Math.sin(ts*0.3450)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#faf5ff");g.addColorStop(0.45+corPct*0.35,"#6d28d9");g.addColorStop(1,"#2e1065");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(corPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(109,40,217,"+(corPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=corPct>0.88?"#c4b5fd":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(corPct>0.88?"💜":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawCubaniteOrb9e(ctx,r,ts,cubPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3454);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+cubPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+cubPct*0.35,"#c2410c");g.addColorStop(1,"#431407");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+cubPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(194,65,12,"+(0.45+cubPct*0.55)+")";ctx.lineWidth=3.5+cubPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(cubPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(251,146,60,"+(cubPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=cubPct>0.88?"#fdba74":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(cubPct>0.88?"🟠":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawClinozoisiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="clinozoisite_fox9e"){'
A6_NEW = (
'else if(t.type==="cordierite_fox9e"){\n'
'      const corPct=Math.min(1,(ts-t.born)/2800);t._corPct=corPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawCordieriteFox9e(ctx,t.radius,ts,corPct);ctx.restore();\n'
'    } else if(t.type==="cubanite_orb9e"){\n'
'      const cubPct=Math.min(1,(ts-t.born)/2800);t._cubPct=cubPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawCubaniteOrb9e(ctx,t.radius,ts,cubPct);ctx.restore();\n'
'    } else if(t.type==="clinozoisite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="clinozoisite_fox9e"){'
A7_NEW = (
'if(hit.type==="cordierite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(262*(hit._corPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#6d28d9",1866);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("cordierite_fox9e_tap");\n'
'        if((hit._corPct||0)>0.88)unlock("cordierite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="cubanite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(257*(hit._cubPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#c2410c",1868);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("cubanite_orb9e_tap");\n'
'        if((hit._cubPct||0)>0.88)unlock("cubanite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="clinozoisite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="clinozoisite_fox9e";color="#4d7c0f";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="coltan_orb9e"')
A8_NEW = ('      type="cordierite_fox9e";color="#6d28d9";glow="#faf5ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="cubanite_orb9e";color="#c2410c";glow="#fff7ed";\n'
           '    } else if('+COND100F+'){\n'
           '      type="clinozoisite_fox9e";color="#4d7c0f";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="coltan_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="clinozoisite_fox9e"?BASE_R*1.22:type==="coltan_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="cordierite_fox9e"?BASE_R*1.22:type==="cubanite_orb9e"?BASE_R*1.21:type==="clinozoisite_fox9e"?BASE_R*1.22:type==="coltan_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'SOLAR_PULSE41:"☀️💠",ECLIPSE_PULSE41:"🌑💠",'
A10_NEW = 'SOLAR_PULSE41:"☀️💠",ECLIPSE_PULSE41:"🌑💠",NOVA_PULSE41:"🌟💠",COMET_PULSE41:"☄️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 639 done! +{len(src)-original_len} bytes")
