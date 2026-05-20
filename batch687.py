import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"scacchite_orb9e_peak", label:"Scacchite Orb Peak", desc:"Reach peak with Scacchite Orb", icon:"🟤", xp:120 },'
A1_NEW=('{ id:"scacchite_orb9e_peak", label:"Scacchite Orb Peak", desc:"Reach peak with Scacchite Orb", icon:"🟤", xp:120 },\n'
        '  { id:"thunder_ray42_use", label:"Thunder Ray 42", desc:"Activate THUNDER_RAY42 power-up", icon:"⚡", xp:60 },\n'
        '  { id:"thunder_ray42_max", label:"Thunder Rayer 42", desc:"Reach max with THUNDER_RAY42 active", icon:"⚡", xp:120 },\n'
        '  { id:"aurora_ray42_use", label:"Aurora Ray 42", desc:"Activate AURORA_RAY42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"aurora_ray42_max", label:"Aurora Rayer 42", desc:"Reach max with AURORA_RAY42 active", icon:"🌌", xp:120 },\n'
        '  { id:"scawtite_fox9e_tap", label:"Scawtite Fox", desc:"Tap a Scawtite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"scawtite_fox9e_peak", label:"Scawtite Fox Peak", desc:"Reach peak with Scawtite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"scheelite_orb9e_tap", label:"Scheelite Orb", desc:"Tap a Scheelite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"scheelite_orb9e_peak", label:"Scheelite Orb Peak", desc:"Reach peak with Scheelite Orb", icon:"⚪", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NOVA_RAY42","VOID_RAY42","COSMOS_BEAM42"'
A2_NEW='"THUNDER_RAY42","AURORA_RAY42","NOVA_RAY42","VOID_RAY42","COSMOS_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NOVA_RAY42"){'
A3_NEW=('  } else if(ptype==="THUNDER_RAY42"){\n'
        '        gs.score+=2212;showPopup(cx,cy-1922,"+2212 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a0406",2084);if(gs.score>=bonusTotal)unlock("thunder_ray42_max");\n'
        '      } else if(ptype==="AURORA_RAY42"){\n'
        '        gs.score+=2214;showPopup(cx,cy-1924,"+2214 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a08da",2086);if(gs.score>=bonusTotal)unlock("aurora_ray42_max");\n'
        '      } else if(ptype==="NOVA_RAY42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NOVA_RAY42 — +2208 nova ray bonus'
A4_NEW=('  // THUNDER_RAY42 — +2212 thunder ray bonus\n'
        '      if(ptype==="THUNDER_RAY42"){sfx("powerUp",1875);unlock("thunder_ray42_use");}\n'
        '      // AURORA_RAY42 — +2214 aurora ray bonus\n'
        '      if(ptype==="AURORA_RAY42"){sfx("powerUp",1877);unlock("aurora_ray42_use");}\n'
        '  // NOVA_RAY42 — +2208 nova ray bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSarkiniteFox9e('
A5_NEW=('function drawScawtiteFox9e(ctx,r,ts,scwPct){\n'
        '  const bob=Math.sin(ts*0.3834)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#bfdbfe");g.addColorStop(0.45+scwPct*0.35,"#1e40af");g.addColorStop(1,"#0c1a4a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(scwPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(191,219,254,"+(scwPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=scwPct>0.88?"#bfdbfe":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(scwPct>0.88?"💙":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawScheeliteOrb9e(ctx,r,ts,schPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3838);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+schPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f9fafb");g.addColorStop(0.35+schPct*0.35,"#d1d5db");g.addColorStop(1,"#374151");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+schPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(209,213,219,"+(0.45+schPct*0.55)+")";ctx.lineWidth=3.5+schPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(schPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(209,213,219,"+(schPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=schPct>0.88?"#d1d5db":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(schPct>0.88?"⚪":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSarkiniteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sarkinite_fox9e"){'
A6_NEW=('  else if(t.type==="scawtite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2058);drawScawtiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="scheelite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2060);drawScheeliteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sarkinite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sarkinite_fox9e"){'
A7_NEW=('    if(hit.type==="scawtite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2058);\n'
        '      const pts=Math.round(358*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#1e40af",2058);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💙","#eff6ff",22);\n'
        '      unlock("scawtite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("scawtite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="scheelite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2060);\n'
        '      const pts=Math.round(353*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#d1d5db",2060);\n'
        '      showPopup(cx,cy-38,"+"+pts+" ⚪","#f9fafb",22);\n'
        '      unlock("scheelite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("scheelite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sarkinite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sarkinite_fox9e";color="#c2410c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scacchite_orb9e"')
A8_NEW=('      type="scawtite_fox9e";color="#1e40af";glow="#eff6ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scheelite_orb9e";color="#d1d5db";glow="#f9fafb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sarkinite_fox9e";color="#c2410c";glow="#fff7ed";\n'
        '    } else if('+COND100F+'){\n'
        '      type="scacchite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sarkinite_fox9e"?BASE_R*1.31:type==="scacchite_orb9e"?BASE_R*1.30:'
A9_NEW='type==="scawtite_fox9e"?BASE_R*1.32:type==="scheelite_orb9e"?BASE_R*1.31:type==="sarkinite_fox9e"?BASE_R*1.31:type==="scacchite_orb9e"?BASE_R*1.30:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NOVA_RAY42:"💥🔆",VOID_RAY42:"🕳️🔆",COSMOS_BEAM42:"🌌💡"'
A10_NEW='THUNDER_RAY42:"⚡🔆",AURORA_RAY42:"🌌🔆",NOVA_RAY42:"💥🔆",VOID_RAY42:"🕳️🔆",COSMOS_BEAM42:"🌌💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 687 done! +{len(src)-len(orig)} bytes")
