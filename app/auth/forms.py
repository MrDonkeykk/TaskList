# encoding=utf-8
"""
Date:2019-09-08 17:12
User:LiYu
Email:liyu_5498@163.com

"""
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, ValidationError
from app.models import User


class RegistrationForm(FlaskForm):
    """用户注册表单"""
    email = StringField(
        '电子邮箱',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(message=u'邮箱格式错误')
        ],
        render_kw={
            "placeholder": "电子邮箱"
        }
    )
    username = StringField(
        '用户名',
        validators=[
            DataRequired(),
            Length(1, 64),
            Regexp(r'^\w*$', message=u'用户名只能由字母数字或者下划线组成')
        ],
        render_kw={
            "placeholder": "用户名"
        }
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired(),
        ],
        render_kw={
            "placeholder": "密码"
        }
    )
    repassword = PasswordField(
        '确认密码',
        validators=[
            DataRequired(),
            EqualTo('password', message='密码不一致')
        ],
        render_kw={
            "placeholder": "确认密码"
        }
    )
    submit = SubmitField(
        '注册'
    )

    # 两个自定义的验证函数, 以validate_ 开头且跟着字段名的方法,这个方法和常规的验证函数一起调用。
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            # 自定义的验证函数要想表示验证失败,可以抛出 ValidationError 异常,其参数就是错误消息。
            raise ValidationError('电子邮箱已经注册.')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('用户名已经占用.')


class LoginForm(FlaskForm):
    """用户登录表单"""
    email = StringField(
        '电子邮箱',
        validators=[
            DataRequired(),
            Length(1, 64),
            Email(message=u'邮箱格式错误')
        ],
        render_kw={
            "placeholder": "电子邮箱",
            'class': 'layui-input',
            'lay-verify': 'required'
        }
    )
    password = PasswordField(
        '密码',
        validators=[
            DataRequired()
        ],
        render_kw={
            "placeholder": "密码",
            'class': 'layui-input',
            'lay-verify': 'required'
        }
    )
    submit = SubmitField(
        '登录'
    )
