# Releasing NexusTap to Google Play

## Why the old build could not be published

The repository only ever produced `app-debug.apk` (`./gradlew assembleDebug`).
Google Play rejects that artifact for three independent reasons:

1. **It is debuggable.** Play refuses any upload where `android:debuggable="true"`.
2. **It is signed with the debug key.** Play requires an upload key you control.
3. **New apps must ship as an Android App Bundle (`.aab`), not an APK.**

On top of that, `versionCode` was hard-coded to `1`, so the *second* upload
would always fail with *"Version code 1 has already been used."*

`release-android.yml` plus the signing config in `android/app/build.gradle`
fix all four.

## One-time setup

### 1. Create an upload keystore

Keep this file safe and backed up. If you lose it you cannot ship updates to
the same listing without asking Google to reset your upload key.

```bash
keytool -genkeypair -v \
  -keystore upload-keystore.jks \
  -alias upload \
  -keyalg RSA -keysize 2048 -validity 10000
```

### 2. Add the secrets to GitHub

`Settings → Secrets and variables → Actions → New repository secret`:

| Secret | Value |
|---|---|
| `ANDROID_KEYSTORE_BASE64` | `base64 -w0 upload-keystore.jks` |
| `ANDROID_KEYSTORE_PASSWORD` | keystore password from step 1 |
| `ANDROID_KEY_ALIAS` | `upload` |
| `ANDROID_KEY_PASSWORD` | key password from step 1 |

### 3. (Optional) Local release builds

Create `android/keystore.properties` — it is git-ignored:

```properties
storeFile=/absolute/path/to/upload-keystore.jks
storePassword=…
keyAlias=upload
keyPassword=…
```

Then `cd android && ./gradlew bundleRelease -PappVersionCode=2 -PappVersionName=1.0.1`.

Without these credentials the release build still runs but emits an **unsigned**
artifact and logs a warning — it deliberately does not fall back to the debug
key, because that would produce something Play silently rejects at upload time.

## Cutting a release

Run the **Release Android AAB** workflow (Actions tab → Run workflow), or push a
`v*` tag. Download the `nexustap-release-aab` artifact and upload
`app-release.aab` in the Play Console.

`versionCode` comes from `github.run_number`, so every run produces a value Play
has not seen. `versionName` defaults to `1.0.<run_number>` and can be overridden
via the workflow input.

## Play Console items that are not fixable from code

These have to be filled in on the console side:

- **Privacy policy URL** — required for every app. The game runs entirely
  offline (see below), so a short policy is enough; host it anywhere public,
  e.g. GitHub Pages.
- **Data safety form** — the app collects and shares **nothing**. There is no
  backend, no analytics SDK, no ad SDK, and no `fetch`/`XMLHttpRequest` anywhere
  in `src/`. All progress is stored locally in the WebView's `localStorage` and
  never leaves the device. Answer *"No, this app does not collect or share any
  user data."*
- **Content rating questionnaire** — a tap-reflex game with no user-generated
  content, no chat, no purchases and no ads.
- **Target audience & content** — declare the intended age group.
- **Ads declaration** — the app contains no ads.
- **App access** — no login required; all content is available without credentials.

## Permissions the app declares

Both are in `android/app/src/main/AndroidManifest.xml`:

- `INTERNET` — Capacitor default. The WebView loads only bundled local assets.
- `VIBRATE` — haptic feedback on tap (`vibrate()` in `src/NexusTap.jsx`).
