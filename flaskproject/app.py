from flask import Flask,render_template, request, url_for
import config
from exts import db
from models import Stockdata, Stocklist
from flask_migrate import Migrate
from eastmoneystockdataget import getjson_stockdata
from eastmoneystocklistget import getjson_stocklist, pageNumber

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
migrate = Migrate(app, db)


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello Wo'


@app.route('/update/stockdata/',methods=['GET','POST'])
def update_stockdata():
    if request.method == 'GET':
        return render_template('stockdata.html')
    else:
        # 验证密码
        username = request.form.get('username')
        password = request.form.get('password')
        # 更新数据库
        if username == 'wsy'and password == 'mtjb1..':
            lies = db.session.query(Stocklist).all()
            for li in lies:
                SECURITY_CODE = li.SECURITY_CODE
                SECURITY_NAME_ABBR = li.SECURITY_NAME_ABBR
                da = db.session.query(Stockdata).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                datajson = getjson_stockdata(SECURITY_CODE)
                if da:
                    da.datajson=datajson
                    db.session.commit()
                else:
                    stockdata = Stockdata(SECURITY_CODE=SECURITY_CODE, SECURITY_NAME_ABBR=SECURITY_NAME_ABBR, datajson=datajson)
                    db.session.add(stockdata)
                    db.session.commit()
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
                li = db.session.query(Stocklist).filter_by(SECURITY_CODE=SECURITY_CODE).first()
                # print(bool(li))
                if li:
                    li.SECURITY_CODE = SECURITY_CODE
                    li.SECURITY_NAME_ABBR = SECURITY_NAME_ABBR
                    db.session.commit()
                else:
                    stocklist = Stocklist(SECURITY_CODE=SECURITY_CODE, SECURITY_NAME_ABBR=SECURITY_NAME_ABBR)
                    db.session.add(stocklist)
                    db.session.commit()
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