import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"heazlewoodite_orb9e_peak", label:"Heazlewoodite Orb Peak", desc:"Reach peak with Heazlewoodite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"ionic_wave41_use", label:"Ionic Wave", desc:"Activate IONIC_WAVE41 power-up", icon:"⚗️", xp:60 },\n'
'  { id:"ionic_wave41_max", label:"Ionic Waver", desc:"Reach max with IONIC_WAVE41 active", icon:"⚗️", xp:120 },\n'
'  { id:"lunar_wave41_use", label:"Lunar Wave", desc:"Activate LUNAR_WAVE41 power-up", icon:"🌙", xp:60 },\n'
'  { id:"lunar_wave41_max", label:"Lunar Waver", desc:"Reach max with LUNAR_WAVE41 active", icon:"🌙", xp:120 },\n'
'  { id:"hureaulite_fox9e_tap", label:"Hureaulite Fox", desc:"Tap a Hureaulite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"hureaulite_fox9e_peak", label:"Hureaulite Fox Peak", desc:"Reach peak with Hureaulite Fox", icon:"🦊", xp:120 },\n'
'  { id:"hibonite_orb9e_tap", label:"Hibonite Orb", desc:"Tap a Hibonite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"hibonite_orb9e_peak", label:"Hibonite Orb Peak", desc:"Reach peak with Hibonite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"PHOTON_WAVE41","QUANTUM_WAVE41","PRISM_PULSE41"'
A2_NEW = '"PHOTON_WAVE41","QUANTUM_WAVE41","IONIC_WAVE41","LUNAR_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="PHOTON_WAVE41"){'
A3_NEW = (
'} else if(ptype==="IONIC_WAVE41"){\n'
'        gs.score+=2064;showPopup(cx,cy-1774,"+2064 ⚗️",theme.accent,26);spawnShockwave(cx,cy,"#0a03bc",1936);if(gs.score>=bonusTotal)unlock("ionic_wave41_max");\n'
'      } else if(ptype==="LUNAR_WAVE41"){\n'
'        gs.score+=2066;showPopup(cx,cy-1776,"+2066 🌙",theme.accent,26);spawnShockwave(cx,cy,"#0a0890",1938);if(gs.score>=bonusTotal)unlock("lunar_wave41_max");\n'
'      } else if(ptype==="PHOTON_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// PHOTON_WAVE41 — +2060 photon wave bonus'
A4_NEW = ('// IONIC_WAVE41 — +2064 ionic wave bonus\n'
'      if(ptype==="IONIC_WAVE41"){sfx("powerUp",1727);unlock("ionic_wave41_use");}\n'
'      // LUNAR_WAVE41 — +2066 lunar wave bonus\n'
'      if(ptype==="LUNAR_WAVE41"){sfx("powerUp",1729);unlock("lunar_wave41_use");}\n'
'      // PHOTON_WAVE41 — +2060 photon wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawHayneFox9e('
A5_NEW = (
'function drawHureauliteFox9e(ctx,r,ts,hurPct){\n'
'  const bob=Math.sin(ts*0.3538)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+hurPct*0.35,"#db2777");g.addColorStop(1,"#500724");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(hurPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(219,39,119,"+(hurPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=hurPct>0.88?"#f9a8d4":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(hurPct>0.88?"🌸":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawHiboniteOrb9e(ctx,r,ts,hibPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3542);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+hibPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+hibPct*0.35,"#92400e");g.addColorStop(1,"#451a03");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+hibPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(146,64,14,"+(0.45+hibPct*0.55)+")";ctx.lineWidth=3.5+hibPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(hibPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(253,186,116,"+(hibPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=hibPct>0.88?"#fb923c":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(hibPct>0.88?"🟠":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawHayneFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="hauyne_fox9e"){'
A6_NEW = (
'else if(t.type==="hureaulite_fox9e"){\n'
'      const hurPct=Math.min(1,(ts-t.born)/2800);t._hurPct=hurPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawHureauliteFox9e(ctx,t.radius,ts,hurPct);ctx.restore();\n'
'    } else if(t.type==="hibonite_orb9e"){\n'
'      const hibPct=Math.min(1,(ts-t.born)/2800);t._hibPct=hibPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawHiboniteOrb9e(ctx,t.radius,ts,hibPct);ctx.restore();\n'
'    } else if(t.type==="hauyne_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="hauyne_fox9e"){'
A7_NEW = (
'if(hit.type==="hureaulite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(284*(hit._hurPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#db2777",1910);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("hureaulite_fox9e_tap");\n'
'        if((hit._hurPct||0)>0.88)unlock("hureaulite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="hibonite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(279*(hit._hibPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#92400e",1912);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("hibonite_orb9e_tap");\n'
'        if((hit._hibPct||0)>0.88)unlock("hibonite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="hauyne_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="hauyne_fox9e";color="#2563eb";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="heazlewoodite_orb9e"')
A8_NEW = ('      type="hureaulite_fox9e";color="#db2777";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="hibonite_orb9e";color="#92400e";glow="#fef3c7";\n'
           '    } else if('+COND100F+'){\n'
           '      type="hauyne_fox9e";color="#2563eb";glow="#eff6ff";\n'
           '    } else if('+COND100F+'){\n'
           '      type="heazlewoodite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="hauyne_fox9e"?BASE_R*1.22:type==="heazlewoodite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="hureaulite_fox9e"?BASE_R*1.22:type==="hibonite_orb9e"?BASE_R*1.21:type==="hauyne_fox9e"?BASE_R*1.22:type==="heazlewoodite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'PHOTON_WAVE41:"🌟💠",QUANTUM_WAVE41:"⚛️💠",'
A10_NEW = 'PHOTON_WAVE41:"🌟💠",QUANTUM_WAVE41:"⚛️💠",IONIC_WAVE41:"⚗️💠",LUNAR_WAVE41:"🌙💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 650 done! +{len(src)-original_len} bytes")
