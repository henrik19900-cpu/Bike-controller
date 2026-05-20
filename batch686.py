import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"saneroite_orb9e_peak", label:"Saneroite Orb Peak", desc:"Reach peak with Saneroite Orb", icon:"🔵", xp:120 },'
A1_NEW=('{ id:"saneroite_orb9e_peak", label:"Saneroite Orb Peak", desc:"Reach peak with Saneroite Orb", icon:"🔵", xp:120 },\n'
        '  { id:"nova_ray42_use", label:"Nova Ray 42", desc:"Activate NOVA_RAY42 power-up", icon:"💥", xp:60 },\n'
        '  { id:"nova_ray42_max", label:"Nova Rayer 42", desc:"Reach max with NOVA_RAY42 active", icon:"💥", xp:120 },\n'
        '  { id:"void_ray42_use", label:"Void Ray 42", desc:"Activate VOID_RAY42 power-up", icon:"🕳️", xp:60 },\n'
        '  { id:"void_ray42_max", label:"Void Rayer 42", desc:"Reach max with VOID_RAY42 active", icon:"🕳️", xp:120 },\n'
        '  { id:"sarkinite_fox9e_tap", label:"Sarkinite Fox", desc:"Tap a Sarkinite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sarkinite_fox9e_peak", label:"Sarkinite Fox Peak", desc:"Reach peak with Sarkinite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"scacchite_orb9e_tap", label:"Scacchite Orb", desc:"Tap a Scacchite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"scacchite_orb9e_peak", label:"Scacchite Orb Peak", desc:"Reach peak with Scacchite Orb", icon:"🟤", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"COSMOS_BEAM42","SOLAR_RAY42","ECLIPSE_BEAM42"'
A2_NEW='"NOVA_RAY42","VOID_RAY42","COSMOS_BEAM42","SOLAR_RAY42","ECLIPSE_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="COSMOS_BEAM42"){'
A3_NEW=('  } else if(ptype==="NOVA_RAY42"){\n'
        '        gs.score+=2208;showPopup(cx,cy-1918,"+2208 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a0404",2080);if(gs.score>=bonusTotal)unlock("nova_ray42_max");\n'
        '      } else if(ptype==="VOID_RAY42"){\n'
        '        gs.score+=2210;showPopup(cx,cy-1920,"+2210 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a08d8",2082);if(gs.score>=bonusTotal)unlock("void_ray42_max");\n'
        '      } else if(ptype==="COSMOS_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // COSMOS_BEAM42 — +2204 cosmos beam bonus'
A4_NEW=('  // NOVA_RAY42 — +2208 nova ray bonus\n'
        '      if(ptype==="NOVA_RAY42"){sfx("powerUp",1871);unlock("nova_ray42_use");}\n'
        '      // VOID_RAY42 — +2210 void ray bonus\n'
        '      if(ptype==="VOID_RAY42"){sfx("powerUp",1873);unlock("void_ray42_use");}\n'
        '  // COSMOS_BEAM42 — +2204 cosmos beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSampleiteFox9e('
A5_NEW=('function drawSarkiniteFox9e(ctx,r,ts,srkPct){\n'
        '  const bob=Math.sin(ts*0.3826)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fb923c");g.addColorStop(0.45+srkPct*0.35,"#c2410c");g.addColorStop(1,"#431407");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(srkPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(251,146,60,"+(srkPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=srkPct>0.88?"#fb923c":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(srkPct>0.88?"🔥":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScacchiteOrb9e(ctx,r,ts,scaPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3830);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+scaPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+scaPct*0.35,"#d97706");g.addColorStop(1,"#78350f");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+scaPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+scaPct*0.55)+")";ctx.lineWidth=3.5+scaPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(scaPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(217,119,6,"+(scaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=scaPct>0.88?"#d97706":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(scaPct>0.88?"🟤":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSampleiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sampleite_fox9e"){'
A6_NEW=('  else if(t.type==="sarkinite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2054);drawSarkiniteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="scacchite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2056);drawScacchiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sampleite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sampleite_fox9e"){'
A7_NEW=('    if(hit.type==="sarkinite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2054);\n'
        '      const pts=Math.round(356*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#c2410c",2054);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔥","#fff7ed",22);\n'
        '      unlock("sarkinite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sarkinite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scacchite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2056);\n'
        '      const pts=Math.round(351*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#d97706",2056);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fefce8",22);\n'
        '      unlock("scacchite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("scacchite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sampleite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sampleite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="saneroite_orb9e"')
A8_NEW=('      type="sarkinite_fox9e";color="#c2410c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scacchite_orb9e";color="#d97706";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sampleite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="saneroite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sampleite_fox9e"?BASE_R*1.30:type==="saneroite_orb9e"?BASE_R*1.29:'
A9_NEW='type==="sarkinite_fox9e"?BASE_R*1.31:type==="scacchite_orb9e"?BASE_R*1.30:type==="sampleite_fox9e"?BASE_R*1.30:type==="saneroite_orb9e"?BASE_R*1.29:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='COSMOS_BEAM42:"🌌💡",SOLAR_RAY42:"☀️🔆",ECLIPSE_BEAM42:"🌑💡"'
A10_NEW='NOVA_RAY42:"💥🔆",VOID_RAY42:"🕳️🔆",COSMOS_BEAM42:"🌌💡",SOLAR_RAY42:"☀️🔆",ECLIPSE_BEAM42:"🌑💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 686 done! +{len(src)-len(orig)} bytes")
