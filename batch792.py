#!/usr/bin/env python3
"""Batch 792 — FLUX_GLOW44+RUSH_GLOW44 + NorthupiteFox9e+NovacekiteOrb9e + 8 achievements"""
import sys

SRC = "src/NexusTap.jsx"
data = open(SRC, encoding="utf-8").read()
orig_len = len(data)

COND100F = ('(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive'
            '&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")'
            '&&!modifier?.type?.includes("final")')

OSC   = "0.4417"
SW    = "2378"

FOX_TYPE   = "northupite_fox9e"
FOX_COLOR  = "#d97706"
FOX_GLOW   = "#fef3c7"
FOX_LIGHT  = "#fef3c7"
FOX_MID    = "#fbbf24"
FOX_DARK   = "#78350f"
FOX_RGB    = "251,191,36"
FOX_PEAK   = "🌟"
FOX_SC     = "568"
FOX_R      = "BASE_R*2.37"

ORB_TYPE   = "novacekite_orb9e"
ORB_COLOR  = "#be185d"
ORB_GLOW   = "#fce7f3"
ORB_LIGHT  = "#fce7f3"
ORB_MID    = "#f472b6"
ORB_DARK   = "#831843"
ORB_RGB    = "244,114,182"
ORB_PEAK   = "🌸"
ORB_SC     = "563"
ORB_R      = "BASE_R*2.36"

PW1        = "FLUX_GLOW44"
PW1_SC     = "2632"
PW1_SHOCK  = "#8b5cf6"
PW1_ICON   = "⚡💫"

PW2        = "RUSH_GLOW44"
PW2_SC     = "2634"
PW2_SHOCK  = "#f59e0b"
PW2_ICON   = "🚀✨"

def replace_once(old, new, label):
    global data
    cnt = data.count(old)
    if cnt != 1:
        print(f"ERROR {label}: expected 1, found {cnt}")
        sys.exit(1)
    data = data.replace(old, new, 1)
    print(f"OK {label}")

# Step 1
A1_OLD = '  { id:"niobite_fox9e_tap",      label:"Niobite Fox Tap"'
A1_NEW = (
    '  { id:"northupite_fox9e_tap",   label:"Northupite Fox Tap",     desc:"Tap Northupite Fox target",            icon:"🌟", xp:62 },\n'
    '  { id:"northupite_fox9e_peak",  label:"Northupite Fox Peak",    desc:"Reach peak with Northupite Fox",       icon:"🌟", xp:124 },\n'
    '  { id:"novacekite_orb9e_tap",   label:"Novacekite Orb Tap",     desc:"Tap Novacekite Orb target",            icon:"🌸", xp:62 },\n'
    '  { id:"novacekite_orb9e_peak",  label:"Novacekite Orb Peak",    desc:"Reach peak with Novacekite Orb",       icon:"🌸", xp:124 },\n'
    '  { id:"flux_glow44_use",        label:"Flux Glow",              desc:"Trigger FLUX_GLOW44 power-up",         icon:"⚡", xp:62 },\n'
    '  { id:"flux_glow44_max",        label:"Flux Glow Max",          desc:"Trigger FLUX_GLOW44 at max streak",    icon:"⚡", xp:124 },\n'
    '  { id:"rush_glow44_use",        label:"Rush Glow",              desc:"Trigger RUSH_GLOW44 power-up",         icon:"🚀", xp:62 },\n'
    '  { id:"rush_glow44_max",        label:"Rush Glow Max",          desc:"Trigger RUSH_GLOW44 at max streak",    icon:"🚀", xp:124 },\n'
    '  { id:"niobite_fox9e_tap",      label:"Niobite Fox Tap"'
)
replace_once(A1_OLD, A1_NEW, "Step1-achievements")

# Step 2
A2_OLD = '"FLOW_GLOW44","RUN_GLOW44"'
A2_NEW = f'"{PW1}","{PW2}","FLOW_GLOW44","RUN_GLOW44"'
replace_once(A2_OLD, A2_NEW, "Step2-pw-list")

