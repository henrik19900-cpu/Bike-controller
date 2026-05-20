import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"polylithionite_orb9e_peak", label:"Polylithionite Peak", desc:"Reach peak with Polylithionite Orb", icon:"🔹", xp:120 },'
A1_NEW=(
  '{ id:"polylithionite_orb9e_peak", label:"Polylithionite Peak", desc:"Reach peak with Polylithionite Orb", icon:"🔹", xp:120 },\n'
  '  { id:"void_surge42_use", label:"Void Surge 42", desc:"Activate VOID_SURGE42 power-up", icon:"🕳️", xp:60 },\n'
  '  { id:"void_surge42_max", label:"Void Surger 42", desc:"Reach max with VOID_SURGE42 active", icon:"🕳️", xp:120 },\n'
  '  { id:"thunder_surge42_use", label:"Thunder Surge 42", desc:"Activate THUNDER_SURGE42 power-up", icon:"⚡", xp:60 },\n'
  '  { id:"thunder_surge42_max", label:"Thunder Surger 42", desc:"Reach max with THUNDER_SURGE42 active", icon:"⚡", xp:120 },\n'
  '  { id:"powellite_fox9e_tap", label:"Powellite Fox", desc:"Tap Powellite Fox target", icon:"🌕", xp:60 },\n'
  '  { id:"powellite_fox9e_peak", label:"Powellite Peak", desc:"Reach peak with Powellite Fox", icon:"🌕", xp:120 },\n'
  '  { id:"pucherite_orb9e_tap", label:"Pucherite Orb", desc:"Tap Pucherite Orb target", icon:"🟫", xp:60 },\n'
  '  { id:"pucherite_orb9e_peak", label:"Pucherite Orb Peak", desc:"Reach peak with Pucherite Orb", icon:"🟫", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"AURORA_SURGE42","PRISM_SURGE42","ECLIPSE_SURGE42"'
A2_NEW='"VOID_SURGE42","THUNDER_SURGE42","AURORA_SURGE42","PRISM_SURGE42","ECLIPSE_SURGE42"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="AURORA_SURGE42"){\n        gs.score+=2164;showPopup(cx,cy-1874,"+2164 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03ee",2036);if(gs.score>=bonusTotal)unlock("aurora_surge42_max");\n      } else if(ptype==="PRISM_SURGE42"){'
A3_NEW=(
  '  } else if(ptype==="VOID_SURGE42"){\n'
  '        gs.score+=2168;showPopup(cx,cy-1878,"+2168 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a03f0",2040);if(gs.score>=bonusTotal)unlock("void_surge42_max");\n'
  '      } else if(ptype==="THUNDER_SURGE42"){\n'
  '        gs.score+=2170;showPopup(cx,cy-1880,"+2170 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a08c4",2042);if(gs.score>=bonusTotal)unlock("thunder_surge42_max");\n'
  '      } else if(ptype==="AURORA_SURGE42"){\n'
  '        gs.score+=2164;showPopup(cx,cy-1874,"+2164 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03ee",2036);if(gs.score>=bonusTotal)unlock("aurora_surge42_max");\n'
  '      } else if(ptype==="PRISM_SURGE42"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // AURORA_SURGE42 — +2164 aurora surge bonus\n      if(ptype==="AURORA_SURGE42"){sfx("powerUp",1827);unlock("aurora_surge42_use");}'
A4_NEW=(
  '  // VOID_SURGE42 — +2168 void surge bonus\n'
  '      if(ptype==="VOID_SURGE42"){sfx("powerUp",1831);unlock("void_surge42_use");}\n'
  '      // THUNDER_SURGE42 — +2170 thunder surge bonus\n'
  '      if(ptype==="THUNDER_SURGE42"){sfx("powerUp",1833);unlock("thunder_surge42_use");}\n'
  '  // AURORA_SURGE42 — +2164 aurora surge bonus\n'
  '      if(ptype==="AURORA_SURGE42"){sfx("powerUp",1827);unlock("aurora_surge42_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPolycraseFox9e('
A5_NEW=(
  'function drawPowelliteFox9e(ctx,r,ts,powPct){\n'
  '  const bob=Math.sin(ts*0.3746)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+powPct*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(powPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(202,138,4,"+(powPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=powPct>0.88?"#713f12":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(powPct>0.88?"🌕":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPucheriteOrb9e(ctx,r,ts,pucPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3750);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+pucPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+pucPct*0.35,"#92400e");g.addColorStop(1,"#1c0a00");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+pucPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(146,64,14,"+(0.45+pucPct*0.55)+")";ctx.lineWidth=3.5+pucPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(pucPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(217,119,6,"+(pucPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=pucPct>0.88?"#92400e":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pucPct>0.88?"🟫":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPolycraseFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="polycrase_fox9e"){\n      const polcrPct=Math.min(1,(ts-t.born)/2800);t._polcrPct=polcrPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPolycraseFox9e(ctx,t.radius,ts,polcrPct);ctx.restore();\n    } else if(t.type==="polylithionite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="powellite_fox9e"){\n'
  '      const powPct=Math.min(1,(ts-t.born)/2800);t._powPct=powPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPowelliteFox9e(ctx,t.radius,ts,powPct);ctx.restore();\n'
  '    } else if(t.type==="pucherite_orb9e"){\n'
  '      const pucPct=Math.min(1,(ts-t.born)/2800);t._pucPct=pucPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPucheriteOrb9e(ctx,t.radius,ts,pucPct);ctx.restore();\n'
  '    } else if(t.type==="polycrase_fox9e"){\n'
  '      const polcrPct=Math.min(1,(ts-t.born)/2800);t._polcrPct=polcrPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPolycraseFox9e(ctx,t.radius,ts,polcrPct);ctx.restore();\n'
  '    } else if(t.type==="polylithionite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="polycrase_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(334*(hit._polcrPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#111827",2010);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌑",theme.accent,22);\n        unlock("polycrase_fox9e_tap");\n        if((hit._polcrPct||0)>0.88)unlock("polycrase_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="polylithionite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="powellite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(336*(hit._powPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ca8a04",2014);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌕",theme.accent,22);\n'
  '        unlock("powellite_fox9e_tap");\n'
  '        if((hit._powPct||0)>0.88)unlock("powellite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pucherite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(331*(hit._pucPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#92400e",2016);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟫",theme.accent,22);\n'
  '        unlock("pucherite_orb9e_tap");\n'
  '        if((hit._pucPct||0)>0.88)unlock("pucherite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="polycrase_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(334*(hit._polcrPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#111827",2010);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌑",theme.accent,22);\n'
  '        unlock("polycrase_fox9e_tap");\n'
  '        if((hit._polcrPct||0)>0.88)unlock("polycrase_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="polylithionite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="polycrase_fox9e";color="#111827";glow="#f3f4f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polylithionite_orb9e"')
A8_NEW=('      type="powellite_fox9e";color="#ca8a04";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pucherite_orb9e";color="#92400e";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polycrase_fox9e";color="#111827";glow="#f3f4f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polylithionite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="polycrase_fox9e"?BASE_R*1.22:type==="polylithionite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="powellite_fox9e"?BASE_R*1.22:type==="pucherite_orb9e"?BASE_R*1.21:type==="polycrase_fox9e"?BASE_R*1.22:type==="polylithionite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='AURORA_SURGE42:"🌌💠",PRISM_SURGE42:"🔆💠",ECLIPSE_SURGE42:"🌑💠"'
A10_NEW='VOID_SURGE42:"🕳️💠",THUNDER_SURGE42:"⚡💠",AURORA_SURGE42:"🌌💠",PRISM_SURGE42:"🔆💠",ECLIPSE_SURGE42:"🌑💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("void_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"VOID_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="VOID_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1831)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPowelliteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="powellite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="powellite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="powellite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="powellite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('VOID_SURGE42:"🕳️💠"')>=2 else "Step 10 FAIL")
print(f"Batch 676 done! +{len(src)-len(orig)} bytes")
