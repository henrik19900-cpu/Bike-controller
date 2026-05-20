import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"liroconite_orb9e_peak", label:"Liroconite Orb Peak", desc:"Reach peak with Liroconite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"pulsar_wave41_use", label:"Pulsar Wave", desc:"Activate PULSAR_WAVE41 power-up", icon:"💫", xp:60 },\n'
'  { id:"pulsar_wave41_max", label:"Pulsar Waver", desc:"Reach max with PULSAR_WAVE41 active", icon:"💫", xp:120 },\n'
'  { id:"quasar_wave41_use", label:"Quasar Wave", desc:"Activate QUASAR_WAVE41 power-up", icon:"⭐", xp:60 },\n'
'  { id:"quasar_wave41_max", label:"Quasar Waver", desc:"Reach max with QUASAR_WAVE41 active", icon:"⭐", xp:120 },\n'
'  { id:"lollingite_fox9e_tap", label:"Lollingite Fox", desc:"Tap a Lollingite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"lollingite_fox9e_peak", label:"Lollingite Fox Peak", desc:"Reach peak with Lollingite Fox", icon:"🦊", xp:120 },\n'
'  { id:"lorenzenite_orb9e_tap", label:"Lorenzenite Orb", desc:"Tap a Lorenzenite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"lorenzenite_orb9e_peak", label:"Lorenzenite Orb Peak", desc:"Reach peak with Lorenzenite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"CORONA_WAVE41","ECLIPSE_WAVE41","PRISM_PULSE41"'
A2_NEW = '"CORONA_WAVE41","ECLIPSE_WAVE41","PULSAR_WAVE41","QUASAR_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="CORONA_WAVE41"){'
A3_NEW = (
'} else if(ptype==="PULSAR_WAVE41"){\n'
'        gs.score+=2096;showPopup(cx,cy-1806,"+2096 💫",theme.accent,26);spawnShockwave(cx,cy,"#0a03cc",1968);if(gs.score>=bonusTotal)unlock("pulsar_wave41_max");\n'
'      } else if(ptype==="QUASAR_WAVE41"){\n'
'        gs.score+=2098;showPopup(cx,cy-1808,"+2098 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#0a08a0",1970);if(gs.score>=bonusTotal)unlock("quasar_wave41_max");\n'
'      } else if(ptype==="CORONA_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// CORONA_WAVE41 — +2092 corona wave bonus'
A4_NEW = ('// PULSAR_WAVE41 — +2096 pulsar wave bonus\n'
'      if(ptype==="PULSAR_WAVE41"){sfx("powerUp",1759);unlock("pulsar_wave41_use");}\n'
'      // QUASAR_WAVE41 — +2098 quasar wave bonus\n'
'      if(ptype==="QUASAR_WAVE41"){sfx("powerUp",1761);unlock("quasar_wave41_use");}\n'
'      // CORONA_WAVE41 — +2092 corona wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawLeifiteFox9e('
A5_NEW = (
'function drawLollingiteFox9e(ctx,r,ts,lolPct){\n'
'  const bob=Math.sin(ts*0.3602)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+lolPct*0.35,"#64748b");g.addColorStop(1,"#1e293b");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(lolPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(100,116,139,"+(lolPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=lolPct>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lolPct>0.88?"🪨":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLorenzeniteOrb9e(ctx,r,ts,lorPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3606);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+lorPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+lorPct*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+lorPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(180,83,9,"+(0.45+lorPct*0.55)+")";ctx.lineWidth=3.5+lorPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(lorPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(251,191,36,"+(lorPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=lorPct>0.88?"#fcd34d":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lorPct>0.88?"🟡":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLeifiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="leifite_fox9e"){'
A6_NEW = (
'else if(t.type==="lollingite_fox9e"){\n'
'      const lolPct=Math.min(1,(ts-t.born)/2800);t._lolPct=lolPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLollingiteFox9e(ctx,t.radius,ts,lolPct);ctx.restore();\n'
'    } else if(t.type==="lorenzenite_orb9e"){\n'
'      const lorPct=Math.min(1,(ts-t.born)/2800);t._lorPct=lorPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLorenzeniteOrb9e(ctx,t.radius,ts,lorPct);ctx.restore();\n'
'    } else if(t.type==="leifite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="leifite_fox9e"){'
A7_NEW = (
'if(hit.type==="lollingite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(300*(hit._lolPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#64748b",1942);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("lollingite_fox9e_tap");\n'
'        if((hit._lolPct||0)>0.88)unlock("lollingite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="lorenzenite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(295*(hit._lorPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#b45309",1944);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("lorenzenite_orb9e_tap");\n'
'        if((hit._lorPct||0)>0.88)unlock("lorenzenite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="leifite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="leifite_fox9e";color="#8b5cf6";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="liroconite_orb9e"')
A8_NEW = ('      type="lollingite_fox9e";color="#64748b";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lorenzenite_orb9e";color="#b45309";glow="#fef3c7";\n'
           '    } else if('+COND100F+'){\n'
           '      type="leifite_fox9e";color="#8b5cf6";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="liroconite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="leifite_fox9e"?BASE_R*1.22:type==="liroconite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="lollingite_fox9e"?BASE_R*1.22:type==="lorenzenite_orb9e"?BASE_R*1.21:type==="leifite_fox9e"?BASE_R*1.22:type==="liroconite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'CORONA_WAVE41:"🌞💠",ECLIPSE_WAVE41:"🌑💠",'
A10_NEW = 'CORONA_WAVE41:"🌞💠",ECLIPSE_WAVE41:"🌑💠",PULSAR_WAVE41:"💫💠",QUASAR_WAVE41:"⭐💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 658 done! +{len(src)-original_len} bytes")
