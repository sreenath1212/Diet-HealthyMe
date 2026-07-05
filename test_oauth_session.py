#!/usr/bin/env python
"""
Test script to verify Google OAuth session handling
"""
import requests
import json

def test_oauth_session():
    """Test the Google OAuth session handling"""
    
    # Base URL
    base_url = "http://127.0.0.1:8000"
    
    # Create a session to maintain cookies
    session = requests.Session()
    
    print("=== Testing Google OAuth Session Handling ===")
    
    # Step 1: Access login page
    print("\n1. Accessing login page...")
    try:
        response = session.get(f"{base_url}/login/")
        print(f"   Status: {response.status_code}")
        print(f"   Session cookies: {dict(session.cookies)}")
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 2: Initiate Google OAuth (this will redirect to Google)
    print("\n2. Initiating Google OAuth...")
    try:
        response = session.get(f"{base_url}/google-login/", allow_redirects=False)
        print(f"   Status: {response.status_code}")
        print(f"   Redirect location: {response.headers.get('Location', 'None')}")
        print(f"   Session cookies: {dict(session.cookies)}")
        
        # Check if we got a redirect to Google
        if response.status_code == 302:
            redirect_url = response.headers.get('Location', '')
            if 'accounts.google.com' in redirect_url:
                print("   ✓ Successfully redirected to Google OAuth")
            else:
                print(f"   ⚠ Unexpected redirect: {redirect_url}")
        else:
            print("   ⚠ No redirect received")
            
    except Exception as e:
        print(f"   Error: {e}")
        return
    
    # Step 3: Test userhome access (should fail without login)
    print("\n3. Testing userhome access without login...")
    try:
        response = session.get(f"{base_url}/userhome/")
        print(f"   Status: {response.status_code}")
        print(f"   Session cookies: {dict(session.cookies)}")
        
        if response.status_code == 200:
            if "Please login first" in response.text:
                print("   ✓ Correctly requires login")
            else:
                print("   ⚠ Unexpected response - should require login")
        else:
            print(f"   ⚠ Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 4: Test regular login for comparison
    print("\n4. Testing regular login...")
    try:
        # This is a GET request, but in real app it would be POST
        # For testing, we'll just check if the endpoint exists
        response = session.get(f"{base_url}/searchlogin/")
        print(f"   Status: {response.status_code}")
        print(f"   Session cookies: {dict(session.cookies)}")
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Test Complete ===")
    print("\nNote: To fully test Google OAuth, you need to:")
    print("1. Visit http://127.0.0.1:8000/login/ in your browser")
    print("2. Click 'Login with Google'")
    print("3. Complete the OAuth flow")
    print("4. Check if you remain logged in when clicking other links")

if __name__ == "__main__":
    test_oauth_session() 