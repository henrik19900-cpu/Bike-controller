import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"ruarsite_orb9e_peak", label:"Ruarsite Orb Peak", desc:"Reach peak with Ruarsite Orb", icon:"🔴", xp:120 },'
A1_NEW=('{ id:"ruarsite_orb9e_peak", label:"Ruarsite Orb Peak", desc:"Reach peak with Ruarsite Orb", icon:"🔴", xp:120 },\n'
        '  { id:"thunder_beam42_use", label:"Thunder Beam 42", desc:"Activate THUNDER_BEAM42 power-up", icon:"⚡", xp:60 },\n'
        '  { id:"thunder_beam42_max", label:"Thunder Beamer 42", desc:"Reach max with THUNDER_BEAM42 active", icon:"⚡", xp:120 },\n'
        '  { id:"aurora_beam42_use", label:"Aurora Beam 42", desc:"Activate AURORA_BEAM42 power-up", icon:"🌌", xp:60 },\n'
        '  { id:"aurora_beam42_max", label:"Aurora Beamer 42", desc:"Reach max with AURORA_BEAM42 active", icon:"🌌", xp:120 },\n'
        '  { id:"rubicline_fox9e_tap", label:"Rubicline Fox", desc:"Tap a Rubicline Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"rubicline_fox9e_peak", label:"Rubicline Fox Peak", desc:"Reach peak with Rubicline Fox", icon:"🦊", xp:120 },\n'
        '  { id:"ruizite_orb9e_tap", label:"Ruizite Orb", desc:"Tap a Ruizite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"ruizite_orb9e_peak", label:"Ruizite Orb Peak", desc:"Reach peak with Ruizite Orb", icon:"🟡", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"VOID_BEAM42","PRISM_BEAM42","STAR_BEAM42"'
A2_NEW='"THUNDER_BEAM42","AURORA_BEAM42","VOID_BEAM42","PRISM_BEAM42","STAR_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="VOID_BEAM42"){'
A3_NEW=('  } else if(ptype==="THUNDER_BEAM42"){\n'
        '        gs.score+=2196;showPopup(cx,cy-1906,"+2196 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03fe",2068);if(gs.score>=bonusTotal)unlock("thunder_beam42_max");\n'
        '      } else if(ptype==="AURORA_BEAM42"){\n'
        '        gs.score+=2198;showPopup(cx,cy-1908,"+2198 🌌",theme.accent,26);spawnShockwave(cx,cy,"#0a08d2",2070);if(gs.score>=bonusTotal)unlock("aurora_beam42_max");\n'
        '      } else if(ptype==="VOID_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // VOID_BEAM42 — +2192 void beam bonus'
A4_NEW=('  // THUNDER_BEAM42 — +2196 thunder beam bonus\n'
        '      if(ptype==="THUNDER_BEAM42"){sfx("powerUp",1859);unlock("thunder_beam42_use");}\n'
        '      // AURORA_BEAM42 — +2198 aurora beam bonus\n'
        '      if(ptype==="AURORA_BEAM42"){sfx("powerUp",1861);unlock("aurora_beam42_use");}\n'
        '  // VOID_BEAM42 — +2192 void beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRoweiteeFox9e('
A5_NEW=('function drawRubiclineFox9e(ctx,r,ts,rubPct){\n'
        '  const bob=Math.sin(ts*0.3802)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fca5a5");g.addColorStop(0.45+rubPct*0.35,"#991b1b");g.addColorStop(1,"#450a0a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(rubPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(252,165,165,"+(rubPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rubPct>0.88?"#fca5a5":"#fff5f5";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rubPct>0.88?"🔥":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRuiziteOrb9e(ctx,r,ts,ruiPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3806);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ruiPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+ruiPct*0.35,"#fde047");g.addColorStop(1,"#854d0e");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+ruiPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(253,224,71,"+(0.45+ruiPct*0.55)+")";ctx.lineWidth=3.5+ruiPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(ruiPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(253,224,71,"+(ruiPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=ruiPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ruiPct>0.88?"🟡":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRoweiteeFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="roweite_fox9e"){'
A6_NEW=('  else if(t.type==="rubicline_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2042);drawRubiclineFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="ruizite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2044);drawRuiziteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="roweite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="roweite_fox9e"){'
A7_NEW=('    if(hit.type==="rubicline_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2042);\n'
        '      const pts=Math.round(350*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#991b1b",2042);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔥","#fff5f5",22);\n'
        '      unlock("rubicline_fox9e_tap");\n'
        '      if(rp>0.88)unlock("rubicline_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="ruizite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2044);\n'
        '      const pts=Math.round(345*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#fde047",2044);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟡","#fefce8",22);\n'
        '      unlock("ruizite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("ruizite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="roweite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="roweite_fox9e";color="#4c1d95";glow="#ede9fe";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruarsite_orb9e"')
A8_NEW=('      type="rubicline_fox9e";color="#991b1b";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruizite_orb9e";color="#fde047";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="roweite_fox9e";color="#4c1d95";glow="#ede9fe";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruarsite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="roweite_fox9e"?BASE_R*1.27:type==="ruarsite_orb9e"?BASE_R*1.26:'
A9_NEW='type==="rubicline_fox9e"?BASE_R*1.28:type==="ruizite_orb9e"?BASE_R*1.27:type==="roweite_fox9e"?BASE_R*1.27:type==="ruarsite_orb9e"?BASE_R*1.26:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='VOID_BEAM42:"🕳️💡",PRISM_BEAM42:"🔆💡",STAR_BEAM42:"⭐💡"'
A10_NEW='THUNDER_BEAM42:"⚡💡",AURORA_BEAM42:"🌌💡",VOID_BEAM42:"🕳️💡",PRISM_BEAM42:"🔆💡",STAR_BEAM42:"⭐💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 683 done! +{len(src)-len(orig)} bytes")
