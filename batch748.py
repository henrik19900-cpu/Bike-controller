import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

orig_len = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

FOX   = "coloradoite_fox9e"
ORB   = "columbite_orb9e"
PW1   = "VORTEX_GLOW44"
PW2   = "SURGE_GLOW44"
PW1SC = 2456
PW2SC = 2458
FOXSC = 480
ORBSC = 475
FOX_R = "BASE_R*1.93"
ORB_R = "BASE_R*1.92"
OSC   = "0.4241"
SW    = "2290"
FOX_C = "#b91c1c"; FOX_G = "#fef2f2"
ORB_C = "#0f766e"; ORB_G = "#f0fdfa"
FOX_L = "#fca5a5"; FOX_M = "#ef4444"; FOX_D = "#450a0a"
FOX_RL,FOX_RG,FOX_RB = 252,165,165
ORB_L = "#5eead4"; ORB_M = "#0d9488"; ORB_D = "#042f2e"
ORB_RL,ORB_RG,ORB_RB = 94,234,212
PW1C = "#8b5cf6"; PW2C = "#0ea5e9"
PEAK_FOX = "🔴"; PEAK_ORB = "🌿"

# STEP 1
A1_ANCHOR = '{ id:"churchite_fox9e_tap", label:"Churchite Fox Tap"'
assert A1_ANCHOR in code, "S1 anchor missing"
A1_NEW = (
  '{ id:"coloradoite_fox9e_tap", label:"Coloradoite Fox Tap", desc:"Tap Coloradoite Fox", icon:"🦊", xp:62 },\n'
  '  { id:"coloradoite_fox9e_peak", label:"Coloradoite Fox Peak", desc:"Hit Coloradoite Fox at peak", icon:"🔴", xp:78 },\n'
  '  { id:"columbite_orb9e_tap", label:"Columbite Orb Tap", desc:"Tap Columbite Orb", icon:"🔮", xp:60 },\n'
  '  { id:"columbite_orb9e_peak", label:"Columbite Orb Peak", desc:"Hit Columbite Orb at peak", icon:"🌿", xp:76 },\n'
  '  { id:"vortex_glow44_use", label:"Vortex Glow Use", desc:"Collect Vortex Glow power-up", icon:"🌀", xp:44 },\n'
  '  { id:"vortex_glow44_max", label:"Vortex Glow Max", desc:"Collect 5 Vortex Glow power-ups", icon:"🌀", xp:88 },\n'
  '  { id:"surge_glow44_use", label:"Surge Glow Use", desc:"Collect Surge Glow power-up", icon:"⚡", xp:44 },\n'
  '  { id:"surge_glow44_max", label:"Surge Glow Max", desc:"Collect 5 Surge Glow power-ups", icon:"⚡", xp:88 },\n'
  '  { id:"churchite_fox9e_tap", label:"Churchite Fox Tap"'
)
code = code.replace(A1_ANCHOR, A1_NEW, 1)
assert '{ id:"coloradoite_fox9e_tap"' in code, "S1 failed"
print("S1 ok")

# STEP 2
A2_ANCHOR = '"ZENITH_GLOW44","APEX_GLOW44","SPARK_GLOW44"'
assert A2_ANCHOR in code, "S2 anchor missing"
A2_NEW = f'"{PW1}","{PW2}","ZENITH_GLOW44","APEX_GLOW44","SPARK_GLOW44"'
code = code.replace(A2_ANCHOR, A2_NEW, 1)
assert f'"{PW1}"' in code, "S2 failed"
print("S2 ok")

# STEP 3
A3_ANCHOR = '} else if(ptype==="ZENITH_GLOW44"){'
assert A3_ANCHOR in code, "S3 anchor missing"
A3_NEW = (
  f'}} else if(ptype==="{PW1}"){{gs.score+=Math.round({PW1SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW1C}");'
  f'setNotif("VORTEX GLOW +{PW1SC}!");'
  f'}} else if(ptype==="{PW2}"){{gs.score+=Math.round({PW2SC}*multi);addParticle(hit.x,hit.y,"shockwave","{PW2C}");'
  f'setNotif("SURGE GLOW +{PW2SC}!");'
  f'}} else if(ptype==="ZENITH_GLOW44"){{'
)
code = code.replace(A3_ANCHOR, A3_NEW, 1)
assert f'ptype==="{PW1}"' in code, "S3 failed"
print("S3 ok")

# STEP 4
A4_ANCHOR = '// ZENITH_GLOW44 — +2452 zenith glow bonus'
assert A4_ANCHOR in code, "S4 anchor missing"
A4_NEW = (
  f'// {PW1} — +{PW1SC} vortex glow bonus\n'
  f'      // {PW2} — +{PW2SC} surge glow bonus\n'
  f'      // ZENITH_GLOW44 — +2452 zenith glow bonus'
)
code = code.replace(A4_ANCHOR, A4_NEW, 1)
assert f'// {PW1}' in code, "S4 failed"
print("S4 ok")

