#!/usr/bin/env python
"""
Test script to verify session handling fix for Google OAuth vs Password login
"""
import requests
import json

def test_session_handling():
    """Test session handling for both password and Google OAuth login"""
    
    base_url = "http://127.0.0.1:8000"
    
    print("=== Testing Session Handling Fix ===")
    
    # Test 1: Password Login Session
    print("\n1. Testing Password Login Session...")
    session1 = requests.Session()
    
    # Simulate password login (you'll need to replace with actual credentials)
    login_data = {
        'email': 'test@example.com',  # Replace with actual test user
        'password': 'testpassword'    # Replace with actual test password
    }
    
    response = session1.get(f"{base_url}/searchlogin/", params=login_data)
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session1.cookies)}")
    
    if session1.cookies.get('sessionid'):
        print(f"   ✅ Session created: {session1.cookies['sessionid']}")
        
        # Test session persistence
        response = session1.get(f"{base_url}/userhome/")
        print(f"   Home page status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Session persists correctly")
        else:
            print("   ❌ Session lost")
    else:
        print("   ⚠ No session created")
    
    # Test 2: Google OAuth Session (simulation)
    print("\n2. Testing Google OAuth Session...")
    session2 = requests.Session()
    
    # Get initial session from OAuth initiation
    response = session2.get(f"{base_url}/google-login/", allow_redirects=False)
    print(f"   OAuth initiation status: {response.status_code}")
    print(f"   Initial session cookies: {dict(session2.cookies)}")
    
    if session2.cookies.get('sessionid'):
        print(f"   ✅ Initial session created: {session2.cookies['sessionid']}")
        
        # Simulate OAuth callback with invalid code (should maintain session)
        redirect_url = response.headers.get('Location', '')
        import urllib.parse
        parsed_url = urllib.parse.urlparse(redirect_url)
        query_params = urllib.parse.parse_qs(parsed_url.query)
        state = query_params.get('state', [None])[0]
        
        callback_params = {
            'code': 'invalid_code_for_testing',
            'state': state
        }
        
        response = session2.get(f"{base_url}/google-login-callback/", params=callback_params)
        print(f"   Callback status: {response.status_code}")
        print(f"   Session cookies after callback: {dict(session2.cookies)}")
        
        if session2.cookies.get('sessionid'):
            print(f"   ✅ Session maintained: {session2.cookies['sessionid']}")
        else:
            print("   ❌ Session lost during callback")
    else:
        print("   ⚠ No initial session created")
    
    # Test 3: Session Test Endpoint
    print("\n3. Testing Session Test Endpoint...")
    if session1.cookies.get('sessionid'):
        response = session1.get(f"{base_url}/test-session/")
        print(f"   Test endpoint status: {response.status_code}")
        print(f"   Response: {response.text}")
    
    print("\n=== Test Complete ===")
    print("If both sessions are maintained correctly, the fix is working!")

if __name__ == "__main__":
    test_session_handling() 