import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"sinhalite_orb9e_peak", label:"Sinhalite Orb Peak", desc:"Reach peak with Sinhalite Orb", icon:"🟤", xp:120 },'
A1_NEW=('{ id:"sinhalite_orb9e_peak", label:"Sinhalite Orb Peak", desc:"Reach peak with Sinhalite Orb", icon:"🟤", xp:120 },\n'
        '  { id:"star_flare42_use", label:"Star Flare 42", desc:"Activate STAR_FLARE42 power-up", icon:"⭐", xp:60 },\n'
        '  { id:"star_flare42_max", label:"Star Flarer 42", desc:"Reach max with STAR_FLARE42 active", icon:"⭐", xp:120 },\n'
        '  { id:"moon_flare42_use", label:"Moon Flare 42", desc:"Activate MOON_FLARE42 power-up", icon:"🌙", xp:60 },\n'
        '  { id:"moon_flare42_max", label:"Moon Flarer 42", desc:"Reach max with MOON_FLARE42 active", icon:"🌙", xp:120 },\n'
        '  { id:"sinkankasite_fox9e_tap", label:"Sinkankasite Fox", desc:"Tap a Sinkankasite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sinkankasite_fox9e_peak", label:"Sinkankasite Fox Peak", desc:"Reach peak with Sinkankasite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"skinnerite_orb9e_tap", label:"Skinnerite Orb", desc:"Tap a Skinnerite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"skinnerite_orb9e_peak", label:"Skinnerite Orb Peak", desc:"Reach peak with Skinnerite Orb", icon:"🟡", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NOVA_FLARE42","ECHO_FLARE42","ORBIT_RAY42"'
A2_NEW='"STAR_FLARE42","MOON_FLARE42","NOVA_FLARE42","ECHO_FLARE42","ORBIT_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NOVA_FLARE42"){'
A3_NEW=('  } else if(ptype==="STAR_FLARE42"){\n'
        '        gs.score+=2236;showPopup(cx,cy-1946,"+2236 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#0a0412",2108);if(gs.score>=bonusTotal)unlock("star_flare42_max");\n'
        '      } else if(ptype==="MOON_FLARE42"){\n'
        '        gs.score+=2238;showPopup(cx,cy-1948,"+2238 🌙",theme.accent,26);spawnShockwave(cx,cy,"#0a08e6",2110);if(gs.score>=bonusTotal)unlock("moon_flare42_max");\n'
        '      } else if(ptype==="NOVA_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NOVA_FLARE42 — +2232 nova flare bonus'
A4_NEW=('  // STAR_FLARE42 — +2236 star flare bonus\n'
        '      if(ptype==="STAR_FLARE42"){sfx("powerUp",1899);unlock("star_flare42_use");}\n'
        '      // MOON_FLARE42 — +2238 moon flare bonus\n'
        '      if(ptype==="MOON_FLARE42"){sfx("powerUp",1901);unlock("moon_flare42_use");}\n'
        '  // NOVA_FLARE42 — +2232 nova flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSincositeFox9e('
A5_NEW=('function drawSinkankasiteFox9e(ctx,r,ts,snkPct){\n'
        '  const bob=Math.sin(ts*0.3882)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#d9f99d");g.addColorStop(0.45+snkPct*0.35,"#4d7c0f");g.addColorStop(1,"#1a2e05");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(snkPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(217,249,157,"+(snkPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=snkPct>0.88?"#d9f99d":"#f7fee7";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(snkPct>0.88?"🌱":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSkinneriteOrb9e(ctx,r,ts,sknPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3886);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sknPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+sknPct*0.35,"#a16207");g.addColorStop(1,"#422006");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sknPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(161,98,7,"+(0.45+sknPct*0.55)+")";ctx.lineWidth=3.5+sknPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sknPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(161,98,7,"+(sknPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sknPct>0.88?"#a16207":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sknPct>0.88?"🟡":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSincositeFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sincosite_fox9e"){'
A6_NEW=('  else if(t.type==="sinkankasite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2082);drawSinkankasiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="skinnerite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2084);drawSkinneriteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sincosite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sincosite_fox9e"){'
A7_NEW=('    if(hit.type==="sinkankasite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2082);\n'
        '      const pts=Math.round(370*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#4d7c0f",2082);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌱","#f7fee7",22);\n'
        '      unlock("sinkankasite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sinkankasite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="skinnerite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2084);\n'
        '      const pts=Math.round(365*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#a16207",2084);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟡","#fef9c3",22);\n'
        '      unlock("skinnerite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("skinnerite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sincosite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sincosite_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sinhalite_orb9e"')
A8_NEW=('      type="sinkankasite_fox9e";color="#4d7c0f";glow="#f7fee7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="skinnerite_orb9e";color="#a16207";glow="#fef9c3";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sincosite_fox9e";color="#ea580c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sinhalite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sincosite_fox9e"?BASE_R*1.37:type==="sinhalite_orb9e"?BASE_R*1.36:'
A9_NEW='type==="sinkankasite_fox9e"?BASE_R*1.38:type==="skinnerite_orb9e"?BASE_R*1.37:type==="sincosite_fox9e"?BASE_R*1.37:type==="sinhalite_orb9e"?BASE_R*1.36:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NOVA_FLARE42:"💥🌟",ECHO_FLARE42:"📡🌟",ORBIT_RAY42:"🌀🔆"'
A10_NEW='STAR_FLARE42:"⭐🌟",MOON_FLARE42:"🌙🌟",NOVA_FLARE42:"💥🌟",ECHO_FLARE42:"📡🌟",ORBIT_RAY42:"🌀🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 693 done! +{len(src)-len(orig)} bytes")
