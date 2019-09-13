# encoding=utf-8
"""
Date:2019-09-08 17:12
User:LiYu
Email:liyu_5498@163.com

"""
from . import todo


@todo.route('/add/')
def add():
    return 'todo add'


@todo.route('/delete/')
def delete():
    return 'todo delete'
