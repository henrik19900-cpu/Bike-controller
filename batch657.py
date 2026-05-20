import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"leadhillite_orb9e_peak", label:"Leadhillite Orb Peak", desc:"Reach peak with Leadhillite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"corona_wave41_use", label:"Corona Wave", desc:"Activate CORONA_WAVE41 power-up", icon:"🌞", xp:60 },\n'
'  { id:"corona_wave41_max", label:"Corona Waver", desc:"Reach max with CORONA_WAVE41 active", icon:"🌞", xp:120 },\n'
'  { id:"eclipse_wave41_use", label:"Eclipse Wave", desc:"Activate ECLIPSE_WAVE41 power-up", icon:"🌑", xp:60 },\n'
'  { id:"eclipse_wave41_max", label:"Eclipse Waver", desc:"Reach max with ECLIPSE_WAVE41 active", icon:"🌑", xp:120 },\n'
'  { id:"leifite_fox9e_tap", label:"Leifite Fox", desc:"Tap a Leifite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"leifite_fox9e_peak", label:"Leifite Fox Peak", desc:"Reach peak with Leifite Fox", icon:"🦊", xp:120 },\n'
'  { id:"liroconite_orb9e_tap", label:"Liroconite Orb", desc:"Tap a Liroconite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"liroconite_orb9e_peak", label:"Liroconite Orb Peak", desc:"Reach peak with Liroconite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"GALAXY_WAVE41","VOID_WAVE41","PRISM_PULSE41"'
A2_NEW = '"GALAXY_WAVE41","VOID_WAVE41","CORONA_WAVE41","ECLIPSE_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="GALAXY_WAVE41"){'
A3_NEW = (
'} else if(ptype==="CORONA_WAVE41"){\n'
'        gs.score+=2092;showPopup(cx,cy-1802,"+2092 🌞",theme.accent,26);spawnShockwave(cx,cy,"#0a03ca",1964);if(gs.score>=bonusTotal)unlock("corona_wave41_max");\n'
'      } else if(ptype==="ECLIPSE_WAVE41"){\n'
'        gs.score+=2094;showPopup(cx,cy-1804,"+2094 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a089e",1966);if(gs.score>=bonusTotal)unlock("eclipse_wave41_max");\n'
'      } else if(ptype==="GALAXY_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// GALAXY_WAVE41 — +2088 galaxy wave bonus'
A4_NEW = ('// CORONA_WAVE41 — +2092 corona wave bonus\n'
'      if(ptype==="CORONA_WAVE41"){sfx("powerUp",1755);unlock("corona_wave41_use");}\n'
'      // ECLIPSE_WAVE41 — +2094 eclipse wave bonus\n'
'      if(ptype==="ECLIPSE_WAVE41"){sfx("powerUp",1757);unlock("eclipse_wave41_use");}\n'
'      // GALAXY_WAVE41 — +2088 galaxy wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawLawsoniteFox9e('
A5_NEW = (
'function drawLeifiteFox9e(ctx,r,ts,leiFct){\n'
'  const bob=Math.sin(ts*0.3594)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fafafa");g.addColorStop(0.45+leiFct*0.35,"#8b5cf6");g.addColorStop(1,"#3730a3");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(leiFct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(139,92,246,"+(leiFct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=leiFct>0.88?"#c4b5fd":"#fafafa";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(leiFct>0.88?"💜":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLiroconiteOrb9e(ctx,r,ts,lirPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3598);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+lirPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.35+lirPct*0.35,"#059669");g.addColorStop(1,"#064e3b");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+lirPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(5,150,105,"+(0.45+lirPct*0.55)+")";ctx.lineWidth=3.5+lirPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(lirPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(52,211,153,"+(lirPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=lirPct>0.88?"#34d399":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(lirPct>0.88?"💚":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLawsoniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="lawsonite_fox9e"){'
A6_NEW = (
'else if(t.type==="leifite_fox9e"){\n'
'      const leiFct=Math.min(1,(ts-t.born)/2800);t._leiFct=leiFct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLeifiteFox9e(ctx,t.radius,ts,leiFct);ctx.restore();\n'
'    } else if(t.type==="liroconite_orb9e"){\n'
'      const lirPct=Math.min(1,(ts-t.born)/2800);t._lirPct=lirPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLiroconiteOrb9e(ctx,t.radius,ts,lirPct);ctx.restore();\n'
'    } else if(t.type==="lawsonite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="lawsonite_fox9e"){'
A7_NEW = (
'if(hit.type==="leifite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(298*(hit._leiFct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#8b5cf6",1938);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("leifite_fox9e_tap");\n'
'        if((hit._leiFct||0)>0.88)unlock("leifite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="liroconite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(293*(hit._lirPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#059669",1940);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("liroconite_orb9e_tap");\n'
'        if((hit._lirPct||0)>0.88)unlock("liroconite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="lawsonite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="lawsonite_fox9e";color="#0891b2";glow="#f0f9ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="leadhillite_orb9e"')
A8_NEW = ('      type="leifite_fox9e";color="#8b5cf6";glow="#fafafa";\n'
           '    } else if('+COND100F+'){\n'
           '      type="liroconite_orb9e";color="#059669";glow="#ecfdf5";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lawsonite_fox9e";color="#0891b2";glow="#f0f9ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="leadhillite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="lawsonite_fox9e"?BASE_R*1.22:type==="leadhillite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="leifite_fox9e"?BASE_R*1.22:type==="liroconite_orb9e"?BASE_R*1.21:type==="lawsonite_fox9e"?BASE_R*1.22:type==="leadhillite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'GALAXY_WAVE41:"🌌💠",VOID_WAVE41:"🕳️💠",'
A10_NEW = 'GALAXY_WAVE41:"🌌💠",VOID_WAVE41:"🕳️💠",CORONA_WAVE41:"🌞💠",ECLIPSE_WAVE41:"🌑💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 657 done! +{len(src)-original_len} bytes")
