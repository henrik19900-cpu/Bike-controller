import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

orig_len = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

FOX   = "forsterite_fox9e"
ORB   = "froodite_orb9e"
PW1   = "DESERT_GLOW44"
PW2   = "MESA_GLOW44"
PW1SC = 2504
PW2SC = 2506
FOXSC = 504
ORBSC = 499
FOX_R = "BASE_R*2.05"
ORB_R = "BASE_R*2.04"
OSC   = "0.4289"
SW    = "2314"
FOX_C = "#d97706"; FOX_G = "#fffbeb"
ORB_C = "#b91c1c"; ORB_G = "#fef2f2"
FOX_L = "#fde68a"; FOX_M = "#f59e0b"; FOX_D = "#78350f"
FOX_RL,FOX_RG,FOX_RB = 253,230,138
ORB_L = "#fca5a5"; ORB_M = "#dc2626"; ORB_D = "#450a0a"
ORB_RL,ORB_RG,ORB_RB = 252,165,165
PW1C = "#fbbf24"; PW2C = "#f97316"
PEAK_FOX = "🏜️"; PEAK_ORB = "🌋"

# STEP 1
A1_ANCHOR = '{ id:"fenaksite_fox9e_tap", label:"Fenaksite Fox Tap"'
assert A1_ANCHOR in code, "S1 anchor missing"
A1_NEW = (
  '{ id:"forsterite_fox9e_tap", label:"Forsterite Fox Tap", desc:"Tap Forsterite Fox", icon:"🦊", xp:62 },\n'
  '  { id:"forsterite_fox9e_peak", label:"Forsterite Fox Peak", desc:"Hit Forsterite Fox at peak", icon:"🏜️", xp:78 },\n'
  '  { id:"froodite_orb9e_tap", label:"Froodite Orb Tap", desc:"Tap Froodite Orb", icon:"🔮", xp:60 },\n'
  '  { id:"froodite_orb9e_peak", label:"Froodite Orb Peak", desc:"Hit Froodite Orb at peak", icon:"🌋", xp:76 },\n'
  '  { id:"desert_glow44_use", label:"Desert Glow Use", desc:"Collect Desert Glow power-up", icon:"🏜️", xp:44 },\n'
  '  { id:"desert_glow44_max", label:"Desert Glow Max", desc:"Collect 5 Desert Glow power-ups", icon:"🏜️", xp:88 },\n'
  '  { id:"mesa_glow44_use", label:"Mesa Glow Use", desc:"Collect Mesa Glow power-up", icon:"🌵", xp:44 },\n'
  '  { id:"mesa_glow44_max", label:"Mesa Glow Max", desc:"Collect 5 Mesa Glow power-ups", icon:"🌵", xp:88 },\n'
  '  { id:"fenaksite_fox9e_tap", label:"Fenaksite Fox Tap"'
)
code = code.replace(A1_ANCHOR, A1_NEW, 1)
assert '{ id:"forsterite_fox9e_tap"' in code, "S1 failed"
print("S1 ok")

# STEP 2
A2_ANCHOR = '"JUNGLE_GLOW44","SAVANNA_GLOW44","BOREAL_GLOW44"'
assert A2_ANCHOR in code, "S2 anchor missing"
A2_NEW = f'"{PW1}","{PW2}","JUNGLE_GLOW44","SAVANNA_GLOW44","BOREAL_GLOW44"'
code = code.replace(A2_ANCHOR, A2_NEW, 1)
assert f'"{PW1}"' in code, "S2 failed"
print("S2 ok")

# STEP 3
A3_ANCHOR = '} else if(ptype==="JUNGLE_GLOW44"){'
assert A3_ANCHOR in code, "S3 anchor missing"
A3_NEW = (
  f'}} else if(ptype==="{PW1}"){{gs.score+=Math.round({PW1SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW1C}");'
  f'setNotif("DESERT GLOW +{PW1SC}!");'
  f'}} else if(ptype==="{PW2}"){{gs.score+=Math.round({PW2SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW2C}");'
  f'setNotif("MESA GLOW +{PW2SC}!");'
  f'}} else if(ptype==="JUNGLE_GLOW44"){{'
)
code = code.replace(A3_ANCHOR, A3_NEW, 1)
assert f'ptype==="{PW1}"' in code, "S3 failed"
print("S3 ok")

# STEP 4
A4_ANCHOR = '// JUNGLE_GLOW44 — +2500 jungle glow bonus'
assert A4_ANCHOR in code, "S4 anchor missing"
A4_NEW = (
  f'// {PW1} — +{PW1SC} desert glow bonus\n'
  f'      // {PW2} — +{PW2SC} mesa glow bonus\n'
  f'      // JUNGLE_GLOW44 — +2500 jungle glow bonus'
)
code = code.replace(A4_ANCHOR, A4_NEW, 1)
assert f'// {PW1}' in code, "S4 failed"
print("S4 ok")

