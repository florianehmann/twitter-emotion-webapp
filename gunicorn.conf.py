"""Configuration of the Gunicorn WSGI Server"""
# pylint: disable=invalid-name

wsgi_app = 'app_entry:app'

accesslog = 'logs/access.log'
access_log_format = '%({x-forwarded-for}i)s %(t)s "%(r)s" %(s)s "%(f)s" "%(a)s"'
errorlog = 'logs/error.log'
loglevel = 'error'

bind = ':5000'
