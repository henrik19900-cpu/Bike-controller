import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"pyrochroite_orb9e_peak", label:"Pyrochroite Orb Peak", desc:"Reach peak with Pyrochroite Orb", icon:"🌸", xp:120 },'
A1_NEW=('{ id:"pyrochroite_orb9e_peak", label:"Pyrochroite Orb Peak", desc:"Reach peak with Pyrochroite Orb", icon:"🌸", xp:120 },\n'
        '  { id:"nexus_beam42_use", label:"Nexus Beam 42", desc:"Activate NEXUS_BEAM42 power-up", icon:"🔵", xp:60 },\n'
        '  { id:"nexus_beam42_max", label:"Nexus Beamer 42", desc:"Reach max with NEXUS_BEAM42 active", icon:"🔵", xp:120 },\n'
        '  { id:"solar_beam42_use", label:"Solar Beam 42", desc:"Activate SOLAR_BEAM42 power-up", icon:"☀️", xp:60 },\n'
        '  { id:"solar_beam42_max", label:"Solar Beamer 42", desc:"Reach max with SOLAR_BEAM42 active", icon:"☀️", xp:120 },\n'
        '  { id:"ramsdellite_fox9e_tap", label:"Ramsdellite Fox", desc:"Tap a Ramsdellite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"ramsdellite_fox9e_peak", label:"Ramsdellite Fox Peak", desc:"Reach peak with Ramsdellite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"ralstonite_orb9e_tap", label:"Ralstonite Orb", desc:"Tap a Ralstonite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"ralstonite_orb9e_peak", label:"Ralstonite Orb Peak", desc:"Reach peak with Ralstonite Orb", icon:"❄️", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"CRYSTAL_SURGE42","STAR_SURGE42","VOID_SURGE42"'
A2_NEW='"NEXUS_BEAM42","SOLAR_BEAM42","CRYSTAL_SURGE42","STAR_SURGE42","VOID_SURGE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="CRYSTAL_SURGE42"){'
A3_NEW=('  } else if(ptype==="NEXUS_BEAM42"){\n'
        '        gs.score+=2176;showPopup(cx,cy-1886,"+2176 🔵",theme.accent,26);spawnShockwave(cx,cy,"#0a03f4",2048);if(gs.score>=bonusTotal)unlock("nexus_beam42_max");\n'
        '      } else if(ptype==="SOLAR_BEAM42"){\n'
        '        gs.score+=2178;showPopup(cx,cy-1888,"+2178 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a08c8",2050);if(gs.score>=bonusTotal)unlock("solar_beam42_max");\n'
        '      } else if(ptype==="CRYSTAL_SURGE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // CRYSTAL_SURGE42 — +2172 crystal surge bonus'
A4_NEW=('  // NEXUS_BEAM42 — +2176 nexus beam bonus\n'
        '      if(ptype==="NEXUS_BEAM42"){sfx("powerUp",1839);unlock("nexus_beam42_use");}\n'
        '      // SOLAR_BEAM42 — +2178 solar beam bonus\n'
        '      if(ptype==="SOLAR_BEAM42"){sfx("powerUp",1841);unlock("solar_beam42_use");}\n'
        '  // CRYSTAL_SURGE42 — +2172 crystal surge bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawPurpuriteFox9e('
A5_NEW=('function drawRamsdelliteFox9e(ctx,r,ts,ramPct){\n'
        '  const bob=Math.sin(ts*0.3762)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#94a3b8");g.addColorStop(0.45+ramPct*0.35,"#334155");g.addColorStop(1,"#0f172a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(ramPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(148,163,184,"+(ramPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=ramPct>0.88?"#94a3b8":"#f1f5f9";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ramPct>0.88?"🐺":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRalstoniteOrb9e(ctx,r,ts,ralPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3766);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ralPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.35+ralPct*0.35,"#bae6fd");g.addColorStop(1,"#0369a1");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+ralPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(186,230,253,"+(0.45+ralPct*0.55)+")";ctx.lineWidth=3.5+ralPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(ralPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(186,230,253,"+(ralPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=ralPct>0.88?"#bae6fd":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ralPct>0.88?"❄️":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawPurpuriteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="purpurite_fox9e"){'
A6_NEW=('  else if(t.type==="ramsdellite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2022);drawRamsdelliteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="ralstonite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2024);drawRalstoniteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="purpurite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="purpurite_fox9e"){'
A7_NEW=('    if(hit.type==="ramsdellite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2022);\n'
        '      const pts=Math.round(340*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#334155",2022);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🐺",\"#f1f5f9\",22);\n'
        '      unlock("ramsdellite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("ramsdellite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="ralstonite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2024);\n'
        '      const pts=Math.round(335*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#bae6fd",2024);\n'
        '      showPopup(cx,cy-38,"+"+pts+" ❄️",\"#f0f9ff\",22);\n'
        '      unlock("ralstonite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("ralstonite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="purpurite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="purpurite_fox9e";color="#7e22ce";glow="#faf5ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pyrochroite_orb9e"')
A8_NEW=('      type="ramsdellite_fox9e";color="#334155";glow="#f1f5f9";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ralstonite_orb9e";color="#bae6fd";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="purpurite_fox9e";color="#7e22ce";glow="#faf5ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="pyrochroite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="purpurite_fox9e"?BASE_R*1.22:type==="pyrochroite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="ramsdellite_fox9e"?BASE_R*1.23:type==="ralstonite_orb9e"?BASE_R*1.22:type==="purpurite_fox9e"?BASE_R*1.22:type==="pyrochroite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='CRYSTAL_SURGE42:"💎💠",STAR_SURGE42:"⭐💠",'
A10_NEW='NEXUS_BEAM42:"🔵💡",SOLAR_BEAM42:"☀️💡",CRYSTAL_SURGE42:"💎💠",STAR_SURGE42:"⭐💠",'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 678 done! +{len(src)-len(orig)} bytes")
