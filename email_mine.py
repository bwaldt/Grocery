import smtplib
import time
import imaplib
import email
import re

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "trackmyfood123" + ORG_EMAIL
FROM_PWD = "peasants"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

mail = imaplib.IMAP4_SSL(SMTP_SERVER)
mail.login(FROM_EMAIL, FROM_PWD)
mail.select('inbox')

type, data = mail.search(None, 'ALL')
mail_ids = data[0]

id_list = mail_ids.split()
first_email_id = int(id_list[0])
latest_email_id = int(id_list[-1])

def get_acme():
    for i in range(latest_email_id, first_email_id, -1):
        typ, data = mail.fetch(i, '(RFC822)')

        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                if 'Receipt' in email_subject:
                    if msg.is_multipart():
                        for part in msg.walk():
                            body = part.get_payload()
                            rest = body[0]
                            return str(rest)


groceryList = get_acme()

import string
groceryList = groceryList.translate(None,string.ascii_lowercase)
#print groceryList


test ='this is text to keep T N: 2912017050720040050290 [: M ] R F Y <#_-3746339460747013820__3961495309290320556_> $5.00  $50.00'

groceryList = groceryList.split("[: M")[0]
groceryList = groceryList.split("//>")[1]
print groceryList