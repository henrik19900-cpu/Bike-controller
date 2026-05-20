#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"calaverite_orb9e_peak", label:"Calaverite Orb Peak", desc:"Hit Calaverite Orb at peak glow", icon:"🥇", xp:150 },'
A1_NEW = (
    '  { id:"calaverite_orb9e_peak", label:"Calaverite Orb Peak", desc:"Hit Calaverite Orb at peak glow", icon:"🥇", xp:150 },\n'
    '  { id:"arcane_glow44_use", label:"Arcane Glow", desc:"Activate ARCANE_GLOW44 power-up", icon:"🔮", xp:65 },\n'
    '  { id:"arcane_glow44_max", label:"Arcane Master", desc:"Reach max score with ARCANE_GLOW44 active", icon:"✨", xp:130 },\n'
    '  { id:"inferno_glow44_use", label:"Inferno Glow", desc:"Activate INFERNO_GLOW44 power-up", icon:"🔥", xp:65 },\n'
    '  { id:"inferno_glow44_max", label:"Inferno Master", desc:"Reach max score with INFERNO_GLOW44 active", icon:"🌋", xp:130 },\n'
    '  { id:"calderite_fox9e_tap", label:"Calderite Fox", desc:"Tap a Calderite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"calderite_fox9e_peak", label:"Calderite Fox Peak", desc:"Hit Calderite Fox at peak glow", icon:"❤️", xp:150 },\n'
    '  { id:"caledonite_orb9e_tap", label:"Caledonite Orb", desc:"Tap a Caledonite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"caledonite_orb9e_peak", label:"Caledonite Orb Peak", desc:"Hit Caledonite Orb at peak glow", icon:"💙", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"PRIMAL_GLOW44","DIVINE_GLOW44","RADIANT_GLOW44","MYSTIC_GLOW44","GOLD_GLOW44"'
A2_NEW = '"ARCANE_GLOW44","INFERNO_GLOW44","PRIMAL_GLOW44","DIVINE_GLOW44","RADIANT_GLOW44","MYSTIC_GLOW44","GOLD_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="PRIMAL_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="ARCANE_GLOW44"){\n'
    '    gs.score+=2428;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2138,text:"+2428",color:"#9333ea",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#9333ea",life:0.7});\n'
    '    sfx("powerUp");unlock("arcane_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("arcane_glow44_max");\n'
    '  } else if(ptype==="INFERNO_GLOW44"){\n'
    '    gs.score+=2430;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2140,text:"+2430",color:"#dc2626",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#dc2626",life:0.7});\n'
    '    sfx("powerUp");unlock("inferno_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("inferno_glow44_max");\n'
    '  } else if(ptype==="PRIMAL_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // PRIMAL_GLOW44 — +2424 primal glow bonus'
A4_NEW = (
    '  // ARCANE_GLOW44 — +2428 arcane glow bonus\n'
    '  // INFERNO_GLOW44 — +2430 inferno glow bonus\n'
    '  // PRIMAL_GLOW44 — +2424 primal glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawCafarsiteFox9e('
A5_NEW = (
    'function drawCalderiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4209)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fca5a5");g.addColorStop(0.45+sp*0.35,"#ef4444");g.addColorStop(1,"#7f1d1d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(239,68,68,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#7f1d1d":"#fef2f2";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"❤️":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawCaledoniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4213);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#93c5fd");g.addColorStop(0.35+tp*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(37,99,235,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(37,99,235,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#2563eb":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💙":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawCafarsiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="cafarsite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="calderite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2274);\n'
    '    drawCalderiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="caledonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2276);\n'
    '    drawCaledoniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="cafarsite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="cafarsite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="calderite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(466*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" ❤️":""),color:"#ef4444",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#ef4444",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("calderite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("calderite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="caledonite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(461*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 💙":""),color:"#2563eb",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#2563eb",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("caledonite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("caledonite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="cafarsite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="cafarsite_fox9e";color="#ea580c";glow="#fff7ed";\n'
          '    } else if('+COND100F+'){\n'
          '      type="calaverite_orb9e"')
A8_NEW = (
    '      type="calderite_fox9e";color="#ef4444";glow="#fef2f2";\n'
    '    } else if('+COND100F+'){\n'
    '      type="caledonite_orb9e";color="#2563eb";glow="#eff6ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="cafarsite_fox9e";color="#ea580c";glow="#fff7ed";\n'
    '    } else if('+COND100F+'){\n'
    '      type="calaverite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="cafarsite_fox9e"?BASE_R*1.85:type==="calaverite_orb9e"?BASE_R*1.84:'
A9_NEW = 'type==="calderite_fox9e"?BASE_R*1.86:type==="caledonite_orb9e"?BASE_R*1.85:type==="cafarsite_fox9e"?BASE_R*1.85:type==="calaverite_orb9e"?BASE_R*1.84:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'PRIMAL_GLOW44:"🌿✨",DIVINE_GLOW44:"👼✨",RADIANT_GLOW44:"✨✨"'
A10_NEW = 'ARCANE_GLOW44:"🔮✨",INFERNO_GLOW44:"🔥✨",PRIMAL_GLOW44:"🌿✨",DIVINE_GLOW44:"👼✨",RADIANT_GLOW44:"✨✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 741 done! +{len(src)-orig_len} bytes")
