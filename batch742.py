import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

orig_len = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'
BASE_R = "BASE_R"

# ── names ──────────────────────────────────────────────────────────────
FOX   = "calomel_fox9e"
ORB   = "carminite_orb9e"
PW1   = "SHADOW_GLOW44"
PW2   = "AETHER_GLOW44"
PW1SC = 2432
PW2SC = 2434
FOXSC = 468
ORBSC = 463
FOX_R = "BASE_R*1.87"
ORB_R = "BASE_R*1.86"
OSC   = "0.4217"
SW    = "2278"
FOX_C = "#6d28d9"; FOX_G = "#f5f3ff"
ORB_C = "#0891b2"; ORB_G = "#ecfeff"
FOX_L = "#c4b5fd"; FOX_M = "#8b5cf6"; FOX_D = "#3b0764"
FOX_RL,FOX_RG,FOX_RB = 196,181,253
ORB_L = "#67e8f9"; ORB_M = "#0e7490"; ORB_D = "#083344"
ORB_RL,ORB_RG,ORB_RB = 103,232,249
PW1C = "#7c3aed"; PW2C = "#06b6d4"
PEAK_FOX = "🔮"; PEAK_ORB = "💎"

# ── STEP 1: achievements ────────────────────────────────────────────────
A1_ANCHOR = '{ id:"caledonite_orb9e_peak", label:"Caledonite Orb Peak"'
assert A1_ANCHOR in code, "S1 anchor missing"
A1_NEW = (
  '{ id:"calomel_fox9e_tap", label:"Calomel Fox Tap", desc:"Tap Calomel Fox", icon:"🦊", xp:62 },\n'
  '  { id:"calomel_fox9e_peak", label:"Calomel Fox Peak", desc:"Hit Calomel Fox at peak", icon:"🔮", xp:78 },\n'
  '  { id:"carminite_orb9e_tap", label:"Carminite Orb Tap", desc:"Tap Carminite Orb", icon:"🔮", xp:60 },\n'
  '  { id:"carminite_orb9e_peak", label:"Carminite Orb Peak", desc:"Hit Carminite Orb at peak", icon:"💎", xp:76 },\n'
  '  { id:"shadow_glow44_use", label:"Shadow Glow Use", desc:"Collect Shadow Glow power-up", icon:"🌑", xp:44 },\n'
  '  { id:"shadow_glow44_max", label:"Shadow Glow Max", desc:"Collect 5 Shadow Glow power-ups", icon:"🌑", xp:88 },\n'
  '  { id:"aether_glow44_use", label:"Aether Glow Use", desc:"Collect Aether Glow power-up", icon:"🌀", xp:44 },\n'
  '  { id:"aether_glow44_max", label:"Aether Glow Max", desc:"Collect 5 Aether Glow power-ups", icon:"🌀", xp:88 },\n'
  '  { id:"caledonite_orb9e_peak", label:"Caledonite Orb Peak"'
)
code = code.replace(A1_ANCHOR, A1_NEW, 1)
assert A1_NEW[:40] in code, "S1 failed"
print("S1 ok")

# ── STEP 2: power-up ID list ─────────────────────────────────────────────
A2_ANCHOR = '"ARCANE_GLOW44","INFERNO_GLOW44","PRIMAL_GLOW44"'
assert A2_ANCHOR in code, "S2 anchor missing"
A2_NEW = f'"{PW1}","{PW2}","ARCANE_GLOW44","INFERNO_GLOW44","PRIMAL_GLOW44"'
code = code.replace(A2_ANCHOR, A2_NEW, 1)
assert f'"{PW1}"' in code, "S2 failed"
print("S2 ok")

# ── STEP 3: power-up handler ──────────────────────────────────────────────
A3_ANCHOR = '} else if(ptype==="ARCANE_GLOW44"){'
assert A3_ANCHOR in code, "S3 anchor missing"
A3_NEW = (
  f'}} else if(ptype==="{PW1}"){{gs.score+=Math.round({PW1SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW1C}");'
  f'setNotif("SHADOW GLOW +{PW1SC}!");'
  f'}} else if(ptype==="{PW2}"){{gs.score+=Math.round({PW2SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW2C}");'
  f'setNotif("AETHER GLOW +{PW2SC}!");'
  f'}} else if(ptype==="ARCANE_GLOW44"){{'
)
code = code.replace(A3_ANCHOR, A3_NEW, 1)
assert f'ptype==="{PW1}"' in code, "S3 failed"
print("S3 ok")

# ── STEP 4: sfx + unlock comments ─────────────────────────────────────────
A4_ANCHOR = '// ARCANE_GLOW44 — +2428 arcane glow bonus'
assert A4_ANCHOR in code, "S4 anchor missing"
A4_NEW = (
  f'// {PW1} — +{PW1SC} shadow glow bonus\n'
  f'      // {PW2} — +{PW2SC} aether glow bonus\n'
  f'      // ARCANE_GLOW44 — +2428 arcane glow bonus'
)
code = code.replace(A4_ANCHOR, A4_NEW, 1)
assert f'// {PW1}' in code, "S4 failed"
print("S4 ok")

