#!/usr/bin/env python3
# Batch 618: NEXUS_RING40 + SOLAR_RING40 + KyaniteFox9e + KaoliniteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"jadeite_orb9e_peak",    label:"Jadeite Orb Peak",            desc:"Tap jadeite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_ring40_use",      label:"Nexus Ring 40",              desc:"Activate NEXUS_RING40",                 icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_ring40_max",      label:"Nexus Ring Max 40",          desc:"Score 1936 pts in NEXUS_RING40",        icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_ring40_use",      label:"Solar Ring 40",               desc:"Activate SOLAR_RING40",                 icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_ring40_max",      label:"Solar Ring Max 40",           desc:"Score 1938 pts in SOLAR_RING40",        icon:"\U00002600️", xp:88 },'
  '\n  { id:"kyanite_fox9e_tap",     label:"Kyanite Fox",                 desc:"Tap kyanite_fox9e",                     icon:"\U0001f98a", xp:44 },'
  '\n  { id:"kyanite_fox9e_peak",    label:"Kyanite Fox Peak",            desc:"Tap kyanite_fox9e at >85% charge",      icon:"\U0001f98a", xp:88 },'
  '\n  { id:"kaolinite_orb9e_tap",   label:"Kaolinite Orb",               desc:"Tap kaolinite_orb9e",                   icon:"\U0001f52e", xp:44 },'
  '\n  { id:"kaolinite_orb9e_peak",  label:"Kaolinite Orb Peak",          desc:"Tap kaolinite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_BEAM40","THUNDER_BEAM40",'
A2_NEW = '"NEXUS_RING40","SOLAR_RING40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_BEAM40"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_RING40"){\n'
  '    activePwrRef.current.push({type:"NEXUS_RING40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1599);\n'
  '    showNotif("\U0001f4ab\U0001f48d NEXUS RING 40!");unlock("nexus_ring40_use");\n'
  '  } else if(ptype==="SOLAR_RING40"){\n'
  '    activePwrRef.current.push({type:"SOLAR_RING40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1601);\n'
  '    showNotif("\U00002600️\U0001f48d SOLAR RING 40!");unlock("solar_ring40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_BEAM40 — +1932 aurora bonus'
A4_NEW = (
  '// NEXUS_RING40 — +1936 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_RING40")){\n'
  '    const bonusTotal=Math.round(91.8*1000);\n'
  '    gs.score+=1936;showPopup(cx,cy-1646,"+1936 \U0001f4ab\U0001f48d",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a037c",1808);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_ring40_max");\n'
  '  }\n'
  '  // SOLAR_RING40 — +1938 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_RING40")){\n'
  '    const bonusTotal=Math.round(91.9*1000);\n'
  '    gs.score+=1938;showPopup(cx,cy-1648,"+1938 \U00002600️\U0001f48d",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0850",1810);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_ring40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawJarositeFox9e('
FOX_FN = (
  'function drawKyaniteFox9e(ctx,r,ts,kyaPct){\n'
  '  const bob=Math.sin(ts*0.3282)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+kyaPct*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(kyaPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(37,99,235,"+(kyaPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=kyaPct>0.88?"#60a5fa":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(kyaPct>0.88?"\U0001f48e":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawKaoliniteOrb9e(ctx,r,ts,kaoPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3286);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+kaoPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+kaoPct*0.35,"#e2e8f0");g.addColorStop(1,"#475569");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+kaoPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(226,232,240,"+(0.45+kaoPct*0.55)+")";ctx.lineWidth=3.5+kaoPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(kaoPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(203,213,225,"+(kaoPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=kaoPct>0.88?"#cbd5e1":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(kaoPct>0.88?"\U0001f90d":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="jarosite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="kyanite_fox9e"){\n'
  '    const bf9eKya618=(Math.sin((Date.now()-t.spawnedAt)*0.3282)+1)/2;\n'
  '    t._bf9eKya618=bf9eKya618;\n'
  '    drawKyaniteFox9e(ctx,t.radius,ts,bf9eKya618);\n'
  '  }\n'
  '  else if(t.type==="kaolinite_orb9e"){\n'
  '    const ao9eKao618=(Math.sin((Date.now()-t.spawnedAt)*0.3286)+1)/2;\n'
  '    t._ao9eKao618=ao9eKao618;\n'
  '    drawKaoliniteOrb9e(ctx,t.radius,ts,ao9eKao618);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="jarosite_fox9e"){'
A7_NEW = (
  'if(hit.type==="kyanite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo618bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult618bf=gs.feverActive?2:1;\n'
  '      const isPeak618bf=((hit._bf9eKya618||0)>0.85);\n'
  '      const pts618bf=Math.round((isPeak618bf?542:352)*combo618bf*feverMult618bf);\n'
  '      gs.score+=pts618bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1782,"#2563eb");\n'
  '      if(isPeak618bf){spawnPopup(hit.x,hit.y-28,"\U0001f48e +"+pts618bf,theme.accent);unlock("kyanite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts618bf,theme.accent);}\n'
  '      unlock("kyanite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="kaolinite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo618ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult618ao=gs.feverActive?2:1;\n'
  '      const isPeak618ao=((hit._ao9eKao618||0)>0.85);\n'
  '      const pts618ao=Math.round((isPeak618ao?544:354)*combo618ao*feverMult618ao);\n'
  '      gs.score+=pts618ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1784,"#e2e8f0");\n'
  '      if(isPeak618ao){spawnPopup(hit.x,hit.y-28,"\U0001f90d +"+pts618ao,theme.accent);unlock("kaolinite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts618ao,theme.accent);}\n'
  '      unlock("kaolinite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="jarosite_fox9e";color="#d97706";glow="#fffbeb";'
A8_NEW = (
  'type="kyanite_fox9e";color="#2563eb";glow="#eff6ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="kaolinite_orb9e";color="#e2e8f0";glow="#f8fafc";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="jarosite_fox9e"?BASE_R*1.06:type==="jadeite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="kyanite_fox9e"?BASE_R*1.06:type==="kaolinite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_BEAM40:"\U0001f30c\U0001f4a1",THUNDER_BEAM40:"⚡\U0001f4a1",'
A10_NEW = 'NEXUS_RING40:"\U0001f4ab\U0001f48d",SOLAR_RING40:"\U00002600️\U0001f48d",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 618 done! +{delta} bytes")
