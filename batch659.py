import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"lorenzenite_orb9e_peak", label:"Lorenzenite Orb Peak", desc:"Reach peak with Lorenzenite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"radiance_wave41_use", label:"Radiance Wave", desc:"Activate RADIANCE_WAVE41 power-up", icon:"✨", xp:60 },\n'
'  { id:"radiance_wave41_max", label:"Radiance Waver", desc:"Reach max with RADIANCE_WAVE41 active", icon:"✨", xp:120 },\n'
'  { id:"void_pulse41_use", label:"Void Pulse", desc:"Activate VOID_PULSE41 power-up", icon:"🌑", xp:60 },\n'
'  { id:"void_pulse41_max", label:"Void Pulser", desc:"Reach max with VOID_PULSE41 active", icon:"🌑", xp:120 },\n'
'  { id:"loseyite_fox9e_tap", label:"Loseyite Fox", desc:"Tap a Loseyite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"loseyite_fox9e_peak", label:"Loseyite Fox Peak", desc:"Reach peak with Loseyite Fox", icon:"🦊", xp:120 },\n'
'  { id:"ludlamite_orb9e_tap", label:"Ludlamite Orb", desc:"Tap a Ludlamite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"ludlamite_orb9e_peak", label:"Ludlamite Orb Peak", desc:"Reach peak with Ludlamite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"PULSAR_WAVE41","QUASAR_WAVE41","PRISM_PULSE41"'
A2_NEW = '"PULSAR_WAVE41","QUASAR_WAVE41","RADIANCE_WAVE41","VOID_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="PULSAR_WAVE41"){'
A3_NEW = (
'} else if(ptype==="RADIANCE_WAVE41"){\n'
'        gs.score+=2100;showPopup(cx,cy-1810,"+2100 ✨",theme.accent,26);spawnShockwave(cx,cy,"#0a03ce",1972);if(gs.score>=bonusTotal)unlock("radiance_wave41_max");\n'
'      } else if(ptype==="VOID_PULSE41"){\n'
'        gs.score+=2102;showPopup(cx,cy-1812,"+2102 🌑",theme.accent,26);spawnShockwave(cx,cy,"#0a08a2",1974);if(gs.score>=bonusTotal)unlock("void_pulse41_max");\n'
'      } else if(ptype==="PULSAR_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// PULSAR_WAVE41 — +2096 pulsar wave bonus'
A4_NEW = ('// RADIANCE_WAVE41 — +2100 radiance wave bonus\n'
'      if(ptype==="RADIANCE_WAVE41"){sfx("powerUp",1763);unlock("radiance_wave41_use");}\n'
'      // VOID_PULSE41 — +2102 void pulse bonus\n'
'      if(ptype==="VOID_PULSE41"){sfx("powerUp",1765);unlock("void_pulse41_use");}\n'
'      // PULSAR_WAVE41 — +2096 pulsar wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawLollingiteFox9e('
A5_NEW = (
'function drawLoseyiteFox9e(ctx,r,ts,losPct){\n'
'  const bob=Math.sin(ts*0.3610)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f9fafb");g.addColorStop(0.45+losPct*0.35,"#9ca3af");g.addColorStop(1,"#374151");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(losPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(156,163,175,"+(losPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=losPct>0.88?"#d1d5db":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(losPct>0.88?"🌫️":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLudlamiteOrb9e(ctx,r,ts,ludPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3614);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ludPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+ludPct*0.35,"#22c55e");g.addColorStop(1,"#14532d");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+ludPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(34,197,94,"+(0.45+ludPct*0.55)+")";ctx.lineWidth=3.5+ludPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(ludPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(134,239,172,"+(ludPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=ludPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ludPct>0.88?"🍀":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawLollingiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="lollingite_fox9e"){'
A6_NEW = (
'else if(t.type==="loseyite_fox9e"){\n'
'      const losPct=Math.min(1,(ts-t.born)/2800);t._losPct=losPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLoseyiteFox9e(ctx,t.radius,ts,losPct);ctx.restore();\n'
'    } else if(t.type==="ludlamite_orb9e"){\n'
'      const ludPct=Math.min(1,(ts-t.born)/2800);t._ludPct=ludPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawLudlamiteOrb9e(ctx,t.radius,ts,ludPct);ctx.restore();\n'
'    } else if(t.type==="lollingite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="lollingite_fox9e"){'
A7_NEW = (
'if(hit.type==="loseyite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(302*(hit._losPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#9ca3af",1946);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("loseyite_fox9e_tap");\n'
'        if((hit._losPct||0)>0.88)unlock("loseyite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="ludlamite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(297*(hit._ludPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#22c55e",1948);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("ludlamite_orb9e_tap");\n'
'        if((hit._ludPct||0)>0.88)unlock("ludlamite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="lollingite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="lollingite_fox9e";color="#64748b";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lorenzenite_orb9e"')
A8_NEW = ('      type="loseyite_fox9e";color="#9ca3af";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="ludlamite_orb9e";color="#22c55e";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lollingite_fox9e";color="#64748b";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="lorenzenite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="lollingite_fox9e"?BASE_R*1.22:type==="lorenzenite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="loseyite_fox9e"?BASE_R*1.22:type==="ludlamite_orb9e"?BASE_R*1.21:type==="lollingite_fox9e"?BASE_R*1.22:type==="lorenzenite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'PULSAR_WAVE41:"💫💠",QUASAR_WAVE41:"⭐💠",'
A10_NEW = 'PULSAR_WAVE41:"💫💠",QUASAR_WAVE41:"⭐💠",RADIANCE_WAVE41:"✨💠",VOID_PULSE41:"🌑💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 659 done! +{len(src)-original_len} bytes")
