import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()
original_len = len(src)

# ── Batch 819 constants ───────────────────────────────────────────────────────
FOX      = "wurtzite"
ORB      = "zirconolite"
FOX_TYPE = f"{FOX}_fox9e"
ORB_TYPE = f"{ORB}_orb9e"
FOX_COLOR = "#fef08a"; FOX_GLOW = "#fefce8"; FOX_PEAK = "⭐"
ORB_COLOR = "#44403c"; ORB_GLOW = "#fafaf9"; ORB_PEAK = "🪨"
FOX_SC   = 622;  ORB_SC  = 617
FOX_R    = "BASE_R*2.64"; ORB_R = "BASE_R*2.63"
OSC      = 0.4525; SW = 2432
PW1 = "DAWN2_GLOW44"; PW1_SC = 2740; PW1_SHOCK = "#f97316"; PW1_ICON = "🌅💫"
PW2 = "TIDE2_GLOW44"; PW2_SC = 2742; PW2_SHOCK = "#0891b2"; PW2_ICON = "🌊✨"

# Prev-batch anchors (batch 818)
PREV_FOX_FULL = "wardite_fox9e"
PREV_FOX_COLOR = "#6ee7b7"; PREV_FOX_GLOW = "#ecfdf5"
PREV_PW1  = "VEIL_GLOW44"; PREV_PW1_ICON = "🌫️💫"
PREV_DRAW_FOX = "drawWarditeFox9e"
PREV_FOX_R = "BASE_R*2.63"

# ── Step 1 – 8 achievements ───────────────────────────────────────────────────
ACH = f'''  {{ id:"{FOX_TYPE}_tap",          label:"Wurtzite Fox Tap",            desc:"Tap Wurtzite Fox target",               icon:"{FOX_PEAK}", xp:62 }},
  {{ id:"{FOX_TYPE}_peak",         label:"Wurtzite Fox Peak",           desc:"Reach peak with Wurtzite Fox",          icon:"{FOX_PEAK}", xp:124 }},
  {{ id:"{ORB_TYPE}_tap",          label:"Zirconolite Orb Tap",         desc:"Tap Zirconolite Orb target",            icon:"{ORB_PEAK}", xp:62 }},
  {{ id:"{ORB_TYPE}_peak",         label:"Zirconolite Orb Peak",        desc:"Reach peak with Zirconolite Orb",       icon:"{ORB_PEAK}", xp:124 }},
  {{ id:"{PW1.lower()}_use",       label:"Dawn2 Glow",                  desc:"Trigger DAWN2_GLOW44 power-up",         icon:"🌅", xp:62 }},
  {{ id:"{PW1.lower()}_max",       label:"Dawn2 Glow Max",              desc:"Trigger DAWN2_GLOW44 at max streak",    icon:"🌅", xp:124 }},
  {{ id:"{PW2.lower()}_use",       label:"Tide Glow",                   desc:"Trigger TIDE2_GLOW44 power-up",         icon:"🌊", xp:62 }},
  {{ id:"{PW2.lower()}_max",       label:"Tide Glow Max",               desc:"Trigger TIDE2_GLOW44 at max streak",    icon:"🌊", xp:124 }},
  {{ id:"{PREV_FOX_FULL}_tap",'''

anchor1 = f'  {{ id:"{PREV_FOX_FULL}_tap",'
assert src.count(anchor1) == 1, f"Step1 anchor count={src.count(anchor1)}"
src = src.replace(anchor1, ACH, 1)
print("OK Step1-achievements")

# ── Step 2 – power-up list ────────────────────────────────────────────────────
OLD2 = f'"{PREV_PW1}",'
NEW2 = f'"{PW1}","{PW2}","{PREV_PW1}",'
assert src.count(OLD2) >= 1
src = src.replace(OLD2, NEW2, 1)
print("OK Step2-pw-list")

# ── Step 3 – power-up handler ─────────────────────────────────────────────────
HANDLER = f'''}} else if(ptype==="{PW1}"){{
      const bns={PW1_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW1_SHOCK}",28,"shockwave");
      showNotif("🌅 DAWN2 GLOW +"+bns);
      unlock("{PW1.lower()}_use");
      if(gs.streak>=20)unlock("{PW1.lower()}_max");
    }} else if(ptype==="{PW2}"){{
      const bns={PW2_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW2_SHOCK}",28,"shockwave");
      showNotif("🌊 TIDE GLOW +"+bns);
      unlock("{PW2.lower()}_use");
      if(gs.streak>=20)unlock("{PW2.lower()}_max");
    }} else if(ptype==="{PREV_PW1}")''' + '{'

OLD3 = f'}} else if(ptype==="{PREV_PW1}")' + '{'
assert src.count(OLD3) == 1, f"Step3 anchor count={src.count(OLD3)}"
src = src.replace(OLD3, HANDLER, 1)
print("OK Step3-pw-handler")

# ── Step 4 – comment block ────────────────────────────────────────────────────
CMT = f'''// {PW1} — +{PW1_SC} dawn2 glow bonus
    // {PW2} — +{PW2_SC} tide2 glow bonus
    // {PREV_PW1}'''

OLD4 = f'// {PREV_PW1}'
assert src.count(OLD4) >= 1
src = src.replace(OLD4, CMT, 1)
print("OK Step4-pw-comment")

