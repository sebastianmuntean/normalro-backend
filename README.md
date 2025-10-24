# Normal.ro Backend API

Flask API backend for normal.ro tools application.

## 🚀 Deploy to Vercel

1. **Push to GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/YOUR-USERNAME/normalro-backend.git
   git push -u origin main
   ```

2. **Deploy on Vercel:**
   - Go to [Vercel Dashboard](https://vercel.com)
   - Click "Add New Project"
   - Import this repository
   - Deploy (no configuration needed - Vercel will auto-detect everything)

3. **Configure Environment Variables:**
   After deployment:
   - Go to Project Settings → Environment Variables
   - Add: `ALLOWED_ORIGINS` = `https://your-frontend-url.vercel.app,http://localhost:3000`
   - Redeploy

## 🧪 Test API

After deployment, test these endpoints:

- Health check: `https://your-backend.vercel.app/api/health`
- List tools: `https://your-backend.vercel.app/api/tools`

## 🛠️ Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run server
python app.py
```

Server will run on `http://localhost:5000`

## 📡 API Endpoints

- `GET /api/health` - Health check
- `GET /api/tools` - List all tools
- `POST /api/tools/slug-generator` - Generate slug from text
- `POST /api/tools/word-counter` - Count words in text
- `POST /api/tools/password-generator` - Generate random password
- `POST /api/tools/base64-converter` - Encode/decode base64
- `POST /api/tools/cnp-generator` - Generate Romanian CNP
- `POST /api/tools/cnp-validator` - Validate Romanian CNP

## 🔧 Environment Variables

- `ALLOWED_ORIGINS` - Comma-separated list of allowed CORS origins
- `PORT` - Port for local development (default: 5000)

