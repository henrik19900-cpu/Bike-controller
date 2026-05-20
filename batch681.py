import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"rodalquilarite_orb9e_peak", label:"Rodalquilarite Orb Peak", desc:"Reach peak with Rodalquilarite Orb", icon:"🟢", xp:120 },'
A1_NEW=('{ id:"rodalquilarite_orb9e_peak", label:"Rodalquilarite Orb Peak", desc:"Reach peak with Rodalquilarite Orb", icon:"🟢", xp:120 },\n'
        '  { id:"star_beam42_use", label:"Star Beam 42", desc:"Activate STAR_BEAM42 power-up", icon:"⭐", xp:60 },\n'
        '  { id:"star_beam42_max", label:"Star Beamer 42", desc:"Reach max with STAR_BEAM42 active", icon:"⭐", xp:120 },\n'
        '  { id:"moon_beam42_use", label:"Moon Beam 42", desc:"Activate MOON_BEAM42 power-up", icon:"🌙", xp:60 },\n'
        '  { id:"moon_beam42_max", label:"Moon Beamer 42", desc:"Reach max with MOON_BEAM42 active", icon:"🌙", xp:120 },\n'
        '  { id:"roscherite_fox9e_tap", label:"Roscherite Fox", desc:"Tap a Roscherite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"roscherite_fox9e_peak", label:"Roscherite Fox Peak", desc:"Reach peak with Roscherite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"rosenbuschite_orb9e_tap", label:"Rosenbuschite Orb", desc:"Tap a Rosenbuschite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"rosenbuschite_orb9e_peak", label:"Rosenbuschite Orb Peak", desc:"Reach peak with Rosenbuschite Orb", icon:"🟠", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NOVA_BEAM42","ECHO_BEAM42","ORBIT_BEAM42"'
A2_NEW='"STAR_BEAM42","MOON_BEAM42","NOVA_BEAM42","ECHO_BEAM42","ORBIT_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NOVA_BEAM42"){'
A3_NEW=('  } else if(ptype==="STAR_BEAM42"){\n'
        '        gs.score+=2188;showPopup(cx,cy-1898,"+2188 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#0a03fa",2060);if(gs.score>=bonusTotal)unlock("star_beam42_max");\n'
        '      } else if(ptype==="MOON_BEAM42"){\n'
        '        gs.score+=2190;showPopup(cx,cy-1900,"+2190 🌙",theme.accent,26);spawnShockwave(cx,cy,"#0a08ce",2062);if(gs.score>=bonusTotal)unlock("moon_beam42_max");\n'
        '      } else if(ptype==="NOVA_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NOVA_BEAM42 — +2184 nova beam bonus'
A4_NEW=('  // STAR_BEAM42 — +2188 star beam bonus\n'
        '      if(ptype==="STAR_BEAM42"){sfx("powerUp",1851);unlock("star_beam42_use");}\n'
        '      // MOON_BEAM42 — +2190 moon beam bonus\n'
        '      if(ptype==="MOON_BEAM42"){sfx("powerUp",1853);unlock("moon_beam42_use");}\n'
        '  // NOVA_BEAM42 — +2184 nova beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRichelsdorfiteFox9e('
A5_NEW=('function drawRoscheriteFox9e(ctx,r,ts,rscPct){\n'
        '  const bob=Math.sin(ts*0.3786)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fde68a");g.addColorStop(0.45+rscPct*0.35,"#92400e");g.addColorStop(1,"#451a03");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(rscPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(253,230,138,"+(rscPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rscPct>0.88?"#fde68a":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rscPct>0.88?"🟤":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRosenbuschiteOrb9e(ctx,r,ts,rsnPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3790);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+rsnPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+rsnPct*0.35,"#fdba74");g.addColorStop(1,"#c2410c");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+rsnPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(253,186,116,"+(0.45+rsnPct*0.55)+")";ctx.lineWidth=3.5+rsnPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(rsnPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(253,186,116,"+(rsnPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rsnPct>0.88?"#fdba74":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rsnPct>0.88?"🟠":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRichelsdorfiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="richelsdorfite_fox9e"){'
A6_NEW=('  else if(t.type==="roscherite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2034);drawRoscheriteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="rosenbuschite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2036);drawRosenbuschiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="richelsdorfite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="richelsdorfite_fox9e"){'
A7_NEW=('    if(hit.type==="roscherite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2034);\n'
        '      const pts=Math.round(346*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#92400e",2034);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fffbeb",22);\n'
        '      unlock("roscherite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("roscherite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="rosenbuschite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2036);\n'
        '      const pts=Math.round(341*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#fdba74",2036);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟠","#fff7ed",22);\n'
        '      unlock("rosenbuschite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("rosenbuschite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="richelsdorfite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="richelsdorfite_fox9e";color="#0e7490";glow="#ecfeff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rodalquilarite_orb9e"')
A8_NEW=('      type="roscherite_fox9e";color="#92400e";glow="#fffbeb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rosenbuschite_orb9e";color="#fdba74";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="richelsdorfite_fox9e";color="#0e7490";glow="#ecfeff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rodalquilarite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="richelsdorfite_fox9e"?BASE_R*1.25:type==="rodalquilarite_orb9e"?BASE_R*1.24:'
A9_NEW='type==="roscherite_fox9e"?BASE_R*1.26:type==="rosenbuschite_orb9e"?BASE_R*1.25:type==="richelsdorfite_fox9e"?BASE_R*1.25:type==="rodalquilarite_orb9e"?BASE_R*1.24:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NOVA_BEAM42:"💥💡",ECHO_BEAM42:"📡💡",ORBIT_BEAM42:"🌀💡"'
A10_NEW='STAR_BEAM42:"⭐💡",MOON_BEAM42:"🌙💡",NOVA_BEAM42:"💥💡",ECHO_BEAM42:"📡💡",ORBIT_BEAM42:"🌀💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 681 done! +{len(src)-len(orig)} bytes")
