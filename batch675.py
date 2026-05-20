import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"polianite_orb9e_peak", label:"Polianite Orb Peak", desc:"Reach peak with Polianite Orb", icon:"🖤", xp:120 },'
A1_NEW=(
  '{ id:"polianite_orb9e_peak", label:"Polianite Orb Peak", desc:"Reach peak with Polianite Orb", icon:"🖤", xp:120 },\n'
  '  { id:"aurora_surge42_use", label:"Aurora Surge 42", desc:"Activate AURORA_SURGE42 power-up", icon:"🌌", xp:60 },\n'
  '  { id:"aurora_surge42_max", label:"Aurora Surger 42", desc:"Reach max with AURORA_SURGE42 active", icon:"🌌", xp:120 },\n'
  '  { id:"prism_surge42_use", label:"Prism Surge 42", desc:"Activate PRISM_SURGE42 power-up", icon:"🔆", xp:60 },\n'
  '  { id:"prism_surge42_max", label:"Prism Surger 42", desc:"Reach max with PRISM_SURGE42 active", icon:"🔆", xp:120 },\n'
  '  { id:"polycrase_fox9e_tap", label:"Polycrase Fox", desc:"Tap Polycrase Fox target", icon:"🌑", xp:60 },\n'
  '  { id:"polycrase_fox9e_peak", label:"Polycrase Peak", desc:"Reach peak with Polycrase Fox", icon:"🌑", xp:120 },\n'
  '  { id:"polylithionite_orb9e_tap", label:"Polylithionite Orb", desc:"Tap Polylithionite Orb target", icon:"🔹", xp:60 },\n'
  '  { id:"polylithionite_orb9e_peak", label:"Polylithionite Peak", desc:"Reach peak with Polylithionite Orb", icon:"🔹", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"ECLIPSE_SURGE42","NEXUS_SURGE42","SOLAR_SURGE42"'
A2_NEW='"AURORA_SURGE42","PRISM_SURGE42","ECLIPSE_SURGE42","NEXUS_SURGE42","SOLAR_SURGE42"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="ECLIPSE_SURGE42"){\n        gs.score+=2160;showPopup(cx,cy-1870,"+2160 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a03ec",2032);if(gs.score>=bonusTotal)unlock("eclipse_surge42_max");\n      } else if(ptype==="NEXUS_SURGE42"){'
A3_NEW=(
  '  } else if(ptype==="AURORA_SURGE42"){\n'
  '        gs.score+=2164;showPopup(cx,cy-1874,"+2164 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a03ee",2036);if(gs.score>=bonusTotal)unlock("aurora_surge42_max");\n'
  '      } else if(ptype==="PRISM_SURGE42"){\n'
  '        gs.score+=2166;showPopup(cx,cy-1876,"+2166 🔆",theme.accent,26);spawnShockwave(cx,cy,"#0a08c2",2038);if(gs.score>=bonusTotal)unlock("prism_surge42_max");\n'
  '      } else if(ptype==="ECLIPSE_SURGE42"){\n'
  '        gs.score+=2160;showPopup(cx,cy-1870,"+2160 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a03ec",2032);if(gs.score>=bonusTotal)unlock("eclipse_surge42_max");\n'
  '      } else if(ptype==="NEXUS_SURGE42"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // ECLIPSE_SURGE42 — +2160 eclipse surge bonus\n      if(ptype==="ECLIPSE_SURGE42"){sfx("powerUp",1823);unlock("eclipse_surge42_use");}'
A4_NEW=(
  '  // AURORA_SURGE42 — +2164 aurora surge bonus\n'
  '      if(ptype==="AURORA_SURGE42"){sfx("powerUp",1827);unlock("aurora_surge42_use");}\n'
  '      // PRISM_SURGE42 — +2166 prism surge bonus\n'
  '      if(ptype==="PRISM_SURGE42"){sfx("powerUp",1829);unlock("prism_surge42_use");}\n'
  '  // ECLIPSE_SURGE42 — +2160 eclipse surge bonus\n'
  '      if(ptype==="ECLIPSE_SURGE42"){sfx("powerUp",1823);unlock("eclipse_surge42_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPlancheiteFox9e('
A5_NEW=(
  'function drawPolycraseFox9e(ctx,r,ts,polcrPct){\n'
  '  const bob=Math.sin(ts*0.3738)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f3f4f6");g.addColorStop(0.45+polcrPct*0.35,"#111827");g.addColorStop(1,"#030712");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(polcrPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(17,24,39,"+(polcrPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=polcrPct>0.88?"#030712":"#f3f4f6";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(polcrPct>0.88?"🌑":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPolylithioniteOrb9e(ctx,r,ts,polyPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3742);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+polyPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.35+polyPct*0.35,"#7dd3fc");g.addColorStop(1,"#0c4a6e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+polyPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(125,211,252,"+(0.45+polyPct*0.55)+")";ctx.lineWidth=3.5+polyPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(polyPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(186,230,253,"+(polyPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=polyPct>0.88?"#7dd3fc":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(polyPct>0.88?"🔹":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPlancheiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="plancheite_fox9e"){\n      const planPct=Math.min(1,(ts-t.born)/2800);t._planPct=planPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPlancheiteFox9e(ctx,t.radius,ts,planPct);ctx.restore();\n    } else if(t.type==="polianite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="polycrase_fox9e"){\n'
  '      const polcrPct=Math.min(1,(ts-t.born)/2800);t._polcrPct=polcrPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPolycraseFox9e(ctx,t.radius,ts,polcrPct);ctx.restore();\n'
  '    } else if(t.type==="polylithionite_orb9e"){\n'
  '      const polyPct=Math.min(1,(ts-t.born)/2800);t._polyPct=polyPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPolylithioniteOrb9e(ctx,t.radius,ts,polyPct);ctx.restore();\n'
  '    } else if(t.type==="plancheite_fox9e"){\n'
  '      const planPct=Math.min(1,(ts-t.born)/2800);t._planPct=planPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPlancheiteFox9e(ctx,t.radius,ts,planPct);ctx.restore();\n'
  '    } else if(t.type==="polianite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="plancheite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(332*(hit._planPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#2563eb",2006);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔵",theme.accent,22);\n        unlock("plancheite_fox9e_tap");\n        if((hit._planPct||0)>0.88)unlock("plancheite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="polianite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="polycrase_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(334*(hit._polcrPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#111827",2010);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌑",theme.accent,22);\n'
  '        unlock("polycrase_fox9e_tap");\n'
  '        if((hit._polcrPct||0)>0.88)unlock("polycrase_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="polylithionite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(329*(hit._polyPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#7dd3fc",2012);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔹",theme.accent,22);\n'
  '        unlock("polylithionite_orb9e_tap");\n'
  '        if((hit._polyPct||0)>0.88)unlock("polylithionite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="plancheite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(332*(hit._planPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#2563eb",2006);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔵",theme.accent,22);\n'
  '        unlock("plancheite_fox9e_tap");\n'
  '        if((hit._planPct||0)>0.88)unlock("plancheite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="polianite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="plancheite_fox9e";color="#2563eb";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polianite_orb9e"')
A8_NEW=('      type="polycrase_fox9e";color="#111827";glow="#f3f4f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polylithionite_orb9e";color="#7dd3fc";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="plancheite_fox9e";color="#2563eb";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="polianite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="plancheite_fox9e"?BASE_R*1.22:type==="polianite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="polycrase_fox9e"?BASE_R*1.22:type==="polylithionite_orb9e"?BASE_R*1.21:type==="plancheite_fox9e"?BASE_R*1.22:type==="polianite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='ECLIPSE_SURGE42:"🌑💠",NEXUS_SURGE42:"💫💠",SOLAR_SURGE42:"☀️💠"'
A10_NEW='AURORA_SURGE42:"🌌💠",PRISM_SURGE42:"🔆💠",ECLIPSE_SURGE42:"🌑💠",NEXUS_SURGE42:"💫💠",SOLAR_SURGE42:"☀️💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("aurora_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"AURORA_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="AURORA_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1827)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPolycraseFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="polycrase_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="polycrase_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="polycrase_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="polycrase_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('AURORA_SURGE42:"🌌💠"')>=2 else "Step 10 FAIL")
print(f"Batch 675 done! +{len(src)-len(orig)} bytes")
