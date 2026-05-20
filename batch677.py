import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"pucherite_orb9e_peak", label:"Pucherite Orb Peak", desc:"Reach peak with Pucherite Orb", icon:"🟫", xp:120 },'
A1_NEW=(
  '{ id:"pucherite_orb9e_peak", label:"Pucherite Orb Peak", desc:"Reach peak with Pucherite Orb", icon:"🟫", xp:120 },\n'
  '  { id:"crystal_surge42_use", label:"Crystal Surge 42", desc:"Activate CRYSTAL_SURGE42 power-up", icon:"💎", xp:60 },\n'
  '  { id:"crystal_surge42_max", label:"Crystal Surger 42", desc:"Reach max with CRYSTAL_SURGE42 active", icon:"💎", xp:120 },\n'
  '  { id:"star_surge42_use", label:"Star Surge 42", desc:"Activate STAR_SURGE42 power-up", icon:"⭐", xp:60 },\n'
  '  { id:"star_surge42_max", label:"Star Surger 42", desc:"Reach max with STAR_SURGE42 active", icon:"⭐", xp:120 },\n'
  '  { id:"purpurite_fox9e_tap", label:"Purpurite Fox", desc:"Tap Purpurite Fox target", icon:"🟣", xp:60 },\n'
  '  { id:"purpurite_fox9e_peak", label:"Purpurite Peak", desc:"Reach peak with Purpurite Fox", icon:"🟣", xp:120 },\n'
  '  { id:"pyrochroite_orb9e_tap", label:"Pyrochroite Orb", desc:"Tap Pyrochroite Orb target", icon:"🌸", xp:60 },\n'
  '  { id:"pyrochroite_orb9e_peak", label:"Pyrochroite Orb Peak", desc:"Reach peak with Pyrochroite Orb", icon:"🌸", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"VOID_SURGE42","THUNDER_SURGE42","AURORA_SURGE42"'
A2_NEW='"CRYSTAL_SURGE42","STAR_SURGE42","VOID_SURGE42","THUNDER_SURGE42","AURORA_SURGE42"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="VOID_SURGE42"){\n        gs.score+=2168;showPopup(cx,cy-1878,"+2168 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a03f0",2040);if(gs.score>=bonusTotal)unlock("void_surge42_max");\n      } else if(ptype==="THUNDER_SURGE42"){'
A3_NEW=(
  '  } else if(ptype==="CRYSTAL_SURGE42"){\n'
  '        gs.score+=2172;showPopup(cx,cy-1882,"+2172 💎",theme.accent,26);spawnShockwave(cx,cy,"#0a03f2",2044);if(gs.score>=bonusTotal)unlock("crystal_surge42_max");\n'
  '      } else if(ptype==="STAR_SURGE42"){\n'
  '        gs.score+=2174;showPopup(cx,cy-1884,"+2174 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#0a08c6",2046);if(gs.score>=bonusTotal)unlock("star_surge42_max");\n'
  '      } else if(ptype==="VOID_SURGE42"){\n'
  '        gs.score+=2168;showPopup(cx,cy-1878,"+2168 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a03f0",2040);if(gs.score>=bonusTotal)unlock("void_surge42_max");\n'
  '      } else if(ptype==="THUNDER_SURGE42"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // VOID_SURGE42 — +2168 void surge bonus\n      if(ptype==="VOID_SURGE42"){sfx("powerUp",1831);unlock("void_surge42_use");}'
A4_NEW=(
  '  // CRYSTAL_SURGE42 — +2172 crystal surge bonus\n'
  '      if(ptype==="CRYSTAL_SURGE42"){sfx("powerUp",1835);unlock("crystal_surge42_use");}\n'
  '      // STAR_SURGE42 — +2174 star surge bonus\n'
  '      if(ptype==="STAR_SURGE42"){sfx("powerUp",1837);unlock("star_surge42_use");}\n'
  '  // VOID_SURGE42 — +2168 void surge bonus\n'
  '      if(ptype==="VOID_SURGE42"){sfx("powerUp",1831);unlock("void_surge42_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPowelliteFox9e('
A5_NEW=(
  'function drawPurpuriteFox9e(ctx,r,ts,purpPct){\n'
  '  const bob=Math.sin(ts*0.3754)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#faf5ff");g.addColorStop(0.45+purpPct*0.35,"#7e22ce");g.addColorStop(1,"#3b0764");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(purpPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(126,34,206,"+(purpPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=purpPct>0.88?"#3b0764":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(purpPct>0.88?"🟣":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPyrochroiteOrb9e(ctx,r,ts,pyroPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3758);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+pyroPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fff1f2");g.addColorStop(0.35+pyroPct*0.35,"#be123c");g.addColorStop(1,"#4c0519");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+pyroPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(190,18,60,"+(0.45+pyroPct*0.55)+")";ctx.lineWidth=3.5+pyroPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(pyroPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(253,164,175,"+(pyroPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=pyroPct>0.88?"#be123c":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pyroPct>0.88?"🌸":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPowelliteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="powellite_fox9e"){\n      const powPct=Math.min(1,(ts-t.born)/2800);t._powPct=powPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPowelliteFox9e(ctx,t.radius,ts,powPct);ctx.restore();\n    } else if(t.type==="pucherite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="purpurite_fox9e"){\n'
  '      const purpPct=Math.min(1,(ts-t.born)/2800);t._purpPct=purpPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPurpuriteFox9e(ctx,t.radius,ts,purpPct);ctx.restore();\n'
  '    } else if(t.type==="pyrochroite_orb9e"){\n'
  '      const pyroPct=Math.min(1,(ts-t.born)/2800);t._pyroPct=pyroPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPyrochroiteOrb9e(ctx,t.radius,ts,pyroPct);ctx.restore();\n'
  '    } else if(t.type==="powellite_fox9e"){\n'
  '      const powPct=Math.min(1,(ts-t.born)/2800);t._powPct=powPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPowelliteFox9e(ctx,t.radius,ts,powPct);ctx.restore();\n'
  '    } else if(t.type==="pucherite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="powellite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(336*(hit._powPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#ca8a04",2014);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌕",theme.accent,22);\n        unlock("powellite_fox9e_tap");\n        if((hit._powPct||0)>0.88)unlock("powellite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="pucherite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="purpurite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(338*(hit._purpPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#7e22ce",2018);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟣",theme.accent,22);\n'
  '        unlock("purpurite_fox9e_tap");\n'
  '        if((hit._purpPct||0)>0.88)unlock("purpurite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pyrochroite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(333*(hit._pyroPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#be123c",2020);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌸",theme.accent,22);\n'
  '        unlock("pyrochroite_orb9e_tap");\n'
  '        if((hit._pyroPct||0)>0.88)unlock("pyrochroite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="powellite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(336*(hit._powPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ca8a04",2014);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌕",theme.accent,22);\n'
  '        unlock("powellite_fox9e_tap");\n'
  '        if((hit._powPct||0)>0.88)unlock("powellite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pucherite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="powellite_fox9e";color="#ca8a04";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pucherite_orb9e"')
A8_NEW=('      type="purpurite_fox9e";color="#7e22ce";glow="#faf5ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pyrochroite_orb9e";color="#be123c";glow="#fff1f2";\n'
        '    } else if('+COND100F+'){\n'
        '      type="powellite_fox9e";color="#ca8a04";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pucherite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="powellite_fox9e"?BASE_R*1.22:type==="pucherite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="purpurite_fox9e"?BASE_R*1.22:type==="pyrochroite_orb9e"?BASE_R*1.21:type==="powellite_fox9e"?BASE_R*1.22:type==="pucherite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='VOID_SURGE42:"🕳️💠",THUNDER_SURGE42:"⚡💠",AURORA_SURGE42:"🌌💠"'
A10_NEW='CRYSTAL_SURGE42:"💎💠",STAR_SURGE42:"⭐💠",VOID_SURGE42:"🕳️💠",THUNDER_SURGE42:"⚡💠",AURORA_SURGE42:"🌌💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("crystal_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"CRYSTAL_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="CRYSTAL_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1835)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPurpuriteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="purpurite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="purpurite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="purpurite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="purpurite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('CRYSTAL_SURGE42:"💎💠"')>=2 else "Step 10 FAIL")
print(f"Batch 677 done! +{len(src)-len(orig)} bytes")
