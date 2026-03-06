# GoDaddy cPanel Deployment Guide

## Prerequisites
- GoDaddy hosting with cPanel access
- Git version control enabled in cPanel
- Python 3.11+ available
- Node.js 18+ available

## Deployment Steps

### 1. **Push to GitHub/GitLab**
```powershell
git add .
git commit -m "Ready for deployment"
git push origin master
```

### 2. **Setup in cPanel - File Manager**
- Login to your GoDaddy cPanel
- Upload your project files to `public_html` or create a subdomain

### 3. **Setup Git Integration (if available)**
- Go to **Git Version Control**
- Click **Create Repository**
- Select your remote repository (GitHub/GitLab)
- Set deployment branch to `master`
- Paste your `.cpanel.yml` configuration

### 4. **Configure Backend (Python/Flask)**

In cPanel **Setup Python App**:
- App URI: `/api` or `/backend`
- App Directory: `/home/username/public_html/backend`
- Application Startup File: `app.py`
- Application Entry Point: `application` (or `app`)
- Python Version: 3.11

### 5. **Configure Frontend (React)**

Your built React app in `public_html/` will serve automatically.

### 6. **Environment Variables**

In cPanel, set environment variables for your Python app:
- `FLASK_ENV=production`
- `DATABASE_URL=your_db_connection_string`
- `SECRET_KEY=your_secret_key`

### 7. **Database Setup (if needed)**

- Go to **MySQL Databases** in cPanel
- Create a new database
- Create a database user with appropriate privileges
- Update `backend/config.py` with connection string

### 8. **Deploy**

After pushing to your repository, cPanel will automatically:
1. ✅ Install Python dependencies
2. ✅ Build React frontend
3. ✅ Copy build files to `public_html`
4. ✅ Setup Python application
5. ✅ Routes API requests to backend

### 9. **API Configuration**

Update your frontend `api.js` to use your domain:
```javascript
const API_URL = process.env.NODE_ENV === 'production' 
  ? 'https://yourdomain.com/api' 
  : 'http://localhost:5000/api';
```

## Troubleshooting

**Backend not responding:**
- Check cPanel Python App configuration
- View error logs in cPanel
- Verify `app.py` entry point

**Frontend not loading:**
- Verify React build files are in `public_html`
- Check `.htaccess` rewrite rules
- Clear browser cache

**CORS Issues:**
- Update `backend/app.py` to allow your domain:
```python
CORS(app, origins=['https://yourdomain.com'])
```

## File Structure on cPanel

```
public_html/
├── index.html (React)
├── static/ (React assets)
├── api/ → backend/
└── .htaccess
```

## API Endpoints

- Frontend: `https://yourdomain.com`
- Backend: `https://yourdomain.com/api`
- Customer routes: `https://yourdomain.com/api/customers`
- Invoices routes: `https://yourdomain.com/api/invoices`
- Products routes: `https://yourdomain.com/api/products`
