import logging
import time
from django.conf import settings
from django.db import connection

class LoggingMiddleware(object):
    
    def __init__(self,get_response) -> None:
        self.start_time = time.time()
        self.get_response = get_response
        

    def __call__(self, request):
        response = self.get_response(request)
        try:    
            remote_addr = request.META.get('REMOTE_ADDR')    
            if remote_addr in getattr(settings, 'INTERNAL_IPS', []):
                remote_addr = request.META.get('HTTP_X_FORWARDED_FOR') or remote_addr
            user_email = "-" 
            extra_log = ""
            if hasattr(request,'user'):
                user_email = getattr(request.user, 'email', '-')
            req_time = time.time() - self.start_time
            content_len = len(response.content)
            if settings.DEBUG:
                sql_time = sum(float(q['time']) for q in connection.queries) * 1000
                extra_log += " (%s SQL queries, %s ms)" % (len(connection.queries), sql_time)
            logging.info("%s %s %s %s %s %s (%.02f seconds)%s" % (remote_addr, user_email, request.method, request.get_full_path(), response.status_code, content_len, req_time, extra_log))
        except Exception as e:
            logging.error("LoggingMiddleware Error: %s" % e)
        return response