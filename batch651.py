import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"hibonite_orb9e_peak", label:"Hibonite Orb Peak", desc:"Reach peak with Hibonite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"solar_wave41_use", label:"Solar Wave", desc:"Activate SOLAR_WAVE41 power-up", icon:"☀️", xp:60 },\n'
'  { id:"solar_wave41_max", label:"Solar Waver", desc:"Reach max with SOLAR_WAVE41 active", icon:"☀️", xp:120 },\n'
'  { id:"tide_wave41_use", label:"Tide Wave", desc:"Activate TIDE_WAVE41 power-up", icon:"🌊", xp:60 },\n'
'  { id:"tide_wave41_max", label:"Tide Waver", desc:"Reach max with TIDE_WAVE41 active", icon:"🌊", xp:120 },\n'
'  { id:"inderite_fox9e_tap", label:"Inderite Fox", desc:"Tap an Inderite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"inderite_fox9e_peak", label:"Inderite Fox Peak", desc:"Reach peak with Inderite Fox", icon:"🦊", xp:120 },\n'
'  { id:"inesite_orb9e_tap", label:"Inesite Orb", desc:"Tap an Inesite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"inesite_orb9e_peak", label:"Inesite Orb Peak", desc:"Reach peak with Inesite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"IONIC_WAVE41","LUNAR_WAVE41","PRISM_PULSE41"'
A2_NEW = '"IONIC_WAVE41","LUNAR_WAVE41","SOLAR_WAVE41","TIDE_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="IONIC_WAVE41"){'
A3_NEW = (
'} else if(ptype==="SOLAR_WAVE41"){\n'
'        gs.score+=2068;showPopup(cx,cy-1778,"+2068 ☀️",theme.accent,26);spawnShockwave(cx,cy,"#0a03be",1940);if(gs.score>=bonusTotal)unlock("solar_wave41_max");\n'
'      } else if(ptype==="TIDE_WAVE41"){\n'
'        gs.score+=2070;showPopup(cx,cy-1780,"+2070 🌊",theme.accent,26);spawnShockwave(cx,cy,"#0a0892",1942);if(gs.score>=bonusTotal)unlock("tide_wave41_max");\n'
'      } else if(ptype==="IONIC_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// IONIC_WAVE41 — +2064 ionic wave bonus'
A4_NEW = ('// SOLAR_WAVE41 — +2068 solar wave bonus\n'
'      if(ptype==="SOLAR_WAVE41"){sfx("powerUp",1731);unlock("solar_wave41_use");}\n'
'      // TIDE_WAVE41 — +2070 tide wave bonus\n'
'      if(ptype==="TIDE_WAVE41"){sfx("powerUp",1733);unlock("tide_wave41_use");}\n'
'      // IONIC_WAVE41 — +2064 ionic wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawHureauliteFox9e('
A5_NEW = (
'function drawInderiteFox9e(ctx,r,ts,indPct){\n'
'  const bob=Math.sin(ts*0.3546)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fafafa");g.addColorStop(0.45+indPct*0.35,"#a78bfa");g.addColorStop(1,"#4c1d95");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(indPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(167,139,250,"+(indPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=indPct>0.88?"#ddd6fe":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(indPct>0.88?"🫧":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawInesiteOrb9e(ctx,r,ts,inePct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3550);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+inePct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fff1f2");g.addColorStop(0.35+inePct*0.35,"#e11d48");g.addColorStop(1,"#4c0519");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+inePct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(225,29,72,"+(0.45+inePct*0.55)+")";ctx.lineWidth=3.5+inePct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(inePct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(253,164,175,"+(inePct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=inePct>0.88?"#fda4af":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(inePct>0.88?"🌹":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawHureauliteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="hureaulite_fox9e"){'
A6_NEW = (
'else if(t.type==="inderite_fox9e"){\n'
'      const indPct=Math.min(1,(ts-t.born)/2800);t._indPct=indPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawInderiteFox9e(ctx,t.radius,ts,indPct);ctx.restore();\n'
'    } else if(t.type==="inesite_orb9e"){\n'
'      const inePct=Math.min(1,(ts-t.born)/2800);t._inePct=inePct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawInesiteOrb9e(ctx,t.radius,ts,inePct);ctx.restore();\n'
'    } else if(t.type==="hureaulite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="hureaulite_fox9e"){'
A7_NEW = (
'if(hit.type==="inderite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(286*(hit._indPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#a78bfa",1914);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("inderite_fox9e_tap");\n'
'        if((hit._indPct||0)>0.88)unlock("inderite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="inesite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(281*(hit._inePct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#e11d48",1916);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("inesite_orb9e_tap");\n'
'        if((hit._inePct||0)>0.88)unlock("inesite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="hureaulite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="hureaulite_fox9e";color="#db2777";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="hibonite_orb9e"')
A8_NEW = ('      type="inderite_fox9e";color="#a78bfa";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="inesite_orb9e";color="#e11d48";glow="#fff1f2";\n'
           '    } else if('+COND100F+'){\n'
           '      type="hureaulite_fox9e";color="#db2777";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="hibonite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="hureaulite_fox9e"?BASE_R*1.22:type==="hibonite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="inderite_fox9e"?BASE_R*1.22:type==="inesite_orb9e"?BASE_R*1.21:type==="hureaulite_fox9e"?BASE_R*1.22:type==="hibonite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'IONIC_WAVE41:"⚗️💠",LUNAR_WAVE41:"🌙💠",'
A10_NEW = 'IONIC_WAVE41:"⚗️💠",LUNAR_WAVE41:"🌙💠",SOLAR_WAVE41:"☀️💠",TIDE_WAVE41:"🌊💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 651 done! +{len(src)-original_len} bytes")
