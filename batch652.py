import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"inesite_orb9e_peak", label:"Inesite Orb Peak", desc:"Reach peak with Inesite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"storm_wave41_use", label:"Storm Wave", desc:"Activate STORM_WAVE41 power-up", icon:"⛈️", xp:60 },\n'
'  { id:"storm_wave41_max", label:"Storm Waver", desc:"Reach max with STORM_WAVE41 active", icon:"⛈️", xp:120 },\n'
'  { id:"nova_wave41_use", label:"Nova Wave", desc:"Activate NOVA_WAVE41 power-up", icon:"💥", xp:60 },\n'
'  { id:"nova_wave41_max", label:"Nova Waver", desc:"Reach max with NOVA_WAVE41 active", icon:"💥", xp:120 },\n'
'  { id:"iridosmine_fox9e_tap", label:"Iridosmine Fox", desc:"Tap an Iridosmine Fox target", icon:"🦊", xp:60 },\n'
'  { id:"iridosmine_fox9e_peak", label:"Iridosmine Fox Peak", desc:"Reach peak with Iridosmine Fox", icon:"🦊", xp:120 },\n'
'  { id:"johannsenite_orb9e_tap", label:"Johannsenite Orb", desc:"Tap a Johannsenite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"johannsenite_orb9e_peak", label:"Johannsenite Orb Peak", desc:"Reach peak with Johannsenite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"SOLAR_WAVE41","TIDE_WAVE41","PRISM_PULSE41"'
A2_NEW = '"SOLAR_WAVE41","TIDE_WAVE41","STORM_WAVE41","NOVA_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="SOLAR_WAVE41"){'
A3_NEW = (
'} else if(ptype==="STORM_WAVE41"){\n'
'        gs.score+=2072;showPopup(cx,cy-1782,"+2072 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#0a03c0",1944);if(gs.score>=bonusTotal)unlock("storm_wave41_max");\n'
'      } else if(ptype==="NOVA_WAVE41"){\n'
'        gs.score+=2074;showPopup(cx,cy-1784,"+2074 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a0894",1946);if(gs.score>=bonusTotal)unlock("nova_wave41_max");\n'
'      } else if(ptype==="SOLAR_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// SOLAR_WAVE41 — +2068 solar wave bonus'
A4_NEW = ('// STORM_WAVE41 — +2072 storm wave bonus\n'
'      if(ptype==="STORM_WAVE41"){sfx("powerUp",1735);unlock("storm_wave41_use");}\n'
'      // NOVA_WAVE41 — +2074 nova wave bonus\n'
'      if(ptype==="NOVA_WAVE41"){sfx("powerUp",1737);unlock("nova_wave41_use");}\n'
'      // SOLAR_WAVE41 — +2068 solar wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawInderiteFox9e('
A5_NEW = (
'function drawIridosmineFox9e(ctx,r,ts,iriPct){\n'
'  const bob=Math.sin(ts*0.3554)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+iriPct*0.35,"#94a3b8");g.addColorStop(1,"#1e293b");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(iriPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(148,163,184,"+(iriPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=iriPct>0.88?"#cbd5e1":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(iriPct>0.88?"🪙":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawJohannseniteOrb9e(ctx,r,ts,johPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3558);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+johPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+johPct*0.35,"#a16207");g.addColorStop(1,"#713f12");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+johPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(161,98,7,"+(0.45+johPct*0.55)+")";ctx.lineWidth=3.5+johPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(johPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(234,179,8,"+(johPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=johPct>0.88?"#fde047":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(johPct>0.88?"🌕":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawInderiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="inderite_fox9e"){'
A6_NEW = (
'else if(t.type==="iridosmine_fox9e"){\n'
'      const iriPct=Math.min(1,(ts-t.born)/2800);t._iriPct=iriPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawIridosmineFox9e(ctx,t.radius,ts,iriPct);ctx.restore();\n'
'    } else if(t.type==="johannsenite_orb9e"){\n'
'      const johPct=Math.min(1,(ts-t.born)/2800);t._johPct=johPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawJohannseniteOrb9e(ctx,t.radius,ts,johPct);ctx.restore();\n'
'    } else if(t.type==="inderite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="inderite_fox9e"){'
A7_NEW = (
'if(hit.type==="iridosmine_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(288*(hit._iriPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#94a3b8",1918);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("iridosmine_fox9e_tap");\n'
'        if((hit._iriPct||0)>0.88)unlock("iridosmine_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="johannsenite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(283*(hit._johPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#a16207",1920);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("johannsenite_orb9e_tap");\n'
'        if((hit._johPct||0)>0.88)unlock("johannsenite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="inderite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="inderite_fox9e";color="#a78bfa";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="inesite_orb9e"')
A8_NEW = ('      type="iridosmine_fox9e";color="#94a3b8";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="johannsenite_orb9e";color="#a16207";glow="#fef9c3";\n'
           '    } else if('+COND100F+'){\n'
           '      type="inderite_fox9e";color="#a78bfa";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="inesite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="inderite_fox9e"?BASE_R*1.22:type==="inesite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="iridosmine_fox9e"?BASE_R*1.22:type==="johannsenite_orb9e"?BASE_R*1.21:type==="inderite_fox9e"?BASE_R*1.22:type==="inesite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'SOLAR_WAVE41:"☀️💠",TIDE_WAVE41:"🌊💠",'
A10_NEW = 'SOLAR_WAVE41:"☀️💠",TIDE_WAVE41:"🌊💠",STORM_WAVE41:"⛈️💠",NOVA_WAVE41:"💥💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 652 done! +{len(src)-original_len} bytes")
