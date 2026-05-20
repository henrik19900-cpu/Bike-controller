#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ──────────────────────────────────────────────────
A1_OLD = '  { id:"akermanite_orb9e_peak", label:"Akermanite Orb Peak", desc:"Hit Akermanite Orb at peak glow", icon:"🟠", xp:150 },'
A1_NEW = (
    '  { id:"akermanite_orb9e_peak", label:"Akermanite Orb Peak", desc:"Hit Akermanite Orb at peak glow", icon:"🟠", xp:150 },\n'
    '  { id:"fire_glow44_use", label:"Fire Glow", desc:"Activate FIRE_GLOW44 power-up", icon:"🔥", xp:65 },\n'
    '  { id:"fire_glow44_max", label:"Fire Master", desc:"Reach max score with FIRE_GLOW44 active", icon:"🔥", xp:130 },\n'
    '  { id:"ice_glow44_use", label:"Ice Glow", desc:"Activate ICE_GLOW44 power-up", icon:"❄️", xp:65 },\n'
    '  { id:"ice_glow44_max", label:"Ice Master", desc:"Reach max score with ICE_GLOW44 active", icon:"🧊", xp:130 },\n'
    '  { id:"alacranite_fox9e_tap", label:"Alacranite Fox", desc:"Tap an Alacranite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"alacranite_fox9e_peak", label:"Alacranite Fox Peak", desc:"Hit Alacranite Fox at peak glow", icon:"🔴", xp:150 },\n'
    '  { id:"algodonite_orb9e_tap", label:"Algodonite Orb", desc:"Tap an Algodonite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"algodonite_orb9e_peak", label:"Algodonite Orb Peak", desc:"Hit Algodonite Orb at peak glow", icon:"🔵", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ──────────────────────────────────────────────────
A2_OLD = '"DAWN_GLOW44","DUSK_GLOW44","STAR_GLOW44","MOON_GLOW44","NOVA_GLOW44"'
A2_NEW = '"FIRE_GLOW44","ICE_GLOW44","DAWN_GLOW44","DUSK_GLOW44","STAR_GLOW44","MOON_GLOW44","NOVA_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="DAWN_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="FIRE_GLOW44"){\n'
    '    gs.score+=2352;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2062,text:"+2352",color:"#dc2626",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#dc2626",life:0.7});\n'
    '    sfx("powerUp");unlock("fire_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("fire_glow44_max");\n'
    '  } else if(ptype==="ICE_GLOW44"){\n'
    '    gs.score+=2354;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2064,text:"+2354",color:"#0284c7",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#0284c7",life:0.7});\n'
    '    sfx("powerUp");unlock("ice_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("ice_glow44_max");\n'
    '  } else if(ptype==="DAWN_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // DAWN_GLOW44 — +2348 dawn glow bonus'
A4_NEW = (
    '  // FIRE_GLOW44 — +2352 fire glow bonus\n'
    '  // ICE_GLOW44 — +2354 ice glow bonus\n'
    '  // DAWN_GLOW44 — +2348 dawn glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAjoiteFox9e('
A5_NEW = (
    'function drawAlacraniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4089)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fca5a5");g.addColorStop(0.45+sp*0.35,"#dc2626");g.addColorStop(1,"#991b1b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(220,38,38,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#991b1b":"#fef2f2";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🔴":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAlgodoniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4091);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bae6fd");g.addColorStop(0.35+tp*0.35,"#0284c7");g.addColorStop(1,"#075985");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(2,132,199,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(2,132,199,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#0284c7":"#f0f9ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔵":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAjoiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="ajoite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="alacranite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2198);\n'
    '    drawAlacraniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="algodonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2200);\n'
    '    drawAlgodoniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="ajoite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="ajoite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="alacranite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(428*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🔴":""),color:"#dc2626",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#dc2626",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("alacranite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("alacranite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="algodonite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(423*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🔵":""),color:"#0284c7",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#0284c7",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("algodonite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("algodonite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="ajoite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="ajoite_fox9e";color="#34d399";glow="#ecfdf5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="akermanite_orb9e"')
A8_NEW = (
    '      type="alacranite_fox9e";color="#dc2626";glow="#fef2f2";\n'
    '    } else if('+COND100F+'){\n'
    '      type="algodonite_orb9e";color="#0284c7";glow="#f0f9ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ajoite_fox9e";color="#34d399";glow="#ecfdf5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="akermanite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="ajoite_fox9e"?BASE_R*1.66:type==="akermanite_orb9e"?BASE_R*1.65:'
A9_NEW = 'type==="alacranite_fox9e"?BASE_R*1.67:type==="algodonite_orb9e"?BASE_R*1.66:type==="ajoite_fox9e"?BASE_R*1.66:type==="akermanite_orb9e"?BASE_R*1.65:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'DAWN_GLOW44:"🌅✨",DUSK_GLOW44:"🌆✨",STAR_GLOW44:"⭐✨"'
A10_NEW = 'FIRE_GLOW44:"🔥✨",ICE_GLOW44:"❄️✨",DAWN_GLOW44:"🌅✨",DUSK_GLOW44:"🌆✨",STAR_GLOW44:"⭐✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 722 done! +{len(src)-orig_len} bytes")
