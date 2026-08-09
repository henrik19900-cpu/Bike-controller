# CLAUDE.md — NexusTap Game

This file provides everything an AI assistant needs to work effectively in this repository.

---

## Project Overview

**NexusTap** is a mobile-first tap-reflex game built as a single-page React application and packaged as an Android app via Capacitor. The entire game lives in one large component file (`src/NexusTap.jsx`, ~4 200+ lines). There is no backend — all state is persisted to `localStorage`.

- **App ID:** `com.nexustap.game`
- **Platform target:** Android (via Capacitor), also runs in any modern browser
- **Tech stack:** React 19, Vite 8, Tailwind CSS 3, Capacitor 8
- **Build output:** `dist/` (web) → synced to Android via `npx cap sync android`

---

## Development Commands

```bash
npm run dev        # Vite dev server (hot reload in browser)
npm run build      # Production build to dist/
npm run android    # build + cap sync (prepares Android project)
```

> There is no test suite. Manual testing in the browser dev server is the workflow.

---

## Repository Layout

```
Bike-controller/
├── src/
│   ├── NexusTap.jsx   # ENTIRE game — ~4 200 lines, single file
│   ├── main.jsx       # React root mount
│   └── index.css      # Minimal global CSS (fonts, reset)
├── index.html          # Vite entry point
├── android/            # Capacitor Android project (generated)
├── dist/               # Vite build output (generated)
├── capacitor.config.json
├── vite.config.js
├── tailwind.config.js
└── package.json
```

**All game logic, UI, audio, drawing, and data lives in `src/NexusTap.jsx`.**

---

## Architecture of NexusTap.jsx

The file has a clear top-to-bottom structure:

### 1. Top-Level Constants (lines ~1–480)

All defined *outside* the React component, so they are module-level singletons:

| Constant | Description |
|---|---|
| `WORLDS` | 10 world objects — id, name, emoji, color, bg, grid, accent, atmos |
| `MASCOTS` | 10 mascot companions with id, name, color, rarity, emoji states (`e`), dance key, speeches, unlockCond |
| `MASCOT_AUDIO` | Per-mascot combo note base frequency + oscillator wave type |
| `MASCOT_HAPTIC` | Per-mascot vibration pattern array (ms) for each tap |
| `MASCOT_ACCESSORIES` | 6 cosmetic accessories (hat, crown, glasses, halo, bow, star) with cost |
| `LEVEL_NAMES` | 100 level names (10 per world) |
| `MILESTONE_MODS` | Special level modifiers at levels 10, 20, 30 … 100 |
| `MYSTERY_PRIZES` | 6 weighted mystery-box prize types |
| `RARITY` | 5 rarity tiers — COMMON/UNCOMMON/RARE/EPIC/LEGENDARY with chance, color, glow, mult, size |
| `THEMES` | 6 visual themes (neon, cyber, inferno, matrix, abyss, rose) |
| `COMBO_LABELS` | Milestone combo label messages (5×, 10×, 20×, 35×, 50×) |
| `ACHIEVEMENTS` | 17 achievement definitions with id, label, desc, icon, xp |
| `MISSION_TEMPLATES` | 9 daily mission types (tap_30, rare_5, combo_15, boss_1, fever_2, perfect_5, levels_3, powerup_3, score_500) |
| `SHOP_ITEMS` | 4 purchasable boosts (extra_life 60🪙, head_start 80🪙, shield_start 100🪙, power_pack 120🪙) |
| `MAIN_STORY` | Intro story title + panels |
| `WORLD_STORIES` | Per-world story panels + boss intro + victory text |

**Helper functions also at module level:**

