#!/usr/bin/env python3
# Batch 620: NEXUS_GLOW40 + SOLAR_GLOW40 + MagnesiteFox9e + MarcasiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"leucite_orb9e_peak",    label:"Leucite Orb Peak",            desc:"Tap leucite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_glow40_use",      label:"Nexus Glow 40",              desc:"Activate NEXUS_GLOW40",                 icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_glow40_max",      label:"Nexus Glow Max 40",          desc:"Score 1944 pts in NEXUS_GLOW40",        icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_glow40_use",      label:"Solar Glow 40",               desc:"Activate SOLAR_GLOW40",                 icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_glow40_max",      label:"Solar Glow Max 40",           desc:"Score 1946 pts in SOLAR_GLOW40",        icon:"\U00002600️", xp:88 },'
  '\n  { id:"magnesite_fox9e_tap",   label:"Magnesite Fox",               desc:"Tap magnesite_fox9e",                   icon:"\U0001f98a", xp:44 },'
  '\n  { id:"magnesite_fox9e_peak",  label:"Magnesite Fox Peak",          desc:"Tap magnesite_fox9e at >85% charge",    icon:"\U0001f98a", xp:88 },'
  '\n  { id:"marcasite_orb9e_tap",   label:"Marcasite Orb",               desc:"Tap marcasite_orb9e",                   icon:"\U0001f52e", xp:44 },'
  '\n  { id:"marcasite_orb9e_peak",  label:"Marcasite Orb Peak",          desc:"Tap marcasite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_RING40","THUNDER_RING40",'
A2_NEW = '"NEXUS_GLOW40","SOLAR_GLOW40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_RING40"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_GLOW40"){\n'
  '    activePwrRef.current.push({type:"NEXUS_GLOW40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1607);\n'
  '    showNotif("\U0001f4ab\U0001f31f NEXUS GLOW 40!");unlock("nexus_glow40_use");\n'
  '  } else if(ptype==="SOLAR_GLOW40"){\n'
  '    activePwrRef.current.push({type:"SOLAR_GLOW40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1609);\n'
  '    showNotif("\U00002600️\U0001f31f SOLAR GLOW 40!");unlock("solar_glow40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_RING40 — +1940 aurora bonus'
A4_NEW = (
  '// NEXUS_GLOW40 — +1944 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_GLOW40")){\n'
  '    const bonusTotal=Math.round(92.2*1000);\n'
  '    gs.score+=1944;showPopup(cx,cy-1654,"+1944 \U0001f4ab\U0001f31f",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0380",1816);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_glow40_max");\n'
  '  }\n'
  '  // SOLAR_GLOW40 — +1946 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_GLOW40")){\n'
  '    const bonusTotal=Math.round(92.3*1000);\n'
  '    gs.score+=1946;showPopup(cx,cy-1656,"+1946 \U00002600️\U0001f31f",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0854",1818);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_glow40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawLepidoliteFox9e('
FOX_FN = (
  'function drawMagnesiteFox9e(ctx,r,ts,magPct){\n'
  '  const bob=Math.sin(ts*0.3298)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+magPct*0.35,"#fde68a");g.addColorStop(1,"#a16207");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(magPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(253,230,138,"+(magPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=magPct>0.88?"#fcd34d":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(magPct>0.88?"\U0001f31f":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawMarcasiteOrb9e(ctx,r,ts,mrcPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3302);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+mrcPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+mrcPct*0.35,"#facc15");g.addColorStop(1,"#854d0e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+mrcPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(250,204,21,"+(0.45+mrcPct*0.55)+")";ctx.lineWidth=3.5+mrcPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(mrcPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(253,224,71,"+(mrcPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=mrcPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(mrcPct>0.88?"⚡":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="lepidolite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="magnesite_fox9e"){\n'
  '    const bf9eMag620=(Math.sin((Date.now()-t.spawnedAt)*0.3298)+1)/2;\n'
  '    t._bf9eMag620=bf9eMag620;\n'
  '    drawMagnesiteFox9e(ctx,t.radius,ts,bf9eMag620);\n'
  '  }\n'
  '  else if(t.type==="marcasite_orb9e"){\n'
  '    const ao9eMrc620=(Math.sin((Date.now()-t.spawnedAt)*0.3302)+1)/2;\n'
  '    t._ao9eMrc620=ao9eMrc620;\n'
  '    drawMarcasiteOrb9e(ctx,t.radius,ts,ao9eMrc620);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="lepidolite_fox9e"){'
A7_NEW = (
  'if(hit.type==="magnesite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo620bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult620bf=gs.feverActive?2:1;\n'
  '      const isPeak620bf=((hit._bf9eMag620||0)>0.85);\n'
  '      const pts620bf=Math.round((isPeak620bf?550:360)*combo620bf*feverMult620bf);\n'
  '      gs.score+=pts620bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1790,"#fde68a");\n'
  '      if(isPeak620bf){spawnPopup(hit.x,hit.y-28,"\U0001f31f +"+pts620bf,theme.accent);unlock("magnesite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts620bf,theme.accent);}\n'
  '      unlock("magnesite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="marcasite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo620ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult620ao=gs.feverActive?2:1;\n'
  '      const isPeak620ao=((hit._ao9eMrc620||0)>0.85);\n'
  '      const pts620ao=Math.round((isPeak620ao?552:362)*combo620ao*feverMult620ao);\n'
  '      gs.score+=pts620ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1792,"#facc15");\n'
  '      if(isPeak620ao){spawnPopup(hit.x,hit.y-28,"⚡ +"+pts620ao,theme.accent);unlock("marcasite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts620ao,theme.accent);}\n'
  '      unlock("marcasite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="lepidolite_fox9e";color="#a855f7";glow="#faf5ff";'
A8_NEW = (
  'type="magnesite_fox9e";color="#fde68a";glow="#fefce8";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="marcasite_orb9e";color="#facc15";glow="#fefce8";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="lepidolite_fox9e"?BASE_R*1.06:type==="leucite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="magnesite_fox9e"?BASE_R*1.06:type==="marcasite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_RING40:"\U0001f30c\U0001f48d",THUNDER_RING40:"⚡\U0001f48d",'
A10_NEW = 'NEXUS_GLOW40:"\U0001f4ab\U0001f31f",SOLAR_GLOW40:"\U00002600️\U0001f31f",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 620 done! +{delta} bytes")
