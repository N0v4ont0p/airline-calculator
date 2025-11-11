# 🚀 Deployment Guide - SkyMiles Calculator

This guide will help you deploy the SkyMiles Calculator to Render.com (or any other static hosting platform).

---

## 📋 Prerequisites

- GitHub account
- Render.com account (free tier available)
- Git installed locally

---

## 🌐 Option 1: Deploy to Render.com (Recommended)

### Step 1: Push to GitHub

1. **Create a new GitHub repository:**
   ```bash
   # Initialize git (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit
   git commit -m "Initial commit: SkyMiles Calculator"
   
   # Add remote (replace with your repo URL)
   git remote add origin https://github.com/YOUR_USERNAME/airline-miles-calculator.git
   
   # Push to GitHub
   git branch -M main
   git push -u origin main
   ```

### Step 2: Connect to Render

1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click **"New +"** → **"Static Site"**
3. Connect your GitHub account
4. Select your `airline-miles-calculator` repository

### Step 3: Configure Build Settings

**Build Settings:**
- **Name**: `skymiles-calculator` (or your preferred name)
- **Branch**: `main`
- **Root Directory**: (leave blank)
- **Build Command**: `pnpm install && pnpm build`
- **Publish Directory**: `client/dist`

**Advanced Settings:**
- **Auto-Deploy**: Yes (recommended)
- **Pull Request Previews**: Yes (optional)

### Step 4: Deploy!

1. Click **"Create Static Site"**
2. Wait for the build to complete (2-3 minutes)
3. Your site will be live at `https://skymiles-calculator.onrender.com`

### Step 5: Custom Domain (Optional)

1. Go to your site's **Settings** → **Custom Domain**
2. Add your domain (e.g., `skymiles.yourdomain.com`)
3. Follow DNS configuration instructions
4. Wait for SSL certificate provisioning

---

## 🔧 Option 2: Deploy to Vercel

### Quick Deploy

```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
cd airline-miles-calculator
vercel

# Follow the prompts
# Build Command: pnpm build
# Output Directory: client/dist
```

### Configuration File

Create `vercel.json`:

```json
{
  "buildCommand": "pnpm build",
  "outputDirectory": "client/dist",
  "framework": "vite",
  "rewrites": [
    { "source": "/(.*)", "destination": "/index.html" }
  ]
}
```

---

## 🌍 Option 3: Deploy to Netlify

### Via Netlify CLI

```bash
# Install Netlify CLI
npm install -g netlify-cli

# Build the project
pnpm build

# Deploy
netlify deploy --prod --dir=client/dist
```

### Via Netlify Dashboard

