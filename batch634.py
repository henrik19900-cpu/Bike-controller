#!/usr/bin/env python3
# Batch 634: SOLAR_BEAM41 + AURORA_BEAM41 + arsenopyrite_fox9e + autunite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"annabergite_orb9e_peak", label:"Annabergite Orb Peak",'
A1_NEW = '''{ id:"solar_beam41_use", label:"Solar Beam", desc:"Activate SOLAR_BEAM41 power-up", icon:"☀️", xp:60 },
  { id:"solar_beam41_max", label:"Solar Beamer", desc:"Reach max with SOLAR_BEAM41 active", icon:"☀️", xp:120 },
  { id:"aurora_beam41_use", label:"Aurora Beam", desc:"Activate AURORA_BEAM41 power-up", icon:"🌠", xp:60 },
  { id:"aurora_beam41_max", label:"Aurora Beamer", desc:"Reach max with AURORA_BEAM41 active", icon:"🌠", xp:120 },
  { id:"arsenopyrite_fox9e_tap", label:"Arsenopyrite Fox", desc:"Tap an Arsenopyrite Fox target", icon:"🦊", xp:60 },
  { id:"arsenopyrite_fox9e_peak", label:"Arsenopyrite Fox Peak", desc:"Reach peak with Arsenopyrite Fox", icon:"🦊", xp:120 },
  { id:"autunite_orb9e_tap", label:"Autunite Orb", desc:"Tap an Autunite Orb target", icon:"🔮", xp:60 },
  { id:"autunite_orb9e_peak", label:"Autunite Orb Peak", desc:"Reach peak with Autunite Orb", icon:"🔮", xp:120 },
  { id:"annabergite_orb9e_peak", label:"Annabergite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"PRISM_BEAM41","NEXUS_BEAM41","NOVA_RAY40"'
A2_NEW = '"SOLAR_BEAM41","AURORA_BEAM41","PRISM_BEAM41","NEXUS_BEAM41","NOVA_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="PRISM_BEAM41"){'
A3_NEW = '''} else if(ptype==="SOLAR_BEAM41"){
        activePwrRef.current.push({type:"SOLAR_BEAM41",left:12000});
        sfx("comboNote",1663);
        unlock("solar_beam41_use");
      } else if(ptype==="AURORA_BEAM41"){
        activePwrRef.current.push({type:"AURORA_BEAM41",left:12000});
        sfx("comboNote",1665);
        unlock("aurora_beam41_use");
      } else if(ptype==="PRISM_BEAM41"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // PRISM_BEAM41 — +1996 prism bonus'
A4_NEW = '''  // SOLAR_BEAM41 — +2000 solar bonus
  if(activePwrRef.current.some(p=>p.type==="SOLAR_BEAM41")){
    const bonusTotal=Math.round(95.4*1000);
    gs.score+=2000;showPopup(cx,cy-1710,"+2000 ☀️💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a039c",1872);
    if(gs.score>=bonusTotal)unlock("solar_beam41_max");
  }
  // AURORA_BEAM41 — +2002 aurora bonus
  if(activePwrRef.current.some(p=>p.type==="AURORA_BEAM41")){
    const bonusTotal=Math.round(95.5*1000);
    gs.score+=2002;showPopup(cx,cy-1712,"+2002 🌠💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0870",1874);
    if(gs.score>=bonusTotal)unlock("aurora_beam41_max");
  }
  // PRISM_BEAM41 — +1996 prism bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawAlunogenFox9e('
A5_NEW = '''function drawArsenopyrlteFox9e(ctx,r,ts,arsPct){
  const bob=Math.sin(ts*0.3410)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f9fafb");g.addColorStop(0.45+arsPct*0.35,"#6b7280");g.addColorStop(1,"#1f2937");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(arsPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(107,114,128,"+(arsPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=arsPct>0.88?"#9ca3af":"#f9fafb";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(arsPct>0.88?"⚙️":"🦊",0,1);
  ctx.restore();
}
function drawAutuniteOrb9e(ctx,r,ts,autPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3414);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+autPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fefce8");g.addColorStop(0.35+autPct*0.35,"#a16207");g.addColorStop(1,"#713f12");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+autPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(161,98,7,"+(0.45+autPct*0.55)+")";ctx.lineWidth=3.5+autPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(autPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(202,138,4,"+(autPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=autPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(autPct>0.88?"☢️":"🔮",0,1);
  ctx.restore();
}
function drawAlunogenFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="alunogen_fox9e"){'
A6_NEW = '''  else if(t.type==="arsenopyrite_fox9e"){
    const arsPct634=(Math.sin((Date.now()-t.spawnedAt)*0.3410)+1)/2;
    t._arsPct634=arsPct634;
    drawArsenopyrlteFox9e(ctx,t.radius,ts,arsPct634);
  }
  else if(t.type==="autunite_orb9e"){
    const autPct634=(Math.sin((Date.now()-t.spawnedAt)*0.3414)+1)/2;
    t._autPct634=autPct634;
    drawAutuniteOrb9e(ctx,t.radius,ts,autPct634);
  }
  else if(t.type==="alunogen_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="alunogen_fox9e"){'
A7_NEW = '''    if(hit.type==="arsenopyrite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo634ars=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult634ars=gs.feverActive?2:1;
      const isPeak634ars=((hit._arsPct634||0)>0.88);
      const pts634ars=Math.round((isPeak634ars?584:394)*combo634ars*feverMult634ars);
      gs.score+=pts634ars;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1846,"#6b7280");
      if(isPeak634ars){spawnPopup(hit.x,hit.y-28,"⚙️ +"+pts634ars,theme.accent);unlock("arsenopyrite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts634ars,theme.accent);}
      unlock("arsenopyrite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="autunite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo634aut=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult634aut=gs.feverActive?2:1;
      const isPeak634aut=((hit._autPct634||0)>0.88);
      const pts634aut=Math.round((isPeak634aut?572:386)*combo634aut*feverMult634aut);
      gs.score+=pts634aut;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1848,"#a16207");
      if(isPeak634aut){spawnPopup(hit.x,hit.y-28,"☢️ +"+pts634aut,theme.accent);unlock("autunite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts634aut,theme.accent);}
      unlock("autunite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="alunogen_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="alunogen_fox9e";color="#737373";glow="#fafafa";\n'
          '    } else if('+COND100F+'){\n'
          '      type="annabergite_orb9e"')
A8_NEW = ('      type="arsenopyrite_fox9e";color="#6b7280";glow="#f9fafb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="autunite_orb9e";color="#a16207";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="alunogen_fox9e";color="#737373";glow="#fafafa";\n'
          '    } else if('+COND100F+'){\n'
          '      type="annabergite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="alunogen_fox9e"?BASE_R*1.18:type==="annabergite_orb9e"?BASE_R*1.17:'
A9_NEW = 'type==="arsenopyrite_fox9e"?BASE_R*1.19:type==="autunite_orb9e"?BASE_R*1.18:type==="alunogen_fox9e"?BASE_R*1.18:type==="annabergite_orb9e"?BASE_R*1.17:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'PRISM_BEAM41:"🔷💥",NEXUS_BEAM41:"🌐💥",NOVA_RAY40:"💥⚡"'
A10_NEW = 'SOLAR_BEAM41:"☀️💥",AURORA_BEAM41:"🌠💥",PRISM_BEAM41:"🔷💥",NEXUS_BEAM41:"🌐💥",NOVA_RAY40:"💥⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 634 done! +{len(content)-original_size} bytes")
