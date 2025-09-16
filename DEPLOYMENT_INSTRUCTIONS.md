# Diriyah Brain AI - Production Deployment Instructions

## 🚀 Deploy to Render (Recommended)

### Step 1: Upload to GitHub
1. Create a new repository on GitHub
2. Upload the `diriyah-brain-ai-production.zip` contents
3. Push all files to the repository

### Step 2: Deploy on Render
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:

**Build Settings:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `python main.py`
- **Environment:** `Python 3`

**Environment Variables:**
```
OPENAI_API_KEY=your_openai_api_key_here

GOOGLE_CLIENT_ID=your_google_client_id_here

GOOGLE_CLIENT_SECRET=your_google_client_secret_here

GOOGLE_REDIRECT_URI=https://diriyah-ai-demo.onrender.com/api/enhanced-drive/callback
```

### Step 3: Update Google Cloud Console
Add this redirect URI to your Google Cloud OAuth settings:
```
https://diriyah-ai-demo.onrender.com/api/enhanced-drive/callback
```

## 🌐 Current Working System

**Live Demo:** https://8080-iff10znhxt946xatplzfe-f2efef9c.manus.computer

## ✅ Features Included

### 🎨 User Interface
- Clean Manus-style chat interface
- Diriyah branding with authentic logo
- Responsive design for mobile and desktop
- Professional sidebar with projects and tasks
- Bottom navigation bar with settings, help, home, support, profile

### 🤖 AI Capabilities
- Real OpenAI GPT-4.1-mini integration
- Contextual responses for construction projects
- Intelligent fallback responses
- Project-specific knowledge base

### 📁 File Management
- Universal file upload (any file type)
- Google Drive OAuth integration
- Camera capture functionality
- Voice message recording
- ZIP/RAR archive processing

### 🔧 Background Services
- Document processing (PDF, Word, Excel, CAD)
- BIM file analysis
- Project data integration
- Real-time progress tracking

### 🛡️ Security & Authentication
- Role-based access control
- Google OAuth integration
- Secure API endpoints
- Environment variable configuration

## 📋 Post-Deployment Checklist

1. ✅ Verify all environment variables are set
2. ✅ Test Google Drive OAuth flow
3. ✅ Confirm AI chat responses
4. ✅ Test file upload functionality
5. ✅ Verify mobile responsiveness
6. ✅ Check all navigation buttons

## 🆘 Support

If you encounter any issues:
1. Check the Render deployment logs
2. Verify environment variables are correct
3. Ensure Google Cloud OAuth settings match
4. Test the live demo for comparison

## 🎉 Success!

Once deployed, your Diriyah Brain AI will be live at:
`https://diriyah-ai-demo.onrender.com`

The system includes all the features we built together:
- Professional Manus-style interface
- Real AI integration
- Google Drive connectivity
- Comprehensive file processing
- Mobile-optimized design

