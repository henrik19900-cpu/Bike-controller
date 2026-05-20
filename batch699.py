import re

with open("src/NexusTap.jsx","r") as f:
    src=f.read()

orig=src

COND100F='(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

# ── Step 1: 8 achievements ────────────────────────────────────────────────────
A1_OLD='{ id:"studenitsite_orb9e_peak", label:"Studenitsite Orb Peak", desc:"Reach peak with Studenitsite Orb", icon:"🟢", xp:120 },'
A1_NEW=('{ id:"studenitsite_orb9e_peak", label:"Studenitsite Orb Peak", desc:"Reach peak with Studenitsite Orb", icon:"🟢", xp:120 },\n'
        '  { id:"nova_glow42_use", label:"Nova Glow 42", desc:"Activate NOVA_GLOW42 power-up", icon:"💥", xp:60 },\n'
        '  { id:"nova_glow42_max", label:"Nova Glower 42", desc:"Reach max with NOVA_GLOW42 active", icon:"💥", xp:120 },\n'
        '  { id:"echo_glow42_use", label:"Echo Glow 42", desc:"Activate ECHO_GLOW42 power-up", icon:"📡", xp:60 },\n'
        '  { id:"echo_glow42_max", label:"Echo Glower 42", desc:"Reach max with ECHO_GLOW42 active", icon:"📡", xp:120 },\n'
        '  { id:"sulfohalite_fox9e_tap", label:"Sulfohalite Fox", desc:"Tap a Sulfohalite Fox target", icon:"🦊", xp:60 },\n'
        '  { id:"sulfohalite_fox9e_peak", label:"Sulfohalite Fox Peak", desc:"Reach peak with Sulfohalite Fox", icon:"🦊", xp:120 },\n'
        '  { id:"sulvanite_orb9e_tap", label:"Sulvanite Orb", desc:"Tap a Sulvanite Orb target", icon:"🔮", xp:60 },\n'
        '  { id:"sulvanite_orb9e_peak", label:"Sulvanite Orb Peak", desc:"Reach peak with Sulvanite Orb", icon:"🟤", xp:120 },')
assert src.count(A1_OLD)==1, f"Step1 anchor count={src.count(A1_OLD)}"
src=src.replace(A1_OLD,A1_NEW,1)

# ── Step 2: add power-up IDs to pool ─────────────────────────────────────────
A2_OLD='"NEXUS_FLARE42","PRISM_GLOW42","COSMOS_FLARE42"'
A2_NEW='"NOVA_GLOW42","ECHO_GLOW42","NEXUS_FLARE42","PRISM_GLOW42","COSMOS_FLARE42"'
assert src.count(A2_OLD)==1, f"Step2 anchor count={src.count(A2_OLD)}"
src=src.replace(A2_OLD,A2_NEW,1)

# ── Step 3: power-up score handler ───────────────────────────────────────────
A3_OLD='  } else if(ptype==="NEXUS_FLARE42"){'
A3_NEW=('  } else if(ptype==="NOVA_GLOW42"){\n'
        '        gs.score+=2260;showPopup(cx,cy-1970,"+2260 💥",theme.accent,26);spawnShockwave(cx,cy,"#0a041e",2132);if(gs.score>=bonusTotal)unlock("nova_glow42_max");\n'
        '      } else if(ptype==="ECHO_GLOW42"){\n'
        '        gs.score+=2262;showPopup(cx,cy-1972,"+2262 📡",theme.accent,26);spawnShockwave(cx,cy,"#0a08f2",2134);if(gs.score>=bonusTotal)unlock("echo_glow42_max");\n'
        '      } else if(ptype==="NEXUS_FLARE42"){')
assert src.count(A3_OLD)==1, f"Step3 anchor count={src.count(A3_OLD)}"
src=src.replace(A3_OLD,A3_NEW,1)

# ── Step 4: sfx + unlock lines ────────────────────────────────────────────────
A4_OLD='  // NEXUS_FLARE42 — +2256 nexus flare bonus'
A4_NEW=('  // NOVA_GLOW42 — +2260 nova glow bonus\n'
        '      if(ptype==="NOVA_GLOW42"){sfx("powerUp",1923);unlock("nova_glow42_use");}\n'
        '      // ECHO_GLOW42 — +2262 echo glow bonus\n'
        '      if(ptype==="ECHO_GLOW42"){sfx("powerUp",1925);unlock("echo_glow42_use");}\n'
        '  // NEXUS_FLARE42 — +2256 nexus flare bonus')
assert src.count(A4_OLD)==1, f"Step4 anchor count={src.count(A4_OLD)}"
src=src.replace(A4_OLD,A4_NEW,1)

