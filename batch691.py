import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"sepiolite_orb9e_peak", label:"Sepiolite Orb Peak", desc:"Reach peak with Sepiolite Orb", icon:"🌾", xp:120 },'
A1_NEW=('{ id:"sepiolite_orb9e_peak", label:"Sepiolite Orb Peak", desc:"Reach peak with Sepiolite Orb", icon:"🌾", xp:120 },\n'
        '  { id:"orbit_ray42_use", label:"Orbit Ray 42", desc:"Activate ORBIT_RAY42 power-up", icon:"🌀", xp:60 },\n'
        '  { id:"orbit_ray42_max", label:"Orbit Rayer 42", desc:"Reach max with ORBIT_RAY42 active", icon:"🌀", xp:120 },\n'
        '  { id:"tide_ray42_use", label:"Tide Ray 42", desc:"Activate TIDE_RAY42 power-up", icon:"🌊", xp:60 },\n'
        '  { id:"tide_ray42_max", label:"Tide Rayer 42", desc:"Reach max with TIDE_RAY42 active", icon:"🌊", xp:120 },\n'
        '  { id:"siderite_fox9e_tap", label:"Siderite Fox", desc:"Tap a Siderite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"siderite_fox9e_peak", label:"Siderite Fox Peak", desc:"Reach peak with Siderite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"simpsonite_orb9e_tap", label:"Simpsonite Orb", desc:"Tap a Simpsonite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"simpsonite_orb9e_peak", label:"Simpsonite Orb Peak", desc:"Reach peak with Simpsonite Orb", icon:"🟡", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NEXUS_RAY42","PRISM_RAY42","COSMOS_RAY42"'
A2_NEW='"ORBIT_RAY42","TIDE_RAY42","NEXUS_RAY42","PRISM_RAY42","COSMOS_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NEXUS_RAY42"){'
A3_NEW=('  } else if(ptype==="ORBIT_RAY42"){\n'
        '        gs.score+=2228;showPopup(cx,cy-1938,"+2228 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a040e",2100);if(gs.score>=bonusTotal)unlock("orbit_ray42_max");\n'
        '      } else if(ptype==="TIDE_RAY42"){\n'
        '        gs.score+=2230;showPopup(cx,cy-1940,"+2230 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a08e2",2102);if(gs.score>=bonusTotal)unlock("tide_ray42_max");\n'
        '      } else if(ptype==="NEXUS_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NEXUS_RAY42 — +2224 nexus ray bonus'
A4_NEW=('  // ORBIT_RAY42 — +2228 orbit ray bonus\n'
        '      if(ptype==="ORBIT_RAY42"){sfx("powerUp",1891);unlock("orbit_ray42_use");}\n'
        '      // TIDE_RAY42 — +2230 tide ray bonus\n'
        '      if(ptype==="TIDE_RAY42"){sfx("powerUp",1893);unlock("tide_ray42_use");}\n'
        '  // NEXUS_RAY42 — +2224 nexus ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSenarmontiteFox9e('
A5_NEW=('function drawSideriteFox9e(ctx,r,ts,sidPct){\n'
        '  const bob=Math.sin(ts*0.3866)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fca5a5");g.addColorStop(0.45+sidPct*0.35,"#b91c1c");g.addColorStop(1,"#450a0a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(sidPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(252,165,165,"+(sidPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sidPct>0.88?"#fca5a5":"#fff5f5";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sidPct>0.88?"🌋":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSimpsoniteOrb9e(ctx,r,ts,simPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3870);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+simPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+simPct*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+simPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(234,179,8,"+(0.45+simPct*0.55)+")";ctx.lineWidth=3.5+simPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(simPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(234,179,8,"+(simPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=simPct>0.88?"#eab308":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(simPct>0.88?"🟡":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSenarmontiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="senarmontite_fox9e"){'
A6_NEW=('  else if(t.type==="siderite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2074);drawSideriteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="simpsonite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2076);drawSimpsoniteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="senarmontite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="senarmontite_fox9e"){'
A7_NEW=('    if(hit.type==="siderite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2074);\n'
        '      const pts=Math.round(366*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#b91c1c",2074);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌋","#fff5f5",22);\n'
        '      unlock("siderite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("siderite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="simpsonite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2076);\n'
        '      const pts=Math.round(361*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#eab308",2076);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟡","#fefce8",22);\n'
        '      unlock("simpsonite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("simpsonite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="senarmontite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="senarmontite_fox9e";color="#0284c7";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sepiolite_orb9e"')
A8_NEW=('      type="siderite_fox9e";color="#b91c1c";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="simpsonite_orb9e";color="#eab308";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="senarmontite_fox9e";color="#0284c7";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sepiolite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="senarmontite_fox9e"?BASE_R*1.35:type==="sepiolite_orb9e"?BASE_R*1.34:'
A9_NEW='type==="siderite_fox9e"?BASE_R*1.36:type==="simpsonite_orb9e"?BASE_R*1.35:type==="senarmontite_fox9e"?BASE_R*1.35:type==="sepiolite_orb9e"?BASE_R*1.34:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NEXUS_RAY42:"🔵🔆",PRISM_RAY42:"🔆🔆",COSMOS_RAY42:"🌌🔆"'
A10_NEW='ORBIT_RAY42:"🌀🔆",TIDE_RAY42:"🌊🔆",NEXUS_RAY42:"🔵🔆",PRISM_RAY42:"🔆🔆",COSMOS_RAY42:"🌌🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 691 done! +{len(src)-len(orig)} bytes")
