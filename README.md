# Grandma's Translator App
Real-time translator with Persian TTS. Fully free, installs on iPhone.

## How it works
- **Translation**: Python backend using `deep-translator` (Google Translate, free & unlimited)
- **Text-to-Speech**: Browser Web Speech API — Persian (`fa-IR`) built into iOS Safari
- **Speech Input**: Browser microphone via Web Speech API
- **iPhone install**: Progressive Web App (PWA) — no App Store needed

---

## Step 1 — Deploy the Backend (Render.com, free)

1. Create a free account at https://render.com
2. Create a new **Web Service**
3. Connect your GitHub repo (push the `backend/` folder)
4. Set these settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python version**: 3.11
5. Deploy — Render gives you a URL like `https://translator-backend-xxxx.onrender.com`

> **Note**: Free Render instances sleep after 15 min of inactivity. First request may take ~30 seconds to wake up. To avoid this, use Render's free "cron job" to ping `/health` every 10 minutes.

---

## Step 2 — Configure the Frontend

Open `frontend/index.html` and find this line near the top:

```js
const BACKEND_URL = "https://YOUR-APP-NAME.onrender.com";
```

Replace `YOUR-APP-NAME` with your actual Render URL.

---

## Step 3 — Host the Frontend (GitHub Pages, free)

1. Create a GitHub account at https://github.com if you don't have one
2. Create a new repository (e.g. `grandma-translator`)
3. Upload everything in the `frontend/` folder to the repo root
4. Go to **Settings → Pages → Source** → select `main` branch → Save
5. Your app will be live at `https://YOUR-USERNAME.github.io/grandma-translator`

---

## Step 4 — Install on iPhone

1. Open the GitHub Pages URL in **Safari** on her iPhone (must be Safari)
2. Tap the **Share** button (box with arrow pointing up)
3. Tap **"Add to Home Screen"**
4. Tap **Add**

The app now appears on her home screen like a native app — full screen, no browser bar.

---

## App Icons (optional)

Replace the placeholder icons in `frontend/icons/` with real PNG images:
- `icon-192.png` — 192×192 pixels
- `icon-512.png` — 512×512 pixels

You can generate these from any image at https://realfavicongenerator.net

---

## Language Support

| Language | Translation | Voice (TTS) | Mic (STT) |
|----------|-------------|-------------|-----------|
| English  | ✅ | ✅ | ✅ |
| Persian  | ✅ | ✅ iOS/Chrome | ✅ Chrome |
| Arabic   | ✅ | ✅ | ✅ |
| French   | ✅ | ✅ | ✅ |
| Spanish  | ✅ | ✅ | ✅ |
| German   | ✅ | ✅ | ✅ |
| Chinese  | ✅ | ✅ | ✅ |
| Russian  | ✅ | ✅ | ✅ |
| Turkish  | ✅ | ✅ | ✅ |
| Urdu     | ✅ | ✅ | ✅ |
| Hindi    | ✅ | ✅ | ✅ |

---

## Persian TTS on iPhone

iOS Safari includes a Persian (`fa-IR`) voice natively. If voice doesn't play:
1. Go to iPhone **Settings → Accessibility → Spoken Content → Voices**
2. Select **Persian** and download the enhanced voice
3. Return to the app and press **Listen** again

---

## Folder Structure

```
translator-app/
├── backend/
│   ├── app.py            # Flask API
│   ├── requirements.txt  # Python dependencies
│   └── render.yaml       # Render.com config
└── frontend/
    ├── index.html         # The entire app
    ├── manifest.json      # PWA manifest (enables "Add to Home Screen")
    ├── sw.js              # Service worker (offline support)
    └── icons/
        ├── icon-192.png   # App icon (replace with your own)
        └── icon-512.png   # App icon (replace with your own)
```
