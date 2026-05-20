import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"ottemannite_orb9e_peak", label:"Ottemannite Orb Peak", desc:"Reach peak with Ottemannite Orb", icon:"🔘", xp:120 },'
A1_NEW=(
  '{ id:"ottemannite_orb9e_peak", label:"Ottemannite Orb Peak", desc:"Reach peak with Ottemannite Orb", icon:"🔘", xp:120 },\n'
  '  { id:"bolt_wave41_use", label:"Bolt Wave", desc:"Activate BOLT_WAVE41 power-up", icon:"⚡", xp:60 },\n'
  '  { id:"bolt_wave41_max", label:"Bolt Waver", desc:"Reach max with BOLT_WAVE41 active", icon:"⚡", xp:120 },\n'
  '  { id:"haze_surge41_use", label:"Haze Surge", desc:"Activate HAZE_SURGE41 power-up", icon:"🌫️", xp:60 },\n'
  '  { id:"haze_surge41_max", label:"Haze Surger", desc:"Reach max with HAZE_SURGE41 active", icon:"🌫️", xp:120 },\n'
  '  { id:"palygorskite_fox9e_tap", label:"Palygorskite Fox", desc:"Tap Palygorskite Fox target", icon:"🤍", xp:60 },\n'
  '  { id:"palygorskite_fox9e_peak", label:"Palygorskite Peak", desc:"Reach peak with Palygorskite Fox", icon:"🤍", xp:120 },\n'
  '  { id:"paragonite_orb9e_tap", label:"Paragonite Orb", desc:"Tap Paragonite Orb target", icon:"🪩", xp:60 },\n'
  '  { id:"paragonite_orb9e_peak", label:"Paragonite Orb Peak", desc:"Reach peak with Paragonite Orb", icon:"🪩", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"STORM_SURGE41","AURA_WAVE41","GUST_WAVE41"'
A2_NEW='"BOLT_WAVE41","HAZE_SURGE41","STORM_SURGE41","AURA_WAVE41","GUST_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="STORM_SURGE41"){\n        gs.score+=2140;showPopup(cx,cy-1850,"+2140 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#0a03e2",2012);if(gs.score>=bonusTotal)unlock("storm_surge41_max");\n      } else if(ptype==="AURA_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="BOLT_WAVE41"){\n'
  '        gs.score+=2144;showPopup(cx,cy-1854,"+2144 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03e4",2016);if(gs.score>=bonusTotal)unlock("bolt_wave41_max");\n'
  '      } else if(ptype==="HAZE_SURGE41"){\n'
  '        gs.score+=2146;showPopup(cx,cy-1856,"+2146 🌫️",theme.accent,26);spawnShockwave(cx,cy,"#0a08b8",2018);if(gs.score>=bonusTotal)unlock("haze_surge41_max");\n'
  '      } else if(ptype==="STORM_SURGE41"){\n'
  '        gs.score+=2140;showPopup(cx,cy-1850,"+2140 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#0a03e2",2012);if(gs.score>=bonusTotal)unlock("storm_surge41_max");\n'
  '      } else if(ptype==="AURA_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // STORM_SURGE41 — +2140 storm surge bonus\n      if(ptype==="STORM_SURGE41"){sfx("powerUp",1803);unlock("storm_surge41_use");}'
A4_NEW=(
  '  // BOLT_WAVE41 — +2144 bolt wave bonus\n'
  '      if(ptype==="BOLT_WAVE41"){sfx("powerUp",1807);unlock("bolt_wave41_use");}\n'
  '      // HAZE_SURGE41 — +2146 haze surge bonus\n'
  '      if(ptype==="HAZE_SURGE41"){sfx("powerUp",1809);unlock("haze_surge41_use");}\n'
  '  // STORM_SURGE41 — +2140 storm surge bonus\n'
  '      if(ptype==="STORM_SURGE41"){sfx("powerUp",1803);unlock("storm_surge41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawOsumiliteFox9e('
A5_NEW=(
  'function drawPalygorskiteFox9e(ctx,r,ts,palPct){\n'
  '  const bob=Math.sin(ts*0.3698)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fafafa");g.addColorStop(0.45+palPct*0.35,"#e5e7eb");g.addColorStop(1,"#374151");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(palPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(229,231,235,"+(palPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=palPct>0.88?"#374151":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(palPct>0.88?"🤍":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawParagoniteOrb9e(ctx,r,ts,parPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3702);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+parPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.35+parPct*0.35,"#c026d3");g.addColorStop(1,"#4a044e");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+parPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(192,38,211,"+(0.45+parPct*0.55)+")";ctx.lineWidth=3.5+parPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(parPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(240,171,252,"+(parPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=parPct>0.88?"#c026d3":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(parPct>0.88?"🪩":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOsumiliteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="osumilite_fox9e"){\n      const osuPct=Math.min(1,(ts-t.born)/2800);t._osuPct=osuPct;\n      ctx.save();ctx.translate(t.x,t.y);drawOsumiliteFox9e(ctx,t.radius,ts,osuPct);ctx.restore();\n    } else if(t.type==="ottemannite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="palygorskite_fox9e"){\n'
  '      const palPct=Math.min(1,(ts-t.born)/2800);t._palPct=palPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawPalygorskiteFox9e(ctx,t.radius,ts,palPct);ctx.restore();\n'
  '    } else if(t.type==="paragonite_orb9e"){\n'
  '      const parPct=Math.min(1,(ts-t.born)/2800);t._parPct=parPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawParagoniteOrb9e(ctx,t.radius,ts,parPct);ctx.restore();\n'
  '    } else if(t.type==="osumilite_fox9e"){\n'
  '      const osuPct=Math.min(1,(ts-t.born)/2800);t._osuPct=osuPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOsumiliteFox9e(ctx,t.radius,ts,osuPct);ctx.restore();\n'
  '    } else if(t.type==="ottemannite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="osumilite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(322*(hit._osuPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#3b82f6",1986);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💙",theme.accent,22);\n        unlock("osumilite_fox9e_tap");\n        if((hit._osuPct||0)>0.88)unlock("osumilite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="ottemannite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="palygorskite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(324*(hit._palPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#e5e7eb",1990);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🤍",theme.accent,22);\n'
  '        unlock("palygorskite_fox9e_tap");\n'
  '        if((hit._palPct||0)>0.88)unlock("palygorskite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="paragonite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(319*(hit._parPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#c026d3",1992);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🪩",theme.accent,22);\n'
  '        unlock("paragonite_orb9e_tap");\n'
  '        if((hit._parPct||0)>0.88)unlock("paragonite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="osumilite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(322*(hit._osuPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#3b82f6",1986);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💙",theme.accent,22);\n'
  '        unlock("osumilite_fox9e_tap");\n'
  '        if((hit._osuPct||0)>0.88)unlock("osumilite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="ottemannite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="osumilite_fox9e";color="#3b82f6";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ottemannite_orb9e"')
A8_NEW=('      type="palygorskite_fox9e";color="#e5e7eb";glow="#fafafa";\n'
        '    } else if('+COND100F+'){\n'
        '      type="paragonite_orb9e";color="#c026d3";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="osumilite_fox9e";color="#3b82f6";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ottemannite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="osumilite_fox9e"?BASE_R*1.22:type==="ottemannite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="palygorskite_fox9e"?BASE_R*1.22:type==="paragonite_orb9e"?BASE_R*1.21:type==="osumilite_fox9e"?BASE_R*1.22:type==="ottemannite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='STORM_SURGE41:"⛈️💠",AURA_WAVE41:"🌟💠",GUST_WAVE41:"💨💠"'
A10_NEW='BOLT_WAVE41:"⚡💠",HAZE_SURGE41:"🌫️💠",STORM_SURGE41:"⛈️💠",AURA_WAVE41:"🌟💠",GUST_WAVE41:"💨💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("bolt_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"BOLT_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="BOLT_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1807)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawPalygorskiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="palygorskite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="palygorskite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="palygorskite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="palygorskite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('BOLT_WAVE41:"⚡💠"')>=2 else "Step 10 FAIL")
print(f"Batch 670 done! +{len(src)-len(orig)} bytes")
