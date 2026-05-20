#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"anatase_orb9e_peak", label:"Anatase Orb Peak", desc:"Hit Anatase Orb at peak glow", icon:"🔷", xp:150 },'
A1_NEW = (
    '  { id:"anatase_orb9e_peak", label:"Anatase Orb Peak", desc:"Hit Anatase Orb at peak glow", icon:"🔷", xp:150 },\n'
    '  { id:"nebula_glow44_use", label:"Nebula Glow", desc:"Activate NEBULA_GLOW44 power-up", icon:"🌠", xp:65 },\n'
    '  { id:"nebula_glow44_max", label:"Nebula Master", desc:"Reach max score with NEBULA_GLOW44 active", icon:"💫", xp:130 },\n'
    '  { id:"aurora_glow44_use", label:"Aurora Glow", desc:"Activate AURORA_GLOW44 power-up", icon:"🌌", xp:65 },\n'
    '  { id:"aurora_glow44_max", label:"Aurora Master", desc:"Reach max score with AURORA_GLOW44 active", icon:"🌈", xp:130 },\n'
    '  { id:"andorite_fox9e_tap", label:"Andorite Fox", desc:"Tap an Andorite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"andorite_fox9e_peak", label:"Andorite Fox Peak", desc:"Hit Andorite Fox at peak glow", icon:"🥈", xp:150 },\n'
    '  { id:"ankerite_orb9e_tap", label:"Ankerite Orb", desc:"Tap an Ankerite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"ankerite_orb9e_peak", label:"Ankerite Orb Peak", desc:"Hit Ankerite Orb at peak glow", icon:"🌕", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"COSMIC_GLOW44","VOID_GLOW44","SOLAR_GLOW44","LUNAR_GLOW44","LIGHT_GLOW44"'
A2_NEW = '"NEBULA_GLOW44","AURORA_GLOW44","COSMIC_GLOW44","VOID_GLOW44","SOLAR_GLOW44","LUNAR_GLOW44","LIGHT_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="COSMIC_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="NEBULA_GLOW44"){\n'
    '    gs.score+=2372;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2082,text:"+2372",color:"#a855f7",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#a855f7",life:0.7});\n'
    '    sfx("powerUp");unlock("nebula_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("nebula_glow44_max");\n'
    '  } else if(ptype==="AURORA_GLOW44"){\n'
    '    gs.score+=2374;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2084,text:"+2374",color:"#06b6d4",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#06b6d4",life:0.7});\n'
    '    sfx("powerUp");unlock("aurora_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("aurora_glow44_max");\n'
    '  } else if(ptype==="COSMIC_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // COSMIC_GLOW44 — +2368 cosmic glow bonus'
A4_NEW = (
    '  // NEBULA_GLOW44 — +2372 nebula glow bonus\n'
    '  // AURORA_GLOW44 — +2374 aurora glow bonus\n'
    '  // COSMIC_GLOW44 — +2368 cosmic glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAndesineFox9e('
A5_NEW = (
    'function drawAndoriteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4119)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e5e7eb");g.addColorStop(0.45+sp*0.35,"#9ca3af");g.addColorStop(1,"#4b5563");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(156,163,175,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#4b5563":"#f3f4f6";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🥈":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAnkeriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4123);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fde68a");g.addColorStop(0.35+tp*0.35,"#d97706");g.addColorStop(1,"#78350f");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(217,119,6,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#d97706":"#fffbeb";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌕":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAndesineFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="andesine_fox9e"){'
A6_NEW = (
    '  else if(t.type==="andorite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2218);\n'
    '    drawAndoriteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="ankerite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2220);\n'
    '    drawAnkeriteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="andesine_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="andesine_fox9e"){'
A7_NEW = (
    '    if(hit.type==="andorite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(438*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🥈":""),color:"#9ca3af",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#9ca3af",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("andorite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("andorite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="ankerite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(433*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🌕":""),color:"#d97706",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#d97706",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("ankerite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("ankerite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="andesine_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="andesine_fox9e";color="#6b7280";glow="#f9fafb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="anatase_orb9e"')
A8_NEW = (
    '      type="andorite_fox9e";color="#9ca3af";glow="#f3f4f6";\n'
    '    } else if('+COND100F+'){\n'
    '      type="ankerite_orb9e";color="#d97706";glow="#fffbeb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="andesine_fox9e";color="#6b7280";glow="#f9fafb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="anatase_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="andesine_fox9e"?BASE_R*1.71:type==="anatase_orb9e"?BASE_R*1.70:'
A9_NEW = 'type==="andorite_fox9e"?BASE_R*1.72:type==="ankerite_orb9e"?BASE_R*1.71:type==="andesine_fox9e"?BASE_R*1.71:type==="anatase_orb9e"?BASE_R*1.70:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'COSMIC_GLOW44:"🌌✨",VOID_GLOW44:"🕳️✨",SOLAR_GLOW44:"☀️✨"'
A10_NEW = 'NEBULA_GLOW44:"🌠✨",AURORA_GLOW44:"🌌✨",COSMIC_GLOW44:"🌌✨",VOID_GLOW44:"🕳️✨",SOLAR_GLOW44:"☀️✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 727 done! +{len(src)-orig_len} bytes")