# ── STEP 5: draw functions ───────────────────────────────────────────────
A5_ANCHOR = 'function drawCalderiteFox9e('
assert A5_ANCHOR in code, "S5 anchor missing"
DRAW_FUNCS = (
f'function drawCalomelFox9e(ctx,r,ts,sp){{\n'
f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
f'  ctx.save();ctx.translate(0,bob);\n'
f'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
f'  g.addColorStop(0,"{FOX_L}");g.addColorStop(0.45+sp*0.35,"{FOX_M}");g.addColorStop(1,"{FOX_D}");\n'
f'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
f'  if(sp>0.65){{\n'
f'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
f'    ctx.strokeStyle="rgba({FOX_RL},{FOX_RG},{FOX_RB},"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}}\n'
f'  ctx.fillStyle=sp>0.88?"{FOX_D}":"{FOX_L}";ctx.font=(r*0.56)+"px serif";\n'
f'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"{PEAK_FOX}":"🦊",0,1);\n'
f'  ctx.restore();\n'
f'}}\n'
f'function drawCarminiteOrb9e(ctx,r,ts,tp){{\n'
f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
f'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
f'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
f'  g.addColorStop(0,"{ORB_L}");g.addColorStop(0.35+tp*0.35,"{ORB_M}");g.addColorStop(1,"{ORB_D}");\n'
f'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
f'  const ring=r*(0.54+tp*0.42);\n'
f'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
f'  ctx.strokeStyle="rgba({ORB_RL},{ORB_RG},{ORB_RB},"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
f'  ctx.globalAlpha=1;\n'
f'  if(tp>0.82){{\n'
f'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
f'    ctx.strokeStyle="rgba({ORB_RL},{ORB_RG},{ORB_RB},"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}}\n'
f'  ctx.fillStyle=tp>0.88?"{ORB_M}":"{ORB_L}";ctx.font=(r*0.56)+"px serif";\n'
f'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"{PEAK_ORB}":"🔮",0,1);\n'
f'  ctx.restore();\n'
f'}}\n'
f'function drawCalderiteFox9e('
)
code = code.replace(A5_ANCHOR, DRAW_FUNCS, 1)
assert 'function drawCalomelFox9e(' in code, "S5 failed"
print("S5 ok")

# ── STEP 6: draw dispatch ───────────────────────────────────────────────
A6_ANCHOR = '  else if(t.type==="calderite_fox9e"){'
assert A6_ANCHOR in code, "S6 anchor missing"
A6_NEW = (
f'  else if(t.type==="{FOX}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const sp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawCalomelFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="{ORB}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const tp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawCarminiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="calderite_fox9e"){{'
)
code = code.replace(A6_ANCHOR, A6_NEW, 1)
assert f't.type==="{FOX}"' in code, "S6 failed"
print("S6 ok")

# ── STEP 7: handleTap handlers ──────────────────────────────────────────
A7_ANCHOR = 'if(hit.type==="calderite_fox9e"){'
assert A7_ANCHOR in code, "S7 anchor missing"
A7_NEW = (
f'if(hit.type==="{FOX}"){{\n'
f'      const sp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=sp>0.88;\n'
f'      const pts=Math.round({FOXSC}*(1+sp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{FOX_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🦊 +"+pts);\n'
f'      if(isPeak)unlock("{FOX.replace("_fox9e","_fox9e_peak").replace("-","_")}");\n'
f'      unlock("{FOX.replace("_fox9e","_fox9e_tap").replace("-","_")}");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("rare");vibrate([30]);\n'
f'    }}else if(hit.type==="{ORB}"){{\n'
f'      const tp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=tp>0.88;\n'
f'      const pts=Math.round({ORBSC}*(1+tp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{ORB_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🔮 +"+pts);\n'
f'      if(isPeak)unlock("{ORB.replace("_orb9e","_orb9e_peak").replace("-","_")}");\n'
f'      unlock("{ORB.replace("_orb9e","_orb9e_tap").replace("-","_")}");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("epic");vibrate([40,10,20]);\n'
f'    }}else if(hit.type==="calderite_fox9e"){{'
)
code = code.replace(A7_ANCHOR, A7_NEW, 1)
assert f'hit.type==="{FOX}"' in code, "S7 failed"
print("S7 ok")

# ── STEP 8: spawnTarget entries ─────────────────────────────────────────
A8_OLD = ('      type="calderite_fox9e";color="#ef4444";glow="#fef2f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="caledonite_orb9e"')
assert A8_OLD in code, "S8 anchor missing"
A8_NEW = (
    f'      type="{FOX}";color="{FOX_C}";glow="{FOX_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB}";color="{ORB_C}";glow="{ORB_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="calderite_fox9e";color="#ef4444";glow="#fef2f2";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="caledonite_orb9e"'
)
code = code.replace(A8_OLD, A8_NEW, 1)
assert f'type="{FOX}"' in code, "S8 failed"
print("S8 ok")

# ── STEP 9: radius table ────────────────────────────────────────────────
A9_ANCHOR = 'type==="calderite_fox9e"?BASE_R*1.86:type==="caledonite_orb9e"?BASE_R*1.85:'
assert A9_ANCHOR in code, "S9 anchor missing"
A9_NEW = f'type==="{FOX}"?{FOX_R}:type==="{ORB}"?{ORB_R}:{A9_ANCHOR}'
code = code.replace(A9_ANCHOR, A9_NEW, 1)
assert f'type==="{FOX}"?{FOX_R}' in code, "S9 failed"
print("S9 ok")

# ── STEP 10: icon map ────────────────────────────────────────────────────
A10_ANCHOR = 'ARCANE_GLOW44:"🔮✨",INFERNO_GLOW44:"🔥✨",PRIMAL_GLOW44:"🌿✨"'
cnt = code.count(A10_ANCHOR)
assert cnt == 2, f"S10 anchor count={cnt}, expected 2"
A10_NEW = f'{PW1}:"🌑✨",{PW2}:"🌀✨",ARCANE_GLOW44:"🔮✨",INFERNO_GLOW44:"🔥✨",PRIMAL_GLOW44:"🌿✨"'
code = code.replace(A10_ANCHOR, A10_NEW)
assert code.count(A10_NEW) == 2, "S10 replace_all failed"
print("S10 ok")

with open(SRC, "w") as f:
    f.write(code)
print(f"Batch 742 done! +{len(code)-orig_len} bytes")
