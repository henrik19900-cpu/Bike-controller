#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"antlerite_orb9e_peak", label:"Antlerite Orb Peak", desc:"Hit Antlerite Orb at peak glow", icon:"💚", xp:150 },'
A1_NEW = (
    '  { id:"antlerite_orb9e_peak", label:"Antlerite Orb Peak", desc:"Hit Antlerite Orb at peak glow", icon:"💚", xp:150 },\n'
    '  { id:"ember_glow44_use", label:"Ember Glow", desc:"Activate EMBER_GLOW44 power-up", icon:"🔥", xp:65 },\n'
    '  { id:"ember_glow44_max", label:"Ember Master", desc:"Reach max score with EMBER_GLOW44 active", icon:"🌋", xp:130 },\n'
    '  { id:"plasma_glow44_use", label:"Plasma Glow", desc:"Activate PLASMA_GLOW44 power-up", icon:"⚛️", xp:65 },\n'
    '  { id:"plasma_glow44_max", label:"Plasma Master", desc:"Reach max score with PLASMA_GLOW44 active", icon:"🌐", xp:130 },\n'
    '  { id:"arfvedsonite_fox9e_tap", label:"Arfvedsonite Fox", desc:"Tap an Arfvedsonite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"arfvedsonite_fox9e_peak", label:"Arfvedsonite Fox Peak", desc:"Hit Arfvedsonite Fox at peak glow", icon:"🖤", xp:150 },\n'
    '  { id:"argentite_orb9e_tap", label:"Argentite Orb", desc:"Tap an Argentite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"argentite_orb9e_peak", label:"Argentite Orb Peak", desc:"Hit Argentite Orb at peak glow", icon:"🪙", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"THUNDER_GLOW44","FROST_GLOW44","NEBULA_GLOW44","AURORA_GLOW44","COSMIC_GLOW44"'
A2_NEW = '"EMBER_GLOW44","PLASMA_GLOW44","THUNDER_GLOW44","FROST_GLOW44","NEBULA_GLOW44","AURORA_GLOW44","COSMIC_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="THUNDER_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="EMBER_GLOW44"){\n'
    '    gs.score+=2380;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2090,text:"+2380",color:"#f97316",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#f97316",life:0.7});\n'
    '    sfx("powerUp");unlock("ember_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("ember_glow44_max");\n'
    '  } else if(ptype==="PLASMA_GLOW44"){\n'
    '    gs.score+=2382;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2092,text:"+2382",color:"#ec4899",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#ec4899",life:0.7});\n'
    '    sfx("powerUp");unlock("plasma_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("plasma_glow44_max");\n'
    '  } else if(ptype==="THUNDER_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // THUNDER_GLOW44 — +2376 thunder glow bonus'
A4_NEW = (
    '  // EMBER_GLOW44 — +2380 ember glow bonus\n'
    '  // PLASMA_GLOW44 — +2382 plasma glow bonus\n'
    '  // THUNDER_GLOW44 — +2376 thunder glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAnorthiteFox9e('
A5_NEW = (
    'function drawArfvedsoniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4133)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#6b7280");g.addColorStop(0.45+sp*0.35,"#111827");g.addColorStop(1,"#030712");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(17,24,39,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#030712":"#f9fafb";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🖤":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawArgentiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4137);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.35+tp*0.35,"#94a3b8");g.addColorStop(1,"#475569");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(148,163,184,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🪙":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAnorthiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="anorthite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="arfvedsonite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2226);\n'
    '    drawArfvedsoniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="argentite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2228);\n'
    '    drawArgentiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="anorthite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="anorthite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="arfvedsonite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(442*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🖤":""),color:"#111827",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#111827",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("arfvedsonite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("arfvedsonite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="argentite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(437*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🪙":""),color:"#94a3b8",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#94a3b8",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("argentite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("argentite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="anorthite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="anorthite_fox9e";color="#f1f5f9";glow="#ffffff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="antlerite_orb9e"')
A8_NEW = (
    '      type="arfvedsonite_fox9e";color="#111827";glow="#f9fafb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="argentite_orb9e";color="#94a3b8";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="anorthite_fox9e";color="#f1f5f9";glow="#ffffff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="antlerite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="anorthite_fox9e"?BASE_R*1.73:type==="antlerite_orb9e"?BASE_R*1.72:'
A9_NEW = 'type==="arfvedsonite_fox9e"?BASE_R*1.74:type==="argentite_orb9e"?BASE_R*1.73:type==="anorthite_fox9e"?BASE_R*1.73:type==="antlerite_orb9e"?BASE_R*1.72:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'THUNDER_GLOW44:"⚡✨",FROST_GLOW44:"🧊✨",NEBULA_GLOW44:"🌠✨"'
A10_NEW = 'EMBER_GLOW44:"🔥✨",PLASMA_GLOW44:"⚛️✨",THUNDER_GLOW44:"⚡✨",FROST_GLOW44:"🧊✨",NEBULA_GLOW44:"🌠✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 729 done! +{len(src)-orig_len} bytes")
