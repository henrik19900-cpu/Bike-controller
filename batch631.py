#!/usr/bin/env python3
# Batch 631: STELLAR_RAY40 + LUNAR_RAY40 + vivianite_fox9e + wavellite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"uvarovite_orb9e_peak", label:"Uvarovite Orb Peak",'
A1_NEW = '''{ id:"stellar_ray40_use", label:"Stellar Ray", desc:"Activate STELLAR_RAY40 power-up", icon:"⭐", xp:60 },
  { id:"stellar_ray40_max", label:"Stellar Rayer", desc:"Reach max with STELLAR_RAY40 active", icon:"⭐", xp:120 },
  { id:"lunar_ray40_use", label:"Lunar Ray", desc:"Activate LUNAR_RAY40 power-up", icon:"🌙", xp:60 },
  { id:"lunar_ray40_max", label:"Lunar Rayer", desc:"Reach max with LUNAR_RAY40 active", icon:"🌙", xp:120 },
  { id:"vivianite_fox9e_tap", label:"Vivianite Fox", desc:"Tap a Vivianite Fox target", icon:"🦊", xp:60 },
  { id:"vivianite_fox9e_peak", label:"Vivianite Fox Peak", desc:"Reach peak with Vivianite Fox", icon:"🦊", xp:120 },
  { id:"wavellite_orb9e_tap", label:"Wavellite Orb", desc:"Tap a Wavellite Orb target", icon:"🔮", xp:60 },
  { id:"wavellite_orb9e_peak", label:"Wavellite Orb Peak", desc:"Reach peak with Wavellite Orb", icon:"🔮", xp:120 },
  { id:"uvarovite_orb9e_peak", label:"Uvarovite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"ECLIPSE_RAY40","COSMIC_RAY40","VOID_RAY40"'
A2_NEW = '"STELLAR_RAY40","LUNAR_RAY40","ECLIPSE_RAY40","COSMIC_RAY40","VOID_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="ECLIPSE_RAY40"){'
A3_NEW = '''} else if(ptype==="STELLAR_RAY40"){
        activePwrRef.current.push({type:"STELLAR_RAY40",left:12000});
        sfx("comboNote",1651);
        unlock("stellar_ray40_use");
      } else if(ptype==="LUNAR_RAY40"){
        activePwrRef.current.push({type:"LUNAR_RAY40",left:12000});
        sfx("comboNote",1653);
        unlock("lunar_ray40_use");
      } else if(ptype==="ECLIPSE_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // ECLIPSE_RAY40 — +1984 eclipse bonus'
A4_NEW = '''  // STELLAR_RAY40 — +1988 stellar bonus
  if(activePwrRef.current.some(p=>p.type==="STELLAR_RAY40")){
    const bonusTotal=Math.round(94.8*1000);
    gs.score+=1988;showPopup(cx,cy-1698,"+1988 ⭐⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0396",1860);
    if(gs.score>=bonusTotal)unlock("stellar_ray40_max");
  }
  // LUNAR_RAY40 — +1990 lunar bonus
  if(activePwrRef.current.some(p=>p.type==="LUNAR_RAY40")){
    const bonusTotal=Math.round(94.9*1000);
    gs.score+=1990;showPopup(cx,cy-1700,"+1990 🌙⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a086a",1862);
    if(gs.score>=bonusTotal)unlock("lunar_ray40_max");
  }
  // ECLIPSE_RAY40 — +1984 eclipse bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawUlexiteFox9e('
A5_NEW = '''function drawVivianiteFox9e(ctx,r,ts,vivPct){
  const bob=Math.sin(ts*0.3386)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#eff6ff");g.addColorStop(0.45+vivPct*0.35,"#1e40af");g.addColorStop(1,"#1e1b4b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(vivPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(30,64,175,"+(vivPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=vivPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(vivPct>0.88?"🫐":"🦊",0,1);
  ctx.restore();
}
function drawWavelliteOrb9e(ctx,r,ts,wavPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3390);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+wavPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f7fee7");g.addColorStop(0.35+wavPct*0.35,"#65a30d");g.addColorStop(1,"#365314");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+wavPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(101,163,13,"+(0.45+wavPct*0.55)+")";ctx.lineWidth=3.5+wavPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(wavPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(132,204,22,"+(wavPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=wavPct>0.88?"#bef264":"#f7fee7";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(wavPct>0.88?"🍋":"🔮",0,1);
  ctx.restore();
}
function drawUlexiteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="ulexite_fox9e"){'
A6_NEW = '''  else if(t.type==="vivianite_fox9e"){
    const vivPct631=(Math.sin((Date.now()-t.spawnedAt)*0.3386)+1)/2;
    t._vivPct631=vivPct631;
    drawVivianiteFox9e(ctx,t.radius,ts,vivPct631);
  }
  else if(t.type==="wavellite_orb9e"){
    const wavPct631=(Math.sin((Date.now()-t.spawnedAt)*0.3390)+1)/2;
    t._wavPct631=wavPct631;
    drawWavelliteOrb9e(ctx,t.radius,ts,wavPct631);
  }
  else if(t.type==="ulexite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="ulexite_fox9e"){'
A7_NEW = '''    if(hit.type==="vivianite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo631viv=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult631viv=gs.feverActive?2:1;
      const isPeak631viv=((hit._vivPct631||0)>0.88);
      const pts631viv=Math.round((isPeak631viv?578:388)*combo631viv*feverMult631viv);
      gs.score+=pts631viv;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1834,"#1e40af");
      if(isPeak631viv){spawnPopup(hit.x,hit.y-28,"🫐 +"+pts631viv,theme.accent);unlock("vivianite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts631viv,theme.accent);}
      unlock("vivianite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="wavellite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo631wav=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult631wav=gs.feverActive?2:1;
      const isPeak631wav=((hit._wavPct631||0)>0.88);
      const pts631wav=Math.round((isPeak631wav?566:380)*combo631wav*feverMult631wav);
      gs.score+=pts631wav;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1836,"#65a30d");
      if(isPeak631wav){spawnPopup(hit.x,hit.y-28,"🍋 +"+pts631wav,theme.accent);unlock("wavellite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts631wav,theme.accent);}
      unlock("wavellite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="ulexite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="ulexite_fox9e";color="#475569";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="uvarovite_orb9e"')
A8_NEW = ('      type="vivianite_fox9e";color="#1e40af";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wavellite_orb9e";color="#65a30d";glow="#f7fee7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="ulexite_fox9e";color="#475569";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="uvarovite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="ulexite_fox9e"?BASE_R*1.15:type==="uvarovite_orb9e"?BASE_R*1.14:'
A9_NEW = 'type==="vivianite_fox9e"?BASE_R*1.16:type==="wavellite_orb9e"?BASE_R*1.15:type==="ulexite_fox9e"?BASE_R*1.15:type==="uvarovite_orb9e"?BASE_R*1.14:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'ECLIPSE_RAY40:"🌒⚡",COSMIC_RAY40:"🌌⚡",VOID_RAY40:"⚫⚡"'
A10_NEW = 'STELLAR_RAY40:"⭐⚡",LUNAR_RAY40:"🌙⚡",ECLIPSE_RAY40:"🌒⚡",COSMIC_RAY40:"🌌⚡",VOID_RAY40:"⚫⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 631 done! +{len(content)-original_size} bytes")
