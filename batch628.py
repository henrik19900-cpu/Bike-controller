#!/usr/bin/env python3
# Batch 628: NEXUS_RAY40 + SOLAR_RAY40 + sylvite_fox9e + sodalite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"spessartine_orb9e_peak", label:"Spessartine Orb Peak",'
A1_NEW = '''{ id:"nexus_ray40_use", label:"Nexus Ray", desc:"Activate NEXUS_RAY40 power-up", icon:"🌐", xp:60 },
  { id:"nexus_ray40_max", label:"Nexus Rayer", desc:"Reach max with NEXUS_RAY40 active", icon:"🌐", xp:120 },
  { id:"solar_ray40_use", label:"Solar Ray", desc:"Activate SOLAR_RAY40 power-up", icon:"☀️", xp:60 },
  { id:"solar_ray40_max", label:"Solar Rayer", desc:"Reach max with SOLAR_RAY40 active", icon:"☀️", xp:120 },
  { id:"sylvite_fox9e_tap", label:"Sylvite Fox", desc:"Tap a Sylvite Fox target", icon:"🦊", xp:60 },
  { id:"sylvite_fox9e_peak", label:"Sylvite Fox Peak", desc:"Reach peak with Sylvite Fox", icon:"🦊", xp:120 },
  { id:"sodalite_orb9e_tap", label:"Sodalite Orb", desc:"Tap a Sodalite Orb target", icon:"🔮", xp:60 },
  { id:"sodalite_orb9e_peak", label:"Sodalite Orb Peak", desc:"Reach peak with Sodalite Orb", icon:"🔮", xp:120 },
  { id:"spessartine_orb9e_peak", label:"Spessartine Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"AURORA_RAY40","THUNDER_RAY40","NOVA_FLARE40"'
A2_NEW = '"NEXUS_RAY40","SOLAR_RAY40","AURORA_RAY40","THUNDER_RAY40","NOVA_FLARE40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_RAY40"){'
A3_NEW = '''} else if(ptype==="NEXUS_RAY40"){
        activePwrRef.current.push({type:"NEXUS_RAY40",left:12000});
        sfx("comboNote",1639);
        unlock("nexus_ray40_use");
      } else if(ptype==="SOLAR_RAY40"){
        activePwrRef.current.push({type:"SOLAR_RAY40",left:12000});
        sfx("comboNote",1641);
        unlock("solar_ray40_use");
      } else if(ptype==="AURORA_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // AURORA_RAY40 — +1972 aurora bonus'
A4_NEW = '''  // NEXUS_RAY40 — +1976 nexus bonus
  if(activePwrRef.current.some(p=>p.type==="NEXUS_RAY40")){
    const bonusTotal=Math.round(94.2*1000);
    gs.score+=1976;showPopup(cx,cy-1686,"+1976 🌐⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0390",1848);
    if(gs.score>=bonusTotal)unlock("nexus_ray40_max");
  }
  // SOLAR_RAY40 — +1978 solar bonus
  if(activePwrRef.current.some(p=>p.type==="SOLAR_RAY40")){
    const bonusTotal=Math.round(94.3*1000);
    gs.score+=1978;showPopup(cx,cy-1688,"+1978 ☀️⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0864",1850);
    if(gs.score>=bonusTotal)unlock("solar_ray40_max");
  }
  // AURORA_RAY40 — +1972 aurora bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSillimaniteFox9e('
A5_NEW = '''function drawSylviteFox9e(ctx,r,ts,sylvPct){
  const bob=Math.sin(ts*0.3362)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#faf5ff");g.addColorStop(0.45+sylvPct*0.35,"#9333ea");g.addColorStop(1,"#4a044e");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(sylvPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(147,51,234,"+(sylvPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=sylvPct>0.88?"#d8b4fe":"#faf5ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sylvPct>0.88?"💜":"🦊",0,1);
  ctx.restore();
}
function drawSodaliteOrb9e(ctx,r,ts,sodPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3366);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+sodPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#eff6ff");g.addColorStop(0.35+sodPct*0.35,"#1d4ed8");g.addColorStop(1,"#1e1b4b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+sodPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(29,78,216,"+(0.45+sodPct*0.55)+")";ctx.lineWidth=3.5+sodPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(sodPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(59,130,246,"+(sodPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=sodPct>0.88?"#93c5fd":"#eff6ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sodPct>0.88?"🔵":"🔮",0,1);
  ctx.restore();
}
function drawSillimaniteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="sillimanite_fox9e"){'
A6_NEW = '''  else if(t.type==="sylvite_fox9e"){
    const sylvPct628=(Math.sin((Date.now()-t.spawnedAt)*0.3362)+1)/2;
    t._sylvPct628=sylvPct628;
    drawSylviteFox9e(ctx,t.radius,ts,sylvPct628);
  }
  else if(t.type==="sodalite_orb9e"){
    const sodPct628=(Math.sin((Date.now()-t.spawnedAt)*0.3366)+1)/2;
    t._sodPct628=sodPct628;
    drawSodaliteOrb9e(ctx,t.radius,ts,sodPct628);
  }
  else if(t.type==="sillimanite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="sillimanite_fox9e"){'
A7_NEW = '''    if(hit.type==="sylvite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo628sylv=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult628sylv=gs.feverActive?2:1;
      const isPeak628sylv=((hit._sylvPct628||0)>0.88);
      const pts628sylv=Math.round((isPeak628sylv?572:382)*combo628sylv*feverMult628sylv);
      gs.score+=pts628sylv;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1822,"#9333ea");
      if(isPeak628sylv){spawnPopup(hit.x,hit.y-28,"💜 +"+pts628sylv,theme.accent);unlock("sylvite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts628sylv,theme.accent);}
      unlock("sylvite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="sodalite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo628sod=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult628sod=gs.feverActive?2:1;
      const isPeak628sod=((hit._sodPct628||0)>0.88);
      const pts628sod=Math.round((isPeak628sod?560:374)*combo628sod*feverMult628sod);
      gs.score+=pts628sod;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1824,"#1d4ed8");
      if(isPeak628sod){spawnPopup(hit.x,hit.y-28,"🔵 +"+pts628sod,theme.accent);unlock("sodalite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts628sod,theme.accent);}
      unlock("sodalite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="sillimanite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="sillimanite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="spessartine_orb9e"')
A8_NEW = ('      type="sylvite_fox9e";color="#9333ea";glow="#faf5ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sodalite_orb9e";color="#1d4ed8";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sillimanite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="spessartine_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="sillimanite_fox9e"?BASE_R*1.12:type==="spessartine_orb9e"?BASE_R*1.11:'
A9_NEW = 'type==="sylvite_fox9e"?BASE_R*1.13:type==="sodalite_orb9e"?BASE_R*1.12:type==="sillimanite_fox9e"?BASE_R*1.12:type==="spessartine_orb9e"?BASE_R*1.11:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'AURORA_RAY40:"🌠⚡",THUNDER_RAY40:"⚡🌠",NOVA_FLARE40:"💥✨"'
A10_NEW = 'NEXUS_RAY40:"🌐⚡",SOLAR_RAY40:"☀️⚡",AURORA_RAY40:"🌠⚡",THUNDER_RAY40:"⚡🌠",NOVA_FLARE40:"💥✨"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 628 done! +{len(content)-original_size} bytes")