# STEP 5
A5_ANCHOR = 'function drawFenaksiteFox9e('
assert A5_ANCHOR in code, "S5 anchor missing"
DRAW = (
f'function drawForsteriteFox9e(ctx,r,ts,sp){{\n'
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
f'function drawFrooditeOrb9e(ctx,r,ts,tp){{\n'
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
f'function drawFenaksiteFox9e('
)
code = code.replace(A5_ANCHOR, DRAW, 1)
assert 'function drawForsteriteFox9e(' in code, "S5 failed"
print("S5 ok")

# STEP 6
A6_ANCHOR = '  else if(t.type==="fenaksite_fox9e"){'
assert A6_ANCHOR in code, "S6 anchor missing"
A6_NEW = (
f'  else if(t.type==="{FOX}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const sp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawForsteriteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="{ORB}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const tp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawFrooditeOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="fenaksite_fox9e"){{'
)
code = code.replace(A6_ANCHOR, A6_NEW, 1)
assert f't.type==="{FOX}"' in code, "S6 failed"
print("S6 ok")

# STEP 7
A7_ANCHOR = 'if(hit.type==="fenaksite_fox9e"){'
assert A7_ANCHOR in code, "S7 anchor missing"
A7_NEW = (
f'if(hit.type==="{FOX}"){{\n'
f'      const sp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=sp>0.88;\n'
f'      const pts=Math.round({FOXSC}*(1+sp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{FOX_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🦊 +"+pts);\n'
f'      if(isPeak)unlock("forsterite_fox9e_peak");\n'
f'      unlock("forsterite_fox9e_tap");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("rare");vibrate([30]);\n'
f'    }}else if(hit.type==="{ORB}"){{\n'
f'      const tp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=tp>0.88;\n'
f'      const pts=Math.round({ORBSC}*(1+tp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{ORB_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🔮 +"+pts);\n'
f'      if(isPeak)unlock("froodite_orb9e_peak");\n'
f'      unlock("froodite_orb9e_tap");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("epic");vibrate([40,10,20]);\n'
f'    }}else if(hit.type==="fenaksite_fox9e"){{'
)
code = code.replace(A7_ANCHOR, A7_NEW, 1)
assert f'hit.type==="{FOX}"' in code, "S7 failed"
print("S7 ok")

# STEP 8
A8_OLD = ('      type="fenaksite_fox9e";color="#065f46";glow="#ecfdf5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="fluellite_orb9e"')
assert A8_OLD in code, "S8 anchor missing"
A8_NEW = (
    f'      type="{FOX}";color="{FOX_C}";glow="{FOX_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB}";color="{ORB_C}";glow="{ORB_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="fenaksite_fox9e";color="#065f46";glow="#ecfdf5";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="fluellite_orb9e"'
)
code = code.replace(A8_OLD, A8_NEW, 1)
assert f'type="{FOX}"' in code, "S8 failed"
print("S8 ok")

# STEP 9
A9_ANCHOR = 'type==="fenaksite_fox9e"?BASE_R*2.04:type==="fluellite_orb9e"?BASE_R*2.03:'
assert A9_ANCHOR in code, "S9 anchor missing"
A9_NEW = f'type==="{FOX}"?{FOX_R}:type==="{ORB}"?{ORB_R}:{A9_ANCHOR}'
code = code.replace(A9_ANCHOR, A9_NEW, 1)
assert f'type==="{FOX}"?{FOX_R}' in code, "S9 failed"
print("S9 ok")

# STEP 10
A10_ANCHOR = 'JUNGLE_GLOW44:"🌴✨",SAVANNA_GLOW44:"🦁✨",BOREAL_GLOW44:"🌲✨"'
cnt = code.count(A10_ANCHOR)
assert cnt == 2, f"S10 anchor count={cnt}, expected 2"
A10_NEW = f'{PW1}:"🏜️✨",{PW2}:"🌵✨",JUNGLE_GLOW44:"🌴✨",SAVANNA_GLOW44:"🦁✨",BOREAL_GLOW44:"🌲✨"'
code = code.replace(A10_ANCHOR, A10_NEW)
assert code.count(A10_NEW) == 2, "S10 replace_all failed"
print("S10 ok")

with open(SRC, "w") as f:
    f.write(code)
print(f"Batch 760 done! +{len(code)-orig_len} bytes")