- `getLevelConfig(n)` — generates a full level config object for level n (1–100)
- `getDailyMissions()` — returns 3 deterministic daily missions from MISSION_TEMPLATES (seeded by date)
- `seededRng(seed)` — deterministic pseudo-random number generator
- `getTodayKey()` — returns `"YYYY-M-D"` string
- `getWeekKey()` — returns `"YYYY-Wnn"` string
- `getDailyChallengeLevel()` — returns a seeded level number (5–22) for today's daily challenge
- `getWeeklyChallengeLevel()` — returns a seeded level number (20–39) for this week's weekly challenge
- `createAudio()` — factory that returns the audio engine object (Web Audio API)
- `drawBg()`, `drawBgParticles()`, `drawRipples()`, `drawVignette()`, `drawWorldForeground()` — canvas drawing helpers
- `drawTarget()`, `drawBomb()`, `drawPowerup()`, `drawBoss()`, `drawTreasure()`, `drawMystery()` — target-specific canvas drawers
- `loadSave()` — reads from localStorage key `"nexustap_v5"`, merges with DEFAULT_SAVE
- `vibrate(pattern)` — wraps `navigator.vibrate` safely

### 2. Helper Components (lines ~1 680–1 710)

- **`NeonButton`** — animated press-scale button with shine effect, used throughout all screens. Props: `{children, onClick, style, className, disabled}`.

### 3. The `NexusTap` Component (lines ~1 710–4 225)

One massive default-export React functional component. It uses no Redux, no router, no external state library.

---

## State Management

### Persistent Save (`saveRef`)

All game progress is stored in `saveRef.current` (a `useRef`) and synced to `localStorage`.

**Key:** `"nexustap_v5"`

**Shape (`DEFAULT_SAVE`):**
```js
{
  highScore: 0,
  xp: 0,
  bestStreak: 0,
  coins: 0,
  totalCoins: 0,
  unlockedAchievements: [],
  themeId: "neon",
  soundEnabled: true,
  scores: [],
  lastLoginDate: null,
  loginStreak: 0,
  missionDate: null,
  missionProgress: {},
  missionCompleted: false,
  levelStars: {},          // { levelId: 1|2|3 }
  unlockedLevel: 1,
  seenWorldStories: [],
  seenMainStory: false,
  seenBossIntros: [],
  seenTutorial: false,
  lastSpinDate: null,
  mascotId: "dragon",
  unlockedMascots: ["dragon", "fox"],
  // Added in later iterations:
  consecutiveWins: 0,      // hot-streak tracking
  hotStreakActive: false,
  mascotScores: {},        // { mascotId: bestScore }
  mascotAccessories: {},   // { mascotId: accessoryId }
  levelScores: {},         // { levelId: bestScore }
  weeklyChallenge: null,   // { weekKey, completed, score }
  dailyChallengeCompleted: null,
  ghostTaps: {},           // { levelId: [{x,y,pts}] }
}
```

**Save helpers:**
- `flushSave()` — immediate `localStorage.setItem` (use after critical changes)
- `debounceSave()` — debounced 1 800 ms save (use during gameplay)

### In-Game State (`gsRef`)

The live game state during play is in `gsRef.current` (a `useRef`, not React state — avoids renders in the RAF loop).

**Shape (set in `startGame`):**
```js
{
  score: number,
  lives: number,
  streak: number,
  feverActive: boolean,
  feverTimeLeft: number,
  startTime: number,       // Date.now()
  bonusRoundActive: boolean,
  missesThisLevel: number, // for Flawless Run detection
  miniBossSpawned: boolean,
  tapPositions: [],        // [{x,y,pts}] for ghost run recording
  sessionStats: {
    tapsTotal, rareHits, bestCombo, score,
    feverCount, powerupCollected, bossKills, perfectTaps
  }
}
```

### React State (`useState`)

Used only for UI rendering triggers. Key ones:

| State | Purpose |
|---|---|
| `screen` | Current screen name |
| `hud` | `{score, lives, streak}` — updated from gsRef on a 60 fps tick |
| `theme` | Active visual theme object |
| `paused` | Pause overlay |
| `levelCompleteData` | Data bundle for level complete screen |
| `gameOverData` | Data bundle for game over screen |
| `mascotMood` | `"idle"/"happy"/"excited"/"fire"/"fever"/"sad"/"victory"` |
| `notif` | Transient toast notification text |
| `streakBurst` | `{label, color}` — combo milestone burst overlay |
| `chainFlash` | `{label, at}` — rapid combo chain flash overlay |
| `flawlessRun` | boolean — displayed on level complete |
| `hotStreak` | boolean — hot streak banner visibility |
| `dailyBonusData` | object — daily login bonus overlay data |
| `feverBorder` | boolean — glowing fever border effect |
| `epicFlash` / `legendaryFlash` | boolean — rarity flash overlays |
| `screenShake` | boolean — CSS transform shake |
| `bonusRound` | boolean — bonus round active |
| `rescueSecondsLeft` | number — rescue gamble countdown |

