#!/usr/bin/env python3
# Batch 632: NOVA_RAY40 + VOID_BEAM40 + xenotime_fox9e + zinnwaldite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"wavellite_orb9e_peak", label:"Wavellite Orb Peak",'
A1_NEW = '''{ id:"nova_ray40_use", label:"Nova Ray", desc:"Activate NOVA_RAY40 power-up", icon:"💥", xp:60 },
  { id:"nova_ray40_max", label:"Nova Rayer", desc:"Reach max with NOVA_RAY40 active", icon:"💥", xp:120 },
  { id:"void_beam40_use", label:"Void Beam", desc:"Activate VOID_BEAM40 power-up", icon:"🔦", xp:60 },
  { id:"void_beam40_max", label:"Void Beamer", desc:"Reach max with VOID_BEAM40 active", icon:"🔦", xp:120 },
  { id:"xenotime_fox9e_tap", label:"Xenotime Fox", desc:"Tap a Xenotime Fox target", icon:"🦊", xp:60 },
  { id:"xenotime_fox9e_peak", label:"Xenotime Fox Peak", desc:"Reach peak with Xenotime Fox", icon:"🦊", xp:120 },
  { id:"zinnwaldite_orb9e_tap", label:"Zinnwaldite Orb", desc:"Tap a Zinnwaldite Orb target", icon:"🔮", xp:60 },
  { id:"zinnwaldite_orb9e_peak", label:"Zinnwaldite Orb Peak", desc:"Reach peak with Zinnwaldite Orb", icon:"🔮", xp:120 },
  { id:"wavellite_orb9e_peak", label:"Wavellite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"STELLAR_RAY40","LUNAR_RAY40","ECLIPSE_RAY40"'
A2_NEW = '"NOVA_RAY40","VOID_BEAM40","STELLAR_RAY40","LUNAR_RAY40","ECLIPSE_RAY40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="STELLAR_RAY40"){'
A3_NEW = '''} else if(ptype==="NOVA_RAY40"){
        activePwrRef.current.push({type:"NOVA_RAY40",left:12000});
        sfx("comboNote",1655);
        unlock("nova_ray40_use");
      } else if(ptype==="VOID_BEAM40"){
        activePwrRef.current.push({type:"VOID_BEAM40",left:12000});
        sfx("comboNote",1657);
        unlock("void_beam40_use");
      } else if(ptype==="STELLAR_RAY40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // STELLAR_RAY40 — +1988 stellar bonus'
A4_NEW = '''  // NOVA_RAY40 — +1992 nova bonus
  if(activePwrRef.current.some(p=>p.type==="NOVA_RAY40")){
    const bonusTotal=Math.round(95.0*1000);
    gs.score+=1992;showPopup(cx,cy-1702,"+1992 💥⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0398",1864);
    if(gs.score>=bonusTotal)unlock("nova_ray40_max");
  }
  // VOID_BEAM40 — +1994 void bonus
  if(activePwrRef.current.some(p=>p.type==="VOID_BEAM40")){
    const bonusTotal=Math.round(95.1*1000);
    gs.score+=1994;showPopup(cx,cy-1704,"+1994 🔦💥",theme.accent,26);
    spawnShockwave(cx,cy,"#0a086c",1866);
    if(gs.score>=bonusTotal)unlock("void_beam40_max");
  }
  // STELLAR_RAY40 — +1988 stellar bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawVivianiteFox9e('
A5_NEW = '''function drawXenotimeFox9e(ctx,r,ts,xenoPct){
  const bob=Math.sin(ts*0.3394)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+xenoPct*0.35,"#854d0e");g.addColorStop(1,"#431407");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(xenoPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(133,77,14,"+(xenoPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=xenoPct>0.88?"#fcd34d":"#fefce8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(xenoPct>0.88?"🪙":"🦊",0,1);
  ctx.restore();
}
function drawZinnwalditeOrb9e(ctx,r,ts,zinnPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3398);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+zinnPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.35+zinnPct*0.35,"#9d174d");g.addColorStop(1,"#500724");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+zinnPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(157,23,77,"+(0.45+zinnPct*0.55)+")";ctx.lineWidth=3.5+zinnPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(zinnPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(219,39,119,"+(zinnPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=zinnPct>0.88?"#f9a8d4":"#fdf2f8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(zinnPct>0.88?"🌸":"🔮",0,1);
  ctx.restore();
}
function drawVivianiteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="vivianite_fox9e"){'
A6_NEW = '''  else if(t.type==="xenotime_fox9e"){
    const xenoPct632=(Math.sin((Date.now()-t.spawnedAt)*0.3394)+1)/2;
    t._xenoPct632=xenoPct632;
    drawXenotimeFox9e(ctx,t.radius,ts,xenoPct632);
  }
  else if(t.type==="zinnwaldite_orb9e"){
    const zinnPct632=(Math.sin((Date.now()-t.spawnedAt)*0.3398)+1)/2;
    t._zinnPct632=zinnPct632;
    drawZinnwalditeOrb9e(ctx,t.radius,ts,zinnPct632);
  }
  else if(t.type==="vivianite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="vivianite_fox9e"){'
A7_NEW = '''    if(hit.type==="xenotime_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo632xeno=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult632xeno=gs.feverActive?2:1;
      const isPeak632xeno=((hit._xenoPct632||0)>0.88);
      const pts632xeno=Math.round((isPeak632xeno?580:390)*combo632xeno*feverMult632xeno);
      gs.score+=pts632xeno;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1838,"#854d0e");
      if(isPeak632xeno){spawnPopup(hit.x,hit.y-28,"🪙 +"+pts632xeno,theme.accent);unlock("xenotime_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts632xeno,theme.accent);}
      unlock("xenotime_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="zinnwaldite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo632zinn=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult632zinn=gs.feverActive?2:1;
      const isPeak632zinn=((hit._zinnPct632||0)>0.88);
      const pts632zinn=Math.round((isPeak632zinn?568:382)*combo632zinn*feverMult632zinn);
      gs.score+=pts632zinn;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1840,"#9d174d");
      if(isPeak632zinn){spawnPopup(hit.x,hit.y-28,"🌸 +"+pts632zinn,theme.accent);unlock("zinnwaldite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts632zinn,theme.accent);}
      unlock("zinnwaldite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="vivianite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="vivianite_fox9e";color="#1e40af";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wavellite_orb9e"')
A8_NEW = ('      type="xenotime_fox9e";color="#854d0e";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="zinnwaldite_orb9e";color="#9d174d";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="vivianite_fox9e";color="#1e40af";glow="#eff6ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="wavellite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="vivianite_fox9e"?BASE_R*1.16:type==="wavellite_orb9e"?BASE_R*1.15:'
A9_NEW = 'type==="xenotime_fox9e"?BASE_R*1.17:type==="zinnwaldite_orb9e"?BASE_R*1.16:type==="vivianite_fox9e"?BASE_R*1.16:type==="wavellite_orb9e"?BASE_R*1.15:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'STELLAR_RAY40:"⭐⚡",LUNAR_RAY40:"🌙⚡",ECLIPSE_RAY40:"🌒⚡"'
A10_NEW = 'NOVA_RAY40:"💥⚡",VOID_BEAM40:"🔦💥",STELLAR_RAY40:"⭐⚡",LUNAR_RAY40:"🌙⚡",ECLIPSE_RAY40:"🌒⚡"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 632 done! +{len(content)-original_size} bytes")
