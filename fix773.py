#!/usr/bin/env python3
"""Fix batch 773: rename new jarosite_fox9e additions to jungeite_fox9e"""
F = "src/NexusTap.jsx"
src = open(F, encoding="utf-8").read()
orig_len = len(src)

# Fix step 1 - new achievement (different label format than old)
A1_OLD = '  { id:"jarosite_fox9e_tap", label:"Jarosite Fox Tap", desc:"Tap Jarosite Fox", icon:"🦊", xp:62 },\n  { id:"jarosite_fox9e_peak", label:"Jarosite Fox Peak", desc:"Tap Jarosite Fox at peak", icon:"🌻", xp:88 },'
A1_NEW = '  { id:"jungeite_fox9e_tap", label:"Jungeite Fox Tap", desc:"Tap Jungeite Fox", icon:"🦊", xp:62 },\n  { id:"jungeite_fox9e_peak", label:"Jungeite Fox Peak", desc:"Tap Jungeite Fox at peak", icon:"🌻", xp:88 },'
assert src.count(A1_OLD) == 1, f"A1 count={src.count(A1_OLD)}"
src = src.replace(A1_OLD, A1_NEW, 1)

# Fix step 5 - new draw function (uses 0.4341 OSC)
A5_OLD = 'function drawJarositeFox9e(ctx,r,ts,sp){\n  const bob=Math.sin(ts*0.4341)'
A5_NEW = 'function drawJungeite773Fox9e(ctx,r,ts,sp){\n  const bob=Math.sin(ts*0.4341)'
assert src.count(A5_OLD) == 1, f"A5 count={src.count(A5_OLD)}"
src = src.replace(A5_OLD, A5_NEW, 1)

# Fix step 6 - new dispatch (uses sp773a)
A6_OLD = '  else if(t.type==="jarosite_fox9e"){\n    ctx.save();ctx.translate(t.x,t.y);\n    const sp773a=Math.min'
A6_NEW = '  else if(t.type==="jungeite_fox9e"){\n    ctx.save();ctx.translate(t.x,t.y);\n    const sp773a=Math.min'
assert src.count(A6_OLD) == 1, f"A6 count={src.count(A6_OLD)}"
src = src.replace(A6_OLD, A6_NEW, 1)

# Fix step 6 - draw call in dispatch
A6b_OLD = 'drawJarositeFox9e(ctx,t.radius,ts,sp773a);ctx.restore();\n  }\n  else if(t.type==="jennite_orb9e")'
A6b_NEW = 'drawJungeite773Fox9e(ctx,t.radius,ts,sp773a);ctx.restore();\n  }\n  else if(t.type==="jennite_orb9e")'
assert src.count(A6b_OLD) == 1, f"A6b count={src.count(A6b_OLD)}"
src = src.replace(A6b_OLD, A6b_NEW, 1)

# Fix step 7 - new handler (uses sp773c, pts773a)
A7_OLD = 'if(hit.type==="jarosite_fox9e"){\n          const sp773c'
A7_NEW = 'if(hit.type==="jungeite_fox9e"){\n          const sp773c'
assert src.count(A7_OLD) == 1, f"A7 count={src.count(A7_OLD)}"
src = src.replace(A7_OLD, A7_NEW, 1)

A7b_OLD = 'unlock("jarosite_fox9e_peak");}else unlock("jarosite_fox9e_tap");\n          updateMissions(gs.sessionStats);debounceSave();\n        } else if(hit.type==="jennite_orb9e")'
A7b_NEW = 'unlock("jungeite_fox9e_peak");}else unlock("jungeite_fox9e_tap");\n          updateMissions(gs.sessionStats);debounceSave();\n        } else if(hit.type==="jennite_orb9e")'
assert src.count(A7b_OLD) == 1, f"A7b count={src.count(A7b_OLD)}"
src = src.replace(A7b_OLD, A7b_NEW, 1)

A7c_OLD = 'addPopup("+"+pts773a+(sp773c>0.88?" 🌻 PEAK!":""),hit.x,hit.y,"#fde68a");\n          spawnShockwave(hit.x,hit.y,"#b45309");targetsRef.current=targetsRef.current.filter(x=>x.id!==hit.id);\n          sfx("tap");if(sp773c>0.88){sfx("legendary");unlock("jungeite_fox9e_peak");}else unlock("jungeite_fox9e_tap")'
# Already renamed above, just verify
assert 'unlock("jungeite_fox9e_peak")' in src, "jungeite unlock not found"

# Fix step 8 - new spawnTarget (color="#b45309" is the new one, "#d97706" is old)
A8_OLD = '      type="jarosite_fox9e";color="#b45309";glow="#fde68a";\n    } else if'
A8_NEW = '      type="jungeite_fox9e";color="#b45309";glow="#fde68a";\n    } else if'
assert src.count(A8_OLD) == 1, f"A8 count={src.count(A8_OLD)}"
src = src.replace(A8_OLD, A8_NEW, 1)

# Fix step 9 - radius table (BASE_R*2.18 is new for batch 773)
A9_OLD = 'type==="jarosite_fox9e"?BASE_R*2.18:'
A9_NEW = 'type==="jungeite_fox9e"?BASE_R*2.18:'
assert src.count(A9_OLD) == 1, f"A9 count={src.count(A9_OLD)}"
src = src.replace(A9_OLD, A9_NEW, 1)

open(F, "w", encoding="utf-8").write(src)
print(f"fix773 done! delta={len(src)-orig_len} bytes")
