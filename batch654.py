import re

SRC = "src/NexusTap.jsx"
with open(SRC, encoding="utf-8") as f:
    src = f.read()
original_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1 ── 8 achievements ─────────────────────────────────────────────────
A1_OLD = '{ id:"kaersutite_orb9e_peak", label:"Kaersutite Orb Peak", desc:"Reach peak with Kaersutite Orb", icon:"🔮", xp:120 },'
A1_NEW = (A1_OLD + '\n'
'  { id:"crystal_wave41_use", label:"Crystal Wave", desc:"Activate CRYSTAL_WAVE41 power-up", icon:"💎", xp:60 },\n'
'  { id:"crystal_wave41_max", label:"Crystal Waver", desc:"Reach max with CRYSTAL_WAVE41 active", icon:"💎", xp:120 },\n'
'  { id:"prism_wave41_use", label:"Prism Wave", desc:"Activate PRISM_WAVE41 power-up", icon:"🔮", xp:60 },\n'
'  { id:"prism_wave41_max", label:"Prism Waver", desc:"Reach max with PRISM_WAVE41 active", icon:"🔮", xp:120 },\n'
'  { id:"kernite_fox9e_tap", label:"Kernite Fox", desc:"Tap a Kernite Fox target", icon:"🦊", xp:60 },\n'
'  { id:"kernite_fox9e_peak", label:"Kernite Fox Peak", desc:"Reach peak with Kernite Fox", icon:"🦊", xp:120 },\n'
'  { id:"kinoite_orb9e_tap", label:"Kinoite Orb", desc:"Tap a Kinoite Orb target", icon:"🔮", xp:60 },\n'
'  { id:"kinoite_orb9e_peak", label:"Kinoite Orb Peak", desc:"Reach peak with Kinoite Orb", icon:"🔮", xp:120 },')
assert src.count(A1_OLD) == 1, f"Step 1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── Step 2 ── power-up list ───────────────────────────────────────────────────
A2_OLD = '"COMET_WAVE41","ECHO_WAVE41","PRISM_PULSE41"'
A2_NEW = '"COMET_WAVE41","ECHO_WAVE41","CRYSTAL_WAVE41","PRISM_WAVE41","PRISM_PULSE41"'
assert src.count(A2_OLD) == 1, f"Step 2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── Step 3 ── power-up else-if handler ───────────────────────────────────────
A3_OLD = '} else if(ptype==="COMET_WAVE41"){'
A3_NEW = (
'} else if(ptype==="CRYSTAL_WAVE41"){\n'
'        gs.score+=2080;showPopup(cx,cy-1790,"+2080 💎",theme.accent,26);spawnShockwave(cx,cy,"#0a03c4",1952);if(gs.score>=bonusTotal)unlock("crystal_wave41_max");\n'
'      } else if(ptype==="PRISM_WAVE41"){\n'
'        gs.score+=2082;showPopup(cx,cy-1792,"+2082 🔮",theme.accent,26);spawnShockwave(cx,cy,"#0a0898",1954);if(gs.score>=bonusTotal)unlock("prism_wave41_max");\n'
'      } else if(ptype==="COMET_WAVE41"){'
)
assert src.count(A3_OLD) == 1, f"Step 3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── Step 4 ── power-up sfx + unlock ──────────────────────────────────────────
A4_OLD = '// COMET_WAVE41 — +2076 comet wave bonus'
A4_NEW = ('// CRYSTAL_WAVE41 — +2080 crystal wave bonus\n'
'      if(ptype==="CRYSTAL_WAVE41"){sfx("powerUp",1743);unlock("crystal_wave41_use");}\n'
'      // PRISM_WAVE41 — +2082 prism wave bonus\n'
'      if(ptype==="PRISM_WAVE41"){sfx("powerUp",1745);unlock("prism_wave41_use");}\n'
'      // COMET_WAVE41 — +2076 comet wave bonus')
assert src.count(A4_OLD) == 1, f"Step 4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── Step 5 ── two draw functions ──────────────────────────────────────────────
A5_OLD = 'function drawJulgolditeFox9e('
A5_NEW = (
'function drawKerniteFox9e(ctx,r,ts,kerPct){\n'
'  const bob=Math.sin(ts*0.3570)*r*0.07;\n'
'  ctx.save();ctx.translate(0,bob);\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+kerPct*0.35,"#cbd5e1");g.addColorStop(1,"#475569");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  if(kerPct>0.65){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(203,213,225,"+(kerPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
'  ctx.fillStyle=kerPct>0.88?"#e2e8f0":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(kerPct>0.88?"🤍":"🦊",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawKinoiteOrb9e(ctx,r,ts,kinPct){\n'
'  const pulse=0.72+0.28*Math.sin(ts*0.3574);\n'
'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+kinPct*0.27;\n'
'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
'  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.35+kinPct*0.35,"#0369a1");g.addColorStop(1,"#0c4a6e");\n'
'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
'  const ring=r*(0.54+kinPct*0.42);\n'
'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
'  ctx.strokeStyle="rgba(3,105,161,"+(0.45+kinPct*0.55)+")";ctx.lineWidth=3.5+kinPct*3;ctx.stroke();\n'
'  ctx.globalAlpha=1;\n'
'  if(kinPct>0.82){\n'
'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
'    ctx.strokeStyle="rgba(56,189,248,"+(kinPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
'  ctx.fillStyle=kinPct>0.88?"#38bdf8":"#e0f2fe";ctx.font=(r*0.56)+"px serif";\n'
'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(kinPct>0.88?"💙":"🔮",0,1);\n'
'  ctx.restore();\n'
'}\n'
'function drawJulgolditeFox9e('
)
assert src.count(A5_OLD) == 1, f"Step 5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── Step 6 ── draw dispatch ───────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="julgoldite_fox9e"){'
A6_NEW = (
'else if(t.type==="kernite_fox9e"){\n'
'      const kerPct=Math.min(1,(ts-t.born)/2800);t._kerPct=kerPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawKerniteFox9e(ctx,t.radius,ts,kerPct);ctx.restore();\n'
'    } else if(t.type==="kinoite_orb9e"){\n'
'      const kinPct=Math.min(1,(ts-t.born)/2800);t._kinPct=kinPct;\n'
'      ctx.save();ctx.translate(t.x,t.y);drawKinoiteOrb9e(ctx,t.radius,ts,kinPct);ctx.restore();\n'
'    } else if(t.type==="julgoldite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step 6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── Step 7 ── handleTap ───────────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="julgoldite_fox9e"){'
A7_NEW = (
'if(hit.type==="kernite_fox9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(292*(hit._kerPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#cbd5e1",1926);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🦊",theme.accent,22);\n'
'        unlock("kernite_fox9e_tap");\n'
'        if((hit._kerPct||0)>0.88)unlock("kernite_fox9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="kinoite_orb9e"){\n'
'        targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);\n'
'        const combo=gs.streak+1;const pts=Math.round(287*(hit._kinPct||0.5)*combo);\n'
'        gs.score+=pts;gs.streak++;gs.lastTapTime=Date.now();\n'
'        spawnShockwave(hit.x,hit.y,"#0369a1",1928);\n'
'        spawnPopup(hit.x,hit.y-28,"+"+pts+" 🔮",theme.accent,22);\n'
'        unlock("kinoite_orb9e_tap");\n'
'        if((hit._kinPct||0)>0.88)unlock("kinoite_orb9e_peak");\n'
'        updateMissions({type:"special_tap"});debounceSave();return;\n'
'      } if(hit.type==="julgoldite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step 7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── Step 8 ── spawnTarget ─────────────────────────────────────────────────────
A8_OLD = ('      type="julgoldite_fox9e";color="#065f46";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kaersutite_orb9e"')
A8_NEW = ('      type="kernite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kinoite_orb9e";color="#0369a1";glow="#e0f2fe";\n'
           '    } else if('+COND100F+'){\n'
           '      type="julgoldite_fox9e";color="#065f46";glow="#f0fdf4";\n'
           '    } else if('+COND100F+'){\n'
           '      type="kaersutite_orb9e"')
assert src.count(A8_OLD) == 1, f"Step 8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── Step 9 ── radius table ────────────────────────────────────────────────────
A9_OLD = 'type==="julgoldite_fox9e"?BASE_R*1.22:type==="kaersutite_orb9e"?BASE_R*1.21:'
A9_NEW = 'type==="kernite_fox9e"?BASE_R*1.22:type==="kinoite_orb9e"?BASE_R*1.21:type==="julgoldite_fox9e"?BASE_R*1.22:type==="kaersutite_orb9e"?BASE_R*1.21:'
assert src.count(A9_OLD) == 1, f"Step 9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── Step 10 ── icon map (appears twice) ──────────────────────────────────────
A10_OLD = 'COMET_WAVE41:"☄️💠",ECHO_WAVE41:"📣💠",'
A10_NEW = 'COMET_WAVE41:"☄️💠",ECHO_WAVE41:"📣💠",CRYSTAL_WAVE41:"💎💠",PRISM_WAVE41:"🔮💠",'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open(SRC, "w", encoding="utf-8") as f:
    f.write(src)
print(f"Batch 654 done! +{len(src)-original_len} bytes")
