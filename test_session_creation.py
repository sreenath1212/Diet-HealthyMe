#!/usr/bin/env python
"""
Test script to verify session creation and storage
"""
import requests
import json

def test_session_creation():
    """Test session creation and storage"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("=== Testing Session Creation ===")
    
    # Step 1: Access login page
    print("\n1. Accessing login page...")
    response = session.get(f"{base_url}/login/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    # Step 2: Try to access a page that should create a session
    print("\n2. Accessing a page that should create session...")
    response = session.get(f"{base_url}/userhome/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    # Step 3: Check if session was created
    if session.cookies.get('sessionid'):
        print("   ✓ Session cookie was created")
        session_key = session.cookies['sessionid']
        print(f"   Session key: {session_key}")
    else:
        print("   ⚠ No session cookie was created")
    
    # Step 4: Try to access another page to see if session persists
    print("\n3. Testing session persistence...")
    response = session.get(f"{base_url}/login/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if session.cookies.get('sessionid'):
        print("   ✓ Session cookie persists")
    else:
        print("   ⚠ Session cookie lost")
    
    print("\n=== Test Complete ===")

def test_google_oauth_session():
    """Test Google OAuth session handling"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("\n=== Testing Google OAuth Session ===")
    
    # Step 1: Access login page to get initial session
    print("\n1. Getting initial session...")
    response = session.get(f"{base_url}/login/")
    print(f"   Initial session cookies: {dict(session.cookies)}")
    
    # Step 2: Initiate Google OAuth
    print("\n2. Initiating Google OAuth...")
    response = session.get(f"{base_url}/google-login/", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies after OAuth initiation: {dict(session.cookies)}")
    
    if response.status_code == 302:
        redirect_url = response.headers.get('Location', '')
        if 'accounts.google.com' in redirect_url:
            print("   ✓ Successfully redirected to Google OAuth")
            
            # Extract state parameter from redirect URL
            import urllib.parse
            parsed_url = urllib.parse.urlparse(redirect_url)
            query_params = urllib.parse.parse_qs(parsed_url.query)
            state = query_params.get('state', [None])[0]
            print(f"   OAuth state: {state}")
            
            if session.cookies.get('sessionid'):
                print("   ✓ Session cookie maintained during OAuth initiation")
            else:
                print("   ⚠ No session cookie during OAuth initiation")
        else:
            print(f"   ⚠ Unexpected redirect: {redirect_url}")
    else:
        print("   ⚠ No redirect received")
    
    print("\n=== OAuth Test Complete ===")

if __name__ == "__main__":
    test_session_creation()
    test_google_oauth_session() 