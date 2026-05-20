#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"argentite_orb9e_peak", label:"Argentite Orb Peak", desc:"Hit Argentite Orb at peak glow", icon:"🪙", xp:150 },'
A1_NEW = (
    '  { id:"argentite_orb9e_peak", label:"Argentite Orb Peak", desc:"Hit Argentite Orb at peak glow", icon:"🪙", xp:150 },\n'
    '  { id:"magma_glow44_use", label:"Magma Glow", desc:"Activate MAGMA_GLOW44 power-up", icon:"🌋", xp:65 },\n'
    '  { id:"magma_glow44_max", label:"Magma Master", desc:"Reach max score with MAGMA_GLOW44 active", icon:"🔥", xp:130 },\n'
    '  { id:"quartz_glow44_use", label:"Quartz Glow", desc:"Activate QUARTZ_GLOW44 power-up", icon:"💎", xp:65 },\n'
    '  { id:"quartz_glow44_max", label:"Quartz Master", desc:"Reach max score with QUARTZ_GLOW44 active", icon:"🔮", xp:130 },\n'
    '  { id:"argyrodite_fox9e_tap", label:"Argyrodite Fox", desc:"Tap an Argyrodite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"argyrodite_fox9e_peak", label:"Argyrodite Fox Peak", desc:"Hit Argyrodite Fox at peak glow", icon:"⬛", xp:150 },\n'
    '  { id:"arrojadite_orb9e_tap", label:"Arrojadite Orb", desc:"Tap an Arrojadite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"arrojadite_orb9e_peak", label:"Arrojadite Orb Peak", desc:"Hit Arrojadite Orb at peak glow", icon:"🍀", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"EMBER_GLOW44","PLASMA_GLOW44","THUNDER_GLOW44","FROST_GLOW44","NEBULA_GLOW44"'
A2_NEW = '"MAGMA_GLOW44","QUARTZ_GLOW44","EMBER_GLOW44","PLASMA_GLOW44","THUNDER_GLOW44","FROST_GLOW44","NEBULA_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="EMBER_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="MAGMA_GLOW44"){\n'
    '    gs.score+=2384;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2094,text:"+2384",color:"#ef4444",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#ef4444",life:0.7});\n'
    '    sfx("powerUp");unlock("magma_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("magma_glow44_max");\n'
    '  } else if(ptype==="QUARTZ_GLOW44"){\n'
    '    gs.score+=2386;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2096,text:"+2386",color:"#e879f9",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#e879f9",life:0.7});\n'
    '    sfx("powerUp");unlock("quartz_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("quartz_glow44_max");\n'
    '  } else if(ptype==="EMBER_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // EMBER_GLOW44 — +2380 ember glow bonus'
A4_NEW = (
    '  // MAGMA_GLOW44 — +2384 magma glow bonus\n'
    '  // QUARTZ_GLOW44 — +2386 quartz glow bonus\n'
    '  // EMBER_GLOW44 — +2380 ember glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawArfvedsoniteFox9e('
A5_NEW = (
    'function drawArgyroditeFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4141)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#78716c");g.addColorStop(0.45+sp*0.35,"#1c1917");g.addColorStop(1,"#0c0a09");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(28,25,23,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0c0a09":"#fafaf9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"⬛":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawArrojaditeOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4143);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#4ade80");g.addColorStop(0.35+tp*0.35,"#166534");g.addColorStop(1,"#052e16");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(22,101,52,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,101,52,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#166534":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🍀":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawArfvedsoniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="arfvedsonite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="argyrodite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2230);\n'
    '    drawArgyroditeFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="arrojadite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2232);\n'
    '    drawArrojaditeOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="arfvedsonite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="arfvedsonite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="argyrodite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(444*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" ⬛":""),color:"#1c1917",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#1c1917",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("argyrodite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("argyrodite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="arrojadite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(439*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🍀":""),color:"#166534",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#166534",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("arrojadite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("arrojadite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="arfvedsonite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="arfvedsonite_fox9e";color="#111827";glow="#f9fafb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="argentite_orb9e"')
A8_NEW = (
    '      type="argyrodite_fox9e";color="#1c1917";glow="#fafaf9";\n'
    '    } else if('+COND100F+'){\n'
    '      type="arrojadite_orb9e";color="#166534";glow="#f0fdf4";\n'
    '    } else if('+COND100F+'){\n'
    '      type="arfvedsonite_fox9e";color="#111827";glow="#f9fafb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="argentite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="arfvedsonite_fox9e"?BASE_R*1.74:type==="argentite_orb9e"?BASE_R*1.73:'
A9_NEW = 'type==="argyrodite_fox9e"?BASE_R*1.75:type==="arrojadite_orb9e"?BASE_R*1.74:type==="arfvedsonite_fox9e"?BASE_R*1.74:type==="argentite_orb9e"?BASE_R*1.73:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'EMBER_GLOW44:"🔥✨",PLASMA_GLOW44:"⚛️✨",THUNDER_GLOW44:"⚡✨"'
A10_NEW = 'MAGMA_GLOW44:"🌋✨",QUARTZ_GLOW44:"💎✨",EMBER_GLOW44:"🔥✨",PLASMA_GLOW44:"⚛️✨",THUNDER_GLOW44:"⚡✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 730 done! +{len(src)-orig_len} bytes")
