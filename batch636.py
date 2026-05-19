#!/usr/bin/env python3
# Batch 636: PRISM_PULSE41 + NEXUS_PULSE41 + bassanite_fox9e + benitoite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"baryte_orb9e_peak", label:"Baryte Orb Peak",'
A1_NEW = '''{ id:"prism_pulse41_use", label:"Prism Pulse", desc:"Activate PRISM_PULSE41 power-up", icon:"🔷", xp:60 },
  { id:"prism_pulse41_max", label:"Prism Pulser", desc:"Reach max with PRISM_PULSE41 active", icon:"🔷", xp:120 },
  { id:"nexus_pulse41_use", label:"Nexus Pulse", desc:"Activate NEXUS_PULSE41 power-up", icon:"🌐", xp:60 },
  { id:"nexus_pulse41_max", label:"Nexus Pulser", desc:"Reach max with NEXUS_PULSE41 active", icon:"🌐", xp:120 },
  { id:"bassanite_fox9e_tap", label:"Bassanite Fox", desc:"Tap a Bassanite Fox target", icon:"🦊", xp:60 },
  { id:"bassanite_fox9e_peak", label:"Bassanite Fox Peak", desc:"Reach peak with Bassanite Fox", icon:"🦊", xp:120 },
  { id:"benitoite_orb9e_tap", label:"Benitoite Orb", desc:"Tap a Benitoite Orb target", icon:"🔮", xp:60 },
  { id:"benitoite_orb9e_peak", label:"Benitoite Orb Peak", desc:"Reach peak with Benitoite Orb", icon:"🔮", xp:120 },
  { id:"baryte_orb9e_peak", label:"Baryte Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"THUNDER_BEAM41","VOID_PULSE41","SOLAR_BEAM41"'
A2_NEW = '"PRISM_PULSE41","NEXUS_PULSE41","THUNDER_BEAM41","VOID_PULSE41","SOLAR_BEAM41"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="THUNDER_BEAM41"){'
A3_NEW = '''} else if(ptype==="PRISM_PULSE41"){
        activePwrRef.current.push({type:"PRISM_PULSE41",left:12000});
        sfx("comboNote",1671);
        unlock("prism_pulse41_use");
      } else if(ptype==="NEXUS_PULSE41"){
        activePwrRef.current.push({type:"NEXUS_PULSE41",left:12000});
        sfx("comboNote",1673);
        unlock("nexus_pulse41_use");
      } else if(ptype==="THUNDER_BEAM41"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // THUNDER_BEAM41 — +2004 thunder bonus'
A4_NEW = '''  // PRISM_PULSE41 — +2008 prism bonus
  if(activePwrRef.current.some(p=>p.type==="PRISM_PULSE41")){
    const bonusTotal=Math.round(95.8*1000);
    gs.score+=2008;showPopup(cx,cy-1718,"+2008 🔷💠",theme.accent,26);
    spawnShockwave(cx,cy,"#0a03a0",1880);
    if(gs.score>=bonusTotal)unlock("prism_pulse41_max");
  }
  // NEXUS_PULSE41 — +2010 nexus bonus
  if(activePwrRef.current.some(p=>p.type==="NEXUS_PULSE41")){
    const bonusTotal=Math.round(95.9*1000);
    gs.score+=2010;showPopup(cx,cy-1720,"+2010 🌐💠",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0874",1882);
    if(gs.score>=bonusTotal)unlock("nexus_pulse41_max");
  }
  // THUNDER_BEAM41 — +2004 thunder bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBorniteFox9e('
A5_NEW = '''function drawBassaniteFox9e(ctx,r,ts,bassPct){
  const bob=Math.sin(ts*0.3426)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fffbeb");g.addColorStop(0.45+bassPct*0.35,"#f59e0b");g.addColorStop(1,"#78350f");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(bassPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(245,158,11,"+(bassPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=bassPct>0.88?"#fcd34d":"#fffbeb";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(bassPct>0.88?"🌻":"🦊",0,1);
  ctx.restore();
}
function drawBenitoiteOrb9e(ctx,r,ts,benPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3430);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+benPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#eff6ff");g.addColorStop(0.35+benPct*0.35,"#2563eb");g.addColorStop(1,"#1e3a8a");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+benPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(37,99,235,"+(0.45+benPct*0.55)+")";ctx.lineWidth=3.5+benPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(benPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(59,130,246,"+(benPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=benPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(benPct>0.88?"💎":"🔮",0,1);
  ctx.restore();
}
function drawBorniteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="bornite_fox9e"){'
A6_NEW = '''  else if(t.type==="bassanite_fox9e"){
    const bassPct636=(Math.sin((Date.now()-t.spawnedAt)*0.3426)+1)/2;
    t._bassPct636=bassPct636;
    drawBassaniteFox9e(ctx,t.radius,ts,bassPct636);
  }
  else if(t.type==="benitoite_orb9e"){
    const benPct636=(Math.sin((Date.now()-t.spawnedAt)*0.3430)+1)/2;
    t._benPct636=benPct636;
    drawBenitoiteOrb9e(ctx,t.radius,ts,benPct636);
  }
  else if(t.type==="bornite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="bornite_fox9e"){'
A7_NEW = '''    if(hit.type==="bassanite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo636bass=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult636bass=gs.feverActive?2:1;
      const isPeak636bass=((hit._bassPct636||0)>0.88);
      const pts636bass=Math.round((isPeak636bass?588:398)*combo636bass*feverMult636bass);
      gs.score+=pts636bass;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1854,"#f59e0b");
      if(isPeak636bass){spawnPopup(hit.x,hit.y-28,"🌻 +"+pts636bass,theme.accent);unlock("bassanite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts636bass,theme.accent);}
      unlock("bassanite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="benitoite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo636ben=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult636ben=gs.feverActive?2:1;
      const isPeak636ben=((hit._benPct636||0)>0.88);
      const pts636ben=Math.round((isPeak636ben?576:390)*combo636ben*feverMult636ben);
      gs.score+=pts636ben;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1856,"#2563eb");
      if(isPeak636ben){spawnPopup(hit.x,hit.y-28,"💎 +"+pts636ben,theme.accent);unlock("benitoite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts636ben,theme.accent);}
      unlock("benitoite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="bornite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="bornite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="baryte_orb9e"')
A8_NEW = ('      type="bassanite_fox9e";color="#f59e0b";glow="#fffbeb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="benitoite_orb9e";color="#2563eb";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bornite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="baryte_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="bornite_fox9e"?BASE_R*1.20:type==="baryte_orb9e"?BASE_R*1.19:'
A9_NEW = 'type==="bassanite_fox9e"?BASE_R*1.21:type==="benitoite_orb9e"?BASE_R*1.20:type==="bornite_fox9e"?BASE_R*1.20:type==="baryte_orb9e"?BASE_R*1.19:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'THUNDER_BEAM41:"⚡💥",VOID_PULSE41:"💠💥",SOLAR_BEAM41:"☀️💥"'
A10_NEW = 'PRISM_PULSE41:"🔷💠",NEXUS_PULSE41:"🌐💠",THUNDER_BEAM41:"⚡💥",VOID_PULSE41:"💠💥",SOLAR_BEAM41:"☀️💥"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 636 done! +{len(content)-original_size} bytes")
