import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"orpiment_orb9e_peak", label:"Orpiment Orb Peak", desc:"Reach peak with Orpiment Orb", icon:"🌼", xp:120 },'
A1_NEW=(
  '{ id:"orpiment_orb9e_peak", label:"Orpiment Orb Peak", desc:"Reach peak with Orpiment Orb", icon:"🌼", xp:120 },\n'
  '  { id:"storm_surge41_use", label:"Storm Surge", desc:"Activate STORM_SURGE41 power-up", icon:"⛈️", xp:60 },\n'
  '  { id:"storm_surge41_max", label:"Storm Surger", desc:"Reach max with STORM_SURGE41 active", icon:"⛈️", xp:120 },\n'
  '  { id:"aura_wave41_use", label:"Aura Wave", desc:"Activate AURA_WAVE41 power-up", icon:"🌟", xp:60 },\n'
  '  { id:"aura_wave41_max", label:"Aura Waver", desc:"Reach max with AURA_WAVE41 active", icon:"🌟", xp:120 },\n'
  '  { id:"osumilite_fox9e_tap", label:"Osumilite Fox", desc:"Tap Osumilite Fox target", icon:"💙", xp:60 },\n'
  '  { id:"osumilite_fox9e_peak", label:"Osumilite Peak", desc:"Reach peak with Osumilite Fox", icon:"💙", xp:120 },\n'
  '  { id:"ottemannite_orb9e_tap", label:"Ottemannite Orb", desc:"Tap Ottemannite Orb target", icon:"🔘", xp:60 },\n'
  '  { id:"ottemannite_orb9e_peak", label:"Ottemannite Orb Peak", desc:"Reach peak with Ottemannite Orb", icon:"🔘", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"GUST_WAVE41","TIDE_SURGE41","RADIANT_WAVE41"'
A2_NEW='"STORM_SURGE41","AURA_WAVE41","GUST_WAVE41","TIDE_SURGE41","RADIANT_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="GUST_WAVE41"){\n        gs.score+=2136;showPopup(cx,cy-1846,"+2136 💨",theme.accent,26);spawnShockwave(cx,cy,"#0a03e0",2008);if(gs.score>=bonusTotal)unlock("gust_wave41_max");\n      } else if(ptype==="TIDE_SURGE41"){'
A3_NEW=(
  '  } else if(ptype==="STORM_SURGE41"){\n'
  '        gs.score+=2140;showPopup(cx,cy-1850,"+2140 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#0a03e2",2012);if(gs.score>=bonusTotal)unlock("storm_surge41_max");\n'
  '      } else if(ptype==="AURA_WAVE41"){\n'
  '        gs.score+=2142;showPopup(cx,cy-1852,"+2142 🌟",theme.accent,26);spawnShockwave(cx,cy,"#0a08b6",2014);if(gs.score>=bonusTotal)unlock("aura_wave41_max");\n'
  '      } else if(ptype==="GUST_WAVE41"){\n'
  '        gs.score+=2136;showPopup(cx,cy-1846,"+2136 💨",theme.accent,26);spawnShockwave(cx,cy,"#0a03e0",2008);if(gs.score>=bonusTotal)unlock("gust_wave41_max");\n'
  '      } else if(ptype==="TIDE_SURGE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // GUST_WAVE41 — +2136 gust wave bonus\n      if(ptype==="GUST_WAVE41"){sfx("powerUp",1799);unlock("gust_wave41_use");}'
A4_NEW=(
  '  // STORM_SURGE41 — +2140 storm surge bonus\n'
  '      if(ptype==="STORM_SURGE41"){sfx("powerUp",1803);unlock("storm_surge41_use");}\n'
  '      // AURA_WAVE41 — +2142 aura wave bonus\n'
  '      if(ptype==="AURA_WAVE41"){sfx("powerUp",1805);unlock("aura_wave41_use");}\n'
  '  // GUST_WAVE41 — +2136 gust wave bonus\n'
  '      if(ptype==="GUST_WAVE41"){sfx("powerUp",1799);unlock("gust_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawOmphaciteFox9e('
A5_NEW=(
  'function drawOsumiliteFox9e(ctx,r,ts,osuPct){\n'
  '  const bob=Math.sin(ts*0.3690)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+osuPct*0.35,"#3b82f6");g.addColorStop(1,"#1e3a8a");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(osuPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(59,130,246,"+(osuPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=osuPct>0.88?"#1e3a8a":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(osuPct>0.88?"💙":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOttemanniteOrb9e(ctx,r,ts,ottPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3694);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ottPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f9fafb");g.addColorStop(0.35+ottPct*0.35,"#6b7280");g.addColorStop(1,"#111827");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+ottPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(107,114,128,"+(0.45+ottPct*0.55)+")";ctx.lineWidth=3.5+ottPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(ottPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(209,213,219,"+(ottPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=ottPct>0.88?"#6b7280":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ottPct>0.88?"🔘":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOmphaciteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="omphacite_fox9e"){\n      const ompPct=Math.min(1,(ts-t.born)/2800);t._ompPct=ompPct;\n      ctx.save();ctx.translate(t.x,t.y);drawOmphaciteFox9e(ctx,t.radius,ts,ompPct);ctx.restore();\n    } else if(t.type==="orpiment_orb9e"){'
A6_NEW=(
  '  else if(t.type==="osumilite_fox9e"){\n'
  '      const osuPct=Math.min(1,(ts-t.born)/2800);t._osuPct=osuPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOsumiliteFox9e(ctx,t.radius,ts,osuPct);ctx.restore();\n'
  '    } else if(t.type==="ottemannite_orb9e"){\n'
  '      const ottPct=Math.min(1,(ts-t.born)/2800);t._ottPct=ottPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOttemanniteOrb9e(ctx,t.radius,ts,ottPct);ctx.restore();\n'
  '    } else if(t.type==="omphacite_fox9e"){\n'
  '      const ompPct=Math.min(1,(ts-t.born)/2800);t._ompPct=ompPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOmphaciteFox9e(ctx,t.radius,ts,ompPct);ctx.restore();\n'
  '    } else if(t.type==="orpiment_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="omphacite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(320*(hit._ompPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#059669",1982);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n        unlock("omphacite_fox9e_tap");\n        if((hit._ompPct||0)>0.88)unlock("omphacite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="orpiment_orb9e"){'
A7_NEW=(
  '    if(hit.type==="osumilite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(322*(hit._osuPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#3b82f6",1986);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💙",theme.accent,22);\n'
  '        unlock("osumilite_fox9e_tap");\n'
  '        if((hit._osuPct||0)>0.88)unlock("osumilite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="ottemannite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(317*(hit._ottPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#6b7280",1988);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔘",theme.accent,22);\n'
  '        unlock("ottemannite_orb9e_tap");\n'
  '        if((hit._ottPct||0)>0.88)unlock("ottemannite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="omphacite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(320*(hit._ompPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#059669",1982);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n'
  '        unlock("omphacite_fox9e_tap");\n'
  '        if((hit._ompPct||0)>0.88)unlock("omphacite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="orpiment_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="omphacite_fox9e";color="#059669";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="orpiment_orb9e"')
A8_NEW=('      type="osumilite_fox9e";color="#3b82f6";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ottemannite_orb9e";color="#6b7280";glow="#f9fafb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="omphacite_fox9e";color="#059669";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="orpiment_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="omphacite_fox9e"?BASE_R*1.22:type==="orpiment_orb9e"?BASE_R*1.21:'
A9_NEW='type==="osumilite_fox9e"?BASE_R*1.22:type==="ottemannite_orb9e"?BASE_R*1.21:type==="omphacite_fox9e"?BASE_R*1.22:type==="orpiment_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='GUST_WAVE41:"💨💠",TIDE_SURGE41:"🌊💠",RADIANT_WAVE41:"✨💠"'
A10_NEW='STORM_SURGE41:"⛈️💠",AURA_WAVE41:"🌟💠",GUST_WAVE41:"💨💠",TIDE_SURGE41:"🌊💠",RADIANT_WAVE41:"✨💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("storm_surge41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"STORM_SURGE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="STORM_SURGE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1803)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawOsumiliteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="osumilite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="osumilite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="osumilite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="osumilite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('STORM_SURGE41:"⛈️💠"')>=2 else "Step 10 FAIL")
print(f"Batch 669 done! +{len(src)-len(orig)} bytes")
