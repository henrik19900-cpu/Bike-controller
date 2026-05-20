#!/usr/bin/env python3
"""Batch 714: LIGHT_GLOW43+DARK_GLOW43 + XonotliteFox9e+ZeuneriteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"xanthite_orb9e_peak", label:"Xanthite Orb Peak", desc:"Reach peak with Xanthite Orb", icon:"🌼", xp:120 },'
A1_NEW = (
    '{ id:"xanthite_orb9e_peak", label:"Xanthite Orb Peak", desc:"Reach peak with Xanthite Orb", icon:"🌼", xp:120 },\n'
    '  { id:"light_glow43_use", label:"Light Glow 43", desc:"Activate LIGHT_GLOW43 power-up", icon:"💡", xp:60 },\n'
    '  { id:"light_glow43_max", label:"Light Glower 43", desc:"Reach max with LIGHT_GLOW43 active", icon:"💡", xp:120 },\n'
    '  { id:"dark_glow43_use", label:"Dark Glow 43", desc:"Activate DARK_GLOW43 power-up", icon:"🌑", xp:60 },\n'
    '  { id:"dark_glow43_max", label:"Dark Glower 43", desc:"Reach max with DARK_GLOW43 active", icon:"🌑", xp:120 },\n'
    '  { id:"xonotlite_fox9e_tap", label:"Xonotlite Fox", desc:"Tap a Xonotlite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"xonotlite_fox9e_peak", label:"Xonotlite Fox Peak", desc:"Reach peak with Xonotlite Fox", icon:"🌟", xp:120 },\n'
    '  { id:"zeunerite_orb9e_tap", label:"Zeunerite Orb", desc:"Tap a Zeunerite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"zeunerite_orb9e_peak", label:"Zeunerite Orb Peak", desc:"Reach peak with Zeunerite Orb", icon:"💚", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"WIND_GLOW43","STORM_GLOW43","FIRE_GLOW43","ICE_GLOW43"'
A2_NEW = '"LIGHT_GLOW43","DARK_GLOW43","WIND_GLOW43","STORM_GLOW43","FIRE_GLOW43","ICE_GLOW43"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="WIND_GLOW43"){\n'
          '        gs.score+=2316;showPopup(cx,cy-2026,"+2316 💨",theme.accent,26);spawnShockwave(cx,cy,"#84cc16",2188);if(gs.score>=bonusTotal)unlock("wind_glow43_max");')
A3_NEW = ('  } else if(ptype==="LIGHT_GLOW43"){\n'
          '        gs.score+=2320;showPopup(cx,cy-2030,"+2320 💡",theme.accent,26);spawnShockwave(cx,cy,"#fbbf24",2192);if(gs.score>=bonusTotal)unlock("light_glow43_max");\n'
          '      } else if(ptype==="DARK_GLOW43"){\n'
          '        gs.score+=2322;showPopup(cx,cy-2032,"+2322 🌑",theme.accent,26);spawnShockwave(cx,cy,"#1e1b4b",2194);if(gs.score>=bonusTotal)unlock("dark_glow43_max");\n'
          '      } else if(ptype==="WIND_GLOW43"){\n'
          '        gs.score+=2316;showPopup(cx,cy-2026,"+2316 💨",theme.accent,26);spawnShockwave(cx,cy,"#84cc16",2188);if(gs.score>=bonusTotal)unlock("wind_glow43_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // WIND_GLOW43 — +2316 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW43"){sfx("powerUp",1979);unlock("wind_glow43_use");}')
A4_NEW = ('  // LIGHT_GLOW43 — +2320 light glow bonus\n'
          '      if(ptype==="LIGHT_GLOW43"){sfx("powerUp",1983);unlock("light_glow43_use");}\n'
          '  // DARK_GLOW43 — +2322 dark glow bonus\n'
          '      if(ptype==="DARK_GLOW43"){sfx("powerUp",1985);unlock("dark_glow43_use");}\n'
          '  // WIND_GLOW43 — +2316 wind glow bonus\n'
          '      if(ptype==="WIND_GLOW43"){sfx("powerUp",1979);unlock("wind_glow43_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawWitheriteFox9e('
A5_NEW = (
    'function drawXonotliteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.4035)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#fff1f2");g.addColorStop(0.45+sp*0.35,"#fb7185");g.addColorStop(1,"#9f1239");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(251,113,133,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#9f1239":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌟":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawZeuneriteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.4039);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+tp*0.35,"#4ade80");g.addColorStop(1,"#14532d");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(74,222,128,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(74,222,128,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#4ade80":"#f0fdf4";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"💚":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawWitheriteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="witherite_fox9e"){'
A6_NEW = (
    'else if(t.type==="xonotlite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2166);\n'
    '    drawXonotliteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="zeunerite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2168);\n'
    '    drawZeuneriteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="witherite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="witherite_fox9e"){'
A7_NEW = (
    'if(hit.type==="xonotlite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2166);\n'
    '      const pts=Math.round(412*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#fb7185",2166);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌟","#fff1f2",22);\n'
    '      unlock("xonotlite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("xonotlite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="zeunerite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2168);\n'
    '      const pts=Math.round(407*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#4ade80",2168);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 💚","#f0fdf4",22);\n'
    '      unlock("zeunerite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("zeunerite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="witherite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="witherite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="xanthite_orb9e"')
A8_NEW = ('      type="xonotlite_fox9e";color="#fb7185";glow="#fff1f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zeunerite_orb9e";color="#4ade80";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="witherite_fox9e";color="#94a3b8";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="xanthite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="witherite_fox9e"?BASE_R*1.58:type==="xanthite_orb9e"?BASE_R*1.57:'
A9_NEW = 'type==="xonotlite_fox9e"?BASE_R*1.59:type==="zeunerite_orb9e"?BASE_R*1.58:type==="witherite_fox9e"?BASE_R*1.58:type==="xanthite_orb9e"?BASE_R*1.57:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'WIND_GLOW43:"💨✨",STORM_GLOW43:"⛈️✨",FIRE_GLOW43:"🔥✨"'
A10_NEW = 'LIGHT_GLOW43:"💡✨",DARK_GLOW43:"🌑✨",WIND_GLOW43:"💨✨",STORM_GLOW43:"⛈️✨",FIRE_GLOW43:"🔥✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 714 done! +{len(code)-ORIG} bytes")
