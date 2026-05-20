import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"semseyite_orb9e_peak", label:"Semseyite Orb Peak", desc:"Reach peak with Semseyite Orb", icon:"🖤", xp:120 },'
A1_NEW=('{ id:"semseyite_orb9e_peak", label:"Semseyite Orb Peak", desc:"Reach peak with Semseyite Orb", icon:"🖤", xp:120 },\n'
        '  { id:"nexus_ray42_use", label:"Nexus Ray 42", desc:"Activate NEXUS_RAY42 power-up", icon:"🔵", xp:60 },\n'
        '  { id:"nexus_ray42_max", label:"Nexus Rayer 42", desc:"Reach max with NEXUS_RAY42 active", icon:"🔵", xp:120 },\n'
        '  { id:"prism_ray42_use", label:"Prism Ray 42", desc:"Activate PRISM_RAY42 power-up", icon:"🔆", xp:60 },\n'
        '  { id:"prism_ray42_max", label:"Prism Rayer 42", desc:"Reach max with PRISM_RAY42 active", icon:"🔆", xp:120 },\n'
        '  { id:"senarmontite_fox9e_tap", label:"Senarmontite Fox", desc:"Tap a Senarmontite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"senarmontite_fox9e_peak", label:"Senarmontite Fox Peak", desc:"Reach peak with Senarmontite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"sepiolite_orb9e_tap", label:"Sepiolite Orb", desc:"Tap a Sepiolite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"sepiolite_orb9e_peak", label:"Sepiolite Orb Peak", desc:"Reach peak with Sepiolite Orb", icon:"🌾", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"COSMOS_RAY42","STELLAR_RAY42","ECLIPSE_RAY42"'
A2_NEW='"NEXUS_RAY42","PRISM_RAY42","COSMOS_RAY42","STELLAR_RAY42","ECLIPSE_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="COSMOS_RAY42"){'
A3_NEW=('  } else if(ptype==="NEXUS_RAY42"){\n'
        '        gs.score+=2224;showPopup(cx,cy-1934,"+2224 🔵",theme.accent,26);spawnShockwave(cx,cy,"#0a040c",2096);if(gs.score>=bonusTotal)unlock("nexus_ray42_max");\n'
        '      } else if(ptype==="PRISM_RAY42"){\n'
        '        gs.score+=2226;showPopup(cx,cy-1936,"+2226 🔆",theme.accent,26);spawnShockwave(cx,cy,"#0a08e0",2098);if(gs.score>=bonusTotal)unlock("prism_ray42_max");\n'
        '      } else if(ptype==="COSMOS_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // COSMOS_RAY42 — +2220 cosmos ray bonus'
A4_NEW=('  // NEXUS_RAY42 — +2224 nexus ray bonus\n'
        '      if(ptype==="NEXUS_RAY42"){sfx("powerUp",1887);unlock("nexus_ray42_use");}\n'
        '      // PRISM_RAY42 — +2226 prism ray bonus\n'
        '      if(ptype==="PRISM_RAY42"){sfx("powerUp",1889);unlock("prism_ray42_use");}\n'
        '  // COSMOS_RAY42 — +2220 cosmos ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawScorzaliteFox9e('
A5_NEW=('function drawSenarmontiteFox9e(ctx,r,ts,senPct){\n'
        '  const bob=Math.sin(ts*0.3858)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.45+senPct*0.35,"#0284c7");g.addColorStop(1,"#0c4a6e");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(senPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(224,242,254,"+(senPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=senPct>0.88?"#e0f2fe":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(senPct>0.88?"❄️":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSepioliteOrb9e(ctx,r,ts,sepPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3862);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sepPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+sepPct*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sepPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(202,138,4,"+(0.45+sepPct*0.55)+")";ctx.lineWidth=3.5+sepPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sepPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(202,138,4,"+(sepPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sepPct>0.88?"#ca8a04":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sepPct>0.88?"🌾":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScorzaliteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="scorzalite_fox9e"){'
A6_NEW=('  else if(t.type==="senarmontite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2070);drawSenarmontiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="sepiolite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2072);drawSepioliteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="scorzalite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="scorzalite_fox9e"){'
A7_NEW=('    if(hit.type==="senarmontite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2070);\n'
        '      const pts=Math.round(364*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#0284c7",2070);\n'
        '      showPopup(cx,cy-38,"+"+pts+" ❄️","#f0f9ff",22);\n'
        '      unlock("senarmontite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("senarmontite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sepiolite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2072);\n'
        '      const pts=Math.round(359*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#ca8a04",2072);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌾","#fef9c3",22);\n'
        '      unlock("sepiolite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("sepiolite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scorzalite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="scorzalite_fox9e";color="#065f46";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="semseyite_orb9e"')
A8_NEW=('      type="senarmontite_fox9e";color="#0284c7";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sepiolite_orb9e";color="#ca8a04";glow="#fef9c3";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scorzalite_fox9e";color="#065f46";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="semseyite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="scorzalite_fox9e"?BASE_R*1.34:type==="semseyite_orb9e"?BASE_R*1.33:'
A9_NEW='type==="senarmontite_fox9e"?BASE_R*1.35:type==="sepiolite_orb9e"?BASE_R*1.34:type==="scorzalite_fox9e"?BASE_R*1.34:type==="semseyite_orb9e"?BASE_R*1.33:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='COSMOS_RAY42:"🌌🔆",STELLAR_RAY42:"🌟🔆",ECLIPSE_RAY42:"🌑🔆"'
A10_NEW='NEXUS_RAY42:"🔵🔆",PRISM_RAY42:"🔆🔆",COSMOS_RAY42:"🌌🔆",STELLAR_RAY42:"🌟🔆",ECLIPSE_RAY42:"🌑🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 690 done! +{len(src)-len(orig)} bytes")
