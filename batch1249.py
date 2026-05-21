import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()
original_len = len(src)

FOX      = "tatarskite"
ORB      = "tausonite"
FOX_TYPE = f"{FOX}_fox9e"
ORB_TYPE = f"{ORB}_orb9e"
FOX_COLOR = "#001818"; FOX_GLOW = "#0e7490"; FOX_PEAK = "\U0001fab5"
ORB_COLOR = "#180018"; ORB_GLOW = "#7c3aed"; ORB_PEAK = "\U0001fa84"
FOX_SC   = 1482;  ORB_SC  = 1477
FOX_R    = "BASE_R*6.94"; ORB_R = "BASE_R*6.93"
OSC      = 0.6245; SW = 3292
PW1 = "XI34_GLOW44"; PW1_SC = 4460; PW1_SHOCK = "#0e7490"; PW1_ICON = "ξ\U0001fab5"
PW2 = "OMICRON34_GLOW44"; PW2_SC = 4462; PW2_SHOCK = "#7c3aed"; PW2_ICON = "ο\U0001fa84"

PREV_FOX_FULL = "taraspite_fox9e"
PREV_FOX_COLOR = "#0c1c00"; PREV_FOX_GLOW = "#65a30d"
PREV_PW1  = "NU34_GLOW44"; PREV_PW1_ICON = "ν\U0001f9a0"
PREV_DRAW_FOX = "draw" + "Taraspite" + "Fox9e"
PREV_FOX_R = "BASE_R*6.93"

FOX_FN = "draw" + "Tatarskite" + "Fox9e"
ORB_FN = "draw" + "Tausonite" + "Orb9e"

ACH = f'''  {{ id:"{FOX_TYPE}_tap",          label:"Tatarskite Fox Tap",          desc:"Tap Tatarskite Fox target",             icon:"{FOX_PEAK}", xp:62 }},
  {{ id:"{FOX_TYPE}_peak",         label:"Tatarskite Fox Peak",         desc:"Reach peak with Tatarskite Fox",        icon:"{FOX_PEAK}", xp:124 }},
  {{ id:"{ORB_TYPE}_tap",          label:"Tausonite Orb Tap",           desc:"Tap Tausonite Orb target",              icon:"{ORB_PEAK}", xp:62 }},
  {{ id:"{ORB_TYPE}_peak",         label:"Tausonite Orb Peak",          desc:"Reach peak with Tausonite Orb",         icon:"{ORB_PEAK}", xp:124 }},
  {{ id:"{PW1.lower()}_use",       label:"Xi34 Glow",                   desc:"Trigger XI34_GLOW44 power-up",          icon:"ξ", xp:62 }},
  {{ id:"{PW1.lower()}_max",       label:"Xi34 Glow Max",               desc:"Trigger XI34_GLOW44 at max streak",     icon:"ξ", xp:124 }},
  {{ id:"{PW2.lower()}_use",       label:"Omicron34 Glow",              desc:"Trigger OMICRON34_GLOW44 power-up",     icon:"ο", xp:62 }},
  {{ id:"{PW2.lower()}_max",       label:"Omicron34 Glow Max",          desc:"Trigger OMICRON34_GLOW44 at max streak",icon:"ο", xp:124 }},
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
      showNotif("ξ XI34 GLOW +"+bns);
      unlock("{PW1.lower()}_use");if(gs.streak>=20)unlock("{PW1.lower()}_max");
    }} else if(ptype==="{PW2}"){{
      const bns={PW2_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW2_SHOCK}",28,"shockwave");
      showNotif("ο OMICRON34 GLOW +"+bns);
      unlock("{PW2.lower()}_use");if(gs.streak>=20)unlock("{PW2.lower()}_max");
    }} else if(ptype==="{PREV_PW1}")''' + '{'
OLD3 = f'}} else if(ptype==="{PREV_PW1}")' + '{'
assert src.count(OLD3) == 1; src = src.replace(OLD3, HANDLER, 1); print("OK Step3")

CMT = f'// {PW1} — +{PW1_SC} xi34\n    // {PW2} — +{PW2_SC} omicron34\n    // {PREV_PW1}'
OLD4 = f'// {PREV_PW1}'; assert src.count(OLD4) >= 1
src = src.replace(OLD4, CMT, 1); print("OK Step4")

DRAWS = f'''function {FOX_FN}(ctx,r,ts,sp){{
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{FOX_GLOW}";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#0e7490");g.addColorStop(0.5,"{FOX_COLOR}");g.addColorStop(1,"#083344");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="{FOX_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{FOX_PEAK}",0,0);ctx.restore();
}}
function {ORB_FN}(ctx,r,ts,tp){{
  const p=ts/tp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{ORB_GLOW}";ctx.shadowBlur=18+pu*16;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#7c3aed");g.addColorStop(0.5,"{ORB_COLOR}");g.addColorStop(1,"#2e1065");
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
print(f"Batch 1249 done! +{len(src)-original_len} bytes")