### Key Refs

| Ref | Purpose |
|---|---|
| `canvasRef` | The `<canvas>` element |
| `gsRef` | Live game state (see above) |
| `targetsRef` | Array of active target objects on screen |
| `particlesRef` | Array of visual particle objects |
| `bgPartsRef` | Array of background floating particles |
| `ripplesRef` | Array of tap ripple effects |
| `activePwrRef` | Array of active power-up effects |
| `levelCfgRef` | Current level config object |
| `pausedRef` | Pause flag (read in RAF without stale closure) |
| `rafRef` | `requestAnimationFrame` handle |
| `lastTickRef` | Previous frame timestamp for delta-time |
| `chainTimesRef` | Array of recent tap timestamps (combo chain detection) |

---

## Screens

Screens are simple conditional renders in the final `return`. Add a new screen by:
1. Creating a `renderMyScreen()` function inside the component
2. Adding `{screen==="myscreen" && renderMyScreen()}` to the final JSX return
3. Navigating with `setScreen("myscreen")`

**Existing screens:**

| Screen key | Render function |
|---|---|
| `"menu"` | `renderMenu()` |
| `"levelmap"` | `renderLevelMap()` |
| `"shop"` | `renderShop()` |
| `"playing"` | `renderPlaying()` |
| `"levelcomplete"` | `renderLevelComplete()` |
| `"gameover"` | `renderGameOver()` |
| `"missions"` | `renderMissions()` |
| `"achievements"` | `renderAchievements()` |
| `"leaderboard"` | `renderLeaderboard()` |
| `"settings"` | `renderSettings()` |
| `"mascotcollection"` | `renderMascotCollection()` |
| `"spinwheel"` | `renderSpinWheel()` |

Overlay-style screens (rendered regardless of `screen`):
- `storyData && renderWorldStory()` — world story panels
- `tutStep !== null && renderTutorial()` — tutorial overlay

---

## Game Loop

The RAF loop is `gameLoopFn` (a `useCallback`). Called via `rafRef.current = requestAnimationFrame(gameLoopFn)`.

**Draw order each frame:**
1. `drawBg()` — clears canvas, draws grid
2. `drawBgParticles()` — floating world-specific bg particles (accepts `speedMult` for fever/bonus dynamic speed)
3. `drawRipples()` — tap ripple rings
4. Particle physics update + draw (sparks, dots, popups, shockwaves, trail particles)
5. Ghost run dots (previous best taps, faint translucent)
6. Mini-boss force-spawn check (milestone levels)
7. Target spawn timer
8. Target update + draw (expiry, movement, drawing)
9. `drawWorldForeground()` — world silhouettes on top
10. `drawVignette()` — depth vignette

**HUD** is updated in the RAF loop by calling `setHud({score, lives, streak})` on a separate ref-counted cycle to avoid 60 fps React renders.

---

## Target System

### Target Object Shape
```js
{
  id: string,           // random hex
  type: "normal"|"bomb"|"powerup"|"boss"|"treasure"|"mystery"|"miniboss",
  x, y: number,         // canvas position
  radius: number,       // hit radius
  color, glow: string,  // CSS color strings
  rarity: RARITY object,
  lifetime: number,     // ms alive
  spawnedAt: number,    // Date.now()
  born: number,         // performance.now()
  moving: boolean,
  ghost: boolean,       // semi-transparent shrinking target
  vx, vy: number,       // velocity for moving targets
  trail: [...],         // position history for motion trail
  hitsLeft: number,     // boss/miniboss hit points
  maxHits: number,
  dying: number|null,   // performance.now() when hit (squish animation)
}
```

