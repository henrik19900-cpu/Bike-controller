import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"fuchsite_orb9e_peak", label:"Fuchsite Orb Peak", desc:"Reach peak with Fuchsite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"storm_pulse41_use", label:"Storm Pulse", desc:"Activate STORM_PULSE41 power-up", icon:"⛈️", xp:60 },\n'
'  { id:"storm_pulse41_max", label:"Storm Pulser", desc:"Reach max with STORM_PULSE41 active", icon:"⛈️", xp:120 },\n'
'  { id:"crystal_pulse41_use", label:"Crystal Pulse", desc:"Activate CRYSTAL_PULSE41 power-up", icon:"💎", xp:60 },\n'
'  { id:"crystal_pulse41_max", label:"Crystal Pulser", desc:"Reach max with CRYSTAL_PULSE41 active", icon:"💎", xp:120 },\n'
'  { id:"gadolinite_fox9e_tap", label:"Gadolinite Fox", desc:"Tap a Gadolinite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"gadolinite_fox9e_peak", label:"Gadolinite Fox Peak", desc:"Reach peak with Gadolinite Fox", icon:"🦊", xp:120 },\n'
'  { id:"gehlenite_orb9e_tap", label:"Gehlenite Orb", desc:"Tap a Gehlenite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"gehlenite_orb9e_peak", label:"Gehlenite Orb Peak", desc:"Reach peak with Gehlenite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"BLAZE_PULSE41","FROST_PULSE41","PRISM_PULSE41"'
A2_NEW = '"BLAZE_PULSE41","FROST_PULSE41","STORM_PULSE41","CRYSTAL_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="BLAZE_PULSE41"){'
A3_NEW = (
'} else if(ptype==="STORM_PULSE41"){\n'
'        gs.score+=2044;showPopup(cx,cy-1754,"+2044 ⛈️",theme.accent,26);spawnShockwave(cx,cy,"#0a03b2",1916);if(gs.score>=bonusTotal)unlock("storm_pulse41_max");\n'
'      } else if(ptype==="CRYSTAL_PULSE41"){\n'
'        gs.score+=2046;showPopup(cx,cy-1756,"+2046 💎",theme.accent,26);spawnShockwave(cx,cy,"#0a0886",1918);if(gs.score>=bonusTotal)unlock("crystal_pulse41_max");\n'
'      } else if(ptype==="BLAZE_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// BLAZE_PULSE41 — +2040 blaze bonus'
A4_NEW = ('// STORM_PULSE41 — +2044 storm bonus\n'
'      if(ptype==="STORM_PULSE41"){sfx("powerUp",1707);unlock("storm_pulse41_use");}\n'
'      // CRYSTAL_PULSE41 — +2046 crystal bonus\n'
'      if(ptype==="CRYSTAL_PULSE41"){sfx("powerUp",1709);unlock("crystal_pulse41_use");}\n'
'      // BLAZE_PULSE41 — +2040 blaze bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawFergusoniteFox9e('
A5_NEW = (
'function drawGadoliniteFox9e(ctx,r,ts,gadPct){\n'
'  const bob=Math.sin(ts*0.3498)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.45+gadPct*0.35,"#6b21a8");g.addColorStop(1,"#3b0764");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(gadPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(107,33,168,"+(gadPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=gadPct>0.88?"#d8b4fe":"#fdf4ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gadPct>0.88?"🔮":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGehleniteOrb9e(ctx,r,ts,gehPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3502);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+gehPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+gehPct*0.35,"#475569");g.addColorStop(1,"#1e293b");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+gehPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(71,85,105,"+(0.45+gehPct*0.55)+")";ctx.lineWidth=3.5+gehPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(gehPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(148,163,184,"+(gehPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=gehPct>0.88?"#cbd5e1":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gehPct>0.88?"🩶":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawFergusoniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="fergusonite_fox9e"){'
A6_NEW = (
'else if(t.type==="gadolinite_fox9e"){\n'
'      const gadPct=Math.min(1,(ts-t.born)/2800);t._gadPct=gadPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGadoliniteFox9e(ctx,t.radius,ts,gadPct);ctx.restore();\n'
'    } else if(t.type==="gehlenite_orb9e"){\n'
'      const gehPct=Math.min(1,(ts-t.born)/2800);t._gehPct=gehPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGehleniteOrb9e(ctx,t.radius,ts,gehPct);ctx.restore();\n'
'    } else if(t.type==="fergusonite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="fergusonite_fox9e"){'
A7_NEW = (
'if(hit.type==="gadolinite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(274*(hit._gadPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#6b21a8",1890);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("gadolinite_fox9e_tap");\n'
'        if((hit._gadPct||0)>0.88)unlock("gadolinite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="gehlenite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(269*(hit._gehPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#475569",1892);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("gehlenite_orb9e_tap");\n'
'        if((hit._gehPct||0)>0.88)unlock("gehlenite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="fergusonite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="fergusonite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fuchsite_orb9e"')
A8_NEW = ('      type="gadolinite_fox9e";color="#6b21a8";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gehlenite_orb9e";color="#475569";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fergusonite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fuchsite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="fergusonite_fox9e"?BASE_R*1.22:type==="fuchsite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="gadolinite_fox9e"?BASE_R*1.22:type==="gehlenite_orb9e"?BASE_R*1.21:type==="fergusonite_fox9e"?BASE_R*1.22:type==="fuchsite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'BLAZE_PULSE41:"🔥💠",FROST_PULSE41:"❄️💠",'
A10_NEW = 'BLAZE_PULSE41:"🔥💠",FROST_PULSE41:"❄️💠",STORM_PULSE41:"⛈️💠",CRYSTAL_PULSE41:"💎💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 645 done! +{len(src)-original_len} bytes")
