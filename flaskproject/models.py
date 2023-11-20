from exts import db
import shortuuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class UserModel(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(100),primary_key=True, default=shortuuid.uuid)
    email = db.Column(db.String(120), unique=True, nullable=True)
    mobile_number = db.Column(db.String(20), unique=True, nullable=True)
    username = db.Column(db.String(80), unique=True, nullable=False)  # 用户名字段
    _password = db.Column(db.String(120), nullable=False)  # 密码字段
    signature = db.Column(db.String(255), nullable=True)  # 个性签名字段
    avatar = db.Column(db.String(255), nullable=True)  # 头像字段
    registration_date = db.Column(db.DateTime, default=datetime.now)  # 注册时间字段
    is_internal_employee = db.Column(db.Boolean, default=False)  # 是否为内部员工字段
    is_active = db.Column(db.Boolean, default=True)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password = kwargs.get('password')
            kwargs.pop('password')
        super(UserModel,self).__init__(*args,**kwargs)

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self, rawpwd):
        return check_password_hash(self.password,rawpwd)


class Stockdatabase(db.Model):
    __tablename__ = 'stock_database'
    # stock 代码
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # stock code number
    SECURITY_CODE = db.Column(db.String(50), unique=True, nullable=True)
    # stock 名称
    SECURITY_NAME_ABBR = db.Column(db.String(50), nullable=True)
    # 市场标签 沪，深，创，科创
    # markettag = db.Column(db.String(50), nullable=True)
    # 数据
    PRICE_datajson = db.Column(db.JSON)
    INCOME_datajson = db.Column(db.JSON)

    def __repr__(self):
        return f'<Stockdatabase {self.SECURITY_CODE}>'


class Stockdata(db.Model):
    __tablename__ = 'stock_data'
    # stock 代码
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # stock code number
    SECURITY_CODE = db.Column(db.String(50), unique=True, nullable=True)
    # stock 名称
    SECURITY_NAME_ABBR = db.Column(db.String(50), nullable=True)
    # 市场标签 沪，深，创，科创
    # markettag = db.Column(db.String(50), nullable=True)
    # 数据

    INCOME_datajson = db.Column(db.JSON, nullable=True)


class Stocklist(db.Model):
    __tablename__ = 'stock_list'
    # stock 代码
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    # stock code number
    SECURITY_CODE = db.Column(db.String(50),unique=True,nullable=True)
    # stock 名称
    SECURITY_NAME_ABBR = db.Column(db.String(50), nullable=True)


class Stockincome(db.Model):
    __tablename__ = 'stock_income'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # stock code number
    SECURITY_CODE = db.Column(db.String(50), unique=True, nullable=True)
    # stock 名称
    SECURITY_NAME_ABBR = db.Column(db.String(50), nullable=True)
    # 数据
    INCOME_datajson = db.Column(db.JSON, nullable=True)

