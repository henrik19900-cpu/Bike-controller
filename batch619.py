#!/usr/bin/env python3
# Batch 619: AURORA_RING40 + THUNDER_RING40 + LepidoliteFox9e + LeuciteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"kaolinite_orb9e_peak",  label:"Kaolinite Orb Peak",          desc:"Tap kaolinite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_ring40_use",     label:"Aurora Ring 40",             desc:"Activate AURORA_RING40",                icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_ring40_max",     label:"Aurora Ring Max 40",         desc:"Score 1940 pts in AURORA_RING40",       icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_ring40_use",    label:"Thunder Ring 40",             desc:"Activate THUNDER_RING40",               icon:"⚡", xp:44 },'
  '\n  { id:"thunder_ring40_max",    label:"Thunder Ring Max 40",         desc:"Score 1942 pts in THUNDER_RING40",      icon:"⚡", xp:88 },'
  '\n  { id:"lepidolite_fox9e_tap",  label:"Lepidolite Fox",              desc:"Tap lepidolite_fox9e",                  icon:"\U0001f98a", xp:44 },'
  '\n  { id:"lepidolite_fox9e_peak", label:"Lepidolite Fox Peak",         desc:"Tap lepidolite_fox9e at >85% charge",   icon:"\U0001f98a", xp:88 },'
  '\n  { id:"leucite_orb9e_tap",     label:"Leucite Orb",                 desc:"Tap leucite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"leucite_orb9e_peak",    label:"Leucite Orb Peak",            desc:"Tap leucite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_RING40","SOLAR_RING40",'
A2_NEW = '"AURORA_RING40","THUNDER_RING40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_RING40"){'
A3_NEW = (
  '} else if(ptype==="AURORA_RING40"){\n'
  '    activePwrRef.current.push({type:"AURORA_RING40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1603);\n'
  '    showNotif("\U0001f30c\U0001f48d AURORA RING 40!");unlock("aurora_ring40_use");\n'
  '  } else if(ptype==="THUNDER_RING40"){\n'
  '    activePwrRef.current.push({type:"THUNDER_RING40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1605);\n'
  '    showNotif("⚡\U0001f48d THUNDER RING 40!");unlock("thunder_ring40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_RING40 — +1936 nexus bonus'
A4_NEW = (
  '// AURORA_RING40 — +1940 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_RING40")){\n'
  '    const bonusTotal=Math.round(92.0*1000);\n'
  '    gs.score+=1940;showPopup(cx,cy-1650,"+1940 \U0001f30c\U0001f48d",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a037e",1812);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_ring40_max");\n'
  '  }\n'
  '  // THUNDER_RING40 — +1942 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_RING40")){\n'
  '    const bonusTotal=Math.round(92.1*1000);\n'
  '    gs.score+=1942;showPopup(cx,cy-1652,"+1942 ⚡\U0001f48d",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0852",1814);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_ring40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawKyaniteFox9e('
FOX_FN = (
  'function drawLepidoliteFox9e(ctx,r,ts,lepPct){\n'
  '  const bob=Math.sin(ts*0.3290)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#faf5ff");g.addColorStop(0.45+lepPct*0.35,"#a855f7");g.addColorStop(1,"#6b21a8");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(lepPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(168,85,247,"+(lepPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=lepPct>0.88?"#d8b4fe":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lepPct>0.88?"\U0001f49c":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawLeuciteOrb9e(ctx,r,ts,leuPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3294);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+leuPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.35+leuPct*0.35,"#7dd3fc");g.addColorStop(1,"#0369a1");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+leuPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(125,211,252,"+(0.45+leuPct*0.55)+")";ctx.lineWidth=3.5+leuPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(leuPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(186,230,253,"+(leuPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=leuPct>0.88?"#bae6fd":"#e0f2fe";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(leuPct>0.88?"\U0001f319":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="kyanite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="lepidolite_fox9e"){\n'
  '    const bf9eLep619=(Math.sin((Date.now()-t.spawnedAt)*0.3290)+1)/2;\n'
  '    t._bf9eLep619=bf9eLep619;\n'
  '    drawLepidoliteFox9e(ctx,t.radius,ts,bf9eLep619);\n'
  '  }\n'
  '  else if(t.type==="leucite_orb9e"){\n'
  '    const ao9eLeu619=(Math.sin((Date.now()-t.spawnedAt)*0.3294)+1)/2;\n'
  '    t._ao9eLeu619=ao9eLeu619;\n'
  '    drawLeuciteOrb9e(ctx,t.radius,ts,ao9eLeu619);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="kyanite_fox9e"){'
A7_NEW = (
  'if(hit.type==="lepidolite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo619bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult619bf=gs.feverActive?2:1;\n'
  '      const isPeak619bf=((hit._bf9eLep619||0)>0.85);\n'
  '      const pts619bf=Math.round((isPeak619bf?546:356)*combo619bf*feverMult619bf);\n'
  '      gs.score+=pts619bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1786,"#a855f7");\n'
  '      if(isPeak619bf){spawnPopup(hit.x,hit.y-28,"\U0001f49c +"+pts619bf,theme.accent);unlock("lepidolite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts619bf,theme.accent);}\n'
  '      unlock("lepidolite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="leucite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo619ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult619ao=gs.feverActive?2:1;\n'
  '      const isPeak619ao=((hit._ao9eLeu619||0)>0.85);\n'
  '      const pts619ao=Math.round((isPeak619ao?548:358)*combo619ao*feverMult619ao);\n'
  '      gs.score+=pts619ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1788,"#7dd3fc");\n'
  '      if(isPeak619ao){spawnPopup(hit.x,hit.y-28,"\U0001f319 +"+pts619ao,theme.accent);unlock("leucite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts619ao,theme.accent);}\n'
  '      unlock("leucite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="kyanite_fox9e";color="#2563eb";glow="#eff6ff";'
A8_NEW = (
  'type="lepidolite_fox9e";color="#a855f7";glow="#faf5ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="leucite_orb9e";color="#7dd3fc";glow="#e0f2fe";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="kyanite_fox9e"?BASE_R*1.06:type==="kaolinite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="lepidolite_fox9e"?BASE_R*1.06:type==="leucite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_RING40:"\U0001f4ab\U0001f48d",SOLAR_RING40:"\U00002600️\U0001f48d",'
A10_NEW = 'AURORA_RING40:"\U0001f30c\U0001f48d",THUNDER_RING40:"⚡\U0001f48d",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 619 done! +{delta} bytes")
