import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"gehlenite_orb9e_peak", label:"Gehlenite Orb Peak", desc:"Reach peak with Gehlenite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"plasma_pulse41_use", label:"Plasma Pulse", desc:"Activate PLASMA_PULSE41 power-up", icon:"⚡", xp:60 },\n'
'  { id:"plasma_pulse41_max", label:"Plasma Pulser", desc:"Reach max with PLASMA_PULSE41 active", icon:"⚡", xp:120 },\n'
'  { id:"spark_pulse41_use", label:"Spark Pulse", desc:"Activate SPARK_PULSE41 power-up", icon:"✴️", xp:60 },\n'
'  { id:"spark_pulse41_max", label:"Spark Pulser", desc:"Reach max with SPARK_PULSE41 active", icon:"✴️", xp:120 },\n'
'  { id:"gibbsite_fox9e_tap", label:"Gibbsite Fox", desc:"Tap a Gibbsite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"gibbsite_fox9e_peak", label:"Gibbsite Fox Peak", desc:"Reach peak with Gibbsite Fox", icon:"🦊", xp:120 },\n'
'  { id:"glaucophane_orb9e_tap", label:"Glaucophane Orb", desc:"Tap a Glaucophane Orb target", icon:"🔮", xp:60 },\n'
'  { id:"glaucophane_orb9e_peak", label:"Glaucophane Orb Peak", desc:"Reach peak with Glaucophane Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"STORM_PULSE41","CRYSTAL_PULSE41","PRISM_PULSE41"'
A2_NEW = '"STORM_PULSE41","CRYSTAL_PULSE41","PLASMA_PULSE41","SPARK_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="STORM_PULSE41"){'
A3_NEW = (
'} else if(ptype==="PLASMA_PULSE41"){\n'
'        gs.score+=2048;showPopup(cx,cy-1758,"+2048 ⚡",theme.accent,26);spawnShockwave(cx,cy,"#0a03b4",1920);if(gs.score>=bonusTotal)unlock("plasma_pulse41_max");\n'
'      } else if(ptype==="SPARK_PULSE41"){\n'
'        gs.score+=2050;showPopup(cx,cy-1760,"+2050 ✴️",theme.accent,26);spawnShockwave(cx,cy,"#0a0888",1922);if(gs.score>=bonusTotal)unlock("spark_pulse41_max");\n'
'      } else if(ptype==="STORM_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// STORM_PULSE41 — +2044 storm bonus'
A4_NEW = ('// PLASMA_PULSE41 — +2048 plasma bonus\n'
'      if(ptype==="PLASMA_PULSE41"){sfx("powerUp",1711);unlock("plasma_pulse41_use");}\n'
'      // SPARK_PULSE41 — +2050 spark bonus\n'
'      if(ptype==="SPARK_PULSE41"){sfx("powerUp",1713);unlock("spark_pulse41_use");}\n'
'      // STORM_PULSE41 — +2044 storm bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawGadoliniteFox9e('
A5_NEW = (
'function drawGibbsiteFox9e(ctx,r,ts,gibPct){\n'
'  const bob=Math.sin(ts*0.3506)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fafafa");g.addColorStop(0.45+gibPct*0.35,"#d1d5db");g.addColorStop(1,"#6b7280");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(gibPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(209,213,219,"+(gibPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=gibPct>0.88?"#e5e7eb":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(gibPct>0.88?"⚪":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGlaucophaneOrb9e(ctx,r,ts,glaPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3510);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+glaPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#eff6ff");g.addColorStop(0.35+glaPct*0.35,"#1d4ed8");g.addColorStop(1,"#1e3a8a");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+glaPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(29,78,216,"+(0.45+glaPct*0.55)+")";ctx.lineWidth=3.5+glaPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(glaPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(147,197,253,"+(glaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=glaPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(glaPct>0.88?"💙":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawGadoliniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="gadolinite_fox9e"){'
A6_NEW = (
'else if(t.type==="gibbsite_fox9e"){\n'
'      const gibPct=Math.min(1,(ts-t.born)/2800);t._gibPct=gibPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGibbsiteFox9e(ctx,t.radius,ts,gibPct);ctx.restore();\n'
'    } else if(t.type==="glaucophane_orb9e"){\n'
'      const glaPct=Math.min(1,(ts-t.born)/2800);t._glaPct=glaPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawGlaucophaneOrb9e(ctx,t.radius,ts,glaPct);ctx.restore();\n'
'    } else if(t.type==="gadolinite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="gadolinite_fox9e"){'
A7_NEW = (
'if(hit.type==="gibbsite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(276*(hit._gibPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#d1d5db",1894);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("gibbsite_fox9e_tap");\n'
'        if((hit._gibPct||0)>0.88)unlock("gibbsite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="glaucophane_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(271*(hit._glaPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#1d4ed8",1896);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("glaucophane_orb9e_tap");\n'
'        if((hit._glaPct||0)>0.88)unlock("glaucophane_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="gadolinite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="gadolinite_fox9e";color="#6b21a8";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gehlenite_orb9e"')
A8_NEW = ('      type="gibbsite_fox9e";color="#d1d5db";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="glaucophane_orb9e";color="#1d4ed8";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gadolinite_fox9e";color="#6b21a8";glow="#fdf4ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="gehlenite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="gadolinite_fox9e"?BASE_R*1.22:type==="gehlenite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="gibbsite_fox9e"?BASE_R*1.22:type==="glaucophane_orb9e"?BASE_R*1.21:type==="gadolinite_fox9e"?BASE_R*1.22:type==="gehlenite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'STORM_PULSE41:"⛈️💠",CRYSTAL_PULSE41:"💎💠",'
A10_NEW = 'STORM_PULSE41:"⛈️💠",CRYSTAL_PULSE41:"💎💠",PLASMA_PULSE41:"⚡💠",SPARK_PULSE41:"✴️💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 646 done! +{len(src)-original_len} bytes")
