import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"paragonite_orb9e_peak", label:"Paragonite Orb Peak", desc:"Reach peak with Paragonite Orb", icon:"🪩", xp:120 },'
A1_NEW=(
  '{ id:"paragonite_orb9e_peak", label:"Paragonite Orb Peak", desc:"Reach peak with Paragonite Orb", icon:"🪩", xp:120 },\n'
  '  { id:"quake_wave41_use", label:"Quake Wave", desc:"Activate QUAKE_WAVE41 power-up", icon:"🌋", xp:60 },\n'
  '  { id:"quake_wave41_max", label:"Quake Waver", desc:"Reach max with QUAKE_WAVE41 active", icon:"🌋", xp:120 },\n'
  '  { id:"wind_surge41_use", label:"Wind Surge", desc:"Activate WIND_SURGE41 power-up", icon:"💨", xp:60 },\n'
  '  { id:"wind_surge41_max", label:"Wind Surger", desc:"Reach max with WIND_SURGE41 active", icon:"💨", xp:120 },\n'
  '  { id:"pargasite_fox9e_tap", label:"Pargasite Fox", desc:"Tap Pargasite Fox target", icon:"🌲", xp:60 },\n'
  '  { id:"pargasite_fox9e_peak", label:"Pargasite Peak", desc:"Reach peak with Pargasite Fox", icon:"🌲", xp:120 },\n'
  '  { id:"petalite_orb9e_tap", label:"Petalite Orb", desc:"Tap Petalite Orb target", icon:"🌸", xp:60 },\n'
  '  { id:"petalite_orb9e_peak", label:"Petalite Orb Peak", desc:"Reach peak with Petalite Orb", icon:"🌸", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"BOLT_WAVE41","HAZE_SURGE41","STORM_SURGE41"'
A2_NEW='"QUAKE_WAVE41","WIND_SURGE41","BOLT_WAVE41","HAZE_SURGE41","STORM_SURGE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="BOLT_WAVE41"){\n        gs.score+=2144;showPopup(cx,cy-1854,"+2144 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03e4",2016);if(gs.score>=bonusTotal)unlock("bolt_wave41_max");\n      } else if(ptype==="HAZE_SURGE41"){'
A3_NEW=(
  '  } else if(ptype==="QUAKE_WAVE41"){\n'
  '        gs.score+=2148;showPopup(cx,cy-1858,"+2148 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03e6",2020);if(gs.score>=bonusTotal)unlock("quake_wave41_max");\n'
  '      } else if(ptype==="WIND_SURGE41"){\n'
  '        gs.score+=2150;showPopup(cx,cy-1860,"+2150 💨",theme.accent,26);spawnShockwave(cx,cy,"#0a08ba",2022);if(gs.score>=bonusTotal)unlock("wind_surge41_max");\n'
  '      } else if(ptype==="BOLT_WAVE41"){\n'
  '        gs.score+=2144;showPopup(cx,cy-1854,"+2144 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03e4",2016);if(gs.score>=bonusTotal)unlock("bolt_wave41_max");\n'
  '      } else if(ptype==="HAZE_SURGE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // BOLT_WAVE41 — +2144 bolt wave bonus\n      if(ptype==="BOLT_WAVE41"){sfx("powerUp",1807);unlock("bolt_wave41_use");}'
A4_NEW=(
  '  // QUAKE_WAVE41 — +2148 quake wave bonus\n'
  '      if(ptype==="QUAKE_WAVE41"){sfx("powerUp",1811);unlock("quake_wave41_use");}\n'
  '      // WIND_SURGE41 — +2150 wind surge bonus\n'
  '      if(ptype==="WIND_SURGE41"){sfx("powerUp",1813);unlock("wind_surge41_use");}\n'
  '  // BOLT_WAVE41 — +2144 bolt wave bonus\n'
  '      if(ptype==="BOLT_WAVE41"){sfx("powerUp",1807);unlock("bolt_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawPalygorskiteFox9e('
A5_NEW=(
  'function drawPargasiteFox9e(ctx,r,ts,pgaPct){\n'
  '  const bob=Math.sin(ts*0.3706)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+pgaPct*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(pgaPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(22,101,52,"+(pgaPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=pgaPct>0.88?"#052e16":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pgaPct>0.88?"🌲":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPetaliteOrb9e(ctx,r,ts,petPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3710);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+petPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.35+petPct*0.35,"#db2777");g.addColorStop(1,"#500724");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+petPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(219,39,119,"+(0.45+petPct*0.55)+")";ctx.lineWidth=3.5+petPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(petPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(249,168,212,"+(petPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=petPct>0.88?"#db2777":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(petPct>0.88?"🌸":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawPalygorskiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="palygorskite_fox9e"){\n      const palPct=Math.min(1,(ts-t.born)/2800);t._palPct=palPct;\n      ctx.save();ctx.translate(t.x,t.y);drawPalygorskiteFox9e(ctx,t.radius,ts,palPct);ctx.restore();\n    } else if(t.type==="paragonite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="pargasite_fox9e"){\n'
  '      const pgaPct=Math.min(1,(ts-t.born)/2800);t._pgaPct=pgaPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPargasiteFox9e(ctx,t.radius,ts,pgaPct);ctx.restore();\n'
  '    } else if(t.type==="petalite_orb9e"){\n'
  '      const petPct=Math.min(1,(ts-t.born)/2800);t._petPct=petPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPetaliteOrb9e(ctx,t.radius,ts,petPct);ctx.restore();\n'
  '    } else if(t.type==="palygorskite_fox9e"){\n'
  '      const palPct=Math.min(1,(ts-t.born)/2800);t._palPct=palPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPalygorskiteFox9e(ctx,t.radius,ts,palPct);ctx.restore();\n'
  '    } else if(t.type==="paragonite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="palygorskite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(324*(hit._palPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#e5e7eb",1990);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🤍",theme.accent,22);\n        unlock("palygorskite_fox9e_tap");\n        if((hit._palPct||0)>0.88)unlock("palygorskite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="paragonite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="pargasite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(326*(hit._pgaPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#166534",1994);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌲",theme.accent,22);\n'
  '        unlock("pargasite_fox9e_tap");\n'
  '        if((hit._pgaPct||0)>0.88)unlock("pargasite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="petalite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(321*(hit._petPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#db2777",1996);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌸",theme.accent,22);\n'
  '        unlock("petalite_orb9e_tap");\n'
  '        if((hit._petPct||0)>0.88)unlock("petalite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="palygorskite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(324*(hit._palPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#e5e7eb",1990);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🤍",theme.accent,22);\n'
  '        unlock("palygorskite_fox9e_tap");\n'
  '        if((hit._palPct||0)>0.88)unlock("palygorskite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="paragonite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="palygorskite_fox9e";color="#e5e7eb";glow="#fafafa";\n'
        '    } else if('+COND100F+'){\n'
        '      type="paragonite_orb9e"')
A8_NEW=('      type="pargasite_fox9e";color="#166534";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="petalite_orb9e";color="#db2777";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="palygorskite_fox9e";color="#e5e7eb";glow="#fafafa";\n'
        '    } else if('+COND100F+'){\n'
        '      type="paragonite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="palygorskite_fox9e"?BASE_R*1.22:type==="paragonite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="pargasite_fox9e"?BASE_R*1.22:type==="petalite_orb9e"?BASE_R*1.21:type==="palygorskite_fox9e"?BASE_R*1.22:type==="paragonite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='BOLT_WAVE41:"⚡💠",HAZE_SURGE41:"🌫️💠",STORM_SURGE41:"⛈️💠"'
A10_NEW='QUAKE_WAVE41:"🌋💠",WIND_SURGE41:"💨💠",BOLT_WAVE41:"⚡💠",HAZE_SURGE41:"🌫️💠",STORM_SURGE41:"⛈️💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("quake_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"QUAKE_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="QUAKE_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1811)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPargasiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="pargasite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="pargasite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="pargasite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="pargasite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('QUAKE_WAVE41:"🌋💠"')>=2 else "Step 10 FAIL")
print(f"Batch 671 done! +{len(src)-len(orig)} bytes")