1. Drag and drop `client/dist` folder to [Netlify Drop](https://app.netlify.com/drop)
2. Or connect GitHub repository with these settings:
   - **Build Command**: `pnpm build`
   - **Publish Directory**: `client/dist`

### Configuration File

Create `netlify.toml`:

```toml
[build]
  command = "pnpm build"
  publish = "client/dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

---

## ☁️ Option 4: Deploy to AWS S3 + CloudFront

### Step 1: Build the Project

```bash
pnpm build
```

### Step 2: Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://skymiles-calculator

# Enable static website hosting
aws s3 website s3://skymiles-calculator \
  --index-document index.html \
  --error-document index.html
```

### Step 3: Upload Files

```bash
# Sync build files to S3
aws s3 sync client/dist s3://skymiles-calculator \
  --acl public-read \
  --cache-control "max-age=31536000,public" \
  --exclude "index.html"

# Upload index.html separately (no cache)
aws s3 cp client/dist/index.html s3://skymiles-calculator/index.html \
  --acl public-read \
  --cache-control "no-cache"
```

### Step 4: Configure CloudFront (Optional)

1. Create CloudFront distribution
2. Set origin to S3 bucket
3. Configure custom error responses (404 → /index.html)
4. Enable HTTPS with ACM certificate

---

## 📦 Option 5: Manual Deployment (Any Host)

### Build the Project

```bash
# Install dependencies
pnpm install

# Build for production
pnpm build

# Output will be in client/dist/
```

### Upload to Your Host

The `client/dist` folder contains:
- `index.html` - Main HTML file
- `assets/` - JavaScript, CSS, and other assets
- `airports.json`, `airlines.json`, `programs.json` - Data files

Upload these files to your web server's public directory.

### Server Configuration

**Apache (.htaccess):**
```apache
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteBase /
  RewriteRule ^index\.html$ - [L]
  RewriteCond %{REQUEST_FILENAME} !-f
  RewriteCond %{REQUEST_FILENAME} !-d
  RewriteRule . /index.html [L]
</IfModule>
```

**Nginx:**
```nginx
location / {
  try_files $uri $uri/ /index.html;
}
```

---

## 🔍 Troubleshooting

### Build Fails

**Issue**: `pnpm: command not found`

**Solution**: Use npm instead:
```bash
# Build Command
npm install && npm run build
```

### Assets Not Loading

**Issue**: 404 errors for CSS/JS files

**Solution**: Check that `Publish Directory` is set to `client/dist` (not just `dist`)

### Blank Page After Deployment

**Issue**: White screen, no errors in console

**Solution**: 
1. Check browser console for errors
2. Verify all data files (airports.json, airlines.json, programs.json) are in the dist folder
3. Check network tab for failed requests

### Data Files Not Found

**Issue**: `Failed to fetch /airports.json`

**Solution**: Ensure data files are copied to `client/public/` before building:
```bash
cp data/*.json client/public/
pnpm build
```

---

## 🎯 Performance Optimization

### Enable Compression

**Render/Vercel/Netlify**: Automatic gzip/brotli compression

**Custom Server**:
```nginx
# Nginx
gzip on;
gzip_types text/plain text/css application/json application/javascript;
```

### Cache Headers

Data files should be cached:
```
airports.json: Cache-Control: public, max-age=86400
airlines.json: Cache-Control: public, max-age=86400
programs.json: Cache-Control: public, max-age=3600
```

### CDN

For global performance, use a CDN:
- Cloudflare (free tier available)
- AWS CloudFront
- Fastly

---

## 🔐 Security Headers

Add these headers for better security:

```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Referrer-Policy: strict-origin-when-cross-origin
Permissions-Policy: geolocation=(), microphone=(), camera=()
```

**Render**: Add in `render.yaml`
**Vercel**: Add in `vercel.json`
**Netlify**: Add in `netlify.toml`

---

## 📊 Monitoring

### Analytics

The app includes Umami analytics (configured via environment variables).

To set up:
1. Create Umami account
2. Add website
3. Set environment variables:
   - `VITE_ANALYTICS_ENDPOINT`
   - `VITE_ANALYTICS_WEBSITE_ID`

### Error Tracking

Consider adding:
- Sentry for error tracking
- LogRocket for session replay
- Google Analytics for user behavior

---

## 🔄 Continuous Deployment

### Automatic Deploys

**Render/Vercel/Netlify**: Automatically deploy on push to `main` branch

### Manual Deploys

```bash
# Render
git push origin main

# Vercel
vercel --prod

# Netlify
netlify deploy --prod
```

---

## 📝 Environment Variables

The app uses these environment variables (all have defaults):

```bash
# App Configuration
VITE_APP_TITLE="SkyMiles Calculator"
VITE_APP_LOGO="/vite.svg"

# Analytics (optional)
VITE_ANALYTICS_ENDPOINT="https://analytics.example.com"
VITE_ANALYTICS_WEBSITE_ID="your-website-id"
```

Set these in your hosting platform's dashboard under **Environment Variables**.

---

## ✅ Post-Deployment Checklist

- [ ] Site loads correctly
- [ ] Airport search works
- [ ] Calculator produces results
- [ ] Export to CSV works
- [ ] Export to PDF works
- [ ] Share link copies to clipboard
- [ ] Save route works
- [ ] Mobile responsive design looks good
- [ ] All 50+ programs load correctly
- [ ] Distance calculations are accurate
- [ ] Custom domain configured (if applicable)
- [ ] SSL certificate active
- [ ] Analytics tracking (if configured)

---

## 🎉 You're Live!

Congratulations! Your SkyMiles Calculator is now live and ready to help people maximize their airline miles!

**Share your deployment:**
- Tweet about it
- Share on Reddit (r/awardtravel, r/churning)
- Post on FlyerTalk forums
- Submit to Product Hunt

---

## 📧 Need Help?

If you encounter any issues:
1. Check the troubleshooting section above
2. Review build logs in your hosting platform
3. Open an issue on GitHub
4. Contact support for your hosting platform

**Happy deploying!** ✈️🚀
