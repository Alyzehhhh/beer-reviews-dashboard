# 🚀 Deploy to Render — Step by Step

Your code is already on GitHub: **https://github.com/Alyzehhhh/beer-reviews-dashboard**

---

## Step 1: Sign up / Log in to Render
- Go to **https://render.com**
- Click **"Get Started for Free"**
- Choose **"Sign in with GitHub"** (use your `Alyzehhhh` account)

## Step 2: Create a New Web Service
- From the Render dashboard, click **"New +"** → **"Web Service"**
- Click **"Connect a repository"**
- Find and select **`beer-reviews-dashboard`**
- Click **"Connect"**

## Step 3: Configure the Service
Render will auto-detect Python. Set these values:

| Setting | Value |
|---------|-------|
| **Name** | `beer-reviews-dashboard` |
| **Region** | Pick closest to you (e.g., `Singapore` for Pakistan) |
| **Branch** | `main` |
| **Runtime** | `Python 3` |
| **Build Command** | `chmod +x build.sh && ./build.sh` |
| **Start Command** | `streamlit run app.py --server.port $PORT --server.headless true --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false` |
| **Plan** | `Free` |

## Step 4: Environment Variables
Click **"Advanced"** → **"Add Environment Variable"**:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.6` |

## Step 5: Deploy
- Click **"Create Web Service"**
- Wait for the build (~3-5 minutes)
- Once done, you'll get a URL like: `https://beer-reviews-dashboard.onrender.com`

## Step 6: Custom Domain (Optional)
- Go to **Settings** → **Custom Domains**
- Add your domain and update DNS records as shown

---

## ⚠️ Notes
- **Free tier**: App sleeps after 15 min of inactivity. First request after sleep takes ~30s.
- **Build time**: First build takes longer (installs git-lfs + downloads 172MB CSV).
- **Auto-deploy**: Every push to `main` branch triggers a new deployment automatically.
