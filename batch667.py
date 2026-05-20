import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"norbergite_orb9e_peak", label:"Norbergite Orb Peak", desc:"Reach peak with Norbergite Orb", icon:"🔶", xp:120 },'
A1_NEW=(
  '{ id:"norbergite_orb9e_peak", label:"Norbergite Orb Peak", desc:"Reach peak with Norbergite Orb", icon:"🔶", xp:120 },\n'
  '  { id:"radiant_wave41_use", label:"Radiant Wave", desc:"Activate RADIANT_WAVE41 power-up", icon:"✨", xp:60 },\n'
  '  { id:"radiant_wave41_max", label:"Radiant Waver", desc:"Reach max with RADIANT_WAVE41 active", icon:"✨", xp:120 },\n'
  '  { id:"pulse_surge41_use", label:"Pulse Surge", desc:"Activate PULSE_SURGE41 power-up", icon:"💫", xp:60 },\n'
  '  { id:"pulse_surge41_max", label:"Pulse Surger", desc:"Reach max with PULSE_SURGE41 active", icon:"💫", xp:120 },\n'
  '  { id:"oligoclase_fox9e_tap", label:"Oligoclase Fox", desc:"Tap Oligoclase Fox target", icon:"⚪", xp:60 },\n'
  '  { id:"oligoclase_fox9e_peak", label:"Oligoclase Peak", desc:"Reach peak with Oligoclase Fox", icon:"⚪", xp:120 },\n'
  '  { id:"olivenite_orb9e_tap", label:"Olivenite Orb", desc:"Tap Olivenite Orb target", icon:"🫒", xp:60 },\n'
  '  { id:"olivenite_orb9e_peak", label:"Olivenite Orb Peak", desc:"Reach peak with Olivenite Orb", icon:"🫒", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"VORTEX_WAVE41","FLUX_PULSE41","SONIC_WAVE41"'
A2_NEW='"RADIANT_WAVE41","PULSE_SURGE41","VORTEX_WAVE41","FLUX_PULSE41","SONIC_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="VORTEX_WAVE41"){\n        gs.score+=2128;showPopup(cx,cy-1838,"+2128 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a03dc",2000);if(gs.score>=bonusTotal)unlock("vortex_wave41_max");\n      } else if(ptype==="FLUX_PULSE41"){'
A3_NEW=(
  '  } else if(ptype==="RADIANT_WAVE41"){\n'
  '        gs.score+=2132;showPopup(cx,cy-1842,"+2132 ✨",theme.accent,26);spawnShockwave(cx,cy,"#0a03de",2004);if(gs.score>=bonusTotal)unlock("radiant_wave41_max");\n'
  '      } else if(ptype==="PULSE_SURGE41"){\n'
  '        gs.score+=2134;showPopup(cx,cy-1844,"+2134 💫",theme.accent,26);spawnShockwave(cx,cy,"#0a08b2",2006);if(gs.score>=bonusTotal)unlock("pulse_surge41_max");\n'
  '      } else if(ptype==="VORTEX_WAVE41"){\n'
  '        gs.score+=2128;showPopup(cx,cy-1838,"+2128 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a03dc",2000);if(gs.score>=bonusTotal)unlock("vortex_wave41_max");\n'
  '      } else if(ptype==="FLUX_PULSE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // VORTEX_WAVE41 — +2128 vortex wave bonus\n      if(ptype==="VORTEX_WAVE41"){sfx("powerUp",1791);unlock("vortex_wave41_use");}'
A4_NEW=(
  '  // RADIANT_WAVE41 — +2132 radiant wave bonus\n'
  '      if(ptype==="RADIANT_WAVE41"){sfx("powerUp",1795);unlock("radiant_wave41_use");}\n'
  '      // PULSE_SURGE41 — +2134 pulse surge bonus\n'
  '      if(ptype==="PULSE_SURGE41"){sfx("powerUp",1797);unlock("pulse_surge41_use");}\n'
  '  // VORTEX_WAVE41 — +2128 vortex wave bonus\n'
  '      if(ptype==="VORTEX_WAVE41"){sfx("powerUp",1791);unlock("vortex_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawNickelineFox9e('
A5_NEW=(
  'function drawOligoclaseFox9e(ctx,r,ts,oliPct){\n'
  '  const bob=Math.sin(ts*0.3674)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+oliPct*0.35,"#94a3b8");g.addColorStop(1,"#1e293b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(oliPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(148,163,184,"+(oliPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=oliPct>0.88?"#1e293b":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(oliPct>0.88?"⚪":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawOliveniteOrb9e(ctx,r,ts,olivPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3678);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+olivPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#f7fee7");g.addColorStop(0.35+olivPct*0.35,"#65a30d");g.addColorStop(1,"#1a2e05");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+olivPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(101,163,13,"+(0.45+olivPct*0.55)+")";ctx.lineWidth=3.5+olivPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(olivPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(190,242,100,"+(olivPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=olivPct>0.88?"#65a30d":"#f7fee7";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(olivPct>0.88?"🫒":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawNickelineFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="nickeline_fox9e"){\n      const nickPct=Math.min(1,(ts-t.born)/2800);t._nickPct=nickPct;\n      ctx.save();ctx.translate(t.x,t.y);drawNickelineFox9e(ctx,t.radius,ts,nickPct);ctx.restore();\n    } else if(t.type==="norbergite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="oligoclase_fox9e"){\n'
  '      const oliPct=Math.min(1,(ts-t.born)/2800);t._oliPct=oliPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOligoclaseFox9e(ctx,t.radius,ts,oliPct);ctx.restore();\n'
  '    } else if(t.type==="olivenite_orb9e"){\n'
  '      const olivPct=Math.min(1,(ts-t.born)/2800);t._olivPct=olivPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawOliveniteOrb9e(ctx,t.radius,ts,olivPct);ctx.restore();\n'
  '    } else if(t.type==="nickeline_fox9e"){\n'
  '      const nickPct=Math.min(1,(ts-t.born)/2800);t._nickPct=nickPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawNickelineFox9e(ctx,t.radius,ts,nickPct);ctx.restore();\n'
  '    } else if(t.type==="norbergite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="nickeline_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(316*(hit._nickPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#ea580c",1974);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟠",theme.accent,22);\n        unlock("nickeline_fox9e_tap");\n        if((hit._nickPct||0)>0.88)unlock("nickeline_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="norbergite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="oligoclase_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(318*(hit._oliPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#94a3b8",1978);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" ⚪",theme.accent,22);\n'
  '        unlock("oligoclase_fox9e_tap");\n'
  '        if((hit._oliPct||0)>0.88)unlock("oligoclase_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="olivenite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(313*(hit._olivPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#65a30d",1980);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🫒",theme.accent,22);\n'
  '        unlock("olivenite_orb9e_tap");\n'
  '        if((hit._olivPct||0)>0.88)unlock("olivenite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="nickeline_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(316*(hit._nickPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#ea580c",1974);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🟠",theme.accent,22);\n'
  '        unlock("nickeline_fox9e_tap");\n'
  '        if((hit._nickPct||0)>0.88)unlock("nickeline_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="norbergite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="nickeline_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="norbergite_orb9e"')
A8_NEW=('      type="oligoclase_fox9e";color="#94a3b8";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="olivenite_orb9e";color="#65a30d";glow="#f7fee7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="nickeline_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="norbergite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="nickeline_fox9e"?BASE_R*1.22:type==="norbergite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="oligoclase_fox9e"?BASE_R*1.22:type==="olivenite_orb9e"?BASE_R*1.21:type==="nickeline_fox9e"?BASE_R*1.22:type==="norbergite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='VORTEX_WAVE41:"🌀💠",FLUX_PULSE41:"⚡💠",SONIC_WAVE41:"🔊💠"'
A10_NEW='RADIANT_WAVE41:"✨💠",PULSE_SURGE41:"💫💠",VORTEX_WAVE41:"🌀💠",FLUX_PULSE41:"⚡💠",SONIC_WAVE41:"🔊💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("radiant_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"RADIANT_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="RADIANT_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1795)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawOligoclaseFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="oligoclase_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="oligoclase_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="oligoclase_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="oligoclase_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('RADIANT_WAVE41:"✨💠"')>=2 else "Step 10 FAIL")
print(f"Batch 667 done! +{len(src)-len(orig)} bytes")
