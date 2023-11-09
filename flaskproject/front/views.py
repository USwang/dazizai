from flask import Blueprint, request, render_template

bp = Blueprint("front", __name__, url_prefix='/')


@bp.route('/login',methods=['GET','POST'])
def loging():
    if request.method =='GET':
        return render_template("")