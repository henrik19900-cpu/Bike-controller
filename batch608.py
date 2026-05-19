#!/usr/bin/env python3
# Batch 608: NEXUS_STORM39B10 + SOLAR_WAVE39B10 + BruciteFox9e + BustamiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"berlinite_orb9e_peak",   label:"Berlinite Orb Peak",       desc:"Tap berlinite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_storm39b10_use",  label:"Nexus Storm 39B10",        desc:"Activate NEXUS_STORM39B10",             icon:"\U000026a1", xp:44 },'
  '\n  { id:"nexus_storm39b10_max",  label:"Nexus Storm Max 39B10",    desc:"Score 1896 pts in NEXUS_STORM39B10",    icon:"\U000026a1", xp:88 },'
  '\n  { id:"solar_wave39b10_use",   label:"Solar Wave 39B10",          desc:"Activate SOLAR_WAVE39B10",              icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_wave39b10_max",   label:"Solar Wave Max 39B10",      desc:"Score 1898 pts in SOLAR_WAVE39B10",     icon:"\U00002600️", xp:88 },'
  '\n  { id:"brucite_fox9e_tap",     label:"Brucite Fox",               desc:"Tap brucite_fox9e",                     icon:"\U0001f98a", xp:44 },'
  '\n  { id:"brucite_fox9e_peak",    label:"Brucite Fox Peak",          desc:"Tap brucite_fox9e at >85% charge",      icon:"\U0001f98a", xp:88 },'
  '\n  { id:"bustamite_orb9e_tap",   label:"Bustamite Orb",             desc:"Tap bustamite_orb9e",                   icon:"\U0001f52e", xp:44 },'
  '\n  { id:"bustamite_orb9e_peak",  label:"Bustamite Orb Peak",        desc:"Tap bustamite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_CREST39B10","THUNDER_FLARE39B10",'
A2_NEW = '"NEXUS_STORM39B10","SOLAR_WAVE39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_CREST39B10"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_STORM39B10"){\n'
  '    activePwrRef.current.push({type:"NEXUS_STORM39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1559);\n'
  '    showNotif("\U000026a1\U0001f300 NEXUS STORM 39B10!");unlock("nexus_storm39b10_use");\n'
  '  } else if(ptype==="SOLAR_WAVE39B10"){\n'
  '    activePwrRef.current.push({type:"SOLAR_WAVE39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1561);\n'
  '    showNotif("\U00002600️\U0001f30a SOLAR WAVE 39B10!");unlock("solar_wave39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_CREST39B10 — +1892 aurora bonus'
A4_NEW = (
  '// NEXUS_STORM39B10 — +1896 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_STORM39B10")){\n'
  '    const bonusTotal=Math.round(89.8*1000);\n'
  '    gs.score+=1896;showPopup(cx,cy-1606,"+1896 \U000026a1\U0001f300",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0368",1768);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_storm39b10_max");\n'
  '  }\n'
  '  // SOLAR_WAVE39B10 — +1898 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_WAVE39B10")){\n'
  '    const bonusTotal=Math.round(89.9*1000);\n'
  '    gs.score+=1898;showPopup(cx,cy-1608,"+1898 \U00002600️\U0001f30a",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a083c",1770);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_wave39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBoraxFox9e('
FOX_FN = (
  'function drawBruciteFox9e(ctx,r,ts,bruPct){\n'
  '  const bob=Math.sin(ts*0.3202)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.45+bruPct*0.35,"#bae6fd");g.addColorStop(1,"#0369a1");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(bruPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(186,230,253,"+(bruPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=bruPct>0.88?"#7dd3fc":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(bruPct>0.88?"\U0001faa7":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawBustamiteOrb9e(ctx,r,ts,busPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3206);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+busPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fff1f2");g.addColorStop(0.35+busPct*0.35,"#fecaca");g.addColorStop(1,"#b91c1c");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+busPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(254,202,202,"+(0.45+busPct*0.55)+")";ctx.lineWidth=3.5+busPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(busPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(252,165,165,"+(busPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=busPct>0.88?"#fca5a5":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(busPct>0.88?"\U0001f338":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="borax_fox9e"){'
A6_NEW = (
  '  else if(t.type==="brucite_fox9e"){\n'
  '    const bf9eBru608=(Math.sin((Date.now()-t.spawnedAt)*0.3202)+1)/2;\n'
  '    t._bf9eBru608=bf9eBru608;\n'
  '    drawBruciteFox9e(ctx,t.radius,ts,bf9eBru608);\n'
  '  }\n'
  '  else if(t.type==="bustamite_orb9e"){\n'
  '    const ao9eBus608=(Math.sin((Date.now()-t.spawnedAt)*0.3206)+1)/2;\n'
  '    t._ao9eBus608=ao9eBus608;\n'
  '    drawBustamiteOrb9e(ctx,t.radius,ts,ao9eBus608);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="borax_fox9e"){'
A7_NEW = (
  'if(hit.type==="brucite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo608bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult608bf=gs.feverActive?2:1;\n'
  '      const isPeak608bf=((hit._bf9eBru608||0)>0.85);\n'
  '      const pts608bf=Math.round((isPeak608bf?502:312)*combo608bf*feverMult608bf);\n'
  '      gs.score+=pts608bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1742,"#bae6fd");\n'
  '      if(isPeak608bf){spawnPopup(hit.x,hit.y-28,"\U0001faa7 +"+pts608bf,theme.accent);unlock("brucite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts608bf,theme.accent);}\n'
  '      unlock("brucite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="bustamite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo608ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult608ao=gs.feverActive?2:1;\n'
  '      const isPeak608ao=((hit._ao9eBus608||0)>0.85);\n'
  '      const pts608ao=Math.round((isPeak608ao?504:314)*combo608ao*feverMult608ao);\n'
  '      gs.score+=pts608ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1744,"#fecaca");\n'
  '      if(isPeak608ao){spawnPopup(hit.x,hit.y-28,"\U0001f338 +"+pts608ao,theme.accent);unlock("bustamite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts608ao,theme.accent);}\n'
  '      unlock("bustamite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="borax_fox9e";color="#fef08a";glow="#fefce8";'
A8_NEW = (
  'type="brucite_fox9e";color="#bae6fd";glow="#f0f9ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="bustamite_orb9e";color="#fecaca";glow="#fff1f2";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="borax_fox9e"?BASE_R*1.06:type==="berlinite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="brucite_fox9e"?BASE_R*1.06:type==="bustamite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_CREST39B10:"\U0001f30c\U0001f451",THUNDER_FLARE39B10:"⚡\U0001f525",'
A10_NEW = 'NEXUS_STORM39B10:"\U000026a1\U0001f300",SOLAR_WAVE39B10:"\U00002600️\U0001f30a",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 608 done! +{delta} bytes")
