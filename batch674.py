import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"pinakiolite_orb9e_peak", label:"Pinakiolite Orb Peak", desc:"Reach peak with Pinakiolite Orb", icon:"⚫", xp:120 },'
A1_NEW=(
  '{ id:"pinakiolite_orb9e_peak", label:"Pinakiolite Orb Peak", desc:"Reach peak with Pinakiolite Orb", icon:"⚫", xp:120 },\n'
  '  { id:"eclipse_surge42_use", label:"Eclipse Surge 42", desc:"Activate ECLIPSE_SURGE42 power-up", icon:"🌑", xp:60 },\n'
  '  { id:"eclipse_surge42_max", label:"Eclipse Surger 42", desc:"Reach max with ECLIPSE_SURGE42 active", icon:"🌑", xp:120 },\n'
  '  { id:"nexus_surge42_use", label:"Nexus Surge 42", desc:"Activate NEXUS_SURGE42 power-up", icon:"💫", xp:60 },\n'
  '  { id:"nexus_surge42_max", label:"Nexus Surger 42", desc:"Reach max with NEXUS_SURGE42 active", icon:"💫", xp:120 },\n'
  '  { id:"plancheite_fox9e_tap", label:"Plancheite Fox", desc:"Tap Plancheite Fox target", icon:"🔵", xp:60 },\n'
  '  { id:"plancheite_fox9e_peak", label:"Plancheite Peak", desc:"Reach peak with Plancheite Fox", icon:"🔵", xp:120 },\n'
  '  { id:"polianite_orb9e_tap", label:"Polianite Orb", desc:"Tap Polianite Orb target", icon:"🖤", xp:60 },\n'
  '  { id:"polianite_orb9e_peak", label:"Polianite Orb Peak", desc:"Reach peak with Polianite Orb", icon:"🖤", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"SOLAR_SURGE42","ORBIT_WAVE41","NOVA_SURGE42"'
A2_NEW='"ECLIPSE_SURGE42","NEXUS_SURGE42","SOLAR_SURGE42","ORBIT_WAVE41","NOVA_SURGE42"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="SOLAR_SURGE42"){\n        gs.score+=2156;showPopup(cx,cy-1866,"+2156 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a03ea",2028);if(gs.score>=bonusTotal)unlock("solar_surge42_max");\n      } else if(ptype==="ORBIT_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="ECLIPSE_SURGE42"){\n'
  '        gs.score+=2160;showPopup(cx,cy-1870,"+2160 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a03ec",2032);if(gs.score>=bonusTotal)unlock("eclipse_surge42_max");\n'
  '      } else if(ptype==="NEXUS_SURGE42"){\n'
  '        gs.score+=2162;showPopup(cx,cy-1872,"+2162 💫",theme.accent,26);spawnShockwave(cx,cy,"#0a08c0",2034);if(gs.score>=bonusTotal)unlock("nexus_surge42_max");\n'
  '      } else if(ptype==="SOLAR_SURGE42"){\n'
  '        gs.score+=2156;showPopup(cx,cy-1866,"+2156 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a03ea",2028);if(gs.score>=bonusTotal)unlock("solar_surge42_max");\n'
  '      } else if(ptype==="ORBIT_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // SOLAR_SURGE42 — +2156 solar surge bonus\n      if(ptype==="SOLAR_SURGE42"){sfx("powerUp",1819);unlock("solar_surge42_use");}'
A4_NEW=(
  '  // ECLIPSE_SURGE42 — +2160 eclipse surge bonus\n'
  '      if(ptype==="ECLIPSE_SURGE42"){sfx("powerUp",1823);unlock("eclipse_surge42_use");}\n'
  '      // NEXUS_SURGE42 — +2162 nexus surge bonus\n'
  '      if(ptype==="NEXUS_SURGE42"){sfx("powerUp",1825);unlock("nexus_surge42_use");}\n'
  '  // SOLAR_SURGE42 — +2156 solar surge bonus\n'
  '      if(ptype==="SOLAR_SURGE42"){sfx("powerUp",1819);unlock("solar_surge42_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPiemontiteFox9e('
A5_NEW=(
  'function drawPlancheiteFox9e(ctx,r,ts,planPct){\n'
  '  const bob=Math.sin(ts*0.3730)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+planPct*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(planPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(37,99,235,"+(planPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=planPct>0.88?"#1e3a8a":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(planPct>0.88?"🔵":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPolianiteOrb9e(ctx,r,ts,polPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3734);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+polPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f3f4f6");g.addColorStop(0.35+polPct*0.35,"#1f2937");g.addColorStop(1,"#030712");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+polPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(31,41,55,"+(0.45+polPct*0.55)+")";ctx.lineWidth=3.5+polPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(polPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(107,114,128,"+(polPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=polPct>0.88?"#1f2937":"#f3f4f6";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(polPct>0.88?"🖤":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPiemontiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="piemontite_fox9e"){\n      const piePct=Math.min(1,(ts-t.born)/2800);t._piePct=piePct;\n      ctx.save();ctx.translate(t.x,t.y);drawPiemontiteFox9e(ctx,t.radius,ts,piePct);ctx.restore();\n    } else if(t.type==="pinakiolite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="plancheite_fox9e"){\n'
  '      const planPct=Math.min(1,(ts-t.born)/2800);t._planPct=planPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPlancheiteFox9e(ctx,t.radius,ts,planPct);ctx.restore();\n'
  '    } else if(t.type==="polianite_orb9e"){\n'
  '      const polPct=Math.min(1,(ts-t.born)/2800);t._polPct=polPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPolianiteOrb9e(ctx,t.radius,ts,polPct);ctx.restore();\n'
  '    } else if(t.type==="piemontite_fox9e"){\n'
  '      const piePct=Math.min(1,(ts-t.born)/2800);t._piePct=piePct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPiemontiteFox9e(ctx,t.radius,ts,piePct);ctx.restore();\n'
  '    } else if(t.type==="pinakiolite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="piemontite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(330*(hit._piePct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#9333ea",2002);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟣",theme.accent,22);\n        unlock("piemontite_fox9e_tap");\n        if((hit._piePct||0)>0.88)unlock("piemontite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="pinakiolite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="plancheite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(332*(hit._planPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#2563eb",2006);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔵",theme.accent,22);\n'
  '        unlock("plancheite_fox9e_tap");\n'
  '        if((hit._planPct||0)>0.88)unlock("plancheite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="polianite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(327*(hit._polPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#1f2937",2008);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🖤",theme.accent,22);\n'
  '        unlock("polianite_orb9e_tap");\n'
  '        if((hit._polPct||0)>0.88)unlock("polianite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="piemontite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(330*(hit._piePct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#9333ea",2002);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟣",theme.accent,22);\n'
  '        unlock("piemontite_fox9e_tap");\n'
  '        if((hit._piePct||0)>0.88)unlock("piemontite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pinakiolite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="piemontite_fox9e";color="#9333ea";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pinakiolite_orb9e"')
A8_NEW=('      type="plancheite_fox9e";color="#2563eb";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polianite_orb9e";color="#1f2937";glow="#f3f4f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="piemontite_fox9e";color="#9333ea";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pinakiolite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="piemontite_fox9e"?BASE_R*1.22:type==="pinakiolite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="plancheite_fox9e"?BASE_R*1.22:type==="polianite_orb9e"?BASE_R*1.21:type==="piemontite_fox9e"?BASE_R*1.22:type==="pinakiolite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='SOLAR_SURGE42:"☀️💠",ORBIT_WAVE41:"🪐💠",NOVA_SURGE42:"💥💠"'
A10_NEW='ECLIPSE_SURGE42:"🌑💠",NEXUS_SURGE42:"💫💠",SOLAR_SURGE42:"☀️💠",ORBIT_WAVE41:"🪐💠",NOVA_SURGE42:"💥💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("eclipse_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"ECLIPSE_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="ECLIPSE_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1823)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPlancheiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="plancheite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="plancheite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="plancheite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="plancheite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('ECLIPSE_SURGE42:"🌑💠"')>=2 else "Step 10 FAIL")
print(f"Batch 674 done! +{len(src)-len(orig)} bytes")
