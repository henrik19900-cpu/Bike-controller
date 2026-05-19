#!/usr/bin/env python3
# Batch 622: NEXUS_FLARE40 + SOLAR_FLARE40 + olivine_fox9e + orthoclase_orb9e + 8 achievements

with open("src/NexusTap.jsx","r") as f:
    content = f.read()

original_size = len(content)

# ── STEP 1 — 8 new achievements ───────────────────────────────────────────────
A1_OLD = '{ id:"nontronite_orb9e_peak", label:"Nontronite Orb Peak",'
A1_NEW = '''{ id:"nexus_flare40_use", label:"Nexus Flare", desc:"Activate NEXUS_FLARE40 power-up", icon:"🌠", xp:60 },
  { id:"nexus_flare40_max", label:"Nexus Surger", desc:"Reach max with NEXUS_FLARE40 active", icon:"🌠", xp:120 },
  { id:"solar_flare40_use", label:"Solar Flare", desc:"Activate SOLAR_FLARE40 power-up", icon:"☀️", xp:60 },
  { id:"solar_flare40_max", label:"Solar Scorer", desc:"Reach max with SOLAR_FLARE40 active", icon:"☀️", xp:120 },
  { id:"olivine_fox9e_tap", label:"Olivine Fox", desc:"Tap an Olivine Fox target", icon:"🫛", xp:60 },
  { id:"olivine_fox9e_peak", label:"Olivine Fox Peak", desc:"Reach 3000 pts with Olivine Fox", icon:"🫛", xp:120 },
  { id:"orthoclase_orb9e_tap", label:"Orthoclase Orb", desc:"Tap an Orthoclase Orb target", icon:"🟠", xp:60 },
  { id:"orthoclase_orb9e_peak", label:"Orthoclase Orb Peak", desc:"Reach 3000 pts with Orthoclase Orb", icon:"🟠", xp:120 },
  { id:"nontronite_orb9e_peak", label:"Nontronite Orb Peak",'''
assert content.count(A1_OLD) == 1, f"Step 1 anchor count: {content.count(A1_OLD)}"
content = content.replace(A1_OLD, A1_NEW, 1)
print("Step 1 OK")

# ── STEP 2 — add power-up type strings ────────────────────────────────────────
A2_OLD = '"AURORA_GLOW40","THUNDER_GLOW40",'
A2_NEW = '"NEXUS_FLARE40","SOLAR_FLARE40","AURORA_GLOW40","THUNDER_GLOW40",'
assert content.count(A2_OLD) == 1, f"Step 2 anchor count: {content.count(A2_OLD)}"
content = content.replace(A2_OLD, A2_NEW, 1)
print("Step 2 OK")

# ── STEP 3 — power-up activation branches ─────────────────────────────────────
A3_OLD = '} else if(ptype==="AURORA_GLOW40"){'
A3_NEW = '''} else if(ptype==="NEXUS_FLARE40"){
        activePwrRef.current.push({type:"NEXUS_FLARE40",left:12000});
        sfx("comboNote",1615);
        unlock("nexus_flare40_use");
      } else if(ptype==="SOLAR_FLARE40"){
        activePwrRef.current.push({type:"SOLAR_FLARE40",left:12000});
        sfx("comboNote",1617);
        unlock("solar_flare40_use");
      } else if(ptype==="AURORA_GLOW40"){'''
assert content.count(A3_OLD) == 1, f"Step 3 anchor count: {content.count(A3_OLD)}"
content = content.replace(A3_OLD, A3_NEW, 1)
print("Step 3 OK")

# ── STEP 4 — power-up score bonus cases ───────────────────────────────────────
A4_OLD = '// AURORA_GLOW40 — +1948 aurora bonus'
A4_NEW = '''// NEXUS_FLARE40 — +1952 nexus bonus
      if(activePwrRef.current.some(p=>p.type==="NEXUS_FLARE40")){
        pts+=1952;addParticle("popup",hx,hy-226,"+1952 NEXUS",{col:"#0a0384"});
        if(gs.score>=3000) unlock("nexus_flare40_max");
        addShockwave(hx,hy,1824);}
      // SOLAR_FLARE40 — +1954 solar bonus
      if(activePwrRef.current.some(p=>p.type==="SOLAR_FLARE40")){
        pts+=1954;addParticle("popup",hx,hy-228,"+1954 SOLAR",{col:"#0a0858"});
        if(gs.score>=3000) unlock("solar_flare40_max");
        addShockwave(hx,hy,1826);}
      // AURORA_GLOW40 — +1948 aurora bonus'''
assert content.count(A4_OLD) == 1, f"Step 4 anchor count: {content.count(A4_OLD)}"
content = content.replace(A4_OLD, A4_NEW, 1)
print("Step 4 OK")

