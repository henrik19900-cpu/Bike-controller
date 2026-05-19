#!/usr/bin/env python3
# Batch 637: AURORA_PULSE41 + THUNDER_PULSE41 + chrysoberyl_fox9e + celestite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"benitoite_orb9e_peak", label:"Benitoite Orb Peak",'
A1_NEW = '''{ id:"aurora_pulse41_use", label:"Aurora Pulse", desc:"Activate AURORA_PULSE41 power-up", icon:"🌠", xp:60 },
  { id:"aurora_pulse41_max", label:"Aurora Pulser", desc:"Reach max with AURORA_PULSE41 active", icon:"🌠", xp:120 },
  { id:"thunder_pulse41_use", label:"Thunder Pulse", desc:"Activate THUNDER_PULSE41 power-up", icon:"⚡", xp:60 },
  { id:"thunder_pulse41_max", label:"Thunder Pulser", desc:"Reach max with THUNDER_PULSE41 active", icon:"⚡", xp:120 },
  { id:"chrysoberyl_fox9e_tap", label:"Chrysoberyl Fox", desc:"Tap a Chrysoberyl Fox target", icon:"🦊", xp:60 },
  { id:"chrysoberyl_fox9e_peak", label:"Chrysoberyl Fox Peak", desc:"Reach peak with Chrysoberyl Fox", icon:"🦊", xp:120 },
  { id:"celestite_orb9e_tap", label:"Celestite Orb", desc:"Tap a Celestite Orb target", icon:"🔮", xp:60 },
  { id:"celestite_orb9e_peak", label:"Celestite Orb Peak", desc:"Reach peak with Celestite Orb", icon:"🔮", xp:120 },
  { id:"benitoite_orb9e_peak", label:"Benitoite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"PRISM_PULSE41","NEXUS_PULSE41","THUNDER_BEAM41"'
A2_NEW = '"AURORA_PULSE41","THUNDER_PULSE41","PRISM_PULSE41","NEXUS_PULSE41","THUNDER_BEAM41"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="PRISM_PULSE41"){'
A3_NEW = '''} else if(ptype==="AURORA_PULSE41"){
        activePwrRef.current.push({type:"AURORA_PULSE41",left:12000});
        sfx("comboNote",1675);
        unlock("aurora_pulse41_use");
      } else if(ptype==="THUNDER_PULSE41"){
        activePwrRef.current.push({type:"THUNDER_PULSE41",left:12000});
        sfx("comboNote",1677);
        unlock("thunder_pulse41_use");
      } else if(ptype==="PRISM_PULSE41"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // PRISM_PULSE41 — +2008 prism bonus'
A4_NEW = '''  // AURORA_PULSE41 — +2012 aurora bonus
  if(activePwrRef.current.some(p=>p.type==="AURORA_PULSE41")){
    const bonusTotal=Math.round(96.0*1000);
    gs.score+=2012;showPopup(cx,cy-1722,"+2012 🌠💠",theme.accent,26);
    spawnShockwave(cx,cy,"#0a03a2",1884);
    if(gs.score>=bonusTotal)unlock("aurora_pulse41_max");
  }
  // THUNDER_PULSE41 — +2014 thunder bonus
  if(activePwrRef.current.some(p=>p.type==="THUNDER_PULSE41")){
    const bonusTotal=Math.round(96.1*1000);
    gs.score+=2014;showPopup(cx,cy-1724,"+2014 ⚡💠",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0876",1886);
    if(gs.score>=bonusTotal)unlock("thunder_pulse41_max");
  }
  // PRISM_PULSE41 — +2008 prism bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawBassaniteFox9e('
A5_NEW = '''function drawChrysobe rylFox9e(ctx,r,ts,chrPct){
  const bob=Math.sin(ts*0.3434)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+chrPct*0.35,"#047857");g.addColorStop(1,"#064e3b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(chrPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(4,120,87,"+(chrPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=chrPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(chrPct>0.88?"🌿":"🦊",0,1);
  ctx.restore();
}
function drawCelestiteOrb9e(ctx,r,ts,celPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3438);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+celPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.35+celPct*0.35,"#0284c7");g.addColorStop(1,"#0c4a6e");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+celPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(2,132,199,"+(0.45+celPct*0.55)+")";ctx.lineWidth=3.5+celPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(celPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(56,189,248,"+(celPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=celPct>0.88?"#7dd3fc":"#e0f2fe";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(celPct>0.88?"🩵":"🔮",0,1);
  ctx.restore();
}
function drawBassaniteFox9e('''

# Remove the space in function name (fix typo)
A5_NEW = A5_NEW.replace('drawChrysobe rylFox9e', 'drawChrysobe‎rylFox9e')
# Actually fix properly
A5_NEW = '''function drawChrysoberylFox9e(ctx,r,ts,chrPct){
  const bob=Math.sin(ts*0.3434)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.45+chrPct*0.35,"#047857");g.addColorStop(1,"#064e3b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(chrPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(4,120,87,"+(chrPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=chrPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(chrPct>0.88?"🌿":"🦊",0,1);
  ctx.restore();
}
function drawCelestiteOrb9e(ctx,r,ts,celPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3438);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+celPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#e0f2fe");g.addColorStop(0.35+celPct*0.35,"#0284c7");g.addColorStop(1,"#0c4a6e");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+celPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(2,132,199,"+(0.45+celPct*0.55)+")";ctx.lineWidth=3.5+celPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(celPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(56,189,248,"+(celPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=celPct>0.88?"#7dd3fc":"#e0f2fe";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(celPct>0.88?"🩵":"🔮",0,1);
  ctx.restore();
}
function drawBassaniteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="bassanite_fox9e"){'
A6_NEW = '''  else if(t.type==="chrysoberyl_fox9e"){
    const chrPct637=(Math.sin((Date.now()-t.spawnedAt)*0.3434)+1)/2;
    t._chrPct637=chrPct637;
    drawChrysoberylFox9e(ctx,t.radius,ts,chrPct637);
  }
  else if(t.type==="celestite_orb9e"){
    const celPct637=(Math.sin((Date.now()-t.spawnedAt)*0.3438)+1)/2;
    t._celPct637=celPct637;
    drawCelestiteOrb9e(ctx,t.radius,ts,celPct637);
  }
  else if(t.type==="bassanite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="bassanite_fox9e"){'
A7_NEW = '''    if(hit.type==="chrysoberyl_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo637chr=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult637chr=gs.feverActive?2:1;
      const isPeak637chr=((hit._chrPct637||0)>0.88);
      const pts637chr=Math.round((isPeak637chr?590:400)*combo637chr*feverMult637chr);
      gs.score+=pts637chr;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1858,"#047857");
      if(isPeak637chr){spawnPopup(hit.x,hit.y-28,"🌿 +"+pts637chr,theme.accent);unlock("chrysoberyl_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts637chr,theme.accent);}
      unlock("chrysoberyl_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="celestite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo637cel=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult637cel=gs.feverActive?2:1;
      const isPeak637cel=((hit._celPct637||0)>0.88);
      const pts637cel=Math.round((isPeak637cel?578:392)*combo637cel*feverMult637cel);
      gs.score+=pts637cel;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1860,"#0284c7");
      if(isPeak637cel){spawnPopup(hit.x,hit.y-28,"🩵 +"+pts637cel,theme.accent);unlock("celestite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts637cel,theme.accent);}
      unlock("celestite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="bassanite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="bassanite_fox9e";color="#f59e0b";glow="#fffbeb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="benitoite_orb9e"')
A8_NEW = ('      type="chrysoberyl_fox9e";color="#047857";glow="#ecfdf5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="celestite_orb9e";color="#0284c7";glow="#e0f2fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="bassanite_fox9e";color="#f59e0b";glow="#fffbeb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="benitoite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="bassanite_fox9e"?BASE_R*1.21:type==="benitoite_orb9e"?BASE_R*1.20:'
A9_NEW = 'type==="chrysoberyl_fox9e"?BASE_R*1.22:type==="celestite_orb9e"?BASE_R*1.21:type==="bassanite_fox9e"?BASE_R*1.21:type==="benitoite_orb9e"?BASE_R*1.20:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'PRISM_PULSE41:"🔷💠",NEXUS_PULSE41:"🌐💠",THUNDER_BEAM41:"⚡💥"'
A10_NEW = 'AURORA_PULSE41:"🌠💠",THUNDER_PULSE41:"⚡💠",PRISM_PULSE41:"🔷💠",NEXUS_PULSE41:"🌐💠",THUNDER_BEAM41:"⚡💥"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 637 done! +{len(content)-original_size} bytes")
