#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"arrojadite_orb9e_peak", label:"Arrojadite Orb Peak", desc:"Hit Arrojadite Orb at peak glow", icon:"🍀", xp:150 },'
A1_NEW = (
    '  { id:"arrojadite_orb9e_peak", label:"Arrojadite Orb Peak", desc:"Hit Arrojadite Orb at peak glow", icon:"🍀", xp:150 },\n'
    '  { id:"volt_glow44_use", label:"Volt Glow", desc:"Activate VOLT_GLOW44 power-up", icon:"⚡", xp:65 },\n'
    '  { id:"volt_glow44_max", label:"Volt Master", desc:"Reach max score with VOLT_GLOW44 active", icon:"🔋", xp:130 },\n'
    '  { id:"azure_glow44_use", label:"Azure Glow", desc:"Activate AZURE_GLOW44 power-up", icon:"🔵", xp:65 },\n'
    '  { id:"azure_glow44_max", label:"Azure Master", desc:"Reach max score with AZURE_GLOW44 active", icon:"🌊", xp:130 },\n'
    '  { id:"astrophyllite_fox9e_tap", label:"Astrophyllite Fox", desc:"Tap an Astrophyllite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"astrophyllite_fox9e_peak", label:"Astrophyllite Fox Peak", desc:"Hit Astrophyllite Fox at peak glow", icon:"🌟", xp:150 },\n'
    '  { id:"attakolite_orb9e_tap", label:"Attakolite Orb", desc:"Tap an Attakolite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"attakolite_orb9e_peak", label:"Attakolite Orb Peak", desc:"Hit Attakolite Orb at peak glow", icon:"💛", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"MAGMA_GLOW44","QUARTZ_GLOW44","EMBER_GLOW44","PLASMA_GLOW44","THUNDER_GLOW44"'
A2_NEW = '"VOLT_GLOW44","AZURE_GLOW44","MAGMA_GLOW44","QUARTZ_GLOW44","EMBER_GLOW44","PLASMA_GLOW44","THUNDER_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="MAGMA_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="VOLT_GLOW44"){\n'
    '    gs.score+=2388;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2098,text:"+2388",color:"#facc15",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#facc15",life:0.7});\n'
    '    sfx("powerUp");unlock("volt_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("volt_glow44_max");\n'
    '  } else if(ptype==="AZURE_GLOW44"){\n'
    '    gs.score+=2390;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2100,text:"+2390",color:"#2563eb",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#2563eb",life:0.7});\n'
    '    sfx("powerUp");unlock("azure_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("azure_glow44_max");\n'
    '  } else if(ptype==="MAGMA_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // MAGMA_GLOW44 — +2384 magma glow bonus'
A4_NEW = (
    '  // VOLT_GLOW44 — +2388 volt glow bonus\n'
    '  // AZURE_GLOW44 — +2390 azure glow bonus\n'
    '  // MAGMA_GLOW44 — +2384 magma glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawArgyroditeFox9e('
A5_NEW = (
    'function drawAstrophylliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4147)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fde68a");g.addColorStop(0.45+sp*0.35,"#b45309");g.addColorStop(1,"#78350f");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(180,83,9,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#78350f":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌟":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAttakoliteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4151);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef08a");g.addColorStop(0.35+tp*0.35,"#ca8a04");g.addColorStop(1,"#854d0e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(202,138,4,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(202,138,4,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#ca8a04":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💛":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawArgyroditeFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="argyrodite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="astrophyllite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2234);\n'
    '    drawAstrophylliteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="attakolite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2236);\n'
    '    drawAttakoliteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="argyrodite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="argyrodite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="astrophyllite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(446*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🌟":""),color:"#b45309",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#b45309",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("astrophyllite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("astrophyllite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="attakolite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(441*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 💛":""),color:"#ca8a04",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#ca8a04",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("attakolite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("attakolite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="argyrodite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="argyrodite_fox9e";color="#1c1917";glow="#fafaf9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="arrojadite_orb9e"')
A8_NEW = (
    '      type="astrophyllite_fox9e";color="#b45309";glow="#fffbeb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="attakolite_orb9e";color="#ca8a04";glow="#fefce8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="argyrodite_fox9e";color="#1c1917";glow="#fafaf9";\n'
    '    } else if('+COND100F+'){\n'
    '      type="arrojadite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="argyrodite_fox9e"?BASE_R*1.75:type==="arrojadite_orb9e"?BASE_R*1.74:'
A9_NEW = 'type==="astrophyllite_fox9e"?BASE_R*1.76:type==="attakolite_orb9e"?BASE_R*1.75:type==="argyrodite_fox9e"?BASE_R*1.75:type==="arrojadite_orb9e"?BASE_R*1.74:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'MAGMA_GLOW44:"🌋✨",QUARTZ_GLOW44:"💎✨",EMBER_GLOW44:"🔥✨"'
A10_NEW = 'VOLT_GLOW44:"⚡✨",AZURE_GLOW44:"🔵✨",MAGMA_GLOW44:"🌋✨",QUARTZ_GLOW44:"💎✨",EMBER_GLOW44:"🔥✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 731 done! +{len(src)-orig_len} bytes")
