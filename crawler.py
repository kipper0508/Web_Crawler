import requests
from bs4 import BeautifulSoup
import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import json

response = requests.get("https://www.csie.ncu.edu.tw/announcement/category/%E6%8B%9B%E7%94%9F%E5%BF%AB%E8%A8%8A")
soup = BeautifulSoup(response.text, "html.parser")
result = soup.find_all("div", class_='item-time')

date_list=[]
for div in result:
    date_list.append(div.string)

yesterday=(datetime.date.today()- datetime.timedelta(days=1)).strftime("%Y-%m-%d")

i = 0
target = -1
for every in date_list:
    if(every == yesterday):
        target = i
    i+=1

if(target != -1):
    
    with open('mail.json') as data_file:    
            config = json.load(data_file)
    
    result = soup.find_all("div", class_='item-title')
    title = result[target].string
    
    result = soup.find_all("a", class_='link')
    link = result[target].get('href')
    link = "https://www.csie.ncu.edu.tw"+link
    text = title + "\n" + link

    content = MIMEMultipart()  #建立MIMEMultipart物件
    content["subject"] = "中央資工-招生快訊更新"  #郵件標題
    content["from"] = config["sent_account"]  #寄件者
    content["to"] = config["receive_account"] #收件者
    content.attach(MIMEText(text))  #郵件內容

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:  # 設定SMTP伺服器
        try:
            smtp.ehlo()  # 驗證SMTP伺服器
            smtp.starttls()  # 建立加密傳輸
            smtp.login(config["sent_account"], config["sent_password"])  # 登入寄件者gmail
            smtp.send_message(content)  # 寄送郵件
        except Exception as e:
            print("Error message: ",e)
    

