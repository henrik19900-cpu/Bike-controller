#!/usr/bin/env python3
"""Batch 803 — TITAN_GLOW44+FURY_GLOW44 + RoscoeliteFox9e+RosasiteOrb9e + 8 achievements"""
import sys

SRC = "src/NexusTap.jsx"
data = open(SRC, encoding="utf-8").read()
orig_len = len(data)

COND100F = ('(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive'
            '&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")'
            '&&!modifier?.type?.includes("final")')

OSC   = "0.4461"
SW    = "2400"

FOX_TYPE   = "roscoelite_fox9e"
FOX_COLOR  = "#166534"
FOX_GLOW   = "#f0fdf4"
FOX_LIGHT  = "#bbf7d0"
FOX_MID    = "#4ade80"
FOX_DARK   = "#052e16"
FOX_RGB    = "74,222,128"
FOX_PEAK   = "🌱"
FOX_SC     = "590"
FOX_R      = "BASE_R*2.48"

ORB_TYPE   = "rosasite_orb9e"
ORB_COLOR  = "#0891b2"
ORB_GLOW   = "#ecfeff"
ORB_LIGHT  = "#a5f3fc"
ORB_MID    = "#22d3ee"
ORB_DARK   = "#083344"
ORB_RGB    = "34,211,238"
ORB_PEAK   = "🌀"
ORB_SC     = "585"
ORB_R      = "BASE_R*2.47"

PW1        = "TITAN_GLOW44"
PW1_SC     = "2676"
PW1_SHOCK  = "#1e40af"
PW1_ICON   = "🗿✨"

PW2        = "FURY_GLOW44"
PW2_SC     = "2678"
PW2_SHOCK  = "#b91c1c"
PW2_ICON   = "😤✨"

def replace_once(old, new, label):
    global data
    cnt = data.count(old)
    if cnt != 1:
        print(f"ERROR {label}: expected 1, found {cnt}")
        sys.exit(1)
    data = data.replace(old, new, 1)
    print(f"OK {label}")

# Step 1
A1_OLD = '  { id:"quicksilver_fox9e_tap",      label:"Quicksilver Fox Tap"'
A1_NEW = (
    '  { id:"roscoelite_fox9e_tap",       label:"Roscoelite Fox Tap",       desc:"Tap Roscoelite Fox target",          icon:"🌱", xp:62 },\n'
    '  { id:"roscoelite_fox9e_peak",      label:"Roscoelite Fox Peak",      desc:"Reach peak with Roscoelite Fox",     icon:"🌱", xp:124 },\n'
    '  { id:"rosasite_orb9e_tap",         label:"Rosasite Orb Tap",         desc:"Tap Rosasite Orb target",            icon:"🌀", xp:62 },\n'
    '  { id:"rosasite_orb9e_peak",        label:"Rosasite Orb Peak",        desc:"Reach peak with Rosasite Orb",       icon:"🌀", xp:124 },\n'
    '  { id:"titan_glow44_use",           label:"Titan Glow",               desc:"Trigger TITAN_GLOW44 power-up",      icon:"🗿", xp:62 },\n'
    '  { id:"titan_glow44_max",           label:"Titan Glow Max",           desc:"Trigger TITAN_GLOW44 at max streak", icon:"🗿", xp:124 },\n'
    '  { id:"fury_glow44_use",            label:"Fury Glow",                desc:"Trigger FURY_GLOW44 power-up",       icon:"😤", xp:62 },\n'
    '  { id:"fury_glow44_max",            label:"Fury Glow Max",            desc:"Trigger FURY_GLOW44 at max streak",  icon:"😤", xp:124 },\n'
    '  { id:"quicksilver_fox9e_tap",      label:"Quicksilver Fox Tap"'
)
replace_once(A1_OLD, A1_NEW, "Step1-achievements")

# Step 2
A2_OLD = '"MEGA_GLOW44","KING_GLOW44"'
A2_NEW = f'"{PW1}","{PW2}","MEGA_GLOW44","KING_GLOW44"'
replace_once(A2_OLD, A2_NEW, "Step2-pw-list")

