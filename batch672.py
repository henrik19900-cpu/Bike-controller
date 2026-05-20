import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"petalite_orb9e_peak", label:"Petalite Orb Peak", desc:"Reach peak with Petalite Orb", icon:"🌸", xp:120 },'
A1_NEW=(
  '{ id:"petalite_orb9e_peak", label:"Petalite Orb Peak", desc:"Reach peak with Petalite Orb", icon:"🌸", xp:120 },\n'
  '  { id:"nova_surge42_use", label:"Nova Surge 42", desc:"Activate NOVA_SURGE42 power-up", icon:"💥", xp:60 },\n'
  '  { id:"nova_surge42_max", label:"Nova Surger 42", desc:"Reach max with NOVA_SURGE42 active", icon:"💥", xp:120 },\n'
  '  { id:"moon_wave41_use", label:"Moon Wave", desc:"Activate MOON_WAVE41 power-up", icon:"🌙", xp:60 },\n'
  '  { id:"moon_wave41_max", label:"Moon Waver", desc:"Reach max with MOON_WAVE41 active", icon:"🌙", xp:120 },\n'
  '  { id:"phenakite_fox9e_tap", label:"Phenakite Fox", desc:"Tap Phenakite Fox target", icon:"🔷", xp:60 },\n'
  '  { id:"phenakite_fox9e_peak", label:"Phenakite Peak", desc:"Reach peak with Phenakite Fox", icon:"🔷", xp:120 },\n'
  '  { id:"phosphophyllite_orb9e_tap", label:"Phosphophyllite Orb", desc:"Tap Phosphophyllite Orb target", icon:"🧊", xp:60 },\n'
  '  { id:"phosphophyllite_orb9e_peak", label:"Phosphophyllite Peak", desc:"Reach peak with Phosphophyllite Orb", icon:"🧊", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"QUAKE_WAVE41","WIND_SURGE41","BOLT_WAVE41"'
A2_NEW='"NOVA_SURGE42","MOON_WAVE41","QUAKE_WAVE41","WIND_SURGE41","BOLT_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="QUAKE_WAVE41"){\n        gs.score+=2148;showPopup(cx,cy-1858,"+2148 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03e6",2020);if(gs.score>=bonusTotal)unlock("quake_wave41_max");\n      } else if(ptype==="WIND_SURGE41"){'
A3_NEW=(
  '  } else if(ptype==="NOVA_SURGE42"){\n'
  '        gs.score+=2152;showPopup(cx,cy-1862,"+2152 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a03e8",2024);if(gs.score>=bonusTotal)unlock("nova_surge42_max");\n'
  '      } else if(ptype==="MOON_WAVE41"){\n'
  '        gs.score+=2154;showPopup(cx,cy-1864,"+2154 🌙",theme.accent,26);spawnShockwave(cx,cy,"#0a08bc",2026);if(gs.score>=bonusTotal)unlock("moon_wave41_max");\n'
  '      } else if(ptype==="QUAKE_WAVE41"){\n'
  '        gs.score+=2148;showPopup(cx,cy-1858,"+2148 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03e6",2020);if(gs.score>=bonusTotal)unlock("quake_wave41_max");\n'
  '      } else if(ptype==="WIND_SURGE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // QUAKE_WAVE41 — +2148 quake wave bonus\n      if(ptype==="QUAKE_WAVE41"){sfx("powerUp",1811);unlock("quake_wave41_use");}'
A4_NEW=(
  '  // NOVA_SURGE42 — +2152 nova surge bonus\n'
  '      if(ptype==="NOVA_SURGE42"){sfx("powerUp",1815);unlock("nova_surge42_use");}\n'
  '      // MOON_WAVE41 — +2154 moon wave bonus\n'
  '      if(ptype==="MOON_WAVE41"){sfx("powerUp",1817);unlock("moon_wave41_use");}\n'
  '  // QUAKE_WAVE41 — +2148 quake wave bonus\n'
  '      if(ptype==="QUAKE_WAVE41"){sfx("powerUp",1811);unlock("quake_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPargasiteFox9e('
A5_NEW=(
  'function drawPhenakiteFox9e(ctx,r,ts,phenPct){\n'
  '  const bob=Math.sin(ts*0.3714)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.45+phenPct*0.35,"#0ea5e9");g.addColorStop(1,"#0c4a6e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(phenPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(14,165,233,"+(phenPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=phenPct>0.88?"#0c4a6e":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(phenPct>0.88?"🔷":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPhosphophylliteOrb9e(ctx,r,ts,phosPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3718);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+phosPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfeff");g.addColorStop(0.35+phosPct*0.35,"#06b6d4");g.addColorStop(1,"#083344");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+phosPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(6,182,212,"+(0.45+phosPct*0.55)+")";ctx.lineWidth=3.5+phosPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(phosPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(165,243,252,"+(phosPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=phosPct>0.88?"#06b6d4":"#ecfeff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(phosPct>0.88?"🧊":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPargasiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="pargasite_fox9e"){\n      const pgaPct=Math.min(1,(ts-t.born)/2800);t._pgaPct=pgaPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPargasiteFox9e(ctx,t.radius,ts,pgaPct);ctx.restore();\n    } else if(t.type==="petalite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="phenakite_fox9e"){\n'
  '      const phenPct=Math.min(1,(ts-t.born)/2800);t._phenPct=phenPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPhenakiteFox9e(ctx,t.radius,ts,phenPct);ctx.restore();\n'
  '    } else if(t.type==="phosphophyllite_orb9e"){\n'
  '      const phosPct=Math.min(1,(ts-t.born)/2800);t._phosPct=phosPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPhosphophylliteOrb9e(ctx,t.radius,ts,phosPct);ctx.restore();\n'
  '    } else if(t.type==="pargasite_fox9e"){\n'
  '      const pgaPct=Math.min(1,(ts-t.born)/2800);t._pgaPct=pgaPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPargasiteFox9e(ctx,t.radius,ts,pgaPct);ctx.restore();\n'
  '    } else if(t.type==="petalite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="pargasite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(326*(hit._pgaPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#166534",1994);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌲",theme.accent,22);\n        unlock("pargasite_fox9e_tap");\n        if((hit._pgaPct||0)>0.88)unlock("pargasite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="petalite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="phenakite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(328*(hit._phenPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#0ea5e9",1998);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔷",theme.accent,22);\n'
  '        unlock("phenakite_fox9e_tap");\n'
  '        if((hit._phenPct||0)>0.88)unlock("phenakite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="phosphophyllite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(323*(hit._phosPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#06b6d4",2000);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🧊",theme.accent,22);\n'
  '        unlock("phosphophyllite_orb9e_tap");\n'
  '        if((hit._phosPct||0)>0.88)unlock("phosphophyllite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="pargasite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(326*(hit._pgaPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#166534",1994);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌲",theme.accent,22);\n'
  '        unlock("pargasite_fox9e_tap");\n'
  '        if((hit._pgaPct||0)>0.88)unlock("pargasite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="petalite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="pargasite_fox9e";color="#166534";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="petalite_orb9e"')
A8_NEW=('      type="phenakite_fox9e";color="#0ea5e9";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="phosphophyllite_orb9e";color="#06b6d4";glow="#ecfeff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pargasite_fox9e";color="#166534";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="petalite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="pargasite_fox9e"?BASE_R*1.22:type==="petalite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="phenakite_fox9e"?BASE_R*1.22:type==="phosphophyllite_orb9e"?BASE_R*1.21:type==="pargasite_fox9e"?BASE_R*1.22:type==="petalite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='QUAKE_WAVE41:"🌋💠",WIND_SURGE41:"💨💠",BOLT_WAVE41:"⚡💠"'
A10_NEW='NOVA_SURGE42:"💥💠",MOON_WAVE41:"🌙💠",QUAKE_WAVE41:"🌋💠",WIND_SURGE41:"💨💠",BOLT_WAVE41:"⚡💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("nova_surge42_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"NOVA_SURGE42"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="NOVA_SURGE42"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1815)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPhenakiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="phenakite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="phenakite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="phenakite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="phenakite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('NOVA_SURGE42:"💥💠"')>=2 else "Step 10 FAIL")
print(f"Batch 672 done! +{len(src)-len(orig)} bytes")
