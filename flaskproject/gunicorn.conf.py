import multiprocessing

bind = "127.0.0.1:5000"
workers = multiprocessing.cpu_count()*2+1
threads = 10
accesslog = "/var/log/flaskproject/access.log"
errorlog = "/var/log/flaskproject/error.log"
daemon = True