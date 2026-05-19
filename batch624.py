#!/usr/bin/env python3
# Batch 624: ECLIPSE_FLARE40 + COSMIC_FLARE40 + pyromorphite_fox9e + pyrargyrite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"phlogopite_orb9e_peak", label:"Phlogopite Orb Peak",'
A1_NEW = '''{ id:"eclipse_flare40_use", label:"Eclipse Flare", desc:"Activate ECLIPSE_FLARE40 power-up", icon:"🌒", xp:60 },
  { id:"eclipse_flare40_max", label:"Eclipse Surger", desc:"Reach max with ECLIPSE_FLARE40 active", icon:"🌒", xp:120 },
  { id:"cosmic_flare40_use", label:"Cosmic Flare", desc:"Activate COSMIC_FLARE40 power-up", icon:"🌌", xp:60 },
  { id:"cosmic_flare40_max", label:"Cosmic Scorer", desc:"Reach max with COSMIC_FLARE40 active", icon:"🌌", xp:120 },
  { id:"pyromorphite_fox9e_tap", label:"Pyromorphite Fox", desc:"Tap a Pyromorphite Fox target", icon:"🦊", xp:60 },
  { id:"pyromorphite_fox9e_peak", label:"Pyromorphite Fox Peak", desc:"Reach peak with Pyromorphite Fox", icon:"🦊", xp:120 },
  { id:"pyrargyrite_orb9e_tap", label:"Pyrargyrite Orb", desc:"Tap a Pyrargyrite Orb target", icon:"🔮", xp:60 },
  { id:"pyrargyrite_orb9e_peak", label:"Pyrargyrite Orb Peak", desc:"Reach peak with Pyrargyrite Orb", icon:"🔮", xp:120 },
  { id:"phlogopite_orb9e_peak", label:"Phlogopite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"VOID_FLARE40","PRISM_FLARE40","NEXUS_FLARE40"'
A2_NEW = '"ECLIPSE_FLARE40","COSMIC_FLARE40","VOID_FLARE40","PRISM_FLARE40","NEXUS_FLARE40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="VOID_FLARE40"){'
A3_NEW = '''} else if(ptype==="ECLIPSE_FLARE40"){
        activePwrRef.current.push({type:"ECLIPSE_FLARE40",left:12000});
        sfx("comboNote",1623);
        unlock("eclipse_flare40_use");
      } else if(ptype==="COSMIC_FLARE40"){
        activePwrRef.current.push({type:"COSMIC_FLARE40",left:12000});
        sfx("comboNote",1625);
        unlock("cosmic_flare40_use");
      } else if(ptype==="VOID_FLARE40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // VOID_FLARE40 — +1956 void bonus'
A4_NEW = '''  // ECLIPSE_FLARE40 — +1960 eclipse bonus
  if(activePwrRef.current.some(p=>p.type==="ECLIPSE_FLARE40")){
    const bonusTotal=Math.round(93.4*1000);
    gs.score+=1960;showPopup(cx,cy-1670,"+1960 🌒✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0388",1832);
    if(gs.score>=bonusTotal)unlock("eclipse_flare40_max");
  }
  // COSMIC_FLARE40 — +1962 cosmic bonus
  if(activePwrRef.current.some(p=>p.type==="COSMIC_FLARE40")){
    const bonusTotal=Math.round(93.5*1000);
    gs.score+=1962;showPopup(cx,cy-1672,"+1962 🌌✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a085c",1834);
    if(gs.score>=bonusTotal)unlock("cosmic_flare40_max");
  }
  // VOID_FLARE40 — +1956 void bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawPectoliteFox9e('
A5_NEW = '''function drawPyromorphiteFox9e(ctx,r,ts,pyroPct){
  const bob=Math.sin(ts*0.3330)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+pyroPct*0.35,"#84cc16");g.addColorStop(1,"#365314");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(pyroPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(132,204,22,"+(pyroPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=pyroPct>0.88?"#bef264":"#fefce8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pyroPct>0.88?"🟢":"🦊",0,1);
  ctx.restore();
}
function drawPyrargyiteOrb9e(ctx,r,ts,pyrgPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3334);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+pyrgPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fef2f2");g.addColorStop(0.35+pyrgPct*0.35,"#dc2626");g.addColorStop(1,"#7f1d1d");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+pyrgPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(220,38,38,"+(0.45+pyrgPct*0.55)+")";ctx.lineWidth=3.5+pyrgPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(pyrgPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(239,68,68,"+(pyrgPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=pyrgPct>0.88?"#fca5a5":"#fef2f2";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(pyrgPct>0.88?"🔴":"🔮",0,1);
  ctx.restore();
}
function drawPectoliteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="pectolite_fox9e"){'
A6_NEW = '''  else if(t.type==="pyromorphite_fox9e"){
    const pyroPct624=(Math.sin((Date.now()-t.spawnedAt)*0.3330)+1)/2;
    t._pyroPct624=pyroPct624;
    drawPyromorphiteFox9e(ctx,t.radius,ts,pyroPct624);
  }
  else if(t.type==="pyrargyrite_orb9e"){
    const pyrgPct624=(Math.sin((Date.now()-t.spawnedAt)*0.3334)+1)/2;
    t._pyrgPct624=pyrgPct624;
    drawPyrargyiteOrb9e(ctx,t.radius,ts,pyrgPct624);
  }
  else if(t.type==="pectolite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="pectolite_fox9e"){'
A7_NEW = '''    if(hit.type==="pyromorphite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo624pyro=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult624pyro=gs.feverActive?2:1;
      const isPeak624pyro=((hit._pyroPct624||0)>0.88);
      const pts624pyro=Math.round((isPeak624pyro?564:374)*combo624pyro*feverMult624pyro);
      gs.score+=pts624pyro;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1806,"#84cc16");
      if(isPeak624pyro){spawnPopup(hit.x,hit.y-28,"🟢 +"+pts624pyro,theme.accent);unlock("pyromorphite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts624pyro,theme.accent);}
      unlock("pyromorphite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="pyrargyrite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo624pyrg=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult624pyrg=gs.feverActive?2:1;
      const isPeak624pyrg=((hit._pyrgPct624||0)>0.88);
      const pts624pyrg=Math.round((isPeak624pyrg?552:366)*combo624pyrg*feverMult624pyrg);
      gs.score+=pts624pyrg;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1808,"#dc2626");
      if(isPeak624pyrg){spawnPopup(hit.x,hit.y-28,"🔴 +"+pts624pyrg,theme.accent);unlock("pyrargyrite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts624pyrg,theme.accent);}
      unlock("pyrargyrite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="pectolite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="pectolite_fox9e";color="#06b6d4";glow="#ecfeff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="phlogopite_orb9e"')
A8_NEW = ('      type="pyromorphite_fox9e";color="#84cc16";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="pyrargyrite_orb9e";color="#dc2626";glow="#fef2f2";\n'
          '    } else if('+COND100F+'){\n'
          '      type="pectolite_fox9e";color="#06b6d4";glow="#ecfeff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="phlogopite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="pectolite_fox9e"?BASE_R*1.08:type==="phlogopite_orb9e"?BASE_R*1.07:'
A9_NEW = 'type==="pyromorphite_fox9e"?BASE_R*1.09:type==="pyrargyrite_orb9e"?BASE_R*1.08:type==="pectolite_fox9e"?BASE_R*1.08:type==="phlogopite_orb9e"?BASE_R*1.07:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'VOID_FLARE40:"🌑✨",PRISM_FLARE40:"🔷✨",NEXUS_FLARE40:"🌠✨"'
A10_NEW = 'ECLIPSE_FLARE40:"🌒✨",COSMIC_FLARE40:"🌌✨",VOID_FLARE40:"🌑✨",PRISM_FLARE40:"🔷✨",NEXUS_FLARE40:"🌠✨"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 624 done! +{len(content)-original_size} bytes")
