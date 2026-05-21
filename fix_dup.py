# Fix: rename the NEW freieslebenite_fox9e (from batch1090, rose/pink) to freybergite_fox9e

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()
original_len = len(src)

# 1. Fix achievement entries (the new ones with 🌹 icon, near top of achievements list)
OLD1 = '''  { id:"freieslebenite_fox9e_tap",          label:"Freieslebenite Fox Tap",      desc:"Tap Freieslebenite Fox target",         icon:"🌹", xp:62 },
  { id:"freieslebenite_fox9e_peak",         label:"Freieslebenite Fox Peak",     desc:"Reach peak with Freieslebenite Fox",    icon:"🌹", xp:124 },'''
NEW1 = '''  { id:"freybergite_fox9e_tap",             label:"Freybergite Fox Tap",         desc:"Tap Freybergite Fox target",            icon:"🌹", xp:62 },
  { id:"freybergite_fox9e_peak",            label:"Freybergite Fox Peak",        desc:"Reach peak with Freybergite Fox",       icon:"🌹", xp:124 },'''
assert src.count(OLD1) == 1, f"Step1: {src.count(OLD1)}"
src = src.replace(OLD1, NEW1, 1); print("OK Step1")

# 2. Fix the function declaration (the pink/rose one with #fb7185)
OLD2 = '''function drawFreieslebeniteFox9e(ctx,r,ts,sp){
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="#fb7185";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#fb7185");g.addColorStop(0.5,"#1e0010");g.addColorStop(1,"#500724");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="#fb7185";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${Math.round(r*0.5609*10)/10}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("🌹",0,0);ctx.restore();
}'''
NEW2 = '''function drawFreybergiteFox9e(ctx,r,ts,sp){
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="#fb7185";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#fb7185");g.addColorStop(0.5,"#1e0010");g.addColorStop(1,"#500724");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="#fb7185";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${Math.round(r*0.5609*10)/10}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("🌹",0,0);ctx.restore();
}'''
assert src.count(OLD2) == 1, f"Step2: {src.count(OLD2)}"
src = src.replace(OLD2, NEW2, 1); print("OK Step2")

# 3. Fix dispatch - the new one (comes before freboldite_fox9e dispatch)
OLD3 = '  else if(t.type==="freieslebenite_fox9e"){drawFreieslebeniteFox9e(ctx,t.radius,ts-t.born,t.lifetime);}\n  else if(t.type==="friedrichite_orb9e")'
NEW3 = '  else if(t.type==="freybergite_fox9e"){drawFreybergiteFox9e(ctx,t.radius,ts-t.born,t.lifetime);}\n  else if(t.type==="friedrichite_orb9e")'
assert src.count(OLD3) == 1, f"Step3: {src.count(OLD3)}"
src = src.replace(OLD3, NEW3, 1); print("OK Step3")

# 4. Fix spawn (the new one with #1e0010 color, before friedrichite)
OLD4 = '      type="freieslebenite_fox9e";color="#1e0010";glow="#fb7185";\n        }else if(COND100F){\n          type="friedrichite_orb9e"'
NEW4 = '      type="freybergite_fox9e";color="#1e0010";glow="#fb7185";\n        }else if(COND100F){\n          type="friedrichite_orb9e"'
assert src.count(OLD4) == 1, f"Step4: {src.count(OLD4)}"
src = src.replace(OLD4, NEW4, 1); print("OK Step4")

# 5. Fix radius chain (the new one, before friedrichite_orb9e radius)
OLD5 = 'type==="freieslebenite_fox9e"?BASE_R*5.35:type==="friedrichite_orb9e"'
NEW5 = 'type==="freybergite_fox9e"?BASE_R*5.35:type==="friedrichite_orb9e"'
assert src.count(OLD5) == 1, f"Step5: {src.count(OLD5)}"
src = src.replace(OLD5, NEW5, 1); print("OK Step5")

# 6. Fix tap handler (the new one with pts=1164 and score 58200, before friedrichite)
OLD6 = '''    if(hit.type==="freieslebenite_fox9e"){
      const pts=1164+gs.streak*2974;gs.score+=pts;spawnParticles(hit.x,hit.y,"#fb7185",14);
      showPop(hit.x,hit.y,"+"+pts,"#fb7185");gs.sessionStats.score+=pts;
      unlock("freieslebenite_fox9e_tap");if(gs.score>=58200)unlock("freieslebenite_fox9e_peak");
    }else if(hit.type==="friedrichite_orb9e")'''
NEW6 = '''    if(hit.type==="freybergite_fox9e"){
      const pts=1164+gs.streak*2974;gs.score+=pts;spawnParticles(hit.x,hit.y,"#fb7185",14);
      showPop(hit.x,hit.y,"+"+pts,"#fb7185");gs.sessionStats.score+=pts;
      unlock("freybergite_fox9e_tap");if(gs.score>=58200)unlock("freybergite_fox9e_peak");
    }else if(hit.type==="friedrichite_orb9e")'''
assert src.count(OLD6) == 1, f"Step6: {src.count(OLD6)}"
src = src.replace(OLD6, NEW6, 1); print("OK Step6")

# Verify no more duplicates
cnt_fox = src.count('drawFreieslebeniteFox9e')
cnt_type = src.count('"freieslebenite_fox9e"')
print(f"Remaining drawFreieslebeniteFox9e: {cnt_fox}")
print(f"Remaining freieslebenite_fox9e type refs: {cnt_type}")
cnt_new = src.count('drawFreybergiteFox9e')
print(f"New drawFreybergiteFox9e: {cnt_new}")

with open(SRC, "w") as f: f.write(src)
print(f"Fix done! delta={len(src)-original_len}")
