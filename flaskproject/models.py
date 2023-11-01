from exts import db


class Stockdata(db.Model):
    __tablename__ = 'stock_data'
    # stock 代码
    id = db.Column(db.Integer, primary_key=True)
    # stock 名称
    stockname = db.Column(db.String(50), unique=True, nullable=True)
    # 市场标签 沪，深，创，科创
    markettag = db.Column(db.String(50), nullable=True)
    # 数据
    datajson = db.Column(db.JSON, nullable=True)