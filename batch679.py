import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"ralstonite_orb9e_peak", label:"Ralstonite Orb Peak", desc:"Reach peak with Ralstonite Orb", icon:"❄️", xp:120 },'
A1_NEW=('{ id:"ralstonite_orb9e_peak", label:"Ralstonite Orb Peak", desc:"Reach peak with Ralstonite Orb", icon:"❄️", xp:120 },\n'
        '  { id:"orbit_beam42_use", label:"Orbit Beam 42", desc:"Activate ORBIT_BEAM42 power-up", icon:"🌀", xp:60 },\n'
        '  { id:"orbit_beam42_max", label:"Orbit Beamer 42", desc:"Reach max with ORBIT_BEAM42 active", icon:"🌀", xp:120 },\n'
        '  { id:"tide_beam42_use", label:"Tide Beam 42", desc:"Activate TIDE_BEAM42 power-up", icon:"🌊", xp:60 },\n'
        '  { id:"tide_beam42_max", label:"Tide Beamer 42", desc:"Reach max with TIDE_BEAM42 active", icon:"🌊", xp:120 },\n'
        '  { id:"rathite_fox9e_tap", label:"Rathite Fox", desc:"Tap a Rathite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"rathite_fox9e_peak", label:"Rathite Fox Peak", desc:"Reach peak with Rathite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"rhodizite_orb9e_tap", label:"Rhodizite Orb", desc:"Tap a Rhodizite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"rhodizite_orb9e_peak", label:"Rhodizite Orb Peak", desc:"Reach peak with Rhodizite Orb", icon:"💜", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NEXUS_BEAM42","SOLAR_BEAM42","CRYSTAL_SURGE42"'
A2_NEW='"ORBIT_BEAM42","TIDE_BEAM42","NEXUS_BEAM42","SOLAR_BEAM42","CRYSTAL_SURGE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NEXUS_BEAM42"){'
A3_NEW=('  } else if(ptype==="ORBIT_BEAM42"){\n'
        '        gs.score+=2180;showPopup(cx,cy-1890,"+2180 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a03f6",2052);if(gs.score>=bonusTotal)unlock("orbit_beam42_max");\n'
        '      } else if(ptype==="TIDE_BEAM42"){\n'
        '        gs.score+=2182;showPopup(cx,cy-1892,"+2182 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a08ca",2054);if(gs.score>=bonusTotal)unlock("tide_beam42_max");\n'
        '      } else if(ptype==="NEXUS_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NEXUS_BEAM42 — +2176 nexus beam bonus'
A4_NEW=('  // ORBIT_BEAM42 — +2180 orbit beam bonus\n'
        '      if(ptype==="ORBIT_BEAM42"){sfx("powerUp",1843);unlock("orbit_beam42_use");}\n'
        '      // TIDE_BEAM42 — +2182 tide beam bonus\n'
        '      if(ptype==="TIDE_BEAM42"){sfx("powerUp",1845);unlock("tide_beam42_use");}\n'
        '  // NEXUS_BEAM42 — +2176 nexus beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRamsdelliteFox9e('
A5_NEW=('function drawRathiteFox9e(ctx,r,ts,rthPct){\n'
        '  const bob=Math.sin(ts*0.3770)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#94a3b8");g.addColorStop(0.45+rthPct*0.35,"#1e293b");g.addColorStop(1,"#0a0f1a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(rthPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(148,163,184,"+(rthPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rthPct>0.88?"#94a3b8":"#e2e8f0";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rthPct>0.88?"🌑":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRhhodiziteOrb9e(ctx,r,ts,rhdPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3774);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+rhdPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#faf5ff");g.addColorStop(0.35+rhdPct*0.35,"#ede9fe");g.addColorStop(1,"#6d28d9");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+rhdPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(237,233,254,"+(0.45+rhdPct*0.55)+")";ctx.lineWidth=3.5+rhdPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(rhdPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(237,233,254,"+(rhdPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rhdPct>0.88?"#ede9fe":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rhdPct>0.88?"💜":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRamsdelliteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="ramsdellite_fox9e"){'
A6_NEW=('  else if(t.type==="rathite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2026);drawRathiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="rhodizite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2028);drawRhhodiziteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="ramsdellite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="ramsdellite_fox9e"){'
A7_NEW=('    if(hit.type==="rathite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2026);\n'
        '      const pts=Math.round(342*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#1e293b",2026);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌑","#e2e8f0",22);\n'
        '      unlock("rathite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("rathite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="rhodizite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2028);\n'
        '      const pts=Math.round(337*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#ede9fe",2028);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💜","#faf5ff",22);\n'
        '      unlock("rhodizite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("rhodizite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="ramsdellite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="ramsdellite_fox9e";color="#334155";glow="#f1f5f9";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ralstonite_orb9e"')
A8_NEW=('      type="rathite_fox9e";color="#1e293b";glow="#e2e8f0";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rhodizite_orb9e";color="#ede9fe";glow="#faf5ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ramsdellite_fox9e";color="#334155";glow="#f1f5f9";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ralstonite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="ramsdellite_fox9e"?BASE_R*1.23:type==="ralstonite_orb9e"?BASE_R*1.22:'
A9_NEW='type==="rathite_fox9e"?BASE_R*1.24:type==="rhodizite_orb9e"?BASE_R*1.23:type==="ramsdellite_fox9e"?BASE_R*1.23:type==="ralstonite_orb9e"?BASE_R*1.22:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NEXUS_BEAM42:"🔵💡",SOLAR_BEAM42:"☀️💡",CRYSTAL_SURGE42:"💎💠"'
A10_NEW='ORBIT_BEAM42:"🌀💡",TIDE_BEAM42:"🌊💡",NEXUS_BEAM42:"🔵💡",SOLAR_BEAM42:"☀️💡",CRYSTAL_SURGE42:"💎💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 679 done! +{len(src)-len(orig)} bytes")