# Step 3
A3_OLD = '  } else if(ptype==="MEGA_GLOW44"){'
A3_NEW = (
    f'  }} else if(ptype==="{PW1}"){{' + '\n'
    f'        gs.score+=({PW1_SC}+gs.streak*4);addPopup("+{PW1_SC} {PW1_ICON}",cx,cy,"{PW1_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW1_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("titan_glow44_use");if(gs.streak>=30)unlock("titan_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    f'  }} else if(ptype==="{PW2}"){{' + '\n'
    f'        gs.score+=({PW2_SC}+gs.streak*4);addPopup("+{PW2_SC} {PW2_ICON}",cx,cy,"{PW2_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW2_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("fury_glow44_use");if(gs.streak>=30)unlock("fury_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    '  } else if(ptype==="MEGA_GLOW44"){'
)
replace_once(A3_OLD, A3_NEW, "Step3-pw-handler")

# Step 4
A4_OLD = '  // MEGA_GLOW44 — +2672 mega glow bonus'
A4_NEW = (
    f'  // {PW1} — +{PW1_SC} titan glow bonus\n'
    f'        // {PW2} — +{PW2_SC} fury glow bonus\n'
    '  // MEGA_GLOW44 — +2672 mega glow bonus'
)
replace_once(A4_OLD, A4_NEW, "Step4-pw-comment")

# Step 5
A5_OLD = 'function drawQuicksilverFox9e('
A5_NEW = (
    f'function drawRoscoeliteFox9e(ctx,r,ts,sp){{\n'
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
    f'function drawRosasiteOrb9e(ctx,r,ts,tp){{\n'
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
    'function drawQuicksilverFox9e('
)
replace_once(A5_OLD, A5_NEW, "Step5-draw-functions")

# Step 6
A6_OLD = '  else if(t.type==="quicksilver_fox9e"){'
A6_NEW = (
    f'  else if(t.type==="{FOX_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp803a=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawRoscoeliteFox9e(ctx,t.radius,ts,sp803a);ctx.restore();\n'
    f'  }}\n'
    f'  else if(t.type==="{ORB_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp803b=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawRosasiteOrb9e(ctx,t.radius,ts,tp803b);ctx.restore();\n'
    f'  }}\n'
    '  else if(t.type==="quicksilver_fox9e"){'
)
replace_once(A6_OLD, A6_NEW, "Step6-dispatch")

# Step 7
A7_OLD = '    if(hit.type==="quicksilver_fox9e"){'
A7_NEW = (
    f'    if(hit.type==="{FOX_TYPE}"){{\n'
    f'          const sp803c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts803a=Math.round({FOX_SC}*(1+sp803c));\n'
    f'          gs.score+=pts803a;gs.streak++;addPopup("+"+pts803a+(sp803c>0.88?" {FOX_PEAK} PEAK!":""),hit.x,hit.y,"{FOX_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{FOX_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(sp803c>0.88){{sfx("legendary");unlock("{FOX_TYPE}_peak");}}else unlock("{FOX_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="{ORB_TYPE}"){{\n'
    f'          const tp803d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts803b=Math.round({ORB_SC}*(1+tp803d));\n'
    f'          gs.score+=pts803b;gs.streak++;addPopup("+"+pts803b+(tp803d>0.88?" {ORB_PEAK} PEAK!":""),hit.x,hit.y,"{ORB_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{ORB_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(tp803d>0.88){{sfx("legendary");unlock("{ORB_TYPE}_peak");}}else unlock("{ORB_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="quicksilver_fox9e"){{'
)
replace_once(A7_OLD, A7_NEW, "Step7-handlers")

# Step 8
A8_OLD = ('      type="quicksilver_fox9e";color="#4338ca";glow="#e0e7ff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="quetzalcoatlite_orb9e"')
A8_NEW = (
    f'      type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="quicksilver_fox9e";color="#4338ca";glow="#e0e7ff";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="quetzalcoatlite_orb9e"'
)
replace_once(A8_OLD, A8_NEW, "Step8-spawn")

# Step 9
A9_OLD = 'type==="quicksilver_fox9e"?BASE_R*2.47:'
A9_NEW = (
    f'type==="{FOX_TYPE}"?{FOX_R}:'
    f'type==="{ORB_TYPE}"?{ORB_R}:'
    'type==="quicksilver_fox9e"?BASE_R*2.47:'
)
replace_once(A9_OLD, A9_NEW, "Step9-radius")

# Step 10 (cnt==2)
A10_OLD = 'MEGA_GLOW44:"💥🌟"'
A10_NEW = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",MEGA_GLOW44:"💥🌟"'
cnt10 = data.count(A10_OLD)
if cnt10 != 2:
    print(f"ERROR Step10: expected 2, found {cnt10}")
    sys.exit(1)
data = data.replace(A10_OLD, A10_NEW)
print("OK Step10-icons")

open(SRC, "w", encoding="utf-8").write(data)
print(f"Batch 803 done! +{len(data)-orig_len} bytes")
