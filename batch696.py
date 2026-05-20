import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"spertiniite_orb9e_peak", label:"Spertiniite Orb Peak", desc:"Reach peak with Spertiniite Orb", icon:"🔵", xp:120 },'
A1_NEW=('{ id:"spertiniite_orb9e_peak", label:"Spertiniite Orb Peak", desc:"Reach peak with Spertiniite Orb", icon:"🔵", xp:120 },\n'
        '  { id:"eclipse_flare42_use", label:"Eclipse Flare 42", desc:"Activate ECLIPSE_FLARE42 power-up", icon:"🌑", xp:60 },\n'
        '  { id:"eclipse_flare42_max", label:"Eclipse Flarer 42", desc:"Reach max with ECLIPSE_FLARE42 active", icon:"🌑", xp:120 },\n'
        '  { id:"lunar_flare42_use", label:"Lunar Flare 42", desc:"Activate LUNAR_FLARE42 power-up", icon:"🌕", xp:60 },\n'
        '  { id:"lunar_flare42_max", label:"Lunar Flarer 42", desc:"Reach max with LUNAR_FLARE42 active", icon:"🌕", xp:120 },\n'
        '  { id:"spriggite_fox9e_tap", label:"Spriggite Fox", desc:"Tap a Spriggite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"spriggite_fox9e_peak", label:"Spriggite Fox Peak", desc:"Reach peak with Spriggite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"stannite_orb9e_tap", label:"Stannite Orb", desc:"Tap a Stannite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"stannite_orb9e_peak", label:"Stannite Orb Peak", desc:"Reach peak with Stannite Orb", icon:"⚫", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"THUNDER_FLARE42","AURORA_FLARE42","VOID_FLARE42"'
A2_NEW='"ECLIPSE_FLARE42","LUNAR_FLARE42","THUNDER_FLARE42","AURORA_FLARE42","VOID_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="THUNDER_FLARE42"){'
A3_NEW=('  } else if(ptype==="ECLIPSE_FLARE42"){\n'
        '        gs.score+=2248;showPopup(cx,cy-1958,"+2248 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a0418",2120);if(gs.score>=bonusTotal)unlock("eclipse_flare42_max");\n'
        '      } else if(ptype==="LUNAR_FLARE42"){\n'
        '        gs.score+=2250;showPopup(cx,cy-1960,"+2250 🌕",theme.accent,26);spawnShockwave(cx,cy,"#0a08ec",2122);if(gs.score>=bonusTotal)unlock("lunar_flare42_max");\n'
        '      } else if(ptype==="THUNDER_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // THUNDER_FLARE42 — +2244 thunder flare bonus'
A4_NEW=('  // ECLIPSE_FLARE42 — +2248 eclipse flare bonus\n'
        '      if(ptype==="ECLIPSE_FLARE42"){sfx("powerUp",1911);unlock("eclipse_flare42_use");}\n'
        '      // LUNAR_FLARE42 — +2250 lunar flare bonus\n'
        '      if(ptype==="LUNAR_FLARE42"){sfx("powerUp",1913);unlock("lunar_flare42_use");}\n'
        '  // THUNDER_FLARE42 — +2244 thunder flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSperryliteFox9e('
A5_NEW=('function drawSpriggiteFox9e(ctx,r,ts,spgPct){\n'
        '  const bob=Math.sin(ts*0.3906)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fce7f3");g.addColorStop(0.45+spgPct*0.35,"#be185d");g.addColorStop(1,"#500724");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(spgPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(252,231,243,"+(spgPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=spgPct>0.88?"#fce7f3":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(spgPct>0.88?"🌹":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawStanniteOrb9e(ctx,r,ts,stnPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3910);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+stnPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#27272a");g.addColorStop(0.35+stnPct*0.35,"#09090b");g.addColorStop(1,"#000000");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+stnPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(63,63,70,"+(0.45+stnPct*0.55)+")";ctx.lineWidth=3.5+stnPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(stnPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(113,113,122,"+(stnPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=stnPct>0.88?"#71717a":"#a1a1aa";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(stnPct>0.88?"⚫":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSperryliteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sperrylite_fox9e"){'
A6_NEW=('  else if(t.type==="spriggite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2094);drawSpriggiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="stannite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2096);drawStanniteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sperrylite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sperrylite_fox9e"){'
A7_NEW=('    if(hit.type==="spriggite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2094);\n'
        '      const pts=Math.round(376*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#be185d",2094);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌹","#fdf2f8",22);\n'
        '      unlock("spriggite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("spriggite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="stannite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2096);\n'
        '      const pts=Math.round(371*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#3f3f46",2096);\n'
        '      showPopup(cx,cy-38,"+"+pts+" ⚫","#a1a1aa",22);\n'
        '      unlock("stannite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("stannite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sperrylite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sperrylite_fox9e";color="#475569";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="spertiniite_orb9e"')
A8_NEW=('      type="spriggite_fox9e";color="#be185d";glow="#fdf2f8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="stannite_orb9e";color="#3f3f46";glow="#a1a1aa";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sperrylite_fox9e";color="#475569";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="spertiniite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sperrylite_fox9e"?BASE_R*1.40:type==="spertiniite_orb9e"?BASE_R*1.39:'
A9_NEW='type==="spriggite_fox9e"?BASE_R*1.41:type==="stannite_orb9e"?BASE_R*1.40:type==="sperrylite_fox9e"?BASE_R*1.40:type==="spertiniite_orb9e"?BASE_R*1.39:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='THUNDER_FLARE42:"⚡🌟",AURORA_FLARE42:"🌌🌟",VOID_FLARE42:"🕳️🌟"'
A10_NEW='ECLIPSE_FLARE42:"🌑🌟",LUNAR_FLARE42:"🌕🌟",THUNDER_FLARE42:"⚡🌟",AURORA_FLARE42:"🌌🌟",VOID_FLARE42:"🕳️🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 696 done! +{len(src)-len(orig)} bytes")