# STEP 5
A5_ANCHOR = 'function drawChurchiteFox9e('
assert A5_ANCHOR in code, "S5 anchor missing"
DRAW = (
f'function drawColoradoiteFox9e(ctx,r,ts,sp){{\n'
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
f'function drawColumbiteOrb9e(ctx,r,ts,tp){{\n'
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
f'function drawChurchiteFox9e('
)
code = code.replace(A5_ANCHOR, DRAW, 1)
assert 'function drawColoradoiteFox9e(' in code, "S5 failed"
print("S5 ok")

# STEP 6
A6_ANCHOR = '  else if(t.type==="churchite_fox9e"){'
assert A6_ANCHOR in code, "S6 anchor missing"
A6_NEW = (
f'  else if(t.type==="{FOX}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const sp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawColoradoiteFox9e(ctx,t.radius,ts,sp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="{ORB}"){{\n'
f'    ctx.save();ctx.translate(t.x,t.y);\n'
f'    const tp2=Math.min(1,(ts-t.born)/{SW});\n'
f'    drawColumbiteOrb9e(ctx,t.radius,ts,tp2);ctx.restore();\n'
f'  }}\n'
f'  else if(t.type==="churchite_fox9e"){{'
)
code = code.replace(A6_ANCHOR, A6_NEW, 1)
assert f't.type==="{FOX}"' in code, "S6 failed"
print("S6 ok")

# STEP 7
A7_ANCHOR = 'if(hit.type==="churchite_fox9e"){'
assert A7_ANCHOR in code, "S7 anchor missing"
A7_NEW = (
f'if(hit.type==="{FOX}"){{\n'
f'      const sp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=sp>0.88;\n'
f'      const pts=Math.round({FOXSC}*(1+sp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{FOX_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🦊 +"+pts);\n'
f'      if(isPeak)unlock("coloradoite_fox9e_peak");\n'
f'      unlock("coloradoite_fox9e_tap");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("rare");vibrate([30]);\n'
f'    }}else if(hit.type==="{ORB}"){{\n'
f'      const tp=Math.min(1,(performance.now()-hit.born)/{SW});\n'
f'      const isPeak=tp>0.88;\n'
f'      const pts=Math.round({ORBSC}*(1+tp*0.7)*multi*(isPeak?2.1:1));\n'
f'      gs.score+=pts;gs.streak++;gs.sessionStats.rareHits++;\n'
f'      addParticle(hit.x,hit.y,"shockwave","{ORB_C}");\n'
f'      addParticle(hit.x,hit.y,"popup",isPeak?"PEAK! +"+pts:"🔮 +"+pts);\n'
f'      if(isPeak)unlock("columbite_orb9e_peak");\n'
f'      unlock("columbite_orb9e_tap");\n'
f'      updateMissions({{...gs.sessionStats,rareHits:gs.sessionStats.rareHits}});\n'
f'      sfx("epic");vibrate([40,10,20]);\n'
f'    }}else if(hit.type==="churchite_fox9e"){{'
)
code = code.replace(A7_ANCHOR, A7_NEW, 1)
assert f'hit.type==="{FOX}"' in code, "S7 failed"
print("S7 ok")

# STEP 8
A8_OLD = ('      type="churchite_fox9e";color="#1d4ed8";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="clinohumite_orb9e"')
assert A8_OLD in code, "S8 anchor missing"
A8_NEW = (
    f'      type="{FOX}";color="{FOX_C}";glow="{FOX_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB}";color="{ORB_C}";glow="{ORB_G}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="churchite_fox9e";color="#1d4ed8";glow="#eff6ff";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="clinohumite_orb9e"'
)
code = code.replace(A8_OLD, A8_NEW, 1)
assert f'type="{FOX}"' in code, "S8 failed"
print("S8 ok")

# STEP 9
A9_ANCHOR = 'type==="churchite_fox9e"?BASE_R*1.92:type==="clinohumite_orb9e"?BASE_R*1.91:'
assert A9_ANCHOR in code, "S9 anchor missing"
A9_NEW = f'type==="{FOX}"?{FOX_R}:type==="{ORB}"?{ORB_R}:{A9_ANCHOR}'
code = code.replace(A9_ANCHOR, A9_NEW, 1)
assert f'type==="{FOX}"?{FOX_R}' in code, "S9 failed"
print("S9 ok")

# STEP 10
A10_ANCHOR = 'ZENITH_GLOW44:"🌀✨",APEX_GLOW44:"🔱✨",SPARK_GLOW44:"⚡✨"'
cnt = code.count(A10_ANCHOR)
assert cnt == 2, f"S10 anchor count={cnt}, expected 2"
A10_NEW = f'{PW1}:"🌀✨",{PW2}:"⚡✨",ZENITH_GLOW44:"🌀✨",APEX_GLOW44:"🔱✨",SPARK_GLOW44:"⚡✨"'
code = code.replace(A10_ANCHOR, A10_NEW)
assert code.count(A10_NEW) == 2, "S10 replace_all failed"
print("S10 ok")

with open(SRC, "w") as f:
    f.write(code)
print(f"Batch 748 done! +{len(code)-orig_len} bytes")
