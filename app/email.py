# encoding=utf-8
"""
Date:2019-09-15 15:36
User:LiYu
Email:liyu_5498@163.com

"""
from threading import Thread
from flask import render_template, current_app
from flask_mail import Mail, Message


def thread_task(app, mail, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, filename, **kwargs):
    """
    发送邮件的封装
    :param to: 收件人
    :param subject: 邮件主题
    :param filename: 邮件正文对应的html名称
    :param kwargs: 关键字参数， 模版中需要的变量名
    :return:
    """
    app = current_app._get_current_object()
    mail = Mail(app)
    msg = Message(
        subject=subject,
        sender='liyu_5498@163.com',
        recipients=to
    )
    msg.html = render_template(filename + '.html', **kwargs)
    thread = Thread(target=thread_task, args=(app, mail, msg))
    thread.start()
    return thread
