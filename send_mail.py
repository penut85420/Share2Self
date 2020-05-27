import email
import os
import smtplib
import ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_gmail(sender, password, send_to, subject=None, body=None, file_names=None):
   subject = subject or 'None'
   body = body or 'None'

   message = MIMEMultipart()
   message['From'] = sender
   message['To'] = send_to
   message['Subject'] = subject
   message.attach(MIMEText(body, 'plain'))

   if file_names is not None:
      for fn in file_names:
         part = MIMEBase('application', 'octet-stream')
         part.set_payload(open(fn, 'rb').read())
         encoders.encode_base64(part)
         part.add_header(
            'Content-Disposition',
            f'attachment; filename= {os.path.basename(fn)}',
         )
         message.attach(part)

   text = message.as_string()
   context = ssl.create_default_context()

   with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
      server.login(sender, password)
      server.sendmail(sender, send_to, text)

   return True, 'Success'

if __name__ == "__main__":
   user = os.getenv('USER')
   password = os.getenv('PASS')
   to = os.getenv('TO')
   result, reason = send_gmail(user, password, to, filename=None, body='Hello', subject='YAAA')