### Adding a New Target Type
1. Add a spawn branch in `spawnTarget()` to set `type`, `color`, `glow`, `radius`, etc.
2. Add a draw branch in `drawTarget()` or create a dedicated `drawMyType(ctx, t, ts)` function
3. Add a handler in `handleTap()` for when this target type is tapped

---

## Audio Engine

`createAudio()` returns an object of named sound functions. Accessed via `audioRef.current`.

**Playing a sound:**
```js
sfx("tap");                    // simple sound
sfx("comboNote", gs.streak);   // parameterized
sfx("mascotNote", streak, base, wave);  // per-mascot combo note
```

**Key sounds:** `tap`, `miss`, `comboNote`, `mascotNote`, `chainBonus`, `flawless`, `hotStreak`, `bossKill`, `feverStart`, `levelComplete`, `gameOver`, `legendary`, `epic`, `rare`, `powerUp`, `coin`, `starEarn`, `unlock`, `lucky`, `nearMiss`, `treasure`, `jackpot`

**Background music:** `sfx("startBgMusic", worldId)` / `sfx("stopBgMusic")` — plays a looping arpeggio per world.

The audio context is lazily created on first interaction (browser autoplay policy).

---

## Visual System

### Canvas (targets, particles, background)
- Drawn each frame by `gameLoopFn` using standard 2D canvas API
- `canvasRef` is a `<canvas>` element positioned `absolute inset-0 z-0 pointer-events-none`
- Input is handled by an overlay `<div>` on top of the canvas

### CSS / Tailwind
- Tailwind utility classes for all UI screens
- Inline styles for dynamic colors (world color, theme accent)
- All `@keyframes` animations are defined as a single `<style>` block inside the component's JSX return (bottom of file)
- Font: `'Exo 2', 'Rajdhani', 'Segoe UI', system-ui, sans-serif`

### Key CSS Animation Names
`feverPulse`, `epicFlash`, `legendaryRainbow`, `comboAnnounce`, `countAnim`, `levelPulse`, `starPop`, `waveIn`, `shimmer`, `floatGlow`, `bannerSlide`, `victoryBurst`, `coinFall`, `scorePulse`, `heartbeat`, `perfectPop`, `notifSlide`, `sparkleFloat`, `mascotIdle`, `mascotBounce`, `mascotSad`, `mascotShake`, `slotSpin`, `speechBubble`, `rescuePulse`, `danceDragon`, `danceFox`, `danceCat`, `danceFrog`, `danceLion`, `dancePanda`, `dancePenguin`, `danceOctopus`, `danceButterfly`, `danceUnicorn`, `streakBurstAnim`, `chainFlashAnim`, `flawlessBurst`, `hotStreakPulse`

---

## Levels

- **100 levels** across 10 worlds (10 per world)
- Generated dynamically by `getLevelConfig(n)`:
  - `scoreGoal = floor(200 + n×100 + n²×0.6)`
  - `lives`: 5 (levels 1–10), 4 (11–30), 3 (31–70), 2 (71–100)
  - Boss levels: every 10th level (`isBoss = n % 10 === 0`)
  - Milestone modifiers at levels 10, 20, 30 … 100 (from `MILESTONE_MODS`)
  - Spawn rate, target lifetime, moving/ghost/bomb rates all scale with `n`
- **Daily Challenge:** seeded level (5–22), changes daily, 2× coin reward
- **Weekly Challenge:** seeded level (20–39), resets Monday, 3× coin reward + exclusive unlock

---

## Mascots

10 mascots, each with:
- **Rarity:** `starter` (dragon, fox — always unlocked), `common`, `rare`, `epic`, `legendary`
- **Unlock conditions:** level reached, streak achieved, stars collected, or coins spent
- **Emoji states:** `idle`, `happy`, `excited`, `fire`, `fever`, `sad`, `victory`, `scared`
- **Dance animation:** CSS keyframe name in `dance` field
- **Speeches:** object keyed by mood (`idle`, `happy`, `streak`, `fever`, `close`, `miss`, `victory`, `bonus`, `mystery`)
- **Audio profile** (in `MASCOT_AUDIO`): `{base: Hz, wave: "sine"|"square"|"sawtooth"|"triangle"}`
- **Haptic profile** (in `MASCOT_HAPTIC`): vibration pattern array (ms)
- **Accessories** (in `saveRef.current.mascotAccessories`): one optional cosmetic per mascot

