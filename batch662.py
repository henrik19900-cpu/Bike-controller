import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"mesolite_orb9e_peak", label:"Mesolite Orb Peak", desc:"Reach peak with Mesolite Orb", icon:"🌟", xp:120 },'
A1_NEW=(
  '{ id:"mesolite_orb9e_peak", label:"Mesolite Orb Peak", desc:"Reach peak with Mesolite Orb", icon:"🌟", xp:120 },\n'
  '  { id:"magma_wave41_use", label:"Magma Wave", desc:"Activate MAGMA_WAVE41 power-up", icon:"🌋", xp:60 },\n'
  '  { id:"magma_wave41_max", label:"Magma Waver", desc:"Reach max with MAGMA_WAVE41 active", icon:"🌋", xp:120 },\n'
  '  { id:"frost_wave41_use", label:"Frost Wave", desc:"Activate FROST_WAVE41 power-up", icon:"❄️", xp:60 },\n'
  '  { id:"frost_wave41_max", label:"Frost Waver", desc:"Reach max with FROST_WAVE41 active", icon:"❄️", xp:120 },\n'
  '  { id:"microcline_fox9e_tap", label:"Microcline Fox", desc:"Tap Microcline Fox target", icon:"💚", xp:60 },\n'
  '  { id:"microcline_fox9e_peak", label:"Microcline Peak", desc:"Reach peak with Microcline Fox", icon:"💚", xp:120 },\n'
  '  { id:"millerite_orb9e_tap", label:"Millerite Orb", desc:"Tap Millerite Orb target", icon:"🌕", xp:60 },\n'
  '  { id:"millerite_orb9e_peak", label:"Millerite Orb Peak", desc:"Reach peak with Millerite Orb", icon:"🌕", xp:120 },'
)
assert src.count(A1_OLD)==1, f"Step 1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: power-up list ───────────────────────────────────────────────────
A2_OLD='"INFERNO_WAVE41","BLAZE_WAVE41","THUNDER_WAVE41"'
A2_NEW='"MAGMA_WAVE41","FROST_WAVE41","INFERNO_WAVE41","BLAZE_WAVE41","THUNDER_WAVE41"'
assert src.count(A2_OLD)==1, f"Step 2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up handler block ─────────────────────────────────────────
A3_OLD='  } else if(ptype==="INFERNO_WAVE41"){\n        gs.score+=2108;showPopup(cx,cy-1818,"+2108 🔥",theme.accent,26);spawnShockwave(cx,cy,"#0a03d2",1980);if(gs.score>=bonusTotal)unlock("inferno_wave41_max");\n      } else if(ptype==="BLAZE_WAVE41"){'
A3_NEW=(
  '  } else if(ptype==="MAGMA_WAVE41"){\n'
  '        gs.score+=2112;showPopup(cx,cy-1822,"+2112 🌋",theme.accent,26);spawnShockwave(cx,cy,"#0a03d4",1984);if(gs.score>=bonusTotal)unlock("magma_wave41_max");\n'
  '      } else if(ptype==="FROST_WAVE41"){\n'
  '        gs.score+=2114;showPopup(cx,cy-1824,"+2114 ❄️",theme.accent,26);spawnShockwave(cx,cy,"#0a08a8",1986);if(gs.score>=bonusTotal)unlock("frost_wave41_max");\n'
  '      } else if(ptype==="INFERNO_WAVE41"){\n'
  '        gs.score+=2108;showPopup(cx,cy-1818,"+2108 🔥",theme.accent,26);spawnShockwave(cx,cy,"#0a03d2",1980);if(gs.score>=bonusTotal)unlock("inferno_wave41_max");\n'
  '      } else if(ptype==="BLAZE_WAVE41"){'
)
assert src.count(A3_OLD)==1, f"Step 3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock ────────────────────────────────────────────────────
A4_OLD='  // INFERNO_WAVE41 — +2108 inferno wave bonus\n      if(ptype==="INFERNO_WAVE41"){sfx("powerUp",1771);unlock("inferno_wave41_use");}'
A4_NEW=(
  '  // MAGMA_WAVE41 — +2112 magma wave bonus\n'
  '      if(ptype==="MAGMA_WAVE41"){sfx("powerUp",1775);unlock("magma_wave41_use");}\n'
  '      // FROST_WAVE41 — +2114 frost wave bonus\n'
  '      if(ptype==="FROST_WAVE41"){sfx("powerUp",1777);unlock("frost_wave41_use");}\n'
  '  // INFERNO_WAVE41 — +2108 inferno wave bonus\n'
  '      if(ptype==="INFERNO_WAVE41"){sfx("powerUp",1771);unlock("inferno_wave41_use");}'
)
assert src.count(A4_OLD)==1, f"Step 4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ──────────────────────────────────────────────────
A5_OLD='function drawMelliteFox9e('
A5_NEW=(
  'function drawMicroclineFox9e(ctx,r,ts,micPct){\n'
  '  const bob=Math.sin(ts*0.3634)*r*0.07;\n'
  '  ctx.save();ctx.translate(0,bob);\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+micPct*0.35,"#10b981");g.addColorStop(1,"#064e3b");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  if(micPct>0.65){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(16,185,129,"+(micPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
  '  ctx.fillStyle=micPct>0.88?"#064e3b":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(micPct>0.88?"💚":"🦊",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMilleriteOrb9e(ctx,r,ts,milPct){\n'
  '  const pulse=0.72+0.28*Math.sin(ts*0.3638);\n'
  '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+milPct*0.27;\n'
  '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
  '  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+milPct*0.35,"#eab308");g.addColorStop(1,"#713f12");\n'
  '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
  '  const ring=r*(0.54+milPct*0.42);\n'
  '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
  '  ctx.strokeStyle="rgba(234,179,8,"+(0.45+milPct*0.55)+")";ctx.lineWidth=3.5+milPct*3;ctx.stroke();\n'
  '  ctx.globalAlpha=1;\n'
  '  if(milPct>0.82){\n'
  '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
  '    ctx.strokeStyle="rgba(253,224,71,"+(milPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
  '  ctx.fillStyle=milPct>0.88?"#eab308":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
  '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(milPct>0.88?"🌕":"🔮",0,1);\n'
  '  ctx.restore();\n'
  '}\n'
  'function drawMelliteFox9e('
)
assert src.count(A5_OLD)==1, f"Step 5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ───────────────────────────────────────────────────
A6_OLD='  else if(t.type==="mellite_fox9e"){\n      const mellPct=Math.min(1,(ts-t.born)/2800);t._mellPct=mellPct;\n      ctx.save();ctx.translate(t.x,t.y);drawMelliteFox9e(ctx,t.radius,ts,mellPct);ctx.restore();\n    } else if(t.type==="mesolite_orb9e"){'
A6_NEW=(
  '  else if(t.type==="microcline_fox9e"){\n'
  '      const micPct=Math.min(1,(ts-t.born)/2800);t._micPct=micPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMicroclineFox9e(ctx,t.radius,ts,micPct);ctx.restore();\n'
  '    } else if(t.type==="millerite_orb9e"){\n'
  '      const milPct=Math.min(1,(ts-t.born)/2800);t._milPct=milPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMilleriteOrb9e(ctx,t.radius,ts,milPct);ctx.restore();\n'
  '    } else if(t.type==="mellite_fox9e"){\n'
  '      const mellPct=Math.min(1,(ts-t.born)/2800);t._mellPct=mellPct;\n'
  '      ctx.save();ctx.translate(t.x,t.y);drawMelliteFox9e(ctx,t.radius,ts,mellPct);ctx.restore();\n'
  '    } else if(t.type==="mesolite_orb9e"){'
)
assert src.count(A6_OLD)==1, f"Step 6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap ───────────────────────────────────────────────────────
A7_OLD='    if(hit.type==="mellite_fox9e"){\n        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n        const combo=gs.streak+1;const pts=Math.round(306*(hit._mellPct||0.5)*combo);\n        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n        spawnShockwave(hit.x,hit.y,"#f59e0b",1954);\n        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🍯",theme.accent,22);\n        unlock("mellite_fox9e_tap");\n        if((hit._mellPct||0)>0.88)unlock("mellite_fox9e_peak");\n        updateMissions({type:"special_tap"});debounceSave();return;\n      } if(hit.type==="mesolite_orb9e"){'
A7_NEW=(
  '    if(hit.type==="microcline_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(308*(hit._micPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#10b981",1958);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 💚",theme.accent,22);\n'
  '        unlock("microcline_fox9e_tap");\n'
  '        if((hit._micPct||0)>0.88)unlock("microcline_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="millerite_orb9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(303*(hit._milPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#eab308",1960);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🌕",theme.accent,22);\n'
  '        unlock("millerite_orb9e_tap");\n'
  '        if((hit._milPct||0)>0.88)unlock("millerite_orb9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="mellite_fox9e"){\n'
  '        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
  '        const combo=gs.streak+1;const pts=Math.round(306*(hit._mellPct||0.5)*combo);\n'
  '        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
  '        spawnShockwave(hit.x,hit.y,"#f59e0b",1954);\n'
  '        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🍯",theme.accent,22);\n'
  '        unlock("mellite_fox9e_tap");\n'
  '        if((hit._mellPct||0)>0.88)unlock("mellite_fox9e_peak");\n'
  '        updateMissions({type:"special_tap"});debounceSave();return;\n'
  '      } if(hit.type==="mesolite_orb9e"){'
)
assert src.count(A7_OLD)==1, f"Step 7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget ─────────────────────────────────────────────────────
A8_OLD=('      type="mellite_fox9e";color="#f59e0b";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mesolite_orb9e"')
A8_NEW=('      type="microcline_fox9e";color="#10b981";glow="#ecfdf5";\n'
        '    } else if('+COND100F+'){\n'
        '      type="millerite_orb9e";color="#eab308";glow="#fefce8";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mellite_fox9e";color="#f59e0b";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="mesolite_orb9e"')
