#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"attakolite_orb9e_peak", label:"Attakolite Orb Peak", desc:"Hit Attakolite Orb at peak glow", icon:"💛", xp:150 },'
A1_NEW = (
    '  { id:"attakolite_orb9e_peak", label:"Attakolite Orb Peak", desc:"Hit Attakolite Orb at peak glow", icon:"💛", xp:150 },\n'
    '  { id:"jade_glow44_use", label:"Jade Glow", desc:"Activate JADE_GLOW44 power-up", icon:"💚", xp:65 },\n'
    '  { id:"jade_glow44_max", label:"Jade Master", desc:"Reach max score with JADE_GLOW44 active", icon:"🌿", xp:130 },\n'
    '  { id:"ruby_glow44_use", label:"Ruby Glow", desc:"Activate RUBY_GLOW44 power-up", icon:"❤️", xp:65 },\n'
    '  { id:"ruby_glow44_max", label:"Ruby Master", desc:"Reach max score with RUBY_GLOW44 active", icon:"💎", xp:130 },\n'
    '  { id:"augelite_fox9e_tap", label:"Augelite Fox", desc:"Tap an Augelite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"augelite_fox9e_peak", label:"Augelite Fox Peak", desc:"Hit Augelite Fox at peak glow", icon:"🔘", xp:150 },\n'
    '  { id:"azurmalachite_orb9e_tap", label:"Azurmalachite Orb", desc:"Tap an Azurmalachite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"azurmalachite_orb9e_peak", label:"Azurmalachite Orb Peak", desc:"Hit Azurmalachite Orb at peak glow", icon:"🌊", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"VOLT_GLOW44","AZURE_GLOW44","MAGMA_GLOW44","QUARTZ_GLOW44","EMBER_GLOW44"'
A2_NEW = '"JADE_GLOW44","RUBY_GLOW44","VOLT_GLOW44","AZURE_GLOW44","MAGMA_GLOW44","QUARTZ_GLOW44","EMBER_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="VOLT_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="JADE_GLOW44"){\n'
    '    gs.score+=2392;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2102,text:"+2392",color:"#059669",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#059669",life:0.7});\n'
    '    sfx("powerUp");unlock("jade_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("jade_glow44_max");\n'
    '  } else if(ptype==="RUBY_GLOW44"){\n'
    '    gs.score+=2394;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2104,text:"+2394",color:"#e11d48",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#e11d48",life:0.7});\n'
    '    sfx("powerUp");unlock("ruby_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("ruby_glow44_max");\n'
    '  } else if(ptype==="VOLT_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // VOLT_GLOW44 — +2388 volt glow bonus'
A4_NEW = (
    '  // JADE_GLOW44 — +2392 jade glow bonus\n'
    '  // RUBY_GLOW44 — +2394 ruby glow bonus\n'
    '  // VOLT_GLOW44 — +2388 volt glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawAstrophylliteFox9e('
A5_NEW = (
    'function drawAugeliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4153)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+sp*0.35,"#cbd5e1");g.addColorStop(1,"#64748b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(203,213,225,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#64748b":"#0f172a";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🔘":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAzurmalachiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4157);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#67e8f9");g.addColorStop(0.35+tp*0.35,"#0891b2");g.addColorStop(1,"#164e63");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(8,145,178,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(8,145,178,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#0891b2":"#ecfeff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🌊":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAstrophylliteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="astrophyllite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="augelite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2238);\n'
    '    drawAugeliteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="azurmalachite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2240);\n'
    '    drawAzurmalachiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="astrophyllite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="astrophyllite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="augelite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(448*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🔘":""),color:"#cbd5e1",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#cbd5e1",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("augelite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("augelite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="azurmalachite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(443*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🌊":""),color:"#0891b2",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#0891b2",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("azurmalachite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("azurmalachite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="astrophyllite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="astrophyllite_fox9e";color="#b45309";glow="#fffbeb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="attakolite_orb9e"')
A8_NEW = (
    '      type="augelite_fox9e";color="#cbd5e1";glow="#f8fafc";\n'
    '    } else if('+COND100F+'){\n'
    '      type="azurmalachite_orb9e";color="#0891b2";glow="#ecfeff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="astrophyllite_fox9e";color="#b45309";glow="#fffbeb";\n'
    '    } else if('+COND100F+'){\n'
    '      type="attakolite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="astrophyllite_fox9e"?BASE_R*1.76:type==="attakolite_orb9e"?BASE_R*1.75:'
A9_NEW = 'type==="augelite_fox9e"?BASE_R*1.77:type==="azurmalachite_orb9e"?BASE_R*1.76:type==="astrophyllite_fox9e"?BASE_R*1.76:type==="attakolite_orb9e"?BASE_R*1.75:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'VOLT_GLOW44:"⚡✨",AZURE_GLOW44:"🔵✨",MAGMA_GLOW44:"🌋✨"'
A10_NEW = 'JADE_GLOW44:"💚✨",RUBY_GLOW44:"❤️✨",VOLT_GLOW44:"⚡✨",AZURE_GLOW44:"🔵✨",MAGMA_GLOW44:"🌋✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 732 done! +{len(src)-orig_len} bytes")