# ── STEP 5 — draw functions ────────────────────────────────────────────────────
A5_OLD = 'function drawNephriteFox9e('
A5_NEW = '''function drawOlivineFox9e(ctx,r,ts,olivPct){
  const bob=Math.sin(ts*0.3314)*r*0.07;
  ctx.save();ctx.translate(0,bob);
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#f0fdf4");g.addColorStop(0.45+olivPct*0.35,"#4ade80");g.addColorStop(1,"#166534");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  if(olivPct>0.65){
    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);
    ctx.strokeStyle="rgba(74,222,128,"+(olivPct-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}
  ctx.fillStyle=olivPct>0.88?"#86efac":"#f0fdf4";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(olivPct>0.88?"🫛":"🦊",0,1);
  ctx.restore();
}
function drawOrthoclaseOrb9e(ctx,r,ts,orthPct){
  const pulse=0.72+0.28*Math.sin(ts*0.3318);
  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+orthPct*0.27;
  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);
  g.addColorStop(0,"#fff7ed");g.addColorStop(0.35+orthPct*0.35,"#fb923c");g.addColorStop(1,"#7c2d12");
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();
  const ring=r*(0.54+orthPct*0.42);
  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);
  ctx.strokeStyle="rgba(251,146,60,"+(0.45+orthPct*0.55)+")";ctx.lineWidth=3.5+orthPct*3;ctx.stroke();
  ctx.globalAlpha=1;
  if(orthPct>0.82){
    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);
    ctx.strokeStyle="rgba(249,115,22,"+(orthPct-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}
  ctx.fillStyle=orthPct>0.88?"#fed7aa":"#fff7ed";ctx.font=(r*0.56)+"px serif";
  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(orthPct>0.88?"🟠":"🔮",0,1);
  ctx.restore();
}
function drawNephriteFox9e('''
assert content.count(A5_OLD) == 1, f"Step 5 anchor count: {content.count(A5_OLD)}"
content = content.replace(A5_OLD, A5_NEW, 1)
print("Step 5 OK")

# ── STEP 6 — drawTarget dispatch ──────────────────────────────────────────────
A6_OLD = 'else if(t.type==="nephrite_fox9e"){'
A6_NEW = '''else if(t.type==="olivine_fox9e"){
      const olivPct=Math.min(1,(now-t.born)/t.lifetime);
      drawOlivineFox9e(ctx,t.radius,ts,olivPct);
    } else if(t.type==="orthoclase_orb9e"){
      const orthPct=Math.min(1,(now-t.born)/t.lifetime);
      drawOrthoclaseOrb9e(ctx,t.radius,ts,orthPct);
    } else if(t.type==="nephrite_fox9e"){'''
assert content.count(A6_OLD) == 1, f"Step 6 anchor count: {content.count(A6_OLD)}"
content = content.replace(A6_OLD, A6_NEW, 1)
print("Step 6 OK")

# ── STEP 7 — handleTap score logic ────────────────────────────────────────────
A7_OLD = 'if(hit.type==="nephrite_fox9e"){'
A7_NEW = '''if(hit.type==="olivine_fox9e"){
          const olivPct=Math.min(1,(Date.now()-hit.spawnedAt)/hit.lifetime);
          const bfOliv622=Math.floor(180+olivPct*620);
          pts+=bfOliv622;addParticle("popup",hx,hy-230,"+"+bfOliv622+" OLIVINE",{col:"#4ade80"});
          addShockwave(hx,hy,1798);
          unlock("olivine_fox9e_tap");
          if(pts>=3000) unlock("olivine_fox9e_peak");
        } else if(hit.type==="orthoclase_orb9e"){
          const orthPct=Math.min(1,(Date.now()-hit.spawnedAt)/hit.lifetime);
          const aoOrth622=Math.floor(170+orthPct*600);
          pts+=aoOrth622;addParticle("popup",hx,hy-232,"+"+aoOrth622+" ORTHOCLASE",{col:"#fb923c"});
          addShockwave(hx,hy,1800);
          unlock("orthoclase_orb9e_tap");
          if(pts>=3000) unlock("orthoclase_orb9e_peak");
        } else if(hit.type==="nephrite_fox9e"){'''
assert content.count(A7_OLD) == 1, f"Step 7 anchor count: {content.count(A7_OLD)}"
content = content.replace(A7_OLD, A7_NEW, 1)
print("Step 7 OK")

# ── STEP 8 — spawnTarget type assignment ──────────────────────────────────────
A8_OLD = '      type="nephrite_fox9e";color="#064e3b";glow="#ecfdf5";\n    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n      type="nontronite_orb9e"'
A8_NEW = '      type="olivine_fox9e";color="#4ade80";glow="#f0fdf4";\n    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){\n      type="orthoclase_orb9e";color="#fb923c";glow="#fff7ed";\n    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")&&!modifier?.type?.includes("final")){\n      type="nephrite_fox9e";color="#064e3b";glow="#ecfdf5";\n    } else if((cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")){\n      type="nontronite_orb9e"'
assert content.count(A8_OLD) == 1, f"Step 8 anchor count: {content.count(A8_OLD)}"
content = content.replace(A8_OLD, A8_NEW, 1)
print("Step 8 OK")

# ── STEP 9 — radius table ─────────────────────────────────────────────────────
A9_OLD = 'type==="nephrite_fox9e"?BASE_R*1.06:type==="nontronite_orb9e"?BASE_R*1.05:'
A9_NEW = 'type==="olivine_fox9e"?BASE_R*1.07:type==="orthoclase_orb9e"?BASE_R*1.06:type==="nephrite_fox9e"?BASE_R*1.06:type==="nontronite_orb9e"?BASE_R*1.05:'
assert content.count(A9_OLD) == 1, f"Step 9 anchor count: {content.count(A9_OLD)}"
content = content.replace(A9_OLD, A9_NEW, 1)
print("Step 9 OK")

# ── STEP 10 — icon map (appears twice, replace_all) ───────────────────────────
A10_OLD = 'AURORA_GLOW40:"🌌🌟",THUNDER_GLOW40:"⚡🌟",'
A10_NEW = 'NEXUS_FLARE40:"🌠✨",SOLAR_FLARE40:"☀️✨",AURORA_GLOW40:"🌌🌟",THUNDER_GLOW40:"⚡🌟",'
cnt = content.count(A10_OLD)
assert cnt == 2, f"Step 10 anchor count: {cnt}"
content = content.replace(A10_OLD, A10_NEW)
print("Step 10 OK")

with open("src/NexusTap.jsx","w") as f:
    f.write(content)

print(f"Batch 622 done! +{len(content)-original_size} bytes")