assert src.count(A8_OLD)==1, f"Step 8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ────────────────────────────────────────────────────
A9_OLD='type==="mellite_fox9e"?BASE_R*1.22:type==="mesolite_orb9e"?BASE_R*1.21:'
A9_NEW='type==="microcline_fox9e"?BASE_R*1.22:type==="millerite_orb9e"?BASE_R*1.21:type==="mellite_fox9e"?BASE_R*1.22:type==="mesolite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD)==1, f"Step 9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map ───────────────────────────────────────────────────────
A10_OLD='INFERNO_WAVE41:"🔥💠",BLAZE_WAVE41:"🌊💠",THUNDER_WAVE41:"⚡💠"'
A10_NEW='MAGMA_WAVE41:"🌋💠",FROST_WAVE41:"❄️💠",INFERNO_WAVE41:"🔥💠",BLAZE_WAVE41:"🌊💠",THUNDER_WAVE41:"⚡💠"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step 10 anchor count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

with open("src/NexusTap.jsx","w") as f:
    f.write(src)

print("Step 1 OK" if src.count("magma_wave41_use")>=2 else "Step 1 FAIL")
print("Step 2 OK" if src.count('"MAGMA_WAVE41"')>=1 else "Step 2 FAIL")
print("Step 3 OK" if src.count('ptype==="MAGMA_WAVE41"')>=1 else "Step 3 FAIL")
print("Step 4 OK" if src.count('sfx("powerUp",1775)')>=1 else "Step 4 FAIL")
print("Step 5 OK" if src.count("drawMicroclineFox9e")>=1 else "Step 5 FAIL")
print("Step 6 OK" if src.count('t.type==="microcline_fox9e"')>=1 else "Step 6 FAIL")
print("Step 7 OK" if src.count('hit.type==="microcline_fox9e"')>=1 else "Step 7 FAIL")
print("Step 8 OK" if src.count('type="microcline_fox9e"')>=1 else "Step 8 FAIL")
print("Step 9 OK" if src.count('type==="microcline_fox9e"?BASE_R*1.22')>=1 else "Step 9 FAIL")
print("Step 10 OK" if src.count('MAGMA_WAVE41:"🌋💠"')>=2 else "Step 10 FAIL")
print(f"Batch 662 done! +{len(src)-len(orig)} bytes")
