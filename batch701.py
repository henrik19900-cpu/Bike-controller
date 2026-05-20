#!/usr/bin/env python3
"""Batch 701: DAWN_GLOW42+DUSK_GLOW42 + SzomolnokiteFox9e+TarbutiteOrb9e + 8 achievements"""
import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"tangeite_orb9e_peak", label:"Tangeite Orb Peak", desc:"Reach peak with Tangeite Orb", icon:"🟫", xp:120 },'
A1_NEW = (
    '{ id:"tangeite_orb9e_peak", label:"Tangeite Orb Peak", desc:"Reach peak with Tangeite Orb", icon:"🟫", xp:120 },\n'
    '  { id:"dawn_glow42_use", label:"Dawn Glow 42", desc:"Activate DAWN_GLOW42 power-up", icon:"🌅", xp:60 },\n'
    '  { id:"dawn_glow42_max", label:"Dawn Glower 42", desc:"Reach max with DAWN_GLOW42 active", icon:"🌅", xp:120 },\n'
    '  { id:"dusk_glow42_use", label:"Dusk Glow 42", desc:"Activate DUSK_GLOW42 power-up", icon:"🌇", xp:60 },\n'
    '  { id:"dusk_glow42_max", label:"Dusk Glower 42", desc:"Reach max with DUSK_GLOW42 active", icon:"🌇", xp:120 },\n'
    '  { id:"szomolnokite_fox9e_tap", label:"Szomolnokite Fox", desc:"Tap a Szomolnokite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"szomolnokite_fox9e_peak", label:"Szomolnokite Fox Peak", desc:"Reach peak with Szomolnokite Fox", icon:"🔥", xp:120 },\n'
    '  { id:"tarbuttite_orb9e_tap", label:"Tarbuttite Orb", desc:"Tap a Tarbuttite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"tarbuttite_orb9e_peak", label:"Tarbuttite Orb Peak", desc:"Reach peak with Tarbuttite Orb", icon:"🟢", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="STAR_GLOW42"){\n'
          '        gs.score+=2264;showPopup(cx,cy-1974,"+2264 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2136);if(gs.score>=bonusTotal)unlock("star_glow42_max");')
A3_NEW = ('  } else if(ptype==="DAWN_GLOW42"){\n'
          '        gs.score+=2268;showPopup(cx,cy-1978,"+2268 🌅",theme.accent,26);spawnShockwave(cx,cy,"#f97316",2140);if(gs.score>=bonusTotal)unlock("dawn_glow42_max");\n'
          '      } else if(ptype==="DUSK_GLOW42"){\n'
          '        gs.score+=2270;showPopup(cx,cy-1980,"+2270 🌇",theme.accent,26);spawnShockwave(cx,cy,"#7c3aed",2142);if(gs.score>=bonusTotal)unlock("dusk_glow42_max");\n'
          '      } else if(ptype==="STAR_GLOW42"){\n'
          '        gs.score+=2264;showPopup(cx,cy-1974,"+2264 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2136);if(gs.score>=bonusTotal)unlock("star_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // STAR_GLOW42 — +2264 star glow bonus\n'
          '      if(ptype==="STAR_GLOW42"){sfx("powerUp",1927);unlock("star_glow42_use");}')
A4_NEW = ('  // DAWN_GLOW42 — +2268 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW42"){sfx("powerUp",1931);unlock("dawn_glow42_use");}\n'
          '  // DUSK_GLOW42 — +2270 dusk glow bonus\n'
          '      if(ptype==="DUSK_GLOW42"){sfx("powerUp",1933);unlock("dusk_glow42_use");}\n'
          '  // STAR_GLOW42 — +2264 star glow bonus\n'
          '      if(ptype==="STAR_GLOW42"){sfx("powerUp",1927);unlock("star_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSynchysiteFox9e('
A5_NEW = (
    'function drawSzomolnokiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3944)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fef9c3");g.addColorStop(0.45+sp*0.35,"#ca8a04");g.addColorStop(1,"#92400e");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(202,138,4,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#92400e":"#fef9c3";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🔥":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTarbuttiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3948);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#dcfce7");g.addColorStop(0.35+tp*0.35,"#16a34a");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(22,163,74,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(22,163,74,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#16a34a":"#dcfce7";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟢":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawSynchysiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="synchysite_fox9e"){'
A6_NEW = (
    'else if(t.type==="szomolnokite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2114);\n'
    '    drawSzomolnokiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="tarbuttite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2116);\n'
    '    drawTarbuttiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="synchysite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="synchysite_fox9e"){'
A7_NEW = (
    'if(hit.type==="szomolnokite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2114);\n'
    '      const pts=Math.round(386*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#ca8a04",2114);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🔥","#fef9c3",22);\n'
    '      unlock("szomolnokite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("szomolnokite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tarbuttite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2116);\n'
    '      const pts=Math.round(381*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#16a34a",2116);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🟢","#dcfce7",22);\n'
    '      unlock("tarbuttite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("tarbuttite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="synchysite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="synchysite_fox9e";color="#0891b2";glow="#cffafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tangeite_orb9e"')
A8_NEW = ('      type="szomolnokite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tarbuttite_orb9e";color="#16a34a";glow="#dcfce7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="synchysite_fox9e";color="#0891b2";glow="#cffafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tangeite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="synchysite_fox9e"?BASE_R*1.45:type==="tangeite_orb9e"?BASE_R*1.44:'
A9_NEW = 'type==="szomolnokite_fox9e"?BASE_R*1.46:type==="tarbuttite_orb9e"?BASE_R*1.45:type==="synchysite_fox9e"?BASE_R*1.45:type==="tangeite_orb9e"?BASE_R*1.44:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 701 done! +{len(code)-ORIG} bytes")
