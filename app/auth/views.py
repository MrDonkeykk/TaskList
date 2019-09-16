# encoding=utf-8
"""
Date:2019-09-08 17:12
User:LiYu
Email:liyu_5498@163.com

"""
from flask import flash, redirect, render_template, url_for, request
from flask_login import login_user, logout_user, login_required, current_user

from app import db
from app.auth.forms import RegistrationForm, LoginForm
from app.email import send_mail
from app.models import User
from . import auth


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        # 提交数据库之后才能赋予新用户 id 值,而确认令牌需要用到 id ,所以不能延后提交。
        db.session.commit()
        token = user.generate_confirmation_token()
        try:
            # 发送邮件的函数Flask-Mail封装过, 可参考之前讲的内容;
            send_mail([user.email], '请激活你的任务管理平台帐号',
                      'auth/confirm', user=user, token=token)
        except Exception as e:
            flash('平台验证消息已经发送失败.' + str(e), category='error')
            return redirect(url_for('auth.register'))
        else:
            flash('平台验证消息已经发送到你的邮箱, 请确认后登录.', category='success')
            # # 用户登录
            login_user(user)
            return redirect(url_for('auth.index'))
    return render_template('auth/register.html', form=form)


# url_for('auth.confirm', token=token)  ==== 'http://127.0.0.1:5000/confirm/<token>'
@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('todo.index'))
    if current_user.confirm(token):
        flash('验证邮箱通过', category='success')
        return redirect(url_for('todo.index'))
    else:
        flash('验证连接失效', category='error')
        return redirect(url_for('todo.index'))


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            # 调用 Flask-Login 中的 login_user() 函数,在用户会话中把用户标记为已登录。
            # login_user() 函数的参数是要登录的用户,以及可选的“记住我”布尔值,“记住我”也在表单中填写。
            login_user(user)
            flash('登录成功', category='success')
            return redirect(url_for('auth.index'))
        else:
            flash('无效的用户名和密码.', category='error')
            return redirect(request.args.get('next') or url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('用户注销成功', category='success')
    return redirect(url_for('auth.login'))


# before_app_request 处理程序会在每次请求前运行
@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        # 更新已登录用户的访问时间
        current_user.ping()
        # print(type(request.endpoint))
        if not current_user.confirmed \
                and request.endpoint != 'static' \
                and request.endpoint[:5] != 'auth.':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    # 如果当前用户是匿名用户或者已经验证的用户, 则访问主页, 否则进入未验证界面;
    if current_user.is_anonymous or current_user.confirmed:
        return redirect(url_for('todo.index'))
    token = current_user.generate_confirmation_token()
    return render_template('auth/unconfirmed.html')


@auth.route('/reconfirm')
@login_required
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    try:
        send_mail([current_user.email], '请激活你的任务管理平台帐号',
                  'auth/confirm', user=current_user, token=token)
    except Exception as e:
        print(e)
        flash(str(e), category='error')
        return redirect(url_for('auth.register'))
    else:
        flash('新的平台验证消息已经发送到你的邮箱, 请确认后登录.', category='success')
        return redirect(url_for('todo.index'))


@auth.route('/')
def index():
    return render_template('auth/index.html')
