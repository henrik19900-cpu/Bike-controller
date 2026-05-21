import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()
original_len = len(src)

FOX      = "ramdohrite"
ORB      = "rameauite"
FOX_TYPE = f"{FOX}_fox9e"
ORB_TYPE = f"{ORB}_orb9e"
FOX_COLOR = "#180c00"; FOX_GLOW = "#92400e"; FOX_PEAK = "\U0001f9ca"
ORB_COLOR = "#001c10"; ORB_GLOW = "#047857"; ORB_PEAK = "\U0001f343"
FOX_SC   = 1422;  ORB_SC  = 1417
FOX_R    = "BASE_R*6.64"; ORB_R = "BASE_R*6.63"
OSC      = 0.6125; SW = 3232
PW1 = "BETA32_GLOW44"; PW1_SC = 4340; PW1_SHOCK = "#92400e"; PW1_ICON = "β\U0001f9ca"
PW2 = "GAMMA32_GLOW44"; PW2_SC = 4342; PW2_SHOCK = "#047857"; PW2_ICON = "γ\U0001f343"

PREV_FOX_FULL = "raguinite_fox9e"
PREV_FOX_COLOR = "#1c0c00"; PREV_FOX_GLOW = "#b45309"
PREV_PW1  = "ALPHA32_GLOW44"; PREV_PW1_ICON = "α\U0001f30a"
PREV_DRAW_FOX = "draw" + "Raguinite" + "Fox9e"
PREV_FOX_R = "BASE_R*6.63"

FOX_FN = "draw" + "Ramdohrite" + "Fox9e"
ORB_FN = "draw" + "Rameauite" + "Orb9e"

ACH = f'''  {{ id:"{FOX_TYPE}_tap",          label:"Ramdohrite Fox Tap",          desc:"Tap Ramdohrite Fox target",             icon:"{FOX_PEAK}", xp:62 }},
  {{ id:"{FOX_TYPE}_peak",         label:"Ramdohrite Fox Peak",         desc:"Reach peak with Ramdohrite Fox",        icon:"{FOX_PEAK}", xp:124 }},
  {{ id:"{ORB_TYPE}_tap",          label:"Rameauite Orb Tap",           desc:"Tap Rameauite Orb target",              icon:"{ORB_PEAK}", xp:62 }},
  {{ id:"{ORB_TYPE}_peak",         label:"Rameauite Orb Peak",          desc:"Reach peak with Rameauite Orb",         icon:"{ORB_PEAK}", xp:124 }},
  {{ id:"{PW1.lower()}_use",       label:"Beta32 Glow",                 desc:"Trigger BETA32_GLOW44 power-up",        icon:"β", xp:62 }},
  {{ id:"{PW1.lower()}_max",       label:"Beta32 Glow Max",             desc:"Trigger BETA32_GLOW44 at max streak",   icon:"β", xp:124 }},
  {{ id:"{PW2.lower()}_use",       label:"Gamma32 Glow",                desc:"Trigger GAMMA32_GLOW44 power-up",       icon:"γ", xp:62 }},
  {{ id:"{PW2.lower()}_max",       label:"Gamma32 Glow Max",            desc:"Trigger GAMMA32_GLOW44 at max streak",  icon:"γ", xp:124 }},
  {{ id:"{PREV_FOX_FULL}_tap",'''
anchor1 = f'  {{ id:"{PREV_FOX_FULL}_tap",'
assert src.count(anchor1) == 1
src = src.replace(anchor1, ACH, 1); print("OK Step1")

OLD2 = f'"{PREV_PW1}",'; NEW2 = f'"{PW1}","{PW2}","{PREV_PW1}",'
assert src.count(OLD2) >= 1; src = src.replace(OLD2, NEW2, 1); print("OK Step2")

HANDLER = f'''}} else if(ptype==="{PW1}"){{
      const bns={PW1_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW1_SHOCK}",28,"shockwave");
      showNotif("β BETA32 GLOW +"+bns);
      unlock("{PW1.lower()}_use");if(gs.streak>=20)unlock("{PW1.lower()}_max");
    }} else if(ptype==="{PW2}"){{
      const bns={PW2_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW2_SHOCK}",28,"shockwave");
      showNotif("γ GAMMA32 GLOW +"+bns);
      unlock("{PW2.lower()}_use");if(gs.streak>=20)unlock("{PW2.lower()}_max");
    }} else if(ptype==="{PREV_PW1}")''' + '{'
OLD3 = f'}} else if(ptype==="{PREV_PW1}")' + '{'
assert src.count(OLD3) == 1; src = src.replace(OLD3, HANDLER, 1); print("OK Step3")

