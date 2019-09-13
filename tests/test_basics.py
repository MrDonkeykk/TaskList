# encoding=utf-8
"""
Date:2019-09-13 09:53
User:LiYu
Email:liyu_5498@163.com

"""
import unittest
from flask import current_app
from app import create_app, db


class BasicsTestCase(unittest.TestCase):
    """
    setUp() 和 tearDown() 方法分别在各测试前后运行,
    并且名字以 test_ 开头的函数都作为测试执行。
    """

    def setUp(self):
        """

        在测试前创建一个测试环境。
           1). 使用测试配置创建程序
           2). 激活上下文, 确保能在测试中使用 current_app
           3). 创建一个全新的数据库,以备不时之需。
        :return:
        """
        self.app = create_app('testing')  # 使用测试配置创建程序
        self.app_context = self.app.app_context()  # 激活上下文, 确保能在测试中使用 current_app
        self.app_context.push()
        db.create_all()  # 创建一个全新的数据库

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # Pops the app context
        self.app_context.pop()

    def test_app_exists(self):
        """测试当前app是否存在?"""
        self.assertFalse(current_app is None)

    def test_app_is_testing(self):
        """测试当前app是否为测试环境?"""
        self.assertTrue(current_app.config['TESTING'])
