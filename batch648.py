import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"greenockite_orb9e_peak", label:"Greenockite Orb Peak", desc:"Reach peak with Greenockite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"pulse_wave41_use", label:"Pulse Wave", desc:"Activate PULSE_WAVE41 power-up", icon:"📡", xp:60 },\n'
'  { id:"pulse_wave41_max", label:"Pulse Waver", desc:"Reach max with PULSE_WAVE41 active", icon:"📡", xp:120 },\n'
'  { id:"flux_wave41_use", label:"Flux Wave", desc:"Activate FLUX_WAVE41 power-up", icon:"🌀", xp:60 },\n'
'  { id:"flux_wave41_max", label:"Flux Waver", desc:"Reach max with FLUX_WAVE41 active", icon:"🌀", xp:120 },\n'
'  { id:"grossular_fox9e_tap", label:"Grossular Fox", desc:"Tap a Grossular Fox target", icon:"🦊", xp:60 },\n'
'  { id:"grossular_fox9e_peak", label:"Grossular Fox Peak", desc:"Reach peak with Grossular Fox", icon:"🦊", xp:120 },\n'
'  { id:"gypsum_orb9e_tap", label:"Gypsum Orb", desc:"Tap a Gypsum Orb target", icon:"🔮", xp:60 },\n'
'  { id:"gypsum_orb9e_peak", label:"Gypsum Orb Peak", desc:"Reach peak with Gypsum Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"SURGE_PULSE41","RIPPLE_PULSE41","PRISM_PULSE41"'
A2_NEW = '"SURGE_PULSE41","RIPPLE_PULSE41","PULSE_WAVE41","FLUX_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="SURGE_PULSE41"){'
A3_NEW = (
'} else if(ptype==="PULSE_WAVE41"){\n'
'        gs.score+=2056;showPopup(cx,cy-1766,"+2056 📡",theme.accent,26);spawnShockwave(cx,cy,"#0a03b8",1928);if(gs.score>=bonusTotal)unlock("pulse_wave41_max");\n'
'      } else if(ptype==="FLUX_WAVE41"){\n'
'        gs.score+=2058;showPopup(cx,cy-1768,"+2058 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a088c",1930);if(gs.score>=bonusTotal)unlock("flux_wave41_max");\n'
'      } else if(ptype==="SURGE_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// SURGE_PULSE41 — +2052 surge bonus'
A4_NEW = ('// PULSE_WAVE41 — +2056 pulse wave bonus\n'
'      if(ptype==="PULSE_WAVE41"){sfx("powerUp",1719);unlock("pulse_wave41_use");}\n'
'      // FLUX_WAVE41 — +2058 flux wave bonus\n'
'      if(ptype==="FLUX_WAVE41"){sfx("powerUp",1721);unlock("flux_wave41_use");}\n'
'      // SURGE_PULSE41 — +2052 surge bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawGoethiteFox9e('
A5_NEW = (
'function drawGrossularFox9e(ctx,r,ts,grosPct){\n'
'  const bob=Math.sin(ts*0.3522)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f7fee7");g.addColorStop(0.45+grosPct*0.35,"#65a30d");g.addColorStop(1,"#1a2e05");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(grosPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(101,163,13,"+(grosPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=grosPct>0.88?"#a3e635":"#f7fee7";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(grosPct>0.88?"💚":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGypsumOrb9e(ctx,r,ts,gypPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3526);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+gypPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fafafa");g.addColorStop(0.35+gypPct*0.35,"#e2e8f0");g.addColorStop(1,"#94a3b8");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+gypPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(226,232,240,"+(0.45+gypPct*0.55)+")";ctx.lineWidth=3.5+gypPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(gypPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(255,255,255,"+(gypPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=gypPct>0.88?"#f1f5f9":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gypPct>0.88?"🤍":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGoethiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="goethite_fox9e"){'
A6_NEW = (
'else if(t.type==="grossular_fox9e"){\n'
'      const grosPct=Math.min(1,(ts-t.born)/2800);t._grosPct=grosPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGrossularFox9e(ctx,t.radius,ts,grosPct);ctx.restore();\n'
'    } else if(t.type==="gypsum_orb9e"){\n'
'      const gypPct=Math.min(1,(ts-t.born)/2800);t._gypPct=gypPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGypsumOrb9e(ctx,t.radius,ts,gypPct);ctx.restore();\n'
'    } else if(t.type==="goethite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="goethite_fox9e"){'
A7_NEW = (
'if(hit.type==="grossular_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(280*(hit._grosPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#65a30d",1902);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("grossular_fox9e_tap");\n'
'        if((hit._grosPct||0)>0.88)unlock("grossular_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="gypsum_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(275*(hit._gypPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#e2e8f0",1904);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("gypsum_orb9e_tap");\n'
'        if((hit._gypPct||0)>0.88)unlock("gypsum_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="goethite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="goethite_fox9e";color="#b45309";glow="#fef9c3";\n'
           '    } else if('+COND100F+'){\n'
           '      type="greenockite_orb9e"')
A8_NEW = ('      type="grossular_fox9e";color="#65a30d";glow="#f7fee7";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gypsum_orb9e";color="#e2e8f0";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="goethite_fox9e";color="#b45309";glow="#fef9c3";\n'
           '    } else if('+COND100F+'){\n'
           '      type="greenockite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="goethite_fox9e"?BASE_R*1.22:type==="greenockite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="grossular_fox9e"?BASE_R*1.22:type==="gypsum_orb9e"?BASE_R*1.21:type==="goethite_fox9e"?BASE_R*1.22:type==="greenockite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'SURGE_PULSE41:"⚡💠",RIPPLE_PULSE41:"🌊💠",'
A10_NEW = 'SURGE_PULSE41:"⚡💠",RIPPLE_PULSE41:"🌊💠",PULSE_WAVE41:"📡💠",FLUX_WAVE41:"🌀💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 648 done! +{len(src)-original_len} bytes")
