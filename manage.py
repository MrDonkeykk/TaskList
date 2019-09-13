# encoding=utf-8
"""
Date:2019-09-08 17:13
User:LiYu
Email:liyu_5498@163.com

"""
from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Shell
from app import create_app, db

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, db)


# manager.command 修饰器让自定义命令变得简单。
# 修饰函数名就是命令名,函数的文档字符串会显示在帮助消息中。
@manager.command
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)


if __name__ == '__main__':
    manager.run()
