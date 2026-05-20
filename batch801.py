#!/usr/bin/env python3
"""Batch 801 — ULTRA_GLOW44+HYPER_GLOW44 + RaspiteFox9e+QuenstedtiteOrb9e + 8 achievements"""
import sys

SRC = "src/NexusTap.jsx"
data = open(SRC, encoding="utf-8").read()
orig_len = len(data)

COND100F = ('(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive'
            '&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")'
            '&&!modifier?.type?.includes("final")')

OSC   = "0.4453"
SW    = "2396"

FOX_TYPE   = "raspite_fox9e"
FOX_COLOR  = "#a21caf"
FOX_GLOW   = "#fdf4ff"
FOX_LIGHT  = "#f5d0fe"
FOX_MID    = "#e879f9"
FOX_DARK   = "#4a044e"
FOX_RGB    = "232,121,249"
FOX_PEAK   = "🌸"
FOX_SC     = "586"
FOX_R      = "BASE_R*2.46"

ORB_TYPE   = "quenstedtite_orb9e"
ORB_COLOR  = "#ea580c"
ORB_GLOW   = "#fff7ed"
ORB_LIGHT  = "#fed7aa"
ORB_MID    = "#fb923c"
ORB_DARK   = "#431407"
ORB_RGB    = "251,146,60"
ORB_PEAK   = "🍊"
ORB_SC     = "581"
ORB_R      = "BASE_R*2.45"

PW1        = "ULTRA_GLOW44"
PW1_SC     = "2668"
PW1_SHOCK  = "#7c3aed"
PW1_ICON   = "⚡💥"

PW2        = "HYPER_GLOW44"
PW2_SC     = "2670"
PW2_SHOCK  = "#dc2626"
PW2_ICON   = "🔥💥"

def replace_once(old, new, label):
    global data
    cnt = data.count(old)
    if cnt != 1:
        print(f"ERROR {label}: expected 1, found {cnt}")
        sys.exit(1)
    data = data.replace(old, new, 1)
    print(f"OK {label}")

# Step 1
A1_OLD = '  { id:"queluzite_fox9e_tap",         label:"Queluzite Fox Tap"'
A1_NEW = (
    '  { id:"raspite_fox9e_tap",          label:"Raspite Fox Tap",         desc:"Tap Raspite Fox target",             icon:"🌸", xp:62 },\n'
    '  { id:"raspite_fox9e_peak",         label:"Raspite Fox Peak",        desc:"Reach peak with Raspite Fox",        icon:"🌸", xp:124 },\n'
    '  { id:"quenstedtite_orb9e_tap",     label:"Quenstedtite Orb Tap",   desc:"Tap Quenstedtite Orb target",        icon:"🍊", xp:62 },\n'
    '  { id:"quenstedtite_orb9e_peak",    label:"Quenstedtite Orb Peak",  desc:"Reach peak with Quenstedtite Orb",   icon:"🍊", xp:124 },\n'
    '  { id:"ultra_glow44_use",           label:"Ultra Glow",              desc:"Trigger ULTRA_GLOW44 power-up",      icon:"⚡", xp:62 },\n'
    '  { id:"ultra_glow44_max",           label:"Ultra Glow Max",          desc:"Trigger ULTRA_GLOW44 at max streak", icon:"⚡", xp:124 },\n'
    '  { id:"hyper_glow44_use",           label:"Hyper Glow",              desc:"Trigger HYPER_GLOW44 power-up",      icon:"🔥", xp:62 },\n'
    '  { id:"hyper_glow44_max",           label:"Hyper Glow Max",          desc:"Trigger HYPER_GLOW44 at max streak", icon:"🔥", xp:124 },\n'
    '  { id:"queluzite_fox9e_tap",         label:"Queluzite Fox Tap"'
)
replace_once(A1_OLD, A1_NEW, "Step1-achievements")

# Step 2
A2_OLD = '"CROWN_GLOW44","PRIME_GLOW44"'
A2_NEW = f'"{PW1}","{PW2}","CROWN_GLOW44","PRIME_GLOW44"'
replace_once(A2_OLD, A2_NEW, "Step2-pw-list")