CMT = f'// {PW1} — +{PW1_SC} beta32\n    // {PW2} — +{PW2_SC} gamma32\n    // {PREV_PW1}'
OLD4 = f'// {PREV_PW1}'; assert src.count(OLD4) >= 1
src = src.replace(OLD4, CMT, 1); print("OK Step4")

DRAWS = f'''function {FOX_FN}(ctx,r,ts,sp){{
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{FOX_GLOW}";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#92400e");g.addColorStop(0.5,"{FOX_COLOR}");g.addColorStop(1,"#431407");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="{FOX_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{FOX_PEAK}",0,0);ctx.restore();
}}
function {ORB_FN}(ctx,r,ts,tp){{
  const p=ts/tp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{ORB_GLOW}";ctx.shadowBlur=18+pu*16;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#047857");g.addColorStop(0.5,"{ORB_COLOR}");g.addColorStop(1,"#022c22");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="{ORB_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{ORB_PEAK}",0,0);ctx.restore();
}}
function {PREV_DRAW_FOX}('''
OLD5 = f'function {PREV_DRAW_FOX}('
assert src.count(OLD5) == 1; src = src.replace(OLD5, DRAWS, 1); print("OK Step5")

DISP = f'  else if(t.type==="{FOX_TYPE}"){{{FOX_FN}(ctx,t.radius,ts-t.born,t.lifetime);}}\n  else if(t.type==="{ORB_TYPE}"){{{ORB_FN}(ctx,t.radius,ts-t.born,t.lifetime);}}\n  else if(t.type==="{PREV_FOX_FULL}")' + '{'
OLD6 = f'  else if(t.type==="{PREV_FOX_FULL}")' + '{'
assert src.count(OLD6) == 1; src = src.replace(OLD6, DISP, 1); print("OK Step6")

TAP = f'''if(hit.type==="{FOX_TYPE}"){{
      const pts={FOX_SC}+gs.streak*{SW};gs.score+=pts;spawnParticles(hit.x,hit.y,"{FOX_GLOW}",14);
      showPop(hit.x,hit.y,"+"+pts,"{FOX_GLOW}");gs.sessionStats.score+=pts;
      unlock("{FOX_TYPE}_tap");if(gs.score>={FOX_SC*50})unlock("{FOX_TYPE}_peak");
    }}else if(hit.type==="{ORB_TYPE}"){{
      const pts={ORB_SC}+gs.streak*{SW};gs.score+=pts;spawnParticles(hit.x,hit.y,"{ORB_GLOW}",14);
      showPop(hit.x,hit.y,"+"+pts,"{ORB_GLOW}");gs.sessionStats.score+=pts;
      unlock("{ORB_TYPE}_tap");if(gs.score>={ORB_SC*50})unlock("{ORB_TYPE}_peak");
    }}else if(hit.type==="{PREV_FOX_FULL}")''' + '{'
OLD7 = f'if(hit.type==="{PREV_FOX_FULL}")' + '{'
assert src.count(OLD7) == 1; src = src.replace(OLD7, TAP, 1); print("OK Step7")

SPAWN = f'''type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";
        }}else if(COND100F){{
          type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";
        }}else if(COND100F){{
          type="{PREV_FOX_FULL}";color="{PREV_FOX_COLOR}";glow="{PREV_FOX_GLOW}";'''
OLD8 = f'type="{PREV_FOX_FULL}";color="{PREV_FOX_COLOR}";glow="{PREV_FOX_GLOW}";'
assert src.count(OLD8) == 1; src = src.replace(OLD8, SPAWN, 1); print("OK Step8")

RAD = f'type==="{FOX_TYPE}"?{FOX_R}:type==="{ORB_TYPE}"?{ORB_R}:type==="{PREV_FOX_FULL}"?{PREV_FOX_R}:'
OLD9 = f'type==="{PREV_FOX_FULL}"?{PREV_FOX_R}:'
assert src.count(OLD9) == 1; src = src.replace(OLD9, RAD, 1); print("OK Step9")

OLD10 = f'{PREV_PW1}:"{PREV_PW1_ICON}"'
NEW10 = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",{PREV_PW1}:"{PREV_PW1_ICON}"'
cnt = src.count(OLD10); assert cnt == 2, f"cnt={cnt}"
src = src.replace(OLD10, NEW10); print("OK Step10")

with open(SRC, "w") as f: f.write(src)
print(f"Batch 1219 done! +{len(src)-original_len} bytes")
