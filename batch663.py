import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"millerite_orb9e_peak", label:"Millerite Orb Peak", desc:"Reach peak with Millerite Orb", icon:"🌕", xp:120 },'
A1_NEW=(
  '{ id:"millerite_orb9e_peak", label:"Millerite Orb Peak", desc:"Reach peak with Millerite Orb", icon:"🌕", xp:120 },\n'
  '  { id:"lava_wave41_use", label:"Lava Wave", desc:"Activate LAVA_WAVE41 power-up", icon:"🔴", xp:60 },\n'
  '  { id:"lava_wave41_max", label:"Lava Waver", desc:"Reach max with LAVA_WAVE41 active", icon:"🔴", xp:120 },\n'
  '  { id:"snow_wave41_use", label:"Snow Wave", desc:"Activate SNOW_WAVE41 power-up", icon:"❄️", xp:60 },\n'
  '  { id:"snow_wave41_max", label:"Snow Waver", desc:"Reach max with SNOW_WAVE41 active", icon:"❄️", xp:120 },\n'
  '  { id:"mirabilite_fox9e_tap", label:"Mirabilite Fox", desc:"Tap Mirabilite Fox target", icon:"🟡", xp:60 },\n'
  '  { id:"mirabilite_fox9e_peak", label:"Mirabilite Peak", desc:"Reach peak with Mirabilite Fox", icon:"🟡", xp:120 },\n'
  '  { id:"monazite_orb9e_tap", label:"Monazite Orb", desc:"Tap Monazite Orb target", icon:"🟤", xp:60 },\n'
  '  { id:"monazite_orb9e_peak", label:"Monazite Orb Peak", desc:"Reach peak with Monazite Orb", icon:"🟤", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"MAGMA_WAVE41","FROST_WAVE41","INFERNO_WAVE41"'
A2_NEW='"LAVA_WAVE41","SNOW_WAVE41","MAGMA_WAVE41","FROST_WAVE41","INFERNO_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="MAGMA_WAVE41"){\n        gs.score+=2112;showPopup(cx,cy-1822,"+2112 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03d4",1984);if(gs.score>=bonusTotal)unlock("magma_wave41_max");\n      } else if(ptype==="FROST_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="LAVA_WAVE41"){\n'
  '        gs.score+=2116;showPopup(cx,cy-1826,"+2116 🔴",theme.accent,26);spawnShockwave(cx,cy,"#0a03d6",1988);if(gs.score>=bonusTotal)unlock("lava_wave41_max");\n'
  '      } else if(ptype==="SNOW_WAVE41"){\n'
  '        gs.score+=2118;showPopup(cx,cy-1828,"+2118 ❄️",theme.accent,26);spawnShockwave(cx,cy,"#0a08aa",1990);if(gs.score>=bonusTotal)unlock("snow_wave41_max");\n'
  '      } else if(ptype==="MAGMA_WAVE41"){\n'
  '        gs.score+=2112;showPopup(cx,cy-1822,"+2112 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03d4",1984);if(gs.score>=bonusTotal)unlock("magma_wave41_max");\n'
  '      } else if(ptype==="FROST_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // MAGMA_WAVE41 — +2112 magma wave bonus\n      if(ptype==="MAGMA_WAVE41"){sfx("powerUp",1775);unlock("magma_wave41_use");}'
A4_NEW=(
  '  // LAVA_WAVE41 — +2116 lava wave bonus\n'
  '      if(ptype==="LAVA_WAVE41"){sfx("powerUp",1779);unlock("lava_wave41_use");}\n'
  '      // SNOW_WAVE41 — +2118 snow wave bonus\n'
  '      if(ptype==="SNOW_WAVE41"){sfx("powerUp",1781);unlock("snow_wave41_use");}\n'
  '  // MAGMA_WAVE41 — +2112 magma wave bonus\n'
  '      if(ptype==="MAGMA_WAVE41"){sfx("powerUp",1775);unlock("magma_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawMicroclineFox9e('
A5_NEW=(
  'function drawMirabiileFox9e(ctx,r,ts,mirPct){\n'
  '  const bob=Math.sin(ts*0.3642)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+mirPct*0.35,"#fbbf24");g.addColorStop(1,"#78350f");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(mirPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(251,191,36,"+(mirPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=mirPct>0.88?"#78350f":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(mirPct>0.88?"🟡":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMonaziteOrb9e(ctx,r,ts,monPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3646);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+monPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+monPct*0.35,"#b45309");g.addColorStop(1,"#292524");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+monPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(180,83,9,"+(0.45+monPct*0.55)+")";ctx.lineWidth=3.5+monPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(monPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(217,119,6,"+(monPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=monPct>0.88?"#b45309":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(monPct>0.88?"🟤":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMicroclineFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="microcline_fox9e"){\n      const micPct=Math.min(1,(ts-t.born)/2800);t._micPct=micPct;\n      ctx.save();ctx.translate(t.x,t.y);drawMicroclineFox9e(ctx,t.radius,ts,micPct);ctx.restore();\n    } else if(t.type==="millerite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="mirabilite_fox9e"){\n'
  '      const mirPct=Math.min(1,(ts-t.born)/2800);t._mirPct=mirPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMirabiileFox9e(ctx,t.radius,ts,mirPct);ctx.restore();\n'
  '    } else if(t.type==="monazite_orb9e"){\n'
  '      const monPct=Math.min(1,(ts-t.born)/2800);t._monPct=monPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMonaziteOrb9e(ctx,t.radius,ts,monPct);ctx.restore();\n'
  '    } else if(t.type==="microcline_fox9e"){\n'
  '      const micPct=Math.min(1,(ts-t.born)/2800);t._micPct=micPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMicroclineFox9e(ctx,t.radius,ts,micPct);ctx.restore();\n'
  '    } else if(t.type==="millerite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="microcline_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(308*(hit._micPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#10b981",1958);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n        unlock("microcline_fox9e_tap");\n        if((hit._micPct||0)>0.88)unlock("microcline_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="millerite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="mirabilite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(310*(hit._mirPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#fbbf24",1962);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟡",theme.accent,22);\n'
  '        unlock("mirabilite_fox9e_tap");\n'
  '        if((hit._mirPct||0)>0.88)unlock("mirabilite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="monazite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(305*(hit._monPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#b45309",1964);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟤",theme.accent,22);\n'
  '        unlock("monazite_orb9e_tap");\n'
  '        if((hit._monPct||0)>0.88)unlock("monazite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="microcline_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(308*(hit._micPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#10b981",1958);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n'
  '        unlock("microcline_fox9e_tap");\n'
  '        if((hit._micPct||0)>0.88)unlock("microcline_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="millerite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="microcline_fox9e";color="#10b981";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="millerite_orb9e"')
A8_NEW=('      type="mirabilite_fox9e";color="#fbbf24";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="monazite_orb9e";color="#b45309";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="microcline_fox9e";color="#10b981";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="millerite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="microcline_fox9e"?BASE_R*1.22:type==="millerite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="mirabilite_fox9e"?BASE_R*1.22:type==="monazite_orb9e"?BASE_R*1.21:type==="microcline_fox9e"?BASE_R*1.22:type==="millerite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='MAGMA_WAVE41:"🌋💠",FROST_WAVE41:"❄️💠",INFERNO_WAVE41:"🔥💠"'
A10_NEW='LAVA_WAVE41:"🔴💠",SNOW_WAVE41:"❄️💠",MAGMA_WAVE41:"🌋💠",FROST_WAVE41:"❄️💠",INFERNO_WAVE41:"🔥💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("lava_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"LAVA_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="LAVA_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1779)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawMirabiileFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="mirabilite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="mirabilite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="mirabilite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="mirabilite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('LAVA_WAVE41:"🔴💠"')>=2 else "Step 10 FAIL")
print(f"Batch 663 done! +{len(src)-len(orig)} bytes")
