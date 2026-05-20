import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"ruizite_orb9e_peak", label:"Ruizite Orb Peak", desc:"Reach peak with Ruizite Orb", icon:"🟡", xp:120 },'
A1_NEW=('{ id:"ruizite_orb9e_peak", label:"Ruizite Orb Peak", desc:"Reach peak with Ruizite Orb", icon:"🟡", xp:120 },\n'
        '  { id:"eclipse_beam42_use", label:"Eclipse Beam 42", desc:"Activate ECLIPSE_BEAM42 power-up", icon:"🌑", xp:60 },\n'
        '  { id:"eclipse_beam42_max", label:"Eclipse Beamer 42", desc:"Reach max with ECLIPSE_BEAM42 active", icon:"🌑", xp:120 },\n'
        '  { id:"lunar_beam42_use", label:"Lunar Beam 42", desc:"Activate LUNAR_BEAM42 power-up", icon:"🌕", xp:60 },\n'
        '  { id:"lunar_beam42_max", label:"Lunar Beamer 42", desc:"Reach max with LUNAR_BEAM42 active", icon:"🌕", xp:120 },\n'
        '  { id:"russelite_fox9e_tap", label:"Russelite Fox", desc:"Tap a Russelite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"russelite_fox9e_peak", label:"Russelite Fox Peak", desc:"Reach peak with Russelite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"sahamalite_orb9e_tap", label:"Sahamalite Orb", desc:"Tap a Sahamalite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"sahamalite_orb9e_peak", label:"Sahamalite Orb Peak", desc:"Reach peak with Sahamalite Orb", icon:"🌿", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"THUNDER_BEAM42","AURORA_BEAM42","VOID_BEAM42"'
A2_NEW='"ECLIPSE_BEAM42","LUNAR_BEAM42","THUNDER_BEAM42","AURORA_BEAM42","VOID_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="THUNDER_BEAM42"){'
A3_NEW=('  } else if(ptype==="ECLIPSE_BEAM42"){\n'
        '        gs.score+=2200;showPopup(cx,cy-1910,"+2200 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a0400",2072);if(gs.score>=bonusTotal)unlock("eclipse_beam42_max");\n'
        '      } else if(ptype==="LUNAR_BEAM42"){\n'
        '        gs.score+=2202;showPopup(cx,cy-1912,"+2202 🌕",theme.accent,26);spawnShockwave(cx,cy,"#0a08d4",2074);if(gs.score>=bonusTotal)unlock("lunar_beam42_max");\n'
        '      } else if(ptype==="THUNDER_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // THUNDER_BEAM42 — +2196 thunder beam bonus'
A4_NEW=('  // ECLIPSE_BEAM42 — +2200 eclipse beam bonus\n'
        '      if(ptype==="ECLIPSE_BEAM42"){sfx("powerUp",1863);unlock("eclipse_beam42_use");}\n'
        '      // LUNAR_BEAM42 — +2202 lunar beam bonus\n'
        '      if(ptype==="LUNAR_BEAM42"){sfx("powerUp",1865);unlock("lunar_beam42_use");}\n'
        '  // THUNDER_BEAM42 — +2196 thunder beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRubiclineFox9e('
A5_NEW=('function drawRusseliteFox9e(ctx,r,ts,russPct){\n'
        '  const bob=Math.sin(ts*0.3810)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#c4b5fd");g.addColorStop(0.45+russPct*0.35,"#5b21b6");g.addColorStop(1,"#2e1065");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(russPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(196,181,253,"+(russPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=russPct>0.88?"#c4b5fd":"#f5f3ff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(russPct>0.88?"💜":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSahamaliteOrb9e(ctx,r,ts,sahPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3814);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sahPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+sahPct*0.35,"#4ade80");g.addColorStop(1,"#14532d");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sahPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(74,222,128,"+(0.45+sahPct*0.55)+")";ctx.lineWidth=3.5+sahPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sahPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(74,222,128,"+(sahPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sahPct>0.88?"#4ade80":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sahPct>0.88?"🌿":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRubiclineFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="rubicline_fox9e"){'
A6_NEW=('  else if(t.type==="russelite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2046);drawRusseliteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="sahamalite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2048);drawSahamaliteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="rubicline_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="rubicline_fox9e"){'
A7_NEW=('    if(hit.type==="russelite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2046);\n'
        '      const pts=Math.round(352*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#5b21b6",2046);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 💜","#f5f3ff",22);\n'
        '      unlock("russelite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("russelite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sahamalite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2048);\n'
        '      const pts=Math.round(347*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#4ade80",2048);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌿","#f0fdf4",22);\n'
        '      unlock("sahamalite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("sahamalite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="rubicline_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="rubicline_fox9e";color="#991b1b";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruizite_orb9e"')
A8_NEW=('      type="russelite_fox9e";color="#5b21b6";glow="#f5f3ff";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sahamalite_orb9e";color="#4ade80";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rubicline_fox9e";color="#991b1b";glow="#fff5f5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruizite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="rubicline_fox9e"?BASE_R*1.28:type==="ruizite_orb9e"?BASE_R*1.27:'
A9_NEW='type==="russelite_fox9e"?BASE_R*1.29:type==="sahamalite_orb9e"?BASE_R*1.28:type==="rubicline_fox9e"?BASE_R*1.28:type==="ruizite_orb9e"?BASE_R*1.27:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='THUNDER_BEAM42:"⚡💡",AURORA_BEAM42:"🌌💡",VOID_BEAM42:"🕳️💡"'
A10_NEW='ECLIPSE_BEAM42:"🌑💡",LUNAR_BEAM42:"🌕💡",THUNDER_BEAM42:"⚡💡",AURORA_BEAM42:"🌌💡",VOID_BEAM42:"🕳️💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 684 done! +{len(src)-len(orig)} bytes")
