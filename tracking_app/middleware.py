from django.contrib.sessions.backends.db import SessionStore


# Middleware to save the session_key between different sessions
class SessionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        session_key = request.COOKIES.get('session_key')

        if session_key:
            # Set the session key if it exists
            request.session = SessionStore(session_key)

        response = self.get_response(request)

        return response
