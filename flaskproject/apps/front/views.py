from flask import Blueprint, request, render_template

bp = Blueprint("apps", __name__, url_prefix='/')


@bp.route('/')
def index():
    return 'hello world'
    # stockdatas = Stockdatabase.query.all()  # 查询所有数据
    # return render_template('index.html', stockdatas=stockdatas)


@bp.route('/login',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")


@bp.route('/register',methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")