# Step 3
A3_OLD = '  } else if(ptype==="CROWN_GLOW44"){'
A3_NEW = (
    f'  }} else if(ptype==="{PW1}"){{' + '\n'
    f'        gs.score+=({PW1_SC}+gs.streak*4);addPopup("+{PW1_SC} {PW1_ICON}",cx,cy,"{PW1_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW1_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("ultra_glow44_use");if(gs.streak>=30)unlock("ultra_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    f'  }} else if(ptype==="{PW2}"){{' + '\n'
    f'        gs.score+=({PW2_SC}+gs.streak*4);addPopup("+{PW2_SC} {PW2_ICON}",cx,cy,"{PW2_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW2_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("hyper_glow44_use");if(gs.streak>=30)unlock("hyper_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    '  } else if(ptype==="CROWN_GLOW44"){'
)
replace_once(A3_OLD, A3_NEW, "Step3-pw-handler")

# Step 4
A4_OLD = '  // CROWN_GLOW44 — +2664 crown glow bonus'
A4_NEW = (
    f'  // {PW1} — +{PW1_SC} ultra glow bonus\n'
    f'        // {PW2} — +{PW2_SC} hyper glow bonus\n'
    '  // CROWN_GLOW44 — +2664 crown glow bonus'
)
replace_once(A4_OLD, A4_NEW, "Step4-pw-comment")

# Step 5
A5_OLD = 'function drawQueluziteFox9e('
A5_NEW = (
    f'function drawRaspiteFox9e(ctx,r,ts,sp){{\n'
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
    f'function drawQuenstedtiteOrb9e(ctx,r,ts,tp){{\n'
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
    'function drawQueluziteFox9e('
)
replace_once(A5_OLD, A5_NEW, "Step5-draw-functions")

# Step 6
A6_OLD = '  else if(t.type==="queluzite_fox9e"){'
A6_NEW = (
    f'  else if(t.type==="{FOX_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp801a=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawRaspiteFox9e(ctx,t.radius,ts,sp801a);ctx.restore();\n'
    f'  }}\n'
    f'  else if(t.type==="{ORB_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp801b=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawQuenstedtiteOrb9e(ctx,t.radius,ts,tp801b);ctx.restore();\n'
    f'  }}\n'
    '  else if(t.type==="queluzite_fox9e"){'
)
replace_once(A6_OLD, A6_NEW, "Step6-dispatch")

# Step 7
A7_OLD = '    if(hit.type==="queluzite_fox9e"){'
A7_NEW = (
    f'    if(hit.type==="{FOX_TYPE}"){{\n'
    f'          const sp801c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts801a=Math.round({FOX_SC}*(1+sp801c));\n'
    f'          gs.score+=pts801a;gs.streak++;addPopup("+"+pts801a+(sp801c>0.88?" {FOX_PEAK} PEAK!":""),hit.x,hit.y,"{FOX_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{FOX_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(sp801c>0.88){{sfx("legendary");unlock("{FOX_TYPE}_peak");}}else unlock("{FOX_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="{ORB_TYPE}"){{\n'
    f'          const tp801d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts801b=Math.round({ORB_SC}*(1+tp801d));\n'
    f'          gs.score+=pts801b;gs.streak++;addPopup("+"+pts801b+(tp801d>0.88?" {ORB_PEAK} PEAK!":""),hit.x,hit.y,"{ORB_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{ORB_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(tp801d>0.88){{sfx("legendary");unlock("{ORB_TYPE}_peak");}}else unlock("{ORB_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="queluzite_fox9e"){{'
)
replace_once(A7_OLD, A7_NEW, "Step7-handlers")

# Step 8
A8_OLD = ('      type="queluzite_fox9e";color="#0e7490";glow="#ecfeff";\n'
          '    } else if('+COND100F+'){\n'
          '      type="ransomite_orb9e"')
A8_NEW = (
    f'      type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="queluzite_fox9e";color="#0e7490";glow="#ecfeff";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="ransomite_orb9e"'
)
replace_once(A8_OLD, A8_NEW, "Step8-spawn")

# Step 9
A9_OLD = 'type==="queluzite_fox9e"?BASE_R*2.45:'
A9_NEW = (
    f'type==="{FOX_TYPE}"?{FOX_R}:'
    f'type==="{ORB_TYPE}"?{ORB_R}:'
    'type==="queluzite_fox9e"?BASE_R*2.45:'
)
replace_once(A9_OLD, A9_NEW, "Step9-radius")

# Step 10 (cnt==2)
A10_OLD = 'CROWN_GLOW44:"👑✨"'
A10_NEW = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",CROWN_GLOW44:"👑✨"'
cnt10 = data.count(A10_OLD)
if cnt10 != 2:
    print(f"ERROR Step10: expected 2, found {cnt10}")
    sys.exit(1)
data = data.replace(A10_OLD, A10_NEW)
print("OK Step10-icons")

open(SRC, "w", encoding="utf-8").write(data)
print(f"Batch 801 done! +{len(data)-orig_len} bytes")
