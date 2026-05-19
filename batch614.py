#!/usr/bin/env python3
# Batch 614: NEXUS_PULSE40 + SOLAR_PULSE40 + GahniteFox9e + GedriteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"franklinite_orb9e_peak", label:"Franklinite Orb Peak",        desc:"Tap franklinite_orb9e at >85%",        icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_pulse40_use",     label:"Nexus Pulse 40",             desc:"Activate NEXUS_PULSE40",                icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_pulse40_max",     label:"Nexus Pulse Max 40",         desc:"Score 1920 pts in NEXUS_PULSE40",       icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_pulse40_use",     label:"Solar Pulse 40",              desc:"Activate SOLAR_PULSE40",                icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_pulse40_max",     label:"Solar Pulse Max 40",          desc:"Score 1922 pts in SOLAR_PULSE40",       icon:"\U00002600️", xp:88 },'
  '\n  { id:"gahnite_fox9e_tap",     label:"Gahnite Fox",                 desc:"Tap gahnite_fox9e",                     icon:"\U0001f98a", xp:44 },'
  '\n  { id:"gahnite_fox9e_peak",    label:"Gahnite Fox Peak",            desc:"Tap gahnite_fox9e at >85% charge",      icon:"\U0001f98a", xp:88 },'
  '\n  { id:"gedrite_orb9e_tap",     label:"Gedrite Orb",                 desc:"Tap gedrite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"gedrite_orb9e_peak",    label:"Gedrite Orb Peak",            desc:"Tap gedrite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_FLUX40","THUNDER_STREAK40",'
A2_NEW = '"NEXUS_PULSE40","SOLAR_PULSE40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_FLUX40"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_PULSE40"){\n'
  '    activePwrRef.current.push({type:"NEXUS_PULSE40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1583);\n'
  '    showNotif("\U0001f4ab\U0001f49a NEXUS PULSE 40!");unlock("nexus_pulse40_use");\n'
  '  } else if(ptype==="SOLAR_PULSE40"){\n'
  '    activePwrRef.current.push({type:"SOLAR_PULSE40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1585);\n'
  '    showNotif("\U00002600️\U0001f49b SOLAR PULSE 40!");unlock("solar_pulse40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_FLUX40 — +1916 aurora bonus'
A4_NEW = (
  '// NEXUS_PULSE40 — +1920 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_PULSE40")){\n'
  '    const bonusTotal=Math.round(91.0*1000);\n'
  '    gs.score+=1920;showPopup(cx,cy-1630,"+1920 \U0001f4ab\U0001f49a",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0374",1792);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_pulse40_max");\n'
  '  }\n'
  '  // SOLAR_PULSE40 — +1922 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_PULSE40")){\n'
  '    const bonusTotal=Math.round(91.1*1000);\n'
  '    gs.score+=1922;showPopup(cx,cy-1632,"+1922 \U00002600️\U0001f49b",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0848",1794);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_pulse40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawFluoriteFox9e('
FOX_FN = (
  'function drawGahniteFox9e(ctx,r,ts,gahPct){\n'
  '  const bob=Math.sin(ts*0.3250)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+gahPct*0.35,"#1e3a5f");g.addColorStop(1,"#0f172a");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(gahPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(30,58,95,"+(gahPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=gahPct>0.88?"#60a5fa":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gahPct>0.88?"\U0001fad0":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawGedriteOrb9e(ctx,r,ts,gedPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3254);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+gedPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+gedPct*0.35,"#a16207");g.addColorStop(1,"#713f12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+gedPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(161,98,7,"+(0.45+gedPct*0.55)+")";ctx.lineWidth=3.5+gedPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(gedPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(202,138,4,"+(gedPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=gedPct>0.88?"#fbbf24":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gedPct>0.88?"\U0001f33e":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="fluorite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="gahnite_fox9e"){\n'
  '    const bf9eGah614=(Math.sin((Date.now()-t.spawnedAt)*0.3250)+1)/2;\n'
  '    t._bf9eGah614=bf9eGah614;\n'
  '    drawGahniteFox9e(ctx,t.radius,ts,bf9eGah614);\n'
  '  }\n'
  '  else if(t.type==="gedrite_orb9e"){\n'
  '    const ao9eGed614=(Math.sin((Date.now()-t.spawnedAt)*0.3254)+1)/2;\n'
  '    t._ao9eGed614=ao9eGed614;\n'
  '    drawGedriteOrb9e(ctx,t.radius,ts,ao9eGed614);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="fluorite_fox9e"){'
A7_NEW = (
  'if(hit.type==="gahnite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo614bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult614bf=gs.feverActive?2:1;\n'
  '      const isPeak614bf=((hit._bf9eGah614||0)>0.85);\n'
  '      const pts614bf=Math.round((isPeak614bf?526:336)*combo614bf*feverMult614bf);\n'
  '      gs.score+=pts614bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1766,"#1e3a5f");\n'
  '      if(isPeak614bf){spawnPopup(hit.x,hit.y-28,"\U0001fad0 +"+pts614bf,theme.accent);unlock("gahnite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts614bf,theme.accent);}\n'
  '      unlock("gahnite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="gedrite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo614ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult614ao=gs.feverActive?2:1;\n'
  '      const isPeak614ao=((hit._ao9eGed614||0)>0.85);\n'
  '      const pts614ao=Math.round((isPeak614ao?528:338)*combo614ao*feverMult614ao);\n'
  '      gs.score+=pts614ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1768,"#a16207");\n'
  '      if(isPeak614ao){spawnPopup(hit.x,hit.y-28,"\U0001f33e +"+pts614ao,theme.accent);unlock("gedrite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts614ao,theme.accent);}\n'
  '      unlock("gedrite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="fluorite_fox9e";color="#7e22ce";glow="#faf5ff";'
A8_NEW = (
  'type="gahnite_fox9e";color="#1e3a5f";glow="#eff6ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="gedrite_orb9e";color="#a16207";glow="#fef9c3";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="fluorite_fox9e"?BASE_R*1.06:type==="franklinite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="gahnite_fox9e"?BASE_R*1.06:type==="gedrite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_FLUX40:"\U0001f30c\U0001f4a0",THUNDER_STREAK40:"⚡\U0001f525",'
A10_NEW = 'NEXUS_PULSE40:"\U0001f4ab\U0001f49a",SOLAR_PULSE40:"\U00002600️\U0001f49b",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 614 done! +{delta} bytes")
