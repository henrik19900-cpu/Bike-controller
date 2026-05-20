import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"smithite_orb9e_peak", label:"Smithite Orb Peak", desc:"Reach peak with Smithite Orb", icon:"🟤", xp:120 },'
A1_NEW=('{ id:"smithite_orb9e_peak", label:"Smithite Orb Peak", desc:"Reach peak with Smithite Orb", icon:"🟤", xp:120 },\n'
        '  { id:"thunder_flare42_use", label:"Thunder Flare 42", desc:"Activate THUNDER_FLARE42 power-up", icon:"⚡", xp:60 },\n'
        '  { id:"thunder_flare42_max", label:"Thunder Flarer 42", desc:"Reach max with THUNDER_FLARE42 active", icon:"⚡", xp:120 },\n'
        '  { id:"aurora_flare42_use", label:"Aurora Flare 42", desc:"Activate AURORA_FLARE42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"aurora_flare42_max", label:"Aurora Flarer 42", desc:"Reach max with AURORA_FLARE42 active", icon:"🌌", xp:120 },\n'
        '  { id:"sperrylite_fox9e_tap", label:"Sperrylite Fox", desc:"Tap a Sperrylite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sperrylite_fox9e_peak", label:"Sperrylite Fox Peak", desc:"Reach peak with Sperrylite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"spertiniite_orb9e_tap", label:"Spertiniite Orb", desc:"Tap a Spertiniite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"spertiniite_orb9e_peak", label:"Spertiniite Orb Peak", desc:"Reach peak with Spertiniite Orb", icon:"🔵", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"VOID_FLARE42","PRISM_FLARE42","STAR_FLARE42"'
A2_NEW='"THUNDER_FLARE42","AURORA_FLARE42","VOID_FLARE42","PRISM_FLARE42","STAR_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="VOID_FLARE42"){'
A3_NEW=('  } else if(ptype==="THUNDER_FLARE42"){\n'
        '        gs.score+=2244;showPopup(cx,cy-1954,"+2244 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a0416",2116);if(gs.score>=bonusTotal)unlock("thunder_flare42_max");\n'
        '      } else if(ptype==="AURORA_FLARE42"){\n'
        '        gs.score+=2246;showPopup(cx,cy-1956,"+2246 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a08ea",2118);if(gs.score>=bonusTotal)unlock("aurora_flare42_max");\n'
        '      } else if(ptype==="VOID_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // VOID_FLARE42 — +2240 void flare bonus'
A4_NEW=('  // THUNDER_FLARE42 — +2244 thunder flare bonus\n'
        '      if(ptype==="THUNDER_FLARE42"){sfx("powerUp",1907);unlock("thunder_flare42_use");}\n'
        '      // AURORA_FLARE42 — +2246 aurora flare bonus\n'
        '      if(ptype==="AURORA_FLARE42"){sfx("powerUp",1909);unlock("aurora_flare42_use");}\n'
        '  // VOID_FLARE42 — +2240 void flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSklodowskiteFox9e('
A5_NEW=('function drawSperryliteFox9e(ctx,r,ts,sprPct){\n'
        '  const bob=Math.sin(ts*0.3898)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#e2e8f0");g.addColorStop(0.45+sprPct*0.35,"#475569");g.addColorStop(1,"#0f172a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(sprPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(226,232,240,"+(sprPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sprPct>0.88?"#e2e8f0":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sprPct>0.88?"💿":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSpertiniiteOrb9e(ctx,r,ts,sptPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3902);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sptPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#dbeafe");g.addColorStop(0.35+sptPct*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sptPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(37,99,235,"+(0.45+sptPct*0.55)+")";ctx.lineWidth=3.5+sptPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sptPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(37,99,235,"+(sptPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sptPct>0.88?"#2563eb":"#dbeafe";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sptPct>0.88?"🔵":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSklodowskiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sklodowskite_fox9e"){'
A6_NEW=('  else if(t.type==="sperrylite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2090);drawSperryliteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="spertiniite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2092);drawSpertiniiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sklodowskite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sklodowskite_fox9e"){'
A7_NEW=('    if(hit.type==="sperrylite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2090);\n'
        '      const pts=Math.round(374*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#475569",2090);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💿","#f8fafc",22);\n'
        '      unlock("sperrylite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sperrylite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="spertiniite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2092);\n'
        '      const pts=Math.round(369*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#2563eb",2092);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔵","#dbeafe",22);\n'
        '      unlock("spertiniite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("spertiniite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sklodowskite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sklodowskite_fox9e";color="#a21caf";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="smithite_orb9e"')
A8_NEW=('      type="sperrylite_fox9e";color="#475569";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="spertiniite_orb9e";color="#2563eb";glow="#dbeafe";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sklodowskite_fox9e";color="#a21caf";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="smithite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sklodowskite_fox9e"?BASE_R*1.39:type==="smithite_orb9e"?BASE_R*1.38:'
A9_NEW='type==="sperrylite_fox9e"?BASE_R*1.40:type==="spertiniite_orb9e"?BASE_R*1.39:type==="sklodowskite_fox9e"?BASE_R*1.39:type==="smithite_orb9e"?BASE_R*1.38:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='VOID_FLARE42:"🕳️🌟",PRISM_FLARE42:"🔆🌟",STAR_FLARE42:"⭐🌟"'
A10_NEW='THUNDER_FLARE42:"⚡🌟",AURORA_FLARE42:"🌌🌟",VOID_FLARE42:"🕳️🌟",PRISM_FLARE42:"🔆🌟",STAR_FLARE42:"⭐🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 695 done! +{len(src)-len(orig)} bytes")
