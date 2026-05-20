#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"bismite_orb9e_peak", label:"Bismite Orb Peak", desc:"Hit Bismite Orb at peak glow", icon:"🟨", xp:150 },'
A1_NEW = (
    '  { id:"bismite_orb9e_peak", label:"Bismite Orb Peak", desc:"Hit Bismite Orb at peak glow", icon:"🟨", xp:150 },\n'
    '  { id:"pearl_glow44_use", label:"Pearl Glow", desc:"Activate PEARL_GLOW44 power-up", icon:"🤍", xp:65 },\n'
    '  { id:"pearl_glow44_max", label:"Pearl Master", desc:"Reach max score with PEARL_GLOW44 active", icon:"🌊", xp:130 },\n'
    '  { id:"topaz_glow44_use", label:"Topaz Glow", desc:"Activate TOPAZ_GLOW44 power-up", icon:"🟡", xp:65 },\n'
    '  { id:"topaz_glow44_max", label:"Topaz Master", desc:"Reach max score with TOPAZ_GLOW44 active", icon:"💛", xp:130 },\n'
    '  { id:"bixbyite_fox9e_tap", label:"Bixbyite Fox", desc:"Tap a Bixbyite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"bixbyite_fox9e_peak", label:"Bixbyite Fox Peak", desc:"Hit Bixbyite Fox at peak glow", icon:"🖤", xp:150 },\n'
    '  { id:"bobfergusonite_orb9e_tap", label:"Bobfergusonite Orb", desc:"Tap a Bobfergusonite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"bobfergusonite_orb9e_peak", label:"Bobfergusonite Orb Peak", desc:"Hit Bobfergusonite Orb at peak glow", icon:"🔵", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"DIAMOND_GLOW44","ONYX_GLOW44","SAPPHIRE_GLOW44","EMERALD_GLOW44","JADE_GLOW44"'
A2_NEW = '"PEARL_GLOW44","TOPAZ_GLOW44","DIAMOND_GLOW44","ONYX_GLOW44","SAPPHIRE_GLOW44","EMERALD_GLOW44","JADE_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="DIAMOND_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="PEARL_GLOW44"){\n'
    '    gs.score+=2404;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2114,text:"+2404",color:"#e2e8f0",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#e2e8f0",life:0.7});\n'
    '    sfx("powerUp");unlock("pearl_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("pearl_glow44_max");\n'
    '  } else if(ptype==="TOPAZ_GLOW44"){\n'
    '    gs.score+=2406;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2116,text:"+2406",color:"#fbbf24",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#fbbf24",life:0.7});\n'
    '    sfx("powerUp");unlock("topaz_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("topaz_glow44_max");\n'
    '  } else if(ptype==="DIAMOND_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // DIAMOND_GLOW44 — +2400 diamond glow bonus'
A4_NEW = (
    '  // PEARL_GLOW44 — +2404 pearl glow bonus\n'
    '  // TOPAZ_GLOW44 — +2406 topaz glow bonus\n'
    '  // DIAMOND_GLOW44 — +2400 diamond glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawBillingsleyiteFox9e('
A5_NEW = (
    'function drawBixbyiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4173)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#57534e");g.addColorStop(0.45+sp*0.35,"#1c1917");g.addColorStop(1,"#0c0a09");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(28,25,23,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0c0a09":"#fafaf9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🖤":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBobfergusoniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4177);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#93c5fd");g.addColorStop(0.35+tp*0.35,"#1e40af");g.addColorStop(1,"#1e3a8a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(30,64,175,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(30,64,175,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#1e40af":"#eff6ff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔵":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBillingsleyiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="billingsleyite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="bixbyite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2250);\n'
    '    drawBixbyiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="bobfergusonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2252);\n'
    '    drawBobfergusoniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="billingsleyite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="billingsleyite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="bixbyite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(454*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🖤":""),color:"#1c1917",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#1c1917",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("bixbyite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("bixbyite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="bobfergusonite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(449*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🔵":""),color:"#1e40af",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#1e40af",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("bobfergusonite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("bobfergusonite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="billingsleyite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="billingsleyite_fox9e";color="#64748b";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bismite_orb9e"')
A8_NEW = (
    '      type="bixbyite_fox9e";color="#1c1917";glow="#fafaf9";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bobfergusonite_orb9e";color="#1e40af";glow="#eff6ff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="billingsleyite_fox9e";color="#64748b";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bismite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="billingsleyite_fox9e"?BASE_R*1.79:type==="bismite_orb9e"?BASE_R*1.78:'
A9_NEW = 'type==="bixbyite_fox9e"?BASE_R*1.80:type==="bobfergusonite_orb9e"?BASE_R*1.79:type==="billingsleyite_fox9e"?BASE_R*1.79:type==="bismite_orb9e"?BASE_R*1.78:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'DIAMOND_GLOW44:"💎✨",ONYX_GLOW44:"⬛✨",SAPPHIRE_GLOW44:"💙✨"'
A10_NEW = 'PEARL_GLOW44:"🤍✨",TOPAZ_GLOW44:"🟡✨",DIAMOND_GLOW44:"💎✨",ONYX_GLOW44:"⬛✨",SAPPHIRE_GLOW44:"💙✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 735 done! +{len(src)-orig_len} bytes")
