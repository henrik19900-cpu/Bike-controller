#!/usr/bin/env python3
import re

SRC = "/home/user/Bike-controller/src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()

orig_len = len(src)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── STEP 1: 8 achievements ──────────────────────────────────────────────────
A1_OLD = '  { id:"aikinite_orb9e_peak", label:"Aikinite Orb Peak", desc:"Reach peak with Aikinite Orb", icon:"🟤", xp:120 },'
A1_NEW = (
    '  { id:"aikinite_orb9e_peak", label:"Aikinite Orb Peak", desc:"Reach peak with Aikinite Orb", icon:"🟤", xp:120 },\n'
    '  { id:"dawn_glow44_use", label:"Dawn Glow", desc:"Activate DAWN_GLOW44 power-up", icon:"🌅", xp:65 },\n'
    '  { id:"dawn_glow44_max", label:"Dawn Master", desc:"Reach max score with DAWN_GLOW44 active", icon:"🌄", xp:130 },\n'
    '  { id:"dusk_glow44_use", label:"Dusk Glow", desc:"Activate DUSK_GLOW44 power-up", icon:"🌆", xp:65 },\n'
    '  { id:"dusk_glow44_max", label:"Dusk Master", desc:"Reach max score with DUSK_GLOW44 active", icon:"🌇", xp:130 },\n'
    '  { id:"ajoite_fox9e_tap", label:"Ajoite Fox", desc:"Tap an Ajoite Fox target", icon:"🦊", xp:75 },\n'
    '  { id:"ajoite_fox9e_peak", label:"Ajoite Fox Peak", desc:"Hit Ajoite Fox at peak glow", icon:"🟢", xp:150 },\n'
    '  { id:"akermanite_orb9e_tap", label:"Akermanite Orb", desc:"Tap an Akermanite Orb target", icon:"🔮", xp:75 },\n'
    '  { id:"akermanite_orb9e_peak", label:"Akermanite Orb Peak", desc:"Hit Akermanite Orb at peak glow", icon:"🟠", xp:150 },'
)
assert src.count(A1_OLD) == 1, f"Step1 anchor count: {src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW)

# ── STEP 2: add DAWN_GLOW44, DUSK_GLOW44 to power-up list ─────────────────
A2_OLD = '"STAR_GLOW44","MOON_GLOW44","NOVA_GLOW44"'
A2_NEW = '"DAWN_GLOW44","DUSK_GLOW44","STAR_GLOW44","MOON_GLOW44","NOVA_GLOW44"'
assert src.count(A2_OLD) == 1, f"Step2 anchor count: {src.count(A2_OLD)}"
src = src.replace(A2_OLD, A2_NEW)

# ── STEP 3: add power-up handler ───────────────────────────────────────────
A3_OLD = '  } else if(ptype==="STAR_GLOW44"){'
A3_NEW = (
    '  } else if(ptype==="DAWN_GLOW44"){\n'
    '    gs.score+=2348;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2058,text:"+2348",color:"#f97316",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#f97316",life:0.7});\n'
    '    sfx("powerUp");unlock("dawn_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("dawn_glow44_max");\n'
    '  } else if(ptype==="DUSK_GLOW44"){\n'
    '    gs.score+=2350;setHud(h=>({...h,score:gs.score}));\n'
    '    spawnParticle({type:"popup",x:cx,y:cy-2060,text:"+2350",color:"#7c3aed",life:1.1});\n'
    '    spawnParticle({type:"shockwave",x:cx,y:cy,color:"#7c3aed",life:0.7});\n'
    '    sfx("powerUp");unlock("dusk_glow44_use");\n'
    '    if(gs.score>=saveRef.current.highScore)unlock("dusk_glow44_max");\n'
    '  } else if(ptype==="STAR_GLOW44"){'
)
assert src.count(A3_OLD) == 1, f"Step3 anchor count: {src.count(A3_OLD)}"
src = src.replace(A3_OLD, A3_NEW)

# ── STEP 4: comment block ─────────────────────────────────────────────────
A4_OLD = '  // STAR_GLOW44 — +2344 star glow bonus'
A4_NEW = (
    '  // DAWN_GLOW44 — +2348 dawn glow bonus\n'
    '  // DUSK_GLOW44 — +2350 dusk glow bonus\n'
    '  // STAR_GLOW44 — +2344 star glow bonus'
)
assert src.count(A4_OLD) == 1, f"Step4 anchor count: {src.count(A4_OLD)}"
src = src.replace(A4_OLD, A4_NEW)

