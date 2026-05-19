#!/usr/bin/env python3
# Batch 609: AURORA_STORM39B10 + THUNDER_CREST39B10 + ChloriteFox9e + ChalcociteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"bustamite_orb9e_peak",  label:"Bustamite Orb Peak",        desc:"Tap bustamite_orb9e at >85%",          icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"aurora_storm39b10_use",  label:"Aurora Storm 39B10",       desc:"Activate AURORA_STORM39B10",            icon:"\U0001f30c", xp:44 },'
  '\n  { id:"aurora_storm39b10_max",  label:"Aurora Storm Max 39B10",   desc:"Score 1900 pts in AURORA_STORM39B10",   icon:"\U0001f30c", xp:88 },'
  '\n  { id:"thunder_crest39b10_use", label:"Thunder Crest 39B10",      desc:"Activate THUNDER_CREST39B10",           icon:"⚡", xp:44 },'
  '\n  { id:"thunder_crest39b10_max", label:"Thunder Crest Max 39B10",  desc:"Score 1902 pts in THUNDER_CREST39B10",  icon:"⚡", xp:88 },'
  '\n  { id:"chlorite_fox9e_tap",     label:"Chlorite Fox",              desc:"Tap chlorite_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"chlorite_fox9e_peak",    label:"Chlorite Fox Peak",         desc:"Tap chlorite_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"chalcocite_orb9e_tap",   label:"Chalcocite Orb",            desc:"Tap chalcocite_orb9e",                  icon:"\U0001f52e", xp:44 },'
  '\n  { id:"chalcocite_orb9e_peak",  label:"Chalcocite Orb Peak",       desc:"Tap chalcocite_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"NEXUS_STORM39B10","SOLAR_WAVE39B10",'
A2_NEW = '"AURORA_STORM39B10","THUNDER_CREST39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_STORM39B10"){'
A3_NEW = (
  '} else if(ptype==="AURORA_STORM39B10"){\n'
  '    activePwrRef.current.push({type:"AURORA_STORM39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1563);\n'
  '    showNotif("\U0001f30c\U000026c8️ AURORA STORM 39B10!");unlock("aurora_storm39b10_use");\n'
  '  } else if(ptype==="THUNDER_CREST39B10"){\n'
  '    activePwrRef.current.push({type:"THUNDER_CREST39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1565);\n'
  '    showNotif("⚡\U0001f451 THUNDER CREST 39B10!");unlock("thunder_crest39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// NEXUS_STORM39B10 — +1896 nexus bonus'
A4_NEW = (
  '// AURORA_STORM39B10 — +1900 aurora bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="AURORA_STORM39B10")){\n'
  '    const bonusTotal=Math.round(90.0*1000);\n'
  '    gs.score+=1900;showPopup(cx,cy-1610,"+1900 \U0001f30c\U000026c8️",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a036a",1772);\n'
  '    if(gs.score>=bonusTotal)unlock("aurora_storm39b10_max");\n'
  '  }\n'
  '  // THUNDER_CREST39B10 — +1902 thunder bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="THUNDER_CREST39B10")){\n'
  '    const bonusTotal=Math.round(90.1*1000);\n'
  '    gs.score+=1902;showPopup(cx,cy-1612,"+1902 ⚡\U0001f451",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a083e",1774);\n'
  '    if(gs.score>=bonusTotal)unlock("thunder_crest39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBruciteFox9e('
FOX_FN = (
  'function drawChloriteFox9e(ctx,r,ts,chlPct){\n'
  '  const bob=Math.sin(ts*0.3210)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.45+chlPct*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(chlPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(22,101,52,"+(chlPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=chlPct>0.88?"#4ade80":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(chlPct>0.88?"\U0001f33f":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawChalcociteOrb9e(ctx,r,ts,chcPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3214);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+chcPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fafaf9");g.addColorStop(0.35+chcPct*0.35,"#78716c");g.addColorStop(1,"#1c1917");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+chcPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(120,113,108,"+(0.45+chcPct*0.55)+")";ctx.lineWidth=3.5+chcPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(chcPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(168,162,158,"+(chcPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=chcPct>0.88?"#a8a29e":"#fafaf9";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(chcPct>0.88?"\U0001fab6":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="brucite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="chlorite_fox9e"){\n'
  '    const bf9eChl609=(Math.sin((Date.now()-t.spawnedAt)*0.3210)+1)/2;\n'
  '    t._bf9eChl609=bf9eChl609;\n'
  '    drawChloriteFox9e(ctx,t.radius,ts,bf9eChl609);\n'
  '  }\n'
  '  else if(t.type==="chalcocite_orb9e"){\n'
  '    const ao9eChc609=(Math.sin((Date.now()-t.spawnedAt)*0.3214)+1)/2;\n'
  '    t._ao9eChc609=ao9eChc609;\n'
  '    drawChalcociteOrb9e(ctx,t.radius,ts,ao9eChc609);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="brucite_fox9e"){'
A7_NEW = (
  'if(hit.type==="chlorite_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo609bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult609bf=gs.feverActive?2:1;\n'
  '      const isPeak609bf=((hit._bf9eChl609||0)>0.85);\n'
  '      const pts609bf=Math.round((isPeak609bf?506:316)*combo609bf*feverMult609bf);\n'
  '      gs.score+=pts609bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1746,"#166534");\n'
  '      if(isPeak609bf){spawnPopup(hit.x,hit.y-28,"\U0001f33f +"+pts609bf,theme.accent);unlock("chlorite_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts609bf,theme.accent);}\n'
  '      unlock("chlorite_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="chalcocite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo609ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult609ao=gs.feverActive?2:1;\n'
  '      const isPeak609ao=((hit._ao9eChc609||0)>0.85);\n'
  '      const pts609ao=Math.round((isPeak609ao?508:318)*combo609ao*feverMult609ao);\n'
  '      gs.score+=pts609ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1748,"#78716c");\n'
  '      if(isPeak609ao){spawnPopup(hit.x,hit.y-28,"\U0001fab6 +"+pts609ao,theme.accent);unlock("chalcocite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts609ao,theme.accent);}\n'
  '      unlock("chalcocite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="brucite_fox9e";color="#bae6fd";glow="#f0f9ff";'
A8_NEW = (
  'type="chlorite_fox9e";color="#166534";glow="#dcfce7";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="chalcocite_orb9e";color="#78716c";glow="#fafaf9";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="brucite_fox9e"?BASE_R*1.06:type==="bustamite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="chlorite_fox9e"?BASE_R*1.06:type==="chalcocite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'NEXUS_STORM39B10:"\U000026a1\U0001f300",SOLAR_WAVE39B10:"\U00002600️\U0001f30a",'
A10_NEW = 'AURORA_STORM39B10:"\U0001f30c\U000026c8️",THUNDER_CREST39B10:"⚡\U0001f451",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 609 done! +{delta} bytes")
