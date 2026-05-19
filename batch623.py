#!/usr/bin/env python3
# Batch 623: VOID_FLARE40 + PRISM_FLARE40 + pectolite_fox9e + phlogopite_orb9e + 8 achievements

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"orthoclase_orb9e_peak", label:"Orthoclase Orb Peak",'
A1_NEW = '''{ id:"void_flare40_use", label:"Void Flare", desc:"Activate VOID_FLARE40 power-up", icon:"🌑", xp:60 },
  { id:"void_flare40_max", label:"Void Surger", desc:"Reach max with VOID_FLARE40 active", icon:"🌑", xp:120 },
  { id:"prism_flare40_use", label:"Prism Flare", desc:"Activate PRISM_FLARE40 power-up", icon:"🔷", xp:60 },
  { id:"prism_flare40_max", label:"Prism Scorer", desc:"Reach max with PRISM_FLARE40 active", icon:"🔷", xp:120 },
  { id:"pectolite_fox9e_tap", label:"Pectolite Fox", desc:"Tap a Pectolite Fox target", icon:"🦊", xp:60 },
  { id:"pectolite_fox9e_peak", label:"Pectolite Fox Peak", desc:"Reach peak with Pectolite Fox", icon:"🦊", xp:120 },
  { id:"phlogopite_orb9e_tap", label:"Phlogopite Orb", desc:"Tap a Phlogopite Orb target", icon:"🔮", xp:60 },
  { id:"phlogopite_orb9e_peak", label:"Phlogopite Orb Peak", desc:"Reach peak with Phlogopite Orb", icon:"🔮", xp:120 },
  { id:"orthoclase_orb9e_peak", label:"Orthoclase Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"NEXUS_FLARE40","SOLAR_FLARE40","AURORA_GLOW40"'
A2_NEW = '"VOID_FLARE40","PRISM_FLARE40","NEXUS_FLARE40","SOLAR_FLARE40","AURORA_GLOW40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_FLARE40"){'
A3_NEW = '''} else if(ptype==="VOID_FLARE40"){
        activePwrRef.current.push({type:"VOID_FLARE40",left:12000});
        sfx("comboNote",1619);
        unlock("void_flare40_use");
      } else if(ptype==="PRISM_FLARE40"){
        activePwrRef.current.push({type:"PRISM_FLARE40",left:12000});
        sfx("comboNote",1621);
        unlock("prism_flare40_use");
      } else if(ptype==="NEXUS_FLARE40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // NEXUS_FLARE40 — +1952 nexus bonus'
A4_NEW = '''  // VOID_FLARE40 — +1956 void bonus
  if(activePwrRef.current.some(p=>p.type==="VOID_FLARE40")){
    const bonusTotal=Math.round(93.2*1000);
    gs.score+=1956;showPopup(cx,cy-1666,"+1956 🌑✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0386",1828);
    if(gs.score>=bonusTotal)unlock("void_flare40_max");
  }
  // PRISM_FLARE40 — +1958 prism bonus
  if(activePwrRef.current.some(p=>p.type==="PRISM_FLARE40")){
    const bonusTotal=Math.round(93.3*1000);
    gs.score+=1958;showPopup(cx,cy-1668,"+1958 🔷✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a085a",1830);
    if(gs.score>=bonusTotal)unlock("prism_flare40_max");
  }
  // NEXUS_FLARE40 — +1952 nexus bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawOlivineFox9e('
A5_NEW = '''function drawPectoliteFox9e(ctx,r,ts,pectPct){
  const bob=Math.sin(ts*0.3322)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#ecfeff");g.addColorStop(0.45+pectPct*0.35,"#06b6d4");g.addColorStop(1,"#164e63");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(pectPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(6,182,212,"+(pectPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=pectPct>0.88?"#67e8f9":"#ecfeff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pectPct>0.88?"💎":"🦊",0,1);
  ctx.restore();
}
function drawPhlogopiteOrb9e(ctx,r,ts,phlogPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3326);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+phlogPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.35+phlogPct*0.35,"#c026d3");g.addColorStop(1,"#701a75");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+phlogPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(192,38,211,"+(0.45+phlogPct*0.55)+")";ctx.lineWidth=3.5+phlogPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(phlogPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(168,85,247,"+(phlogPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=phlogPct>0.88?"#e879f9":"#fdf4ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(phlogPct>0.88?"🟣":"🔮",0,1);
  ctx.restore();
}
function drawOlivineFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="olivine_fox9e"){'
A6_NEW = '''  else if(t.type==="pectolite_fox9e"){
    const pectPct623=(Math.sin((Date.now()-t.spawnedAt)*0.3322)+1)/2;
    t._pectPct623=pectPct623;
    drawPectoliteFox9e(ctx,t.radius,ts,pectPct623);
  }
  else if(t.type==="phlogopite_orb9e"){
    const phlogPct623=(Math.sin((Date.now()-t.spawnedAt)*0.3326)+1)/2;
    t._phlogPct623=phlogPct623;
    drawPhlogopiteOrb9e(ctx,t.radius,ts,phlogPct623);
  }
  else if(t.type==="olivine_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="olivine_fox9e"){'
A7_NEW = '''    if(hit.type==="pectolite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo623pect=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult623pect=gs.feverActive?2:1;
      const isPeak623pect=((hit._pectPct623||0)>0.88);
      const pts623pect=Math.round((isPeak623pect?562:372)*combo623pect*feverMult623pect);
      gs.score+=pts623pect;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1802,"#06b6d4");
      if(isPeak623pect){spawnPopup(hit.x,hit.y-28,"💎 +"+pts623pect,theme.accent);unlock("pectolite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts623pect,theme.accent);}
      unlock("pectolite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="phlogopite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo623phlog=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult623phlog=gs.feverActive?2:1;
      const isPeak623phlog=((hit._phlogPct623||0)>0.88);
      const pts623phlog=Math.round((isPeak623phlog?550:364)*combo623phlog*feverMult623phlog);
      gs.score+=pts623phlog;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1804,"#c026d3");
      if(isPeak623phlog){spawnPopup(hit.x,hit.y-28,"🟣 +"+pts623phlog,theme.accent);unlock("phlogopite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts623phlog,theme.accent);}
      unlock("phlogopite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="olivine_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'
A8_OLD = '      type="olivine_fox9e";color="#4ade80";glow="#f0fdf4";\n    } else if('+COND100F+'){\n      type="orthoclase_orb9e"'
A8_NEW = ('      type="pectolite_fox9e";color="#06b6d4";glow="#ecfeff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="phlogopite_orb9e";color="#c026d3";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="olivine_fox9e";color="#4ade80";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="orthoclase_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="olivine_fox9e"?BASE_R*1.07:type==="orthoclase_orb9e"?BASE_R*1.06:'
A9_NEW = 'type==="pectolite_fox9e"?BASE_R*1.08:type==="phlogopite_orb9e"?BASE_R*1.07:type==="olivine_fox9e"?BASE_R*1.07:type==="orthoclase_orb9e"?BASE_R*1.06:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'NEXUS_FLARE40:"🌠✨",SOLAR_FLARE40:"☀️✨",AURORA_GLOW40:"🌌🌟"'
A10_NEW = 'VOID_FLARE40:"🌑✨",PRISM_FLARE40:"🔷✨",NEXUS_FLARE40:"🌠✨",SOLAR_FLARE40:"☀️✨",AURORA_GLOW40:"🌌🌟"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 623 done! +{len(content)-original_size} bytes")
