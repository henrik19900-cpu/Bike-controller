import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"skinnerite_orb9e_peak", label:"Skinnerite Orb Peak", desc:"Reach peak with Skinnerite Orb", icon:"🟡", xp:120 },'
A1_NEW=('{ id:"skinnerite_orb9e_peak", label:"Skinnerite Orb Peak", desc:"Reach peak with Skinnerite Orb", icon:"🟡", xp:120 },\n'
        '  { id:"void_flare42_use", label:"Void Flare 42", desc:"Activate VOID_FLARE42 power-up", icon:"🕳️", xp:60 },\n'
        '  { id:"void_flare42_max", label:"Void Flarer 42", desc:"Reach max with VOID_FLARE42 active", icon:"🕳️", xp:120 },\n'
        '  { id:"prism_flare42_use", label:"Prism Flare 42", desc:"Activate PRISM_FLARE42 power-up", icon:"🔆", xp:60 },\n'
        '  { id:"prism_flare42_max", label:"Prism Flarer 42", desc:"Reach max with PRISM_FLARE42 active", icon:"🔆", xp:120 },\n'
        '  { id:"sklodowskite_fox9e_tap", label:"Sklodowskite Fox", desc:"Tap a Sklodowskite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sklodowskite_fox9e_peak", label:"Sklodowskite Fox Peak", desc:"Reach peak with Sklodowskite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"smithite_orb9e_tap", label:"Smithite Orb", desc:"Tap a Smithite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"smithite_orb9e_peak", label:"Smithite Orb Peak", desc:"Reach peak with Smithite Orb", icon:"🟤", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"STAR_FLARE42","MOON_FLARE42","NOVA_FLARE42"'
A2_NEW='"VOID_FLARE42","PRISM_FLARE42","STAR_FLARE42","MOON_FLARE42","NOVA_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="STAR_FLARE42"){'
A3_NEW=('  } else if(ptype==="VOID_FLARE42"){\n'
        '        gs.score+=2240;showPopup(cx,cy-1950,"+2240 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a0414",2112);if(gs.score>=bonusTotal)unlock("void_flare42_max");\n'
        '      } else if(ptype==="PRISM_FLARE42"){\n'
        '        gs.score+=2242;showPopup(cx,cy-1952,"+2242 🔆",theme.accent,26);spawnShockwave(cx,cy,"#0a08e8",2114);if(gs.score>=bonusTotal)unlock("prism_flare42_max");\n'
        '      } else if(ptype==="STAR_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // STAR_FLARE42 — +2236 star flare bonus'
A4_NEW=('  // VOID_FLARE42 — +2240 void flare bonus\n'
        '      if(ptype==="VOID_FLARE42"){sfx("powerUp",1903);unlock("void_flare42_use");}\n'
        '      // PRISM_FLARE42 — +2242 prism flare bonus\n'
        '      if(ptype==="PRISM_FLARE42"){sfx("powerUp",1905);unlock("prism_flare42_use");}\n'
        '  // STAR_FLARE42 — +2236 star flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawSinkankasiteFox9e('
A5_NEW=('function drawSklodowskiteFox9e(ctx,r,ts,skdPct){\n'
        '  const bob=Math.sin(ts*0.3890)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f0abfc");g.addColorStop(0.45+skdPct*0.35,"#a21caf");g.addColorStop(1,"#4a044e");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(skdPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(240,171,252,"+(skdPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=skdPct>0.88?"#f0abfc":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(skdPct>0.88?"🌺":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSmithiteOrb9e(ctx,r,ts,smtPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3894);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+smtPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+smtPct*0.35,"#92400e");g.addColorStop(1,"#451a03");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+smtPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(146,64,14,"+(0.45+smtPct*0.55)+")";ctx.lineWidth=3.5+smtPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(smtPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(146,64,14,"+(smtPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=smtPct>0.88?"#92400e":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(smtPct>0.88?"🟤":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSinkankasiteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="sinkankasite_fox9e"){'
A6_NEW=('  else if(t.type==="sklodowskite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2086);drawSklodowskiteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="smithite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2088);drawSmithiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="sinkankasite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="sinkankasite_fox9e"){'
A7_NEW=('    if(hit.type==="sklodowskite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2086);\n'
        '      const pts=Math.round(372*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#a21caf",2086);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌺","#fdf4ff",22);\n'
        '      unlock("sklodowskite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sklodowskite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="smithite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2088);\n'
        '      const pts=Math.round(367*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#92400e",2088);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fef3c7",22);\n'
        '      unlock("smithite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("smithite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sinkankasite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="sinkankasite_fox9e";color="#4d7c0f";glow="#f7fee7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="skinnerite_orb9e"')
A8_NEW=('      type="sklodowskite_fox9e";color="#a21caf";glow="#fdf4ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="smithite_orb9e";color="#92400e";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sinkankasite_fox9e";color="#4d7c0f";glow="#f7fee7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="skinnerite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="sinkankasite_fox9e"?BASE_R*1.38:type==="skinnerite_orb9e"?BASE_R*1.37:'
A9_NEW='type==="sklodowskite_fox9e"?BASE_R*1.39:type==="smithite_orb9e"?BASE_R*1.38:type==="sinkankasite_fox9e"?BASE_R*1.38:type==="skinnerite_orb9e"?BASE_R*1.37:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='STAR_FLARE42:"⭐🌟",MOON_FLARE42:"🌙🌟",NOVA_FLARE42:"💥🌟"'
A10_NEW='VOID_FLARE42:"🕳️🌟",PRISM_FLARE42:"🔆🌟",STAR_FLARE42:"⭐🌟",MOON_FLARE42:"🌙🌟",NOVA_FLARE42:"💥🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 694 done! +{len(src)-len(orig)} bytes")
