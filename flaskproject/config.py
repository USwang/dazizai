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
MAIL_PASSWORD = "LANTMMHYHCGAWNSE"
MAIL_DEFAULT_SENDER = "wangshiyu217@163.com"