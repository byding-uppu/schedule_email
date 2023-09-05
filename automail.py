import smtplib
import schedule
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication

sender_email = None # replace w/ sender email
smtp_server = 'smtp.gmail.com'
smtp_port = 587
sender_password = None # replace w/ sender password
receiver_email = None # replace w/ receiver email

print("About to send email to " + receiver_email + "...")

subject = '转让会籍申请'
message = '黑骑士球员俱乐部：\
        我申请转让会籍，申请表及相关资料详见附件。\
        2023年9月3日'

target_time_stamp = 1693756789
current_timestamp = int(time.time())
delay_seconds = max(target_time_stamp - current_timestamp, 0)
print("delay seconds:", delay_seconds)

server = smtplib.SMTP ('smtp.gmail.com', 587)

def send_email():
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject
        msg.attach(MIMEText(message, 'plain'))
        
        # Attach files
        for i in [1, 2, 3, 4]:
            attachment_path = 'attachments/' + str(i) + ".pdf" 
            print("attachment_path:", attachment_path)
            with open(attachment_path, 'rb') as file:
                attachment = MIMEApplication(file.read(), _subtype='pdf')
                attachment.add_header('Content-Disposition', f'attachment; filename="{attachment_path}"')
                msg.attach(attachment)

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        print("Start TLS at", int(time.time()))
        server.login(sender_email, sender_password)
        print("Login success at", int(time.time()))
        server.sendmail(sender_email, receiver_email, msg.as_string())
        print("Send success at", int(time.time()))
        server.quit()

        print('Email sent successfully.')
    except Exception as e:
        print('An error occurred:', str(e))
        
print("Delay seconds:", delay_seconds)
# schedule.every(delay_seconds).seconds.do(send_email)
time.sleep(delay_seconds)

interval_seconds = 0.5  # 1 hour
schedule.every(interval_seconds).seconds.do(send_email)

i = 0
# Run the scheduling loop
while i < 10:
    schedule.run_pending()
    time.sleep(1)
    i = i+1
