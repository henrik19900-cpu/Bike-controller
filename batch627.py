#!/usr/bin/env python3
# Batch 627: AURORA_RAY40 + THUNDER_RAY40 + sillimanite_fox9e + spessartine_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"staurolite_orb9e_peak", label:"Staurolite Orb Peak",'
A1_NEW = '''{ id:"aurora_ray40_use", label:"Aurora Ray", desc:"Activate AURORA_RAY40 power-up", icon:"🌠", xp:60 },
  { id:"aurora_ray40_max", label:"Aurora Rayer", desc:"Reach max with AURORA_RAY40 active", icon:"🌠", xp:120 },
  { id:"thunder_ray40_use", label:"Thunder Ray", desc:"Activate THUNDER_RAY40 power-up", icon:"⚡", xp:60 },
  { id:"thunder_ray40_max", label:"Thunder Rayer", desc:"Reach max with THUNDER_RAY40 active", icon:"⚡", xp:120 },
  { id:"sillimanite_fox9e_tap", label:"Sillimanite Fox", desc:"Tap a Sillimanite Fox target", icon:"🦊", xp:60 },
  { id:"sillimanite_fox9e_peak", label:"Sillimanite Fox Peak", desc:"Reach peak with Sillimanite Fox", icon:"🦊", xp:120 },
  { id:"spessartine_orb9e_tap", label:"Spessartine Orb", desc:"Tap a Spessartine Orb target", icon:"🔮", xp:60 },
  { id:"spessartine_orb9e_peak", label:"Spessartine Orb Peak", desc:"Reach peak with Spessartine Orb", icon:"🔮", xp:120 },
  { id:"staurolite_orb9e_peak", label:"Staurolite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"NOVA_FLARE40","VOID_GLOW40","STELLAR_FLARE40"'
A2_NEW = '"AURORA_RAY40","THUNDER_RAY40","NOVA_FLARE40","VOID_GLOW40","STELLAR_FLARE40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="NOVA_FLARE40"){'
A3_NEW = '''} else if(ptype==="AURORA_RAY40"){
        activePwrRef.current.push({type:"AURORA_RAY40",left:12000});
        sfx("comboNote",1635);
        unlock("aurora_ray40_use");
      } else if(ptype==="THUNDER_RAY40"){
        activePwrRef.current.push({type:"THUNDER_RAY40",left:12000});
        sfx("comboNote",1637);
        unlock("thunder_ray40_use");
      } else if(ptype==="NOVA_FLARE40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // NOVA_FLARE40 — +1968 nova bonus'
A4_NEW = '''  // AURORA_RAY40 — +1972 aurora bonus
  if(activePwrRef.current.some(p=>p.type==="AURORA_RAY40")){
    const bonusTotal=Math.round(94.0*1000);
    gs.score+=1972;showPopup(cx,cy-1682,"+1972 🌠⚡",theme.accent,26);
    spawnShockwave(cx,cy,"#0a038e",1844);
    if(gs.score>=bonusTotal)unlock("aurora_ray40_max");
  }
  // THUNDER_RAY40 — +1974 thunder bonus
  if(activePwrRef.current.some(p=>p.type==="THUNDER_RAY40")){
    const bonusTotal=Math.round(94.1*1000);
    gs.score+=1974;showPopup(cx,cy-1684,"+1974 ⚡🌠",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0862",1846);
    if(gs.score>=bonusTotal)unlock("thunder_ray40_max");
  }
  // NOVA_FLARE40 — +1968 nova bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawSphaloriteFox9e('
A5_NEW = '''function drawSillimaniteFox9e(ctx,r,ts,sillPct){
  const bob=Math.sin(ts*0.3354)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f0f9ff");g.addColorStop(0.45+sillPct*0.35,"#0369a1");g.addColorStop(1,"#0c4a6e");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(sillPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(3,105,161,"+(sillPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=sillPct>0.88?"#38bdf8":"#f0f9ff";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sillPct>0.88?"💎":"🦊",0,1);
  ctx.restore();
}
function drawSpessartineOrb9e(ctx,r,ts,spessPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3358);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+spessPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+spessPct*0.35,"#ea580c");g.addColorStop(1,"#7c2d12");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+spessPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(234,88,12,"+(0.45+spessPct*0.55)+")";ctx.lineWidth=3.5+spessPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(spessPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(249,115,22,"+(spessPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=spessPct>0.88?"#fdba74":"#fff7ed";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(spessPct>0.88?"🔶":"🔮",0,1);
  ctx.restore();
}
function drawSphaloriteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="sphalerite_fox9e"){'
A6_NEW = '''  else if(t.type==="sillimanite_fox9e"){
    const sillPct627=(Math.sin((Date.now()-t.spawnedAt)*0.3354)+1)/2;
    t._sillPct627=sillPct627;
    drawSillimaniteFox9e(ctx,t.radius,ts,sillPct627);
  }
  else if(t.type==="spessartine_orb9e"){
    const spessPct627=(Math.sin((Date.now()-t.spawnedAt)*0.3358)+1)/2;
    t._spessPct627=spessPct627;
    drawSpessartineOrb9e(ctx,t.radius,ts,spessPct627);
  }
  else if(t.type==="sphalerite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="sphalerite_fox9e"){'
A7_NEW = '''    if(hit.type==="sillimanite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo627sill=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult627sill=gs.feverActive?2:1;
      const isPeak627sill=((hit._sillPct627||0)>0.88);
      const pts627sill=Math.round((isPeak627sill?570:380)*combo627sill*feverMult627sill);
      gs.score+=pts627sill;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1818,"#0369a1");
      if(isPeak627sill){spawnPopup(hit.x,hit.y-28,"💎 +"+pts627sill,theme.accent);unlock("sillimanite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts627sill,theme.accent);}
      unlock("sillimanite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="spessartine_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo627spess=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult627spess=gs.feverActive?2:1;
      const isPeak627spess=((hit._spessPct627||0)>0.88);
      const pts627spess=Math.round((isPeak627spess?558:372)*combo627spess*feverMult627spess);
      gs.score+=pts627spess;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1820,"#ea580c");
      if(isPeak627spess){spawnPopup(hit.x,hit.y-28,"🔶 +"+pts627spess,theme.accent);unlock("spessartine_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts627spess,theme.accent);}
      unlock("spessartine_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="sphalerite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="sphalerite_fox9e";color="#ca8a04";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="staurolite_orb9e"')
A8_NEW = ('      type="sillimanite_fox9e";color="#0369a1";glow="#f0f9ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="spessartine_orb9e";color="#ea580c";glow="#fff7ed";\n'
          '    } else if('+COND100F+'){\n'
          '      type="sphalerite_fox9e";color="#ca8a04";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="staurolite_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="sphalerite_fox9e"?BASE_R*1.11:type==="staurolite_orb9e"?BASE_R*1.10:'
A9_NEW = 'type==="sillimanite_fox9e"?BASE_R*1.12:type==="spessartine_orb9e"?BASE_R*1.11:type==="sphalerite_fox9e"?BASE_R*1.11:type==="staurolite_orb9e"?BASE_R*1.10:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'NOVA_FLARE40:"💥✨",VOID_GLOW40:"⚫✨",STELLAR_FLARE40:"⭐✨"'
A10_NEW = 'AURORA_RAY40:"🌠⚡",THUNDER_RAY40:"⚡🌠",NOVA_FLARE40:"💥✨",VOID_GLOW40:"⚫✨",STELLAR_FLARE40:"⭐✨"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 627 done! +{len(content)-original_size} bytes")
