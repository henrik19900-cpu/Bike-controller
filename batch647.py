import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"glaucophane_orb9e_peak", label:"Glaucophane Orb Peak", desc:"Reach peak with Glaucophane Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"surge_pulse41_use", label:"Surge Pulse", desc:"Activate SURGE_PULSE41 power-up", icon:"⚡", xp:60 },\n'
'  { id:"surge_pulse41_max", label:"Surge Pulser", desc:"Reach max with SURGE_PULSE41 active", icon:"⚡", xp:120 },\n'
'  { id:"ripple_pulse41_use", label:"Ripple Pulse", desc:"Activate RIPPLE_PULSE41 power-up", icon:"🌊", xp:60 },\n'
'  { id:"ripple_pulse41_max", label:"Ripple Pulser", desc:"Reach max with RIPPLE_PULSE41 active", icon:"🌊", xp:120 },\n'
'  { id:"goethite_fox9e_tap", label:"Goethite Fox", desc:"Tap a Goethite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"goethite_fox9e_peak", label:"Goethite Fox Peak", desc:"Reach peak with Goethite Fox", icon:"🦊", xp:120 },\n'
'  { id:"greenockite_orb9e_tap", label:"Greenockite Orb", desc:"Tap a Greenockite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"greenockite_orb9e_peak", label:"Greenockite Orb Peak", desc:"Reach peak with Greenockite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"PLASMA_PULSE41","SPARK_PULSE41","PRISM_PULSE41"'
A2_NEW = '"PLASMA_PULSE41","SPARK_PULSE41","SURGE_PULSE41","RIPPLE_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="PLASMA_PULSE41"){'
A3_NEW = (
'} else if(ptype==="SURGE_PULSE41"){\n'
'        gs.score+=2052;showPopup(cx,cy-1762,"+2052 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03b6",1924);if(gs.score>=bonusTotal)unlock("surge_pulse41_max");\n'
'      } else if(ptype==="RIPPLE_PULSE41"){\n'
'        gs.score+=2054;showPopup(cx,cy-1764,"+2054 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a088a",1926);if(gs.score>=bonusTotal)unlock("ripple_pulse41_max");\n'
'      } else if(ptype==="PLASMA_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// PLASMA_PULSE41 — +2048 plasma bonus'
A4_NEW = ('// SURGE_PULSE41 — +2052 surge bonus\n'
'      if(ptype==="SURGE_PULSE41"){sfx("powerUp",1715);unlock("surge_pulse41_use");}\n'
'      // RIPPLE_PULSE41 — +2054 ripple bonus\n'
'      if(ptype==="RIPPLE_PULSE41"){sfx("powerUp",1717);unlock("ripple_pulse41_use");}\n'
'      // PLASMA_PULSE41 — +2048 plasma bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawGibbsiteFox9e('
A5_NEW = (
'function drawGoethiteFox9e(ctx,r,ts,goePct){\n'
'  const bob=Math.sin(ts*0.3514)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef9c3");g.addColorStop(0.45+goePct*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(goePct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(180,83,9,"+(goePct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=goePct>0.88?"#fde047":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(goePct>0.88?"🦁":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGreenockiteOrb9e(ctx,r,ts,greePct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3518);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+greePct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+greePct*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+greePct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(234,179,8,"+(0.45+greePct*0.55)+")";ctx.lineWidth=3.5+greePct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(greePct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(253,224,71,"+(greePct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=greePct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(greePct>0.88?"⭐":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGibbsiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="gibbsite_fox9e"){'
A6_NEW = (
'else if(t.type==="goethite_fox9e"){\n'
'      const goePct=Math.min(1,(ts-t.born)/2800);t._goePct=goePct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGoethiteFox9e(ctx,t.radius,ts,goePct);ctx.restore();\n'
'    } else if(t.type==="greenockite_orb9e"){\n'
'      const greePct=Math.min(1,(ts-t.born)/2800);t._greePct=greePct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGreenockiteOrb9e(ctx,t.radius,ts,greePct);ctx.restore();\n'
'    } else if(t.type==="gibbsite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="gibbsite_fox9e"){'
A7_NEW = (
'if(hit.type==="goethite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(278*(hit._goePct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#b45309",1898);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("goethite_fox9e_tap");\n'
'        if((hit._goePct||0)>0.88)unlock("goethite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="greenockite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(273*(hit._greePct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#eab308",1900);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("greenockite_orb9e_tap");\n'
'        if((hit._greePct||0)>0.88)unlock("greenockite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="gibbsite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="gibbsite_fox9e";color="#d1d5db";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="glaucophane_orb9e"')
A8_NEW = ('      type="goethite_fox9e";color="#b45309";glow="#fef9c3";\n'
           '    } else if('+COND100F+'){\n'
           '      type="greenockite_orb9e";color="#eab308";glow="#fefce8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gibbsite_fox9e";color="#d1d5db";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="glaucophane_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="gibbsite_fox9e"?BASE_R*1.22:type==="glaucophane_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="goethite_fox9e"?BASE_R*1.22:type==="greenockite_orb9e"?BASE_R*1.21:type==="gibbsite_fox9e"?BASE_R*1.22:type==="glaucophane_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'PLASMA_PULSE41:"⚡💠",SPARK_PULSE41:"✴️💠",'
A10_NEW = 'PLASMA_PULSE41:"⚡💠",SPARK_PULSE41:"✴️💠",SURGE_PULSE41:"⚡💠",RIPPLE_PULSE41:"🌊💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 647 done! +{len(src)-original_len} bytes")
