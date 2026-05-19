#!/usr/bin/env python3
# Batch 610: NEXUS_NOVA39B10 + SOLAR_STORM39B10 + CorundumFox9e + CristobaliteOrb9e + 8 achievements

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
content = open(SRC, encoding="utf-8").read()
orig_len = len(content)

# ── STEP 1: Achievements ──────────────────────────────────────────────────────
A1_OLD = '{ id:"chalcocite_orb9e_peak",  label:"Chalcocite Orb Peak",       desc:"Tap chalcocite_orb9e at >85%",         icon:"\U0001f52e", xp:88 },'
A1_NEW = A1_OLD + (
  '\n  { id:"nexus_nova39b10_use",   label:"Nexus Nova 39B10",          desc:"Activate NEXUS_NOVA39B10",              icon:"\U0001f4ab", xp:44 },'
  '\n  { id:"nexus_nova39b10_max",   label:"Nexus Nova Max 39B10",      desc:"Score 1904 pts in NEXUS_NOVA39B10",     icon:"\U0001f4ab", xp:88 },'
  '\n  { id:"solar_storm39b10_use",  label:"Solar Storm 39B10",          desc:"Activate SOLAR_STORM39B10",             icon:"\U00002600️", xp:44 },'
  '\n  { id:"solar_storm39b10_max",  label:"Solar Storm Max 39B10",      desc:"Score 1906 pts in SOLAR_STORM39B10",    icon:"\U00002600️", xp:88 },'
  '\n  { id:"corundum_fox9e_tap",    label:"Corundum Fox",               desc:"Tap corundum_fox9e",                    icon:"\U0001f98a", xp:44 },'
  '\n  { id:"corundum_fox9e_peak",   label:"Corundum Fox Peak",          desc:"Tap corundum_fox9e at >85% charge",     icon:"\U0001f98a", xp:88 },'
  '\n  { id:"cristobalite_orb9e_tap",  label:"Cristobalite Orb",         desc:"Tap cristobalite_orb9e",                icon:"\U0001f52e", xp:44 },'
  '\n  { id:"cristobalite_orb9e_peak", label:"Cristobalite Orb Peak",    desc:"Tap cristobalite_orb9e at >85%",       icon:"\U0001f52e", xp:88 },'
)
assert content.count(A1_OLD) == 1, f"Step 1 count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2: pt[] array ────────────────────────────────────────────────────────
A2_OLD = '"AURORA_STORM39B10","THUNDER_CREST39B10",'
A2_NEW = '"NEXUS_NOVA39B10","SOLAR_STORM39B10",' + A2_OLD
assert content.count(A2_OLD) == 1, f"Step 2 count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3: ptype activation block ───────────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_STORM39B10"){'
A3_NEW = (
  '} else if(ptype==="NEXUS_NOVA39B10"){\n'
  '    activePwrRef.current.push({type:"NEXUS_NOVA39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1567);\n'
  '    showNotif("\U0001f4ab\U0001f300 NEXUS NOVA 39B10!");unlock("nexus_nova39b10_use");\n'
  '  } else if(ptype==="SOLAR_STORM39B10"){\n'
  '    activePwrRef.current.push({type:"SOLAR_STORM39B10",left:12000});\n'
  '    sfx("powerUp");sfx("comboNote",1569);\n'
  '    showNotif("\U00002600️\U000026c8️ SOLAR STORM 39B10!");unlock("solar_storm39b10_use");\n'
  '  ' + A3_OLD
)
assert content.count(A3_OLD) == 1, f"Step 3 count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4: per-tap bonus blocks ──────────────────────────────────────────────
A4_OLD = '// AURORA_STORM39B10 — +1900 aurora bonus'
A4_NEW = (
  '// NEXUS_NOVA39B10 — +1904 nexus bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="NEXUS_NOVA39B10")){\n'
  '    const bonusTotal=Math.round(90.2*1000);\n'
  '    gs.score+=1904;showPopup(cx,cy-1614,"+1904 \U0001f4ab\U0001f300",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a036c",1776);\n'
  '    if(gs.score>=bonusTotal)unlock("nexus_nova39b10_max");\n'
  '  }\n'
  '  // SOLAR_STORM39B10 — +1906 solar bonus\n'
  '  if(activePwrRef.current.some(p=>p.type==="SOLAR_STORM39B10")){\n'
  '    const bonusTotal=Math.round(90.3*1000);\n'
  '    gs.score+=1906;showPopup(cx,cy-1616,"+1906 \U00002600️\U000026c8️",theme.accent,26);\n'
  '    spawnShockwave(cx,cy,"#0a0840",1778);\n'
  '    if(gs.score>=bonusTotal)unlock("solar_storm39b10_max");\n'
  '  }\n'
  '  ' + A4_OLD
)
assert content.count(A4_OLD) == 1, f"Step 4 count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawChloriteFox9e('
FOX_FN = (
  'function drawCorundumFox9e(ctx,r,ts,corPct){\n'
  '  const bob=Math.sin(ts*0.3218)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+corPct*0.35,"#be185d");g.addColorStop(1,"#831843");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(corPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(190,24,93,"+(corPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=corPct>0.88?"#f9a8d4":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(corPct>0.88?"\U0001f48e":"\U0001f98a",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
ORB_FN = (
  'function drawCristobaliteOrb9e(ctx,r,ts,criPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3222);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+criPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+criPct*0.35,"#e2e8f0");g.addColorStop(1,"#64748b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+criPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(226,232,240,"+(0.45+criPct*0.55)+")";ctx.lineWidth=3.5+criPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(criPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(203,213,225,"+(criPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=criPct>0.88?"#cbd5e1":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(criPct>0.88?"❄️":"\U0001f52e",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
)
A5_NEW = FOX_FN + ORB_FN + A5_OLD
assert content.count(A5_OLD) == 1, f"Step 5 count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6: drawTarget dispatch ───────────────────────────────────────────────
A6_OLD = '  else if(t.type==="chlorite_fox9e"){'
A6_NEW = (
  '  else if(t.type==="corundum_fox9e"){\n'
  '    const bf9eCor610=(Math.sin((Date.now()-t.spawnedAt)*0.3218)+1)/2;\n'
  '    t._bf9eCor610=bf9eCor610;\n'
  '    drawCorundumFox9e(ctx,t.radius,ts,bf9eCor610);\n'
  '  }\n'
  '  else if(t.type==="cristobalite_orb9e"){\n'
  '    const ao9eCri610=(Math.sin((Date.now()-t.spawnedAt)*0.3222)+1)/2;\n'
  '    t._ao9eCri610=ao9eCri610;\n'
  '    drawCristobaliteOrb9e(ctx,t.radius,ts,ao9eCri610);\n'
  '  }\n'
  '  ' + A6_OLD
)
assert content.count(A6_OLD) == 1, f"Step 6 count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7: handleTap ─────────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="chlorite_fox9e"){'
A7_NEW = (
  'if(hit.type==="corundum_fox9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo610bf=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult610bf=gs.feverActive?2:1;\n'
  '      const isPeak610bf=((hit._bf9eCor610||0)>0.85);\n'
  '      const pts610bf=Math.round((isPeak610bf?510:320)*combo610bf*feverMult610bf);\n'
  '      gs.score+=pts610bf;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1750,"#be185d");\n'
  '      if(isPeak610bf){spawnPopup(hit.x,hit.y-28,"\U0001f48e +"+pts610bf,theme.accent);unlock("corundum_fox9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f98a +"+pts610bf,theme.accent);}\n'
  '      unlock("corundum_fox9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    if(hit.type==="cristobalite_orb9e"){\n'
  '      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '      const combo610ao=Math.min(10,1+Math.floor(gs.streak/5));\n'
  '      const feverMult610ao=gs.feverActive?2:1;\n'
  '      const isPeak610ao=((hit._ao9eCri610||0)>0.85);\n'
  '      const pts610ao=Math.round((isPeak610ao?512:322)*combo610ao*feverMult610ao);\n'
  '      gs.score+=pts610ao;gs.streak++;gs.lastTapTime=Date.now();\n'
  '      spawnShockwave(hit.x,hit.y,1752,"#e2e8f0");\n'
  '      if(isPeak610ao){spawnPopup(hit.x,hit.y-28,"❄️ +"+pts610ao,theme.accent);unlock("cristobalite_orb9e_peak");}\n'
  '      else{spawnPopup(hit.x,hit.y-26,"\U0001f52e +"+pts610ao,theme.accent);}\n'
  '      unlock("cristobalite_orb9e_tap");\n'
  '      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});\n'
  '      debounceSave();return;\n'
  '    }\n'
  '    ' + A7_OLD
)
assert content.count(A7_OLD) == 1, f"Step 7 count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────────
A8_OLD = 'type="chlorite_fox9e";color="#166534";glow="#dcfce7";'
A8_NEW = (
  'type="corundum_fox9e";color="#be185d";glow="#fdf2f8";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      type="cristobalite_orb9e";color="#e2e8f0";glow="#f8fafc";\n'
  '    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n'
  '      ' + A8_OLD
)
assert content.count(A8_OLD) == 1, f"Step 8 count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9: radius chain ──────────────────────────────────────────────────────
A9_OLD = 'type==="chlorite_fox9e"?BASE_R*1.06:type==="chalcocite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="corundum_fox9e"?BASE_R*1.06:type==="cristobalite_orb9e"?BASE_R*1.05:' + A9_OLD
assert content.count(A9_OLD) == 1, f"Step 9 count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10: icon map (replace_all — appears twice) ───────────────────────────
A10_OLD = 'AURORA_STORM39B10:"\U0001f30c\U000026c8️",THUNDER_CREST39B10:"⚡\U0001f451",'
A10_NEW = 'NEXUS_NOVA39B10:"\U0001f4ab\U0001f300",SOLAR_STORM39B10:"\U00002600️\U000026c8️",' + A10_OLD
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

# ── Write ─────────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(content)
delta = len(content) - orig_len
print(f"Batch 610 done! +{delta} bytes")
