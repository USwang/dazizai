import os.path

from flask import (Blueprint,
                   request,
                   render_template,
                   jsonify,
                   current_app,
                   make_response,
                   session,
                   redirect,
                   g, url_for)
import string
import random

from flask_jwt_extended import create_access_token
from flask_mail import Message
from flask_paginate import get_page_parameter, Pagination

from exts import mail,cache
from utils import restful
from utils.captcha import Captcha
import time
from hashlib import md5
from io import BytesIO
from .forms import RegisterForm, LoginForm, UploadAvatarForm, SetSignatureForm, UploadImageForm, PublicPostForm, \
    PublicCommentForm
from models import UserModel, Stockdatabase, PostModel, BoardModel, CommentModel
from exts import db
from .decorators import login_required
from flask_avatars import Identicon
from sqlalchemy.sql import func

bp = Blueprint("apps", __name__, url_prefix='/')


#befor_request
@bp.before_request
def front_before_request():
    if 'user_id' in session:
        user_id = session.get('user_id')
        user = UserModel.query.get(user_id)
        setattr(g, "user", user)
@bp.context_processor
def front_context_processor():
    if hasattr(g, "user"):
        return {"user": g.user}
    else:
        return {}

@bp.route('/')
def index():
    sort = request.args.get("st",type=int,default=1)
    # posts = PostModel.query.order_by(PostModel.create_time.desc()).all()
    post_query = None
    if sort == 1:
        post_query = PostModel.query.order_by(PostModel.create_time.desc())
    else:
        post_query = db.session.query(PostModel).outerjoin(CommentModel).group_by(
            PostModel.id).order_by(func.count(CommentModel.id).desc(),PostModel.create_time.desc())

    total = post_query.count()
    page = request.args.get(get_page_parameter(), type=int, default=1)
    per_page = request.args.get("per_page", type=int, default=current_app.config['PER_PAGE_COUNT'])
    # print(page)
    start = (page-1)*current_app.config['PER_PAGE_COUNT']
    end = start+current_app.config['PER_PAGE_COUNT']
    posts = post_query.slice(start, end)
    pagination = Pagination(bs_version=3, page=page, link_size='sm',
                            prev_label='上一页',next_label='下一页',
                            per_page=per_page, total=total)
    # pagination = Pagination(page=page, per_page=per_page, total=total,
    #                         search=False, record_name='items',
    #                         css_framework='bootstrap4',
    #                         link_size='sm',
    #                         show_single_page=False,
    #                         page_parameter='page',
    #                         per_page_parameter='per_page')
    # boards = BoardModel.query.order_by(BoardModel.create_time.desc()).all()
    context = {
        "posts": posts,
        "pagination": pagination,
        "st": sort
    }
    return render_template('front/index.html', **context)


@bp.get('/cms')
def cms():
    return render_template('cms/index.html')

@bp.route('/post/public/',methods=['GET','POST'])
@login_required
def public_post():
    if request.method=="GET":   #如果GET访问就返回主页
        posts = PostModel.query.all()
        return render_template("front/index.html",posts=posts)
    else:
        form = PublicPostForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            board_id = form.board_id.data
            try:
                board = BoardModel.query.get(board_id)
            except Exception as e:
                return restful.params_error(message="板块不存在!")
            post_model = PostModel(title=title,content=content,board = board,author=g.user)
            db.session.add(post_model)
            db.session.commit()
            return restful.ok(data={"id":post_model.id})
        else:
            return restful.params_error(message=form.messages[0])


@bp.get("/email/captcha")  #直接get模式
def email_captcha():
    #/email/captcha?email=wangshiyu217@163.com
    email = request.args.get("email")
    if not email:
        return restful.params_error(message="请先传入邮箱！")
    source = list(string.digits)
    captcha = "".join(random.sample(source,4))
    subject = "【自游数据】您的注册验证码:%s" % captcha
    recipients = [email]
    body = "【自游数据】您的注册码为：%s" % captcha
    current_app.celery.send_task("send_mail", (email, subject, body))
    cache.set(email, captcha)
    # print(cache.get(email))
    return restful.ok(message="邮件发送成功！")


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
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            remember = form.remember.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                return restful.params_error("邮箱或密码错误！")
            if not user.check_password(password):
                return restful.params_error("邮箱或密码错误！")
            session['user_id'] = user.id
            #如果是员工，才生成token
            token = ""
            if user.is_internal_employee:
                token = create_access_token(identity=user.id)
            if remember==1:
                # 默认浏览器关闭则过期
                session.permanent = True
            return restful.ok(data={"token": token, "user": user.to_dict()})
        else:
            return restful.params_error(message=form.messages[0])

@bp.route("/logout/")
def logout():
    session.clear()
    return redirect('/')


@bp.route('/register/',methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template("front/register.html")
    else:
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            identicon = Identicon()
            filenames = identicon.generate(text=md5(email.encode('utf-8')).hexdigest())
            avatar = filenames[2]
            user = UserModel(email=email,username=username,password=password,avatar=avatar)
            db.session.add(user)
            db.session.commit()
            return restful.ok()

        else:
            message = form.messages[0]
            return restful.params_error(message=message)


@bp.route('/setting/')
@login_required
def setting():
    email_hash = md5(g.user.email.encode("utf-8")).hexdigest()
    return render_template('front/setting.html',email_hash=email_hash)

@bp.post("/avatar/upload/")
@login_required
def upload_avatar():
    form = UploadAvatarForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email+str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['AVATARS_SAVE_PATH'], filename)
        image.save(image_path)
        g.user.avatar = filename
        db.session.commit()
        return restful.ok(data={'avatar': filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.post("/signature/edit/")
@login_required
def set_signature():
    form = SetSignatureForm(request.form)
    if form.validate():
        signature = form.signature.data
        g.user.signature = signature
        db.session.commit()
        return restful.ok()
    else:
        return restful.params_error(message=form.messages[0])


@bp.post("/post/image/upload")
@login_required
def upload_post_image():
    form = UploadImageForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email+str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['POST_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)
        return jsonify({"errno": 0,
                        "data": {
                        "url": url_for("media.get_post_image",filename=filename),
                        "alt": filename,
                        "href": ""
                        }})
    else:
        message = form.messages[0]
        return jsonify({
                    "errno": 1,
                    "message": message
                })


@bp.get("/post/detail/<post_id>")
def post_detail(post_id):
    try:
        post_model = PostModel.query.get(post_id)
    except:
        return "404"
    comment_count = CommentModel.query.filter_by(post_id=post_id).count()
    context = {
        "post":post_model,
        "comment_count":comment_count
    }
    return render_template("front/post_detail.html",**context)


@bp.post("/comment")
@login_required
def public_comment():
    form = PublicCommentForm(request.form)
    if form.validate():
        content = form.content.data
        post_id = form.post_id.data
        try:
            post_model = PostModel.query.get(post_id)
        except Exception as e:
            return restful.params_error(message="贴子不存在！")
        comment = CommentModel(content=content,post_id=post_id,author_id=g.user.id)
        db.session.add(comment)
        db.session.commit()
        return restful.ok()
    else:
        message = form.messages[0]
        return restful.params_error(message=message)