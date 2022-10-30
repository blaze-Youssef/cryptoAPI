bind = "127.0.0.1:8000"
workers = 4
timeout = 60

worker_class = "uvicorn.workers.UvicornWorker"
loglevel = "debug"
accesslog = "/home/ubuntu/log/access/access_log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
errorlog = "/home/ubuntu/log/error/error_log"
