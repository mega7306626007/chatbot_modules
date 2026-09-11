# Build Actual App (Android APK / iOS)

This repo is now a PWA + native wrapper. Two ways to get an actual app:

## Option A — PWA (instant, no build)
1. Open `https://pychat-mvp-XXXX.onrender.com` on Android Chrome → Menu → **Install app** / **Add to Home Screen**
2. Launches as standalone `Mwesh` (manifest + sw.js already in repo)

## Option B — Native APK (Capacitor)
Requires Node 18+ and Android Studio.

```bash
npm install
npx cap init Mwesh com.mwesh.pychat --web-dir="."
npx cap add android
# set server.url in capacitor.config.json to your Render URL (already set to pychat-mvp)
npx cap sync
npx cap open android   # builds APK in Android Studio → Build → Generate APK
```

For local offline app (no Render, uses Python backend):
- Change `capacitor.config.json` server.url to `""` and bundle `index.html`+`app.js` directly, or use `pywebview`/`BeeWare` to wrap `python main.py --web` in WebView.

## Option C — Bubblewrap TWA (Play Store)
```bash
npm i -g @bubblewrap/cli
bubblewrap init --manifest https://pychat-mvp-XXXX.onrender.com/manifest.json
bubblewrap build
```
Generates signed APK/AAB for Play Store from the same PWA.
