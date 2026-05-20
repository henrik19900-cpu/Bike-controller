import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"kinoite_orb9e_peak", label:"Kinoite Orb Peak", desc:"Reach peak with Kinoite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"nebula_wave41_use", label:"Nebula Wave", desc:"Activate NEBULA_WAVE41 power-up", icon:"🌌", xp:60 },\n'
'  { id:"nebula_wave41_max", label:"Nebula Waver", desc:"Reach max with NEBULA_WAVE41 active", icon:"🌌", xp:120 },\n'
'  { id:"aurora_wave41_use", label:"Aurora Wave", desc:"Activate AURORA_WAVE41 power-up", icon:"🌠", xp:60 },\n'
'  { id:"aurora_wave41_max", label:"Aurora Waver", desc:"Reach max with AURORA_WAVE41 active", icon:"🌠", xp:120 },\n'
'  { id:"lazurite_fox9e_tap", label:"Lazurite Fox", desc:"Tap a Lazurite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"lazurite_fox9e_peak", label:"Lazurite Fox Peak", desc:"Reach peak with Lazurite Fox", icon:"🦊", xp:120 },\n'
'  { id:"lazulite_orb9e_tap", label:"Lazulite Orb", desc:"Tap a Lazulite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"lazulite_orb9e_peak", label:"Lazulite Orb Peak", desc:"Reach peak with Lazulite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"CRYSTAL_WAVE41","PRISM_WAVE41","PRISM_PULSE41"'
A2_NEW = '"CRYSTAL_WAVE41","PRISM_WAVE41","NEBULA_WAVE41","AURORA_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="CRYSTAL_WAVE41"){'
A3_NEW = (
'} else if(ptype==="NEBULA_WAVE41"){\n'
'        gs.score+=2084;showPopup(cx,cy-1794,"+2084 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03c6",1956);if(gs.score>=bonusTotal)unlock("nebula_wave41_max");\n'
'      } else if(ptype==="AURORA_WAVE41"){\n'
'        gs.score+=2086;showPopup(cx,cy-1796,"+2086 🌠",theme.accent,26);spawnShockwave(cx,cy,"#0a089a",1958);if(gs.score>=bonusTotal)unlock("aurora_wave41_max");\n'
'      } else if(ptype==="CRYSTAL_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// CRYSTAL_WAVE41 — +2080 crystal wave bonus'
A4_NEW = ('// NEBULA_WAVE41 — +2084 nebula wave bonus\n'
'      if(ptype==="NEBULA_WAVE41"){sfx("powerUp",1747);unlock("nebula_wave41_use");}\n'
'      // AURORA_WAVE41 — +2086 aurora wave bonus\n'
'      if(ptype==="AURORA_WAVE41"){sfx("powerUp",1749);unlock("aurora_wave41_use");}\n'
'      // CRYSTAL_WAVE41 — +2080 crystal wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawKerniteFox9e('
A5_NEW = (
'function drawLazuriteFox9e(ctx,r,ts,lazPct){\n'
'  const bob=Math.sin(ts*0.3578)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+lazPct*0.35,"#1d4ed8");g.addColorStop(1,"#1e3a8a");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(lazPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(29,78,216,"+(lazPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=lazPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lazPct>0.88?"💙":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLazuliteOrb9e(ctx,r,ts,lazuPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3582);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+lazuPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.35+lazuPct*0.35,"#0ea5e9");g.addColorStop(1,"#0c4a6e");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+lazuPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(14,165,233,"+(0.45+lazuPct*0.55)+")";ctx.lineWidth=3.5+lazuPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(lazuPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(125,211,252,"+(lazuPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=lazuPct>0.88?"#7dd3fc":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lazuPct>0.88?"🩵":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawKerniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="kernite_fox9e"){'
A6_NEW = (
'else if(t.type==="lazurite_fox9e"){\n'
'      const lazPct=Math.min(1,(ts-t.born)/2800);t._lazPct=lazPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLazuriteFox9e(ctx,t.radius,ts,lazPct);ctx.restore();\n'
'    } else if(t.type==="lazulite_orb9e"){\n'
'      const lazuPct=Math.min(1,(ts-t.born)/2800);t._lazuPct=lazuPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLazuliteOrb9e(ctx,t.radius,ts,lazuPct);ctx.restore();\n'
'    } else if(t.type==="kernite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="kernite_fox9e"){'
A7_NEW = (
'if(hit.type==="lazurite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(294*(hit._lazPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#1d4ed8",1930);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("lazurite_fox9e_tap");\n'
'        if((hit._lazPct||0)>0.88)unlock("lazurite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="lazulite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(289*(hit._lazuPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#0ea5e9",1932);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("lazulite_orb9e_tap");\n'
'        if((hit._lazuPct||0)>0.88)unlock("lazulite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="kernite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="kernite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kinoite_orb9e"')
A8_NEW = ('      type="lazurite_fox9e";color="#1d4ed8";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lazulite_orb9e";color="#0ea5e9";glow="#f0f9ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kernite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kinoite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="kernite_fox9e"?BASE_R*1.22:type==="kinoite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="lazurite_fox9e"?BASE_R*1.22:type==="lazulite_orb9e"?BASE_R*1.21:type==="kernite_fox9e"?BASE_R*1.22:type==="kinoite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'CRYSTAL_WAVE41:"💎💠",PRISM_WAVE41:"🔮💠",'
A10_NEW = 'CRYSTAL_WAVE41:"💎💠",PRISM_WAVE41:"🔮💠",NEBULA_WAVE41:"🌌💠",AURORA_WAVE41:"🌠💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 655 done! +{len(src)-original_len} bytes")
