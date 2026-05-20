import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"stannite_orb9e_peak", label:"Stannite Orb Peak", desc:"Reach peak with Stannite Orb", icon:"⚫", xp:120 },'
A1_NEW=('{ id:"stannite_orb9e_peak", label:"Stannite Orb Peak", desc:"Reach peak with Stannite Orb", icon:"⚫", xp:120 },\n'
        '  { id:"cosmos_flare42_use", label:"Cosmos Flare 42", desc:"Activate COSMOS_FLARE42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"cosmos_flare42_max", label:"Cosmos Flarer 42", desc:"Reach max with COSMOS_FLARE42 active", icon:"🌌", xp:120 },\n'
        '  { id:"stellar_flare42_use", label:"Stellar Flare 42", desc:"Activate STELLAR_FLARE42 power-up", icon:"🌟", xp:60 },\n'
        '  { id:"stellar_flare42_max", label:"Stellar Flarer 42", desc:"Reach max with STELLAR_FLARE42 active", icon:"🌟", xp:120 },\n'
        '  { id:"stephanite_fox9e_tap", label:"Stephanite Fox", desc:"Tap a Stephanite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"stephanite_fox9e_peak", label:"Stephanite Fox Peak", desc:"Reach peak with Stephanite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"strengite_orb9e_tap", label:"Strengite Orb", desc:"Tap a Strengite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"strengite_orb9e_peak", label:"Strengite Orb Peak", desc:"Reach peak with Strengite Orb", icon:"🌺", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"ECLIPSE_FLARE42","LUNAR_FLARE42","THUNDER_FLARE42"'
A2_NEW='"COSMOS_FLARE42","STELLAR_FLARE42","ECLIPSE_FLARE42","LUNAR_FLARE42","THUNDER_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="ECLIPSE_FLARE42"){'
A3_NEW=('  } else if(ptype==="COSMOS_FLARE42"){\n'
        '        gs.score+=2252;showPopup(cx,cy-1962,"+2252 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a041a",2124);if(gs.score>=bonusTotal)unlock("cosmos_flare42_max");\n'
        '      } else if(ptype==="STELLAR_FLARE42"){\n'
        '        gs.score+=2254;showPopup(cx,cy-1964,"+2254 🌟",theme.accent,26);spawnShockwave(cx,cy,"#0a08ee",2126);if(gs.score>=bonusTotal)unlock("stellar_flare42_max");\n'
        '      } else if(ptype==="ECLIPSE_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // ECLIPSE_FLARE42 — +2248 eclipse flare bonus'
A4_NEW=('  // COSMOS_FLARE42 — +2252 cosmos flare bonus\n'
        '      if(ptype==="COSMOS_FLARE42"){sfx("powerUp",1915);unlock("cosmos_flare42_use");}\n'
        '      // STELLAR_FLARE42 — +2254 stellar flare bonus\n'
        '      if(ptype==="STELLAR_FLARE42"){sfx("powerUp",1917);unlock("stellar_flare42_use");}\n'
        '  // ECLIPSE_FLARE42 — +2248 eclipse flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSpriggiteFox9e('
A5_NEW=('function drawStephaniteFox9e(ctx,r,ts,stpPct){\n'
        '  const bob=Math.sin(ts*0.3914)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#c8b3f5");g.addColorStop(0.45+stpPct*0.35,"#6200ea");g.addColorStop(1,"#2b0080");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(stpPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(200,179,245,"+(stpPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=stpPct>0.88?"#c8b3f5":"#ede7f6";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(stpPct>0.88?"🪄":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawStrengiteOrb9e(ctx,r,ts,strPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3918);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+strPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fce4ec");g.addColorStop(0.35+strPct*0.35,"#e91e63");g.addColorStop(1,"#880e4f");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+strPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(233,30,99,"+(0.45+strPct*0.55)+")";ctx.lineWidth=3.5+strPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(strPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(233,30,99,"+(strPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=strPct>0.88?"#e91e63":"#fce4ec";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(strPct>0.88?"🌺":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSpriggiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="spriggite_fox9e"){'
A6_NEW=('  else if(t.type==="stephanite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2098);drawStephaniteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="strengite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2100);drawStrengiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="spriggite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="spriggite_fox9e"){'
A7_NEW=('    if(hit.type==="stephanite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2098);\n'
        '      const pts=Math.round(378*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#6200ea",2098);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🪄","#ede7f6",22);\n'
        '      unlock("stephanite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("stephanite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="strengite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2100);\n'
        '      const pts=Math.round(373*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#e91e63",2100);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌺","#fce4ec",22);\n'
        '      unlock("strengite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("strengite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="spriggite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="spriggite_fox9e";color="#be185d";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="stannite_orb9e"')
A8_NEW=('      type="stephanite_fox9e";color="#6200ea";glow="#ede7f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="strengite_orb9e";color="#e91e63";glow="#fce4ec";\n'
        '    } else if('+COND100F+'){\n'
        '      type="spriggite_fox9e";color="#be185d";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="stannite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="spriggite_fox9e"?BASE_R*1.41:type==="stannite_orb9e"?BASE_R*1.40:'
A9_NEW='type==="stephanite_fox9e"?BASE_R*1.42:type==="strengite_orb9e"?BASE_R*1.41:type==="spriggite_fox9e"?BASE_R*1.41:type==="stannite_orb9e"?BASE_R*1.40:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='ECLIPSE_FLARE42:"🌑🌟",LUNAR_FLARE42:"🌕🌟",THUNDER_FLARE42:"⚡🌟"'
A10_NEW='COSMOS_FLARE42:"🌌🌟",STELLAR_FLARE42:"⭐✨",ECLIPSE_FLARE42:"🌑🌟",LUNAR_FLARE42:"🌕🌟",THUNDER_FLARE42:"⚡🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 697 done! +{len(src)-len(orig)} bytes")
