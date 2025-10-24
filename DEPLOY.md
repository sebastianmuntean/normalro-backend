# Deploy Simple Backend to Vercel

## ✅ What We Have

A super simple Flask app with just 2 endpoints:
- `/` → Returns "Hello World!"
- `/api/health` → Returns `{"status":"ok"}`

## 🚀 Deploy Steps

### 1. Push to GitHub

```powershell
cd C:\Projects\normalro\_git\normalro-backend

git add .
git commit -m "Simple Hello World Flask app"
git push
```

### 2. Deploy on Vercel

**Option A: Automatic (if already connected)**
- Vercel will auto-deploy when you push

**Option B: Manual**
1. Go to https://vercel.com
2. Go to your backend project
3. Deployments → Click three dots → Redeploy

### 3. Test It

After deployment, visit:
- `https://your-backend-url.vercel.app/`
- `https://your-backend-url.vercel.app/api/health`

Both should work!

## 📝 Files

- `app.py` - Simple Flask app (14 lines)
- `index.py` - Import for Vercel (1 line)
- `requirements.txt` - Just Flask (1 line)
- `vercel.json` - Vercel config

## ✅ Once Working

After this simple app works on Vercel, we can add back all the tools functionality!

