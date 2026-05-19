#!/usr/bin/env python3
# Batch 607: AURORA_CREST39B10 + THUNDER_FLARE39B10 + BoraxFox9e + BerliniteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"apatite_orb9e_peak",    label:"Apatite Orb Peak",         desc:"Tap apatite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_crest39b10_use",  label:"Aurora Crest 39B10",      desc:"Activate AURORA_CREST39B10",            icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_crest39b10_max",  label:"Aurora Crest Max 39B10",   desc:"Score 1892 pts in AURORA_CREST39B10",   icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_flare39b10_use", label:"Thunder Flare 39B10",      desc:"Activate THUNDER_FLARE39B10",           icon:"⚡", xp:44 },'
  '\n  { id:"thunder_flare39b10_max", label:"Thunder Flare Max 39B10",  desc:"Score 1894 pts in THUNDER_FLARE39B10",  icon:"⚡", xp:88 },'
  '\n  { id:"borax_fox9e_tap",        label:"Borax Fox",                desc:"Tap borax_fox9e",                       icon:"\U0001f98a", xp:44 },'
  '\n  { id:"borax_fox9e_peak",       label:"Borax Fox Peak",           desc:"Tap borax_fox9e at >85% charge",        icon:"\U0001f98a", xp:88 },'
  '\n  { id:"berlinite_orb9e_tap",    label:"Berlinite Orb",            desc:"Tap berlinite_orb9e",                   icon:"\U0001f52e", xp:44 },'
  '\n  { id:"berlinite_orb9e_peak",   label:"Berlinite Orb Peak",       desc:"Tap berlinite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_TIDE39B10","SOLAR_CREST39B10",'
A2_NEW = '"AURORA_CREST39B10","THUNDER_FLARE39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_TIDE39B10"){'
A3_NEW = (
  '} else if(ptype==="AURORA_CREST39B10"){\n'
  '    activePwrRef.current.push({type:"AURORA_CREST39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1555);\n'
  '    showNotif("\U0001f30c\U0001f451 AURORA CREST 39B10!");unlock("aurora_crest39b10_use");\n'
  '  } else if(ptype==="THUNDER_FLARE39B10"){\n'
  '    activePwrRef.current.push({type:"THUNDER_FLARE39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1557);\n'
  '    showNotif("⚡\U0001f525 THUNDER FLARE 39B10!");unlock("thunder_flare39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_TIDE39B10 — +1888 nexus bonus'
A4_NEW = (
  '// AURORA_CREST39B10 — +1892 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_CREST39B10")){\n'
  '    const bonusTotal=Math.round(89.6*1000);\n'
  '    gs.score+=1892;showPopup(cx,cy-1602,"+1892 \U0001f30c\U0001f451",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0366",1764);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_crest39b10_max");\n'
  '  }\n'
  '  // THUNDER_FLARE39B10 — +1894 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_FLARE39B10")){\n'
  '    const bonusTotal=Math.round(89.7*1000);\n'
  '    gs.score+=1894;showPopup(cx,cy-1604,"+1894 ⚡\U0001f525",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a083a",1766);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_flare39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBiotiteFox9e('
FOX_FN = (
  'function drawBoraxFox9e(ctx,r,ts,brxPct){\n'
  '  const bob=Math.sin(ts*0.3194)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+brxPct*0.35,"#fef08a");g.addColorStop(1,"#ca8a04");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(brxPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(234,179,8,"+(brxPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=brxPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(brxPct>0.88?"\U0001f31f":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawBerliniteOrb9e(ctx,r,ts,berPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3198);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+berPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f5f3ff");g.addColorStop(0.35+berPct*0.35,"#e0e7ff");g.addColorStop(1,"#4338ca");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+berPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(224,231,255,"+(0.45+berPct*0.55)+")";ctx.lineWidth=3.5+berPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(berPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(199,210,254,"+(berPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=berPct>0.88?"#c7d2fe":"#f5f3ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(berPct>0.88?"\U0001f48e":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="biotite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="borax_fox9e"){\n'
  '    const bf9eBrx607=(Math.sin((Date.now()-t.spawnedAt)*0.3194)+1)/2;\n'
  '    t._bf9eBrx607=bf9eBrx607;\n'
  '    drawBoraxFox9e(ctx,t.radius,ts,bf9eBrx607);\n'
  '  }\n'
  '  else if(t.type==="berlinite_orb9e"){\n'
  '    const ao9eBer607=(Math.sin((Date.now()-t.spawnedAt)*0.3198)+1)/2;\n'
  '    t._ao9eBer607=ao9eBer607;\n'
  '    drawBerliniteOrb9e(ctx,t.radius,ts,ao9eBer607);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="biotite_fox9e"){'
A7_NEW = (
  'if(hit.type==="borax_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo607bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult607bf=gs.feverActive?2:1;\n'
  '      const isPeak607bf=((hit._bf9eBrx607||0)>0.85);\n'
  '      const pts607bf=Math.round((isPeak607bf?498:308)*combo607bf*feverMult607bf);\n'
  '      gs.score+=pts607bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1738,"#fef08a");\n'
  '      if(isPeak607bf){spawnPopup(hit.x,hit.y-28,"\U0001f31f +"+pts607bf,theme.accent);unlock("borax_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts607bf,theme.accent);}\n'
  '      unlock("borax_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="berlinite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo607ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult607ao=gs.feverActive?2:1;\n'
  '      const isPeak607ao=((hit._ao9eBer607||0)>0.85);\n'
  '      const pts607ao=Math.round((isPeak607ao?500:310)*combo607ao*feverMult607ao);\n'
  '      gs.score+=pts607ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1740,"#e0e7ff");\n'
  '      if(isPeak607ao){spawnPopup(hit.x,hit.y-28,"\U0001f48e +"+pts607ao,theme.accent);unlock("berlinite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts607ao,theme.accent);}\n'
  '      unlock("berlinite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="biotite_fox9e";color="#713f12";glow="#fef9c3";'
A8_NEW = (
  'type="borax_fox9e";color="#fef08a";glow="#fefce8";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="berlinite_orb9e";color="#e0e7ff";glow="#f5f3ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="biotite_fox9e"?BASE_R*1.06:type==="apatite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="borax_fox9e"?BASE_R*1.06:type==="berlinite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_TIDE39B10:"\U0001f30a\U0001f300",SOLAR_CREST39B10:"\U00002600️\U0001f451",'
A10_NEW = 'AURORA_CREST39B10:"\U0001f30c\U0001f451",THUNDER_FLARE39B10:"⚡\U0001f525",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 607 done! +{delta} bytes")
