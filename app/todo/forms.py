# encoding=utf-8
"""
Date:2019-09-08 17:12
User:LiYu
Email:liyu_5498@163.com

"""
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models import Category
from flask_login import current_user


class AddTodoForm(FlaskForm):
    content = StringField(
        label='任务内容',
        validators=[DataRequired()]

    )
    category = SelectField(
        label='任务类型',
        coerce=int,  # 存的是id整形
        # choices=[(item.id, item.name) for item in Category.query.all()]

    )
    submit = SubmitField(
        label='添加任务',

    )

    def __init__(self):
        super(AddTodoForm, self).__init__()
        # 用户可以选择的分类是该用户创建的所有分类  current_user
        # 获取当前登录用户创建的所有分类;
        categories = Category.query.filter_by(user_id=current_user.id).all()
        if categories:
            self.category.choices = [(item.id, item.name) for item in categories]
        else:
            self.category.choices = [(-1, "请先创建分类")]


class EditTodoForm(FlaskForm):
    content = StringField(
        label='任务内容',
        validators=[DataRequired()]

    )
    category = SelectField(
        label='任务类型',
        coerce=int,  # 存的是id整形
        # choices=[(item.id, item.name) for item in Category.query.all()]

    )
    submit = SubmitField(
        label='编辑任务',

    )

    def __init__(self):
        super(EditTodoForm, self).__init__()
        categories = Category.query.filter_by(user_id=current_user.id).all()
        if categories:
            self.category.choices = [(item.id, item.name) for item in categories]
        else:
            self.category.choices = [(-1, "请先创建分类")]


class AddCategoryForm(FlaskForm):
    content = StringField(label='分类名称',
                          validators=[DataRequired()]

                          )
    submit = SubmitField(
        label='添加分类',

    )
