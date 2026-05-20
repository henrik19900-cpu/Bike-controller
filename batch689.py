import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"scorodite_orb9e_peak", label:"Scorodite Orb Peak", desc:"Reach peak with Scorodite Orb", icon:"🟣", xp:120 },'
A1_NEW=('{ id:"scorodite_orb9e_peak", label:"Scorodite Orb Peak", desc:"Reach peak with Scorodite Orb", icon:"🟣", xp:120 },\n'
        '  { id:"cosmos_ray42_use", label:"Cosmos Ray 42", desc:"Activate COSMOS_RAY42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"cosmos_ray42_max", label:"Cosmos Rayer 42", desc:"Reach max with COSMOS_RAY42 active", icon:"🌌", xp:120 },\n'
        '  { id:"stellar_ray42_use", label:"Stellar Ray 42", desc:"Activate STELLAR_RAY42 power-up", icon:"🌟", xp:60 },\n'
        '  { id:"stellar_ray42_max", label:"Stellar Rayer 42", desc:"Reach max with STELLAR_RAY42 active", icon:"🌟", xp:120 },\n'
        '  { id:"scorzalite_fox9e_tap", label:"Scorzalite Fox", desc:"Tap a Scorzalite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"scorzalite_fox9e_peak", label:"Scorzalite Fox Peak", desc:"Reach peak with Scorzalite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"semseyite_orb9e_tap", label:"Semseyite Orb", desc:"Tap a Semseyite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"semseyite_orb9e_peak", label:"Semseyite Orb Peak", desc:"Reach peak with Semseyite Orb", icon:"🖤", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"ECLIPSE_RAY42","LUNAR_RAY42","THUNDER_RAY42"'
A2_NEW='"COSMOS_RAY42","STELLAR_RAY42","ECLIPSE_RAY42","LUNAR_RAY42","THUNDER_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="ECLIPSE_RAY42"){'
A3_NEW=('  } else if(ptype==="COSMOS_RAY42"){\n'
        '        gs.score+=2220;showPopup(cx,cy-1930,"+2220 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a040a",2092);if(gs.score>=bonusTotal)unlock("cosmos_ray42_max");\n'
        '      } else if(ptype==="STELLAR_RAY42"){\n'
        '        gs.score+=2222;showPopup(cx,cy-1932,"+2222 🌟",theme.accent,26);spawnShockwave(cx,cy,"#0a08de",2094);if(gs.score>=bonusTotal)unlock("stellar_ray42_max");\n'
        '      } else if(ptype==="ECLIPSE_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // ECLIPSE_RAY42 — +2216 eclipse ray bonus'
A4_NEW=('  // COSMOS_RAY42 — +2220 cosmos ray bonus\n'
        '      if(ptype==="COSMOS_RAY42"){sfx("powerUp",1883);unlock("cosmos_ray42_use");}\n'
        '      // STELLAR_RAY42 — +2222 stellar ray bonus\n'
        '      if(ptype==="STELLAR_RAY42"){sfx("powerUp",1885);unlock("stellar_ray42_use");}\n'
        '  // ECLIPSE_RAY42 — +2216 eclipse ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawScoleciteFox9e('
A5_NEW=('function drawScorzaliteFox9e(ctx,r,ts,sczPct){\n'
        '  const bob=Math.sin(ts*0.3850)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#6ee7b7");g.addColorStop(0.45+sczPct*0.35,"#065f46");g.addColorStop(1,"#022c22");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(sczPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(110,231,183,"+(sczPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sczPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sczPct>0.88?"🌿":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSemseyiteOrb9e(ctx,r,ts,semPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3854);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+semPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#374151");g.addColorStop(0.35+semPct*0.35,"#111827");g.addColorStop(1,"#030712");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+semPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(55,65,81,"+(0.45+semPct*0.55)+")";ctx.lineWidth=3.5+semPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(semPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(107,114,128,"+(semPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=semPct>0.88?"#6b7280":"#d1d5db";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(semPct>0.88?"🖤":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScoleciteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="scolecite_fox9e"){'
A6_NEW=('  else if(t.type==="scorzalite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2066);drawScorzaliteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="semseyite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2068);drawSemseyiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="scolecite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="scolecite_fox9e"){'
A7_NEW=('    if(hit.type==="scorzalite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2066);\n'
        '      const pts=Math.round(362*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#065f46",2066);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌿","#ecfdf5",22);\n'
        '      unlock("scorzalite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("scorzalite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="semseyite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2068);\n'
        '      const pts=Math.round(357*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#374151",2068);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🖤","#d1d5db",22);\n'
        '      unlock("semseyite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("semseyite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scolecite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="scolecite_fox9e";color="#86198f";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scorodite_orb9e"')
A8_NEW=('      type="scorzalite_fox9e";color="#065f46";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="semseyite_orb9e";color="#374151";glow="#d1d5db";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scolecite_fox9e";color="#86198f";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scorodite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="scolecite_fox9e"?BASE_R*1.33:type==="scorodite_orb9e"?BASE_R*1.32:'
A9_NEW='type==="scorzalite_fox9e"?BASE_R*1.34:type==="semseyite_orb9e"?BASE_R*1.33:type==="scolecite_fox9e"?BASE_R*1.33:type==="scorodite_orb9e"?BASE_R*1.32:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='ECLIPSE_RAY42:"🌑🔆",LUNAR_RAY42:"🌕🔆",THUNDER_RAY42:"⚡🔆"'
A10_NEW='COSMOS_RAY42:"🌌🔆",STELLAR_RAY42:"🌟🔆",ECLIPSE_RAY42:"🌑🔆",LUNAR_RAY42:"🌕🔆",THUNDER_RAY42:"⚡🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 689 done! +{len(src)-len(orig)} bytes")
