from flask_login import login_required, current_user
from flask import abort, render_template, flash, redirect, url_for

from app import db
from app.models import User
from app.user.forms import EditProfileForm
from . import user


# westos
# /user/westos

@user.route('/user/<username>')
@login_required
def users(username):  # westos
    user = User.query.filter_by(username=username).first()
    if user is None:
        # 抛出一个404的错误
        abort(404)

    return render_template('user/user.html', user=user)


@user.route('/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        current_user.about_me = form.about_me.data
        db.session.add(current_user)
        flash('用户配置信息更新成功!', category='success')
        return redirect(url_for('user.users', username=current_user.username))
    # 编辑的时候要显示用户的旧信息;
    # current_user.name 获取旧数据
    # form.name.data指定表单中填写的内容
    form.name.data = current_user.name
    form.location.data = current_user.location
    form.about_me.data = current_user.about_me
    return render_template('user/edit_profile.html', form=form)
