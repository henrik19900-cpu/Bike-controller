#!/usr/bin/env python3
# Batch 626: NOVA_FLARE40 + VOID_GLOW40 + sphalerite_fox9e + staurolite_orb9e + 8 achievements

COND100F = '(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")'

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"rutile_orb9e_peak", label:"Rutile Orb Peak",'
A1_NEW = '''{ id:"nova_flare40_use", label:"Nova Flare", desc:"Activate NOVA_FLARE40 power-up", icon:"💥", xp:60 },
  { id:"nova_flare40_max", label:"Nova Surger", desc:"Reach max with NOVA_FLARE40 active", icon:"💥", xp:120 },
  { id:"void_glow40_use", label:"Void Glow", desc:"Activate VOID_GLOW40 power-up", icon:"⚫", xp:60 },
  { id:"void_glow40_max", label:"Void Glower", desc:"Reach max with VOID_GLOW40 active", icon:"⚫", xp:120 },
  { id:"sphalerite_fox9e_tap", label:"Sphalerite Fox", desc:"Tap a Sphalerite Fox target", icon:"🦊", xp:60 },
  { id:"sphalerite_fox9e_peak", label:"Sphalerite Fox Peak", desc:"Reach peak with Sphalerite Fox", icon:"🦊", xp:120 },
  { id:"staurolite_orb9e_tap", label:"Staurolite Orb", desc:"Tap a Staurolite Orb target", icon:"🔮", xp:60 },
  { id:"staurolite_orb9e_peak", label:"Staurolite Orb Peak", desc:"Reach peak with Staurolite Orb", icon:"🔮", xp:120 },
  { id:"rutile_orb9e_peak", label:"Rutile Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"STELLAR_FLARE40","LUNAR_FLARE40","ECLIPSE_FLARE40"'
A2_NEW = '"NOVA_FLARE40","VOID_GLOW40","STELLAR_FLARE40","LUNAR_FLARE40","ECLIPSE_FLARE40"'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="STELLAR_FLARE40"){'
A3_NEW = '''} else if(ptype==="NOVA_FLARE40"){
        activePwrRef.current.push({type:"NOVA_FLARE40",left:12000});
        sfx("comboNote",1631);
        unlock("nova_flare40_use");
      } else if(ptype==="VOID_GLOW40"){
        activePwrRef.current.push({type:"VOID_GLOW40",left:12000});
        sfx("comboNote",1633);
        unlock("void_glow40_use");
      } else if(ptype==="STELLAR_FLARE40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '  // STELLAR_FLARE40 — +1964 stellar bonus'
A4_NEW = '''  // NOVA_FLARE40 — +1968 nova bonus
  if(activePwrRef.current.some(p=>p.type==="NOVA_FLARE40")){
    const bonusTotal=Math.round(93.8*1000);
    gs.score+=1968;showPopup(cx,cy-1678,"+1968 💥✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a038c",1840);
    if(gs.score>=bonusTotal)unlock("nova_flare40_max");
  }
  // VOID_GLOW40 — +1970 void bonus
  if(activePwrRef.current.some(p=>p.type==="VOID_GLOW40")){
    const bonusTotal=Math.round(93.9*1000);
    gs.score+=1970;showPopup(cx,cy-1680,"+1970 ⚫✨",theme.accent,26);
    spawnShockwave(cx,cy,"#0a0860",1842);
    if(gs.score>=bonusTotal)unlock("void_glow40_max");
  }
  // STELLAR_FLARE40 — +1964 stellar bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawRhodochrositeFox9e('
A5_NEW = '''function drawSphaloriteFox9e(ctx,r,ts,sphalPct){
  const bob=Math.sin(ts*0.3346)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fefce8");g.addColorStop(0.45+sphalPct*0.35,"#ca8a04");g.addColorStop(1,"#713f12");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(sphalPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(202,138,4,"+(sphalPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=sphalPct>0.88?"#fde047":"#fefce8";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sphalPct>0.88?"⚡":"🦊",0,1);
  ctx.restore();
}
function drawStauroliteOrb9e(ctx,r,ts,staurPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3350);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+staurPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fef3c7");g.addColorStop(0.35+staurPct*0.35,"#92400e");g.addColorStop(1,"#451a03");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+staurPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(146,64,14,"+(0.45+staurPct*0.55)+")";ctx.lineWidth=3.5+staurPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(staurPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(180,83,9,"+(staurPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=staurPct>0.88?"#fbbf24":"#fef3c7";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(staurPct>0.88?"✖️":"🔮",0,1);
  ctx.restore();
}
function drawRhodochrositeFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = '  else if(t.type==="rhodochrosite_fox9e"){'
A6_NEW = '''  else if(t.type==="sphalerite_fox9e"){
    const sphalPct626=(Math.sin((Date.now()-t.spawnedAt)*0.3346)+1)/2;
    t._sphalPct626=sphalPct626;
    drawSphaloriteFox9e(ctx,t.radius,ts,sphalPct626);
  }
  else if(t.type==="staurolite_orb9e"){
    const staurPct626=(Math.sin((Date.now()-t.spawnedAt)*0.3350)+1)/2;
    t._staurPct626=staurPct626;
    drawStauroliteOrb9e(ctx,t.radius,ts,staurPct626);
  }
  else if(t.type==="rhodochrosite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = '    if(hit.type==="rhodochrosite_fox9e"){'
A7_NEW = '''    if(hit.type==="sphalerite_fox9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo626sphal=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult626sphal=gs.feverActive?2:1;
      const isPeak626sphal=((hit._sphalPct626||0)>0.88);
      const pts626sphal=Math.round((isPeak626sphal?568:378)*combo626sphal*feverMult626sphal);
      gs.score+=pts626sphal;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1814,"#ca8a04");
      if(isPeak626sphal){spawnPopup(hit.x,hit.y-28,"⚡ +"+pts626sphal,theme.accent);unlock("sphalerite_fox9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🦊 +"+pts626sphal,theme.accent);}
      unlock("sphalerite_fox9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="staurolite_orb9e"){
      targetsRef.current=targetsRef.current.filter(t=>t.id!==hit.id);
      const combo626staur=Math.min(10,1+Math.floor(gs.streak/5));
      const feverMult626staur=gs.feverActive?2:1;
      const isPeak626staur=((hit._staurPct626||0)>0.88);
      const pts626staur=Math.round((isPeak626staur?556:370)*combo626staur*feverMult626staur);
      gs.score+=pts626staur;gs.streak++;gs.lastTapTime=Date.now();
      spawnShockwave(hit.x,hit.y,1816,"#92400e");
      if(isPeak626staur){spawnPopup(hit.x,hit.y-28,"✖️ +"+pts626staur,theme.accent);unlock("staurolite_orb9e_peak");}
      else{spawnPopup(hit.x,hit.y-26,"🔮 +"+pts626staur,theme.accent);}
      unlock("staurolite_orb9e_tap");
      updateMissions({...gs.sessionStats,tapsTotal:(gs.sessionStats.tapsTotal||0)+1});
      debounceSave();return;
    }
    if(hit.type==="rhodochrosite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = ('      type="rhodochrosite_fox9e";color="#be185d";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="rutile_orb9e"')
A8_NEW = ('      type="sphalerite_fox9e";color="#ca8a04";glow="#fefce8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="staurolite_orb9e";color="#92400e";glow="#fef3c7";\n'
          '    } else if('+COND100F+'){\n'
          '      type="rhodochrosite_fox9e";color="#be185d";glow="#fdf2f8";\n'
          '    } else if('+COND100F+'){\n'
          '      type="rutile_orb9e"')
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="rhodochrosite_fox9e"?BASE_R*1.10:type==="rutile_orb9e"?BASE_R*1.09:'
A9_NEW = 'type==="sphalerite_fox9e"?BASE_R*1.11:type==="staurolite_orb9e"?BASE_R*1.10:type==="rhodochrosite_fox9e"?BASE_R*1.10:type==="rutile_orb9e"?BASE_R*1.09:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'STELLAR_FLARE40:"⭐✨",LUNAR_FLARE40:"🌙✨",ECLIPSE_FLARE40:"🌒✨"'
A10_NEW = 'NOVA_FLARE40:"💥✨",VOID_GLOW40:"⚫✨",STELLAR_FLARE40:"⭐✨",LUNAR_FLARE40:"🌙✨",ECLIPSE_FLARE40:"🌒✨"'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 626 done! +{len(content)-original_size} bytes")
