import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"fayalite_orb9e_peak", label:"Fayalite Orb Peak", desc:"Reach peak with Fayalite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"blaze_pulse41_use", label:"Blaze Pulse", desc:"Activate BLAZE_PULSE41 power-up", icon:"🔥", xp:60 },\n'
'  { id:"blaze_pulse41_max", label:"Blaze Pulser", desc:"Reach max with BLAZE_PULSE41 active", icon:"🔥", xp:120 },\n'
'  { id:"frost_pulse41_use", label:"Frost Pulse", desc:"Activate FROST_PULSE41 power-up", icon:"❄️", xp:60 },\n'
'  { id:"frost_pulse41_max", label:"Frost Pulser", desc:"Reach max with FROST_PULSE41 active", icon:"❄️", xp:120 },\n'
'  { id:"fergusonite_fox9e_tap", label:"Fergusonite Fox", desc:"Tap a Fergusonite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"fergusonite_fox9e_peak", label:"Fergusonite Fox Peak", desc:"Reach peak with Fergusonite Fox", icon:"🦊", xp:120 },\n'
'  { id:"fuchsite_orb9e_tap", label:"Fuchsite Orb", desc:"Tap a Fuchsite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"fuchsite_orb9e_peak", label:"Fuchsite Orb Peak", desc:"Reach peak with Fuchsite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"VORTEX_PULSE41","RADIANT_PULSE41","PRISM_PULSE41"'
A2_NEW = '"VORTEX_PULSE41","RADIANT_PULSE41","BLAZE_PULSE41","FROST_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="VORTEX_PULSE41"){'
A3_NEW = (
'} else if(ptype==="BLAZE_PULSE41"){\n'
'        gs.score+=2040;showPopup(cx,cy-1750,"+2040 🔥",theme.accent,26);spawnShockwave(cx,cy,"#0a03b0",1912);if(gs.score>=bonusTotal)unlock("blaze_pulse41_max");\n'
'      } else if(ptype==="FROST_PULSE41"){\n'
'        gs.score+=2042;showPopup(cx,cy-1752,"+2042 ❄️",theme.accent,26);spawnShockwave(cx,cy,"#0a0884",1914);if(gs.score>=bonusTotal)unlock("frost_pulse41_max");\n'
'      } else if(ptype==="VORTEX_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// VORTEX_PULSE41 — +2036 vortex bonus'
A4_NEW = ('// BLAZE_PULSE41 — +2040 blaze bonus\n'
'      if(ptype==="BLAZE_PULSE41"){sfx("powerUp",1703);unlock("blaze_pulse41_use");}\n'
'      // FROST_PULSE41 — +2042 frost bonus\n'
'      if(ptype==="FROST_PULSE41"){sfx("powerUp",1705);unlock("frost_pulse41_use");}\n'
'      // VORTEX_PULSE41 — +2036 vortex bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawEuxeniteFox9e('
A5_NEW = (
'function drawFergusoniteFox9e(ctx,r,ts,ferPct){\n'
'  const bob=Math.sin(ts*0.3490)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.45+ferPct*0.35,"#7c3aed");g.addColorStop(1,"#2e1065");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(ferPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(124,58,237,"+(ferPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=ferPct>0.88?"#c4b5fd":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ferPct>0.88?"🟣":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawFuchsiteOrb9e(ctx,r,ts,fucPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3494);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+fucPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+fucPct*0.35,"#15803d");g.addColorStop(1,"#14532d");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+fucPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(21,128,61,"+(0.45+fucPct*0.55)+")";ctx.lineWidth=3.5+fucPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(fucPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(74,222,128,"+(fucPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=fucPct>0.88?"#4ade80":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(fucPct>0.88?"💚":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawEuxeniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="euxenite_fox9e"){'
A6_NEW = (
'else if(t.type==="fergusonite_fox9e"){\n'
'      const ferPct=Math.min(1,(ts-t.born)/2800);t._ferPct=ferPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawFergusoniteFox9e(ctx,t.radius,ts,ferPct);ctx.restore();\n'
'    } else if(t.type==="fuchsite_orb9e"){\n'
'      const fucPct=Math.min(1,(ts-t.born)/2800);t._fucPct=fucPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawFuchsiteOrb9e(ctx,t.radius,ts,fucPct);ctx.restore();\n'
'    } else if(t.type==="euxenite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="euxenite_fox9e"){'
A7_NEW = (
'if(hit.type==="fergusonite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(272*(hit._ferPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#7c3aed",1886);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("fergusonite_fox9e_tap");\n'
'        if((hit._ferPct||0)>0.88)unlock("fergusonite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="fuchsite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(267*(hit._fucPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#15803d",1888);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("fuchsite_orb9e_tap");\n'
'        if((hit._fucPct||0)>0.88)unlock("fuchsite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="euxenite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="euxenite_fox9e";color="#9d174d";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fayalite_orb9e"')
A8_NEW = ('      type="fergusonite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fuchsite_orb9e";color="#15803d";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="euxenite_fox9e";color="#9d174d";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fayalite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="euxenite_fox9e"?BASE_R*1.22:type==="fayalite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="fergusonite_fox9e"?BASE_R*1.22:type==="fuchsite_orb9e"?BASE_R*1.21:type==="euxenite_fox9e"?BASE_R*1.22:type==="fayalite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'VORTEX_PULSE41:"🌀💠",RADIANT_PULSE41:"✨💠",'
A10_NEW = 'VORTEX_PULSE41:"🌀💠",RADIANT_PULSE41:"✨💠",BLAZE_PULSE41:"🔥💠",FROST_PULSE41:"❄️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 644 done! +{len(src)-original_len} bytes")
