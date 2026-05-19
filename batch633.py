#!/usr/bin/env python3
# Batch 633: PRISM_BEAM41 + NEXUS_BEAM41 + alunogen_fox9e + annabergite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"zinnwaldite_orb9e_peak", label:"Zinnwaldite Orb Peak",'
A1_NEW = '''{ id:"prism_beam41_use", label:"Prism Beam", desc:"Activate PRISM_BEAM41 power-up", icon:"🔷", xp:60 },
  { id:"prism_beam41_max", label:"Prism Beamer", desc:"Reach max with PRISM_BEAM41 active", icon:"🔷", xp:120 },
  { id:"nexus_beam41_use", label:"Nexus Beam", desc:"Activate NEXUS_BEAM41 power-up", icon:"🌐", xp:60 },
  { id:"nexus_beam41_max", label:"Nexus Beamer", desc:"Reach max with NEXUS_BEAM41 active", icon:"🌐", xp:120 },
  { id:"alunogen_fox9e_tap", label:"Alunogen Fox", desc:"Tap an Alunogen Fox target", icon:"🦊", xp:60 },
  { id:"alunogen_fox9e_peak", label:"Alunogen Fox Peak", desc:"Reach peak with Alunogen Fox", icon:"🦊", xp:120 },
  { id:"annabergite_orb9e_tap", label:"Annabergite Orb", desc:"Tap an Annabergite Orb target", icon:"🔮", xp:60 },
  { id:"annabergite_orb9e_peak", label:"Annabergite Orb Peak", desc:"Reach peak with Annabergite Orb", icon:"🔮", xp:120 },
  { id:"zinnwaldite_orb9e_peak", label:"Zinnwaldite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"NOVA_RAY40","VOID_BEAM40","STELLAR_RAY40"'
A2_NEW = '"PRISM_BEAM41","NEXUS_BEAM41","NOVA_RAY40","VOID_BEAM40","STELLAR_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="NOVA_RAY40"){'
A3_NEW = '''} else if(ptype==="PRISM_BEAM41"){
        activePwrRef.current.push({type:"PRISM_BEAM41",left:12000});
        sfx("comboNote",1659);
        unlock("prism_beam41_use");
      } else if(ptype==="NEXUS_BEAM41"){
        activePwrRef.current.push({type:"NEXUS_BEAM41",left:12000});
        sfx("comboNote",1661);
        unlock("nexus_beam41_use");
      } else if(ptype==="NOVA_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // NOVA_RAY40 — +1992 nova bonus'
A4_NEW = '''  // PRISM_BEAM41 — +1996 prism bonus
  if(activePwrRef.current.some(p=>p.type==="PRISM_BEAM41")){
    const bonusTotal=Math.round(95.2*1000);
    gs.score+=1996;showPopup(cx,cy-1706,"+1996 🔷💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a039a",1868);
    if(gs.score>=bonusTotal)unlock("prism_beam41_max");
  }
  // NEXUS_BEAM41 — +1998 nexus bonus
  if(activePwrRef.current.some(p=>p.type==="NEXUS_BEAM41")){
    const bonusTotal=Math.round(95.3*1000);
    gs.score+=1998;showPopup(cx,cy-1708,"+1998 🌐💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a086e",1870);
    if(gs.score>=bonusTotal)unlock("nexus_beam41_max");
  }
  // NOVA_RAY40 — +1992 nova bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawXenotimeFox9e('
A5_NEW = '''function drawAlunogenFox9e(ctx,r,ts,alunPct){
  const bob=Math.sin(ts*0.3402)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fafafa");g.addColorStop(0.45+alunPct*0.35,"#737373");g.addColorStop(1,"#262626");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(alunPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(115,115,115,"+(alunPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=alunPct>0.88?"#d4d4d4":"#fafafa";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(alunPct>0.88?"🪡":"🦊",0,1);
  ctx.restore();
}
function drawAnnabergiteOrb9e(ctx,r,ts,annaPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3406);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+annaPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.35+annaPct*0.35,"#15803d");g.addColorStop(1,"#14532d");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+annaPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(21,128,61,"+(0.45+annaPct*0.55)+")";ctx.lineWidth=3.5+annaPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(annaPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(34,197,94,"+(annaPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=annaPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(annaPct>0.88?"🟩":"🔮",0,1);
  ctx.restore();
}
function drawXenotimeFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="xenotime_fox9e"){'
A6_NEW = '''  else if(t.type==="alunogen_fox9e"){
    const alunPct633=(Math.sin((Date.now()-t.spawnedAt)*0.3402)+1)/2;
    t._alunPct633=alunPct633;
    drawAlunogenFox9e(ctx,t.radius,ts,alunPct633);
  }
  else if(t.type==="annabergite_orb9e"){
    const annaPct633=(Math.sin((Date.now()-t.spawnedAt)*0.3406)+1)/2;
    t._annaPct633=annaPct633;
    drawAnnabergiteOrb9e(ctx,t.radius,ts,annaPct633);
  }
  else if(t.type==="xenotime_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="xenotime_fox9e"){'
A7_NEW = '''    if(hit.type==="alunogen_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo633alun=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult633alun=gs.feverActive?2:1;
      const isPeak633alun=((hit._alunPct633||0)>0.88);
      const pts633alun=Math.round((isPeak633alun?582:392)*combo633alun*feverMult633alun);
      gs.score+=pts633alun;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1842,"#737373");
      if(isPeak633alun){spawnPopup(hit.x,hit.y-28,"🪡 +"+pts633alun,theme.accent);unlock("alunogen_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts633alun,theme.accent);}
      unlock("alunogen_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="annabergite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo633anna=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult633anna=gs.feverActive?2:1;
      const isPeak633anna=((hit._annaPct633||0)>0.88);
      const pts633anna=Math.round((isPeak633anna?570:384)*combo633anna*feverMult633anna);
      gs.score+=pts633anna;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1844,"#15803d");
      if(isPeak633anna){spawnPopup(hit.x,hit.y-28,"🟩 +"+pts633anna,theme.accent);unlock("annabergite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts633anna,theme.accent);}
      unlock("annabergite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="xenotime_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="xenotime_fox9e";color="#854d0e";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zinnwaldite_orb9e"')
A8_NEW = ('      type="alunogen_fox9e";color="#737373";glow="#fafafa";\n'
          '    } else if('+COND100F+'){\n'
          '      type="annabergite_orb9e";color="#15803d";glow="#f0fdf4";\n'
          '    } else if('+COND100F+'){\n'
          '      type="xenotime_fox9e";color="#854d0e";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zinnwaldite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="xenotime_fox9e"?BASE_R*1.17:type==="zinnwaldite_orb9e"?BASE_R*1.16:'
A9_NEW = 'type==="alunogen_fox9e"?BASE_R*1.18:type==="annabergite_orb9e"?BASE_R*1.17:type==="xenotime_fox9e"?BASE_R*1.17:type==="zinnwaldite_orb9e"?BASE_R*1.16:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'NOVA_RAY40:"💥⚡",VOID_BEAM40:"🔦💥",STELLAR_RAY40:"⭐⚡"'
A10_NEW = 'PRISM_BEAM41:"🔷💥",NEXUS_BEAM41:"🌐💥",NOVA_RAY40:"💥⚡",VOID_BEAM40:"🔦💥",STELLAR_RAY40:"⭐⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 633 done! +{len(content)-original_size} bytes")
