import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"muscovite_orb9e_peak", label:"Muscovite Orb Peak", desc:"Reach peak with Muscovite Orb", icon:"🪨", xp:120 },'
A1_NEW=(
  '{ id:"muscovite_orb9e_peak", label:"Muscovite Orb Peak", desc:"Reach peak with Muscovite Orb", icon:"🪨", xp:120 },\n'
  '  { id:"vortex_wave41_use", label:"Vortex Wave", desc:"Activate VORTEX_WAVE41 power-up", icon:"🌀", xp:60 },\n'
  '  { id:"vortex_wave41_max", label:"Vortex Waver", desc:"Reach max with VORTEX_WAVE41 active", icon:"🌀", xp:120 },\n'
  '  { id:"flux_pulse41_use", label:"Flux Pulse", desc:"Activate FLUX_PULSE41 power-up", icon:"⚡", xp:60 },\n'
  '  { id:"flux_pulse41_max", label:"Flux Pulser", desc:"Reach max with FLUX_PULSE41 active", icon:"⚡", xp:120 },\n'
  '  { id:"nickeline_fox9e_tap", label:"Nickeline Fox", desc:"Tap Nickeline Fox target", icon:"🟠", xp:60 },\n'
  '  { id:"nickeline_fox9e_peak", label:"Nickeline Peak", desc:"Reach peak with Nickeline Fox", icon:"🟠", xp:120 },\n'
  '  { id:"norbergite_orb9e_tap", label:"Norbergite Orb", desc:"Tap Norbergite Orb target", icon:"🔶", xp:60 },\n'
  '  { id:"norbergite_orb9e_peak", label:"Norbergite Orb Peak", desc:"Reach peak with Norbergite Orb", icon:"🔶", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"SONIC_WAVE41","ECHO_PULSE41","PLASMA_WAVE41"'
A2_NEW='"VORTEX_WAVE41","FLUX_PULSE41","SONIC_WAVE41","ECHO_PULSE41","PLASMA_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="SONIC_WAVE41"){\n        gs.score+=2124;showPopup(cx,cy-1834,"+2124 🔊",theme.accent,26);spawnShockwave(cx,cy,"#0a03da",1996);if(gs.score>=bonusTotal)unlock("sonic_wave41_max");\n      } else if(ptype==="ECHO_PULSE41"){'
A3_NEW=(
  '  } else if(ptype==="VORTEX_WAVE41"){\n'
  '        gs.score+=2128;showPopup(cx,cy-1838,"+2128 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a03dc",2000);if(gs.score>=bonusTotal)unlock("vortex_wave41_max");\n'
  '      } else if(ptype==="FLUX_PULSE41"){\n'
  '        gs.score+=2130;showPopup(cx,cy-1840,"+2130 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a08b0",2002);if(gs.score>=bonusTotal)unlock("flux_pulse41_max");\n'
  '      } else if(ptype==="SONIC_WAVE41"){\n'
  '        gs.score+=2124;showPopup(cx,cy-1834,"+2124 🔊",theme.accent,26);spawnShockwave(cx,cy,"#0a03da",1996);if(gs.score>=bonusTotal)unlock("sonic_wave41_max");\n'
  '      } else if(ptype==="ECHO_PULSE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // SONIC_WAVE41 — +2124 sonic wave bonus\n      if(ptype==="SONIC_WAVE41"){sfx("powerUp",1787);unlock("sonic_wave41_use");}'
A4_NEW=(
  '  // VORTEX_WAVE41 — +2128 vortex wave bonus\n'
  '      if(ptype==="VORTEX_WAVE41"){sfx("powerUp",1791);unlock("vortex_wave41_use");}\n'
  '      // FLUX_PULSE41 — +2130 flux pulse bonus\n'
  '      if(ptype==="FLUX_PULSE41"){sfx("powerUp",1793);unlock("flux_pulse41_use");}\n'
  '  // SONIC_WAVE41 — +2124 sonic wave bonus\n'
  '      if(ptype==="SONIC_WAVE41"){sfx("powerUp",1787);unlock("sonic_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawMottramiteFox9e('
A5_NEW=(
  'function drawNickelineFox9e(ctx,r,ts,nickPct){\n'
  '  const bob=Math.sin(ts*0.3666)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.45+nickPct*0.35,"#ea580c");g.addColorStop(1,"#7c2d12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(nickPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(234,88,12,"+(nickPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=nickPct>0.88?"#7c2d12":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(nickPct>0.88?"🟠":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawNorbergiteOrb9e(ctx,r,ts,norPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3670);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+norPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+norPct*0.35,"#f97316");g.addColorStop(1,"#7c2d12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+norPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(249,115,22,"+(0.45+norPct*0.55)+")";ctx.lineWidth=3.5+norPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(norPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(253,186,116,"+(norPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=norPct>0.88?"#f97316":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(norPct>0.88?"🔶":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMottramiteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="mottramite_fox9e"){\n      const motPct=Math.min(1,(ts-t.born)/2800);t._motPct=motPct;\n      ctx.save();ctx.translate(t.x,t.y);drawMottramiteFox9e(ctx,t.radius,ts,motPct);ctx.restore();\n    } else if(t.type==="muscovite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="nickeline_fox9e"){\n'
  '      const nickPct=Math.min(1,(ts-t.born)/2800);t._nickPct=nickPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawNickelineFox9e(ctx,t.radius,ts,nickPct);ctx.restore();\n'
  '    } else if(t.type==="norbergite_orb9e"){\n'
  '      const norPct=Math.min(1,(ts-t.born)/2800);t._norPct=norPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawNorbergiteOrb9e(ctx,t.radius,ts,norPct);ctx.restore();\n'
  '    } else if(t.type==="mottramite_fox9e"){\n'
  '      const motPct=Math.min(1,(ts-t.born)/2800);t._motPct=motPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMottramiteFox9e(ctx,t.radius,ts,motPct);ctx.restore();\n'
  '    } else if(t.type==="muscovite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="mottramite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(314*(hit._motPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#16a34a",1970);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟢",theme.accent,22);\n        unlock("mottramite_fox9e_tap");\n        if((hit._motPct||0)>0.88)unlock("mottramite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="muscovite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="nickeline_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(316*(hit._nickPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ea580c",1974);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟠",theme.accent,22);\n'
  '        unlock("nickeline_fox9e_tap");\n'
  '        if((hit._nickPct||0)>0.88)unlock("nickeline_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="norbergite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(311*(hit._norPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#f97316",1976);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔶",theme.accent,22);\n'
  '        unlock("norbergite_orb9e_tap");\n'
  '        if((hit._norPct||0)>0.88)unlock("norbergite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="mottramite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(314*(hit._motPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#16a34a",1970);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟢",theme.accent,22);\n'
  '        unlock("mottramite_fox9e_tap");\n'
  '        if((hit._motPct||0)>0.88)unlock("mottramite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="muscovite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="mottramite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="muscovite_orb9e"')
A8_NEW=('      type="nickeline_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="norbergite_orb9e";color="#f97316";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mottramite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="muscovite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="mottramite_fox9e"?BASE_R*1.22:type==="muscovite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="nickeline_fox9e"?BASE_R*1.22:type==="norbergite_orb9e"?BASE_R*1.21:type==="mottramite_fox9e"?BASE_R*1.22:type==="muscovite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='SONIC_WAVE41:"🔊💠",ECHO_PULSE41:"📡💠",PLASMA_WAVE41:"💜💠"'
A10_NEW='VORTEX_WAVE41:"🌀💠",FLUX_PULSE41:"⚡💠",SONIC_WAVE41:"🔊💠",ECHO_PULSE41:"📡💠",PLASMA_WAVE41:"💜💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("vortex_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"VORTEX_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="VORTEX_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1791)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawNickelineFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="nickeline_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="nickeline_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="nickeline_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="nickeline_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('VORTEX_WAVE41:"🌀💠"')>=2 else "Step 10 FAIL")
print(f"Batch 666 done! +{len(src)-len(orig)} bytes")
