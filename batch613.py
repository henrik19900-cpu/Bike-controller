#!/usr/bin/env python3
# Batch 613: AURORA_FLUX40 + THUNDER_STREAK40 + FluoriteFox9e + FrankliniteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"epsomite_orb9e_peak",    label:"Epsomite Orb Peak",          desc:"Tap epsomite_orb9e at >85%",           icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_flux40_use",      label:"Aurora Flux 40",             desc:"Activate AURORA_FLUX40",                icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_flux40_max",      label:"Aurora Flux Max 40",         desc:"Score 1916 pts in AURORA_FLUX40",       icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_streak40_use",   label:"Thunder Streak 40",           desc:"Activate THUNDER_STREAK40",             icon:"⚡", xp:44 },'
  '\n  { id:"thunder_streak40_max",   label:"Thunder Streak Max 40",       desc:"Score 1918 pts in THUNDER_STREAK40",    icon:"⚡", xp:88 },'
  '\n  { id:"fluorite_fox9e_tap",     label:"Fluorite Fox",                desc:"Tap fluorite_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"fluorite_fox9e_peak",    label:"Fluorite Fox Peak",           desc:"Tap fluorite_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"franklinite_orb9e_tap",  label:"Franklinite Orb",             desc:"Tap franklinite_orb9e",                 icon:"\U0001f52e", xp:44 },'
  '\n  { id:"franklinite_orb9e_peak", label:"Franklinite Orb Peak",        desc:"Tap franklinite_orb9e at >85%",        icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_FLUX40","SOLAR_STREAK40",'
A2_NEW = '"AURORA_FLUX40","THUNDER_STREAK40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_FLUX40"){'
A3_NEW = (
  '} else if(ptype==="AURORA_FLUX40"){\n'
  '    activePwrRef.current.push({type:"AURORA_FLUX40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1579);\n'
  '    showNotif("\U0001f30c\U0001f4a0 AURORA FLUX 40!");unlock("aurora_flux40_use");\n'
  '  } else if(ptype==="THUNDER_STREAK40"){\n'
  '    activePwrRef.current.push({type:"THUNDER_STREAK40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1581);\n'
  '    showNotif("⚡\U0001f525 THUNDER STREAK 40!");unlock("thunder_streak40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_FLUX40 — +1912 nexus bonus'
A4_NEW = (
  '// AURORA_FLUX40 — +1916 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_FLUX40")){\n'
  '    const bonusTotal=Math.round(90.8*1000);\n'
  '    gs.score+=1916;showPopup(cx,cy-1626,"+1916 \U0001f30c\U0001f4a0",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0372",1788);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_flux40_max");\n'
  '  }\n'
  '  // THUNDER_STREAK40 — +1918 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_STREAK40")){\n'
  '    const bonusTotal=Math.round(90.9*1000);\n'
  '    gs.score+=1918;showPopup(cx,cy-1628,"+1918 ⚡\U0001f525",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0846",1790);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_streak40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawEnstatiteFox9e('
FOX_FN = (
  'function drawFluoriteFox9e(ctx,r,ts,fluPct){\n'
  '  const bob=Math.sin(ts*0.3242)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#faf5ff");g.addColorStop(0.45+fluPct*0.35,"#7e22ce");g.addColorStop(1,"#4a044e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(fluPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(126,34,206,"+(fluPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=fluPct>0.88?"#c084fc":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(fluPct>0.88?"\U0001f49c":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawFrankliniteOrb9e(ctx,r,ts,fraPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3246);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+fraPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f9fafb");g.addColorStop(0.35+fraPct*0.35,"#374151");g.addColorStop(1,"#111827");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+fraPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(55,65,81,"+(0.45+fraPct*0.55)+")";ctx.lineWidth=3.5+fraPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(fraPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(107,114,128,"+(fraPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=fraPct>0.88?"#6b7280":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(fraPct>0.88?"\U000026ab":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="enstatite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="fluorite_fox9e"){\n'
  '    const bf9eFlu613=(Math.sin((Date.now()-t.spawnedAt)*0.3242)+1)/2;\n'
  '    t._bf9eFlu613=bf9eFlu613;\n'
  '    drawFluoriteFox9e(ctx,t.radius,ts,bf9eFlu613);\n'
  '  }\n'
  '  else if(t.type==="franklinite_orb9e"){\n'
  '    const ao9eFra613=(Math.sin((Date.now()-t.spawnedAt)*0.3246)+1)/2;\n'
  '    t._ao9eFra613=ao9eFra613;\n'
  '    drawFrankliniteOrb9e(ctx,t.radius,ts,ao9eFra613);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="enstatite_fox9e"){'
A7_NEW = (
  'if(hit.type==="fluorite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo613bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult613bf=gs.feverActive?2:1;\n'
  '      const isPeak613bf=((hit._bf9eFlu613||0)>0.85);\n'
  '      const pts613bf=Math.round((isPeak613bf?522:332)*combo613bf*feverMult613bf);\n'
  '      gs.score+=pts613bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1762,"#7e22ce");\n'
  '      if(isPeak613bf){spawnPopup(hit.x,hit.y-28,"\U0001f49c +"+pts613bf,theme.accent);unlock("fluorite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts613bf,theme.accent);}\n'
  '      unlock("fluorite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="franklinite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo613ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult613ao=gs.feverActive?2:1;\n'
  '      const isPeak613ao=((hit._ao9eFra613||0)>0.85);\n'
  '      const pts613ao=Math.round((isPeak613ao?524:334)*combo613ao*feverMult613ao);\n'
  '      gs.score+=pts613ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1764,"#374151");\n'
  '      if(isPeak613ao){spawnPopup(hit.x,hit.y-28,"\U000026ab +"+pts613ao,theme.accent);unlock("franklinite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts613ao,theme.accent);}\n'
  '      unlock("franklinite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="enstatite_fox9e";color="#4c1d95";glow="#f5f3ff";'
A8_NEW = (
  'type="fluorite_fox9e";color="#7e22ce";glow="#faf5ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="franklinite_orb9e";color="#374151";glow="#f9fafb";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="enstatite_fox9e"?BASE_R*1.06:type==="epsomite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="fluorite_fox9e"?BASE_R*1.06:type==="franklinite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_FLUX40:"\U0001f4ab\U0001f30a",SOLAR_STREAK40:"\U00002600️\U0001f525",'
A10_NEW = 'AURORA_FLUX40:"\U0001f30c\U0001f4a0",THUNDER_STREAK40:"⚡\U0001f525",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 613 done! +{delta} bytes")
