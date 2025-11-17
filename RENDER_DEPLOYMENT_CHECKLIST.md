# BlogPro Render Deployment Checklist ✅

## Pre-Deployment Checklist

- [ ] All code is committed and pushed to GitHub
- [ ] `.gitignore` includes `db.sqlite3`, `media/`, `*.pyc`, `.env`
- [ ] `requirements.txt` is updated with all dependencies
- [ ] `SECRET_KEY` is different for production
- [ ] `DEBUG = False` in production settings
- [ ] All database migrations are created and committed
- [ ] Static files configuration is correct
- [ ] `manage.py` is executable (for local testing)

## Render-Specific Configuration

- [ ] `render.yaml` file is created in project root
- [ ] Python version specified in `render.yaml` (currently 3.11)
- [ ] Build command includes migrations and collectstatic
- [ ] Start command uses gunicorn
- [ ] `PYTHON_VERSION` environment variable set to 3.11

## Environment Variables Setup

Before deploying to Render, prepare these variables:

```
DEBUG=False
SECRET_KEY=(Render will auto-generate)
ALLOWED_HOSTS=yourdomain.onrender.com
```

## Step-by-Step Deployment to Render

### 1. Prepare Your Repository
```bash
# Ensure everything is committed
git status
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Sign Up / Log In to Render
- Visit https://dashboard.render.com
- Sign up with GitHub or log in

### 3. Connect GitHub Repository
- Click "New +" → "Web Service"
- Search and select "BlogPro" repository
- Click "Connect"

### 4. Configure Service Settings
| Setting | Value |
|---------|-------|
| Name | blogpro |
| Environment | Python 3 |
| Region | (Choose closest to your users) |
| Branch | main |
| Build Command | `pip install -r requirements.txt && python manage.py migrate --noinput && python manage.py collectstatic --noinput` |
| Start Command | `gunicorn blogpro.wsgi:application --bind 0.0.0.0:$PORT` |

### 5. Set Environment Variables
Click "Advanced" and add:
- `DEBUG`: `False`
- `SECRET_KEY`: (Render auto-generates)
- `ALLOWED_HOSTS`: Your Render domain (e.g., `blogpro-abc123.onrender.com`)

### 6. Deploy
- Click "Create Web Service"
- Wait for build and deployment to complete
- Check the Logs tab for any errors

### 7. Access Your App
- Visit `https://yourdomain.onrender.com`
- Should see the BlogPro homepage

## Post-Deployment Tasks

### Create Superuser

Option A: Using Render Shell (if available)
```bash
python manage.py createsuperuser
```

Option B: Transfer from local
```bash
# Export from local
python manage.py dumpdata > data.json

# Upload and import in production
python manage.py loaddata data.json
```

### Test Admin Access
- Visit `https://yourdomain.onrender.com/admin`
- Log in with superuser credentials
- Test creating a post with "published" status

### Configure Custom Domain (Optional)
1. Go to Service Settings → Custom Domain
2. Add your domain (e.g., `myblogpro.com`)
3. Configure DNS according to Render's instructions

## Troubleshooting

### Build Fails with "ModuleNotFoundError"
**Solution**: Add missing package to `requirements.txt`
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Update dependencies"
git push
```

### "Static files not found" (404 errors)
**Solution**: Ensure WhiteNoise is installed and middleware is added
```python
# In settings.py
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
```

### Database Errors After Restart
**Problem**: SQLite doesn't persist on Render (ephemeral filesystem)
**Solution**: Use PostgreSQL instead
1. Create PostgreSQL in Render
2. Get DATABASE_URL
3. Install `psycopg2-binary` in requirements.txt
4. Update settings.py to use dj_database_url

### Media Files Disappear After Restart
**Problem**: Media stored locally won't persist
**Solutions**:
- Use AWS S3 for permanent storage
- Store media in external database
- Use Render's volume storage (for paid plans)

### Slow Performance
**Solutions**:
- Upgrade to paid instance type
- Enable caching
- Use PostgreSQL instead of SQLite
- Implement CDN for static assets

## Important Notes

⚠️ **Database Persistence**: SQLite data is lost when the service restarts. Use PostgreSQL for production.

⚠️ **Media Files**: Uploaded images won't persist on free tier. Configure S3 or external storage.

⚠️ **Performance**: Free tier may be slow. Upgrade to Starter or higher for better performance.

⚠️ **Security**: Never commit `.env` file or hardcode secrets in code.

## Useful Commands

```bash
# View Render logs
# Use Render dashboard Logs tab

# SSH into service (if available)
# Render Shell in the dashboard

# Restart service
# Use Render dashboard restart button

# Force redeploy
git commit --allow-empty -m "Force redeploy"
git push
```

## Resources

- [Render Documentation](https://render.com/docs)
- [Django Deployment Guide](https://docs.djangoproject.com/en/5.2/howto/deployment/)
- [WhiteNoise Documentation](http://whitenoise.evans.io/)
- [Gunicorn Documentation](https://gunicorn.org/)

## Support

If you encounter issues:
1. Check Render Logs tab for error messages
2. Review this checklist
3. Check Django documentation
4. Contact Render support at support@render.com

---

**Version**: 1.0  
**Last Updated**: November 17, 2025  
**Status**: Ready for Deployment ✅
