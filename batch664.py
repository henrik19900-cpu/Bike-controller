import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"monazite_orb9e_peak", label:"Monazite Orb Peak", desc:"Reach peak with Monazite Orb", icon:"🟤", xp:120 },'
A1_NEW=(
  '{ id:"monazite_orb9e_peak", label:"Monazite Orb Peak", desc:"Reach peak with Monazite Orb", icon:"🟤", xp:120 },\n'
  '  { id:"plasma_wave41_use", label:"Plasma Wave", desc:"Activate PLASMA_WAVE41 power-up", icon:"💜", xp:60 },\n'
  '  { id:"plasma_wave41_max", label:"Plasma Waver", desc:"Reach max with PLASMA_WAVE41 active", icon:"💜", xp:120 },\n'
  '  { id:"arcane_wave41_use", label:"Arcane Wave", desc:"Activate ARCANE_WAVE41 power-up", icon:"🔮", xp:60 },\n'
  '  { id:"arcane_wave41_max", label:"Arcane Waver", desc:"Reach max with ARCANE_WAVE41 active", icon:"🔮", xp:120 },\n'
  '  { id:"moorhouseite_fox9e_tap", label:"Moorhouseite Fox", desc:"Tap Moorhouseite Fox target", icon:"🌸", xp:60 },\n'
  '  { id:"moorhouseite_fox9e_peak", label:"Moorhouseite Peak", desc:"Reach peak with Moorhouseite Fox", icon:"🌸", xp:120 },\n'
  '  { id:"moissanite_orb9e_tap", label:"Moissanite Orb", desc:"Tap Moissanite Orb target", icon:"💎", xp:60 },\n'
  '  { id:"moissanite_orb9e_peak", label:"Moissanite Orb Peak", desc:"Reach peak with Moissanite Orb", icon:"💎", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"LAVA_WAVE41","SNOW_WAVE41","MAGMA_WAVE41"'
A2_NEW='"PLASMA_WAVE41","ARCANE_WAVE41","LAVA_WAVE41","SNOW_WAVE41","MAGMA_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="LAVA_WAVE41"){\n        gs.score+=2116;showPopup(cx,cy-1826,"+2116 🔴",theme.accent,26);spawnShockwave(cx,cy,"#0a03d6",1988);if(gs.score>=bonusTotal)unlock("lava_wave41_max");\n      } else if(ptype==="SNOW_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="PLASMA_WAVE41"){\n'
  '        gs.score+=2120;showPopup(cx,cy-1830,"+2120 💜",theme.accent,26);spawnShockwave(cx,cy,"#0a03d8",1992);if(gs.score>=bonusTotal)unlock("plasma_wave41_max");\n'
  '      } else if(ptype==="ARCANE_WAVE41"){\n'
  '        gs.score+=2122;showPopup(cx,cy-1832,"+2122 🔮",theme.accent,26);spawnShockwave(cx,cy,"#0a08ac",1994);if(gs.score>=bonusTotal)unlock("arcane_wave41_max");\n'
  '      } else if(ptype==="LAVA_WAVE41"){\n'
  '        gs.score+=2116;showPopup(cx,cy-1826,"+2116 🔴",theme.accent,26);spawnShockwave(cx,cy,"#0a03d6",1988);if(gs.score>=bonusTotal)unlock("lava_wave41_max");\n'
  '      } else if(ptype==="SNOW_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // LAVA_WAVE41 — +2116 lava wave bonus\n      if(ptype==="LAVA_WAVE41"){sfx("powerUp",1779);unlock("lava_wave41_use");}'
A4_NEW=(
  '  // PLASMA_WAVE41 — +2120 plasma wave bonus\n'
  '      if(ptype==="PLASMA_WAVE41"){sfx("powerUp",1783);unlock("plasma_wave41_use");}\n'
  '      // ARCANE_WAVE41 — +2122 arcane wave bonus\n'
  '      if(ptype==="ARCANE_WAVE41"){sfx("powerUp",1785);unlock("arcane_wave41_use");}\n'
  '  // LAVA_WAVE41 — +2116 lava wave bonus\n'
  '      if(ptype==="LAVA_WAVE41"){sfx("powerUp",1779);unlock("lava_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawMirabiileFox9e('
A5_NEW=(
  'function drawMoorhouseiteFox9e(ctx,r,ts,moorPct){\n'
  '  const bob=Math.sin(ts*0.3650)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+moorPct*0.35,"#ec4899");g.addColorStop(1,"#831843");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(moorPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(236,72,153,"+(moorPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=moorPct>0.88?"#831843":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(moorPct>0.88?"🌸":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMoissaniteOrb9e(ctx,r,ts,moiPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3654);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+moiPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.35+moiPct*0.35,"#38bdf8");g.addColorStop(1,"#075985");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+moiPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(56,189,248,"+(0.45+moiPct*0.55)+")";ctx.lineWidth=3.5+moiPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(moiPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(186,230,253,"+(moiPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=moiPct>0.88?"#38bdf8":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(moiPct>0.88?"💎":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMirabiileFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="mirabilite_fox9e"){\n      const mirPct=Math.min(1,(ts-t.born)/2800);t._mirPct=mirPct;\n      ctx.save();ctx.translate(t.x,t.y);drawMirabiileFox9e(ctx,t.radius,ts,mirPct);ctx.restore();\n    } else if(t.type==="monazite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="moorhouseite_fox9e"){\n'
  '      const moorPct=Math.min(1,(ts-t.born)/2800);t._moorPct=moorPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMoorhouseiteFox9e(ctx,t.radius,ts,moorPct);ctx.restore();\n'
  '    } else if(t.type==="moissanite_orb9e"){\n'
  '      const moiPct=Math.min(1,(ts-t.born)/2800);t._moiPct=moiPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMoissaniteOrb9e(ctx,t.radius,ts,moiPct);ctx.restore();\n'
  '    } else if(t.type==="mirabilite_fox9e"){\n'
  '      const mirPct=Math.min(1,(ts-t.born)/2800);t._mirPct=mirPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMirabiileFox9e(ctx,t.radius,ts,mirPct);ctx.restore();\n'
  '    } else if(t.type==="monazite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="mirabilite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(310*(hit._mirPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#fbbf24",1962);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟡",theme.accent,22);\n        unlock("mirabilite_fox9e_tap");\n        if((hit._mirPct||0)>0.88)unlock("mirabilite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="monazite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="moorhouseite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(312*(hit._moorPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ec4899",1966);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌸",theme.accent,22);\n'
  '        unlock("moorhouseite_fox9e_tap");\n'
  '        if((hit._moorPct||0)>0.88)unlock("moorhouseite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="moissanite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(307*(hit._moiPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#38bdf8",1968);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💎",theme.accent,22);\n'
  '        unlock("moissanite_orb9e_tap");\n'
  '        if((hit._moiPct||0)>0.88)unlock("moissanite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="mirabilite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(310*(hit._mirPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#fbbf24",1962);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟡",theme.accent,22);\n'
  '        unlock("mirabilite_fox9e_tap");\n'
  '        if((hit._mirPct||0)>0.88)unlock("mirabilite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="monazite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="mirabilite_fox9e";color="#fbbf24";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="monazite_orb9e"')
A8_NEW=('      type="moorhouseite_fox9e";color="#ec4899";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="moissanite_orb9e";color="#38bdf8";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mirabilite_fox9e";color="#fbbf24";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="monazite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="mirabilite_fox9e"?BASE_R*1.22:type==="monazite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="moorhouseite_fox9e"?BASE_R*1.22:type==="moissanite_orb9e"?BASE_R*1.21:type==="mirabilite_fox9e"?BASE_R*1.22:type==="monazite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='LAVA_WAVE41:"🔴💠",SNOW_WAVE41:"❄️💠",MAGMA_WAVE41:"🌋💠"'
A10_NEW='PLASMA_WAVE41:"💜💠",ARCANE_WAVE41:"🔮💠",LAVA_WAVE41:"🔴💠",SNOW_WAVE41:"❄️💠",MAGMA_WAVE41:"🌋💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("plasma_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"PLASMA_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="PLASMA_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1783)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawMoorhouseiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="moorhouseite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="moorhouseite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="moorhouseite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="moorhouseite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('PLASMA_WAVE41:"💜💠"')>=2 else "Step 10 FAIL")
print(f"Batch 664 done! +{len(src)-len(orig)} bytes")
