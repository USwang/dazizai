from flask import Blueprint
from utils import restful
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint("cmsapi", __name__, url_prefix='/cmsapi')

@bp.get("/")
@jwt_required()
def mytest():
    # 这个
    identity =get_jwt_identity()
    return restful.ok(message='success',data={'identity':identity})