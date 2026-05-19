#!/usr/bin/env python3
# Batch 621: AURORA_GLOW40 + THUNDER_GLOW40 + NephriteFox9e + NontroniteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"marcasite_orb9e_peak",  label:"Marcasite Orb Peak",          desc:"Tap marcasite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_glow40_use",     label:"Aurora Glow 40",             desc:"Activate AURORA_GLOW40",                icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_glow40_max",     label:"Aurora Glow Max 40",         desc:"Score 1948 pts in AURORA_GLOW40",       icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_glow40_use",    label:"Thunder Glow 40",             desc:"Activate THUNDER_GLOW40",               icon:"⚡", xp:44 },'
  '\n  { id:"thunder_glow40_max",    label:"Thunder Glow Max 40",         desc:"Score 1950 pts in THUNDER_GLOW40",      icon:"⚡", xp:88 },'
  '\n  { id:"nephrite_fox9e_tap",    label:"Nephrite Fox",                desc:"Tap nephrite_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"nephrite_fox9e_peak",   label:"Nephrite Fox Peak",           desc:"Tap nephrite_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"nontronite_orb9e_tap",  label:"Nontronite Orb",              desc:"Tap nontronite_orb9e",                  icon:"\U0001f52e", xp:44 },'
  '\n  { id:"nontronite_orb9e_peak", label:"Nontronite Orb Peak",         desc:"Tap nontronite_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_GLOW40","SOLAR_GLOW40",'
A2_NEW = '"AURORA_GLOW40","THUNDER_GLOW40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_GLOW40"){'
A3_NEW = (
  '} else if(ptype==="AURORA_GLOW40"){\n'
  '    activePwrRef.current.push({type:"AURORA_GLOW40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1611);\n'
  '    showNotif("\U0001f30c\U0001f31f AURORA GLOW 40!");unlock("aurora_glow40_use");\n'
  '  } else if(ptype==="THUNDER_GLOW40"){\n'
  '    activePwrRef.current.push({type:"THUNDER_GLOW40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1613);\n'
  '    showNotif("⚡\U0001f31f THUNDER GLOW 40!");unlock("thunder_glow40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_GLOW40 — +1944 nexus bonus'
A4_NEW = (
  '// AURORA_GLOW40 — +1948 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_GLOW40")){\n'
  '    const bonusTotal=Math.round(92.4*1000);\n'
  '    gs.score+=1948;showPopup(cx,cy-1658,"+1948 \U0001f30c\U0001f31f",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0382",1820);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_glow40_max");\n'
  '  }\n'
  '  // THUNDER_GLOW40 — +1950 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_GLOW40")){\n'
  '    const bonusTotal=Math.round(92.5*1000);\n'
  '    gs.score+=1950;showPopup(cx,cy-1660,"+1950 ⚡\U0001f31f",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0856",1822);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_glow40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawMagnesiteFox9e('
FOX_FN = (
  'function drawNephriteFox9e(ctx,r,ts,nepPct){\n'
  '  const bob=Math.sin(ts*0.3306)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+nepPct*0.35,"#064e3b");g.addColorStop(1,"#022c22");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(nepPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(6,78,59,"+(nepPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=nepPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(nepPct>0.88?"\U0001f340":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawNontroniteOrb9e(ctx,r,ts,nonPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3310);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+nonPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+nonPct*0.35,"#b45309");g.addColorStop(1,"#7c2d12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+nonPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(180,83,9,"+(0.45+nonPct*0.55)+")";ctx.lineWidth=3.5+nonPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(nonPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(217,119,6,"+(nonPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=nonPct>0.88?"#fdba74":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(nonPct>0.88?"\U0001f7e4":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="magnesite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="nephrite_fox9e"){\n'
  '    const bf9eNep621=(Math.sin((Date.now()-t.spawnedAt)*0.3306)+1)/2;\n'
  '    t._bf9eNep621=bf9eNep621;\n'
  '    drawNephriteFox9e(ctx,t.radius,ts,bf9eNep621);\n'
  '  }\n'
  '  else if(t.type==="nontronite_orb9e"){\n'
  '    const ao9eNon621=(Math.sin((Date.now()-t.spawnedAt)*0.3310)+1)/2;\n'
  '    t._ao9eNon621=ao9eNon621;\n'
  '    drawNontroniteOrb9e(ctx,t.radius,ts,ao9eNon621);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="magnesite_fox9e"){'
A7_NEW = (
  'if(hit.type==="nephrite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo621bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult621bf=gs.feverActive?2:1;\n'
  '      const isPeak621bf=((hit._bf9eNep621||0)>0.85);\n'
  '      const pts621bf=Math.round((isPeak621bf?554:364)*combo621bf*feverMult621bf);\n'
  '      gs.score+=pts621bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1794,"#064e3b");\n'
  '      if(isPeak621bf){spawnPopup(hit.x,hit.y-28,"\U0001f340 +"+pts621bf,theme.accent);unlock("nephrite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts621bf,theme.accent);}\n'
  '      unlock("nephrite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="nontronite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo621ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult621ao=gs.feverActive?2:1;\n'
  '      const isPeak621ao=((hit._ao9eNon621||0)>0.85);\n'
  '      const pts621ao=Math.round((isPeak621ao?556:366)*combo621ao*feverMult621ao);\n'
  '      gs.score+=pts621ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1796,"#b45309");\n'
  '      if(isPeak621ao){spawnPopup(hit.x,hit.y-28,"\U0001f7e4 +"+pts621ao,theme.accent);unlock("nontronite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts621ao,theme.accent);}\n'
  '      unlock("nontronite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="magnesite_fox9e";color="#fde68a";glow="#fefce8";'
A8_NEW = (
  'type="nephrite_fox9e";color="#064e3b";glow="#ecfdf5";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="nontronite_orb9e";color="#b45309";glow="#fff7ed";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="magnesite_fox9e"?BASE_R*1.06:type==="marcasite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="nephrite_fox9e"?BASE_R*1.06:type==="nontronite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_GLOW40:"\U0001f4ab\U0001f31f",SOLAR_GLOW40:"\U00002600️\U0001f31f",'
A10_NEW = 'AURORA_GLOW40:"\U0001f30c\U0001f31f",THUNDER_GLOW40:"⚡\U0001f31f",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 621 done! +{delta} bytes")
