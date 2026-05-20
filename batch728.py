#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"ankerite_orb9e_peak", label:"Ankerite Orb Peak", desc:"Hit Ankerite Orb at peak glow", icon:"🌕", xp:150 },'
A1_NEW = (
    '  { id:"ankerite_orb9e_peak", label:"Ankerite Orb Peak", desc:"Hit Ankerite Orb at peak glow", icon:"🌕", xp:150 },\n'
    '  { id:"thunder_glow44_use", label:"Thunder Glow", desc:"Activate THUNDER_GLOW44 power-up", icon:"⚡", xp:65 },\n'
    '  { id:"thunder_glow44_max", label:"Thunder Master", desc:"Reach max score with THUNDER_GLOW44 active", icon:"🌩️", xp:130 },\n'
    '  { id:"frost_glow44_use", label:"Frost Glow", desc:"Activate FROST_GLOW44 power-up", icon:"🧊", xp:65 },\n'
    '  { id:"frost_glow44_max", label:"Frost Master", desc:"Reach max score with FROST_GLOW44 active", icon:"❄️", xp:130 },\n'
    '  { id:"anorthite_fox9e_tap", label:"Anorthite Fox", desc:"Tap an Anorthite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"anorthite_fox9e_peak", label:"Anorthite Fox Peak", desc:"Hit Anorthite Fox at peak glow", icon:"🤍", xp:150 },\n'
    '  { id:"antlerite_orb9e_tap", label:"Antlerite Orb", desc:"Tap an Antlerite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"antlerite_orb9e_peak", label:"Antlerite Orb Peak", desc:"Hit Antlerite Orb at peak glow", icon:"💚", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"NEBULA_GLOW44","AURORA_GLOW44","COSMIC_GLOW44","VOID_GLOW44","SOLAR_GLOW44"'
A2_NEW = '"THUNDER_GLOW44","FROST_GLOW44","NEBULA_GLOW44","AURORA_GLOW44","COSMIC_GLOW44","VOID_GLOW44","SOLAR_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="NEBULA_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="THUNDER_GLOW44"){\n'
    '    gs.score+=2376;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2086,text:"+2376",color:"#eab308",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#eab308",life:0.7});\n'
    '    sfx("powerUp");unlock("thunder_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("thunder_glow44_max");\n'
    '  } else if(ptype==="FROST_GLOW44"){\n'
    '    gs.score+=2378;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2088,text:"+2378",color:"#38bdf8",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#38bdf8",life:0.7});\n'
    '    sfx("powerUp");unlock("frost_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("frost_glow44_max");\n'
    '  } else if(ptype==="NEBULA_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // NEBULA_GLOW44 — +2372 nebula glow bonus'
A4_NEW = (
    '  // THUNDER_GLOW44 — +2376 thunder glow bonus\n'
    '  // FROST_GLOW44 — +2378 frost glow bonus\n'
    '  // NEBULA_GLOW44 — +2372 nebula glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAndoriteFox9e('
A5_NEW = (
    'function drawAnorthiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4127)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#ffffff");g.addColorStop(0.45+sp*0.35,"#f1f5f9");g.addColorStop(1,"#94a3b8");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(241,245,249,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#94a3b8":"#0f172a";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🤍":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAntleriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4131);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#86efac");g.addColorStop(0.35+tp*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(22,163,74,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,163,74,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#16a34a":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💚":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAndoriteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="andorite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="anorthite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2222);\n'
    '    drawAnorthiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="antlerite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2224);\n'
    '    drawAntleriteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="andorite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="andorite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="anorthite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(440*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🤍":""),color:"#f1f5f9",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#f1f5f9",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("anorthite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("anorthite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="antlerite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(435*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 💚":""),color:"#16a34a",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#16a34a",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("antlerite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("antlerite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="andorite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="andorite_fox9e";color="#9ca3af";glow="#f3f4f6";\n'
          '    } else if('+COND100F+'){\n'
          '      type="ankerite_orb9e"')
A8_NEW = (
    '      type="anorthite_fox9e";color="#f1f5f9";glow="#ffffff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="antlerite_orb9e";color="#16a34a";glow="#f0fdf4";\n'
    '    } else if('+COND100F+'){\n'
    '      type="andorite_fox9e";color="#9ca3af";glow="#f3f4f6";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ankerite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="andorite_fox9e"?BASE_R*1.72:type==="ankerite_orb9e"?BASE_R*1.71:'
A9_NEW = 'type==="anorthite_fox9e"?BASE_R*1.73:type==="antlerite_orb9e"?BASE_R*1.72:type==="andorite_fox9e"?BASE_R*1.72:type==="ankerite_orb9e"?BASE_R*1.71:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'NEBULA_GLOW44:"🌠✨",AURORA_GLOW44:"🌌✨",COSMIC_GLOW44:"🌌✨"'
A10_NEW = 'THUNDER_GLOW44:"⚡✨",FROST_GLOW44:"🧊✨",NEBULA_GLOW44:"🌠✨",AURORA_GLOW44:"🌌✨",COSMIC_GLOW44:"🌌✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 728 done! +{len(src)-orig_len} bytes")
