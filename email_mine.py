import smtplib
import time
import imaplib
import email
import re
import string
import numpy as np

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
listOfCats = ["FLUID DAIRY", "DAIRY CULTURE", "DENTAL HYGIENE", "CEREALS", "COFFEE", "MISC JUICES", "MISC BERRIES",
              "DETERGENTS-LAUNDRY/DISH"] #create list of Categories


def get_acme():
    """
    Reads email for ACME Reciepts
    :return: returns text of acme email
    """
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


def cleanList(groceryList):
    """
    function to clean raw email
    :param groceryList: raw acme emial, output from getacme()
    :return: cleaned list, no lowercase letters and removes html tags
    """
    groceryList = groceryList.translate(None, string.ascii_lowercase)
    groceryList = groceryList.split("[: M")[0]
    groceryList = groceryList.split("//>")[1]
    return groceryList


def hasNumbers(inputString):
    """
    
    :param inputString: string to test
    :return: TRUE if string contains any numbers
    """
    return bool(re.search(r'\d', inputString))


def totalCategories(lst):
    """
    
    :param lst: clean grocery list
    :return: array of the total price of each category
    """
    splitList = re.split(
        r'\s(?=(?:FLUID DAIRY|DAIRY CULTURE|DENTAL HYGIENE|CEREALS|COFFEE|MISC JUICES|MISC BERRIES|DETERGENTS-LAUNDRY/DISH|\nS)\b)',
        lst) # split list into smaller list with these breakwords
    array = []
    # iterate through  list
    for x in splitList[:]:
        for y in listOfCats: ##go through each category in category list
            if y in x and hasNumbers(x): #if that category is in that section of the list
                total = 0
                new = re.split(r'\s(?=(?:Q/W)\b)', x) # split on Q/W in case more than one item in list
                print y # debug print
                for j in new[:]:
                    newJ = j.strip() #strip any spaces
                    non_decimal = re.compile(r'[^\d.$]+') # remove any text, keep only $ and numbers, next line too
                    money = non_decimal.sub('', newJ)
                    result = money.split('$') # split string on $, last amount is the price of that object
                    # print result, '#####'
                    if result[-1] != "": # if last item of list isnt blank
                        total += float(result[-1]) #add to total for the category
                print total
                array.append(total) # append total to the array
    return array


lst = get_acme()

final = cleanList(lst)

res = totalCategories(final)

