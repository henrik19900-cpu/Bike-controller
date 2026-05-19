#!/usr/bin/env python3
# Batch 625: STELLAR_FLARE40 + LUNAR_FLARE40 + rhodochrosite_fox9e + rutile_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"pyrargyrite_orb9e_peak", label:"Pyrargyrite Orb Peak",'
A1_NEW = '''{ id:"stellar_flare40_use", label:"Stellar Flare", desc:"Activate STELLAR_FLARE40 power-up", icon:"⭐", xp:60 },
  { id:"stellar_flare40_max", label:"Stellar Surger", desc:"Reach max with STELLAR_FLARE40 active", icon:"⭐", xp:120 },
  { id:"lunar_flare40_use", label:"Lunar Flare", desc:"Activate LUNAR_FLARE40 power-up", icon:"🌙", xp:60 },
  { id:"lunar_flare40_max", label:"Lunar Scorer", desc:"Reach max with LUNAR_FLARE40 active", icon:"🌙", xp:120 },
  { id:"rhodochrosite_fox9e_tap", label:"Rhodochrosite Fox", desc:"Tap a Rhodochrosite Fox target", icon:"🦊", xp:60 },
  { id:"rhodochrosite_fox9e_peak", label:"Rhodochrosite Fox Peak", desc:"Reach peak with Rhodochrosite Fox", icon:"🦊", xp:120 },
  { id:"rutile_orb9e_tap", label:"Rutile Orb", desc:"Tap a Rutile Orb target", icon:"🔮", xp:60 },
  { id:"rutile_orb9e_peak", label:"Rutile Orb Peak", desc:"Reach peak with Rutile Orb", icon:"🔮", xp:120 },
  { id:"pyrargyrite_orb9e_peak", label:"Pyrargyrite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"ECLIPSE_FLARE40","COSMIC_FLARE40","VOID_FLARE40"'
A2_NEW = '"STELLAR_FLARE40","LUNAR_FLARE40","ECLIPSE_FLARE40","COSMIC_FLARE40","VOID_FLARE40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="ECLIPSE_FLARE40"){'
A3_NEW = '''} else if(ptype==="STELLAR_FLARE40"){
        activePwrRef.current.push({type:"STELLAR_FLARE40",left:12000});
        sfx("comboNote",1627);
        unlock("stellar_flare40_use");
      } else if(ptype==="LUNAR_FLARE40"){
        activePwrRef.current.push({type:"LUNAR_FLARE40",left:12000});
        sfx("comboNote",1629);
        unlock("lunar_flare40_use");
      } else if(ptype==="ECLIPSE_FLARE40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // ECLIPSE_FLARE40 — +1960 eclipse bonus'
A4_NEW = '''  // STELLAR_FLARE40 — +1964 stellar bonus
  if(activePwrRef.current.some(p=>p.type==="STELLAR_FLARE40")){
    const bonusTotal=Math.round(93.6*1000);
    gs.score+=1964;showPopup(cx,cy-1674,"+1964 ⭐✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a038a",1836);
    if(gs.score>=bonusTotal)unlock("stellar_flare40_max");
  }
  // LUNAR_FLARE40 — +1966 lunar bonus
  if(activePwrRef.current.some(p=>p.type==="LUNAR_FLARE40")){
    const bonusTotal=Math.round(93.7*1000);
    gs.score+=1966;showPopup(cx,cy-1676,"+1966 🌙✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a085e",1838);
    if(gs.score>=bonusTotal)unlock("lunar_flare40_max");
  }
  // ECLIPSE_FLARE40 — +1960 eclipse bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawPyromorphiteFox9e('
A5_NEW = '''function drawRhodochrositeFox9e(ctx,r,ts,rhocPct){
  const bob=Math.sin(ts*0.3338)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fdf2f8");g.addColorStop(0.45+rhocPct*0.35,"#be185d");g.addColorStop(1,"#831843");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(rhocPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(190,24,93,"+(rhocPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=rhocPct>0.88?"#f9a8d4":"#fdf2f8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rhocPct>0.88?"🌸":"🦊",0,1);
  ctx.restore();
}
function drawRutileOrb9e(ctx,r,ts,rutPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3342);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+rutPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fffbeb");g.addColorStop(0.35+rutPct*0.35,"#d97706");g.addColorStop(1,"#78350f");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+rutPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(217,119,6,"+(0.45+rutPct*0.55)+")";ctx.lineWidth=3.5+rutPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(rutPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(245,158,11,"+(rutPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=rutPct>0.88?"#fcd34d":"#fffbeb";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(rutPct>0.88?"🟡":"🔮",0,1);
  ctx.restore();
}
function drawPyromorphiteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="pyromorphite_fox9e"){'
A6_NEW = '''  else if(t.type==="rhodochrosite_fox9e"){
    const rhocPct625=(Math.sin((Date.now()-t.spawnedAt)*0.3338)+1)/2;
    t._rhocPct625=rhocPct625;
    drawRhodochrositeFox9e(ctx,t.radius,ts,rhocPct625);
  }
  else if(t.type==="rutile_orb9e"){
    const rutPct625=(Math.sin((Date.now()-t.spawnedAt)*0.3342)+1)/2;
    t._rutPct625=rutPct625;
    drawRutileOrb9e(ctx,t.radius,ts,rutPct625);
  }
  else if(t.type==="pyromorphite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="pyromorphite_fox9e"){'
A7_NEW = '''    if(hit.type==="rhodochrosite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo625rhoc=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult625rhoc=gs.feverActive?2:1;
      const isPeak625rhoc=((hit._rhocPct625||0)>0.88);
      const pts625rhoc=Math.round((isPeak625rhoc?566:376)*combo625rhoc*feverMult625rhoc);
      gs.score+=pts625rhoc;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1810,"#be185d");
      if(isPeak625rhoc){spawnPopup(hit.x,hit.y-28,"🌸 +"+pts625rhoc,theme.accent);unlock("rhodochrosite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts625rhoc,theme.accent);}
      unlock("rhodochrosite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="rutile_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo625rut=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult625rut=gs.feverActive?2:1;
      const isPeak625rut=((hit._rutPct625||0)>0.88);
      const pts625rut=Math.round((isPeak625rut?554:368)*combo625rut*feverMult625rut);
      gs.score+=pts625rut;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1812,"#d97706");
      if(isPeak625rut){spawnPopup(hit.x,hit.y-28,"🟡 +"+pts625rut,theme.accent);unlock("rutile_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts625rut,theme.accent);}
      unlock("rutile_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="pyromorphite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="pyromorphite_fox9e";color="#84cc16";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="pyrargyrite_orb9e"')
A8_NEW = ('      type="rhodochrosite_fox9e";color="#be185d";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="rutile_orb9e";color="#d97706";glow="#fffbeb";\n'
          '    } else if('+COND100F+'){\n'
          '      type="pyromorphite_fox9e";color="#84cc16";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="pyrargyrite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="pyromorphite_fox9e"?BASE_R*1.09:type==="pyrargyrite_orb9e"?BASE_R*1.08:'
A9_NEW = 'type==="rhodochrosite_fox9e"?BASE_R*1.10:type==="rutile_orb9e"?BASE_R*1.09:type==="pyromorphite_fox9e"?BASE_R*1.09:type==="pyrargyrite_orb9e"?BASE_R*1.08:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'ECLIPSE_FLARE40:"🌒✨",COSMIC_FLARE40:"🌌✨",VOID_FLARE40:"🌑✨"'
A10_NEW = 'STELLAR_FLARE40:"⭐✨",LUNAR_FLARE40:"🌙✨",ECLIPSE_FLARE40:"🌒✨",COSMIC_FLARE40:"🌌✨",VOID_FLARE40:"🌑✨"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 625 done! +{len(content)-original_size} bytes")
