#!/usr/bin/env python3
# Batch 616: NEXUS_BEAM40 + SOLAR_BEAM40 + IlmeniteFox9e + IlvaiteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"hornblende_orb9e_peak", label:"Hornblende Orb Peak",         desc:"Tap hornblende_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_beam40_use",      label:"Nexus Beam 40",              desc:"Activate NEXUS_BEAM40",                 icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_beam40_max",      label:"Nexus Beam Max 40",          desc:"Score 1928 pts in NEXUS_BEAM40",        icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_beam40_use",      label:"Solar Beam 40",               desc:"Activate SOLAR_BEAM40",                 icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_beam40_max",      label:"Solar Beam Max 40",           desc:"Score 1930 pts in SOLAR_BEAM40",        icon:"\U00002600️", xp:88 },'
  '\n  { id:"ilmenite_fox9e_tap",    label:"Ilmenite Fox",                desc:"Tap ilmenite_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"ilmenite_fox9e_peak",   label:"Ilmenite Fox Peak",           desc:"Tap ilmenite_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"ilvaite_orb9e_tap",     label:"Ilvaite Orb",                 desc:"Tap ilvaite_orb9e",                     icon:"\U0001f52e", xp:44 },'
  '\n  { id:"ilvaite_orb9e_peak",    label:"Ilvaite Orb Peak",            desc:"Tap ilvaite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_PULSE40","THUNDER_PULSE40",'
A2_NEW = '"NEXUS_BEAM40","SOLAR_BEAM40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_PULSE40"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_BEAM40"){\n'
  '    activePwrRef.current.push({type:"NEXUS_BEAM40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1591);\n'
  '    showNotif("\U0001f4ab\U0001f4a1 NEXUS BEAM 40!");unlock("nexus_beam40_use");\n'
  '  } else if(ptype==="SOLAR_BEAM40"){\n'
  '    activePwrRef.current.push({type:"SOLAR_BEAM40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1593);\n'
  '    showNotif("\U00002600️\U0001f4a1 SOLAR BEAM 40!");unlock("solar_beam40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_PULSE40 — +1924 aurora bonus'
A4_NEW = (
  '// NEXUS_BEAM40 — +1928 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_BEAM40")){\n'
  '    const bonusTotal=Math.round(91.4*1000);\n'
  '    gs.score+=1928;showPopup(cx,cy-1638,"+1928 \U0001f4ab\U0001f4a1",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0378",1800);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_beam40_max");\n'
  '  }\n'
  '  // SOLAR_BEAM40 — +1930 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_BEAM40")){\n'
  '    const bonusTotal=Math.round(91.5*1000);\n'
  '    gs.score+=1930;showPopup(cx,cy-1640,"+1930 \U00002600️\U0001f4a1",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a084c",1802);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_beam40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawHaliteFox9e('
FOX_FN = (
  'function drawIlmeniteFox9e(ctx,r,ts,ilmPct){\n'
  '  const bob=Math.sin(ts*0.3266)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#eef2ff");g.addColorStop(0.45+ilmPct*0.35,"#1e1b4b");g.addColorStop(1,"#0f0a24");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(ilmPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(30,27,75,"+(ilmPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=ilmPct>0.88?"#818cf8":"#eef2ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ilmPct>0.88?"\U0001f30c":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawIlvaiteOrb9e(ctx,r,ts,ilvPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3270);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ilvPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.35+ilvPct*0.35,"#831843");g.addColorStop(1,"#4c0519");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+ilvPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(131,24,67,"+(0.45+ilvPct*0.55)+")";ctx.lineWidth=3.5+ilvPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(ilvPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(190,24,93,"+(ilvPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=ilvPct>0.88?"#f9a8d4":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ilvPct>0.88?"\U0001f338":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="halite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="ilmenite_fox9e"){\n'
  '    const bf9eIlm616=(Math.sin((Date.now()-t.spawnedAt)*0.3266)+1)/2;\n'
  '    t._bf9eIlm616=bf9eIlm616;\n'
  '    drawIlmeniteFox9e(ctx,t.radius,ts,bf9eIlm616);\n'
  '  }\n'
  '  else if(t.type==="ilvaite_orb9e"){\n'
  '    const ao9eIlv616=(Math.sin((Date.now()-t.spawnedAt)*0.3270)+1)/2;\n'
  '    t._ao9eIlv616=ao9eIlv616;\n'
  '    drawIlvaiteOrb9e(ctx,t.radius,ts,ao9eIlv616);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="halite_fox9e"){'
A7_NEW = (
  'if(hit.type==="ilmenite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo616bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult616bf=gs.feverActive?2:1;\n'
  '      const isPeak616bf=((hit._bf9eIlm616||0)>0.85);\n'
  '      const pts616bf=Math.round((isPeak616bf?534:344)*combo616bf*feverMult616bf);\n'
  '      gs.score+=pts616bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1774,"#1e1b4b");\n'
  '      if(isPeak616bf){spawnPopup(hit.x,hit.y-28,"\U0001f30c +"+pts616bf,theme.accent);unlock("ilmenite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts616bf,theme.accent);}\n'
  '      unlock("ilmenite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="ilvaite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo616ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult616ao=gs.feverActive?2:1;\n'
  '      const isPeak616ao=((hit._ao9eIlv616||0)>0.85);\n'
  '      const pts616ao=Math.round((isPeak616ao?536:346)*combo616ao*feverMult616ao);\n'
  '      gs.score+=pts616ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1776,"#831843");\n'
  '      if(isPeak616ao){spawnPopup(hit.x,hit.y-28,"\U0001f338 +"+pts616ao,theme.accent);unlock("ilvaite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts616ao,theme.accent);}\n'
  '      unlock("ilvaite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="halite_fox9e";color="#94a3b8";glow="#f8fafc";'
A8_NEW = (
  'type="ilmenite_fox9e";color="#1e1b4b";glow="#eef2ff";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="ilvaite_orb9e";color="#831843";glow="#fdf2f8";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="halite_fox9e"?BASE_R*1.06:type==="hornblende_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="ilmenite_fox9e"?BASE_R*1.06:type==="ilvaite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_PULSE40:"\U0001f30c\U0001f49a",THUNDER_PULSE40:"⚡\U0001f49b",'
A10_NEW = 'NEXUS_BEAM40:"\U0001f4ab\U0001f4a1",SOLAR_BEAM40:"\U00002600️\U0001f4a1",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 616 done! +{delta} bytes")
