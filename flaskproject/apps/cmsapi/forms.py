from wtforms import Form
from wtforms.fields import FileField, StringField, IntegerField
from flask_wtf.file import FileAllowed, FileSize
from wtforms.validators import InputRequired


class BaseForm(Form):
    @property
    def messages(self):
        message_list = []
        if self.errors:
            for errors in self.errors.values():
                message_list.extend(errors)
            return message_list


class UploadBannerForm(BaseForm):
    image = FileField(validators=[FileAllowed(['jpg','jpeg','png'],message='请上传.jpg .jpeg .png等格式图片'),
                                  FileSize(max_size=1024*1024*5,message='图片最大不超过5M')])


class AddBannerForm(BaseForm):
    name = StringField(validators=[InputRequired(message='请输入轮播图名称！')])
    image_url = StringField(validators=[InputRequired(message='请输入轮播图片链接！')])
    link_url = StringField(validators=[InputRequired(message='请输入轮播图跳转链接！')])
    priority = IntegerField(validators=[InputRequired(message='请输入轮播图优先级!')])