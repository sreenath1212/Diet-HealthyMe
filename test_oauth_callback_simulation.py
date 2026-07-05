#!/usr/bin/env python
"""
Test script to simulate OAuth callback and check session handling
"""
import requests
import json

def test_oauth_callback_simulation():
    """Simulate OAuth callback and check session handling"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("=== Testing OAuth Callback Simulation ===")
    
    # Step 1: Get initial session from OAuth initiation
    print("\n1. Getting initial session from OAuth...")
    response = session.get(f"{base_url}/google-login/", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if not session.cookies.get('sessionid'):
        print("   ⚠ No session created, cannot continue test")
        return
    
    session_key = session.cookies['sessionid']
    print(f"   Session key: {session_key}")
    
    # Step 2: Extract state from redirect URL
    redirect_url = response.headers.get('Location', '')
    import urllib.parse
    parsed_url = urllib.parse.urlparse(redirect_url)
    query_params = urllib.parse.parse_qs(parsed_url.query)
    state = query_params.get('state', [None])[0]
    print(f"   OAuth state: {state}")
    
    # Step 3: Simulate callback with invalid code (should show error but maintain session)
    print("\n2. Simulating OAuth callback with invalid code...")
    callback_params = {
        'code': 'invalid_code_for_testing',
        'state': state
    }
    
    response = session.get(f"{base_url}/google-login-callback/", params=callback_params)
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies after callback: {dict(session.cookies)}")
    
    # Check if session was maintained
    if session.cookies.get('sessionid'):
        print("   ✓ Session cookie maintained after callback")
        if session.cookies['sessionid'] == session_key:
            print("   ✓ Session key unchanged")
        else:
            print(f"   ⚠ Session key changed: {session.cookies['sessionid']}")
    else:
        print("   ⚠ Session cookie lost after callback")
    
    # Step 4: Test what happens when we try to access userhome
    print("\n3. Testing userhome access after callback...")
    response = session.get(f"{base_url}/userhome/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if "Please login first" in response.text:
        print("   ✓ Correctly requires login (expected for invalid OAuth)")
    else:
        print("   ⚠ Unexpected response")
    
    print("\n=== Callback Simulation Complete ===")

def test_session_with_valid_data():
    """Test session with valid user data"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("\n=== Testing Session with Valid Data ===")
    
    # Step 1: Get session from OAuth initiation
    print("\n1. Getting session from OAuth...")
    response = session.get(f"{base_url}/google-login/", allow_redirects=False)
    session_key = session.cookies.get('sessionid')
    print(f"   Session key: {session_key}")
    
    # Step 2: Try to access userhome with session
    print("\n2. Testing userhome with session...")
    response = session.get(f"{base_url}/userhome/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if "Please login first" in response.text:
        print("   ✓ Correctly requires login (no user data in session)")
    else:
        print("   ⚠ Unexpected response")
    
    print("\n=== Valid Data Test Complete ===")

if __name__ == "__main__":
    test_oauth_callback_simulation()
    test_session_with_valid_data() 