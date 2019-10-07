import smtplib  #导入smtplib包
from email.mime.text import MIMEText
# 构建邮箱格式
subject="致我们逝去的青春"  #发送的标题
content="""再见青春"""  #发送的内容
sender="hanshaosh@163.com"  #;发送者邮箱
recver="""  #接收者邮箱
2126579184@qq.com,
1262013975@qq.com,
576492000@qq.com
"""
password="han111111"  #传输中的密码
message=MIMEText(content,"plain","utf-8")
# content：内容；plain:内容类型；utf-8:编码格式
message["Subject"]=subject
message["From"]=sender
message["To"]=recver
# 发送邮件
smtp=smtplib.SMTP_SSL("smtp.163.com",465)
smtp.login(sender,password)
smtp.sendmail(sender,recver.split(",\n"),message.as_string())
# sender:发送人；recver:接收人，需要的是一个列表[];
# message.as_string:发送邮件 as_string是一种类似json的封装方式，目的是为了在协议上传输邮件内容
smtp.close()

