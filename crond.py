# coding: utf-8
# !/usr/bin/env python

import os
import time
import smtplib
from email.mime.text import MIMEText
from email.Header import Header
import threading
import time

__INTERVAL__ = 610 # Each round of attack time interval(second).

'''
发送邮件函数
已经指定发送邮箱和接收邮箱
标题为故障时间
'''
def sendMail():
    mail_host = 'smtp.163.com'  # 设置服务器
    mail_port = '25'  # 服务器端口
    mail_sender = 'pythonqweasd@163.com'  # 发送用户名
    mail_pass = 'xxxx'  # 发送密码 (163是授权码，不是密码)
    mail_receivers = 'leochan2017@gmail.com'  # 接收邮箱
    Subject = '卧槽，Python进程又阻塞了'
    Content = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

    message = MIMEText(Content, 'plain', 'utf-8')
    message['Subject'] = Header(Subject, 'utf-8')
    message['From'] = mail_sender
    message['To'] = mail_receivers

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, mail_port)
        state = smtpObj.login(mail_sender, mail_pass)
        if state[0] == 235:
            smtpObj.sendmail(mail_sender, mail_receivers, message.as_string())
            print '邮件发送成功'
        smtpObj.quit()
    except smtplib.SMTPException, e:
        print str(e)


class intervalFunction(object):
    def __init__(self):
        print 'init interval Function\n'
        self.checkProcess()

    '''
    检查进程是否抽了
    发现距离现在时间超过10分钟，则判断为进程抽了
    '''
    def checkProcess(self):
        fileModifyTime = os.popen('stat -c %Y nohup.out').read().split('\n')[0]
        # fileModifyTime = '1537437334'

        fileModifyTime = int(fileModifyTime)

        nowTime = int(time.time())

        # 相差的秒数
        difference = nowTime - fileModifyTime

        # 如果10分钟没有反应，就证明他挂了呀
        if difference > 600:
            print '挂了呀'
            sendMail()
            command = ''
            os.system(command)


if __name__ == '__main__':
    p = intervalFunction()
    while True:
        timer = threading.Timer(__INTERVAL__, intervalFunction.checkProcess, (p,))
        timer.start()
        timer.join()
