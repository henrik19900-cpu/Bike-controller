#!/usr/bin/env python3
"""Batch 702: FIRE_GLOW42+ICE_GLOW42 + TelluriteFox9e+TenoiteOrb9e + 8 achievements"""

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    code = f.read()

ORIG = len(code)

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 new achievements ────────────────────────────────────────────────
A1_OLD = '{ id:"tarbuttite_orb9e_peak", label:"Tarbuttite Orb Peak", desc:"Reach peak with Tarbuttite Orb", icon:"🟢", xp:120 },'
A1_NEW = (
    '{ id:"tarbuttite_orb9e_peak", label:"Tarbuttite Orb Peak", desc:"Reach peak with Tarbuttite Orb", icon:"🟢", xp:120 },\n'
    '  { id:"fire_glow42_use", label:"Fire Glow 42", desc:"Activate FIRE_GLOW42 power-up", icon:"🔥", xp:60 },\n'
    '  { id:"fire_glow42_max", label:"Fire Glower 42", desc:"Reach max with FIRE_GLOW42 active", icon:"🔥", xp:120 },\n'
    '  { id:"ice_glow42_use", label:"Ice Glow 42", desc:"Activate ICE_GLOW42 power-up", icon:"❄️", xp:60 },\n'
    '  { id:"ice_glow42_max", label:"Ice Glower 42", desc:"Reach max with ICE_GLOW42 active", icon:"❄️", xp:120 },\n'
    '  { id:"tellurite_fox9e_tap", label:"Tellurite Fox", desc:"Tap a Tellurite Fox target", icon:"🦊", xp:60 },\n'
    '  { id:"tellurite_fox9e_peak", label:"Tellurite Fox Peak", desc:"Reach peak with Tellurite Fox", icon:"🌑", xp:120 },\n'
    '  { id:"tenorite_orb9e_tap", label:"Tenorite Orb", desc:"Tap a Tenorite Orb target", icon:"🔮", xp:60 },\n'
    '  { id:"tenorite_orb9e_peak", label:"Tenorite Orb Peak", desc:"Reach peak with Tenorite Orb", icon:"⬛", xp:120 },'
)
assert code.count(A1_OLD) == 1, f"Step 1 anchor not found: {code.count(A1_OLD)}"
code = code.replace(A1_OLD, A1_NEW, 1)

# ── Step 2: power-up list ────────────────────────────────────────────────────
A2_OLD = '"DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
A2_NEW = '"FIRE_GLOW42","ICE_GLOW42","DAWN_GLOW42","DUSK_GLOW42","STAR_GLOW42","MOON_GLOW42","NOVA_GLOW42","ECHO_GLOW42"'
assert code.count(A2_OLD) == 1, f"Step 2 anchor not found: {code.count(A2_OLD)}"
code = code.replace(A2_OLD, A2_NEW, 1)

# ── Step 3: power-up handler ──────────────────────────────────────────────────
A3_OLD = ('  } else if(ptype==="DAWN_GLOW42"){\n'
          '        gs.score+=2268;showPopup(cx,cy-1978,"+2268 🌅",theme.accent,26);spawnShockwave(cx,cy,"#f97316",2140);if(gs.score>=bonusTotal)unlock("dawn_glow42_max");')
A3_NEW = ('  } else if(ptype==="FIRE_GLOW42"){\n'
          '        gs.score+=2272;showPopup(cx,cy-1982,"+2272 🔥",theme.accent,26);spawnShockwave(cx,cy,"#dc2626",2144);if(gs.score>=bonusTotal)unlock("fire_glow42_max");\n'
          '      } else if(ptype==="ICE_GLOW42"){\n'
          '        gs.score+=2274;showPopup(cx,cy-1984,"+2274 ❄️",theme.accent,26);spawnShockwave(cx,cy,"#0ea5e9",2146);if(gs.score>=bonusTotal)unlock("ice_glow42_max");\n'
          '      } else if(ptype==="DAWN_GLOW42"){\n'
          '        gs.score+=2268;showPopup(cx,cy-1978,"+2268 🌅",theme.accent,26);spawnShockwave(cx,cy,"#f97316",2140);if(gs.score>=bonusTotal)unlock("dawn_glow42_max");')
assert code.count(A3_OLD) == 1, f"Step 3 anchor not found: {code.count(A3_OLD)}"
code = code.replace(A3_OLD, A3_NEW, 1)

# ── Step 4: sfx/unlock calls ──────────────────────────────────────────────────
A4_OLD = ('  // DAWN_GLOW42 — +2268 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW42"){sfx("powerUp",1931);unlock("dawn_glow42_use");}')
A4_NEW = ('  // FIRE_GLOW42 — +2272 fire glow bonus\n'
          '      if(ptype==="FIRE_GLOW42"){sfx("powerUp",1935);unlock("fire_glow42_use");}\n'
          '  // ICE_GLOW42 — +2274 ice glow bonus\n'
          '      if(ptype==="ICE_GLOW42"){sfx("powerUp",1937);unlock("ice_glow42_use");}\n'
          '  // DAWN_GLOW42 — +2268 dawn glow bonus\n'
          '      if(ptype==="DAWN_GLOW42"){sfx("powerUp",1931);unlock("dawn_glow42_use");}')