# Step 3
A3_OLD = '  } else if(ptype==="FLOW_GLOW44"){'
A3_NEW = (
    f'  }} else if(ptype==="{PW1}"){{' + '\n'
    f'        gs.score+=({PW1_SC}+gs.streak*4);addPopup("+{PW1_SC} {PW1_ICON}",cx,cy,"{PW1_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW1_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("flux_glow44_use");if(gs.streak>=30)unlock("flux_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    f'  }} else if(ptype==="{PW2}"){{' + '\n'
    f'        gs.score+=({PW2_SC}+gs.streak*4);addPopup("+{PW2_SC} {PW2_ICON}",cx,cy,"{PW2_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW2_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("rush_glow44_use");if(gs.streak>=30)unlock("rush_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    '  } else if(ptype==="FLOW_GLOW44"){'
)
replace_once(A3_OLD, A3_NEW, "Step3-pw-handler")

# Step 4
A4_OLD = '  // FLOW_GLOW44 — +2628 flow glow bonus'
A4_NEW = (
    f'  // {PW1} — +{PW1_SC} flux glow bonus\n'
    f'        // {PW2} — +{PW2_SC} rush glow bonus\n'
    '  // FLOW_GLOW44 — +2628 flow glow bonus'
)
replace_once(A4_OLD, A4_NEW, "Step4-pw-comment")

# Step 5
A5_OLD = 'function drawNiobiteFox9e('
A5_NEW = (
    f'function drawNorthupiteFox9e(ctx,r,ts,sp){{\n'
    f'  const bob=Math.sin(ts*{OSC})*r*0.07;\n'
    f'  ctx.save();ctx.translate(0,bob);\n'
    f'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    f'  g.addColorStop(0,"{FOX_LIGHT}");g.addColorStop(0.45+sp*0.35,"{FOX_MID}");g.addColorStop(1,"{FOX_DARK}");\n'
    f'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    f'  if(sp>0.65){{\n'
    f'    ctx.beginPath();ctx.arc(0,0,r*1.13,0,Math.PI*2);\n'
    f'    ctx.strokeStyle="rgba({FOX_RGB},"+(sp-0.65)*2.8+")";ctx.lineWidth=3.5;ctx.stroke();}}\n'
    f'  ctx.fillStyle=sp>0.88?"{FOX_DARK}":"{FOX_LIGHT}";ctx.font=(r*0.56)+"px serif";\n'
    f'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(sp>0.88?"{FOX_PEAK}":"🦊",0,1);\n'
    f'  ctx.restore();\n'
    f'}}\n'
    f'function drawNovacekiteOrb9e(ctx,r,ts,tp){{\n'
    f'  const pulse=0.72+0.28*Math.sin(ts*{OSC});\n'
    f'  ctx.save();ctx.scale(pulse,pulse);ctx.globalAlpha=0.73+tp*0.27;\n'
    f'  const g=ctx.createRadialGradient(0,0,r*0.12,0,0,r);\n'
    f'  g.addColorStop(0,"{ORB_LIGHT}");g.addColorStop(0.35+tp*0.35,"{ORB_MID}");g.addColorStop(1,"{ORB_DARK}");\n'
    f'  ctx.beginPath();ctx.arc(0,0,r,0,Math.PI*2);ctx.fillStyle=g;ctx.fill();\n'
    f'  const ring=r*(0.54+tp*0.42);\n'
    f'  ctx.beginPath();ctx.arc(0,0,ring,0,Math.PI*2);\n'
    f'  ctx.strokeStyle="rgba({ORB_RGB},"+(0.45+tp*0.55)+")";ctx.lineWidth=3.5+tp*3;ctx.stroke();\n'
    f'  ctx.globalAlpha=1;\n'
    f'  if(tp>0.82){{\n'
    f'    ctx.beginPath();ctx.arc(0,0,r*1.18,0,Math.PI*2);\n'
    f'    ctx.strokeStyle="rgba({ORB_RGB},"+(tp-0.82)*3.5+")";ctx.lineWidth=2.5;ctx.stroke();}}\n'
    f'  ctx.fillStyle=tp>0.88?"{ORB_MID}":"{ORB_LIGHT}";ctx.font=(r*0.56)+"px serif";\n'
    f'  ctx.textAlign="center";ctx.textBaseline="middle";ctx.fillText(tp>0.88?"{ORB_PEAK}":"🔮",0,1);\n'
    f'  ctx.restore();\n'
    f'}}\n'
    'function drawNiobiteFox9e('
)
replace_once(A5_OLD, A5_NEW, "Step5-draw-functions")

# Step 6
A6_OLD = '  else if(t.type==="niobite_fox9e"){'
A6_NEW = (
    f'  else if(t.type==="{FOX_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp792a=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawNorthupiteFox9e(ctx,t.radius,ts,sp792a);ctx.restore();\n'
    f'  }}\n'
    f'  else if(t.type==="{ORB_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp792b=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawNovacekiteOrb9e(ctx,t.radius,ts,tp792b);ctx.restore();\n'
    f'  }}\n'
    '  else if(t.type==="niobite_fox9e"){'
)
replace_once(A6_OLD, A6_NEW, "Step6-dispatch")

# Step 7
A7_OLD = '    if(hit.type==="niobite_fox9e"){'
A7_NEW = (
    f'    if(hit.type==="{FOX_TYPE}"){{\n'
    f'          const sp792c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts792a=Math.round({FOX_SC}*(1+sp792c));\n'
    f'          gs.score+=pts792a;gs.streak++;addPopup("+"+pts792a+(sp792c>0.88?" {FOX_PEAK} PEAK!":""),hit.x,hit.y,"{FOX_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{FOX_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(sp792c>0.88){{sfx("legendary");unlock("{FOX_TYPE}_peak");}}else unlock("{FOX_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="{ORB_TYPE}"){{\n'
    f'          const tp792d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts792b=Math.round({ORB_SC}*(1+tp792d));\n'
    f'          gs.score+=pts792b;gs.streak++;addPopup("+"+pts792b+(tp792d>0.88?" {ORB_PEAK} PEAK!":""),hit.x,hit.y,"{ORB_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{ORB_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(tp792d>0.88){{sfx("legendary");unlock("{ORB_TYPE}_peak");}}else unlock("{ORB_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="niobite_fox9e"){{'
)
replace_once(A7_OLD, A7_NEW, "Step7-handlers")

# Step 8
A8_OLD = ('      type="niobite_fox9e";color="#7c3aed";glow="#ede9fe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="nordite_orb9e"')
A8_NEW = (
    f'      type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="niobite_fox9e";color="#7c3aed";glow="#ede9fe";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="nordite_orb9e"'
)
replace_once(A8_OLD, A8_NEW, "Step8-spawn")

# Step 9
A9_OLD = 'type==="niobite_fox9e"?BASE_R*2.36:'
A9_NEW = (
    f'type==="{FOX_TYPE}"?{FOX_R}:'
    f'type==="{ORB_TYPE}"?{ORB_R}:'
    'type==="niobite_fox9e"?BASE_R*2.36:'
)
replace_once(A9_OLD, A9_NEW, "Step9-radius")

# Step 10 (cnt==2)
A10_OLD = 'FLOW_GLOW44:"💧✨"'
A10_NEW = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",FLOW_GLOW44:"💧✨"'
cnt10 = data.count(A10_OLD)
if cnt10 != 2:
    print(f"ERROR Step10: expected 2, found {cnt10}")
    sys.exit(1)
data = data.replace(A10_OLD, A10_NEW)
print("OK Step10-icons")

open(SRC, "w", encoding="utf-8").write(data)
print(f"Batch 792 done! +{len(data)-orig_len} bytes")
