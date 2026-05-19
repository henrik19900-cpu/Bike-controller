import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"erythrite_orb9e_peak", label:"Erythrite Orb Peak", desc:"Reach peak with Erythrite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"vortex_pulse41_use", label:"Vortex Pulse", desc:"Activate VORTEX_PULSE41 power-up", icon:"🌀", xp:60 },\n'
'  { id:"vortex_pulse41_max", label:"Vortex Pulser", desc:"Reach max with VORTEX_PULSE41 active", icon:"🌀", xp:120 },\n'
'  { id:"radiant_pulse41_use", label:"Radiant Pulse", desc:"Activate RADIANT_PULSE41 power-up", icon:"✨", xp:60 },\n'
'  { id:"radiant_pulse41_max", label:"Radiant Pulser", desc:"Reach max with RADIANT_PULSE41 active", icon:"✨", xp:120 },\n'
'  { id:"euxenite_fox9e_tap", label:"Euxenite Fox", desc:"Tap an Euxenite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"euxenite_fox9e_peak", label:"Euxenite Fox Peak", desc:"Reach peak with Euxenite Fox", icon:"🦊", xp:120 },\n'
'  { id:"fayalite_orb9e_tap", label:"Fayalite Orb", desc:"Tap a Fayalite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"fayalite_orb9e_peak", label:"Fayalite Orb Peak", desc:"Reach peak with Fayalite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"GALAXY_PULSE41","COSMOS_PULSE41","PRISM_PULSE41"'
A2_NEW = '"GALAXY_PULSE41","COSMOS_PULSE41","VORTEX_PULSE41","RADIANT_PULSE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="GALAXY_PULSE41"){'
A3_NEW = (
'} else if(ptype==="VORTEX_PULSE41"){\n'
'        gs.score+=2036;showPopup(cx,cy-1746,"+2036 🌀",theme.accent,26);spawnShockwave(cx,cy,"#0a03ae",1908);if(gs.score>=bonusTotal)unlock("vortex_pulse41_max");\n'
'      } else if(ptype==="RADIANT_PULSE41"){\n'
'        gs.score+=2038;showPopup(cx,cy-1748,"+2038 ✨",theme.accent,26);spawnShockwave(cx,cy,"#0a0882",1910);if(gs.score>=bonusTotal)unlock("radiant_pulse41_max");\n'
'      } else if(ptype==="GALAXY_PULSE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// GALAXY_PULSE41 — +2032 galaxy bonus'
A4_NEW = ('// VORTEX_PULSE41 — +2036 vortex bonus\n'
'      if(ptype==="VORTEX_PULSE41"){sfx("powerUp",1699);unlock("vortex_pulse41_use");}\n'
'      // RADIANT_PULSE41 — +2038 radiant bonus\n'
'      if(ptype==="RADIANT_PULSE41"){sfx("powerUp",1701);unlock("radiant_pulse41_use");}\n'
'      // GALAXY_PULSE41 — +2032 galaxy bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawEnarsiteFox9e('
A5_NEW = (
'function drawEuxeniteFox9e(ctx,r,ts,euxPct){\n'
'  const bob=Math.sin(ts*0.3482)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+euxPct*0.35,"#9d174d");g.addColorStop(1,"#500724");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(euxPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(157,23,77,"+(euxPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=euxPct>0.88?"#fbcfe8":"#fdf2f8";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(euxPct>0.88?"🌸":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawFayaliteOrb9e(ctx,r,ts,fayPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3486);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+fayPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fff7f0");g.addColorStop(0.35+fayPct*0.35,"#b45309");g.addColorStop(1,"#451a03");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+fayPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(180,83,9,"+(0.45+fayPct*0.55)+")";ctx.lineWidth=3.5+fayPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(fayPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(251,191,36,"+(fayPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=fayPct>0.88?"#fcd34d":"#fff7f0";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(fayPct>0.88?"🟡":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawEnarsiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="enarsite_fox9e"){'
A6_NEW = (
'else if(t.type==="euxenite_fox9e"){\n'
'      const euxPct=Math.min(1,(ts-t.born)/2800);t._euxPct=euxPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawEuxeniteFox9e(ctx,t.radius,ts,euxPct);ctx.restore();\n'
'    } else if(t.type==="fayalite_orb9e"){\n'
'      const fayPct=Math.min(1,(ts-t.born)/2800);t._fayPct=fayPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawFayaliteOrb9e(ctx,t.radius,ts,fayPct);ctx.restore();\n'
'    } else if(t.type==="enarsite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="enarsite_fox9e"){'
A7_NEW = (
'if(hit.type==="euxenite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(270*(hit._euxPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#9d174d",1882);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("euxenite_fox9e_tap");\n'
'        if((hit._euxPct||0)>0.88)unlock("euxenite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="fayalite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(265*(hit._fayPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#b45309",1884);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("fayalite_orb9e_tap");\n'
'        if((hit._fayPct||0)>0.88)unlock("fayalite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="enarsite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="enarsite_fox9e";color="#374151";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="erythrite_orb9e"')
A8_NEW = ('      type="euxenite_fox9e";color="#9d174d";glow="#fdf2f8";\n'
           '    } else if('+COND100F+'){\n'
           '      type="fayalite_orb9e";color="#b45309";glow="#fff7f0";\n'
           '    } else if('+COND100F+'){\n'
           '      type="enarsite_fox9e";color="#374151";glow="#f9fafb";\n'
           '    } else if('+COND100F+'){\n'
           '      type="erythrite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="enarsite_fox9e"?BASE_R*1.22:type==="erythrite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="euxenite_fox9e"?BASE_R*1.22:type==="fayalite_orb9e"?BASE_R*1.21:type==="enarsite_fox9e"?BASE_R*1.22:type==="erythrite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'GALAXY_PULSE41:"🌌💠",COSMOS_PULSE41:"🪐💠",'
A10_NEW = 'GALAXY_PULSE41:"🌌💠",COSMOS_PULSE41:"🪐💠",VORTEX_PULSE41:"🌀💠",RADIANT_PULSE41:"✨💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 643 done! +{len(src)-original_len} bytes")
