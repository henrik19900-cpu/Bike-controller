#!/usr/bin/env python3
# Batch 606: NEXUS_TIDE39B10 + SOLAR_CREST39B10 + BiotiteFox9e + ApatiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"alunite_orb9e_peak",     label:"Alunite Orb Peak",        desc:"Tap alunite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_tide39b10_use",   label:"Nexus Tide 39B10",        desc:"Activate NEXUS_TIDE39B10",              icon:"\U0001f30a", xp:44 },'
  '\n  { id:"nexus_tide39b10_max",   label:"Nexus Tide Max 39B10",     desc:"Score 1888 pts in NEXUS_TIDE39B10",     icon:"\U0001f30a", xp:88 },'
  '\n  { id:"solar_crest39b10_use",  label:"Solar Crest 39B10",        desc:"Activate SOLAR_CREST39B10",             icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_crest39b10_max",  label:"Solar Crest Max 39B10",    desc:"Score 1890 pts in SOLAR_CREST39B10",    icon:"\U00002600️", xp:88 },'
  '\n  { id:"biotite_fox9e_tap",     label:"Biotite Fox",              desc:"Tap biotite_fox9e",                     icon:"\U0001f98a", xp:44 },'
  '\n  { id:"biotite_fox9e_peak",    label:"Biotite Fox Peak",         desc:"Tap biotite_fox9e at >85% charge",      icon:"\U0001f98a", xp:88 },'
  '\n  { id:"apatite_orb9e_tap",     label:"Apatite Orb",              desc:"Tap apatite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"apatite_orb9e_peak",    label:"Apatite Orb Peak",         desc:"Tap apatite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_EMBER39B10","THUNDER_TIDE39B10",'
A2_NEW = '"NEXUS_TIDE39B10","SOLAR_CREST39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_EMBER39B10"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_TIDE39B10"){\n'
  '    activePwrRef.current.push({type:"NEXUS_TIDE39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1551);\n'
  '    showNotif("\U0001f30a\U0001f300 NEXUS TIDE 39B10!");unlock("nexus_tide39b10_use");\n'
  '  } else if(ptype==="SOLAR_CREST39B10"){\n'
  '    activePwrRef.current.push({type:"SOLAR_CREST39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1553);\n'
  '    showNotif("\U00002600️\U0001f451 SOLAR CREST 39B10!");unlock("solar_crest39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_EMBER39B10 — +1884 aurora bonus'
A4_NEW = (
  '// NEXUS_TIDE39B10 — +1888 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_TIDE39B10")){\n'
  '    const bonusTotal=Math.round(89.4*1000);\n'
  '    gs.score+=1888;showPopup(cx,cy-1598,"+1888 \U0001f30a\U0001f300",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0364",1760);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_tide39b10_max");\n'
  '  }\n'
  '  // SOLAR_CREST39B10 — +1890 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_CREST39B10")){\n'
  '    const bonusTotal=Math.round(89.5*1000);\n'
  '    gs.score+=1890;showPopup(cx,cy-1600,"+1890 \U00002600️\U0001f451",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0838",1762);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_crest39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBauxiteFox9e('
FOX_FN = (
  'function drawBiotiteFox9e(ctx,r,ts,bioPct){\n'
  '  const bob=Math.sin(ts*0.3186)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.45+bioPct*0.35,"#713f12");g.addColorStop(1,"#422006");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(bioPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(113,63,18,"+(bioPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=bioPct>0.88?"#fde68a":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(bioPct>0.88?"\U0001fab8":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawApatiteOrb9e(ctx,r,ts,apaPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3190);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+apaPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.35+apaPct*0.35,"#6ee7b7");g.addColorStop(1,"#065f46");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+apaPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(110,231,183,"+(0.45+apaPct*0.55)+")";ctx.lineWidth=3.5+apaPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(apaPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(167,243,208,"+(apaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=apaPct>0.88?"#a7f3d0":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(apaPct>0.88?"\U0001f9a2":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="bauxite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="biotite_fox9e"){\n'
  '    const bf9eBio606=(Math.sin((Date.now()-t.spawnedAt)*0.3186)+1)/2;\n'
  '    t._bf9eBio606=bf9eBio606;\n'
  '    drawBiotiteFox9e(ctx,t.radius,ts,bf9eBio606);\n'
  '  }\n'
  '  else if(t.type==="apatite_orb9e"){\n'
  '    const ao9eApa606=(Math.sin((Date.now()-t.spawnedAt)*0.3190)+1)/2;\n'
  '    t._ao9eApa606=ao9eApa606;\n'
  '    drawApatiteOrb9e(ctx,t.radius,ts,ao9eApa606);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="bauxite_fox9e"){'
A7_NEW = (
  'if(hit.type==="biotite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo606bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult606bf=gs.feverActive?2:1;\n'
  '      const isPeak606bf=((hit._bf9eBio606||0)>0.85);\n'
  '      const pts606bf=Math.round((isPeak606bf?494:304)*combo606bf*feverMult606bf);\n'
  '      gs.score+=pts606bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1734,"#713f12");\n'
  '      if(isPeak606bf){spawnPopup(hit.x,hit.y-28,"\U0001fab8 +"+pts606bf,theme.accent);unlock("biotite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts606bf,theme.accent);}\n'
  '      unlock("biotite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="apatite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo606ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult606ao=gs.feverActive?2:1;\n'
  '      const isPeak606ao=((hit._ao9eApa606||0)>0.85);\n'
  '      const pts606ao=Math.round((isPeak606ao?496:306)*combo606ao*feverMult606ao);\n'
  '      gs.score+=pts606ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1736,"#6ee7b7");\n'
  '      if(isPeak606ao){spawnPopup(hit.x,hit.y-28,"\U0001f9a2 +"+pts606ao,theme.accent);unlock("apatite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts606ao,theme.accent);}\n'
  '      unlock("apatite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="bauxite_fox9e";color="#b45309";glow="#fffbeb";'
A8_NEW = (
  'type="biotite_fox9e";color="#713f12";glow="#fef9c3";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="apatite_orb9e";color="#6ee7b7";glow="#ecfdf5";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="bauxite_fox9e"?BASE_R*1.06:type==="alunite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="biotite_fox9e"?BASE_R*1.06:type==="apatite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_EMBER39B10:"\U0001f30c\U0001f525",THUNDER_TIDE39B10:"\U0001f30a⚡",'
A10_NEW = 'NEXUS_TIDE39B10:"\U0001f30a\U0001f300",SOLAR_CREST39B10:"\U00002600️\U0001f451",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 606 done! +{delta} bytes")
