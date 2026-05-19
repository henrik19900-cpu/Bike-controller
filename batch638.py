import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"celestite_orb9e_peak", label:"Celestite Orb Peak", desc:"Reach peak with Celestite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"solar_pulse41_use", label:"Solar Pulse", desc:"Activate SOLAR_PULSE41 power-up", icon:"☀️", xp:60 },\n'
'  { id:"solar_pulse41_max", label:"Solar Pulser", desc:"Reach max with SOLAR_PULSE41 active", icon:"☀️", xp:120 },\n'
'  { id:"eclipse_pulse41_use", label:"Eclipse Pulse", desc:"Activate ECLIPSE_PULSE41 power-up", icon:"🌑", xp:60 },\n'
'  { id:"eclipse_pulse41_max", label:"Eclipse Pulser", desc:"Reach max with ECLIPSE_PULSE41 active", icon:"🌑", xp:120 },\n'
'  { id:"clinozoisite_fox9e_tap", label:"Clinozoisite Fox", desc:"Tap a Clinozoisite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"clinozoisite_fox9e_peak", label:"Clinozoisite Fox Peak", desc:"Reach peak with Clinozoisite Fox", icon:"🦊", xp:120 },\n'
'  { id:"coltan_orb9e_tap", label:"Coltan Orb", desc:"Tap a Coltan Orb target", icon:"🔮", xp:60 },\n'
'  { id:"coltan_orb9e_peak", label:"Coltan Orb Peak", desc:"Reach peak with Coltan Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"AURORA_PULSE41","THUNDER_PULSE41","PRISM_PULSE41"'
A2_NEW = '"AURORA_PULSE41","THUNDER_PULSE41","SOLAR_PULSE41","ECLIPSE_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_PULSE41"){'
A3_NEW = (
'} else if(ptype==="SOLAR_PULSE41"){\n'
'        gs.score+=2016;showPopup(cx,cy-1726,"+2016 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a03a4",1888);if(gs.score>=bonusTotal)unlock("solar_pulse41_max");\n'
'      } else if(ptype==="ECLIPSE_PULSE41"){\n'
'        gs.score+=2018;showPopup(cx,cy-1728,"+2018 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a0878",1890);if(gs.score>=bonusTotal)unlock("eclipse_pulse41_max");\n'
'      } else if(ptype==="AURORA_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// AURORA_PULSE41 — +2012 aurora bonus'
A4_NEW = ('// SOLAR_PULSE41 — +2016 solar bonus\n'
'      if(ptype==="SOLAR_PULSE41"){sfx("powerUp",1679);unlock("solar_pulse41_use");}\n'
'      // ECLIPSE_PULSE41 — +2018 eclipse bonus\n'
'      if(ptype==="ECLIPSE_PULSE41"){sfx("powerUp",1681);unlock("eclipse_pulse41_use");}\n'
'      // AURORA_PULSE41 — +2012 aurora bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawChrysoberylFox9e('
A5_NEW = (
'function drawClinozoisiteFox9e(ctx,r,ts,clinPct){\n'
'  const bob=Math.sin(ts*0.3442)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+clinPct*0.35,"#4d7c0f");g.addColorStop(1,"#1a2e05");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(clinPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(77,124,15,"+(clinPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=clinPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(clinPct>0.88?"🌿":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawColtanOrb9e(ctx,r,ts,coltPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3446);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+coltPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f3f4f6");g.addColorStop(0.35+coltPct*0.35,"#374151");g.addColorStop(1,"#111827");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+coltPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(55,65,81,"+(0.45+coltPct*0.55)+")";ctx.lineWidth=3.5+coltPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(coltPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(156,163,175,"+(coltPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=coltPct>0.88?"#9ca3af":"#f3f4f6";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(coltPct>0.88?"⚫":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawChrysoberylFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="chrysoberyl_fox9e"){'
A6_NEW = (
'else if(t.type==="clinozoisite_fox9e"){\n'
'      const clinPct=Math.min(1,(ts-t.born)/2800);t._clinPct=clinPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawClinozoisiteFox9e(ctx,t.radius,ts,clinPct);ctx.restore();\n'
'    } else if(t.type==="coltan_orb9e"){\n'
'      const coltPct=Math.min(1,(ts-t.born)/2800);t._coltPct=coltPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawColtanOrb9e(ctx,t.radius,ts,coltPct);ctx.restore();\n'
'    } else if(t.type==="chrysoberyl_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="chrysoberyl_fox9e"){'
A7_NEW = (
'if(hit.type==="clinozoisite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(260*(hit._clinPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#4d7c0f",1862);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("clinozoisite_fox9e_tap");\n'
'        if((hit._clinPct||0)>0.88)unlock("clinozoisite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="coltan_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(255*(hit._coltPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#374151",1864);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("coltan_orb9e_tap");\n'
'        if((hit._coltPct||0)>0.88)unlock("coltan_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="chrysoberyl_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="chrysoberyl_fox9e";color="#047857";glow="#ecfdf5";\n'
           '    } else if('+COND100F+'){\n'
           '      type="celestite_orb9e"')
A8_NEW = ('      type="clinozoisite_fox9e";color="#4d7c0f";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="coltan_orb9e";color="#374151";glow="#f3f4f6";\n'
           '    } else if('+COND100F+'){\n'
           '      type="chrysoberyl_fox9e";color="#047857";glow="#ecfdf5";\n'
           '    } else if('+COND100F+'){\n'
           '      type="celestite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="chrysoberyl_fox9e"?BASE_R*1.22:type==="celestite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="clinozoisite_fox9e"?BASE_R*1.22:type==="coltan_orb9e"?BASE_R*1.21:type==="chrysoberyl_fox9e"?BASE_R*1.22:type==="celestite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'AURORA_PULSE41:"🌠💠",THUNDER_PULSE41:"⚡💠",'
A10_NEW = 'AURORA_PULSE41:"🌠💠",THUNDER_PULSE41:"⚡💠",SOLAR_PULSE41:"☀️💠",ECLIPSE_PULSE41:"🌑💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 638 done! +{len(src)-original_len} bytes")
