import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"lazulite_orb9e_peak", label:"Lazulite Orb Peak", desc:"Reach peak with Lazulite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"galaxy_wave41_use", label:"Galaxy Wave", desc:"Activate GALAXY_WAVE41 power-up", icon:"🌌", xp:60 },\n'
'  { id:"galaxy_wave41_max", label:"Galaxy Waver", desc:"Reach max with GALAXY_WAVE41 active", icon:"🌌", xp:120 },\n'
'  { id:"void_wave41_use", label:"Void Wave", desc:"Activate VOID_WAVE41 power-up", icon:"🕳️", xp:60 },\n'
'  { id:"void_wave41_max", label:"Void Waver", desc:"Reach max with VOID_WAVE41 active", icon:"🕳️", xp:120 },\n'
'  { id:"lawsonite_fox9e_tap", label:"Lawsonite Fox", desc:"Tap a Lawsonite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"lawsonite_fox9e_peak", label:"Lawsonite Fox Peak", desc:"Reach peak with Lawsonite Fox", icon:"🦊", xp:120 },\n'
'  { id:"leadhillite_orb9e_tap", label:"Leadhillite Orb", desc:"Tap a Leadhillite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"leadhillite_orb9e_peak", label:"Leadhillite Orb Peak", desc:"Reach peak with Leadhillite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"NEBULA_WAVE41","AURORA_WAVE41","PRISM_PULSE41"'
A2_NEW = '"NEBULA_WAVE41","AURORA_WAVE41","GALAXY_WAVE41","VOID_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="NEBULA_WAVE41"){'
A3_NEW = (
'} else if(ptype==="GALAXY_WAVE41"){\n'
'        gs.score+=2088;showPopup(cx,cy-1798,"+2088 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03c8",1960);if(gs.score>=bonusTotal)unlock("galaxy_wave41_max");\n'
'      } else if(ptype==="VOID_WAVE41"){\n'
'        gs.score+=2090;showPopup(cx,cy-1800,"+2090 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a089c",1962);if(gs.score>=bonusTotal)unlock("void_wave41_max");\n'
'      } else if(ptype==="NEBULA_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// NEBULA_WAVE41 — +2084 nebula wave bonus'
A4_NEW = ('// GALAXY_WAVE41 — +2088 galaxy wave bonus\n'
'      if(ptype==="GALAXY_WAVE41"){sfx("powerUp",1751);unlock("galaxy_wave41_use");}\n'
'      // VOID_WAVE41 — +2090 void wave bonus\n'
'      if(ptype==="VOID_WAVE41"){sfx("powerUp",1753);unlock("void_wave41_use");}\n'
'      // NEBULA_WAVE41 — +2084 nebula wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawLazuriteFox9e('
A5_NEW = (
'function drawLawsoniteFox9e(ctx,r,ts,lawPct){\n'
'  const bob=Math.sin(ts*0.3586)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.45+lawPct*0.35,"#0891b2");g.addColorStop(1,"#164e63");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(lawPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(8,145,178,"+(lawPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=lawPct>0.88?"#67e8f9":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lawPct>0.88?"🩵":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLeadhilliteOrb9e(ctx,r,ts,leaPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3590);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+leaPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+leaPct*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+leaPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(234,179,8,"+(0.45+leaPct*0.55)+")";ctx.lineWidth=3.5+leaPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(leaPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(253,224,71,"+(leaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=leaPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(leaPct>0.88?"💛":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLazuriteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="lazurite_fox9e"){'
A6_NEW = (
'else if(t.type==="lawsonite_fox9e"){\n'
'      const lawPct=Math.min(1,(ts-t.born)/2800);t._lawPct=lawPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLawsoniteFox9e(ctx,t.radius,ts,lawPct);ctx.restore();\n'
'    } else if(t.type==="leadhillite_orb9e"){\n'
'      const leaPct=Math.min(1,(ts-t.born)/2800);t._leaPct=leaPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLeadhilliteOrb9e(ctx,t.radius,ts,leaPct);ctx.restore();\n'
'    } else if(t.type==="lazurite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="lazurite_fox9e"){'
A7_NEW = (
'if(hit.type==="lawsonite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(296*(hit._lawPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#0891b2",1934);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("lawsonite_fox9e_tap");\n'
'        if((hit._lawPct||0)>0.88)unlock("lawsonite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="leadhillite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(291*(hit._leaPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#eab308",1936);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("leadhillite_orb9e_tap");\n'
'        if((hit._leaPct||0)>0.88)unlock("leadhillite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="lazurite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="lazurite_fox9e";color="#1d4ed8";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lazulite_orb9e"')
A8_NEW = ('      type="lawsonite_fox9e";color="#0891b2";glow="#f0f9ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="leadhillite_orb9e";color="#eab308";glow="#fefce8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lazurite_fox9e";color="#1d4ed8";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lazulite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="lazurite_fox9e"?BASE_R*1.22:type==="lazulite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="lawsonite_fox9e"?BASE_R*1.22:type==="leadhillite_orb9e"?BASE_R*1.21:type==="lazurite_fox9e"?BASE_R*1.22:type==="lazulite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'NEBULA_WAVE41:"🌌💠",AURORA_WAVE41:"🌠💠",'
A10_NEW = 'NEBULA_WAVE41:"🌌💠",AURORA_WAVE41:"🌠💠",GALAXY_WAVE41:"🌌💠",VOID_WAVE41:"🕳️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 656 done! +{len(src)-original_len} bytes")
