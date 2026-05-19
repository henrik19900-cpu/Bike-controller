#!/usr/bin/env python3
# Batch 635: THUNDER_BEAM41 + VOID_PULSE41 + bornite_fox9e + baryte_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"autunite_orb9e_peak", label:"Autunite Orb Peak",'
A1_NEW = '''{ id:"thunder_beam41_use", label:"Thunder Beam", desc:"Activate THUNDER_BEAM41 power-up", icon:"⚡", xp:60 },
  { id:"thunder_beam41_max", label:"Thunder Beamer", desc:"Reach max with THUNDER_BEAM41 active", icon:"⚡", xp:120 },
  { id:"void_pulse41_use", label:"Void Pulse", desc:"Activate VOID_PULSE41 power-up", icon:"💠", xp:60 },
  { id:"void_pulse41_max", label:"Void Pulser", desc:"Reach max with VOID_PULSE41 active", icon:"💠", xp:120 },
  { id:"bornite_fox9e_tap", label:"Bornite Fox", desc:"Tap a Bornite Fox target", icon:"🦊", xp:60 },
  { id:"bornite_fox9e_peak", label:"Bornite Fox Peak", desc:"Reach peak with Bornite Fox", icon:"🦊", xp:120 },
  { id:"baryte_orb9e_tap", label:"Baryte Orb", desc:"Tap a Baryte Orb target", icon:"🔮", xp:60 },
  { id:"baryte_orb9e_peak", label:"Baryte Orb Peak", desc:"Reach peak with Baryte Orb", icon:"🔮", xp:120 },
  { id:"autunite_orb9e_peak", label:"Autunite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"SOLAR_BEAM41","AURORA_BEAM41","PRISM_BEAM41"'
A2_NEW = '"THUNDER_BEAM41","VOID_PULSE41","SOLAR_BEAM41","AURORA_BEAM41","PRISM_BEAM41"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="SOLAR_BEAM41"){'
A3_NEW = '''} else if(ptype==="THUNDER_BEAM41"){
        activePwrRef.current.push({type:"THUNDER_BEAM41",left:12000});
        sfx("comboNote",1667);
        unlock("thunder_beam41_use");
      } else if(ptype==="VOID_PULSE41"){
        activePwrRef.current.push({type:"VOID_PULSE41",left:12000});
        sfx("comboNote",1669);
        unlock("void_pulse41_use");
      } else if(ptype==="SOLAR_BEAM41"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // SOLAR_BEAM41 — +2000 solar bonus'
A4_NEW = '''  // THUNDER_BEAM41 — +2004 thunder bonus
  if(activePwrRef.current.some(p=>p.type==="THUNDER_BEAM41")){
    const bonusTotal=Math.round(95.6*1000);
    gs.score+=2004;showPopup(cx,cy-1714,"+2004 ⚡💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a039e",1876);
    if(gs.score>=bonusTotal)unlock("thunder_beam41_max");
  }
  // VOID_PULSE41 — +2006 void bonus
  if(activePwrRef.current.some(p=>p.type==="VOID_PULSE41")){
    const bonusTotal=Math.round(95.7*1000);
    gs.score+=2006;showPopup(cx,cy-1716,"+2006 💠💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0872",1878);
    if(gs.score>=bonusTotal)unlock("void_pulse41_max");
  }
  // SOLAR_BEAM41 — +2000 solar bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawArsenopyrlteFox9e('
A5_NEW = '''function drawBorniteFox9e(ctx,r,ts,bornPct){
  const bob=Math.sin(ts*0.3418)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.45+bornPct*0.35,"#7c3aed");g.addColorStop(1,"#4c1d95");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(bornPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(124,58,237,"+(bornPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=bornPct>0.88?"#c4b5fd":"#fdf4ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(bornPct>0.88?"🦋":"🦊",0,1);
  ctx.restore();
}
function drawBaryteOrb9e(ctx,r,ts,barPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3422);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+barPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f8fafc");g.addColorStop(0.35+barPct*0.35,"#334155");g.addColorStop(1,"#0f172a");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+barPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(51,65,85,"+(0.45+barPct*0.55)+")";ctx.lineWidth=3.5+barPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(barPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(100,116,139,"+(barPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=barPct>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(barPct>0.88?"⬜":"🔮",0,1);
  ctx.restore();
}
function drawArsenopyrlteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="arsenopyrite_fox9e"){'
A6_NEW = '''  else if(t.type==="bornite_fox9e"){
    const bornPct635=(Math.sin((Date.now()-t.spawnedAt)*0.3418)+1)/2;
    t._bornPct635=bornPct635;
    drawBorniteFox9e(ctx,t.radius,ts,bornPct635);
  }
  else if(t.type==="baryte_orb9e"){
    const barPct635=(Math.sin((Date.now()-t.spawnedAt)*0.3422)+1)/2;
    t._barPct635=barPct635;
    drawBaryteOrb9e(ctx,t.radius,ts,barPct635);
  }
  else if(t.type==="arsenopyrite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="arsenopyrite_fox9e"){'
A7_NEW = '''    if(hit.type==="bornite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo635born=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult635born=gs.feverActive?2:1;
      const isPeak635born=((hit._bornPct635||0)>0.88);
      const pts635born=Math.round((isPeak635born?586:396)*combo635born*feverMult635born);
      gs.score+=pts635born;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1850,"#7c3aed");
      if(isPeak635born){spawnPopup(hit.x,hit.y-28,"🦋 +"+pts635born,theme.accent);unlock("bornite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts635born,theme.accent);}
      unlock("bornite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="baryte_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo635bar=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult635bar=gs.feverActive?2:1;
      const isPeak635bar=((hit._barPct635||0)>0.88);
      const pts635bar=Math.round((isPeak635bar?574:388)*combo635bar*feverMult635bar);
      gs.score+=pts635bar;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1852,"#334155");
      if(isPeak635bar){spawnPopup(hit.x,hit.y-28,"⬜ +"+pts635bar,theme.accent);unlock("baryte_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts635bar,theme.accent);}
      unlock("baryte_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="arsenopyrite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="arsenopyrite_fox9e";color="#6b7280";glow="#f9fafb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="autunite_orb9e"')
A8_NEW = ('      type="bornite_fox9e";color="#7c3aed";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="baryte_orb9e";color="#334155";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="arsenopyrite_fox9e";color="#6b7280";glow="#f9fafb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="autunite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="arsenopyrite_fox9e"?BASE_R*1.19:type==="autunite_orb9e"?BASE_R*1.18:'
A9_NEW = 'type==="bornite_fox9e"?BASE_R*1.20:type==="baryte_orb9e"?BASE_R*1.19:type==="arsenopyrite_fox9e"?BASE_R*1.19:type==="autunite_orb9e"?BASE_R*1.18:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'SOLAR_BEAM41:"☀️💥",AURORA_BEAM41:"🌠💥",PRISM_BEAM41:"🔷💥"'
A10_NEW = 'THUNDER_BEAM41:"⚡💥",VOID_PULSE41:"💠💥",SOLAR_BEAM41:"☀️💥",AURORA_BEAM41:"🌠💥",PRISM_BEAM41:"🔷💥"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 635 done! +{len(content)-original_size} bytes")
