# Railway Deployment Order

## Step-by-Step Deployment for Both Repos

### 1. Deploy Backend First
```bash
cd /Users/manishphatak/projects/kwiz-backend
python generate_secret_key.py  # Copy the SECRET_KEY
git add .
git commit -m "Backend ready for Railway"
git push origin main
```

**Railway Setup:**
1. Go to railway.app
2. Deploy kwiz-backend repository
3. Add PostgreSQL database
4. Set environment variables:
   - `SECRET_KEY`: (from generate_secret_key.py)
   - `DEBUG`: False
5. Note the backend URL: `https://kwiz-backend-production.railway.app`

### 2. Deploy Frontend Second
```bash
cd /Users/manishphatak/projects/kwiz-frontend
git add .
git commit -m "Frontend ready for Railway"
git push origin main
```

**Railway Setup:**
1. Deploy kwiz-frontend repository
2. Set environment variable:
   - `REACT_APP_API_URL`: `https://kwiz-backend-production.railway.app`
3. Note the frontend URL: `https://kwiz-frontend-production.railway.app`

### 3. Configure Domain
1. Point kwiz.fun to frontend Railway app
2. Optionally: Point api.kwiz.fun to backend Railway app

### 4. Test Everything
- Visit kwiz.fun
- Test quiz functionality
- Check API calls in browser dev tools
- Verify timer system works

## Benefits of All-Railway Setup
- ✅ One platform to manage
- ✅ One billing account
- ✅ Easy environment variable management
- ✅ Simplified CORS configuration
- ✅ Both apps on same infrastructure
