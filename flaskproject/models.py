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


#隐私设置
# class BoardModel(db.Model):
#     __tablename__ = "board"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(20), default="公开/public")
#     password = db.Column(db.String(20), default="公开/public")
#     create_time = db.Column(db.DateTime, default=datetime)


class PostModel(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime)
    author_id = db.Column(db.String(100),db.ForeignKey("user.id"))

    author = db.relationship("UserModel",backref=db.backref("posts"))


class CommentModel(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime,default=datetime)
    post_id = db.Column(db.Integer,db.ForeignKey("post.id"))
    author_id = db.Column(db.String(100),db.ForeignKey("user.id"),nullable=False)

    post = db.relationship("PostModel",backref=db.backref('comments',
                           order_by="CommentModel.create_time.desc()",cascade="delete,delete-orphan"))
    author = db.relationship("UserModel",backref=db.backref("comments"))


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

