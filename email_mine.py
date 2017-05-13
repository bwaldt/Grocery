import smtplib
import time
import imaplib
import email
import re
import string
import numpy as np
from datetime import datetime
import matplotlib
import scipy
import pandas as pd



ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "trackmyfood123" + ORG_EMAIL
FROM_PWD = raw_input("Please Enter Password")
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993


listOfCats = ["FLUID DAIRY", "DAIRY CULTURE", "DENTAL HYGIENE", "CEREALS", "COFFEE", "MISC JUICES", "FRUITS",
              "CLEANING SUPPLIES","BREAD","CHEESE","MEAT","VEGTABLES"] #create list of Categories


def get_acme():
    """
    Reads email for ACME Reciepts
    :return: returns text of acme email
    """

    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(FROM_EMAIL, FROM_PWD)
    mail.select('inbox')

    type, data = mail.search(None, 'ALL')
    mail_ids = data[0]

    id_list = mail_ids.split()
    first_email_id = int(id_list[0])
    latest_email_id = int(id_list[-1])

    rv = []
    dates = []
    for i in range(first_email_id, latest_email_id + 1):
        typ, data = mail.fetch(i, '(RFC822)')
        #print data
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1])
                email_subject = msg['subject']
                email_from = msg['from']
                email_date = msg['date']
                #print email_subject
                if 'Receipt' in email_subject:
                    email_date =email_date.split(',')[1]
                    email_date = email_date.strip()
                    email_date = email_date.split(' ')
                    email_date = email_date[0:3]
                    email_date = ' '.join(email_date)
                    dates.append(email_date)
                    if msg.is_multipart():
                        for part in msg.walk():
                            body = part.get_payload()
                            rest = body[0]
                            rest = str(rest)
                            #print rest , '$$$$$$$$$$$$$$'
                            rv.append(rest)
    return rv , dates


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

def changeCategoryGroups(groceryList):
    groceryList = groceryList.replace("TORTILLAS", "BREAD")
    groceryList = groceryList.replace("VEGETABLES CANNED", "VEGETABLES")
    groceryList = groceryList.replace("BANANAS", "FRUITS")
    groceryList = groceryList.replace("SHREDDED CHEESE", "CHEESE")
    groceryList = groceryList.replace("BEEF", "MEAT")
    groceryList = groceryList.replace("TURKEY BREAST", "MEAT")
    groceryList = groceryList.replace("MISC BERRIES", "FRUITS")
    groceryList = groceryList.replace("DETERGENTS-LAUNDRY/DISH","CLEANING SUPPLIES")
    groceryList = groceryList.replace("CHICK", "MEAT")
    return groceryList





def hasNumbers(inputString):
    """
    
    :param inputString: string to test
    :return: TRUE if string contains any numbers
    """
    return bool(re.search(r'\d', inputString))


def totalCategories(lst,date):
    """
    
    :param lst: clean grocery list
    :return: array of the total price of each category
    """
    listOfCats = ["FLUID DAIRY", "DAIRY CULTURE", "DENTAL HYGIENE", "CEREALS", "COFFEE", "MISC JUICES", "FRUITS",
                  "CLEANING SUPPLIES", "BREAD", "CHEESE", "MEAT", "VEGTABLES","WATER"]
    splitList = re.split(
        r'\s(?=(?:FLUID DAIRY|DAIRY CULTURE|DENTAL HYGIENE|CEREALS|COFFEE|MISC JUICES|FRUITS|CLEANING SUPPLIES|BREAD|CHEESE|MEAT|VEGETABLES|WATER|\nS)\b)',
        lst) # split list into smaller list with these breakwords
    array = []
    # iterate through  list
    for x in splitList[:]:
        #print x, '**************'
        for y in listOfCats: ##go through each category in category list

            if y in x and hasNumbers(x): #if that category is in that section of the list
                total = 0
                new = re.split(r'\s(?=(?:Q/W)\b)', x) # split on Q/W in case more than one item in list
                #print y # debug print
                for j in new[:]:
                    newJ = j.strip() #strip any spaces
                    non_decimal = re.compile(r'[^\d.$]+') # remove any text, keep only $ and numbers, next line too
                    money = non_decimal.sub('', newJ)
                    result = money.split('$') # split string on $, last amount is the price of that object
                    #print result, '#####'
                    if result[-1] != "": # if last item of list isnt blank
                        total += float(result[-1]) #add to total for the category
                rv_1 = y + "," + str(total) + "," + date
                #print rv_1 , "######"
                array.append(rv_1) # append total to the array
    return array


lst , buy_date = get_acme()

print buy_date
final = []
index = 0
for x in lst:
    if len(x) > 10:
        cleanedList = cleanList(x)
        changedGroups = changeCategoryGroups(cleanedList)
        res = totalCategories(changedGroups,buy_date[index])
        #print res
        index += 1




##Convert to date object, deal with later
datetime_object = datetime.strptime(buy_date[0], '%d %b %Y').date()
print datetime_object
