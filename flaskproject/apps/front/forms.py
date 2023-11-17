from wtforms import Form,ValidationError
from wtforms.fields import StringField
from wtforms.validators import Email, length, EqualTo

from exts import cache
from models import UserModel


class RegisterForm(Form):
    email = StringField(validators=[Email(message="请输入正确的邮箱！")])
    email_captcha = StringField(validators=[length(4,4,message="请输入正确的验证码！")])
    username = StringField(validators=[length(3,30,message="请输入正确长度的用户名！")])
    password = StringField(validators=[length(6,20,message="请输入正确长度的密码！")])
    repeat_password = StringField(validators=[EqualTo("password",message="两次密码不一致！")])
    graph_captcha = StringField(validators=[length(4,4,message="请输入正确长度的图形验证码！")])

    def validate_email(self,field):
        email = field.data
        user = UserModel.query.filter_by(email =email).first()
        if user:
            raise ValidationError(message="邮箱已经被注册！")

    def validate_email_captcha(self,field):
        email_captcha = field.data
        email = self.email.data
        cache_captcha = cache.get(email)
        if not cache_captcha or email_captcha != cache_captcha:
            raise ValidationError(message="邮箱验证码错误！")
