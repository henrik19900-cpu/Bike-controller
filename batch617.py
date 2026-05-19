#!/usr/bin/env python3
# Batch 617: AURORA_BEAM40 + THUNDER_BEAM40 + JarositeFox9e + JadeiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"ilvaite_orb9e_peak",    label:"Ilvaite Orb Peak",            desc:"Tap ilvaite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_beam40_use",     label:"Aurora Beam 40",             desc:"Activate AURORA_BEAM40",                icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_beam40_max",     label:"Aurora Beam Max 40",         desc:"Score 1932 pts in AURORA_BEAM40",       icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_beam40_use",    label:"Thunder Beam 40",             desc:"Activate THUNDER_BEAM40",               icon:"⚡", xp:44 },'
  '\n  { id:"thunder_beam40_max",    label:"Thunder Beam Max 40",         desc:"Score 1934 pts in THUNDER_BEAM40",      icon:"⚡", xp:88 },'
  '\n  { id:"jarosite_fox9e_tap",    label:"Jarosite Fox",                desc:"Tap jarosite_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"jarosite_fox9e_peak",   label:"Jarosite Fox Peak",           desc:"Tap jarosite_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"jadeite_orb9e_tap",     label:"Jadeite Orb",                 desc:"Tap jadeite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"jadeite_orb9e_peak",    label:"Jadeite Orb Peak",            desc:"Tap jadeite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_BEAM40","SOLAR_BEAM40",'
A2_NEW = '"AURORA_BEAM40","THUNDER_BEAM40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_BEAM40"){'
A3_NEW = (
  '} else if(ptype==="AURORA_BEAM40"){\n'
  '    activePwrRef.current.push({type:"AURORA_BEAM40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1595);\n'
  '    showNotif("\U0001f30c\U0001f4a1 AURORA BEAM 40!");unlock("aurora_beam40_use");\n'
  '  } else if(ptype==="THUNDER_BEAM40"){\n'
  '    activePwrRef.current.push({type:"THUNDER_BEAM40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1597);\n'
  '    showNotif("⚡\U0001f4a1 THUNDER BEAM 40!");unlock("thunder_beam40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_BEAM40 — +1928 nexus bonus'
A4_NEW = (
  '// AURORA_BEAM40 — +1932 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_BEAM40")){\n'
  '    const bonusTotal=Math.round(91.6*1000);\n'
  '    gs.score+=1932;showPopup(cx,cy-1642,"+1932 \U0001f30c\U0001f4a1",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a037a",1804);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_beam40_max");\n'
  '  }\n'
  '  // THUNDER_BEAM40 — +1934 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_BEAM40")){\n'
  '    const bonusTotal=Math.round(91.7*1000);\n'
  '    gs.score+=1934;showPopup(cx,cy-1644,"+1934 ⚡\U0001f4a1",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a084e",1806);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_beam40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawIlmeniteFox9e('
FOX_FN = (
  'function drawJarositeFox9e(ctx,r,ts,jarPct){\n'
  '  const bob=Math.sin(ts*0.3274)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fffbeb");g.addColorStop(0.45+jarPct*0.35,"#d97706");g.addColorStop(1,"#92400e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(jarPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(217,119,6,"+(jarPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=jarPct>0.88?"#fbbf24":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(jarPct>0.88?"\U0001f31f":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawJadeiteOrb9e(ctx,r,ts,jadPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3278);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+jadPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+jadPct*0.35,"#15803d");g.addColorStop(1,"#052e16");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+jadPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(21,128,61,"+(0.45+jadPct*0.55)+")";ctx.lineWidth=3.5+jadPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(jadPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(74,222,128,"+(jadPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=jadPct>0.88?"#4ade80":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(jadPct>0.88?"\U0001f331":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="ilmenite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="jarosite_fox9e"){\n'
  '    const bf9eJar617=(Math.sin((Date.now()-t.spawnedAt)*0.3274)+1)/2;\n'
  '    t._bf9eJar617=bf9eJar617;\n'
  '    drawJarositeFox9e(ctx,t.radius,ts,bf9eJar617);\n'
  '  }\n'
  '  else if(t.type==="jadeite_orb9e"){\n'
  '    const ao9eJad617=(Math.sin((Date.now()-t.spawnedAt)*0.3278)+1)/2;\n'
  '    t._ao9eJad617=ao9eJad617;\n'
  '    drawJadeiteOrb9e(ctx,t.radius,ts,ao9eJad617);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="ilmenite_fox9e"){'
A7_NEW = (
  'if(hit.type==="jarosite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo617bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult617bf=gs.feverActive?2:1;\n'
  '      const isPeak617bf=((hit._bf9eJar617||0)>0.85);\n'
  '      const pts617bf=Math.round((isPeak617bf?538:348)*combo617bf*feverMult617bf);\n'
  '      gs.score+=pts617bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1778,"#d97706");\n'
  '      if(isPeak617bf){spawnPopup(hit.x,hit.y-28,"\U0001f31f +"+pts617bf,theme.accent);unlock("jarosite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts617bf,theme.accent);}\n'
  '      unlock("jarosite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="jadeite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo617ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult617ao=gs.feverActive?2:1;\n'
  '      const isPeak617ao=((hit._ao9eJad617||0)>0.85);\n'
  '      const pts617ao=Math.round((isPeak617ao?540:350)*combo617ao*feverMult617ao);\n'
  '      gs.score+=pts617ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1780,"#15803d");\n'
  '      if(isPeak617ao){spawnPopup(hit.x,hit.y-28,"\U0001f331 +"+pts617ao,theme.accent);unlock("jadeite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts617ao,theme.accent);}\n'
  '      unlock("jadeite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="ilmenite_fox9e";color="#1e1b4b";glow="#eef2ff";'
A8_NEW = (
  'type="jarosite_fox9e";color="#d97706";glow="#fffbeb";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="jadeite_orb9e";color="#15803d";glow="#f0fdf4";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="ilmenite_fox9e"?BASE_R*1.06:type==="ilvaite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="jarosite_fox9e"?BASE_R*1.06:type==="jadeite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_BEAM40:"\U0001f4ab\U0001f4a1",SOLAR_BEAM40:"\U00002600️\U0001f4a1",'
A10_NEW = 'AURORA_BEAM40:"\U0001f30c\U0001f4a1",THUNDER_BEAM40:"⚡\U0001f4a1",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 617 done! +{delta} bytes")
