from flask import Flask, render_template, request, url_for
import config
from exts import db,mail
from models import Stockdatabase, UserModel
from flask_migrate import Migrate
from eastmoneystockdataget import getjson_stockdata
from eastmoneystocklistget import getjson_stocklist, pageNumber
from eastmoneyincomedataget import getjson_stockincome
from apps.front import front_bp
from bbs_celery import make_celery
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
mail.init_app(app)
migrate = Migrate(app, db)
mycelery = make_celery(app)

#注册蓝图
app.register_blueprint(front_bp)
@app.route('/update/stockprice/',methods=['GET','POST'])
def update_stockprice():
    if request.method == 'GET':
        return render_template('stockdata.html')
    else:
        # 验证密码
        username = request.form.get('username')
        password = request.form.get('password')
        # 更新数据库
        if username == 'wsy'and password == 'mtjb1..':
            lies = db.session.query(Stockdatabase).all()
            if bool(lies):
                for li in lies:
                    SECURITY_CODE = li.SECURITY_CODE
                    da = db.session.query(Stockdatabase).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                    pricedatajson = getjson_stockdata(SECURITY_CODE)
                    if da:
                        da.PRICE_datajson = pricedatajson
                        db.session.commit()
                    else:
                        stockdatabase = Stockdatabase(PRICE_datajson=pricedatajson)
                        db.session.add(stockdatabase)
                        db.session.commit()
            else:
                return "请先更新列表"
        else:
            return '用户名或密码不正确'
    return 'update finished'


@app.route('/update/stocklist/',methods=['GET', 'POST'])
def update_stocklist():
    if request.method == 'GET':
        return render_template('stocklist.html')
    else:
        # 验证密码
        username = request.form.get('username')
        password = request.form.get('password')
        # 更新数据库
        if username == 'wsy' and password == 'mtjb1..':
            totolPage = pageNumber()
            for page in range(totolPage):
                list_pages = getjson_stocklist(page + 1)
                for lists_page in list_pages:
                    SECURITY_CODE = lists_page['SECURITY_CODE']
                    SECURITY_NAME_ABBR = lists_page['SECURITY_NAME_ABBR']
                    # 判断是否已经在数据库，
                    li = db.session.query(Stockdatabase).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                    if bool(li):
                        li.SECURITY_CODE = SECURITY_CODE
                        li.SECURITY_NAME_ABBR = SECURITY_NAME_ABBR
                        db.session.commit()
                    else:
                        stockdatabase = Stockdatabase(SECURITY_CODE=SECURITY_CODE, SECURITY_NAME_ABBR=SECURITY_NAME_ABBR)

                        db.session.add(stockdatabase)
                        db.session.commit()
        else:
            return '用户名或密码不正确'
    return 'update finished'


@app.route('/update/stockincome/',methods=['GET', 'POST'])
def update_stockincome():
    if request.method == 'GET':
        return render_template('stockincome.html')
    else:
        # 验证密码
        username = request.form.get('username')
        password = request.form.get('password')
        # 更新数据库
        if username == 'wsy' and password == 'mtjb1..':
            lies = db.session.query(Stockdatabase).all() #获取stock列表
            if lies:
                for li in lies:
                    SECURITY_CODE = li.SECURITY_CODE
                    SECURITY_NAME_ABBR = li.SECURITY_NAME_ABBR
                    #判断是否存在
                    da = db.session.query(Stockdatabase).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                    income = getjson_stockincome(SECURITY_CODE)
                    if da:
                        da.INCOME_datajson = income
                        db.session.commit()
                    else:
                        stockdatabase = Stockdatabase(INCOME_datajson=income)
                        db.session.add(stockdatabase)
                        db.session.commit()
            else:
                return "请先更新列表"
        else:
            return '用户名或密码不正确'

    return 'update finished'
# @app.route('/search')
# def search():
#     username = request.args.get('username')  # 从请求参数中获取要搜索的用户名
#     users = User.query.filter_by(username=username).all()  # 使用 SQLAlchemy 查询该用户名的所有用户数据
#
#     if users:
#         return render_template('search.html', users=users)  # 渲染搜索结果页面，并传递用户数据
#     else:
#         return "没有找到相关用户"  # 如果未找到用户，返回相应的提示信息


if __name__ == '__main__':
    app.run()
