import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"sahamalite_orb9e_peak", label:"Sahamalite Orb Peak", desc:"Reach peak with Sahamalite Orb", icon:"🌿", xp:120 },'
A1_NEW=('{ id:"sahamalite_orb9e_peak", label:"Sahamalite Orb Peak", desc:"Reach peak with Sahamalite Orb", icon:"🌿", xp:120 },\n'
        '  { id:"cosmos_beam42_use", label:"Cosmos Beam 42", desc:"Activate COSMOS_BEAM42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"cosmos_beam42_max", label:"Cosmos Beamer 42", desc:"Reach max with COSMOS_BEAM42 active", icon:"🌌", xp:120 },\n'
        '  { id:"solar_ray42_use", label:"Solar Ray 42", desc:"Activate SOLAR_RAY42 power-up", icon:"☀️", xp:60 },\n'
        '  { id:"solar_ray42_max", label:"Solar Rayer 42", desc:"Reach max with SOLAR_RAY42 active", icon:"☀️", xp:120 },\n'
        '  { id:"sampleite_fox9e_tap", label:"Sampleite Fox", desc:"Tap a Sampleite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sampleite_fox9e_peak", label:"Sampleite Fox Peak", desc:"Reach peak with Sampleite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"saneroite_orb9e_tap", label:"Saneroite Orb", desc:"Tap a Saneroite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"saneroite_orb9e_peak", label:"Saneroite Orb Peak", desc:"Reach peak with Saneroite Orb", icon:"🔵", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"ECLIPSE_BEAM42","LUNAR_BEAM42","THUNDER_BEAM42"'
A2_NEW='"COSMOS_BEAM42","SOLAR_RAY42","ECLIPSE_BEAM42","LUNAR_BEAM42","THUNDER_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="ECLIPSE_BEAM42"){'
A3_NEW=('  } else if(ptype==="COSMOS_BEAM42"){\n'
        '        gs.score+=2204;showPopup(cx,cy-1914,"+2204 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a0402",2076);if(gs.score>=bonusTotal)unlock("cosmos_beam42_max");\n'
        '      } else if(ptype==="SOLAR_RAY42"){\n'
        '        gs.score+=2206;showPopup(cx,cy-1916,"+2206 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a08d6",2078);if(gs.score>=bonusTotal)unlock("solar_ray42_max");\n'
        '      } else if(ptype==="ECLIPSE_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // ECLIPSE_BEAM42 — +2200 eclipse beam bonus'
A4_NEW=('  // COSMOS_BEAM42 — +2204 cosmos beam bonus\n'
        '      if(ptype==="COSMOS_BEAM42"){sfx("powerUp",1867);unlock("cosmos_beam42_use");}\n'
        '      // SOLAR_RAY42 — +2206 solar ray bonus\n'
        '      if(ptype==="SOLAR_RAY42"){sfx("powerUp",1869);unlock("solar_ray42_use");}\n'
        '  // ECLIPSE_BEAM42 — +2200 eclipse beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRusseliteFox9e('
A5_NEW=('function drawSampleiteFox9e(ctx,r,ts,samPct){\n'
        '  const bob=Math.sin(ts*0.3818)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#7dd3fc");g.addColorStop(0.45+samPct*0.35,"#0369a1");g.addColorStop(1,"#082f49");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(samPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(125,211,252,"+(samPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=samPct>0.88?"#7dd3fc":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(samPct>0.88?"💎":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSaneroiteOrb9e(ctx,r,ts,sanPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3822);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sanPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#eff6ff");g.addColorStop(0.35+sanPct*0.35,"#93c5fd");g.addColorStop(1,"#1d4ed8");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sanPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(147,197,253,"+(0.45+sanPct*0.55)+")";ctx.lineWidth=3.5+sanPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sanPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(147,197,253,"+(sanPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sanPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sanPct>0.88?"🔵":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRusseliteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="russelite_fox9e"){'
A6_NEW=('  else if(t.type==="sampleite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2050);drawSampleiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="saneroite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2052);drawSaneroiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="russelite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="russelite_fox9e"){'
A7_NEW=('    if(hit.type==="sampleite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2050);\n'
        '      const pts=Math.round(354*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#0369a1",2050);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💎","#f0f9ff",22);\n'
        '      unlock("sampleite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sampleite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="saneroite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2052);\n'
        '      const pts=Math.round(349*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#93c5fd",2052);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔵","#eff6ff",22);\n'
        '      unlock("saneroite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("saneroite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="russelite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="russelite_fox9e";color="#5b21b6";glow="#f5f3ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sahamalite_orb9e"')
A8_NEW=('      type="sampleite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="saneroite_orb9e";color="#93c5fd";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="russelite_fox9e";color="#5b21b6";glow="#f5f3ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sahamalite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="russelite_fox9e"?BASE_R*1.29:type==="sahamalite_orb9e"?BASE_R*1.28:'
A9_NEW='type==="sampleite_fox9e"?BASE_R*1.30:type==="saneroite_orb9e"?BASE_R*1.29:type==="russelite_fox9e"?BASE_R*1.29:type==="sahamalite_orb9e"?BASE_R*1.28:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='ECLIPSE_BEAM42:"🌑💡",LUNAR_BEAM42:"🌕💡",THUNDER_BEAM42:"⚡💡"'
A10_NEW='COSMOS_BEAM42:"🌌💡",SOLAR_RAY42:"☀️🔆",ECLIPSE_BEAM42:"🌑💡",LUNAR_BEAM42:"🌕💡",THUNDER_BEAM42:"⚡💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 685 done! +{len(src)-len(orig)} bytes")
