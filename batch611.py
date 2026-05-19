#!/usr/bin/env python3
# Batch 611: AURORA_NOVA39B10 + THUNDER_WAVE39B10 + DiopsideFox9e + DolomiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"cristobalite_orb9e_peak", label:"Cristobalite Orb Peak",    desc:"Tap cristobalite_orb9e at >85%",       icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_nova39b10_use",   label:"Aurora Nova 39B10",         desc:"Activate AURORA_NOVA39B10",             icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_nova39b10_max",   label:"Aurora Nova Max 39B10",     desc:"Score 1908 pts in AURORA_NOVA39B10",    icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_wave39b10_use",  label:"Thunder Wave 39B10",         desc:"Activate THUNDER_WAVE39B10",            icon:"⚡", xp:44 },'
  '\n  { id:"thunder_wave39b10_max",  label:"Thunder Wave Max 39B10",     desc:"Score 1910 pts in THUNDER_WAVE39B10",   icon:"⚡", xp:88 },'
  '\n  { id:"diopside_fox9e_tap",     label:"Diopside Fox",               desc:"Tap diopside_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"diopside_fox9e_peak",    label:"Diopside Fox Peak",          desc:"Tap diopside_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"dolomite_orb9e_tap",     label:"Dolomite Orb",               desc:"Tap dolomite_orb9e",                    icon:"\U0001f52e", xp:44 },'
  '\n  { id:"dolomite_orb9e_peak",    label:"Dolomite Orb Peak",          desc:"Tap dolomite_orb9e at >85%",           icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_NOVA39B10","SOLAR_STORM39B10",'
A2_NEW = '"AURORA_NOVA39B10","THUNDER_WAVE39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_NOVA39B10"){'
A3_NEW = (
  '} else if(ptype==="AURORA_NOVA39B10"){\n'
  '    activePwrRef.current.push({type:"AURORA_NOVA39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1571);\n'
  '    showNotif("\U0001f30c\U0001f4ab AURORA NOVA 39B10!");unlock("aurora_nova39b10_use");\n'
  '  } else if(ptype==="THUNDER_WAVE39B10"){\n'
  '    activePwrRef.current.push({type:"THUNDER_WAVE39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1573);\n'
  '    showNotif("⚡〰️ THUNDER WAVE 39B10!");unlock("thunder_wave39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_NOVA39B10 — +1904 nexus bonus'
A4_NEW = (
  '// AURORA_NOVA39B10 — +1908 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_NOVA39B10")){\n'
  '    const bonusTotal=Math.round(90.4*1000);\n'
  '    gs.score+=1908;showPopup(cx,cy-1618,"+1908 \U0001f30c\U0001f4ab",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a036e",1780);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_nova39b10_max");\n'
  '  }\n'
  '  // THUNDER_WAVE39B10 — +1910 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_WAVE39B10")){\n'
  '    const bonusTotal=Math.round(90.5*1000);\n'
  '    gs.score+=1910;showPopup(cx,cy-1620,"+1910 ⚡〰️",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0842",1782);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_wave39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawCorundumFox9e('
FOX_FN = (
  'function drawDiopsideFox9e(ctx,r,ts,dioPct){\n'
  '  const bob=Math.sin(ts*0.3226)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+dioPct*0.35,"#059669");g.addColorStop(1,"#064e3b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(dioPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(5,150,105,"+(dioPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=dioPct>0.88?"#34d399":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(dioPct>0.88?"\U0001f331":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawDolomiteOrb9e(ctx,r,ts,dolPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3230);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+dolPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf6ec");g.addColorStop(0.35+dolPct*0.35,"#d6bcaa");g.addColorStop(1,"#78350f");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+dolPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(214,188,170,"+(0.45+dolPct*0.55)+")";ctx.lineWidth=3.5+dolPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(dolPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(196,166,145,"+(dolPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=dolPct>0.88?"#c4a67d":"#fdf6ec";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(dolPct>0.88?"\U0001f3d4️":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="corundum_fox9e"){'
A6_NEW = (
  '  else if(t.type==="diopside_fox9e"){\n'
  '    const bf9eDio611=(Math.sin((Date.now()-t.spawnedAt)*0.3226)+1)/2;\n'
  '    t._bf9eDio611=bf9eDio611;\n'
  '    drawDiopsideFox9e(ctx,t.radius,ts,bf9eDio611);\n'
  '  }\n'
  '  else if(t.type==="dolomite_orb9e"){\n'
  '    const ao9eDol611=(Math.sin((Date.now()-t.spawnedAt)*0.3230)+1)/2;\n'
  '    t._ao9eDol611=ao9eDol611;\n'
  '    drawDolomiteOrb9e(ctx,t.radius,ts,ao9eDol611);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="corundum_fox9e"){'
A7_NEW = (
  'if(hit.type==="diopside_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo611bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult611bf=gs.feverActive?2:1;\n'
  '      const isPeak611bf=((hit._bf9eDio611||0)>0.85);\n'
  '      const pts611bf=Math.round((isPeak611bf?514:324)*combo611bf*feverMult611bf);\n'
  '      gs.score+=pts611bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1754,"#059669");\n'
  '      if(isPeak611bf){spawnPopup(hit.x,hit.y-28,"\U0001f331 +"+pts611bf,theme.accent);unlock("diopside_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts611bf,theme.accent);}\n'
  '      unlock("diopside_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="dolomite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo611ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult611ao=gs.feverActive?2:1;\n'
  '      const isPeak611ao=((hit._ao9eDol611||0)>0.85);\n'
  '      const pts611ao=Math.round((isPeak611ao?516:326)*combo611ao*feverMult611ao);\n'
  '      gs.score+=pts611ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1756,"#d6bcaa");\n'
  '      if(isPeak611ao){spawnPopup(hit.x,hit.y-28,"\U0001f3d4️ +"+pts611ao,theme.accent);unlock("dolomite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts611ao,theme.accent);}\n'
  '      unlock("dolomite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="corundum_fox9e";color="#be185d";glow="#fdf2f8";'
A8_NEW = (
  'type="diopside_fox9e";color="#059669";glow="#ecfdf5";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="dolomite_orb9e";color="#d6bcaa";glow="#fdf6ec";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="corundum_fox9e"?BASE_R*1.06:type==="cristobalite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="diopside_fox9e"?BASE_R*1.06:type==="dolomite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_NOVA39B10:"\U0001f4ab\U0001f300",SOLAR_STORM39B10:"\U00002600️\U000026c8️",'
A10_NEW = 'AURORA_NOVA39B10:"\U0001f30c\U0001f4ab",THUNDER_WAVE39B10:"⚡〰️",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 611 done! +{delta} bytes")
