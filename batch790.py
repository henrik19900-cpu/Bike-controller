#!/usr/bin/env python3
"""Batch 790 — DRIFT_GLOW44+EDDY_GLOW44 + NavajoiteFox9e+NeptuniteOrb9e + 8 achievements"""
import re, sys

SRC = "src/NexusTap.jsx"
data = open(SRC, encoding="utf-8").read()
orig_len = len(data)

COND100F = ('(cfg.id||0)>=100&&Math.random()<0.003&&!gs.bonusRoundActive'
            '&&luckyRef.current!=="active"&&!modifier?.type?.includes("boss")'
            '&&!modifier?.type?.includes("final")')

OSC   = "0.4409"
SW    = "2374"

# Fox: navajoite
FOX_TYPE   = "navajoite_fox9e"
FOX_COLOR  = "#e11d48"
FOX_GLOW   = "#fff1f2"
FOX_LIGHT  = "#ffe4e6"
FOX_MID    = "#fb7185"
FOX_DARK   = "#9f1239"
FOX_RGB    = "251,113,133"
FOX_PEAK   = "🌹"
FOX_SC     = "564"
FOX_R      = "BASE_R*2.35"

# Orb: neptunite
ORB_TYPE   = "neptunite_orb9e"
ORB_COLOR  = "#0f766e"
ORB_GLOW   = "#ccfbf1"
ORB_LIGHT  = "#ccfbf1"
ORB_MID    = "#2dd4bf"
ORB_DARK   = "#134e4a"
ORB_RGB    = "45,212,191"
ORB_PEAK   = "🌊"
ORB_SC     = "559"
ORB_R      = "BASE_R*2.34"

# Power-ups
PW1        = "DRIFT_GLOW44"
PW1_SC     = "2624"
PW1_SHOCK  = "#a16207"
PW1_ICON   = "🌀✨"

PW2        = "EDDY_GLOW44"
PW2_SC     = "2626"
PW2_SHOCK  = "#0369a1"
PW2_ICON   = "🔄✨"

def replace_once(old, new, label):
    global data
    cnt = data.count(old)
    if cnt != 1:
        print(f"ERROR {label}: expected 1 occurrence, found {cnt}")
        sys.exit(1)
    data = data.replace(old, new, 1)
    print(f"OK {label}")

# ── STEP 1 — 8 achievements ────────────────────────────────────────────────
A1_OLD = '  { id:"natrophilite_fox9e_tap"'
A1_NEW = (
    '  { id:"navajoite_fox9e_tap",    label:"Navajoite Fox Tap",      desc:"Tap Navajoite Fox target",             icon:"🌹", xp:62 },\n'
    '  { id:"navajoite_fox9e_peak",   label:"Navajoite Fox Peak",     desc:"Reach peak with Navajoite Fox",        icon:"🌹", xp:124 },\n'
    '  { id:"neptunite_orb9e_tap",    label:"Neptunite Orb Tap",      desc:"Tap Neptunite Orb target",             icon:"🌊", xp:62 },\n'
    '  { id:"neptunite_orb9e_peak",   label:"Neptunite Orb Peak",     desc:"Reach peak with Neptunite Orb",        icon:"🌊", xp:124 },\n'
    '  { id:"drift_glow44_use",       label:"Drift Glow",             desc:"Trigger DRIFT_GLOW44 power-up",        icon:"🌀", xp:62 },\n'
    '  { id:"drift_glow44_max",       label:"Drift Glow Max",         desc:"Trigger DRIFT_GLOW44 at max streak",   icon:"🌀", xp:124 },\n'
    '  { id:"eddy_glow44_use",        label:"Eddy Glow",              desc:"Trigger EDDY_GLOW44 power-up",         icon:"🔄", xp:62 },\n'
    '  { id:"eddy_glow44_max",        label:"Eddy Glow Max",          desc:"Trigger EDDY_GLOW44 at max streak",    icon:"🔄", xp:124 },\n'
    '  { id:"natrophilite_fox9e_tap"'
)
replace_once(A1_OLD, A1_NEW, "Step1-achievements")

# ── STEP 2 — GLOW44 power-up name list ────────────────────────────────────
A2_OLD = '"BANK_GLOW44","BIGHT_GLOW44"'
A2_NEW = f'"{PW1}","{PW2}","BANK_GLOW44","BIGHT_GLOW44"'
replace_once(A2_OLD, A2_NEW, "Step2-pw-list")