# ── Step 5: draw functions ────────────────────────────────────────────────────
A5_OLD='function drawStruviteFox9e('
A5_NEW=('function drawSulfohaliteFox9e(ctx,r,ts,sfhPct){\n'
        '  const bob=Math.sin(ts*0.3930)*r*0.07;\n'
        '  ctx.save();ctx.translate(0,bob);\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+sfhPct*0.35,"#64748b");g.addColorStop(1,"#0f172a");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  if(sfhPct>0.65){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(248,250,252,"+(sfhPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sfhPct>0.88?"#f8fafc":"#ffffff";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sfhPct>0.88?"🌫️":"🦊",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawSulvaniteOrb9e(ctx,r,ts,sulPct){\n'
        '  const pulse=0.72+0.28*Math.sin(ts*0.3934);\n'
        '  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sulPct*0.27;\n'
        '  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
        '  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+sulPct*0.35,"#d97706");g.addColorStop(1,"#78350f");\n'
        '  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
        '  const ring=r*(0.54+sulPct*0.42);\n'
        '  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
        '  ctx.strokeStyle="rgba(217,119,6,"+(0.45+sulPct*0.55)+")";ctx.lineWidth=3.5+sulPct*3;ctx.stroke();\n'
        '  ctx.globalAlpha=1;\n'
        '  if(sulPct>0.82){\n'
        '    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
        '    ctx.strokeStyle="rgba(217,119,6,"+(sulPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}\n'
        '  ctx.fillStyle=sulPct>0.88?"#d97706":"#fef3c7";ctx.font=(r*0.56)+"px serif";\n'
        '  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sulPct>0.88?"🟤":"🔮",0,1);\n'
        '  ctx.restore();\n'
        '}\n'
        'function drawStruviteFox9e(')
assert src.count(A5_OLD)==1, f"Step5 anchor count={src.count(A5_OLD)}"
src=src.replace(A5_OLD,A5_NEW,1)

# ── Step 6: draw dispatch ─────────────────────────────────────────────────────
A6_OLD='  else if(t.type==="struvite_fox9e"){'
A6_NEW=('  else if(t.type==="sulfohalite_fox9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2106);drawSulfohaliteFox9e(ctx,t.radius,ts,rp);\n'
        '    } else if(t.type==="sulvanite_orb9e"){\n'
        '    const rp=Math.min(1,(ts-t.born)/2108);drawSulvaniteOrb9e(ctx,t.radius,ts,rp);\n'
        '  } else if(t.type==="struvite_fox9e"){')
assert src.count(A6_OLD)==1, f"Step6 anchor count={src.count(A6_OLD)}"
src=src.replace(A6_OLD,A6_NEW,1)

# ── Step 7: handleTap handlers ────────────────────────────────────────────────
A7_OLD='    if(hit.type==="struvite_fox9e"){'
A7_NEW=('    if(hit.type==="sulfohalite_fox9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2106);\n'
        '      const pts=Math.round(382*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#64748b",2106);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🌫️","#f8fafc",22);\n'
        '      unlock("sulfohalite_fox9e_tap");\n'
        '      if(rp>0.88)unlock("sulfohalite_fox9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="sulvanite_orb9e"){\n'
        '      const rp=Math.min(1,(performance.now()-hit.born)/2108);\n'
        '      const pts=Math.round(377*(1+rp*1.4));gs.score+=pts;\n'
        '      gs.streak+=2;spawnShockwave(cx,cy,"#d97706",2108);\n'
        '      showPopup(cx,cy-38,"+"+pts+" 🟤","#fef3c7",22);\n'
        '      unlock("sulvanite_orb9e_tap");\n'
        '      if(rp>0.88)unlock("sulvanite_orb9e_peak");\n'
        '      updateMissions(gs.sessionStats);\n'
        '    } if(hit.type==="struvite_fox9e"){')
assert src.count(A7_OLD)==1, f"Step7 anchor count={src.count(A7_OLD)}"
src=src.replace(A7_OLD,A7_NEW,1)

# ── Step 8: spawnTarget entries ───────────────────────────────────────────────
A8_OLD=('      type="struvite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="studenitsite_orb9e"')
A8_NEW=('      type="sulfohalite_fox9e";color="#64748b";glow="#f8fafc";\n'
        '    } else if('+COND100F+'){\n'
        '      type="sulvanite_orb9e";color="#d97706";glow="#fef3c7";\n'
        '    } else if('+COND100F+'){\n'
        '      type="struvite_fox9e";color="#16a34a";glow="#f0fdf4";\n'
        '    } else if('+COND100F+'){\n'
        '      type="studenitsite_orb9e"')
assert src.count(A8_OLD)==1, f"Step8 anchor count={src.count(A8_OLD)}"
src=src.replace(A8_OLD,A8_NEW,1)

# ── Step 9: radius table ─────────────────────────────────────────────────────
A9_OLD='type==="struvite_fox9e"?BASE_R*1.43:type==="studenitsite_orb9e"?BASE_R*1.42:'
A9_NEW='type==="sulfohalite_fox9e"?BASE_R*1.44:type==="sulvanite_orb9e"?BASE_R*1.43:type==="struvite_fox9e"?BASE_R*1.43:type==="studenitsite_orb9e"?BASE_R*1.42:'
assert src.count(A9_OLD)==1, f"Step9 anchor count={src.count(A9_OLD)}"
src=src.replace(A9_OLD,A9_NEW,1)

# ── Step 10: icon map (replace_all, count==2) ─────────────────────────────────
A10_OLD='NEXUS_FLARE42:"🔵✨",PRISM_GLOW42:"🔆✨",COSMOS_FLARE42:"🌌🌟"'
A10_NEW='NOVA_GLOW42:"💥✨",ECHO_GLOW42:"📡✨",NEXUS_FLARE42:"🔵✨",PRISM_GLOW42:"🔆✨",COSMOS_FLARE42:"🌌🌟"'
cnt=src.count(A10_OLD)
assert cnt==2, f"Step10 count={cnt}"
src=src.replace(A10_OLD,A10_NEW)

assert len(src)>len(orig), "No net growth"
with open("src/NexusTap.jsx","w") as f:
    f.write(src)
print(f"Batch 699 done! +{len(src)-len(orig)} bytes")
