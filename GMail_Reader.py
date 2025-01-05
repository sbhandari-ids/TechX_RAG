# Importing libraries and dependencies
import imaplib
import email
from imap_tools import MailBox
import pandas as pd 
import json
from openpyxl.workbook import Workbook

from GMailLoginTestCredentials import get_credentials

credentials = get_credentials()

#URL for IMAP connection
imap_url = 'imap.gmail.com'

#creating an empty list (email_list) to store all the emails and 
# empty string (email_text) to store the body content of the email
email_list = []
email_text = ""

#setting up connection to imap server, authenticating user and logging in to the gmail account. 
mailbox = MailBox(imap_url).login(credentials['user'], credentials['password'])

for num, msg in enumerate(mailbox.fetch('(FROM "noreply@medium.com")'), start=1):
    if num > 200:
        break
    email = {
        "index": num,
        "uid": msg.uid,
        "subject": msg.subject,
        "date": msg.date.strftime("%Y-%m-%d %H:%M:%S"),
        "sender": msg.from_,
        "recipients": msg.to,
        "message": msg.text[:1500],
    }
    
    email_list.append(email)

    email_text += ''.join(msg.text)

#creating a new .txt file and writing the email body contents in a single file. 
with open('email_text.txt', 'w') as f:
    f.write(email_text)

#creating a json file to save the email data and metadata in json(dictionary) format.    
messages_dict = json.dumps(email_list, indent=4)
with open('messages_dict.txt', 'w') as f:
    f.write(messages_dict)

# creating the excel file to save data in excel format. Uses Pandas DataFrame and .to_csv() to write to the file.

df_messages = pd.DataFrame(email_list)
print(df_messages)
df_messages.to_csv('messages.csv', index=False)

# creating the excel file to save data in excel format. Uses Pandas DataFrame and .to_excel() to write to the file.
df_messages.to_excel('messages.xlsx', index=False) 



    