#!/usr/bin/env python3
# Batch 612: NEXUS_FLUX40 + SOLAR_STREAK40 + EnstatiteFox9e + EpsomiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"dolomite_orb9e_peak",    label:"Dolomite Orb Peak",          desc:"Tap dolomite_orb9e at >85%",           icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_flux40_use",       label:"Nexus Flux 40",             desc:"Activate NEXUS_FLUX40",                 icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_flux40_max",       label:"Nexus Flux Max 40",         desc:"Score 1912 pts in NEXUS_FLUX40",        icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_streak40_use",     label:"Solar Streak 40",            desc:"Activate SOLAR_STREAK40",               icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_streak40_max",     label:"Solar Streak Max 40",        desc:"Score 1914 pts in SOLAR_STREAK40",      icon:"\U00002600️", xp:88 },'
  '\n  { id:"enstatite_fox9e_tap",    label:"Enstatite Fox",              desc:"Tap enstatite_fox9e",                   icon:"\U0001f98a", xp:44 },'
  '\n  { id:"enstatite_fox9e_peak",   label:"Enstatite Fox Peak",         desc:"Tap enstatite_fox9e at >85% charge",    icon:"\U0001f98a", xp:88 },'
  '\n  { id:"epsomite_orb9e_tap",     label:"Epsomite Orb",               desc:"Tap epsomite_orb9e",                    icon:"\U0001f52e", xp:44 },'
  '\n  { id:"epsomite_orb9e_peak",    label:"Epsomite Orb Peak",          desc:"Tap epsomite_orb9e at >85%",           icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_NOVA39B10","THUNDER_WAVE39B10",'
A2_NEW = '"NEXUS_FLUX40","SOLAR_STREAK40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_NOVA39B10"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_FLUX40"){\n'
  '    activePwrRef.current.push({type:"NEXUS_FLUX40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1575);\n'
  '    showNotif("\U0001f4ab\U0001f30a NEXUS FLUX 40!");unlock("nexus_flux40_use");\n'
  '  } else if(ptype==="SOLAR_STREAK40"){\n'
  '    activePwrRef.current.push({type:"SOLAR_STREAK40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1577);\n'
  '    showNotif("\U00002600️\U0001f525 SOLAR STREAK 40!");unlock("solar_streak40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_NOVA39B10 — +1908 aurora bonus'
A4_NEW = (
  '// NEXUS_FLUX40 — +1912 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_FLUX40")){\n'
  '    const bonusTotal=Math.round(90.6*1000);\n'
  '    gs.score+=1912;showPopup(cx,cy-1622,"+1912 \U0001f4ab\U0001f30a",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0370",1784);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_flux40_max");\n'
  '  }\n'
  '  // SOLAR_STREAK40 — +1914 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_STREAK40")){\n'
  '    const bonusTotal=Math.round(90.7*1000);\n'
  '    gs.score+=1914;showPopup(cx,cy-1624,"+1914 \U00002600️\U0001f525",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0844",1786);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_streak40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawDiopsideFox9e('
FOX_FN = (
  'function drawEnstatiteFox9e(ctx,r,ts,ensPct){\n'
  '  const bob=Math.sin(ts*0.3234)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f5f3ff");g.addColorStop(0.45+ensPct*0.35,"#4c1d95");g.addColorStop(1,"#2e1065");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(ensPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(76,29,149,"+(ensPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=ensPct>0.88?"#a78bfa":"#f5f3ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ensPct>0.88?"\U0001fad0":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawEpsomiteOrb9e(ctx,r,ts,epsPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3238);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+epsPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fffbeb");g.addColorStop(0.35+epsPct*0.35,"#fbbf24");g.addColorStop(1,"#92400e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+epsPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(251,191,36,"+(0.45+epsPct*0.55)+")";ctx.lineWidth=3.5+epsPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(epsPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(252,211,77,"+(epsPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=epsPct>0.88?"#fcd34d":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(epsPct>0.88?"\U00002728":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="diopside_fox9e"){'
A6_NEW = (
  '  else if(t.type==="enstatite_fox9e"){\n'
  '    const bf9eEns612=(Math.sin((Date.now()-t.spawnedAt)*0.3234)+1)/2;\n'
  '    t._bf9eEns612=bf9eEns612;\n'
  '    drawEnstatiteFox9e(ctx,t.radius,ts,bf9eEns612);\n'
  '  }\n'
  '  else if(t.type==="epsomite_orb9e"){\n'
  '    const ao9eEps612=(Math.sin((Date.now()-t.spawnedAt)*0.3238)+1)/2;\n'
  '    t._ao9eEps612=ao9eEps612;\n'
  '    drawEpsomiteOrb9e(ctx,t.radius,ts,ao9eEps612);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="diopside_fox9e"){'
A7_NEW = (
  'if(hit.type==="enstatite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo612bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult612bf=gs.feverActive?2:1;\n'
  '      const isPeak612bf=((hit._bf9eEns612||0)>0.85);\n'
  '      const pts612bf=Math.round((isPeak612bf?518:328)*combo612bf*feverMult612bf);\n'
  '      gs.score+=pts612bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1758,"#4c1d95");\n'
  '      if(isPeak612bf){spawnPopup(hit.x,hit.y-28,"\U0001fad0 +"+pts612bf,theme.accent);unlock("enstatite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts612bf,theme.accent);}\n'
  '      unlock("enstatite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="epsomite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo612ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult612ao=gs.feverActive?2:1;\n'
  '      const isPeak612ao=((hit._ao9eEps612||0)>0.85);\n'
  '      const pts612ao=Math.round((isPeak612ao?520:330)*combo612ao*feverMult612ao);\n'
  '      gs.score+=pts612ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1760,"#fbbf24");\n'
  '      if(isPeak612ao){spawnPopup(hit.x,hit.y-28,"\U00002728 +"+pts612ao,theme.accent);unlock("epsomite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts612ao,theme.accent);}\n'
  '      unlock("epsomite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="diopside_fox9e";color="#059669";glow="#ecfdf5";'
A8_NEW = (
  'type="enstatite_fox9e";color="#4c1d95";glow="#f5f3ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="epsomite_orb9e";color="#fbbf24";glow="#fffbeb";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="diopside_fox9e"?BASE_R*1.06:type==="dolomite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="enstatite_fox9e"?BASE_R*1.06:type==="epsomite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_NOVA39B10:"\U0001f30c\U0001f4ab",THUNDER_WAVE39B10:"⚡〰️",'
A10_NEW = 'NEXUS_FLUX40:"\U0001f4ab\U0001f30a",SOLAR_STREAK40:"\U00002600️\U0001f525",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 612 done! +{delta} bytes")
