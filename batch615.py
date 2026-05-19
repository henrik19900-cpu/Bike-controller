#!/usr/bin/env python3
# Batch 615: AURORA_PULSE40 + THUNDER_PULSE40 + HaliteFox9e + HornblendeOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"gedrite_orb9e_peak",    label:"Gedrite Orb Peak",            desc:"Tap gedrite_orb9e at >85%",            icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_pulse40_use",    label:"Aurora Pulse 40",            desc:"Activate AURORA_PULSE40",               icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_pulse40_max",    label:"Aurora Pulse Max 40",        desc:"Score 1924 pts in AURORA_PULSE40",      icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_pulse40_use",   label:"Thunder Pulse 40",            desc:"Activate THUNDER_PULSE40",              icon:"⚡", xp:44 },'
  '\n  { id:"thunder_pulse40_max",   label:"Thunder Pulse Max 40",        desc:"Score 1926 pts in THUNDER_PULSE40",     icon:"⚡", xp:88 },'
  '\n  { id:"halite_fox9e_tap",      label:"Halite Fox",                  desc:"Tap halite_fox9e",                      icon:"\U0001f98a", xp:44 },'
  '\n  { id:"halite_fox9e_peak",     label:"Halite Fox Peak",             desc:"Tap halite_fox9e at >85% charge",       icon:"\U0001f98a", xp:88 },'
  '\n  { id:"hornblende_orb9e_tap",  label:"Hornblende Orb",              desc:"Tap hornblende_orb9e",                  icon:"\U0001f52e", xp:44 },'
  '\n  { id:"hornblende_orb9e_peak", label:"Hornblende Orb Peak",         desc:"Tap hornblende_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_PULSE40","SOLAR_PULSE40",'
A2_NEW = '"AURORA_PULSE40","THUNDER_PULSE40",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_PULSE40"){'
A3_NEW = (
  '} else if(ptype==="AURORA_PULSE40"){\n'
  '    activePwrRef.current.push({type:"AURORA_PULSE40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1587);\n'
  '    showNotif("\U0001f30c\U0001f49a AURORA PULSE 40!");unlock("aurora_pulse40_use");\n'
  '  } else if(ptype==="THUNDER_PULSE40"){\n'
  '    activePwrRef.current.push({type:"THUNDER_PULSE40",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1589);\n'
  '    showNotif("⚡\U0001f49b THUNDER PULSE 40!");unlock("thunder_pulse40_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_PULSE40 — +1920 nexus bonus'
A4_NEW = (
  '// AURORA_PULSE40 — +1924 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_PULSE40")){\n'
  '    const bonusTotal=Math.round(91.2*1000);\n'
  '    gs.score+=1924;showPopup(cx,cy-1634,"+1924 \U0001f30c\U0001f49a",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0376",1796);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_pulse40_max");\n'
  '  }\n'
  '  // THUNDER_PULSE40 — +1926 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_PULSE40")){\n'
  '    const bonusTotal=Math.round(91.3*1000);\n'
  '    gs.score+=1926;showPopup(cx,cy-1636,"+1926 ⚡\U0001f49b",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a084a",1798);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_pulse40_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawGahniteFox9e('
FOX_FN = (
  'function drawHaliteFox9e(ctx,r,ts,halPct){\n'
  '  const bob=Math.sin(ts*0.3258)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+halPct*0.35,"#94a3b8");g.addColorStop(1,"#334155");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(halPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(148,163,184,"+(halPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=halPct>0.88?"#e2e8f0":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(halPct>0.88?"❄️":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawHornblendeOrb9e(ctx,r,ts,horPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3262);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+horPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f9fafb");g.addColorStop(0.35+horPct*0.35,"#1f2937");g.addColorStop(1,"#030712");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+horPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(31,41,55,"+(0.45+horPct*0.55)+")";ctx.lineWidth=3.5+horPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(horPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(75,85,99,"+(horPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=horPct>0.88?"#4b5563":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(horPct>0.88?"\U000026ab":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="gahnite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="halite_fox9e"){\n'
  '    const bf9eHal615=(Math.sin((Date.now()-t.spawnedAt)*0.3258)+1)/2;\n'
  '    t._bf9eHal615=bf9eHal615;\n'
  '    drawHaliteFox9e(ctx,t.radius,ts,bf9eHal615);\n'
  '  }\n'
  '  else if(t.type==="hornblende_orb9e"){\n'
  '    const ao9eHor615=(Math.sin((Date.now()-t.spawnedAt)*0.3262)+1)/2;\n'
  '    t._ao9eHor615=ao9eHor615;\n'
  '    drawHornblendeOrb9e(ctx,t.radius,ts,ao9eHor615);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="gahnite_fox9e"){'
A7_NEW = (
  'if(hit.type==="halite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo615bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult615bf=gs.feverActive?2:1;\n'
  '      const isPeak615bf=((hit._bf9eHal615||0)>0.85);\n'
  '      const pts615bf=Math.round((isPeak615bf?530:340)*combo615bf*feverMult615bf);\n'
  '      gs.score+=pts615bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1770,"#94a3b8");\n'
  '      if(isPeak615bf){spawnPopup(hit.x,hit.y-28,"❄️ +"+pts615bf,theme.accent);unlock("halite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts615bf,theme.accent);}\n'
  '      unlock("halite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="hornblende_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo615ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult615ao=gs.feverActive?2:1;\n'
  '      const isPeak615ao=((hit._ao9eHor615||0)>0.85);\n'
  '      const pts615ao=Math.round((isPeak615ao?532:342)*combo615ao*feverMult615ao);\n'
  '      gs.score+=pts615ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1772,"#1f2937");\n'
  '      if(isPeak615ao){spawnPopup(hit.x,hit.y-28,"\U000026ab +"+pts615ao,theme.accent);unlock("hornblende_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts615ao,theme.accent);}\n'
  '      unlock("hornblende_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="gahnite_fox9e";color="#1e3a5f";glow="#eff6ff";'
A8_NEW = (
  'type="halite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="hornblende_orb9e";color="#1f2937";glow="#f9fafb";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="gahnite_fox9e"?BASE_R*1.06:type==="gedrite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="halite_fox9e"?BASE_R*1.06:type==="hornblende_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_PULSE40:"\U0001f4ab\U0001f49a",SOLAR_PULSE40:"\U00002600️\U0001f49b",'
A10_NEW = 'AURORA_PULSE40:"\U0001f30c\U0001f49a",THUNDER_PULSE40:"⚡\U0001f49b",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 615 done! +{delta} bytes")
