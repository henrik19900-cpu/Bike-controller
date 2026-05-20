import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"scheelite_orb9e_peak", label:"Scheelite Orb Peak", desc:"Reach peak with Scheelite Orb", icon:"⚪", xp:120 },'
A1_NEW=('{ id:"scheelite_orb9e_peak", label:"Scheelite Orb Peak", desc:"Reach peak with Scheelite Orb", icon:"⚪", xp:120 },\n'
        '  { id:"eclipse_ray42_use", label:"Eclipse Ray 42", desc:"Activate ECLIPSE_RAY42 power-up", icon:"🌑", xp:60 },\n'
        '  { id:"eclipse_ray42_max", label:"Eclipse Rayer 42", desc:"Reach max with ECLIPSE_RAY42 active", icon:"🌑", xp:120 },\n'
        '  { id:"lunar_ray42_use", label:"Lunar Ray 42", desc:"Activate LUNAR_RAY42 power-up", icon:"🌕", xp:60 },\n'
        '  { id:"lunar_ray42_max", label:"Lunar Rayer 42", desc:"Reach max with LUNAR_RAY42 active", icon:"🌕", xp:120 },\n'
        '  { id:"scolecite_fox9e_tap", label:"Scolecite Fox", desc:"Tap a Scolecite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"scolecite_fox9e_peak", label:"Scolecite Fox Peak", desc:"Reach peak with Scolecite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"scorodite_orb9e_tap", label:"Scorodite Orb", desc:"Tap a Scorodite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"scorodite_orb9e_peak", label:"Scorodite Orb Peak", desc:"Reach peak with Scorodite Orb", icon:"🟣", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"THUNDER_RAY42","AURORA_RAY42","NOVA_RAY42"'
A2_NEW='"ECLIPSE_RAY42","LUNAR_RAY42","THUNDER_RAY42","AURORA_RAY42","NOVA_RAY42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="THUNDER_RAY42"){'
A3_NEW=('  } else if(ptype==="ECLIPSE_RAY42"){\n'
        '        gs.score+=2216;showPopup(cx,cy-1926,"+2216 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a0408",2088);if(gs.score>=bonusTotal)unlock("eclipse_ray42_max");\n'
        '      } else if(ptype==="LUNAR_RAY42"){\n'
        '        gs.score+=2218;showPopup(cx,cy-1928,"+2218 🌕",theme.accent,26);spawnShockwave(cx,cy,"#0a08dc",2090);if(gs.score>=bonusTotal)unlock("lunar_ray42_max");\n'
        '      } else if(ptype==="THUNDER_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // THUNDER_RAY42 — +2212 thunder ray bonus'
A4_NEW=('  // ECLIPSE_RAY42 — +2216 eclipse ray bonus\n'
        '      if(ptype==="ECLIPSE_RAY42"){sfx("powerUp",1879);unlock("eclipse_ray42_use");}\n'
        '      // LUNAR_RAY42 — +2218 lunar ray bonus\n'
        '      if(ptype==="LUNAR_RAY42"){sfx("powerUp",1881);unlock("lunar_ray42_use");}\n'
        '  // THUNDER_RAY42 — +2212 thunder ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawScawtiteFox9e('
A5_NEW=('function drawScoleciteFox9e(ctx,r,ts,sclPct){\n'
        '  const bob=Math.sin(ts*0.3842)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f5d0fe");g.addColorStop(0.45+sclPct*0.35,"#86198f");g.addColorStop(1,"#3b0764");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(sclPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(245,208,254,"+(sclPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sclPct>0.88?"#f5d0fe":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sclPct>0.88?"🌸":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScoroditeOrb9e(ctx,r,ts,scrPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3846);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+scrPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#faf5ff");g.addColorStop(0.35+scrPct*0.35,"#a855f7");g.addColorStop(1,"#4c1d95");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+scrPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(168,85,247,"+(0.45+scrPct*0.55)+")";ctx.lineWidth=3.5+scrPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(scrPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(168,85,247,"+(scrPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=scrPct>0.88?"#a855f7":"#faf5ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(scrPct>0.88?"🟣":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScawtiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="scawtite_fox9e"){'
A6_NEW=('  else if(t.type==="scolecite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2062);drawScoleciteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="scorodite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2064);drawScoroditeOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="scawtite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="scawtite_fox9e"){'
A7_NEW=('    if(hit.type==="scolecite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2062);\n'
        '      const pts=Math.round(360*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#86198f",2062);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌸","#fdf4ff",22);\n'
        '      unlock("scolecite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("scolecite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scorodite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2064);\n'
        '      const pts=Math.round(355*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#a855f7",2064);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟣","#faf5ff",22);\n'
        '      unlock("scorodite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("scorodite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scawtite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="scawtite_fox9e";color="#1e40af";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scheelite_orb9e"')
A8_NEW=('      type="scolecite_fox9e";color="#86198f";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scorodite_orb9e";color="#a855f7";glow="#faf5ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scawtite_fox9e";color="#1e40af";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scheelite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="scawtite_fox9e"?BASE_R*1.32:type==="scheelite_orb9e"?BASE_R*1.31:'
A9_NEW='type==="scolecite_fox9e"?BASE_R*1.33:type==="scorodite_orb9e"?BASE_R*1.32:type==="scawtite_fox9e"?BASE_R*1.32:type==="scheelite_orb9e"?BASE_R*1.31:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='THUNDER_RAY42:"⚡🔆",AURORA_RAY42:"🌌🔆",NOVA_RAY42:"💥🔆"'
A10_NEW='ECLIPSE_RAY42:"🌑🔆",LUNAR_RAY42:"🌕🔆",THUNDER_RAY42:"⚡🔆",AURORA_RAY42:"🌌🔆",NOVA_RAY42:"💥🔆"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 688 done! +{len(src)-len(orig)} bytes")
