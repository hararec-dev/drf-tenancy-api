import multiprocessing
import os

os.makedirs("logs", exist_ok=True)

bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 30
keepalive = 2
loglevel = "info"
accesslog = "logs/gunicorn-access.log"
errorlog = "logs/gunicorn-error.log"
capture_output = True
max_requests = 1000
max_requests_jitter = 50
