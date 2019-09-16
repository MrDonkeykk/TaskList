# encoding=utf-8
"""
Date:2019-09-08 17:10
User:LiYu
Email:liyu_5498@163.com
file:程序工厂函数, 延迟创建程序实例

"""
from flask import Flask
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_login import LoginManager
# Python2使用MySQLdb，Python3使用pymysql，有些模块没有更新
import pymysql
pymysql.install_as_MySQLdb()

login_manager = LoginManager()
# session_protection 属性提供不同的安全等级防止用户会话遭篡改。
login_manager.session_protection = 'strong'
# login_view 属性设置登录页面的端点。
login_manager.login_view = 'auth.login'

bootstrap = Bootstrap()
mail = Mail()
db = SQLAlchemy()


def create_app(config_name='development'):
    """
   默认创建开发环境的app对象
   """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    mail.init_app(app)
    db.init_app(app)

    # url_prefix: 指定访问该蓝图中定义的视图函数时需要添加的前缀, 没有指定则不加;
    from app.auth import auth  # auth的views里导入了db，放在上面的时候，db还没有创建，会报错
    app.register_blueprint(auth, url_prefix='/auth')
    from app.todo import todo
    app.register_blueprint(todo, url_prefix='/todo')  # 注册蓝本
    from app.user import user
    app.register_blueprint(user, url_prefix='/user')
    login_manager.init_app(app)  # 用户认证新加扩展
    return app
