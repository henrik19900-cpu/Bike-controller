#!/usr/bin/env python3

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"bultfonteinite_orb9e_peak", label:"Bultfonteinite Orb Peak", desc:"Hit Bultfonteinite Orb at peak glow", icon:"🌸", xp:150 },'
A1_NEW = (
    '  { id:"bultfonteinite_orb9e_peak", label:"Bultfonteinite Orb Peak", desc:"Hit Bultfonteinite Orb at peak glow", icon:"🌸", xp:150 },\n'
    '  { id:"gold_glow44_use", label:"Gold Glow", desc:"Activate GOLD_GLOW44 power-up", icon:"🥇", xp:65 },\n'
    '  { id:"gold_glow44_max", label:"Gold Master", desc:"Reach max score with GOLD_GLOW44 active", icon:"✨", xp:130 },\n'
    '  { id:"bronze_glow44_use", label:"Bronze Glow", desc:"Activate BRONZE_GLOW44 power-up", icon:"🥉", xp:65 },\n'
    '  { id:"bronze_glow44_max", label:"Bronze Master", desc:"Reach max score with BRONZE_GLOW44 active", icon:"🏆", xp:130 },\n'
    '  { id:"bunsenite_fox9e_tap", label:"Bunsenite Fox", desc:"Tap a Bunsenite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"bunsenite_fox9e_peak", label:"Bunsenite Fox Peak", desc:"Hit Bunsenite Fox at peak glow", icon:"🟩", xp:150 },\n'
    '  { id:"buttgenbachite_orb9e_tap", label:"Buttgenbachite Orb", desc:"Tap a Buttgenbachite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"buttgenbachite_orb9e_peak", label:"Buttgenbachite Orb Peak", desc:"Hit Buttgenbachite Orb at peak glow", icon:"🔹", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: power-up list ─────────────────────────────────────────────────
A2_OLD = '"AMBER_GLOW44","SILVER_GLOW44","OPAL_GLOW44","GARNET_GLOW44","PEARL_GLOW44"'
A2_NEW = '"GOLD_GLOW44","BRONZE_GLOW44","AMBER_GLOW44","SILVER_GLOW44","OPAL_GLOW44","GARNET_GLOW44","PEARL_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: handler ───────────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="AMBER_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="GOLD_GLOW44"){\n'
    '    gs.score+=2416;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2126,text:"+2416",color:"#d97706",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#d97706",life:0.7});\n'
    '    sfx("powerUp");unlock("gold_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("gold_glow44_max");\n'
    '  } else if(ptype==="BRONZE_GLOW44"){\n'
    '    gs.score+=2418;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2128,text:"+2418",color:"#b45309",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#b45309",life:0.7});\n'
    '    sfx("powerUp");unlock("bronze_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("bronze_glow44_max");\n'
    '  } else if(ptype==="AMBER_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment ───────────────────────────────────────────────────────
A4_OLD = '  // AMBER_GLOW44 — +2412 amber glow bonus'
A4_NEW = (
    '  // GOLD_GLOW44 — +2416 gold glow bonus\n'
    '  // BRONZE_GLOW44 — +2418 bronze glow bonus\n'
    '  // AMBER_GLOW44 — +2412 amber glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ────────────────────────────────────────────────
A5_OLD = 'function drawBrazilianiteFox9e('
A5_NEW = (
    'function drawBunseniteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4193)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#86efac");g.addColorStop(0.45+sp*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,163,74,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#14532d":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟩":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawButtgenbachiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4197);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#a5f3fc");g.addColorStop(0.35+tp*0.35,"#0e7490");g.addColorStop(1,"#164e63");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(14,116,144,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(14,116,144,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#0e7490":"#ecfeff";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🔹":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawBrazilianiteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="brazilianite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="bunsenite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2262);\n'
    '    drawBunseniteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="buttgenbachite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2264);\n'
    '    drawButtgenbachiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="brazilianite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="brazilianite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="bunsenite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(460*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🟩":""),color:"#16a34a",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#16a34a",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("bunsenite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("bunsenite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="buttgenbachite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(455*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🔹":""),color:"#0e7490",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#0e7490",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("buttgenbachite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("buttgenbachite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="brazilianite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget ───────────────────────────────────────────────────
A8_OLD = ('      type="brazilianite_fox9e";color="#65a30d";glow="#f7fee7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bultfonteinite_orb9e"')
A8_NEW = (
    '      type="bunsenite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
    '    } else if('+COND100F+'){\n'
    '      type="buttgenbachite_orb9e";color="#0e7490";glow="#ecfeff";\n'
    '    } else if('+COND100F+'){\n'
    '      type="brazilianite_fox9e";color="#65a30d";glow="#f7fee7";\n'
    '    } else if('+COND100F+'){\n'
    '      type="bultfonteinite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ──────────────────────────────────────────────────
A9_OLD = 'type==="brazilianite_fox9e"?BASE_R*1.82:type==="bultfonteinite_orb9e"?BASE_R*1.81:'
A9_NEW = 'type==="bunsenite_fox9e"?BASE_R*1.83:type==="buttgenbachite_orb9e"?BASE_R*1.82:type==="brazilianite_fox9e"?BASE_R*1.82:type==="bultfonteinite_orb9e"?BASE_R*1.81:'
assert src.count(A9_OLD) == 1, f"Step9: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'AMBER_GLOW44:"🟡✨",SILVER_GLOW44:"⚪✨",OPAL_GLOW44:"🌈✨"'
A10_NEW = 'GOLD_GLOW44:"🥇✨",BRONZE_GLOW44:"🥉✨",AMBER_GLOW44:"🟡✨",SILVER_GLOW44:"⚪✨",OPAL_GLOW44:"🌈✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 738 done! +{len(src)-orig_len} bytes")
