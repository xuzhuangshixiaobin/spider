#coding=utf8
# import smtplib
# from email.mime.text import MIMEText
# from email.header import Header
#
# # 服务器设置
# mail_host = 'smtp.mxhichina.com'
#
# # 发送邮箱帐号
# sender = 'monitor@aojinzhice.com'
#
# # 接收邮箱帐号
# receiver = '920386111@qq.com'
#
# # 发送邮箱帐号密码
# user = 'monitor@aojinzhice.com'
# password = 'MKjkx520'  # 需要到qq邮箱设置-账户开启pop3-生成暂时密码
#
# # 邮件主题和正文
# title = 'python test'
# text = '你好...............'
#
# msg = MIMEText(text, 'plain', 'utf-8')  # 中文需参数'utf-8',单字节字符不需要
# msg['Subject'] = Header(title, 'utf-8')  # Header()定义邮件标题,MIMEText()定义正文
#
# # 连接发送
# # smtp = smtplib.SMTP(mail_host)
# smtp= smtplib.SMTP_SSL(mail_host, 465)
#
# smtp.login(user, password)
# smtp.sendmail(sender, receiver, msg.as_string())
# smtp.quit()

# coding:utf-8
# -*- coding: UTF-8 -*-
import sys, os, re, urllib
import smtplib
import traceback
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
#发邮件
fromaddr = "support@aojinzhice.com"  # 发件人
smtpaddr = "smtp.mxhichina.com"  # 设置服务器  第三方 SMTP 服务
subject = ""  # 标题 （特殊符号影响发邮件）
password = ")2$d&l1@O0*)"  # 邮箱密码

toaddrs = "920386111@qq.com"#收件人

def sendmail(msg, toaddrs,subject):
        ''''' 
        @subject:邮件主题 
        @msg:邮件内容 
        @toaddrs:收信人的邮箱地址 
        @fromaddr:发信人的邮箱地址 
        @smtpaddr:smtp服务地址，可以在邮箱看，比如163邮箱为smtp.163.com 
        @password:发信人的邮箱密码 
        '''

        mail_msg = MIMEMultipart()



        mail_msg['Subject'] = subject
        mail_msg['From'] = fromaddr
        mail_msg['To'] = ','.join(toaddrs)
        mail_msg.attach(MIMEText(msg, 'html', 'utf-8'))

        s = smtplib.SMTP()
        s.connect(smtpaddr)  # 连接smtp服务器
        s.login(fromaddr, password)  # 登录邮箱

        s.sendmail(fromaddr, toaddrs, mail_msg.as_string())  # 发送邮件
        s.quit()

fromaddr = "support@aojinzhice.com"  # 发件人
smtpaddr = "smtp.mxhichina.com"  # 设置服务器  第三方 SMTP 服务
# subject = "利码联码包密码"  # 标题 （特殊符号影响发邮件）
password = ")2$d&l1@O0*)"  # 邮箱密码
#
# toaddrs = "920386111@qq.com"#收件人

# msg = "解压密码是：111111"
# sendmail(msg, toaddrs,"xuxuxu")