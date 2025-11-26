# 🚀 Deployment Guide

This guide covers multiple deployment options for the Health Assistant application.

---

## Option 1: Deploy to Render (Recommended - Free Tier Available)

Render provides free hosting for web services and is perfect for this project.

### Backend Deployment

1. **Create a `render.yaml` file** (already included in the project)
2. **Push to GitHub** (already done ✅)
3. **Go to [Render Dashboard](https://dashboard.render.com/)**
4. **Create New Web Service**
   - Connect your GitHub repository: `Sagi-Vijay/health-assistant`
   - Root Directory: leave blank
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. **Add Environment Variable**
   - Key: `GOOGLE_API_KEY`
   - Value: Your Google API Key
6. **Deploy** - Render will give you a URL like `https://health-assistant-xyz.onrender.com`

### Frontend Deployment

1. **Create another Web Service on Render**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0`
2. **Add Environment Variable**
   - Key: `API_URL`
   - Value: Your backend URL from step 6 above
3. **Update `frontend/app.py`** to use environment variable:
   ```python
   import os
   API_URL = os.getenv("API_URL", "http://localhost:8000")
   ```

---

## Option 2: Deploy to Railway

Railway offers a simple deployment process with a generous free tier.

1. **Go to [Railway](https://railway.app/)**
2. **New Project → Deploy from GitHub**
3. **Select your repository**
4. **Add Environment Variables**:
   - `GOOGLE_API_KEY`: Your API key
5. **Railway will auto-detect and deploy**

---

## Option 3: Docker Deployment (Self-Hosted)

### Create Dockerfile

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Build and Run

```bash
# Build the image
docker build -t health-assistant .

# Run the container
docker run -p 8000:8000 -e GOOGLE_API_KEY=your_key health-assistant
```

---

## Option 4: Deploy to Google Cloud Run

1. **Install Google Cloud CLI**
2. **Build and push to Google Container Registry**:
   ```bash
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/health-assistant
   ```
3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy health-assistant \
     --image gcr.io/YOUR_PROJECT_ID/health-assistant \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars GOOGLE_API_KEY=your_key
   ```

---

## Option 5: Deploy to Heroku

1. **Create `Procfile`**:
   ```
   web: uvicorn backend.main:app --host 0.0.0.0 --port $PORT
   ```
2. **Deploy**:
   ```bash
   heroku create health-assistant-app
   heroku config:set GOOGLE_API_KEY=your_key
   git push heroku main
   ```

---

## 🌐 GitHub Pages (Static Frontend Only)

If you want to deploy just the documentation or a static version:

1. **Go to Repository Settings → Pages**
2. **Select branch: `main`**
3. **Select folder: `/` (root)**
4. **Save**

Your README will be visible at: `https://sagi-vijay.github.io/health-assistant/`

---

## ⚙️ Environment Variables Required

For any deployment option, you'll need:

| Variable | Description | Example |
|----------|-------------|---------|
| `GOOGLE_API_KEY` | Your Gemini API key | `AIza...` |
| `SECRET_KEY` | JWT secret (change in production) | `your-secret-key` |
| `DATABASE_URL` | Optional: PostgreSQL URL for production | `postgresql://...` |

---

## 📝 Post-Deployment Checklist

- [ ] Test all endpoints (use `/docs` for Swagger UI)
- [ ] Verify authentication works
- [ ] Test file uploads (PDF, Audio)
- [ ] Check database persistence
- [ ] Monitor logs for errors
- [ ] Set up HTTPS (most platforms do this automatically)

---

## 🔒 Security Recommendations

1. **Change the SECRET_KEY** in `backend/auth.py` to a strong random value
2. **Use environment variables** for all sensitive data
3. **Enable CORS** properly in production
4. **Use PostgreSQL** instead of SQLite for production
5. **Implement rate limiting** on API endpoints

---

## 🆘 Troubleshooting

**Issue**: Database not persisting
- **Solution**: Use a managed database service (PostgreSQL on Render/Railway)

**Issue**: File uploads failing
- **Solution**: Ensure temp directory has write permissions

**Issue**: API key errors
- **Solution**: Verify environment variable is set correctly

---

**Need help?** Open an issue on GitHub: https://github.com/Sagi-Vijay/health-assistant/issues
