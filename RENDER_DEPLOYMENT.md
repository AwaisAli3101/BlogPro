# Render Deployment Guide for BlogPro

This guide walks you through deploying the BlogPro Django application on Render.

## Prerequisites

1. **GitHub Repository**: Your BlogPro project pushed to GitHub
2. **Render Account**: Sign up at https://render.com
3. **GitHub Account**: Connected to Render

## Deployment Steps

### Step 1: Connect GitHub to Render

1. Go to [https://dashboard.render.com](https://dashboard.render.com)
2. Sign up or log in with your GitHub account
3. Click **"Connect account"** and authorize GitHub

### Step 2: Create a New Web Service

1. Click **"New +"** button in the Render dashboard
2. Select **"Web Service"**
3. Connect your GitHub repository (search for "BlogPro")
4. Select the repository

### Step 3: Configure the Web Service

Fill in the following details:

| Field | Value |
|-------|-------|
| **Name** | `blogpro` |
| **Environment** | `Python 3` |
| **Region** | Select your closest region |
| **Branch** | `main` |
| **Build Command** | See below |
| **Start Command** | See below |
| **Instance Type** | `Free` (for testing) or `Starter` (for production) |

#### Build Command:
```bash
pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput
```

#### Start Command:
```bash
gunicorn blogpro.wsgi:application --bind 0.0.0.0:$PORT
```

### Step 4: Set Environment Variables

Click **"Advanced"** and add the following environment variables:

| Key | Value | Notes |
|-----|-------|-------|
| `DEBUG` | `False` | Must be False in production |
| `SECRET_KEY` | (Generate) | Render will auto-generate a secure key |
| `ALLOWED_HOSTS` | `yourdomain.onrender.com` | Replace with your actual Render domain |
| `DATABASE_URL` | (Optional) | If using external database |

### Step 5: Deploy

1. Review all settings
2. Click **"Create Web Service"**
3. Render will automatically build and deploy your app
4. Monitor the build progress in the "Logs" tab
5. Once deployed, your app will be live at `https://blogpro-xxxxx.onrender.com`

---

## After Deployment

### Create a Superuser

Once your app is running, create a superuser to access the Django admin:

```bash
# In Render Shell (if available) or via direct SSH
python manage.py createsuperuser
```

Alternatively, you can create it locally and transfer the database.

### Configure Static Files

The project uses WhiteNoise to serve static files automatically. Ensure:

```python
# In settings.py (already configured)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

### Media Files Storage

**Important**: SQLite database and media files stored on Render's ephemeral filesystem will be **deleted** when the service restarts.

**For persistent storage**, consider using:
- **AWS S3** for media files
- **PostgreSQL** for database (via Render or external service)

#### To use PostgreSQL on Render:

1. Create a PostgreSQL database in Render
2. Get the `DATABASE_URL`
3. Add to your `requirements.txt`:
   ```
   psycopg2-binary==2.9.9
   ```
4. Update `DATABASES` in `settings.py`:
   ```python
   import dj_database_url
   DATABASES = {'default': dj_database_url.config(default='sqlite:///db.sqlite3')}
   ```
5. Redeploy

---

## Troubleshooting

### Build Fails
- Check the build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version compatibility

### "Static files not found" Error
- Ensure `python manage.py collectstatic --noinput` runs in build command
- Check `STATIC_ROOT` and `STATICFILES_DIRS` in settings.py

### Database Errors After Restart
- SQLite doesn't persist on Render
- Use PostgreSQL for persistent database storage

### Media Files Not Showing
- Media files don't persist on Render's free tier
- Implement S3 or similar cloud storage for uploads

### Custom Domain
1. Go to Settings → Custom Domain
2. Add your domain (e.g., `blogpro.com`)
3. Follow DNS configuration instructions

---

## Environment Variables Reference

```env
DEBUG=False
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=yourdomain.onrender.com,www.yourdomain.com
DATABASE_URL=postgresql://user:password@host:port/dbname  # Optional
AWS_ACCESS_KEY_ID=your-key  # For S3 storage (optional)
AWS_SECRET_ACCESS_KEY=your-secret  # For S3 storage (optional)
AWS_STORAGE_BUCKET_NAME=your-bucket  # For S3 storage (optional)
```

---

## Performance Tips

1. **Use PostgreSQL** instead of SQLite for production
2. **Upgrade Instance Type** if you need more resources
3. **Enable Caching** for frequently accessed pages
4. **Use S3** for media files to reduce server load
5. **Monitor Resource Usage** in Render dashboard

---

## Support & Resources

- **Render Docs**: https://render.com/docs
- **Django Deployment**: https://docs.djangoproject.com/en/5.2/howto/deployment/
- **WhiteNoise**: http://whitenoise.evans.io/
- **Gunicorn**: https://gunicorn.org/

---

## Quick Deploy Summary

```
1. Push code to GitHub
2. Connect Render to GitHub
3. Create Web Service
4. Set environment variables
5. Deploy
6. Access your app at yourdomain.onrender.com
```

Happy deploying! 🚀
