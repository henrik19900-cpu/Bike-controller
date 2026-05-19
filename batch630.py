#!/usr/bin/env python3
# Batch 630: ECLIPSE_RAY40 + COSMIC_RAY40 + ulexite_fox9e + uvarovite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"tremolite_orb9e_peak", label:"Tremolite Orb Peak",'
A1_NEW = '''{ id:"eclipse_ray40_use", label:"Eclipse Ray", desc:"Activate ECLIPSE_RAY40 power-up", icon:"🌒", xp:60 },
  { id:"eclipse_ray40_max", label:"Eclipse Rayer", desc:"Reach max with ECLIPSE_RAY40 active", icon:"🌒", xp:120 },
  { id:"cosmic_ray40_use", label:"Cosmic Ray", desc:"Activate COSMIC_RAY40 power-up", icon:"🌌", xp:60 },
  { id:"cosmic_ray40_max", label:"Cosmic Rayer", desc:"Reach max with COSMIC_RAY40 active", icon:"🌌", xp:120 },
  { id:"ulexite_fox9e_tap", label:"Ulexite Fox", desc:"Tap an Ulexite Fox target", icon:"🦊", xp:60 },
  { id:"ulexite_fox9e_peak", label:"Ulexite Fox Peak", desc:"Reach peak with Ulexite Fox", icon:"🦊", xp:120 },
  { id:"uvarovite_orb9e_tap", label:"Uvarovite Orb", desc:"Tap an Uvarovite Orb target", icon:"🔮", xp:60 },
  { id:"uvarovite_orb9e_peak", label:"Uvarovite Orb Peak", desc:"Reach peak with Uvarovite Orb", icon:"🔮", xp:120 },
  { id:"tremolite_orb9e_peak", label:"Tremolite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"VOID_RAY40","PRISM_RAY40","NEXUS_RAY40"'
A2_NEW = '"ECLIPSE_RAY40","COSMIC_RAY40","VOID_RAY40","PRISM_RAY40","NEXUS_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="VOID_RAY40"){'
A3_NEW = '''} else if(ptype==="ECLIPSE_RAY40"){
        activePwrRef.current.push({type:"ECLIPSE_RAY40",left:12000});
        sfx("comboNote",1647);
        unlock("eclipse_ray40_use");
      } else if(ptype==="COSMIC_RAY40"){
        activePwrRef.current.push({type:"COSMIC_RAY40",left:12000});
        sfx("comboNote",1649);
        unlock("cosmic_ray40_use");
      } else if(ptype==="VOID_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // VOID_RAY40 — +1980 void bonus'
A4_NEW = '''  // ECLIPSE_RAY40 — +1984 eclipse bonus
  if(activePwrRef.current.some(p=>p.type==="ECLIPSE_RAY40")){
    const bonusTotal=Math.round(94.6*1000);
    gs.score+=1984;showPopup(cx,cy-1694,"+1984 🌒⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0394",1856);
    if(gs.score>=bonusTotal)unlock("eclipse_ray40_max");
  }
  // COSMIC_RAY40 — +1986 cosmic bonus
  if(activePwrRef.current.some(p=>p.type==="COSMIC_RAY40")){
    const bonusTotal=Math.round(94.7*1000);
    gs.score+=1986;showPopup(cx,cy-1696,"+1986 🌌⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0868",1858);
    if(gs.score>=bonusTotal)unlock("cosmic_ray40_max");
  }
  // VOID_RAY40 — +1980 void bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawTourmalineFox9e('
A5_NEW = '''function drawUlexiteFox9e(ctx,r,ts,ulexPct){
  const bob=Math.sin(ts*0.3378)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f8fafc");g.addColorStop(0.45+ulexPct*0.35,"#475569");g.addColorStop(1,"#1e293b");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(ulexPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(71,85,105,"+(ulexPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=ulexPct>0.88?"#94a3b8":"#f8fafc";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(ulexPct>0.88?"🪨":"🦊",0,1);
  ctx.restore();
}
function drawUvaroviteOrb9e(ctx,r,ts,uvarPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3382);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+uvarPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+uvarPct*0.35,"#16a34a");g.addColorStop(1,"#14532d");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+uvarPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(22,163,74,"+(0.45+uvarPct*0.55)+")";ctx.lineWidth=3.5+uvarPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(uvarPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(34,197,94,"+(uvarPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=uvarPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(uvarPct>0.88?"🍀":"🔮",0,1);
  ctx.restore();
}
function drawTourmalineFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="tourmaline_fox9e"){'
A6_NEW = '''  else if(t.type==="ulexite_fox9e"){
    const ulexPct630=(Math.sin((Date.now()-t.spawnedAt)*0.3378)+1)/2;
    t._ulexPct630=ulexPct630;
    drawUlexiteFox9e(ctx,t.radius,ts,ulexPct630);
  }
  else if(t.type==="uvarovite_orb9e"){
    const uvarPct630=(Math.sin((Date.now()-t.spawnedAt)*0.3382)+1)/2;
    t._uvarPct630=uvarPct630;
    drawUvaroviteOrb9e(ctx,t.radius,ts,uvarPct630);
  }
  else if(t.type==="tourmaline_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="tourmaline_fox9e"){'
A7_NEW = '''    if(hit.type==="ulexite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo630ulex=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult630ulex=gs.feverActive?2:1;
      const isPeak630ulex=((hit._ulexPct630||0)>0.88);
      const pts630ulex=Math.round((isPeak630ulex?576:386)*combo630ulex*feverMult630ulex);
      gs.score+=pts630ulex;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1830,"#475569");
      if(isPeak630ulex){spawnPopup(hit.x,hit.y-28,"🪨 +"+pts630ulex,theme.accent);unlock("ulexite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts630ulex,theme.accent);}
      unlock("ulexite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="uvarovite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo630uvar=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult630uvar=gs.feverActive?2:1;
      const isPeak630uvar=((hit._uvarPct630||0)>0.88);
      const pts630uvar=Math.round((isPeak630uvar?564:378)*combo630uvar*feverMult630uvar);
      gs.score+=pts630uvar;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1832,"#16a34a");
      if(isPeak630uvar){spawnPopup(hit.x,hit.y-28,"🍀 +"+pts630uvar,theme.accent);unlock("uvarovite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts630uvar,theme.accent);}
      unlock("uvarovite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="tourmaline_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="tourmaline_fox9e";color="#a21caf";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tremolite_orb9e"')
A8_NEW = ('      type="ulexite_fox9e";color="#475569";glow="#f8fafc";\n'
          '    } else if('+COND100F+'){\n'
          '      type="uvarovite_orb9e";color="#16a34a";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tourmaline_fox9e";color="#a21caf";glow="#fdf4ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="tremolite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="tourmaline_fox9e"?BASE_R*1.14:type==="tremolite_orb9e"?BASE_R*1.13:'
A9_NEW = 'type==="ulexite_fox9e"?BASE_R*1.15:type==="uvarovite_orb9e"?BASE_R*1.14:type==="tourmaline_fox9e"?BASE_R*1.14:type==="tremolite_orb9e"?BASE_R*1.13:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'VOID_RAY40:"⚫⚡",PRISM_RAY40:"🔷⚡",NEXUS_RAY40:"🌐⚡"'
A10_NEW = 'ECLIPSE_RAY40:"🌒⚡",COSMIC_RAY40:"🌌⚡",VOID_RAY40:"⚫⚡",PRISM_RAY40:"🔷⚡",NEXUS_RAY40:"🌐⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 630 done! +{len(content)-original_size} bytes")
