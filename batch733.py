#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"azurmalachite_orb9e_peak", label:"Azurmalachite Orb Peak", desc:"Hit Azurmalachite Orb at peak glow", icon:"🌊", xp:150 },'
A1_NEW = (
    '  { id:"azurmalachite_orb9e_peak", label:"Azurmalachite Orb Peak", desc:"Hit Azurmalachite Orb at peak glow", icon:"🌊", xp:150 },\n'
    '  { id:"sapphire_glow44_use", label:"Sapphire Glow", desc:"Activate SAPPHIRE_GLOW44 power-up", icon:"💙", xp:65 },\n'
    '  { id:"sapphire_glow44_max", label:"Sapphire Master", desc:"Reach max score with SAPPHIRE_GLOW44 active", icon:"🔷", xp:130 },\n'
    '  { id:"emerald_glow44_use", label:"Emerald Glow", desc:"Activate EMERALD_GLOW44 power-up", icon:"💚", xp:65 },\n'
    '  { id:"emerald_glow44_max", label:"Emerald Master", desc:"Reach max score with EMERALD_GLOW44 active", icon:"🟢", xp:130 },\n'
    '  { id:"babingtonite_fox9e_tap", label:"Babingtonite Fox", desc:"Tap a Babingtonite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"babingtonite_fox9e_peak", label:"Babingtonite Fox Peak", desc:"Hit Babingtonite Fox at peak glow", icon:"🌲", xp:150 },\n'
    '  { id:"bertrandite_orb9e_tap", label:"Bertrandite Orb", desc:"Tap a Bertrandite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"bertrandite_orb9e_peak", label:"Bertrandite Orb Peak", desc:"Hit Bertrandite Orb at peak glow", icon:"🌼", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"JADE_GLOW44","RUBY_GLOW44","VOLT_GLOW44","AZURE_GLOW44","MAGMA_GLOW44"'
A2_NEW = '"SAPPHIRE_GLOW44","EMERALD_GLOW44","JADE_GLOW44","RUBY_GLOW44","VOLT_GLOW44","AZURE_GLOW44","MAGMA_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="JADE_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="SAPPHIRE_GLOW44"){\n'
    '    gs.score+=2396;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2106,text:"+2396",color:"#1d4ed8",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#1d4ed8",life:0.7});\n'
    '    sfx("powerUp");unlock("sapphire_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("sapphire_glow44_max");\n'
    '  } else if(ptype==="EMERALD_GLOW44"){\n'
    '    gs.score+=2398;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2108,text:"+2398",color:"#047857",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#047857",life:0.7});\n'
    '    sfx("powerUp");unlock("emerald_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("emerald_glow44_max");\n'
    '  } else if(ptype==="JADE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // JADE_GLOW44 — +2392 jade glow bonus'
A4_NEW = (
    '  // SAPPHIRE_GLOW44 — +2396 sapphire glow bonus\n'
    '  // EMERALD_GLOW44 — +2398 emerald glow bonus\n'
    '  // JADE_GLOW44 — +2392 jade glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAugeliteFox9e('
A5_NEW = (
    'function drawBabingtoniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4159)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#6ee7b7");g.addColorStop(0.45+sp*0.35,"#065f46");g.addColorStop(1,"#022c22");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(6,95,70,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#022c22":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌲":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBertranditeOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4163);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+tp*0.35,"#d97706");g.addColorStop(1,"#92400e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(217,119,6,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#d97706":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌼":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAugeliteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="augelite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="babingtonite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2242);\n'
    '    drawBabingtoniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="bertrandite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2244);\n'
    '    drawBertranditeOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="augelite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="augelite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="babingtonite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(450*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🌲":""),color:"#065f46",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#065f46",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("babingtonite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("babingtonite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="bertrandite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(445*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🌼":""),color:"#d97706",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#d97706",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("bertrandite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("bertrandite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="augelite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="augelite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="azurmalachite_orb9e"')
A8_NEW = (
    '      type="babingtonite_fox9e";color="#065f46";glow="#ecfdf5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bertrandite_orb9e";color="#d97706";glow="#fffbeb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="augelite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="azurmalachite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="augelite_fox9e"?BASE_R*1.77:type==="azurmalachite_orb9e"?BASE_R*1.76:'
A9_NEW = 'type==="babingtonite_fox9e"?BASE_R*1.78:type==="bertrandite_orb9e"?BASE_R*1.77:type==="augelite_fox9e"?BASE_R*1.77:type==="azurmalachite_orb9e"?BASE_R*1.76:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'JADE_GLOW44:"💚✨",RUBY_GLOW44:"❤️✨",VOLT_GLOW44:"⚡✨"'
A10_NEW = 'SAPPHIRE_GLOW44:"💙✨",EMERALD_GLOW44:"💚✨",JADE_GLOW44:"💚✨",RUBY_GLOW44:"❤️✨",VOLT_GLOW44:"⚡✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 733 done! +{len(src)-orig_len} bytes")
