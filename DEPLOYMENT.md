# Deployment Guide

This guide explains how to deploy the RAG Semantic Search application to various hosting platforms.

## General Requirements

- Python 3.8 or higher
- Persistent file storage for `notes/` and `data/` directories
- At least 512MB RAM (for model loading)
- ~200MB disk space

## Platform-Specific Instructions

### Railway

1. Sign up at [railway.app](https://railway.app)
2. Click "New Project" → "Deploy from GitHub repo"
3. Select your repository
4. Railway will auto-detect Python and install dependencies
5. The app will be available at `https://your-app.railway.app`
6. Access the UI at `https://your-app.railway.app/ui`

**Note**: Railway provides persistent storage by default, so your `notes/` and `data/` folders will persist.

### Render

1. Sign up at [render.com](https://render.com)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.api:app --host 0.0.0.0 --port $PORT`
   - **Environment**: Python 3
5. Click "Create Web Service"
6. Access at `https://your-app.onrender.com/ui`

**Note**: Render's free tier spins down after inactivity. First request may take 30-60 seconds.

### Heroku

1. Install Heroku CLI
2. Login: `heroku login`
3. Create app: `heroku create your-app-name`
4. Set Python version: `heroku stack:set heroku-22`
5. Deploy: `git push heroku main`
6. Access at `https://your-app-name.herokuapp.com/ui`

### DigitalOcean App Platform

1. Sign up at [digitalocean.com](https://digitalocean.com)
2. Go to App Platform → Create App
3. Connect GitHub repository
4. Auto-detects FastAPI
5. Review and deploy
6. Access at your provided URL

### VPS (Ubuntu/Debian)

1. SSH into your server
2. Install Python and pip:
   ```bash
   sudo apt update
   sudo apt install python3 python3-pip
   ```
3. Clone repository:
   ```bash
   git clone <your-repo-url>
   cd semantic-notes-search
   ```
4. Install dependencies:
   ```bash
   pip3 install -r requirements.txt
   ```
5. Run with systemd (create `/etc/systemd/system/rag-search.service`):
   ```ini
   [Unit]
   Description=RAG Semantic Search
   After=network.target

   [Service]
   User=www-data
   WorkingDirectory=/path/to/semantic-notes-search
   ExecStart=/usr/bin/python3 -m uvicorn app.api:app --host 0.0.0.0 --port 8000
   Restart=always

   [Install]
   WantedBy=multi-user.target
   ```
6. Enable and start:
   ```bash
   sudo systemctl enable rag-search
   sudo systemctl start rag-search
   ```

## Post-Deployment

1. **Build the Index**: Visit `/ui` and click "Build Index" or call `/index` endpoint
2. **Test Search**: Try a search query to verify everything works
3. **Monitor**: Check logs for any errors

## Troubleshooting

**Model not downloading**: Ensure internet connectivity on first run
**Index not persisting**: Check that `data/` folder has write permissions
**Port issues**: Ensure `$PORT` environment variable is set (most platforms set this automatically)
**Memory issues**: Upgrade to a plan with more RAM if model loading fails

## Security Considerations

For production deployments:
- Restrict CORS origins in `app/api.py` (currently allows all)
- Add authentication if exposing publicly
- Use HTTPS (most platforms provide this automatically)
- Consider rate limiting for API endpoints

