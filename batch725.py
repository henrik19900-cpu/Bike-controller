#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"amarantite_orb9e_peak", label:"Amarantite Orb Peak", desc:"Hit Amarantite Orb at peak glow", icon:"🔺", xp:150 },'
A1_NEW = (
    '  { id:"amarantite_orb9e_peak", label:"Amarantite Orb Peak", desc:"Hit Amarantite Orb at peak glow", icon:"🔺", xp:150 },\n'
    '  { id:"solar_glow44_use", label:"Solar Glow", desc:"Activate SOLAR_GLOW44 power-up", icon:"☀️", xp:65 },\n'
    '  { id:"solar_glow44_max", label:"Solar Master", desc:"Reach max score with SOLAR_GLOW44 active", icon:"🌞", xp:130 },\n'
    '  { id:"lunar_glow44_use", label:"Lunar Glow", desc:"Activate LUNAR_GLOW44 power-up", icon:"🌙", xp:65 },\n'
    '  { id:"lunar_glow44_max", label:"Lunar Master", desc:"Reach max score with LUNAR_GLOW44 active", icon:"🌛", xp:130 },\n'
    '  { id:"amazonite_fox9e_tap", label:"Amazonite Fox", desc:"Tap an Amazonite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"amazonite_fox9e_peak", label:"Amazonite Fox Peak", desc:"Hit Amazonite Fox at peak glow", icon:"🟦", xp:150 },\n'
    '  { id:"amblygonite_orb9e_tap", label:"Amblygonite Orb", desc:"Tap an Amblygonite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"amblygonite_orb9e_peak", label:"Amblygonite Orb Peak", desc:"Hit Amblygonite Orb at peak glow", icon:"🟡", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"LIGHT_GLOW44","DARK_GLOW44","WIND_GLOW44","STORM_GLOW44","FIRE_GLOW44"'
A2_NEW = '"SOLAR_GLOW44","LUNAR_GLOW44","LIGHT_GLOW44","DARK_GLOW44","WIND_GLOW44","STORM_GLOW44","FIRE_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="LIGHT_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="SOLAR_GLOW44"){\n'
    '    gs.score+=2364;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2074,text:"+2364",color:"#f59e0b",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#f59e0b",life:0.7});\n'
    '    sfx("powerUp");unlock("solar_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("solar_glow44_max");\n'
    '  } else if(ptype==="LUNAR_GLOW44"){\n'
    '    gs.score+=2366;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2076,text:"+2366",color:"#8b5cf6",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#8b5cf6",life:0.7});\n'
    '    sfx("powerUp");unlock("lunar_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("lunar_glow44_max");\n'
    '  } else if(ptype==="LIGHT_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // LIGHT_GLOW44 — +2360 light glow bonus'
A4_NEW = (
    '  // SOLAR_GLOW44 — +2364 solar glow bonus\n'
    '  // LUNAR_GLOW44 — +2366 lunar glow bonus\n'
    '  // LIGHT_GLOW44 — +2360 light glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAltaiteFox9e('
A5_NEW = (
    'function drawAmazoniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4107)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#99f6e4");g.addColorStop(0.45+sp*0.35,"#0d9488");g.addColorStop(1,"#134e4a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(13,148,136,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#134e4a":"#f0fdfa";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟦":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAmblygoniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4111);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+tp*0.35,"#ca8a04");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(202,138,4,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(202,138,4,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#ca8a04":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟡":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAltaiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="altaite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="amazonite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2210);\n'
    '    drawAmazoniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="amblygonite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2212);\n'
    '    drawAmblygoniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="altaite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="altaite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="amazonite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(434*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🟦":""),color:"#0d9488",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#0d9488",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("amazonite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("amazonite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="amblygonite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(429*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🟡":""),color:"#ca8a04",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#ca8a04",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("amblygonite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("amblygonite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="altaite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="altaite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="amarantite_orb9e"')
A8_NEW = (
    '      type="amazonite_fox9e";color="#0d9488";glow="#f0fdfa";\n'
    '    } else if('+COND100F+'){\n'
    '      type="amblygonite_orb9e";color="#ca8a04";glow="#fefce8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="altaite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="amarantite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="altaite_fox9e"?BASE_R*1.69:type==="amarantite_orb9e"?BASE_R*1.68:'
A9_NEW = 'type==="amazonite_fox9e"?BASE_R*1.70:type==="amblygonite_orb9e"?BASE_R*1.69:type==="altaite_fox9e"?BASE_R*1.69:type==="amarantite_orb9e"?BASE_R*1.68:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'LIGHT_GLOW44:"💡✨",DARK_GLOW44:"🌑✨",WIND_GLOW44:"💨✨"'
A10_NEW = 'SOLAR_GLOW44:"☀️✨",LUNAR_GLOW44:"🌙✨",LIGHT_GLOW44:"💡✨",DARK_GLOW44:"🌑✨",WIND_GLOW44:"💨✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 725 done! +{len(src)-orig_len} bytes")
