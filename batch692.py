import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"simpsonite_orb9e_peak", label:"Simpsonite Orb Peak", desc:"Reach peak with Simpsonite Orb", icon:"🟡", xp:120 },'
A1_NEW=('{ id:"simpsonite_orb9e_peak", label:"Simpsonite Orb Peak", desc:"Reach peak with Simpsonite Orb", icon:"🟡", xp:120 },\n'
        '  { id:"nova_flare42_use", label:"Nova Flare 42", desc:"Activate NOVA_FLARE42 power-up", icon:"💥", xp:60 },\n'
        '  { id:"nova_flare42_max", label:"Nova Flarer 42", desc:"Reach max with NOVA_FLARE42 active", icon:"💥", xp:120 },\n'
        '  { id:"echo_flare42_use", label:"Echo Flare 42", desc:"Activate ECHO_FLARE42 power-up", icon:"📡", xp:60 },\n'
        '  { id:"echo_flare42_max", label:"Echo Flarer 42", desc:"Reach max with ECHO_FLARE42 active", icon:"📡", xp:120 },\n'
        '  { id:"sincosite_fox9e_tap", label:"Sincosite Fox", desc:"Tap a Sincosite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sincosite_fox9e_peak", label:"Sincosite Fox Peak", desc:"Reach peak with Sincosite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"sinhalite_orb9e_tap", label:"Sinhalite Orb", desc:"Tap a Sinhalite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"sinhalite_orb9e_peak", label:"Sinhalite Orb Peak", desc:"Reach peak with Sinhalite Orb", icon:"🟤", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"ORBIT_RAY42","TIDE_RAY42","NEXUS_RAY42"'
A2_NEW='"NOVA_FLARE42","ECHO_FLARE42","ORBIT_RAY42","TIDE_RAY42","NEXUS_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="ORBIT_RAY42"){'
A3_NEW=('  } else if(ptype==="NOVA_FLARE42"){\n'
        '        gs.score+=2232;showPopup(cx,cy-1942,"+2232 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a0410",2104);if(gs.score>=bonusTotal)unlock("nova_flare42_max");\n'
        '      } else if(ptype==="ECHO_FLARE42"){\n'
        '        gs.score+=2234;showPopup(cx,cy-1944,"+2234 📡",theme.accent,26);spawnShockwave(cx,cy,"#0a08e4",2106);if(gs.score>=bonusTotal)unlock("echo_flare42_max");\n'
        '      } else if(ptype==="ORBIT_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // ORBIT_RAY42 — +2228 orbit ray bonus'
A4_NEW=('  // NOVA_FLARE42 — +2232 nova flare bonus\n'
        '      if(ptype==="NOVA_FLARE42"){sfx("powerUp",1895);unlock("nova_flare42_use");}\n'
        '      // ECHO_FLARE42 — +2234 echo flare bonus\n'
        '      if(ptype==="ECHO_FLARE42"){sfx("powerUp",1897);unlock("echo_flare42_use");}\n'
        '  // ORBIT_RAY42 — +2228 orbit ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSideriteFox9e('
A5_NEW=('function drawSincositeFox9e(ctx,r,ts,scsPct){\n'
        '  const bob=Math.sin(ts*0.3874)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fed7aa");g.addColorStop(0.45+scsPct*0.35,"#ea580c");g.addColorStop(1,"#431407");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(scsPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(254,215,170,"+(scsPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=scsPct>0.88?"#fed7aa":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(scsPct>0.88?"🍊":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSinhaliteOrb9e(ctx,r,ts,snhPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3878);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+snhPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+snhPct*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+snhPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(180,83,9,"+(0.45+snhPct*0.55)+")";ctx.lineWidth=3.5+snhPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(snhPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(180,83,9,"+(snhPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=snhPct>0.88?"#b45309":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(snhPct>0.88?"🟤":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSideriteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="siderite_fox9e"){'
A6_NEW=('  else if(t.type==="sincosite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2078);drawSincositeFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="sinhalite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2080);drawSinhaliteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="siderite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="siderite_fox9e"){'
A7_NEW=('    if(hit.type==="sincosite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2078);\n'
        '      const pts=Math.round(368*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#ea580c",2078);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🍊","#fff7ed",22);\n'
        '      unlock("sincosite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sincosite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sinhalite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2080);\n'
        '      const pts=Math.round(363*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#b45309",2080);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fef3c7",22);\n'
        '      unlock("sinhalite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("sinhalite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="siderite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="siderite_fox9e";color="#b91c1c";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="simpsonite_orb9e"')
A8_NEW=('      type="sincosite_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sinhalite_orb9e";color="#b45309";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="siderite_fox9e";color="#b91c1c";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="simpsonite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="siderite_fox9e"?BASE_R*1.36:type==="simpsonite_orb9e"?BASE_R*1.35:'
A9_NEW='type==="sincosite_fox9e"?BASE_R*1.37:type==="sinhalite_orb9e"?BASE_R*1.36:type==="siderite_fox9e"?BASE_R*1.36:type==="simpsonite_orb9e"?BASE_R*1.35:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='ORBIT_RAY42:"🌀🔆",TIDE_RAY42:"🌊🔆",NEXUS_RAY42:"🔵🔆"'
A10_NEW='NOVA_FLARE42:"💥🌟",ECHO_FLARE42:"📡🌟",ORBIT_RAY42:"🌀🔆",TIDE_RAY42:"🌊🔆",NEXUS_RAY42:"🔵🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 692 done! +{len(src)-len(orig)} bytes")
