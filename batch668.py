import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"olivenite_orb9e_peak", label:"Olivenite Orb Peak", desc:"Reach peak with Olivenite Orb", icon:"🫒", xp:120 },'
A1_NEW=(
  '{ id:"olivenite_orb9e_peak", label:"Olivenite Orb Peak", desc:"Reach peak with Olivenite Orb", icon:"🫒", xp:120 },\n'
  '  { id:"gust_wave41_use", label:"Gust Wave", desc:"Activate GUST_WAVE41 power-up", icon:"💨", xp:60 },\n'
  '  { id:"gust_wave41_max", label:"Gust Waver", desc:"Reach max with GUST_WAVE41 active", icon:"💨", xp:120 },\n'
  '  { id:"tide_surge41_use", label:"Tide Surge", desc:"Activate TIDE_SURGE41 power-up", icon:"🌊", xp:60 },\n'
  '  { id:"tide_surge41_max", label:"Tide Surger", desc:"Reach max with TIDE_SURGE41 active", icon:"🌊", xp:120 },\n'
  '  { id:"omphacite_fox9e_tap", label:"Omphacite Fox", desc:"Tap Omphacite Fox target", icon:"💚", xp:60 },\n'
  '  { id:"omphacite_fox9e_peak", label:"Omphacite Peak", desc:"Reach peak with Omphacite Fox", icon:"💚", xp:120 },\n'
  '  { id:"orpiment_orb9e_tap", label:"Orpiment Orb", desc:"Tap Orpiment Orb target", icon:"🌼", xp:60 },\n'
  '  { id:"orpiment_orb9e_peak", label:"Orpiment Orb Peak", desc:"Reach peak with Orpiment Orb", icon:"🌼", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"RADIANT_WAVE41","PULSE_SURGE41","VORTEX_WAVE41"'
A2_NEW='"GUST_WAVE41","TIDE_SURGE41","RADIANT_WAVE41","PULSE_SURGE41","VORTEX_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="RADIANT_WAVE41"){\n        gs.score+=2132;showPopup(cx,cy-1842,"+2132 ✨",theme.accent,26);spawnShockwave(cx,cy,"#0a03de",2004);if(gs.score>=bonusTotal)unlock("radiant_wave41_max");\n      } else if(ptype==="PULSE_SURGE41"){'
A3_NEW=(
  '  } else if(ptype==="GUST_WAVE41"){\n'
  '        gs.score+=2136;showPopup(cx,cy-1846,"+2136 💨",theme.accent,26);spawnShockwave(cx,cy,"#0a03e0",2008);if(gs.score>=bonusTotal)unlock("gust_wave41_max");\n'
  '      } else if(ptype==="TIDE_SURGE41"){\n'
  '        gs.score+=2138;showPopup(cx,cy-1848,"+2138 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a08b4",2010);if(gs.score>=bonusTotal)unlock("tide_surge41_max");\n'
  '      } else if(ptype==="RADIANT_WAVE41"){\n'
  '        gs.score+=2132;showPopup(cx,cy-1842,"+2132 ✨",theme.accent,26);spawnShockwave(cx,cy,"#0a03de",2004);if(gs.score>=bonusTotal)unlock("radiant_wave41_max");\n'
  '      } else if(ptype==="PULSE_SURGE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // RADIANT_WAVE41 — +2132 radiant wave bonus\n      if(ptype==="RADIANT_WAVE41"){sfx("powerUp",1795);unlock("radiant_wave41_use");}'
A4_NEW=(
  '  // GUST_WAVE41 — +2136 gust wave bonus\n'
  '      if(ptype==="GUST_WAVE41"){sfx("powerUp",1799);unlock("gust_wave41_use");}\n'
  '      // TIDE_SURGE41 — +2138 tide surge bonus\n'
  '      if(ptype==="TIDE_SURGE41"){sfx("powerUp",1801);unlock("tide_surge41_use");}\n'
  '  // RADIANT_WAVE41 — +2132 radiant wave bonus\n'
  '      if(ptype==="RADIANT_WAVE41"){sfx("powerUp",1795);unlock("radiant_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawOligoclaseFox9e('
A5_NEW=(
  'function drawOmphaciteFox9e(ctx,r,ts,ompPct){\n'
  '  const bob=Math.sin(ts*0.3682)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+ompPct*0.35,"#059669");g.addColorStop(1,"#064e3b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(ompPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(5,150,105,"+(ompPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=ompPct>0.88?"#064e3b":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ompPct>0.88?"💚":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOrpimentOrb9e(ctx,r,ts,orpPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3686);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+orpPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fffbeb");g.addColorStop(0.35+orpPct*0.35,"#d97706");g.addColorStop(1,"#451a03");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+orpPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+orpPct*0.55)+")";ctx.lineWidth=3.5+orpPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(orpPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(252,211,77,"+(orpPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=orpPct>0.88?"#d97706":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(orpPct>0.88?"🌼":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOligoclaseFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="oligoclase_fox9e"){\n      const oliPct=Math.min(1,(ts-t.born)/2800);t._oliPct=oliPct;\n      ctx.save();ctx.translate(t.x,t.y);drawOligoclaseFox9e(ctx,t.radius,ts,oliPct);ctx.restore();\n    } else if(t.type==="olivenite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="omphacite_fox9e"){\n'
  '      const ompPct=Math.min(1,(ts-t.born)/2800);t._ompPct=ompPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOmphaciteFox9e(ctx,t.radius,ts,ompPct);ctx.restore();\n'
  '    } else if(t.type==="orpiment_orb9e"){\n'
  '      const orpPct=Math.min(1,(ts-t.born)/2800);t._orpPct=orpPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOrpimentOrb9e(ctx,t.radius,ts,orpPct);ctx.restore();\n'
  '    } else if(t.type==="oligoclase_fox9e"){\n'
  '      const oliPct=Math.min(1,(ts-t.born)/2800);t._oliPct=oliPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOligoclaseFox9e(ctx,t.radius,ts,oliPct);ctx.restore();\n'
  '    } else if(t.type==="olivenite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="oligoclase_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(318*(hit._oliPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#94a3b8",1978);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" ⚪",theme.accent,22);\n        unlock("oligoclase_fox9e_tap");\n        if((hit._oliPct||0)>0.88)unlock("oligoclase_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="olivenite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="omphacite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(320*(hit._ompPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#059669",1982);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n'
  '        unlock("omphacite_fox9e_tap");\n'
  '        if((hit._ompPct||0)>0.88)unlock("omphacite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="orpiment_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(315*(hit._orpPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#d97706",1984);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌼",theme.accent,22);\n'
  '        unlock("orpiment_orb9e_tap");\n'
  '        if((hit._orpPct||0)>0.88)unlock("orpiment_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="oligoclase_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(318*(hit._oliPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#94a3b8",1978);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" ⚪",theme.accent,22);\n'
  '        unlock("oligoclase_fox9e_tap");\n'
  '        if((hit._oliPct||0)>0.88)unlock("oligoclase_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="olivenite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="oligoclase_fox9e";color="#94a3b8";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="olivenite_orb9e"')
A8_NEW=('      type="omphacite_fox9e";color="#059669";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="orpiment_orb9e";color="#d97706";glow="#fffbeb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="oligoclase_fox9e";color="#94a3b8";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="olivenite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="oligoclase_fox9e"?BASE_R*1.22:type==="olivenite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="omphacite_fox9e"?BASE_R*1.22:type==="orpiment_orb9e"?BASE_R*1.21:type==="oligoclase_fox9e"?BASE_R*1.22:type==="olivenite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='RADIANT_WAVE41:"✨💠",PULSE_SURGE41:"💫💠",VORTEX_WAVE41:"🌀💠"'
A10_NEW='GUST_WAVE41:"💨💠",TIDE_SURGE41:"🌊💠",RADIANT_WAVE41:"✨💠",PULSE_SURGE41:"💫💠",VORTEX_WAVE41:"🌀💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("gust_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"GUST_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="GUST_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1799)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawOmphaciteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="omphacite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="omphacite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="omphacite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="omphacite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('GUST_WAVE41:"💨💠"')>=2 else "Step 10 FAIL")
print(f"Batch 668 done! +{len(src)-len(orig)} bytes")
