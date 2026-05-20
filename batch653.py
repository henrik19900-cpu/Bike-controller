import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"johannsenite_orb9e_peak", label:"Johannsenite Orb Peak", desc:"Reach peak with Johannsenite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"comet_wave41_use", label:"Comet Wave", desc:"Activate COMET_WAVE41 power-up", icon:"☄️", xp:60 },\n'
'  { id:"comet_wave41_max", label:"Comet Waver", desc:"Reach max with COMET_WAVE41 active", icon:"☄️", xp:120 },\n'
'  { id:"echo_wave41_use", label:"Echo Wave", desc:"Activate ECHO_WAVE41 power-up", icon:"📣", xp:60 },\n'
'  { id:"echo_wave41_max", label:"Echo Waver", desc:"Reach max with ECHO_WAVE41 active", icon:"📣", xp:120 },\n'
'  { id:"julgoldite_fox9e_tap", label:"Julgoldite Fox", desc:"Tap a Julgoldite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"julgoldite_fox9e_peak", label:"Julgoldite Fox Peak", desc:"Reach peak with Julgoldite Fox", icon:"🦊", xp:120 },\n'
'  { id:"kaersutite_orb9e_tap", label:"Kaersutite Orb", desc:"Tap a Kaersutite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"kaersutite_orb9e_peak", label:"Kaersutite Orb Peak", desc:"Reach peak with Kaersutite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"STORM_WAVE41","NOVA_WAVE41","PRISM_PULSE41"'
A2_NEW = '"STORM_WAVE41","NOVA_WAVE41","COMET_WAVE41","ECHO_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="STORM_WAVE41"){'
A3_NEW = (
'} else if(ptype==="COMET_WAVE41"){\n'
'        gs.score+=2076;showPopup(cx,cy-1786,"+2076 ☄️",theme.accent,26);spawnShockwave(cx,cy,"#0a03c2",1948);if(gs.score>=bonusTotal)unlock("comet_wave41_max");\n'
'      } else if(ptype==="ECHO_WAVE41"){\n'
'        gs.score+=2078;showPopup(cx,cy-1788,"+2078 📣",theme.accent,26);spawnShockwave(cx,cy,"#0a0896",1950);if(gs.score>=bonusTotal)unlock("echo_wave41_max");\n'
'      } else if(ptype==="STORM_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// STORM_WAVE41 — +2072 storm wave bonus'
A4_NEW = ('// COMET_WAVE41 — +2076 comet wave bonus\n'
'      if(ptype==="COMET_WAVE41"){sfx("powerUp",1739);unlock("comet_wave41_use");}\n'
'      // ECHO_WAVE41 — +2078 echo wave bonus\n'
'      if(ptype==="ECHO_WAVE41"){sfx("powerUp",1741);unlock("echo_wave41_use");}\n'
'      // STORM_WAVE41 — +2072 storm wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawIridosmineFox9e('
A5_NEW = (
'function drawJulgolditeFox9e(ctx,r,ts,julPct){\n'
'  const bob=Math.sin(ts*0.3562)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+julPct*0.35,"#065f46");g.addColorStop(1,"#022c22");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(julPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(6,95,70,"+(julPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=julPct>0.88?"#34d399":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(julPct>0.88?"🌿":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawKaersutiteOrb9e(ctx,r,ts,kaePct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3566);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+kaePct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#fef2f2");g.addColorStop(0.35+kaePct*0.35,"#7f1d1d");g.addColorStop(1,"#3f0000");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+kaePct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(127,29,29,"+(0.45+kaePct*0.55)+")";ctx.lineWidth=3.5+kaePct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(kaePct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(252,165,165,"+(kaePct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=kaePct>0.88?"#fca5a5":"#fef2f2";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(kaePct>0.88?"🩸":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawIridosmineFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="iridosmine_fox9e"){'
A6_NEW = (
'else if(t.type==="julgoldite_fox9e"){\n'
'      const julPct=Math.min(1,(ts-t.born)/2800);t._julPct=julPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawJulgolditeFox9e(ctx,t.radius,ts,julPct);ctx.restore();\n'
'    } else if(t.type==="kaersutite_orb9e"){\n'
'      const kaePct=Math.min(1,(ts-t.born)/2800);t._kaePct=kaePct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawKaersutiteOrb9e(ctx,t.radius,ts,kaePct);ctx.restore();\n'
'    } else if(t.type==="iridosmine_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="iridosmine_fox9e"){'
A7_NEW = (
'if(hit.type==="julgoldite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(290*(hit._julPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#065f46",1922);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("julgoldite_fox9e_tap");\n'
'        if((hit._julPct||0)>0.88)unlock("julgoldite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="kaersutite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(285*(hit._kaePct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#7f1d1d",1924);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("kaersutite_orb9e_tap");\n'
'        if((hit._kaePct||0)>0.88)unlock("kaersutite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="iridosmine_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="iridosmine_fox9e";color="#94a3b8";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="johannsenite_orb9e"')
A8_NEW = ('      type="julgoldite_fox9e";color="#065f46";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kaersutite_orb9e";color="#7f1d1d";glow="#fef2f2";\n'
           '    } else if('+COND100F+'){\n'
           '      type="iridosmine_fox9e";color="#94a3b8";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="johannsenite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="iridosmine_fox9e"?BASE_R*1.22:type==="johannsenite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="julgoldite_fox9e"?BASE_R*1.22:type==="kaersutite_orb9e"?BASE_R*1.21:type==="iridosmine_fox9e"?BASE_R*1.22:type==="johannsenite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'STORM_WAVE41:"⛈️💠",NOVA_WAVE41:"💥💠",'
A10_NEW = 'STORM_WAVE41:"⛈️💠",NOVA_WAVE41:"💥💠",COMET_WAVE41:"☄️💠",ECHO_WAVE41:"📣💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 653 done! +{len(src)-original_len} bytes")
