import smtplib
import sys
from urllib import request
from email import encoders
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from config import config_read

def email(proverit):
    spisok = open('./email.txt', 'r')
    # res = {}
    slov = []
    otvet = False
    for i in spisok.readlines():
        i = i.split('\n')
        if i[0] == proverit.lower():
            otvet = True
        slov += [f'{i[0]}']
    return otvet

def register(id):
    with open(".//registerID.txt", "a") as file:
        file.write(f'{id}\n')

def sverka_reg():
    spisok = open(".//registerID.txt", 'r')
    slov = {}
    for i in spisok.readlines():
        i = i.split('\n')
        i = i[0]
        i = i.split(': ')
        test = {int(i[0]): i[1]}
        slov.update(test)
    return slov

def post(from_addr, subject, body_text, path):  #Отправка почты
    #to_emails = "alexandr.kirichenko@kmf.kz"
    to_emails = config_read('to_emails')
    host = config_read('host')
    if path is not None:
        print(path.find('192.168.'))
        if path.find('192.168.') == 0:
            file_to_attach = path
            header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach
        else:
            request.urlretrieve(path, r"photo.jpg")
            file_to_attach = r"photo.jpg"
            header = 'Content-Disposition', 'attachment; filename="%s"' % file_to_attach
    # create the message
    msg = MIMEMultipart()
    msg["From"] = from_addr
    msg["Subject"] = subject
    msg["Date"] = formatdate(localtime=True)
    if body_text:
        msg.attach(MIMEText(body_text))
    msg["To"] = to_emails
    if path is not None:
        attachment = MIMEBase('application', "octet-stream")
        try:
            with open(file_to_attach, "rb") as fh:
                data = fh.read()
            attachment.set_payload(data)
            encoders.encode_base64(attachment)
            attachment.add_header(*header)
            msg.attach(attachment)
        except IOError:
            msg = "Error opening attachment file %s" % file_to_attach
            print(msg)
            sys.exit(1)
    emails = to_emails
    server = smtplib.SMTP(host)
    server.sendmail(from_addr, emails, msg.as_string())
    server.quit()


