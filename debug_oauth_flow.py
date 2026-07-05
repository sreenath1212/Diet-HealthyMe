#!/usr/bin/env python
"""
Debug script to help identify OAuth callback issues
"""
import requests
import json

def debug_oauth_flow():
    """Debug the OAuth flow step by step"""
    
    print("=== Google OAuth Flow Debug Guide ===")
    print("\nTo debug the OAuth session issue:")
    
    print("\n1. **Start the OAuth flow:**")
    print("   - Go to: http://127.0.0.1:8000/login/")
    print("   - Click 'Login with Google'")
    print("   - Check browser developer tools -> Network tab")
    print("   - Look for the sessionid cookie")
    
    print("\n2. **Complete OAuth authorization:**")
    print("   - Authorize the app in Google")
    print("   - You'll be redirected back to: http://127.0.0.1:8000/google-login-callback/")
    print("   - Check the URL parameters: code=...&state=...")
    
    print("\n3. **Check server logs:**")
    print("   - Look for these debug messages in Django console:")
    print("   - 'DEBUG: Google callback - Initial session key: ...'")
    print("   - 'DEBUG: Google callback - Initial session data: ...'")
    print("   - 'DEBUG: Database check - existing_user: ...'")
    print("   - 'DEBUG: Session set for existing user - UID: ...'")
    
    print("\n4. **Expected behavior:**")
    print("   - Session should contain: UID, UNAME, UPASSWORD, UTYPE, status")
    print("   - You should be redirected to /userhome/")
    print("   - Session cookie should persist")
    
    print("\n5. **Common issues to check:**")
    print("   - Is the user email in the database?")
    print("   - Is the database query working?")
    print("   - Is the session data being set correctly?")
    print("   - Is the redirect working properly?")
    
    print("\n6. **Test session after OAuth:**")
    print("   - After OAuth login, try accessing: http://127.0.0.1:8000/userhome/")
    print("   - Check if you're still logged in")
    print("   - Check browser cookies for sessionid")
    
    print("\n=== Debug Complete ===")

def check_database_connection():
    """Check if database connection is working"""
    
    print("\n=== Database Connection Test ===")
    
    try:
        import django
        import os
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'HealthyMe.settings')
        django.setup()
        
        from django.db import connection
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) FROM login")
            count = cursor.fetchone()[0]
            print(f"   ✓ Database connected successfully")
            print(f"   ✓ Login table has {count} records")
            
            # Check for Google OAuth test user
            cursor.execute("SELECT * FROM login WHERE uname LIKE '%@gmail.com' LIMIT 5")
            users = cursor.fetchall()
            print(f"   ✓ Found {len(users)} Gmail users in database")
            
            for user in users:
                print(f"      - UID: {user[0]}, Email: {user[1]}, Type: {user[3]}")
                
    except Exception as e:
        print(f"   ❌ Database connection failed: {e}")
    
    print("=== Database Test Complete ===")

if __name__ == "__main__":
    debug_oauth_flow()
    check_database_connection() 