assert code.count(A4_OLD) == 1, f"Step 4 anchor not found: {code.count(A4_OLD)}"
code = code.replace(A4_OLD, A4_NEW, 1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSzomolnokiteFox9e('
A5_NEW = (
    'function drawTelluriteFox9e(ctx,r,ts,sp){\n'
    '  const bob=Math.sin(ts*0.3951)*r*0.07;\n'
    '  ctx.save();ctx.translate(0,bob);\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#f1f5f9");g.addColorStop(0.45+sp*0.35,"#475569");g.addColorStop(1,"#1e293b");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  if(sp>0.65){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(71,85,105,"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
    '  ctx.fillStyle=sp>0.88?"#1e293b":"#f1f5f9";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"🌑":"🦊",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawTenoiteOrb9e(ctx,r,ts,tp){\n'
    '  const pulse=0.72+0.28*Math.sin(ts*0.3955);\n'
    '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    '  g.addColorStop(0,"#e2e8f0");g.addColorStop(0.35+tp*0.35,"#334155");g.addColorStop(1,"#0f172a");\n'
    '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    '  const ring=r*(0.54+tp*0.42);\n'
    '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    '  ctx.strokeStyle="rgba(51,65,85,"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    '  ctx.globalAlpha=1;\n'
    '  if(tp>0.82){\n'
    '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    '    ctx.strokeStyle="rgba(51,65,85,"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
    '  ctx.fillStyle=tp>0.88?"#334155":"#e2e8f0";ctx.font=(r*0.56)+"px serif";\n'
    '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"⬛":"🔮",0,1);\n'
    '  ctx.restore();\n'
    '}\n'
    'function drawSzomolnokiteFox9e('
)
assert code.count(A5_OLD) == 1, f"Step 5 anchor not found: {code.count(A5_OLD)}"
code = code.replace(A5_OLD, A5_NEW, 1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD = 'else if(t.type==="szomolnokite_fox9e"){'
A6_NEW = (
    'else if(t.type==="tellurite_fox9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const sp=Math.min(1,(ts-t.born)/2118);\n'
    '    drawTelluriteFox9e(ctx,t.radius,ts,sp);ctx.restore();\n'
    '    } else if(t.type==="tenorite_orb9e"){\n'
    '    ctx.save();ctx.translate(t.x,t.y);\n'
    '    const tp=Math.min(1,(ts-t.born)/2120);\n'
    '    drawTenoiteOrb9e(ctx,t.radius,ts,tp);ctx.restore();\n'
    '    } else if(t.type==="szomolnokite_fox9e"){'
)
assert code.count(A6_OLD) == 1, f"Step 6 anchor not found: {code.count(A6_OLD)}"
code = code.replace(A6_OLD, A6_NEW, 1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD = 'if(hit.type==="szomolnokite_fox9e"){'
A7_NEW = (
    'if(hit.type==="tellurite_fox9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2118);\n'
    '      const pts=Math.round(388*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#475569",2118);\n'
    '      showPopup(cx,cy-38,"+"+pts+" 🌑","#f1f5f9",22);\n'
    '      unlock("tellurite_fox9e_tap");\n'
    '      if(rp>0.88)unlock("tellurite_fox9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="tenorite_orb9e"){\n'
    '      const rp=Math.min(1,(performance.now()-hit.born)/2120);\n'
    '      const pts=Math.round(383*(1+rp*1.4));gs.score+=pts;\n'
    '      gs.streak+=2;spawnShockwave(cx,cy,"#334155",2120);\n'
    '      showPopup(cx,cy-38,"+"+pts+" ⬛","#e2e8f0",22);\n'
    '      unlock("tenorite_orb9e_tap");\n'
    '      if(rp>0.88)unlock("tenorite_orb9e_peak");\n'
    '      updateMissions(gs.sessionStats);\n'
    '    } if(hit.type==="szomolnokite_fox9e"){'
)
assert code.count(A7_OLD) == 1, f"Step 7 anchor not found: {code.count(A7_OLD)}"
code = code.replace(A7_OLD, A7_NEW, 1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD = ('      type="szomolnokite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tarbuttite_orb9e"')
A8_NEW = ('      type="tellurite_fox9e";color="#475569";glow="#f1f5f9";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tenorite_orb9e";color="#334155";glow="#e2e8f0";\n'
          '    } else if('+COND100F+'){\n'
          '      type="szomolnokite_fox9e";color="#ca8a04";glow="#fef9c3";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tarbuttite_orb9e"')
assert code.count(A8_OLD) == 1, f"Step 8 anchor not found: {code.count(A8_OLD)}"
code = code.replace(A8_OLD, A8_NEW, 1)

# ── Step 9: radius table ──────────────────────────────────────────────────────
A9_OLD = 'type==="szomolnokite_fox9e"?BASE_R*1.46:type==="tarbuttite_orb9e"?BASE_R*1.45:'
A9_NEW = 'type==="tellurite_fox9e"?BASE_R*1.47:type==="tenorite_orb9e"?BASE_R*1.46:type==="szomolnokite_fox9e"?BASE_R*1.46:type==="tarbuttite_orb9e"?BASE_R*1.45:'
assert code.count(A9_OLD) == 1, f"Step 9 anchor not found: {code.count(A9_OLD)}"
code = code.replace(A9_OLD, A9_NEW, 1)

# ── Step 10: icon map (replace_all, expect 2) ─────────────────────────────────
A10_OLD = 'DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
A10_NEW = 'FIRE_GLOW42:"🔥✨",ICE_GLOW42:"❄️✨",DAWN_GLOW42:"🌅✨",DUSK_GLOW42:"🌇✨",STAR_GLOW42:"⭐✨",MOON_GLOW42:"🌙✨",NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨"'
cnt = code.count(A10_OLD)
assert cnt == 2, f"Step 10 expected 2, got {cnt}"
code = code.replace(A10_OLD, A10_NEW)

with open(SRC, "w") as f:
    f.write(code)

print(f"Batch 702 done! +{len(code)-ORIG} bytes")
