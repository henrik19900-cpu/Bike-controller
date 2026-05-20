import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"ludlamite_orb9e_peak", label:"Ludlamite Orb Peak", desc:"Reach peak with Ludlamite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"thunder_wave41_use", label:"Thunder Wave", desc:"Activate THUNDER_WAVE41 power-up", icon:"⚡", xp:60 },\n'
'  { id:"thunder_wave41_max", label:"Thunder Waver", desc:"Reach max with THUNDER_WAVE41 active", icon:"⚡", xp:120 },\n'
'  { id:"blizzard_wave41_use", label:"Blizzard Wave", desc:"Activate BLIZZARD_WAVE41 power-up", icon:"🌨️", xp:60 },\n'
'  { id:"blizzard_wave41_max", label:"Blizzard Waver", desc:"Reach max with BLIZZARD_WAVE41 active", icon:"🌨️", xp:120 },\n'
'  { id:"manganite_fox9e_tap", label:"Manganite Fox", desc:"Tap a Manganite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"manganite_fox9e_peak", label:"Manganite Fox Peak", desc:"Reach peak with Manganite Fox", icon:"🦊", xp:120 },\n'
'  { id:"melanterite_orb9e_tap", label:"Melanterite Orb", desc:"Tap a Melanterite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"melanterite_orb9e_peak", label:"Melanterite Orb Peak", desc:"Reach peak with Melanterite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"RADIANCE_WAVE41","VOID_PULSE41","PRISM_PULSE41"'
A2_NEW = '"RADIANCE_WAVE41","VOID_PULSE41","THUNDER_WAVE41","BLIZZARD_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="RADIANCE_WAVE41"){'
A3_NEW = (
'} else if(ptype==="THUNDER_WAVE41"){\n'
'        gs.score+=2104;showPopup(cx,cy-1814,"+2104 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03d0",1976);if(gs.score>=bonusTotal)unlock("thunder_wave41_max");\n'
'      } else if(ptype==="BLIZZARD_WAVE41"){\n'
'        gs.score+=2106;showPopup(cx,cy-1816,"+2106 🌨️",theme.accent,26);spawnShockwave(cx,cy,"#0a08a4",1978);if(gs.score>=bonusTotal)unlock("blizzard_wave41_max");\n'
'      } else if(ptype==="RADIANCE_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// RADIANCE_WAVE41 — +2100 radiance wave bonus'
A4_NEW = ('// THUNDER_WAVE41 — +2104 thunder wave bonus\n'
'      if(ptype==="THUNDER_WAVE41"){sfx("powerUp",1767);unlock("thunder_wave41_use");}\n'
'      // BLIZZARD_WAVE41 — +2106 blizzard wave bonus\n'
'      if(ptype==="BLIZZARD_WAVE41"){sfx("powerUp",1769);unlock("blizzard_wave41_use");}\n'
'      // RADIANCE_WAVE41 — +2100 radiance wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawLoseyiteFox9e('
A5_NEW = (
'function drawManganiteFox9e(ctx,r,ts,manPct){\n'
'  const bob=Math.sin(ts*0.3618)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f9fafb");g.addColorStop(0.45+manPct*0.35,"#4b5563");g.addColorStop(1,"#111827");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(manPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(75,85,99,"+(manPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=manPct>0.88?"#9ca3af":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(manPct>0.88?"🖤":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawMelanteriteOrb9e(ctx,r,ts,melPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3622);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+melPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.35+melPct*0.35,"#10b981");g.addColorStop(1,"#064e3b");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+melPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(16,185,129,"+(0.45+melPct*0.55)+")";ctx.lineWidth=3.5+melPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(melPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(52,211,153,"+(melPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=melPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(melPct>0.88?"🌊":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLoseyiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="loseyite_fox9e"){'
A6_NEW = (
'else if(t.type==="manganite_fox9e"){\n'
'      const manPct=Math.min(1,(ts-t.born)/2800);t._manPct=manPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawManganiteFox9e(ctx,t.radius,ts,manPct);ctx.restore();\n'
'    } else if(t.type==="melanterite_orb9e"){\n'
'      const melPct=Math.min(1,(ts-t.born)/2800);t._melPct=melPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawMelanteriteOrb9e(ctx,t.radius,ts,melPct);ctx.restore();\n'
'    } else if(t.type==="loseyite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="loseyite_fox9e"){'
A7_NEW = (
'if(hit.type==="manganite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(304*(hit._manPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#4b5563",1950);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("manganite_fox9e_tap");\n'
'        if((hit._manPct||0)>0.88)unlock("manganite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="melanterite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(299*(hit._melPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#10b981",1952);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("melanterite_orb9e_tap");\n'
'        if((hit._melPct||0)>0.88)unlock("melanterite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="loseyite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="loseyite_fox9e";color="#9ca3af";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="ludlamite_orb9e"')
A8_NEW = ('      type="manganite_fox9e";color="#4b5563";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="melanterite_orb9e";color="#10b981";glow="#ecfdf5";\n'
           '    } else if('+COND100F+'){\n'
           '      type="loseyite_fox9e";color="#9ca3af";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="ludlamite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="loseyite_fox9e"?BASE_R*1.22:type==="ludlamite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="manganite_fox9e"?BASE_R*1.22:type==="melanterite_orb9e"?BASE_R*1.21:type==="loseyite_fox9e"?BASE_R*1.22:type==="ludlamite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'RADIANCE_WAVE41:"✨💠",VOID_PULSE41:"🌑💠",'
A10_NEW = 'RADIANCE_WAVE41:"✨💠",VOID_PULSE41:"🌑💠",THUNDER_WAVE41:"⚡💠",BLIZZARD_WAVE41:"🌨️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 660 done! +{len(src)-original_len} bytes")
