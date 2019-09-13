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
from app.auth import auth
from config import config
from app.todo import todo

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
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(todo, url_prefix='/todo')  # 注册蓝本
    # 附加路由和自定义的错误页面
    # .........后续还需完善, 补充视图和错误页面
    return app