**Rivalry scores:** `saveRef.current.mascotScores[mascotId]` — per-mascot personal best score.

---

## Achievements

17 achievements. To add a new one:
1. Add an entry to the `ACHIEVEMENTS` array: `{id, label, desc, icon, xp}`
2. Call `unlock("your_id")` at the appropriate game event

---

## Missions

- 3 missions selected daily (deterministic by date from `MISSION_TEMPLATES`)
- Progress tracked in `saveRef.current.missionProgress`
- Updated via `updateMissions(sessionStats)` called after each tap
- Completing all 3 awards 200 XP and triggers `unlock("missions_all")`

---

## Adding Features — Conventions

### New game mechanic (affects score / lives)
1. Add any new save fields to `DEFAULT_SAVE` and document them above
2. Add any new `gsRef` fields in `startGame()`
3. Hook into `handleTap()` (normal hit section, lines ~2 125–2 210) for per-tap logic
4. Hook into `endLevel(won)` for end-of-level logic

### New screen
1. Write `renderMyScreen()` function (follow existing pattern — full-height flex column, uses `theme` and world colors)
2. Add `{screen==="myscreen" && renderMyScreen()}` in the final JSX return
3. Add a `NeonButton` navigation entry where appropriate

### New target type
1. Add to `spawnTarget()` with a type string
2. Add `drawMyType(ctx, t, ts)` function at module level
3. Handle tap in `handleTap()` before the `// NORMAL` comment

### New shop item
Add to `SHOP_ITEMS` array. Handle the item id in `startGame()` where `shopCart` is processed.

### New achievement
Add to `ACHIEVEMENTS` array, then call `unlock("id")` at the right moment.

### New animation
Add `@keyframes myAnim {...}` inside the `<style>` block near the bottom of the JSX return.

---

## Common Pitfalls

- **Never call `setState` inside the RAF loop** for performance-critical things — update `gsRef` instead and let `setHud` handle display
- **`saveRef.current` is mutable** — mutate it directly, then call `flushSave()` or `debounceSave()`
- **`pausedRef.current`** must be checked at the top of `handleTap` and `gameLoopFn`; never use `paused` state inside those
- **Touch events need `e.preventDefault()`** to avoid scroll/zoom conflicts on mobile
- **`vibrate()`** and **`sfx()`** are always safe to call — they handle missing APIs gracefully
- **Canvas coordinates** are raw pixel values; the canvas CSS size equals the canvas pixel size (set on mount)
- **`drawBgParticles` mutates `bgPartsRef.current` positions** — it both updates and draws in one pass
- **localStorage key** is `"nexustap_v5"` — changing this resets all player progress

---

## Build & Deploy

```bash
npm run build          # outputs to dist/
npm run android        # build + npx cap sync android
# Then open android/ in Android Studio to build the APK
```

The `dist/` directory is git-ignored and rebuilt each time.

Two GitHub Actions workflows exist:

- `.github/workflows/build-android.yml` — debug APK on every push. For device
  testing only; Play rejects debuggable, debug-signed uploads.
- `.github/workflows/release-android.yml` — signed release `.aab` for Play, run
  manually or by pushing a `v*` tag. Needs the four `ANDROID_*` repository
  secrets.

Release signing is configured in `android/app/build.gradle` and reads either
`android/keystore.properties` (git-ignored) or `ANDROID_KEYSTORE_FILE` /
`ANDROID_KEYSTORE_PASSWORD` / `ANDROID_KEY_ALIAS` / `ANDROID_KEY_PASSWORD` from
the environment. `versionCode` / `versionName` come from the `appVersionCode` /
`appVersionName` Gradle properties so each upload gets a fresh version code.

See `RELEASE.md` for the full Play release procedure.

The active development branch is `claude/mobile-game-react-Y66kc`.