# ── STEP 5: draw functions ─────────────────────────────────────────────────
A5_OLD = 'function drawAheyliteFox9e('
A5_NEW = (
    'function drawAjoiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4083)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#a7f3d0");g.addColorStop(0.45+sp*0.35,"#34d399");g.addColorStop(1,"#059669");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(52,211,153,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#059669":"#ecfdf5";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🟢":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAkermaniteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4087);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fed7aa");g.addColorStop(0.35+tp*0.35,"#fb923c");g.addColorStop(1,"#c2410c");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(251,146,60,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(251,146,60,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#fb923c":"#fff7ed";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟠":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawAheyliteFox9e('
)
assert src.count(A5_OLD) == 1, f"Step5 anchor count: {src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW)

# ── STEP 6: draw dispatch ─────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="aheylite_fox9e"){'
A6_NEW = (
    '  else if(t.type==="ajoite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp2=Math.min(1,(ts-t.born)/2194);\n'
    '    drawAjoiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="akermanite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp2=Math.min(1,(ts-t.born)/2196);\n'
    '    drawAkermaniteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
    '  }\n'
    '  else if(t.type==="aheylite_fox9e"){'
)
assert src.count(A6_OLD) == 1, f"Step6 anchor count: {src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW)

# ── STEP 7: handleTap handlers ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="aheylite_fox9e"){'
A7_NEW = (
    '    if(hit.type==="ajoite_fox9e"){\n'
    '      const sp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(426*(1+sp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(sp2>0.88?" 🟢":""),color:"#34d399",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#34d399",life:0.55});\n'
    '      if(sp2>0.88){sfx("legendary");unlock("ajoite_fox9e_peak");}else sfx("tap");\n'
    '      unlock("ajoite_fox9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="akermanite_orb9e"){\n'
    '      const tp2=Math.min(1,(performance.now()-hit.born)/hit.lifetime);\n'
    '      const pts=Math.round(421*(1+tp2));gs.score+=pts;gs.streak++;\n'
    '      spawnParticle({type:"popup",x:hit.x,y:hit.y-30,text:"+"+pts+(tp2>0.88?" 🟠":""),color:"#fb923c",life:1.0});\n'
    '      spawnParticle({type:"shockwave",x:hit.x,y:hit.y,color:"#fb923c",life:0.55});\n'
    '      if(tp2>0.88){sfx("legendary");unlock("akermanite_orb9e_peak");}else sfx("tap");\n'
    '      unlock("akermanite_orb9e_tap");updateMissions({...gs.sessionStats,tapsTotal:1});\n'
    '    } else if(hit.type==="aheylite_fox9e"){'
)
assert src.count(A7_OLD) == 1, f"Step7 anchor count: {src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW)

# ── STEP 8: spawnTarget entries ────────────────────────────────────────────
A8_OLD = ('      type="aheylite_fox9e";color="#f472b6";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="aikinite_orb9e"')
A8_NEW = (
    '      type="ajoite_fox9e";color="#34d399";glow="#ecfdf5";\n'
    '    } else if('+COND100F+'){\n'
    '      type="akermanite_orb9e";color="#fb923c";glow="#fff7ed";\n'
    '    } else if('+COND100F+'){\n'
    '      type="aheylite_fox9e";color="#f472b6";glow="#fdf2f8";\n'
    '    } else if('+COND100F+'){\n'
    '      type="aikinite_orb9e"'
)
assert src.count(A8_OLD) == 1, f"Step8 anchor count: {src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW)

# ── STEP 9: radius table ───────────────────────────────────────────────────
A9_OLD = 'type==="aheylite_fox9e"?BASE_R*1.65:type==="aikinite_orb9e"?BASE_R*1.64:'
A9_NEW = 'type==="ajoite_fox9e"?BASE_R*1.66:type==="akermanite_orb9e"?BASE_R*1.65:type==="aheylite_fox9e"?BASE_R*1.65:type==="aikinite_orb9e"?BASE_R*1.64:'
assert src.count(A9_OLD) == 1, f"Step9 anchor count: {src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW)

# ── STEP 10: icon map (replace_all, expect 2) ─────────────────────────────
A10_OLD = 'STAR_GLOW44:"⭐✨",MOON_GLOW44:"🌙✨",NOVA_GLOW44:"💥✨"'
A10_NEW = 'DAWN_GLOW44:"🌅✨",DUSK_GLOW44:"🌆✨",STAR_GLOW44:"⭐✨",MOON_GLOW44:"🌙✨",NOVA_GLOW44:"💥✨"'
cnt = src.count(A10_OLD)
assert cnt == 2, f"Step10 icon map count: {cnt}"
src = src.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(src)

print(f"Batch 721 done! +{len(src)-orig_len} bytes")
