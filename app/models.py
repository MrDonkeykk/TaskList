# encoding=utf-8
"""
Date:2019-09-08 17:14
User:LiYu
Email:liyu_5498@163.com

"""
from datetime import datetime

from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer

from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from . import login_manager
"""
Flask-Login 提供了一个 UserMixin 类,包含常用方法的默认实现,且能满足大多数需求。
1). is_authenticated  用户是否已经登录?  
2). is_active         是否允许用户登录?False代表用户禁用
3). is_anonymous      是否匿名用户?
4). get_id()          返回用户的唯一标识符
"""


# 加载用户的回调函数;如果能找到用户,返回用户对象;否则返回 None 。
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    """用户"""
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))  # 加密的密码
    # 电子邮件地址email,相对于用户名而言,用户更不容易忘记自己的电子邮件地址。
    email = db.Column(db.String(64), unique=True, index=True)
    confirmed = db.Column(db.Boolean, default=False)
    # 新添加的用户资料
    name = db.Column(db.String(64))
    # 用户的真实姓名
    location = db.Column(db.String(64))  # 所在地
    about_me = db.Column(db.Text())  # 自我介绍
    # 注册日期
    # default 参数可以接受函数作为默认值,
    # 所以每次生成默认值时,db.Column() 都会调用指定的函数。
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 最后访问日期
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    # 1). Category添加一个属性todos, 2). Todo添加属性category;
    todos = db.relationship('Todo', backref='user')
    categories = db.relationship('Category', backref='user')

    def generate_confirmation_token(self, expiration=3600):
        """生成一个令牌,有效期默认为一小时。"""
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'],
                                            expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        """

        检验令牌和检查令牌中id和已登录用户id是否匹配?如果检验通过,则把新添加的 confirmed 属
        性设为 True

        """
        s = TimedJSONWebSignatureSerializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        # generate_password_hash(password, method= pbkdf2:sha1 , salt_length=8):密码加密的散列值。
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        # check_password_hash(hash, password) :密码散列值和用户输入的密码是否匹配.
        return check_password_hash(self.password_hash, password)

    def ping(self):
        """刷新用户的最后访问时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)

    def __repr__(self):
        return '<User % r>' % self.username


# 任务和分类的关系: 一对多
# 分类是一, 任务是多, 外键写在多的一端
class Todo(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    content = db.Column(db.String(100))  # 任务内容
    status = db.Column(db.Boolean, default=False)  # 任务的状态
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 任务的类型,关联另外一个表的id
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    # 任务所属用户;
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Todo %s>" % (self.content[:6])


class Category(db.Model):
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(20), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())  # 任务创建时间
    # 1). Category添加一个属性todos, 2). Todo添加属性category;
    todos = db.relationship('Todo', backref='category')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return "<Category %s>" % self.name
