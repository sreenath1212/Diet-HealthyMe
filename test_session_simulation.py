#!/usr/bin/env python
"""
Test script to simulate session behavior after Google OAuth callback
"""
import requests
import json

def test_session_simulation():
    """Simulate session behavior after OAuth callback"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("=== Testing Session Simulation ===")
    
    # Step 1: Access login page to get initial session
    print("\n1. Getting initial session...")
    response = session.get(f"{base_url}/login/")
    print(f"   Initial session cookie: {dict(session.cookies)}")
    
    # Step 2: Simulate what happens after OAuth callback
    # We'll directly access the callback URL with mock data
    print("\n2. Simulating OAuth callback...")
    
    # Mock OAuth parameters (this won't work with real Google, but tests the flow)
    mock_params = {
        'code': 'mock_authorization_code',
        'state': 'mock_state'
    }
    
    try:
        response = session.get(f"{base_url}/google-login-callback/", params=mock_params)
        print(f"   Status: {response.status_code}")
        print(f"   Session cookies after callback: {dict(session.cookies)}")
        
        if response.status_code == 200:
            if "Google OAuth error" in response.text or "No authorization code" in response.text:
                print("   [OK] Correctly handles invalid OAuth parameters")
            else:
                print("   [WARN] Unexpected response")
        else:
            print(f"   [WARN] Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    # Step 3: Test session persistence
    print("\n3. Testing session persistence...")
    try:
        response = session.get(f"{base_url}/userhome/")
        print(f"   Status: {response.status_code}")
        print(f"   Session cookies: {dict(session.cookies)}")
        
        if "Please login first" in response.text:
            print("   [OK] Session correctly shows not logged in")
        else:
            print("   [WARN] Unexpected session state")
            
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n=== Test Complete ===")

def test_regular_login_comparison():
    """Test regular login for comparison"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("\n=== Testing Regular Login Comparison ===")
    
    # Step 1: Access login page
    print("\n1. Accessing login page...")
    response = session.get(f"{base_url}/login/")
    print(f"   Session cookie: {dict(session.cookies)}")
    
    # Step 2: Try to access userhome (should fail)
    print("\n2. Testing userhome access without login...")
    response = session.get(f"{base_url}/userhome/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookie: {dict(session.cookies)}")
    
    if "Please login first" in response.text:
        print("   [OK] Correctly requires login")
    else:
        print("   [WARN] Unexpected response")
    
    print("\n=== Comparison Complete ===")

if __name__ == "__main__":
    test_session_simulation()
    test_regular_login_comparison() 