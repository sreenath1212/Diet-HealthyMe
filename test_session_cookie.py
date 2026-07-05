#!/usr/bin/env python
"""
Test script to verify session cookie handling
"""
import requests
import json

def test_session_cookie_handling():
    """Test session cookie handling"""
    
    base_url = "http://127.0.0.1:8000"
    session = requests.Session()
    
    print("=== Testing Session Cookie Handling ===")
    
    # Step 1: Access login page
    print("\n1. Accessing login page...")
    response = session.get(f"{base_url}/login/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    # Step 2: Initiate Google OAuth
    print("\n2. Initiating Google OAuth...")
    response = session.get(f"{base_url}/google-login/", allow_redirects=False)
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if session.cookies.get('sessionid'):
        print("   ✓ Session cookie created")
        session_key = session.cookies['sessionid']
        print(f"   Session key: {session_key}")
    else:
        print("   ⚠ No session cookie created")
        return
    
    # Step 3: Test session persistence across requests
    print("\n3. Testing session persistence...")
    response = session.get(f"{base_url}/login/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if session.cookies.get('sessionid') == session_key:
        print("   ✓ Session cookie maintained")
    else:
        print("   ⚠ Session cookie changed or lost")
    
    # Step 4: Test userhome access
    print("\n4. Testing userhome access...")
    response = session.get(f"{base_url}/userhome/")
    print(f"   Status: {response.status_code}")
    print(f"   Session cookies: {dict(session.cookies)}")
    
    if "Please login first" in response.text:
        print("   ✓ Correctly requires login (expected)")
    else:
        print("   ⚠ Unexpected response")
    
    print("\n=== Test Complete ===")
    print("\nNote: The session cookie should be maintained across all requests.")
    print("If you see different session keys, there's a session continuity issue.")

if __name__ == "__main__":
    test_session_cookie_handling() 