from flask import Blueprint, request, render_template, jsonify, current_app, make_response
import string
import random
from flask_mail import Message
from exts import mail,cache
from utils.captcha import Captcha
import time
from hashlib import md5
from io import BytesIO

bp = Blueprint("apps", __name__, url_prefix='/')


@bp.route('/')
def index():
    return 'hello worl'
    # stockdatas = Stockdatabase.query.all()  # 查询所有数据
    # return render_template('index.html', stockdatas=stockdatas)


# @bp.get("/email/captcha")  #直接get模式
# def email_captcha():
#     #/email/captcha?email=wangshiyu217@163.com
#     email = request.args.get("email")
#     if not email:
#         return jsonify({"code":400,"message":"请先输入邮箱！"})
#     source = list(string.digits)
#     captcha = "".join(random.sample(source,4))
#     message = Message(subject="【自游数据】注册验证码",recipients=[email],body="【自游数据】您的注册码为：%s"%captcha)
#     try:
#         mail.send(message)
#     except Exception as e:
#         print("邮件发送失败")
#         print(e)
#         return jsonify({"code":500,"message":"邮件发送失败！"})
#     return jsonify({"code":200,"message":"邮件发送成功！"})

@bp.get("/email/captcha")  #直接get模式
def email_captcha():
    #/email/captcha?email=wangshiyu217@163.com
    email = request.args.get("email")
    if not email:
        return jsonify({"code":400,"message":"请先输入邮箱！"})
    source = list(string.digits)
    captcha = "".join(random.sample(source,4))
    subject = "【自游数据】注册验证码"
    recipients = [email]
    body = "【自游数据】您的注册码为：%s" % captcha
    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, captcha)
    # print(cache.get(email))
    return jsonify({"code":200,"message":"邮件发送成功！"})


@bp.route('/graph/captcha/')
def graph_captcha():
    captcha, image = Captcha.gene_graph_captcha()
    #key, value
    key = md5((captcha+str(time.time())).encode('utf-8')).hexdigest()
    cache.set(key,captcha)
    out = BytesIO()
    image.save(out,'png')
    out.seek(0)
    resp = make_response(out.read())
    resp.content_type = 'image/png'
    resp.set_cookie("_graph_captcha_key",key,max_age = 3600)
    return resp


@bp.route('/login/',methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("front/login.html")


@bp.route('/register/',methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        pass
