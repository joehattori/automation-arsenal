import argparse
import smtplib
import os
from dotenv import load_dotenv
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.utils import formatdate
from email import encoders 

dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

TA_ADDRESS  = os.environ.get("TA_ADDRESS")
MY_ADDRESS  = os.environ.get("GMAIL_ADDRESS") # 自分のメールアドレス
MY_PASSWORD = os.environ.get("GMAIL_PASSWORD") # 自分のパスワード
NAME        = os.environ.get("NAME") # 自分の氏名
FACULTY     = os.environ.get("FACULTY")
STUDENT_ID  = os.environ.get("STUDENT_ID") # 自分の学籍番号

def formatted_output(s):
    print("== {} ==".format(s))

def message(file, num):
    msg = MIMEMultipart()
    msg["Subject"] = " ".join([str(num), FACULTY, STUDENT_ID, NAME])
    msg["From"] = MY_ADDRESS
    msg["To"] = TA_ADDRESS
    msg["Date"] = formatdate()
    att = open(file)
    p = MIMEBase("application", "octet-stream")
    p.set_payload(att.read())
    encoders.encode_base64(p)
    p.add_header("Content-Disposition", "attachment; filename= %s" % file)
    msg.attach(p)
    return msg

def send_gmail(file, num):
    formatted_output("Attaching file")
    msg = message(file, num)
    formatted_output("Connecting to Gmail server")
    with smtplib.SMTP("smtp.gmail.com", 587) as s:
        s.starttls()
        s.ehlo()
        formatted_output("Logging in to Google account")
        s.login(MY_ADDRESS, MY_PASSWORD)
        formatted_output("Sending")
        s.sendmail(MY_ADDRESS, TA_ADDRESS, msg.as_string())
    formatted_output("Done")

def is_not_ready():
    return any(not c for c in [MY_ADDRESS, MY_PASSWORD, TA_ADDRESS, FACULTY, NAME, STUDENT_ID])

if __name__ == "__main__":
    if not os.path.isfile(".env"):
        print(".envファイルを作成し、.env.sampleを参考に自分のgmailアドレスとパスワード、宛先のアドレス、学科、氏名、学籍番号を全て入力してください。")
        exit()
    if is_not_ready():
        print(".env.sampleを参考に.envファイルに自分のgmailアドレスとパスワード、宛先のアドレス、学科、氏名、学籍番号を全て入力してください。")
        exit()
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", help="提出するファイルのパスです。")
    parser.add_argument("-k", "--kadai", help="課題番号です。")
    args = parser.parse_args()
    if args.file and args.kadai:
        send_gmail(args.file, args.kadai)
        exit()
    else:
        print("課題番号と提出ファイルのパスを入力してください。")
        exit()
