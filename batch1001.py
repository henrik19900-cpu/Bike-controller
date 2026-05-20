import re

SRC = "src/NexusTap.jsx"
with open(SRC, "r") as f:
    src = f.read()
original_len = len(src)

FOX      = "zaratite"
ORB      = "zellerite"
FOX_TYPE = f"{FOX}_fox9e"
ORB_TYPE = f"{ORB}_orb9e"
FOX_COLOR = "#065f46"; FOX_GLOW = "#34d399"; FOX_PEAK = "💚"
ORB_COLOR = "#365314"; ORB_GLOW = "#bef264"; ORB_PEAK = "💛"
FOX_SC   = 986;  ORB_SC  = 981
FOX_R    = "BASE_R*4.46"; ORB_R = "BASE_R*4.45"
OSC      = 0.5253; SW = 2796
PW1 = "CHI13_GLOW44"; PW1_SC = 3468; PW1_SHOCK = "#34d399"; PW1_ICON = "χ💚"
PW2 = "PSI13_GLOW44"; PW2_SC = 3470; PW2_SHOCK = "#bef264"; PW2_ICON = "ψ💛"

PREV_FOX_FULL = "zirkelite_fox9e"
PREV_FOX_COLOR = "#1e293b"; PREV_FOX_GLOW = "#94a3b8"
PREV_PW1  = "UPSILON13_GLOW44"; PREV_PW1_ICON = "υ🔮"
PREV_DRAW_FOX = "draw" + "Zirkelite" + "Fox9e"
PREV_FOX_R = "BASE_R*4.45"

FOX_FN = "draw" + "Zaratite" + "Fox9e"
ORB_FN = "draw" + "Zellerite" + "Orb9e"

ACH = f'''  {{ id:"{FOX_TYPE}_tap",          label:"Zaratite Fox Tap",            desc:"Tap Zaratite Fox target",               icon:"{FOX_PEAK}", xp:62 }},
  {{ id:"{FOX_TYPE}_peak",         label:"Zaratite Fox Peak",           desc:"Reach peak with Zaratite Fox",          icon:"{FOX_PEAK}", xp:124 }},
  {{ id:"{ORB_TYPE}_tap",          label:"Zellerite Orb Tap",           desc:"Tap Zellerite Orb target",              icon:"{ORB_PEAK}", xp:62 }},
  {{ id:"{ORB_TYPE}_peak",         label:"Zellerite Orb Peak",          desc:"Reach peak with Zellerite Orb",         icon:"{ORB_PEAK}", xp:124 }},
  {{ id:"{PW1.lower()}_use",       label:"Chi13 Glow",                  desc:"Trigger CHI13_GLOW44 power-up",         icon:"χ", xp:62 }},
  {{ id:"{PW1.lower()}_max",       label:"Chi13 Glow Max",              desc:"Trigger CHI13_GLOW44 at max streak",    icon:"χ", xp:124 }},
  {{ id:"{PW2.lower()}_use",       label:"Psi13 Glow",                  desc:"Trigger PSI13_GLOW44 power-up",         icon:"ψ", xp:62 }},
  {{ id:"{PW2.lower()}_max",       label:"Psi13 Glow Max",              desc:"Trigger PSI13_GLOW44 at max streak",    icon:"ψ", xp:124 }},
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
      showNotif("χ CHI13 GLOW +"+bns);
      unlock("{PW1.lower()}_use");if(gs.streak>=20)unlock("{PW1.lower()}_max");
    }} else if(ptype==="{PW2}"){{
      const bns={PW2_SC}+gs.streak*12;
      gs.score+=bns;setHud(h=>({{...h,score:gs.score}}));
      spawnParticles(W/2,H/2,"{PW2_SHOCK}",28,"shockwave");
      showNotif("ψ PSI13 GLOW +"+bns);
      unlock("{PW2.lower()}_use");if(gs.streak>=20)unlock("{PW2.lower()}_max");
    }} else if(ptype==="{PREV_PW1}")''' + '{'
OLD3 = f'}} else if(ptype==="{PREV_PW1}")' + '{'
assert src.count(OLD3) == 1; src = src.replace(OLD3, HANDLER, 1); print("OK Step3")

CMT = f'// {PW1} — +{PW1_SC} chi13\n    // {PW2} — +{PW2_SC} psi13\n    // {PREV_PW1}'
OLD4 = f'// {PREV_PW1}'; assert src.count(OLD4) >= 1
src = src.replace(OLD4, CMT, 1); print("OK Step4")

DRAWS = f'''function {FOX_FN}(ctx,r,ts,sp){{
  const p=ts/sp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{FOX_GLOW}";ctx.shadowBlur=20+pu*18;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#34d399");g.addColorStop(0.5,"{FOX_COLOR}");g.addColorStop(1,"#022c22");
  ctx.fillStyle=g;ctx.fill();ctx.strokeStyle="{FOX_GLOW}";ctx.lineWidth=2+pu*2;ctx.stroke();
  ctx.font=`${{Math.round(r*{OSC}*10)/10}}px serif`;ctx.textAlign="center";ctx.textBaseline="middle";
  ctx.fillText("{FOX_PEAK}",0,0);ctx.restore();
}}
function {ORB_FN}(ctx,r,ts,tp){{
  const p=ts/tp,pu=p<0.5?p*2:2-p*2;ctx.save();
  ctx.shadowColor="{ORB_GLOW}";ctx.shadowBlur=18+pu*16;
  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);
  const g=ctx.createRadialGradient(0,0,r*0.1,0,0,r);
  g.addColorStop(0,"#bef264");g.addColorStop(0.5,"{ORB_COLOR}");g.addColorStop(1,"#1a2e05");
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
print(f"Batch 1001 done! +{len(src)-original_len} bytes")
