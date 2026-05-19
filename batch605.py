#!/usr/bin/env python3
# Batch 605: AURORA_EMBER39B10 + THUNDER_TIDE39B10 + BauxiteFox9e + AluniteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"arsenolite_orb9e_peak", label:"Arsenolite Orb Peak",    desc:"Tap arsenolite_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_ember39b10_use",  label:"Aurora Ember 39B10",     desc:"Activate AURORA_EMBER39B10",            icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_ember39b10_max",  label:"Aurora Ember Max 39B10",  desc:"Score 1884 pts in AURORA_EMBER39B10",   icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_tide39b10_use",  label:"Thunder Tide 39B10",      desc:"Activate THUNDER_TIDE39B10",            icon:"\U0001f30a", xp:44 },'
  '\n  { id:"thunder_tide39b10_max",  label:"Thunder Tide Max 39B10",  desc:"Score 1886 pts in THUNDER_TIDE39B10",   icon:"\U0001f30a", xp:88 },'
  '\n  { id:"bauxite_fox9e_tap",      label:"Bauxite Fox",             desc:"Tap bauxite_fox9e",                     icon:"\U0001f98a", xp:44 },'
  '\n  { id:"bauxite_fox9e_peak",     label:"Bauxite Fox Peak",        desc:"Tap bauxite_fox9e at >85% charge",      icon:"\U0001f98a", xp:88 },'
  '\n  { id:"alunite_orb9e_tap",      label:"Alunite Orb",             desc:"Tap alunite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"alunite_orb9e_peak",     label:"Alunite Orb Peak",        desc:"Tap alunite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_EMBER39B10","SOLAR_NOVA39B10","AURORA_WAVE39B10"'
A2_NEW = '"AURORA_EMBER39B10","THUNDER_TIDE39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_EMBER39B10"){'
A3_NEW = (
  '} else if(ptype==="AURORA_EMBER39B10"){\n'
  '    activePwrRef.current.push({type:"AURORA_EMBER39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1547);\n'
  '    showNotif("\U0001f30c\U0001f525 AURORA EMBER 39B10!");unlock("aurora_ember39b10_use");\n'
  '  } else if(ptype==="THUNDER_TIDE39B10"){\n'
  '    activePwrRef.current.push({type:"THUNDER_TIDE39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1549);\n'
  '    showNotif("\U0001f30a⚡ THUNDER TIDE 39B10!");unlock("thunder_tide39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_EMBER39B10 — +1880 nexus bonus'
A4_NEW = (
  '// AURORA_EMBER39B10 — +1884 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_EMBER39B10")){\n'
  '    const bonusTotal=Math.round(89.2*1000);\n'
  '    gs.score+=1884;showPopup(cx,cy-1594,"+1884 \U0001f30c\U0001f525",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0362",1756);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_ember39b10_max");\n'
  '  }\n'
  '  // THUNDER_TIDE39B10 — +1886 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_TIDE39B10")){\n'
  '    const bonusTotal=Math.round(89.3*1000);\n'
  '    gs.score+=1886;showPopup(cx,cy-1596,"+1886 \U0001f30a⚡",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0836",1758);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_tide39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawAzuriteFox9e('
FOX_FN = (
  'function drawBauxiteFox9e(ctx,r,ts,baxPct){\n'
  '  const bob=Math.sin(ts*0.3178)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fffbeb");g.addColorStop(0.45+baxPct*0.35,"#b45309");g.addColorStop(1,"#78350f");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(baxPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(180,83,9,"+(baxPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=baxPct>0.88?"#fef3c7":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(baxPct>0.88?"\U0001f3d4️":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawAluniteOrb9e(ctx,r,ts,alnPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3182);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+alnPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fafafa");g.addColorStop(0.35+alnPct*0.35,"#d4d4d8");g.addColorStop(1,"#71717a");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+alnPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(250,250,250,"+(0.45+alnPct*0.55)+")";ctx.lineWidth=3.5+alnPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(alnPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(212,212,216,"+(alnPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=alnPct>0.88?"#e4e4e7":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(alnPct>0.88?"\U0001fab6":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="azurite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="bauxite_fox9e"){\n'
  '    const bf9eBax605=(Math.sin((Date.now()-t.spawnedAt)*0.3178)+1)/2;\n'
  '    t._bf9eBax605=bf9eBax605;\n'
  '    drawBauxiteFox9e(ctx,t.radius,ts,bf9eBax605);\n'
  '  }\n'
  '  else if(t.type==="alunite_orb9e"){\n'
  '    const ao9eAln605=(Math.sin((Date.now()-t.spawnedAt)*0.3182)+1)/2;\n'
  '    t._ao9eAln605=ao9eAln605;\n'
  '    drawAluniteOrb9e(ctx,t.radius,ts,ao9eAln605);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="azurite_fox9e"){'
A7_NEW = (
  'if(hit.type==="bauxite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo605bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult605bf=gs.feverActive?2:1;\n'
  '      const isPeak605bf=((hit._bf9eBax605||0)>0.85);\n'
  '      const pts605bf=Math.round((isPeak605bf?490:300)*combo605bf*feverMult605bf);\n'
  '      gs.score+=pts605bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1730,"#b45309");\n'
  '      if(isPeak605bf){spawnPopup(hit.x,hit.y-28,"\U0001f3d4️ +"+pts605bf,theme.accent);unlock("bauxite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts605bf,theme.accent);}\n'
  '      unlock("bauxite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="alunite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo605ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult605ao=gs.feverActive?2:1;\n'
  '      const isPeak605ao=((hit._ao9eAln605||0)>0.85);\n'
  '      const pts605ao=Math.round((isPeak605ao?492:302)*combo605ao*feverMult605ao);\n'
  '      gs.score+=pts605ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1732,"#d4d4d8");\n'
  '      if(isPeak605ao){spawnPopup(hit.x,hit.y-28,"\U0001fab6 +"+pts605ao,theme.accent);unlock("alunite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts605ao,theme.accent);}\n'
  '      unlock("alunite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="azurite_fox9e";color="#1d4ed8";glow="#eff6ff";'
A8_NEW = (
  'type="bauxite_fox9e";color="#b45309";glow="#fffbeb";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="alunite_orb9e";color="#d4d4d8";glow="#fafafa";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="azurite_fox9e"?BASE_R*1.06:type==="arsenolite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="bauxite_fox9e"?BASE_R*1.06:type==="alunite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_EMBER39B10:"\U0001f4ab\U0001f525",SOLAR_NOVA39B10:"☀️\U0001f4a5",AURORA_WAVE39B10:"\U0001f30c〰️"'
A10_NEW = 'AURORA_EMBER39B10:"\U0001f30c\U0001f525",THUNDER_TIDE39B10:"\U0001f30a⚡",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 605 done! +{delta} bytes")
