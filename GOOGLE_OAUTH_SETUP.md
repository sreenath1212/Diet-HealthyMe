# Google OAuth Setup Guide for HealthyMe

## Overview
This guide will help you set up Google OAuth login for your HealthyMe project.

## Step 1: Create Google OAuth Credentials

### 1. Go to Google Cloud Console
- Visit: https://console.cloud.google.com/
- Sign in with your Google account

### 2. Create a New Project (if needed)
- Click on the project dropdown at the top
- Click "New Project"
- Enter a project name (e.g., "HealthyMe OAuth")
- Click "Create"

### 3. Enable Google+ API
- Go to "APIs & Services" > "Library"
- Search for "Google+ API" or "Google Identity"
- Click on it and click "Enable"

### 4. Create OAuth 2.0 Credentials
- Go to "APIs & Services" > "Credentials"
- Click "Create Credentials" > "OAuth 2.0 Client IDs"
- Choose "Web application" as the application type
- Enter a name (e.g., "HealthyMe Web Client")

### 5. Configure Authorized Redirect URIs
Add these redirect URIs:
- `http://127.0.0.1:8000/google-login-callback/` (for development)
- `http://localhost:8000/google-login-callback/` (alternative development)
- `https://yourdomain.com/google-login-callback/` (for production)

### 6. Get Your Credentials
- After creating, you'll get:
  - **Client ID** (looks like: `123456789-abcdefghijklmnop.apps.googleusercontent.com`)
  - **Client Secret** (looks like: `GOCSPX-abcdefghijklmnopqrstuvwxyz`)

## Step 2: Update Your Environment Variables

Add these to your `.env` file:

```env
# Google OAuth Configuration
GOOGLE_OAUTH_CLIENT_ID=your-client-id-here
GOOGLE_OAUTH_CLIENT_SECRET=your-client-secret-here

# Existing email configuration
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Other existing variables
GEMINI_API_KEY=your-gemini-api-key
YOUTUBE_API_KEY=your-youtube-api-key
EDAMAM_APP_ID=your-edamam-app-id
EDAMAM_APP_KEY=your-edamam-app-key
```

## Step 3: Test the Implementation

### 1. Restart Your Django Server
```bash
python manage.py runserver
```

### 2. Test Google Login
- Go to `http://127.0.0.1:8000/login/`
- Click "Login with Google"
- You should be redirected to Google's consent screen
- After authorization, you'll be redirected back to your app

## Features Implemented

### ✅ **Google OAuth Login Flow**
1. User clicks "Login with Google"
2. Redirected to Google's consent screen
3. User authorizes the application
4. Google redirects back with authorization code
5. App exchanges code for user information
6. User is logged in or account is created

### ✅ **Automatic Account Creation**
- If user doesn't exist, creates new account automatically
- Uses Google profile information (name, email)
- Sets default values for required fields

### ✅ **Existing User Login**
- If user already exists, logs them in directly
- Maintains existing user roles and permissions

### ✅ **Security Features**
- OAuth state verification
- Secure token exchange
- User information validation

## Troubleshooting

### Common Issues:

1. **"Invalid redirect URI" error**
   - Check that your redirect URI exactly matches what's in Google Console
   - Make sure there are no extra spaces or characters

2. **"Client ID not found" error**
   - Verify your GOOGLE_OAUTH_CLIENT_ID in .env file
   - Make sure the .env file is in the project root

3. **"Invalid client secret" error**
   - Check your GOOGLE_OAUTH_CLIENT_SECRET in .env file
   - Regenerate the client secret if needed

4. **"API not enabled" error**
   - Make sure Google+ API or Google Identity API is enabled
   - Check that OAuth consent screen is configured

### Debug Steps:

1. **Check Environment Variables**
   ```python
   # In Django shell
   from django.conf import settings
   print(settings.GOOGLE_OAUTH_CLIENT_ID)
   print(settings.GOOGLE_OAUTH_CLIENT_SECRET)
   ```

2. **Test OAuth Flow**
   - Visit `/google-login/` directly
   - Check browser console for errors
   - Check Django server logs

3. **Verify Google Console Settings**
   - Check that redirect URIs are correct
   - Ensure OAuth consent screen is configured
   - Verify API is enabled

## Production Deployment

### For Production:
1. **Update Redirect URIs** in Google Console:
   - Add your production domain
   - Remove development URLs

2. **Update Environment Variables**:
   ```env
   GOOGLE_OAUTH_REDIRECT_URI=https://yourdomain.com/google-login-callback/
   ```

3. **Configure OAuth Consent Screen**:
   - Add your production domain
   - Set up proper app information
   - Configure user support email

## Security Considerations

### ✅ **Implemented Security Features**:
- OAuth state verification
- Secure token exchange
- User information validation
- Session management
- CSRF protection

### 🔒 **Additional Recommendations**:
- Use HTTPS in production
- Implement rate limiting
- Add logging for OAuth events
- Regular security audits

## User Experience

### **For New Users**:
- Click "Login with Google"
- Authorize the application
- Account created automatically
- Redirected to user dashboard

### **For Existing Users**:
- Click "Login with Google"
- Authorized automatically (if previously authorized)
- Logged in directly
- Redirected based on user type

The Google OAuth implementation provides a seamless, secure login experience for your HealthyMe users! 🎉 