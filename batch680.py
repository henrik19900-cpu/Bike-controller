import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"rhodizite_orb9e_peak", label:"Rhodizite Orb Peak", desc:"Reach peak with Rhodizite Orb", icon:"💜", xp:120 },'
A1_NEW=('{ id:"rhodizite_orb9e_peak", label:"Rhodizite Orb Peak", desc:"Reach peak with Rhodizite Orb", icon:"💜", xp:120 },\n'
        '  { id:"nova_beam42_use", label:"Nova Beam 42", desc:"Activate NOVA_BEAM42 power-up", icon:"💥", xp:60 },\n'
        '  { id:"nova_beam42_max", label:"Nova Beamer 42", desc:"Reach max with NOVA_BEAM42 active", icon:"💥", xp:120 },\n'
        '  { id:"echo_beam42_use", label:"Echo Beam 42", desc:"Activate ECHO_BEAM42 power-up", icon:"📡", xp:60 },\n'
        '  { id:"echo_beam42_max", label:"Echo Beamer 42", desc:"Reach max with ECHO_BEAM42 active", icon:"📡", xp:120 },\n'
        '  { id:"richelsdorfite_fox9e_tap", label:"Richelsdorfite Fox", desc:"Tap a Richelsdorfite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"richelsdorfite_fox9e_peak", label:"Richelsdorfite Fox Peak", desc:"Reach peak with Richelsdorfite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"rodalquilarite_orb9e_tap", label:"Rodalquilarite Orb", desc:"Tap a Rodalquilarite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"rodalquilarite_orb9e_peak", label:"Rodalquilarite Orb Peak", desc:"Reach peak with Rodalquilarite Orb", icon:"🟢", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"ORBIT_BEAM42","TIDE_BEAM42","NEXUS_BEAM42"'
A2_NEW='"NOVA_BEAM42","ECHO_BEAM42","ORBIT_BEAM42","TIDE_BEAM42","NEXUS_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="ORBIT_BEAM42"){'
A3_NEW=('  } else if(ptype==="NOVA_BEAM42"){\n'
        '        gs.score+=2184;showPopup(cx,cy-1894,"+2184 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a03f8",2056);if(gs.score>=bonusTotal)unlock("nova_beam42_max");\n'
        '      } else if(ptype==="ECHO_BEAM42"){\n'
        '        gs.score+=2186;showPopup(cx,cy-1896,"+2186 📡",theme.accent,26);spawnShockwave(cx,cy,"#0a08cc",2058);if(gs.score>=bonusTotal)unlock("echo_beam42_max");\n'
        '      } else if(ptype==="ORBIT_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // ORBIT_BEAM42 — +2180 orbit beam bonus'
A4_NEW=('  // NOVA_BEAM42 — +2184 nova beam bonus\n'
        '      if(ptype==="NOVA_BEAM42"){sfx("powerUp",1847);unlock("nova_beam42_use");}\n'
        '      // ECHO_BEAM42 — +2186 echo beam bonus\n'
        '      if(ptype==="ECHO_BEAM42"){sfx("powerUp",1849);unlock("echo_beam42_use");}\n'
        '  // ORBIT_BEAM42 — +2180 orbit beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRathiteFox9e('
A5_NEW=('function drawRichelsdorfiteFox9e(ctx,r,ts,rchPct){\n'
        '  const bob=Math.sin(ts*0.3778)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#67e8f9");g.addColorStop(0.45+rchPct*0.35,"#0e7490");g.addColorStop(1,"#083344");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(rchPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(103,232,249,"+(rchPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rchPct>0.88?"#67e8f9":"#ecfeff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rchPct>0.88?"💎":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRodalquilariteOrb9e(ctx,r,ts,rodPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3782);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+rodPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+rodPct*0.35,"#86efac");g.addColorStop(1,"#15803d");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+rodPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(134,239,172,"+(0.45+rodPct*0.55)+")";ctx.lineWidth=3.5+rodPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(rodPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(134,239,172,"+(rodPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rodPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rodPct>0.88?"🟢":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRathiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="rathite_fox9e"){'
A6_NEW=('  else if(t.type==="richelsdorfite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2030);drawRichelsdorfiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="rodalquilarite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2032);drawRodalquilariteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="rathite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="rathite_fox9e"){'
A7_NEW=('    if(hit.type==="richelsdorfite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2030);\n'
        '      const pts=Math.round(344*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#0e7490",2030);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💎","#ecfeff",22);\n'
        '      unlock("richelsdorfite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("richelsdorfite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="rodalquilarite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2032);\n'
        '      const pts=Math.round(339*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#86efac",2032);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟢","#f0fdf4",22);\n'
        '      unlock("rodalquilarite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("rodalquilarite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="rathite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="rathite_fox9e";color="#1e293b";glow="#e2e8f0";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rhodizite_orb9e"')
A8_NEW=('      type="richelsdorfite_fox9e";color="#0e7490";glow="#ecfeff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rodalquilarite_orb9e";color="#86efac";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rathite_fox9e";color="#1e293b";glow="#e2e8f0";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rhodizite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="rathite_fox9e"?BASE_R*1.24:type==="rhodizite_orb9e"?BASE_R*1.23:'
A9_NEW='type==="richelsdorfite_fox9e"?BASE_R*1.25:type==="rodalquilarite_orb9e"?BASE_R*1.24:type==="rathite_fox9e"?BASE_R*1.24:type==="rhodizite_orb9e"?BASE_R*1.23:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='ORBIT_BEAM42:"🌀💡",TIDE_BEAM42:"🌊💡",NEXUS_BEAM42:"🔵💡"'
A10_NEW='NOVA_BEAM42:"💥💡",ECHO_BEAM42:"📡💡",ORBIT_BEAM42:"🌀💡",TIDE_BEAM42:"🌊💡",NEXUS_BEAM42:"🔵💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 680 done! +{len(src)-len(orig)} bytes")