# ── STEP 3 — ptype handler ────────────────────────────────────────────────
A3_OLD = '  } else if(ptype==="BANK_GLOW44"){'
A3_NEW = (
    f'  }} else if(ptype==="{PW1}"){{' + '\n'
    f'        gs.score+=({PW1_SC}+gs.streak*4);addPopup("+{PW1_SC} {PW1_ICON}",cx,cy,"{PW1_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW1_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("drift_glow44_use");if(gs.streak>=30)unlock("drift_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    f'  }} else if(ptype==="{PW2}"){{' + '\n'
    f'        gs.score+=({PW2_SC}+gs.streak*4);addPopup("+{PW2_SC} {PW2_ICON}",cx,cy,"{PW2_SHOCK}");' + '\n'
    f'        spawnShockwave(cx,cy,"{PW2_SHOCK}");sfx("powerUp");' + '\n'
    f'        unlock("eddy_glow44_use");if(gs.streak>=30)unlock("eddy_glow44_max");' + '\n'
    f'        debounceSave();return;' + '\n'
    '  } else if(ptype==="BANK_GLOW44"){'
)
replace_once(A3_OLD, A3_NEW, "Step3-pw-handler")

# ── STEP 4 — inline comment block ────────────────────────────────────────
A4_OLD = '  // BANK_GLOW44 — +2620 bank glow bonus'
A4_NEW = (
    f'  // {PW1} — +{PW1_SC} drift glow bonus\n'
    f'        // {PW2} — +{PW2_SC} eddy glow bonus\n'
    '  // BANK_GLOW44 — +2620 bank glow bonus'
)
replace_once(A4_OLD, A4_NEW, "Step4-pw-comment")

# ── STEP 5 — draw functions ───────────────────────────────────────────────
A5_OLD = 'function drawNatrophiliteFox9e('
A5_NEW = (
    f'function drawNavajoiteFox9e(ctx,r,ts,sp){{\n'
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
    f'function drawNeptuniteOrb9e(ctx,r,ts,tp){{\n'
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
    'function drawNatrophiliteFox9e('
)
replace_once(A5_OLD, A5_NEW, "Step5-draw-functions")

# ── STEP 6 — draw dispatch ────────────────────────────────────────────────
A6_OLD = '  else if(t.type==="natrophilite_fox9e"){'
A6_NEW = (
    f'  else if(t.type==="{FOX_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const sp790a=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawNavajoiteFox9e(ctx,t.radius,ts,sp790a);ctx.restore();\n'
    f'  }}\n'
    f'  else if(t.type==="{ORB_TYPE}"){{\n'
    f'    ctx.save();ctx.translate(t.x,t.y);\n'
    f'    const tp790b=Math.min(1,(ts-t.born)/{SW});\n'
    f'    drawNeptuniteOrb9e(ctx,t.radius,ts,tp790b);ctx.restore();\n'
    f'  }}\n'
    '  else if(t.type==="natrophilite_fox9e"){'
)
replace_once(A6_OLD, A6_NEW, "Step6-dispatch")

# ── STEP 7 — tap handlers ─────────────────────────────────────────────────
A7_OLD = '    if(hit.type==="natrophilite_fox9e"){'
A7_NEW = (
    f'    if(hit.type==="{FOX_TYPE}"){{\n'
    f'          const sp790c=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts790a=Math.round({FOX_SC}*(1+sp790c));\n'
    f'          gs.score+=pts790a;gs.streak++;addPopup("+"+pts790a+(sp790c>0.88?" {FOX_PEAK} PEAK!":""),hit.x,hit.y,"{FOX_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{FOX_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(sp790c>0.88){{sfx("legendary");unlock("{FOX_TYPE}_peak");}}else unlock("{FOX_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="{ORB_TYPE}"){{\n'
    f'          const tp790d=Math.min(1,(performance.now()-hit.born)/{SW});\n'
    f'          const pts790b=Math.round({ORB_SC}*(1+tp790d));\n'
    f'          gs.score+=pts790b;gs.streak++;addPopup("+"+pts790b+(tp790d>0.88?" {ORB_PEAK} PEAK!":""),hit.x,hit.y,"{ORB_GLOW}");\n'
    f'          spawnShockwave(hit.x,hit.y,"{ORB_COLOR}");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n'
    f'          sfx("tap");if(tp790d>0.88){{sfx("legendary");unlock("{ORB_TYPE}_peak");}}else unlock("{ORB_TYPE}_tap");\n'
    f'          updateMissions(gs.sessionStats);debounceSave();\n'
    f'        }} else if(hit.type==="natrophilite_fox9e"){{'
)
replace_once(A7_OLD, A7_NEW, "Step7-handlers")

# ── STEP 8 — spawn entries ────────────────────────────────────────────────
A8_OLD = ('      type="natrophilite_fox9e";color="#06b6d4";glow="#cffafe";\n'
          '    } else if('+COND100F+'){\n'
          '      type="naujakasite_orb9e"')
A8_NEW = (
    f'      type="{FOX_TYPE}";color="{FOX_COLOR}";glow="{FOX_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="{ORB_TYPE}";color="{ORB_COLOR}";glow="{ORB_GLOW}";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="natrophilite_fox9e";color="#06b6d4";glow="#cffafe";\n'
    f'    }} else if({COND100F}){{\n'
    f'      type="naujakasite_orb9e"'
)
replace_once(A8_OLD, A8_NEW, "Step8-spawn")

# ── STEP 9 — radius chain ─────────────────────────────────────────────────
A9_OLD = 'type==="natrophilite_fox9e"?BASE_R*2.34:'
A9_NEW = (
    f'type==="{FOX_TYPE}"?{FOX_R}:'
    f'type==="{ORB_TYPE}"?{ORB_R}:'
    'type==="natrophilite_fox9e"?BASE_R*2.34:'
)
replace_once(A9_OLD, A9_NEW, "Step9-radius")

# ── STEP 10 — icon map (replace_all, expect cnt==2) ───────────────────────
A10_OLD = 'BANK_GLOW44:"💰✨"'
A10_NEW = f'{PW1}:"{PW1_ICON}",{PW2}:"{PW2_ICON}",BANK_GLOW44:"💰✨"'
cnt10 = data.count(A10_OLD)
if cnt10 != 2:
    print(f"ERROR Step10: expected 2 occurrences, found {cnt10}")
    sys.exit(1)
data = data.replace(A10_OLD, A10_NEW)
print("OK Step10-icons")

# ── Write ──────────────────────────────────────────────────────────────────
open(SRC, "w", encoding="utf-8").write(data)
print(f"Batch 790 done! +{len(data)-orig_len} bytes")
