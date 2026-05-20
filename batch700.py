#!/usr/bin/env python3
"""Batch 700: STAR_GLOW42+MOON_GLOW42 + SynchysiteFox9e+TangeiteOrb9e + 8 achievements"""
import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"sulvanite_orb9e_peak", label:"Sulvanite Orb Peak", desc:"Reach peak with Sulvanite Orb", icon:"🟤", xp:120 },'
A1_NEW = (
    '{ id:"sulvanite_orb9e_peak", label:"Sulvanite Orb Peak", desc:"Reach peak with Sulvanite Orb", icon:"🟤", xp:120 },\n'
    '  { id:"star_glow42_use", label:"Star Glow 42", desc:"Activate STAR_GLOW42 power-up", icon:"⭐", xp:60 },\n'
    '  { id:"star_glow42_max", label:"Star Glower 42", desc:"Reach max with STAR_GLOW42 active", icon:"⭐", xp:120 },\n'
    '  { id:"moon_glow42_use", label:"Moon Glow 42", desc:"Activate MOON_GLOW42 power-up", icon:"🌙", xp:60 },\n'
    '  { id:"moon_glow42_max", label:"Moon Glower 42", desc:"Reach max with MOON_GLOW42 active", icon:"🌙", xp:120 },\n'
    '  { id:"synchysite_fox9e_tap", label:"Synchysite Fox", desc:"Tap a Synchysite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"synchysite_fox9e_peak", label:"Synchysite Fox Peak", desc:"Reach peak with Synchysite Fox", icon:"🌊", xp:120 },\n'
    '  { id:"tangeite_orb9e_tap", label:"Tangeite Orb", desc:"Tap a Tangeite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"tangeite_orb9e_peak", label:"Tangeite Orb Peak", desc:"Reach peak with Tangeite Orb", icon:"🟫", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="NOVA_GLOW42"){\n'
          '        gs.score+=2260;showPopup(cx,cy-1970,"+2260 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a041e",2132);if(gs.score>=bonusTotal)unlock("nova_glow42_max");')
A3_NEW = ('  } else if(ptype==="STAR_GLOW42"){\n'
          '        gs.score+=2264;showPopup(cx,cy-1974,"+2264 ⭐",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2136);if(gs.score>=bonusTotal)unlock("star_glow42_max");\n'
          '      } else if(ptype==="MOON_GLOW42"){\n'
          '        gs.score+=2266;showPopup(cx,cy-1976,"+2266 🌙",theme.accent,26);spawnShockwave(cx,cy,"#818cf8",2138);if(gs.score>=bonusTotal)unlock("moon_glow42_max");\n'
          '      } else if(ptype==="NOVA_GLOW42"){\n'
          '        gs.score+=2260;showPopup(cx,cy-1970,"+2260 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a041e",2132);if(gs.score>=bonusTotal)unlock("nova_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // NOVA_GLOW42 — +2260 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW42"){sfx("powerUp",1923);unlock("nova_glow42_use");}')
A4_NEW = ('  // STAR_GLOW42 — +2264 star glow bonus\n'
          '      if(ptype==="STAR_GLOW42"){sfx("powerUp",1927);unlock("star_glow42_use");}\n'
          '  // MOON_GLOW42 — +2266 moon glow bonus\n'
          '      if(ptype==="MOON_GLOW42"){sfx("powerUp",1929);unlock("moon_glow42_use");}\n'
          '  // NOVA_GLOW42 — +2260 nova glow bonus\n'
          '      if(ptype==="NOVA_GLOW42"){sfx("powerUp",1923);unlock("nova_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSulfohaliteFox9e('
A5_NEW = (
    'function drawSynchysiteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3937)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#cffafe");g.addColorStop(0.45+sp*0.35,"#0891b2");g.addColorStop(1,"#0e7490");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(8,145,178,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#0e7490":"#cffafe";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌊":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTangeiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3941);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fde68a");g.addColorStop(0.35+tp*0.35,"#92400e");g.addColorStop(1,"#78350f");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(146,64,14,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(146,64,14,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#92400e":"#fde68a";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"🟫":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawSulfohaliteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="sulfohalite_fox9e"){'
A6_NEW = (
    'else if(t.type==="synchysite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2110);\n'
    '    drawSynchysiteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="tangeite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2112);\n'
    '    drawTangeiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="sulfohalite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="sulfohalite_fox9e"){'
A7_NEW = (
    'if(hit.type==="synchysite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2110);\n'
    '      const pts=Math.round(384*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#0891b2",2110);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌊","#cffafe",22);\n'
    '      unlock("synchysite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("synchysite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tangeite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2112);\n'
    '      const pts=Math.round(379*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#92400e",2112);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🟫","#fde68a",22);\n'
    '      unlock("tangeite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("tangeite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="sulfohalite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="sulfohalite_fox9e";color="#64748b";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sulvanite_orb9e"')
A8_NEW = ('      type="synchysite_fox9e";color="#0891b2";glow="#cffafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tangeite_orb9e";color="#92400e";glow="#fde68a";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sulfohalite_fox9e";color="#64748b";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sulvanite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="sulfohalite_fox9e"?BASE_R*1.44:type==="sulvanite_orb9e"?BASE_R*1.43:'
A9_NEW = 'type==="synchysite_fox9e"?BASE_R*1.45:type==="tangeite_orb9e"?BASE_R*1.44:type==="sulfohalite_fox9e"?BASE_R*1.44:type==="sulvanite_orb9e"?BASE_R*1.43:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 700 done! +{len(code)-ORIG} bytes")