# ── Step 5 – draw functions ───────────────────────────────────────────────────
DRAWS = f'''function drawWurtziteFox9e(ctx,r,ts,sp){{
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;
  ctx.save();
  ctx.shadowColor="{FOX_GLOW}";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#fefce8");g.addColorStop(0.5,"{FOX_COLOR}");g.addColorStop(1,"#854d0e");
  ctx.fillStyle=g;ctx.fill();
  ctx.strokeStyle="{FOX_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{FOX_PEAK}",0,0);
  ctx.restore();
}}
function drawZirconoliteOrb9e(ctx,r,ts,tp){{
  const p=ts/tp,pu=p<0.5?p*2:2-p*2;
  ctx.save();
  ctx.shadowColor="{ORB_GLOW}";ctx.shadowBlur=18+pu*16;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#d6d3d1");g.addColorStop(0.5,"{ORB_COLOR}");g.addColorStop(1,"#1c1917");
  ctx.fillStyle=g;ctx.fill();
  ctx.strokeStyle="{ORB_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;
  ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{ORB_PEAK}",0,0);
  ctx.restore();
}}
function {PREV_DRAW_FOX}('''

OLD5 = f'function {PREV_DRAW_FOX}('
assert src.count(OLD5) == 1, f"Step5 anchor count={src.count(OLD5)}"
src = src.replace(OLD5, DRAWS, 1)
print("OK Step5-draw-functions")

# ── Step 6 – draw dispatch ────────────────────────────────────────────────────
DISP = f'''  else if(t.type==="{FOX_TYPE}"){{drawWurtziteFox9e(ctx,t.radius,ts-t.born,t.lifetime);}}
  else if(t.type==="{ORB_TYPE}"){{drawZirconoliteOrb9e(ctx,t.radius,ts-t.born,t.lifetime);}}
  else if(t.type==="{PREV_FOX_FULL}")''' + '{'

OLD6 = f'  else if(t.type==="{PREV_FOX_FULL}")' + '{'
assert src.count(OLD6) == 1, f"Step6 anchor count={src.count(OLD6)}"
src = src.replace(OLD6, DISP, 1)
print("OK Step6-dispatch")

# ── Step 7 – tap handlers ─────────────────────────────────────────────────────
TAP = f'''if(hit.type==="{FOX_TYPE}"){{
      const pts={FOX_SC}+gs.streak*{SW};
      gs.score+=pts;spawnParticles(hit.x,hit.y,"{FOX_GLOW}",14);
      showPop(hit.x,hit.y,"+"+pts,"{FOX_GLOW}");
      gs.sessionStats.score+=pts;
      unlock("{FOX_TYPE}_tap");
      if(gs.score>={FOX_SC*50})unlock("{FOX_TYPE}_peak");
    }}else if(hit.type==="{ORB_TYPE}"){{
      const pts={ORB_SC}+gs.streak*{SW};
      gs.score+=pts;spawnParticles(hit.x,hit.y,"{ORB_GLOW}",14);
      showPop(hit.x,hit.y,"+"+pts,"{ORB_GLOW}");
      gs.sessionStats.score+=pts;
      unlock("{ORB_TYPE}_tap");
      if(gs.score>={ORB_SC*50})unlock("{ORB_TYPE}_peak");
    }}else if(hit.type==="{PREV_FOX_FULL}")''' + '{'

OLD7 = f'if(hit.type==="{PREV_FOX_FULL}")' + '{'
assert src.count(OLD7) == 1, f"Step7 anchor count={src.count(OLD7)}"
src = src.replace(OLD7, TAP, 1)
print("OK Step7-handlers")

# ── Step 8 – spawn entries ────────────────────────────────────────────────────
SPAWN = f'''type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";
        }}else if(COND100F){{
          type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";
        }}else if(COND100F){{
          type="{PREV_FOX_FULL}";color="{PREV_FOX_COLOR}";glow="{PREV_FOX_GLOW}";'''

OLD8 = f'type="{PREV_FOX_FULL}";color="{PREV_FOX_COLOR}";glow="{PREV_FOX_GLOW}";'
assert src.count(OLD8) == 1, f"Step8 anchor count={src.count(OLD8)}"
src = src.replace(OLD8, SPAWN, 1)
print("OK Step8-spawn")

# ── Step 9 – radius dispatch ──────────────────────────────────────────────────
RAD = f'type==="{FOX_TYPE}"?{FOX_R}:type==="{ORB_TYPE}"?{ORB_R}:type==="{PREV_FOX_FULL}"?{PREV_FOX_R}:'
OLD9 = f'type==="{PREV_FOX_FULL}"?{PREV_FOX_R}:'
assert src.count(OLD9) == 1, f"Step9 anchor count={src.count(OLD9)}"
src = src.replace(OLD9, RAD, 1)
print("OK Step9-radius")

# ── Step 10 – icon map ────────────────────────────────────────────────────────
OLD10 = f'{PREV_PW1}:"{PREV_PW1_ICON}"'
NEW10 = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",{PREV_PW1}:"{PREV_PW1_ICON}"'
cnt = src.count(OLD10)
assert cnt == 2, f"Step10 count={cnt}"
src = src.replace(OLD10, NEW10)
print("OK Step10-icons")

# ── Write ─────────────────────────────────────────────────────────────────────
with open(SRC, "w") as f:
    f.write(src)
print(f"Batch 819 done! +{len(src)-original_len} bytes")
