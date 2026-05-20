import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"rosenbuschite_orb9e_peak", label:"Rosenbuschite Orb Peak", desc:"Reach peak with Rosenbuschite Orb", icon:"🟠", xp:120 },'
A1_NEW=('{ id:"rosenbuschite_orb9e_peak", label:"Rosenbuschite Orb Peak", desc:"Reach peak with Rosenbuschite Orb", icon:"🟠", xp:120 },\n'
        '  { id:"void_beam42_use", label:"Void Beam 42", desc:"Activate VOID_BEAM42 power-up", icon:"🕳️", xp:60 },\n'
        '  { id:"void_beam42_max", label:"Void Beamer 42", desc:"Reach max with VOID_BEAM42 active", icon:"🕳️", xp:120 },\n'
        '  { id:"prism_beam42_use", label:"Prism Beam 42", desc:"Activate PRISM_BEAM42 power-up", icon:"🔆", xp:60 },\n'
        '  { id:"prism_beam42_max", label:"Prism Beamer 42", desc:"Reach max with PRISM_BEAM42 active", icon:"🔆", xp:120 },\n'
        '  { id:"roweite_fox9e_tap", label:"Roweite Fox", desc:"Tap a Roweite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"roweite_fox9e_peak", label:"Roweite Fox Peak", desc:"Reach peak with Roweite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"ruarsite_orb9e_tap", label:"Ruarsite Orb", desc:"Tap a Ruarsite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"ruarsite_orb9e_peak", label:"Ruarsite Orb Peak", desc:"Reach peak with Ruarsite Orb", icon:"🔴", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"STAR_BEAM42","MOON_BEAM42","NOVA_BEAM42"'
A2_NEW='"VOID_BEAM42","PRISM_BEAM42","STAR_BEAM42","MOON_BEAM42","NOVA_BEAM42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="STAR_BEAM42"){'
A3_NEW=('  } else if(ptype==="VOID_BEAM42"){\n'
        '        gs.score+=2192;showPopup(cx,cy-1902,"+2192 🕳️",theme.accent,26);spawnShockwave(cx,cy,"#0a03fc",2064);if(gs.score>=bonusTotal)unlock("void_beam42_max");\n'
        '      } else if(ptype==="PRISM_BEAM42"){\n'
        '        gs.score+=2194;showPopup(cx,cy-1904,"+2194 🔆",theme.accent,26);spawnShockwave(cx,cy,"#0a08d0",2066);if(gs.score>=bonusTotal)unlock("prism_beam42_max");\n'
        '      } else if(ptype==="STAR_BEAM42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // STAR_BEAM42 — +2188 star beam bonus'
A4_NEW=('  // VOID_BEAM42 — +2192 void beam bonus\n'
        '      if(ptype==="VOID_BEAM42"){sfx("powerUp",1855);unlock("void_beam42_use");}\n'
        '      // PRISM_BEAM42 — +2194 prism beam bonus\n'
        '      if(ptype==="PRISM_BEAM42"){sfx("powerUp",1857);unlock("prism_beam42_use");}\n'
        '  // STAR_BEAM42 — +2188 star beam bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawRoscheriteFox9e('
A5_NEW=('function drawRoweiteeFox9e(ctx,r,ts,rowPct){\n'
        '  const bob=Math.sin(ts*0.3794)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#a78bfa");g.addColorStop(0.45+rowPct*0.35,"#4c1d95");g.addColorStop(1,"#1e0a3c");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(rowPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(167,139,250,"+(rowPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=rowPct>0.88?"#a78bfa":"#ede9fe";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rowPct>0.88?"🔮":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRuarsiteOrb9e(ctx,r,ts,ruaPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3798);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+ruaPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fff1f2");g.addColorStop(0.35+ruaPct*0.35,"#fda4af");g.addColorStop(1,"#9f1239");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+ruaPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(253,164,175,"+(0.45+ruaPct*0.55)+")";ctx.lineWidth=3.5+ruaPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(ruaPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(253,164,175,"+(ruaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=ruaPct>0.88?"#fda4af":"#fff1f2";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ruaPct>0.88?"🔴":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawRoscheriteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="roscherite_fox9e"){'
A6_NEW=('  else if(t.type==="roweite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2038);drawRoweiteeFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="ruarsite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2040);drawRuarsiteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="roscherite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="roscherite_fox9e"){'
A7_NEW=('    if(hit.type==="roweite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2038);\n'
        '      const pts=Math.round(348*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#4c1d95",2038);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔮","#ede9fe",22);\n'
        '      unlock("roweite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("roweite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="ruarsite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2040);\n'
        '      const pts=Math.round(343*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#fda4af",2040);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🔴","#fff1f2",22);\n'
        '      unlock("ruarsite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("ruarsite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="roscherite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="roscherite_fox9e";color="#92400e";glow="#fffbeb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rosenbuschite_orb9e"')
A8_NEW=('      type="roweite_fox9e";color="#4c1d95";glow="#ede9fe";\n'
        '    } else if('+COND100F+'){\n'
        '      type="ruarsite_orb9e";color="#fda4af";glow="#fff1f2";\n'
        '    } else if('+COND100F+'){\n'
        '      type="roscherite_fox9e";color="#92400e";glow="#fffbeb";\n'
        '    } else if('+COND100F+'){\n'
        '      type="rosenbuschite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="roscherite_fox9e"?BASE_R*1.26:type==="rosenbuschite_orb9e"?BASE_R*1.25:'
A9_NEW='type==="roweite_fox9e"?BASE_R*1.27:type==="ruarsite_orb9e"?BASE_R*1.26:type==="roscherite_fox9e"?BASE_R*1.26:type==="rosenbuschite_orb9e"?BASE_R*1.25:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='STAR_BEAM42:"⭐💡",MOON_BEAM42:"🌙💡",NOVA_BEAM42:"💥💡"'
A10_NEW='VOID_BEAM42:"🕳️💡",PRISM_BEAM42:"🔆💡",STAR_BEAM42:"⭐💡",MOON_BEAM42:"🌙💡",NOVA_BEAM42:"💥💡"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 682 done! +{len(src)-len(orig)} bytes")
