from exts import db


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
    datajson = db.Column(db.JSON, nullable=True)


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

