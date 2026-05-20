#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"bertrandite_orb9e_peak", label:"Bertrandite Orb Peak", desc:"Hit Bertrandite Orb at peak glow", icon:"🌼", xp:150 },'
A1_NEW = (
    '  { id:"bertrandite_orb9e_peak", label:"Bertrandite Orb Peak", desc:"Hit Bertrandite Orb at peak glow", icon:"🌼", xp:150 },\n'
    '  { id:"diamond_glow44_use", label:"Diamond Glow", desc:"Activate DIAMOND_GLOW44 power-up", icon:"💎", xp:65 },\n'
    '  { id:"diamond_glow44_max", label:"Diamond Master", desc:"Reach max score with DIAMOND_GLOW44 active", icon:"✨", xp:130 },\n'
    '  { id:"onyx_glow44_use", label:"Onyx Glow", desc:"Activate ONYX_GLOW44 power-up", icon:"⬛", xp:65 },\n'
    '  { id:"onyx_glow44_max", label:"Onyx Master", desc:"Reach max score with ONYX_GLOW44 active", icon:"🖤", xp:130 },\n'
    '  { id:"billingsleyite_fox9e_tap", label:"Billingsleyite Fox", desc:"Tap a Billingsleyite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"billingsleyite_fox9e_peak", label:"Billingsleyite Fox Peak", desc:"Hit Billingsleyite Fox at peak glow", icon:"🥈", xp:150 },\n'
    '  { id:"bismite_orb9e_tap", label:"Bismite Orb", desc:"Tap a Bismite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"bismite_orb9e_peak", label:"Bismite Orb Peak", desc:"Hit Bismite Orb at peak glow", icon:"🟨", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"SAPPHIRE_GLOW44","EMERALD_GLOW44","JADE_GLOW44","RUBY_GLOW44","VOLT_GLOW44"'
A2_NEW = '"DIAMOND_GLOW44","ONYX_GLOW44","SAPPHIRE_GLOW44","EMERALD_GLOW44","JADE_GLOW44","RUBY_GLOW44","VOLT_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="SAPPHIRE_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="DIAMOND_GLOW44"){\n'
    '    gs.score+=2400;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2110,text:"+2400",color:"#7dd3fc",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#7dd3fc",life:0.7});\n'
    '    sfx("powerUp");unlock("diamond_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("diamond_glow44_max");\n'
    '  } else if(ptype==="ONYX_GLOW44"){\n'
    '    gs.score+=2402;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2112,text:"+2402",color:"#334155",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#334155",life:0.7});\n'
    '    sfx("powerUp");unlock("onyx_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("onyx_glow44_max");\n'
    '  } else if(ptype==="SAPPHIRE_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // SAPPHIRE_GLOW44 — +2396 sapphire glow bonus'
A4_NEW = (
    '  // DIAMOND_GLOW44 — +2400 diamond glow bonus\n'
    '  // ONYX_GLOW44 — +2402 onyx glow bonus\n'
    '  // SAPPHIRE_GLOW44 — +2396 sapphire glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawBabingtoniteFox9e('
A5_NEW = (
    'function drawBillingsleyiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4167)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#cbd5e1");g.addColorStop(0.45+sp*0.35,"#64748b");g.addColorStop(1,"#1e293b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(100,116,139,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#1e293b":"#f8fafc";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🥈":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBismiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4171);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.35+tp*0.35,"#a16207");g.addColorStop(1,"#713f12");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(161,98,7,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(161,98,7,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#a16207":"#fefce8";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟨":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBabingtoniteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="babingtonite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="billingsleyite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2246);\n'
    '    drawBillingsleyiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="bismite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2248);\n'
    '    drawBismiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="babingtonite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="babingtonite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="billingsleyite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(452*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🥈":""),color:"#64748b",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#64748b",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("billingsleyite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("billingsleyite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="bismite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(447*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🟨":""),color:"#a16207",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#a16207",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("bismite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("bismite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="babingtonite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="babingtonite_fox9e";color="#065f46";glow="#ecfdf5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bertrandite_orb9e"')
A8_NEW = (
    '      type="billingsleyite_fox9e";color="#64748b";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bismite_orb9e";color="#a16207";glow="#fefce8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="babingtonite_fox9e";color="#065f46";glow="#ecfdf5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bertrandite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="babingtonite_fox9e"?BASE_R*1.78:type==="bertrandite_orb9e"?BASE_R*1.77:'
A9_NEW = 'type==="billingsleyite_fox9e"?BASE_R*1.79:type==="bismite_orb9e"?BASE_R*1.78:type==="babingtonite_fox9e"?BASE_R*1.78:type==="bertrandite_orb9e"?BASE_R*1.77:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'SAPPHIRE_GLOW44:"💙✨",EMERALD_GLOW44:"💚✨",JADE_GLOW44:"💚✨"'
A10_NEW = 'DIAMOND_GLOW44:"💎✨",ONYX_GLOW44:"⬛✨",SAPPHIRE_GLOW44:"💙✨",EMERALD_GLOW44:"💚✨",JADE_GLOW44:"💚✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 734 done! +{len(src)-orig_len} bytes")
