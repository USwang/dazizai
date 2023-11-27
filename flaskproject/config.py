import os
from datetime import timedelta

SECRET_KEY = 'dazizai'

#session.permanent = True 的情况下过期时间
PERMANENT_SESSION_LIFETIME = timedelta(days=7)

#项目根路径
BASE_DIR = os.path.dirname(__file__)


HOSTNAME = '127.0.0.1'
PORT = '3306'
DATABASE = 'stockdata'
USERNAME = 'root'
PASSWORD = 'mtjb1..'
DB_URI = "mysql+pymysql://{username}:{password}@{host}:{port}/{db}?charset=utf8".format(username=USERNAME,
                                                                                        password=PASSWORD,
                                                                                        host=HOSTNAME, port=PORT,
                                                                                        db=DATABASE)
SQLALCHEMY_DATABASE_URI = DB_URI

MAIL_SERVER = "smtp.163.com"
MAIL_USE_SSL = True
MAIL_PORT = 465
MAIL_USERNAME = "wangshiyu217@163.com"
MAIL_PASSWORD = "LANTMMHYHCGAWNSE" #not true
MAIL_DEFAULT_SENDER = "wangshiyu217@163.com"

#celery的redis配置
CELERY_BROKER_URL = "redis://127.0.0.1:6379/0"
CELERY_RESULT_BACKEND = "redis://127.0.0.1:6379/0"

#flash-caching 的配置
CACHE_TYPE = "RedisCache"
CACHE_DEFAULT_TIMEOUT = 300
CACHE_REDIS_HOST = "127.0.0.1"
CACHE_REDIS_PORT = 6379

#头像配置
AVATARS_SAVE_PATH = os.path.join(BASE_DIR,"media","avatars")

#帖子图片路径
POST_IMAGE_SAVE_PATH = os.path.join(BASE_DIR,"media","post")