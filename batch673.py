import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"phosphophyllite_orb9e_peak", label:"Phosphophyllite Peak", desc:"Reach peak with Phosphophyllite Orb", icon:"🧊", xp:120 },'
A1_NEW=(
  '{ id:"phosphophyllite_orb9e_peak", label:"Phosphophyllite Peak", desc:"Reach peak with Phosphophyllite Orb", icon:"🧊", xp:120 },\n'
  '  { id:"solar_surge42_use", label:"Solar Surge 42", desc:"Activate SOLAR_SURGE42 power-up", icon:"☀️", xp:60 },\n'
  '  { id:"solar_surge42_max", label:"Solar Surger 42", desc:"Reach max with SOLAR_SURGE42 active", icon:"☀️", xp:120 },\n'
  '  { id:"orbit_wave41_use", label:"Orbit Wave", desc:"Activate ORBIT_WAVE41 power-up", icon:"🪐", xp:60 },\n'
  '  { id:"orbit_wave41_max", label:"Orbit Waver", desc:"Reach max with ORBIT_WAVE41 active", icon:"🪐", xp:120 },\n'
  '  { id:"piemontite_fox9e_tap", label:"Piemontite Fox", desc:"Tap Piemontite Fox target", icon:"🟣", xp:60 },\n'
  '  { id:"piemontite_fox9e_peak", label:"Piemontite Peak", desc:"Reach peak with Piemontite Fox", icon:"🟣", xp:120 },\n'
  '  { id:"pinakiolite_orb9e_tap", label:"Pinakiolite Orb", desc:"Tap Pinakiolite Orb target", icon:"⚫", xp:60 },\n'
  '  { id:"pinakiolite_orb9e_peak", label:"Pinakiolite Orb Peak", desc:"Reach peak with Pinakiolite Orb", icon:"⚫", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"NOVA_SURGE42","MOON_WAVE41","QUAKE_WAVE41"'
A2_NEW='"SOLAR_SURGE42","ORBIT_WAVE41","NOVA_SURGE42","MOON_WAVE41","QUAKE_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="NOVA_SURGE42"){\n        gs.score+=2152;showPopup(cx,cy-1862,"+2152 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a03e8",2024);if(gs.score>=bonusTotal)unlock("nova_surge42_max");\n      } else if(ptype==="MOON_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="SOLAR_SURGE42"){\n'
  '        gs.score+=2156;showPopup(cx,cy-1866,"+2156 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a03ea",2028);if(gs.score>=bonusTotal)unlock("solar_surge42_max");\n'
  '      } else if(ptype==="ORBIT_WAVE41"){\n'
  '        gs.score+=2158;showPopup(cx,cy-1868,"+2158 🪐",theme.accent,26);spawnShockwave(cx,cy,"#0a08be",2030);if(gs.score>=bonusTotal)unlock("orbit_wave41_max");\n'
  '      } else if(ptype==="NOVA_SURGE42"){\n'
  '        gs.score+=2152;showPopup(cx,cy-1862,"+2152 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a03e8",2024);if(gs.score>=bonusTotal)unlock("nova_surge42_max");\n'
  '      } else if(ptype==="MOON_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // NOVA_SURGE42 — +2152 nova surge bonus\n      if(ptype==="NOVA_SURGE42"){sfx("powerUp",1815);unlock("nova_surge42_use");}'
A4_NEW=(
  '  // SOLAR_SURGE42 — +2156 solar surge bonus\n'
  '      if(ptype==="SOLAR_SURGE42"){sfx("powerUp",1819);unlock("solar_surge42_use");}\n'
  '      // ORBIT_WAVE41 — +2158 orbit wave bonus\n'
  '      if(ptype==="ORBIT_WAVE41"){sfx("powerUp",1821);unlock("orbit_wave41_use");}\n'
  '  // NOVA_SURGE42 — +2152 nova surge bonus\n'
  '      if(ptype==="NOVA_SURGE42"){sfx("powerUp",1815);unlock("nova_surge42_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPhenakiteFox9e('
A5_NEW=(
  'function drawPiemontiteFox9e(ctx,r,ts,piePct){\n'
  '  const bob=Math.sin(ts*0.3722)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.45+piePct*0.35,"#9333ea");g.addColorStop(1,"#3b0764");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(piePct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(147,51,234,"+(piePct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=piePct>0.88?"#3b0764":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(piePct>0.88?"🟣":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPinakioliteOrb9e(ctx,r,ts,pinPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3726);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+pinPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f9fafb");g.addColorStop(0.35+pinPct*0.35,"#374151");g.addColorStop(1,"#030712");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+pinPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(55,65,81,"+(0.45+pinPct*0.55)+")";ctx.lineWidth=3.5+pinPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(pinPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(156,163,175,"+(pinPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=pinPct>0.88?"#374151":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pinPct>0.88?"⚫":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPhenakiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="phenakite_fox9e"){\n      const phenPct=Math.min(1,(ts-t.born)/2800);t._phenPct=phenPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPhenakiteFox9e(ctx,t.radius,ts,phenPct);ctx.restore();\n    } else if(t.type==="phosphophyllite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="piemontite_fox9e"){\n'
  '      const piePct=Math.min(1,(ts-t.born)/2800);t._piePct=piePct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPiemontiteFox9e(ctx,t.radius,ts,piePct);ctx.restore();\n'
  '    } else if(t.type==="pinakiolite_orb9e"){\n'
  '      const pinPct=Math.min(1,(ts-t.born)/2800);t._pinPct=pinPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPinakioliteOrb9e(ctx,t.radius,ts,pinPct);ctx.restore();\n'
  '    } else if(t.type==="phenakite_fox9e"){\n'
  '      const phenPct=Math.min(1,(ts-t.born)/2800);t._phenPct=phenPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPhenakiteFox9e(ctx,t.radius,ts,phenPct);ctx.restore();\n'
  '    } else if(t.type==="phosphophyllite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="phenakite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(328*(hit._phenPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#0ea5e9",1998);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔷",theme.accent,22);\n        unlock("phenakite_fox9e_tap");\n        if((hit._phenPct||0)>0.88)unlock("phenakite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="phosphophyllite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="piemontite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(330*(hit._piePct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#9333ea",2002);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟣",theme.accent,22);\n'
  '        unlock("piemontite_fox9e_tap");\n'
  '        if((hit._piePct||0)>0.88)unlock("piemontite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pinakiolite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(325*(hit._pinPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#374151",2004);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" ⚫",theme.accent,22);\n'
  '        unlock("pinakiolite_orb9e_tap");\n'
  '        if((hit._pinPct||0)>0.88)unlock("pinakiolite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="phenakite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(328*(hit._phenPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#0ea5e9",1998);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔷",theme.accent,22);\n'
  '        unlock("phenakite_fox9e_tap");\n'
  '        if((hit._phenPct||0)>0.88)unlock("phenakite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="phosphophyllite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="phenakite_fox9e";color="#0ea5e9";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="phosphophyllite_orb9e"')
A8_NEW=('      type="piemontite_fox9e";color="#9333ea";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pinakiolite_orb9e";color="#374151";glow="#f9fafb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="phenakite_fox9e";color="#0ea5e9";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="phosphophyllite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="phenakite_fox9e"?BASE_R*1.22:type==="phosphophyllite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="piemontite_fox9e"?BASE_R*1.22:type==="pinakiolite_orb9e"?BASE_R*1.21:type==="phenakite_fox9e"?BASE_R*1.22:type==="phosphophyllite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='NOVA_SURGE42:"💥💠",MOON_WAVE41:"🌙💠",QUAKE_WAVE41:"🌋💠"'
A10_NEW='SOLAR_SURGE42:"☀️💠",ORBIT_WAVE41:"🪐💠",NOVA_SURGE42:"💥💠",MOON_WAVE41:"🌙💠",QUAKE_WAVE41:"🌋💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("solar_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"SOLAR_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="SOLAR_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1819)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPiemontiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="piemontite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="piemontite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="piemontite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="piemontite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('SOLAR_SURGE42:"☀️💠"')>=2 else "Step 10 FAIL")
print(f"Batch 673 done! +{len(src)-len(orig)} bytes")
