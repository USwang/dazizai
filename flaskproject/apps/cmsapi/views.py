import os
from datetime import time
from hashlib import md5
import time
from flask import Blueprint, request, g, current_app
from models import UserModel, PostModel
from exts import db
from utils import restful
from flask_jwt_extended import jwt_required, get_jwt_identity
from apps.cmsapi.forms import UploadBannerForm, AddBannerForm

bp = Blueprint("cmsapi", __name__, url_prefix='/cmsapi')


@bp.before_request
@jwt_required()
def cmsapi_before_request():
    if request.method=="OPTIONS":
        return
    identity = get_jwt_identity()
    user = UserModel.query.filter_by(id=identity).first()
    if user:
        setattr(g, "user", user)
@bp.get("/")
@jwt_required()
def mytest():
    # 这个
    identity =get_jwt_identity()
    return restful.ok(message='success',data={'identity':identity})


@bp.post("/banner/image/upload")
@jwt_required()
def upload_banner_image():
    form = UploadBannerForm(request.files)
    if form.validate():
        image = form.image.data
        filename = image.filename
        _, ext = os.path.splitext(filename)
        filename = md5((g.user.email + str(time.time())).encode("utf-8")).hexdigest() + ext
        image_path = os.path.join(current_app.config['BANNER_IMAGE_SAVE_PATH'], filename)
        image.save(image_path)
        return restful.ok(data={'image_url': filename})
    else:
        message = form.messages[0]
        return restful.params_error(message=message)


@bp.get("/post/list")
def post_list():
    page = request.args.get('page',default=1,type=int)
    per_page_count = current_app.config['PER_PAGE_COUNT']
    start = (page-1)*per_page_count
    end = start + per_page_count
    query_obj = PostModel.query.order_by(PostModel.create_time.desc())
    total_count = query_obj.count()
    posts = query_obj.slice(start, end)
    post_list = [post.to_dict() for post in posts]
    return restful.ok(data={'total_count':total_count,'post_list': post_list})


@bp.post('/banner/add')
def add_banner():
    pass


