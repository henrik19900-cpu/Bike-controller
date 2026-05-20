import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"moissanite_orb9e_peak", label:"Moissanite Orb Peak", desc:"Reach peak with Moissanite Orb", icon:"💎", xp:120 },'
A1_NEW=(
  '{ id:"moissanite_orb9e_peak", label:"Moissanite Orb Peak", desc:"Reach peak with Moissanite Orb", icon:"💎", xp:120 },\n'
  '  { id:"sonic_wave41_use", label:"Sonic Wave", desc:"Activate SONIC_WAVE41 power-up", icon:"🔊", xp:60 },\n'
  '  { id:"sonic_wave41_max", label:"Sonic Waver", desc:"Reach max with SONIC_WAVE41 active", icon:"🔊", xp:120 },\n'
  '  { id:"echo_pulse41_use", label:"Echo Pulse", desc:"Activate ECHO_PULSE41 power-up", icon:"📡", xp:60 },\n'
  '  { id:"echo_pulse41_max", label:"Echo Pulser", desc:"Reach max with ECHO_PULSE41 active", icon:"📡", xp:120 },\n'
  '  { id:"mottramite_fox9e_tap", label:"Mottramite Fox", desc:"Tap Mottramite Fox target", icon:"🟢", xp:60 },\n'
  '  { id:"mottramite_fox9e_peak", label:"Mottramite Peak", desc:"Reach peak with Mottramite Fox", icon:"🟢", xp:120 },\n'
  '  { id:"muscovite_orb9e_tap", label:"Muscovite Orb", desc:"Tap Muscovite Orb target", icon:"🪨", xp:60 },\n'
  '  { id:"muscovite_orb9e_peak", label:"Muscovite Orb Peak", desc:"Reach peak with Muscovite Orb", icon:"🪨", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"PLASMA_WAVE41","ARCANE_WAVE41","LAVA_WAVE41"'
A2_NEW='"SONIC_WAVE41","ECHO_PULSE41","PLASMA_WAVE41","ARCANE_WAVE41","LAVA_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="PLASMA_WAVE41"){\n        gs.score+=2120;showPopup(cx,cy-1830,"+2120 💜",theme.accent,26);spawnShockwave(cx,cy,"#0a03d8",1992);if(gs.score>=bonusTotal)unlock("plasma_wave41_max");\n      } else if(ptype==="ARCANE_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="SONIC_WAVE41"){\n'
  '        gs.score+=2124;showPopup(cx,cy-1834,"+2124 🔊",theme.accent,26);spawnShockwave(cx,cy,"#0a03da",1996);if(gs.score>=bonusTotal)unlock("sonic_wave41_max");\n'
  '      } else if(ptype==="ECHO_PULSE41"){\n'
  '        gs.score+=2126;showPopup(cx,cy-1836,"+2126 📡",theme.accent,26);spawnShockwave(cx,cy,"#0a08ae",1998);if(gs.score>=bonusTotal)unlock("echo_pulse41_max");\n'
  '      } else if(ptype==="PLASMA_WAVE41"){\n'
  '        gs.score+=2120;showPopup(cx,cy-1830,"+2120 💜",theme.accent,26);spawnShockwave(cx,cy,"#0a03d8",1992);if(gs.score>=bonusTotal)unlock("plasma_wave41_max");\n'
  '      } else if(ptype==="ARCANE_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // PLASMA_WAVE41 — +2120 plasma wave bonus\n      if(ptype==="PLASMA_WAVE41"){sfx("powerUp",1783);unlock("plasma_wave41_use");}'
A4_NEW=(
  '  // SONIC_WAVE41 — +2124 sonic wave bonus\n'
  '      if(ptype==="SONIC_WAVE41"){sfx("powerUp",1787);unlock("sonic_wave41_use");}\n'
  '      // ECHO_PULSE41 — +2126 echo pulse bonus\n'
  '      if(ptype==="ECHO_PULSE41"){sfx("powerUp",1789);unlock("echo_pulse41_use");}\n'
  '  // PLASMA_WAVE41 — +2120 plasma wave bonus\n'
  '      if(ptype==="PLASMA_WAVE41"){sfx("powerUp",1783);unlock("plasma_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawMoorhouseiteFox9e('
A5_NEW=(
  'function drawMottramiteFox9e(ctx,r,ts,motPct){\n'
  '  const bob=Math.sin(ts*0.3658)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+motPct*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(motPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(22,163,74,"+(motPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=motPct>0.88?"#14532d":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(motPct>0.88?"🟢":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMuscoviteOrb9e(ctx,r,ts,musPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3662);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+musPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+musPct*0.35,"#cbd5e1");g.addColorStop(1,"#334155");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+musPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(203,213,225,"+(0.45+musPct*0.55)+")";ctx.lineWidth=3.5+musPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(musPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(241,245,249,"+(musPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=musPct>0.88?"#cbd5e1":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(musPct>0.88?"🪨":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMoorhouseiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="moorhouseite_fox9e"){\n      const moorPct=Math.min(1,(ts-t.born)/2800);t._moorPct=moorPct;\n      ctx.save();ctx.translate(t.x,t.y);drawMoorhouseiteFox9e(ctx,t.radius,ts,moorPct);ctx.restore();\n    } else if(t.type==="moissanite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="mottramite_fox9e"){\n'
  '      const motPct=Math.min(1,(ts-t.born)/2800);t._motPct=motPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMottramiteFox9e(ctx,t.radius,ts,motPct);ctx.restore();\n'
  '    } else if(t.type==="muscovite_orb9e"){\n'
  '      const musPct=Math.min(1,(ts-t.born)/2800);t._musPct=musPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMuscoviteOrb9e(ctx,t.radius,ts,musPct);ctx.restore();\n'
  '    } else if(t.type==="moorhouseite_fox9e"){\n'
  '      const moorPct=Math.min(1,(ts-t.born)/2800);t._moorPct=moorPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMoorhouseiteFox9e(ctx,t.radius,ts,moorPct);ctx.restore();\n'
  '    } else if(t.type==="moissanite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="moorhouseite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(312*(hit._moorPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#ec4899",1966);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌸",theme.accent,22);\n        unlock("moorhouseite_fox9e_tap");\n        if((hit._moorPct||0)>0.88)unlock("moorhouseite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="moissanite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="mottramite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(314*(hit._motPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#16a34a",1970);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟢",theme.accent,22);\n'
  '        unlock("mottramite_fox9e_tap");\n'
  '        if((hit._motPct||0)>0.88)unlock("mottramite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="muscovite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(309*(hit._musPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#cbd5e1",1972);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🪨",theme.accent,22);\n'
  '        unlock("muscovite_orb9e_tap");\n'
  '        if((hit._musPct||0)>0.88)unlock("muscovite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="moorhouseite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(312*(hit._moorPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ec4899",1966);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌸",theme.accent,22);\n'
  '        unlock("moorhouseite_fox9e_tap");\n'
  '        if((hit._moorPct||0)>0.88)unlock("moorhouseite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="moissanite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="moorhouseite_fox9e";color="#ec4899";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="moissanite_orb9e"')
A8_NEW=('      type="mottramite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="muscovite_orb9e";color="#cbd5e1";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="moorhouseite_fox9e";color="#ec4899";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="moissanite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="moorhouseite_fox9e"?BASE_R*1.22:type==="moissanite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="mottramite_fox9e"?BASE_R*1.22:type==="muscovite_orb9e"?BASE_R*1.21:type==="moorhouseite_fox9e"?BASE_R*1.22:type==="moissanite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='PLASMA_WAVE41:"💜💠",ARCANE_WAVE41:"🔮💠",LAVA_WAVE41:"🔴💠"'
A10_NEW='SONIC_WAVE41:"🔊💠",ECHO_PULSE41:"📡💠",PLASMA_WAVE41:"💜💠",ARCANE_WAVE41:"🔮💠",LAVA_WAVE41:"🔴💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("sonic_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"SONIC_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="SONIC_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1787)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawMottramiteFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="mottramite_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="mottramite_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="mottramite_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="mottramite_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('SONIC_WAVE41:"🔊💠"')>=2 else "Step 10 FAIL")
print(f"Batch 665 done! +{len(src)-len(orig)} bytes")
