"""
Custom middleware for session management
"""
import logging

logger = logging.getLogger(__name__)

class SessionMiddleware:
    """
    Custom middleware to ensure session cookies are properly maintained
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        
        # Ensure session cookie is set if session exists
        if hasattr(request, 'session') and request.session.session_key:
            # Always set the session cookie to ensure consistency
            current_cookie = request.COOKIES.get('sessionid')
            if current_cookie != request.session.session_key:
                # Clear ALL possible conflicting cookies first
                response.delete_cookie('sessionid', path='/')
                response.delete_cookie('sessionid', path='')
                response.delete_cookie('sessionid')
                # Set the correct session cookie with domain=None
                response.set_cookie(
                    'sessionid', 
                    request.session.session_key, 
                    max_age=86400,  # 24 hours
                    httponly=True,
                    samesite='Lax',
                    path='/',
                    domain=None
                )
                logger.debug(f"SessionMiddleware: Set session cookie {request.session.session_key}")
            else:
                # Even if it's the same, ensure the cookie is set with proper attributes
                response.set_cookie(
                    'sessionid', 
                    request.session.session_key, 
                    max_age=86400,  # 24 hours
                    httponly=True,
                    samesite='Lax',
                    path='/'
                )
        
        return response 