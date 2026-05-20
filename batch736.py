#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"bobfergusonite_orb9e_peak", label:"Bobfergusonite Orb Peak", desc:"Hit Bobfergusonite Orb at peak glow", icon:"🔵", xp:150 },'
A1_NEW = (
    '  { id:"bobfergusonite_orb9e_peak", label:"Bobfergusonite Orb Peak", desc:"Hit Bobfergusonite Orb at peak glow", icon:"🔵", xp:150 },\n'
    '  { id:"opal_glow44_use", label:"Opal Glow", desc:"Activate OPAL_GLOW44 power-up", icon:"🌈", xp:65 },\n'
    '  { id:"opal_glow44_max", label:"Opal Master", desc:"Reach max score with OPAL_GLOW44 active", icon:"✨", xp:130 },\n'
    '  { id:"garnet_glow44_use", label:"Garnet Glow", desc:"Activate GARNET_GLOW44 power-up", icon:"❤️", xp:65 },\n'
    '  { id:"garnet_glow44_max", label:"Garnet Master", desc:"Reach max score with GARNET_GLOW44 active", icon:"💗", xp:130 },\n'
    '  { id:"boracite_fox9e_tap", label:"Boracite Fox", desc:"Tap a Boracite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"boracite_fox9e_peak", label:"Boracite Fox Peak", desc:"Hit Boracite Fox at peak glow", icon:"⬜", xp:150 },\n'
    '  { id:"bowenite_orb9e_tap", label:"Bowenite Orb", desc:"Tap a Bowenite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"bowenite_orb9e_peak", label:"Bowenite Orb Peak", desc:"Hit Bowenite Orb at peak glow", icon:"🌿", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"PEARL_GLOW44","TOPAZ_GLOW44","DIAMOND_GLOW44","ONYX_GLOW44","SAPPHIRE_GLOW44"'
A2_NEW = '"OPAL_GLOW44","GARNET_GLOW44","PEARL_GLOW44","TOPAZ_GLOW44","DIAMOND_GLOW44","ONYX_GLOW44","SAPPHIRE_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="PEARL_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="OPAL_GLOW44"){\n'
    '    gs.score+=2408;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2118,text:"+2408",color:"#f0abfc",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#f0abfc",life:0.7});\n'
    '    sfx("powerUp");unlock("opal_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("opal_glow44_max");\n'
    '  } else if(ptype==="GARNET_GLOW44"){\n'
    '    gs.score+=2410;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2120,text:"+2410",color:"#9f1239",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#9f1239",life:0.7});\n'
    '    sfx("powerUp");unlock("garnet_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("garnet_glow44_max");\n'
    '  } else if(ptype==="PEARL_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // PEARL_GLOW44 — +2404 pearl glow bonus'
A4_NEW = (
    '  // OPAL_GLOW44 — +2408 opal glow bonus\n'
    '  // GARNET_GLOW44 — +2410 garnet glow bonus\n'
    '  // PEARL_GLOW44 — +2404 pearl glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawBixbyiteFox9e('
A5_NEW = (
    'function drawBoraciteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4179)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.45+sp*0.35,"#94a3b8");g.addColorStop(1,"#475569");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(148,163,184,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#475569":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"⬜":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBoweniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4183);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bbf7d0");g.addColorStop(0.35+tp*0.35,"#15803d");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(21,128,61,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(21,128,61,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#15803d":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌿":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBixbyiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="bixbyite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="boracite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2254);\n'
    '    drawBoraciteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="bowenite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2256);\n'
    '    drawBoweniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="bixbyite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="bixbyite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="boracite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(456*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" ⬜":""),color:"#94a3b8",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#94a3b8",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("boracite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("boracite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="bowenite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(451*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🌿":""),color:"#15803d",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#15803d",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("bowenite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("bowenite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="bixbyite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="bixbyite_fox9e";color="#1c1917";glow="#fafaf9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bobfergusonite_orb9e"')
A8_NEW = (
    '      type="boracite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bowenite_orb9e";color="#15803d";glow="#f0fdf4";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bixbyite_fox9e";color="#1c1917";glow="#fafaf9";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bobfergusonite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="bixbyite_fox9e"?BASE_R*1.80:type==="bobfergusonite_orb9e"?BASE_R*1.79:'
A9_NEW = 'type==="boracite_fox9e"?BASE_R*1.81:type==="bowenite_orb9e"?BASE_R*1.80:type==="bixbyite_fox9e"?BASE_R*1.80:type==="bobfergusonite_orb9e"?BASE_R*1.79:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'PEARL_GLOW44:"🤍✨",TOPAZ_GLOW44:"🟡✨",DIAMOND_GLOW44:"💎✨"'
A10_NEW = 'OPAL_GLOW44:"🌈✨",GARNET_GLOW44:"❤️✨",PEARL_GLOW44:"🤍✨",TOPAZ_GLOW44:"🟡✨",DIAMOND_GLOW44:"💎✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 736 done! +{len(src)-orig_len} bytes")
