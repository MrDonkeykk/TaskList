# encoding=utf-8
"""
Date:2019-09-08 17:12
User:LiYu
Email:liyu_5498@163.com

"""
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user

from app import db
from app.models import Todo, Category
from app.todo import todo
from app.todo.forms import AddTodoForm, AddCategoryForm


@todo.route('/add/', methods=['GET', 'POST'])
@login_required
def add():
    form = AddTodoForm()
    if form.validate_on_submit():
        # 获取用户提交的内容
        content = form.content.data
        category_id = form.category.data
        # 添加到数据库中
        todo = Todo(content=content,
                    category_id=category_id,
                    user_id=current_user.id

                    )
        db.session.add(todo)
        flash('添加任务成功', category='success')
        return redirect(url_for('todo.add'))
    return render_template('todo/add.html', form=form)


@todo.route('/category/add/', methods=['GET', 'POST'])
@login_required
def category_add():
    form = AddCategoryForm()
    if form.validate_on_submit():
        # 获取用户提交的内容
        content = form.content.data
        # 添加到数据库中
        category = Category(name=content, user_id=current_user.id)
        db.session.add(category)
        flash('添加分类成功', category='success')
        return redirect(url_for('todo.category_add'))
    return render_template('todo/category_add.html', form=form)


@todo.route('/delete/')
def delete():
    return 'todo delete'


# 查看任务
@todo.route('/list')
@login_required
def list():
    # 127.0.0.1:5000/todo/list?page=2 获取page对应的value值
    page = int(request.args['page'])
    print(type(page))
    # 任务显示需要分页,每个用户只能查看自己的任务

    # todos = Todo.query.filter_by(user_id=current_user.id).all()
    # page要显示第几页数据， per_page每页显示多少条记录;
    todosObj = Todo.query.filter_by(user_id=current_user.id).paginate(page=page, per_page=3)

    # paginate(
    # # 在config.py文件中有设置;
    # page, per_page=current_app.config['PER_PAGE'])
    return render_template('todo/list.html', todosObj=todosObj)


@todo.route('/')
@login_required
def index():
    return render_template('todo/index.html')
