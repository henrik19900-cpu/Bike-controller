#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"algodonite_orb9e_peak", label:"Algodonite Orb Peak", desc:"Hit Algodonite Orb at peak glow", icon:"🔵", xp:150 },'
A1_NEW = (
    '  { id:"algodonite_orb9e_peak", label:"Algodonite Orb Peak", desc:"Hit Algodonite Orb at peak glow", icon:"🔵", xp:150 },\n'
    '  { id:"wind_glow44_use", label:"Wind Glow", desc:"Activate WIND_GLOW44 power-up", icon:"💨", xp:65 },\n'
    '  { id:"wind_glow44_max", label:"Wind Master", desc:"Reach max score with WIND_GLOW44 active", icon:"🌬️", xp:130 },\n'
    '  { id:"storm_glow44_use", label:"Storm Glow", desc:"Activate STORM_GLOW44 power-up", icon:"⛈️", xp:65 },\n'
    '  { id:"storm_glow44_max", label:"Storm Master", desc:"Reach max score with STORM_GLOW44 active", icon:"🌩️", xp:130 },\n'
    '  { id:"allanite_fox9e_tap", label:"Allanite Fox", desc:"Tap an Allanite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"allanite_fox9e_peak", label:"Allanite Fox Peak", desc:"Hit Allanite Fox at peak glow", icon:"🟫", xp:150 },\n'
    '  { id:"alluaudite_orb9e_tap", label:"Alluaudite Orb", desc:"Tap an Alluaudite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"alluaudite_orb9e_peak", label:"Alluaudite Orb Peak", desc:"Hit Alluaudite Orb at peak glow", icon:"🟩", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"FIRE_GLOW44","ICE_GLOW44","DAWN_GLOW44","DUSK_GLOW44","STAR_GLOW44"'
A2_NEW = '"WIND_GLOW44","STORM_GLOW44","FIRE_GLOW44","ICE_GLOW44","DAWN_GLOW44","DUSK_GLOW44","STAR_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="FIRE_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="WIND_GLOW44"){\n'
    '    gs.score+=2356;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2066,text:"+2356",color:"#0ea5e9",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#0ea5e9",life:0.7});\n'
    '    sfx("powerUp");unlock("wind_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("wind_glow44_max");\n'
    '  } else if(ptype==="STORM_GLOW44"){\n'
    '    gs.score+=2358;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2068,text:"+2358",color:"#4f46e5",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#4f46e5",life:0.7});\n'
    '    sfx("powerUp");unlock("storm_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("storm_glow44_max");\n'
    '  } else if(ptype==="FIRE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // FIRE_GLOW44 — +2352 fire glow bonus'
A4_NEW = (
    '  // WIND_GLOW44 — +2356 wind glow bonus\n'
    '  // STORM_GLOW44 — +2358 storm glow bonus\n'
    '  // FIRE_GLOW44 — +2352 fire glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAlacraniteFox9e('
A5_NEW = (
    'function drawAllaniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4093)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#d97706");g.addColorStop(0.45+sp*0.35,"#92400e");g.addColorStop(1,"#451a03");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(146,64,14,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#451a03":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟫":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAlluauditeOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4097);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#bef264");g.addColorStop(0.35+tp*0.35,"#65a30d");g.addColorStop(1,"#365314");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(101,163,13,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(101,163,13,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#65a30d":"#f7fee7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟩":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAlacraniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="alacranite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="allanite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2202);\n'
    '    drawAllaniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="alluaudite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2204);\n'
    '    drawAlluauditeOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="alacranite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="alacranite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="allanite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(430*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🟫":""),color:"#92400e",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#92400e",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("allanite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("allanite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="alluaudite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(425*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🟩":""),color:"#65a30d",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#65a30d",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("alluaudite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("alluaudite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="alacranite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="alacranite_fox9e";color="#dc2626";glow="#fef2f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="algodonite_orb9e"')
A8_NEW = (
    '      type="allanite_fox9e";color="#92400e";glow="#fef3c7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="alluaudite_orb9e";color="#65a30d";glow="#f7fee7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="alacranite_fox9e";color="#dc2626";glow="#fef2f2";\n'
    '    } else if('+COND100F+'){\n'
    '      type="algodonite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="alacranite_fox9e"?BASE_R*1.67:type==="algodonite_orb9e"?BASE_R*1.66:'
A9_NEW = 'type==="allanite_fox9e"?BASE_R*1.68:type==="alluaudite_orb9e"?BASE_R*1.67:type==="alacranite_fox9e"?BASE_R*1.67:type==="algodonite_orb9e"?BASE_R*1.66:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'FIRE_GLOW44:"🔥✨",ICE_GLOW44:"❄️✨",DAWN_GLOW44:"🌅✨"'
A10_NEW = 'WIND_GLOW44:"💨✨",STORM_GLOW44:"⛈️✨",FIRE_GLOW44:"🔥✨",ICE_GLOW44:"❄️✨",DAWN_GLOW44:"🌅✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 723 done! +{len(src)-orig_len} bytes")
