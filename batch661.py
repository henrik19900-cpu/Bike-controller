import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"melanterite_orb9e_peak", label:"Melanterite Orb Peak", desc:"Reach peak with Melanterite Orb", icon:"🔮", xp:120 },'
A1_NEW=(
  '{ id:"melanterite_orb9e_peak", label:"Melanterite Orb Peak", desc:"Reach peak with Melanterite Orb", icon:"🔮", xp:120 },\n'
  '  { id:"inferno_wave41_use", label:"Inferno Wave", desc:"Activate INFERNO_WAVE41 power-up", icon:"🔥", xp:60 },\n'
  '  { id:"inferno_wave41_max", label:"Inferno Waver", desc:"Reach max with INFERNO_WAVE41 active", icon:"🔥", xp:120 },\n'
  '  { id:"blaze_wave41_use", label:"Blaze Wave", desc:"Activate BLAZE_WAVE41 power-up", icon:"🌊", xp:60 },\n'
  '  { id:"blaze_wave41_max", label:"Blaze Waver", desc:"Reach max with BLAZE_WAVE41 active", icon:"🌊", xp:120 },\n'
  '  { id:"mellite_fox9e_tap", label:"Mellite Fox", desc:"Tap Mellite Fox target", icon:"🍯", xp:60 },\n'
  '  { id:"mellite_fox9e_peak", label:"Mellite Peak", desc:"Reach peak with Mellite Fox", icon:"🍯", xp:120 },\n'
  '  { id:"mesolite_orb9e_tap", label:"Mesolite Orb", desc:"Tap Mesolite Orb target", icon:"🌟", xp:60 },\n'
  '  { id:"mesolite_orb9e_peak", label:"Mesolite Orb Peak", desc:"Reach peak with Mesolite Orb", icon:"🌟", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"THUNDER_WAVE41","BLIZZARD_WAVE41","PRISM_PULSE41"'
A2_NEW='"INFERNO_WAVE41","BLAZE_WAVE41","THUNDER_WAVE41","BLIZZARD_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="THUNDER_WAVE41"){\n        gs.score+=2104;showPopup(cx,cy-1814,"+2104 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03d0",1976);if(gs.score>=bonusTotal)unlock("thunder_wave41_max");\n      } else if(ptype==="BLIZZARD_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="INFERNO_WAVE41"){\n'
  '        gs.score+=2108;showPopup(cx,cy-1818,"+2108 🔥",theme.accent,26);spawnShockwave(cx,cy,"#0a03d2",1980);if(gs.score>=bonusTotal)unlock("inferno_wave41_max");\n'
  '      } else if(ptype==="BLAZE_WAVE41"){\n'
  '        gs.score+=2110;showPopup(cx,cy-1820,"+2110 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a08a6",1982);if(gs.score>=bonusTotal)unlock("blaze_wave41_max");\n'
  '      } else if(ptype==="THUNDER_WAVE41"){\n'
  '        gs.score+=2104;showPopup(cx,cy-1814,"+2104 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03d0",1976);if(gs.score>=bonusTotal)unlock("thunder_wave41_max");\n'
  '      } else if(ptype==="BLIZZARD_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // THUNDER_WAVE41 — +2104 thunder wave bonus\n      if(ptype==="THUNDER_WAVE41"){sfx("powerUp",1767);unlock("thunder_wave41_use");}'
A4_NEW=(
  '  // INFERNO_WAVE41 — +2108 inferno wave bonus\n'
  '      if(ptype==="INFERNO_WAVE41"){sfx("powerUp",1771);unlock("inferno_wave41_use");}\n'
  '      // BLAZE_WAVE41 — +2110 blaze wave bonus\n'
  '      if(ptype==="BLAZE_WAVE41"){sfx("powerUp",1773);unlock("blaze_wave41_use");}\n'
  '  // THUNDER_WAVE41 — +2104 thunder wave bonus\n'
  '      if(ptype==="THUNDER_WAVE41"){sfx("powerUp",1767);unlock("thunder_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawManganiteFox9e('
A5_NEW=(
  'function drawMelliteFox9e(ctx,r,ts,melPct){\n'
  '  const bob=Math.sin(ts*0.3626)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.45+melPct*0.35,"#f59e0b");g.addColorStop(1,"#78350f");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(melPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(245,158,11,"+(melPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=melPct>0.88?"#78350f":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(melPct>0.88?"🍯":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMesoliteOrb9e(ctx,r,ts,mesPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3630);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+mesPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+mesPct*0.35,"#94a3b8");g.addColorStop(1,"#1e293b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+mesPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(148,163,184,"+(0.45+mesPct*0.55)+")";ctx.lineWidth=3.5+mesPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(mesPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(226,232,240,"+(mesPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=mesPct>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(mesPct>0.88?"🌟":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawManganiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="manganite_fox9e"){\n      const manPct=Math.min(1,(ts-t.born)/2800);t._manPct=manPct;\n      ctx.save();ctx.translate(t.x,t.y);drawManganiteFox9e(ctx,t.radius,ts,manPct);ctx.restore();\n    } else if(t.type==="melanterite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="mellite_fox9e"){\n'
  '      const mellPct=Math.min(1,(ts-t.born)/2800);t._mellPct=mellPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMelliteFox9e(ctx,t.radius,ts,mellPct);ctx.restore();\n'
  '    } else if(t.type==="mesolite_orb9e"){\n'
  '      const mesolPct=Math.min(1,(ts-t.born)/2800);t._mesolPct=mesolPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMesoliteOrb9e(ctx,t.radius,ts,mesolPct);ctx.restore();\n'
  '    } else if(t.type==="manganite_fox9e"){\n'
  '      const manPct=Math.min(1,(ts-t.born)/2800);t._manPct=manPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawManganiteFox9e(ctx,t.radius,ts,manPct);ctx.restore();\n'
  '    } else if(t.type==="melanterite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="manganite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(304*(hit._manPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#4b5563",1950);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n        unlock("manganite_fox9e_tap");\n        if((hit._manPct||0)>0.88)unlock("manganite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="melanterite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="mellite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(306*(hit._mellPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#f59e0b",1954);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🍯",theme.accent,22);\n'
  '        unlock("mellite_fox9e_tap");\n'
  '        if((hit._mellPct||0)>0.88)unlock("mellite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="mesolite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(301*(hit._mesolPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#94a3b8",1956);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌟",theme.accent,22);\n'
  '        unlock("mesolite_orb9e_tap");\n'
  '        if((hit._mesolPct||0)>0.88)unlock("mesolite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="manganite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(304*(hit._manPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#4b5563",1950);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
  '        unlock("manganite_fox9e_tap");\n'
  '        if((hit._manPct||0)>0.88)unlock("manganite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="melanterite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="manganite_fox9e";color="#4b5563";glow="#f9fafb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="melanterite_orb9e"')
A8_NEW=('      type="mellite_fox9e";color="#f59e0b";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mesolite_orb9e";color="#94a3b8";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="manganite_fox9e";color="#4b5563";glow="#f9fafb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="melanterite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="manganite_fox9e"?BASE_R*1.22:type==="melanterite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="mellite_fox9e"?BASE_R*1.22:type==="mesolite_orb9e"?BASE_R*1.21:type==="manganite_fox9e"?BASE_R*1.22:type==="melanterite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='THUNDER_WAVE41:"⚡💠",BLIZZARD_WAVE41:"🌨️💠",'
A10_NEW='INFERNO_WAVE41:"🔥💠",BLAZE_WAVE41:"🌊💠",THUNDER_WAVE41:"⚡💠",BLIZZARD_WAVE41:"🌨️💠",'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("inferno_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"INFERNO_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="INFERNO_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1771)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawMelliteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="mellite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="mellite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="mellite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="mellite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('INFERNO_WAVE41:"🔥💠"')>=2 else "Step 10 FAIL")
print(f"Batch 661 done! +{len(src)-len(orig)} bytes")
