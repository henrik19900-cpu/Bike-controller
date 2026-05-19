#!/usr/bin/env python3
# Batch 629: VOID_RAY40 + PRISM_RAY40 + tourmaline_fox9e + tremolite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"sodalite_orb9e_peak", label:"Sodalite Orb Peak",'
A1_NEW = '''{ id:"void_ray40_use", label:"Void Ray", desc:"Activate VOID_RAY40 power-up", icon:"⚫", xp:60 },
  { id:"void_ray40_max", label:"Void Rayer", desc:"Reach max with VOID_RAY40 active", icon:"⚫", xp:120 },
  { id:"prism_ray40_use", label:"Prism Ray", desc:"Activate PRISM_RAY40 power-up", icon:"🔷", xp:60 },
  { id:"prism_ray40_max", label:"Prism Rayer", desc:"Reach max with PRISM_RAY40 active", icon:"🔷", xp:120 },
  { id:"tourmaline_fox9e_tap", label:"Tourmaline Fox", desc:"Tap a Tourmaline Fox target", icon:"🦊", xp:60 },
  { id:"tourmaline_fox9e_peak", label:"Tourmaline Fox Peak", desc:"Reach peak with Tourmaline Fox", icon:"🦊", xp:120 },
  { id:"tremolite_orb9e_tap", label:"Tremolite Orb", desc:"Tap a Tremolite Orb target", icon:"🔮", xp:60 },
  { id:"tremolite_orb9e_peak", label:"Tremolite Orb Peak", desc:"Reach peak with Tremolite Orb", icon:"🔮", xp:120 },
  { id:"sodalite_orb9e_peak", label:"Sodalite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"NEXUS_RAY40","SOLAR_RAY40","AURORA_RAY40"'
A2_NEW = '"VOID_RAY40","PRISM_RAY40","NEXUS_RAY40","SOLAR_RAY40","AURORA_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="NEXUS_RAY40"){'
A3_NEW = '''} else if(ptype==="VOID_RAY40"){
        activePwrRef.current.push({type:"VOID_RAY40",left:12000});
        sfx("comboNote",1643);
        unlock("void_ray40_use");
      } else if(ptype==="PRISM_RAY40"){
        activePwrRef.current.push({type:"PRISM_RAY40",left:12000});
        sfx("comboNote",1645);
        unlock("prism_ray40_use");
      } else if(ptype==="NEXUS_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // NEXUS_RAY40 — +1976 nexus bonus'
A4_NEW = '''  // VOID_RAY40 — +1980 void bonus
  if(activePwrRef.current.some(p=>p.type==="VOID_RAY40")){
    const bonusTotal=Math.round(94.4*1000);
    gs.score+=1980;showPopup(cx,cy-1690,"+1980 ⚫⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0392",1852);
    if(gs.score>=bonusTotal)unlock("void_ray40_max");
  }
  // PRISM_RAY40 — +1982 prism bonus
  if(activePwrRef.current.some(p=>p.type==="PRISM_RAY40")){
    const bonusTotal=Math.round(94.5*1000);
    gs.score+=1982;showPopup(cx,cy-1692,"+1982 🔷⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0866",1854);
    if(gs.score>=bonusTotal)unlock("prism_ray40_max");
  }
  // NEXUS_RAY40 — +1976 nexus bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSylviteFox9e('
A5_NEW = '''function drawTourmalineFox9e(ctx,r,ts,tourPct){
  const bob=Math.sin(ts*0.3370)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fdf4ff");g.addColorStop(0.45+tourPct*0.35,"#a21caf");g.addColorStop(1,"#581c87");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(tourPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(162,28,175,"+(tourPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=tourPct>0.88?"#e879f9":"#fdf4ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tourPct>0.88?"🌺":"🦊",0,1);
  ctx.restore();
}
function drawTremoliteOrb9e(ctx,r,ts,tremPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3374);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tremPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#ecfdf5");g.addColorStop(0.35+tremPct*0.35,"#059669");g.addColorStop(1,"#064e3b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+tremPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(5,150,105,"+(0.45+tremPct*0.55)+")";ctx.lineWidth=3.5+tremPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(tremPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(16,185,129,"+(tremPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=tremPct>0.88?"#6ee7b7":"#ecfdf5";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tremPct>0.88?"💚":"🔮",0,1);
  ctx.restore();
}
function drawSylviteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="sylvite_fox9e"){'
A6_NEW = '''  else if(t.type==="tourmaline_fox9e"){
    const tourPct629=(Math.sin((Date.now()-t.spawnedAt)*0.3370)+1)/2;
    t._tourPct629=tourPct629;
    drawTourmalineFox9e(ctx,t.radius,ts,tourPct629);
  }
  else if(t.type==="tremolite_orb9e"){
    const tremPct629=(Math.sin((Date.now()-t.spawnedAt)*0.3374)+1)/2;
    t._tremPct629=tremPct629;
    drawTremoliteOrb9e(ctx,t.radius,ts,tremPct629);
  }
  else if(t.type==="sylvite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="sylvite_fox9e"){'
A7_NEW = '''    if(hit.type==="tourmaline_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo629tour=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult629tour=gs.feverActive?2:1;
      const isPeak629tour=((hit._tourPct629||0)>0.88);
      const pts629tour=Math.round((isPeak629tour?574:384)*combo629tour*feverMult629tour);
      gs.score+=pts629tour;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1826,"#a21caf");
      if(isPeak629tour){spawnPopup(hit.x,hit.y-28,"🌺 +"+pts629tour,theme.accent);unlock("tourmaline_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts629tour,theme.accent);}
      unlock("tourmaline_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="tremolite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo629trem=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult629trem=gs.feverActive?2:1;
      const isPeak629trem=((hit._tremPct629||0)>0.88);
      const pts629trem=Math.round((isPeak629trem?562:376)*combo629trem*feverMult629trem);
      gs.score+=pts629trem;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1828,"#059669");
      if(isPeak629trem){spawnPopup(hit.x,hit.y-28,"💚 +"+pts629trem,theme.accent);unlock("tremolite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts629trem,theme.accent);}
      unlock("tremolite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="sylvite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="sylvite_fox9e";color="#9333ea";glow="#faf5ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sodalite_orb9e"')
A8_NEW = ('      type="tourmaline_fox9e";color="#a21caf";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tremolite_orb9e";color="#059669";glow="#ecfdf5";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sylvite_fox9e";color="#9333ea";glow="#faf5ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sodalite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="sylvite_fox9e"?BASE_R*1.13:type==="sodalite_orb9e"?BASE_R*1.12:'
A9_NEW = 'type==="tourmaline_fox9e"?BASE_R*1.14:type==="tremolite_orb9e"?BASE_R*1.13:type==="sylvite_fox9e"?BASE_R*1.13:type==="sodalite_orb9e"?BASE_R*1.12:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'NEXUS_RAY40:"🌐⚡",SOLAR_RAY40:"☀️⚡",AURORA_RAY40:"🌠⚡"'
A10_NEW = 'VOID_RAY40:"⚫⚡",PRISM_RAY40:"🔷⚡",NEXUS_RAY40:"🌐⚡",SOLAR_RAY40:"☀️⚡",AURORA_RAY40:"🌠⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 629 done! +{len(content)-original_size} bytes")
