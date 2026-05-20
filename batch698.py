import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"strengite_orb9e_peak", label:"Strengite Orb Peak", desc:"Reach peak with Strengite Orb", icon:"🌺", xp:120 },'
A1_NEW=('{ id:"strengite_orb9e_peak", label:"Strengite Orb Peak", desc:"Reach peak with Strengite Orb", icon:"🌺", xp:120 },\n'
        '  { id:"nexus_flare42_use", label:"Nexus Flare 42", desc:"Activate NEXUS_FLARE42 power-up", icon:"🔵", xp:60 },\n'
        '  { id:"nexus_flare42_max", label:"Nexus Flarer 42", desc:"Reach max with NEXUS_FLARE42 active", icon:"🔵", xp:120 },\n'
        '  { id:"prism_glow42_use", label:"Prism Glow 42", desc:"Activate PRISM_GLOW42 power-up", icon:"🔆", xp:60 },\n'
        '  { id:"prism_glow42_max", label:"Prism Glower 42", desc:"Reach max with PRISM_GLOW42 active", icon:"🔆", xp:120 },\n'
        '  { id:"struvite_fox9e_tap", label:"Struvite Fox", desc:"Tap a Struvite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"struvite_fox9e_peak", label:"Struvite Fox Peak", desc:"Reach peak with Struvite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"studenitsite_orb9e_tap", label:"Studenitsite Orb", desc:"Tap a Studenitsite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"studenitsite_orb9e_peak", label:"Studenitsite Orb Peak", desc:"Reach peak with Studenitsite Orb", icon:"🟢", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"COSMOS_FLARE42","STELLAR_FLARE42","ECLIPSE_FLARE42"'
A2_NEW='"NEXUS_FLARE42","PRISM_GLOW42","COSMOS_FLARE42","STELLAR_FLARE42","ECLIPSE_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="COSMOS_FLARE42"){'
A3_NEW=('  } else if(ptype==="NEXUS_FLARE42"){\n'
        '        gs.score+=2256;showPopup(cx,cy-1966,"+2256 🔵",theme.accent,26);spawnShockwave(cx,cy,"#0a041c",2128);if(gs.score>=bonusTotal)unlock("nexus_flare42_max");\n'
        '      } else if(ptype==="PRISM_GLOW42"){\n'
        '        gs.score+=2258;showPopup(cx,cy-1968,"+2258 🔆",theme.accent,26);spawnShockwave(cx,cy,"#0a08f0",2130);if(gs.score>=bonusTotal)unlock("prism_glow42_max");\n'
        '      } else if(ptype==="COSMOS_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // COSMOS_FLARE42 — +2252 cosmos flare bonus'
A4_NEW=('  // NEXUS_FLARE42 — +2256 nexus flare bonus\n'
        '      if(ptype==="NEXUS_FLARE42"){sfx("powerUp",1919);unlock("nexus_flare42_use");}\n'
        '      // PRISM_GLOW42 — +2258 prism glow bonus\n'
        '      if(ptype==="PRISM_GLOW42"){sfx("powerUp",1921);unlock("prism_glow42_use");}\n'
        '  // COSMOS_FLARE42 — +2252 cosmos flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawStephaniteFox9e('
A5_NEW=('function drawStruviteFox9e(ctx,r,ts,strPct){\n'
        '  const bob=Math.sin(ts*0.3922)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#bbf7d0");g.addColorStop(0.45+strPct*0.35,"#16a34a");g.addColorStop(1,"#052e16");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(strPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(187,247,208,"+(strPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=strPct>0.88?"#bbf7d0":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(strPct>0.88?"🍃":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawStudenitsiteOrb9e(ctx,r,ts,studPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3926);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+studPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.35+studPct*0.35,"#22c55e");g.addColorStop(1,"#14532d");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+studPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(34,197,94,"+(0.45+studPct*0.55)+")";ctx.lineWidth=3.5+studPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(studPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(34,197,94,"+(studPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=studPct>0.88?"#22c55e":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(studPct>0.88?"🟢":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawStephaniteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="stephanite_fox9e"){'
A6_NEW=('  else if(t.type==="struvite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2102);drawStruviteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="studenitsite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2104);drawStudenitsiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="stephanite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="stephanite_fox9e"){'
A7_NEW=('    if(hit.type==="struvite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2102);\n'
        '      const pts=Math.round(380*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#16a34a",2102);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🍃","#f0fdf4",22);\n'
        '      unlock("struvite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("struvite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="studenitsite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2104);\n'
        '      const pts=Math.round(375*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#22c55e",2104);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟢","#dcfce7",22);\n'
        '      unlock("studenitsite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("studenitsite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="stephanite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="stephanite_fox9e";color="#6200ea";glow="#ede7f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="strengite_orb9e"')
A8_NEW=('      type="struvite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="studenitsite_orb9e";color="#22c55e";glow="#dcfce7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="stephanite_fox9e";color="#6200ea";glow="#ede7f6";\n'
        '    } else if('+COND100F+'){\n'
        '      type="strengite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="stephanite_fox9e"?BASE_R*1.42:type==="strengite_orb9e"?BASE_R*1.41:'
A9_NEW='type==="struvite_fox9e"?BASE_R*1.43:type==="studenitsite_orb9e"?BASE_R*1.42:type==="stephanite_fox9e"?BASE_R*1.42:type==="strengite_orb9e"?BASE_R*1.41:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='COSMOS_FLARE42:"🌌🌟",STELLAR_FLARE42:"⭐✨",ECLIPSE_FLARE42:"🌑🌟"'
A10_NEW='NEXUS_FLARE42:"🔵✨",PRISM_GLOW42:"🔆✨",COSMOS_FLARE42:"🌌🌟",STELLAR_FLARE42:"⭐✨",ECLIPSE_FLARE42:"🌑🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 698 done! +{len(src)-len(orig)} bytes")
