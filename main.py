#! python3
# email_cleaner.py - Searches for and deletes emails based on specified criteria.

import os
import imaplib
import pyzmail   # Install pyzmail39 using pip for python3.6 and up
import pyinputplus as pyip
from imapclient import IMAPClient
from dotenv import load_dotenv

load_dotenv()
imaplib._MAXLINE = 10000000

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
HOST = os.environ.get('IMAP_SERVER')

# Connect to email client
imap_object = IMAPClient(HOST, use_uid=True, ssl=True)
imap_object.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# TODO: Define or select criteria to search emails by.
before_date = ''
from_address = ''
search_key = ''
search_arg = ''

# Dict of available search keys.
imap_search_keys = {
    'All Messages': 'ALL',
    'Message Date': ['BEFORE', 'SINCE', 'ON'],
    'Message Content': ['SUBJECT', 'BODY', 'TEXT'],
    'Email Address': ['FROM', 'TO', 'CC', 'BCC'], 
    'Message Status': ['SEEN', 'UNSEEN', 'ANSWERED', 'UNANSWERED', 'DELETED', 'UNDELETED'],
}


def get_search_query():
    """Prompt user for search query to search email messages."""
    
    print('Choose key to search messages by: ')
    search_category = pyip.inputMenu(list(imap_search_keys.keys()), numbered=True)
    if search_category == 'All Messages':
        search_key = 'ALL'
        search_arg = None
    elif search_category == 'Message Date':
        print('Select Message Date option: ')
        search_key = pyip.inputMenu(imap_search_keys['Message Date'], numbered=True)
        search_arg = input('Enter date (required format - 01-Jan-1970): ')
    elif search_category == 'Message Content':
        print('Select option: ')
        search_key = pyip.inputMenu(imap_search_keys['Message Content'], numbered=True)
        search_arg = pyip.inputStr('Enter search term: ')
    elif search_category == 'Email Address':
        search_key = pyip.inputMenu(imap_search_keys['Email Address'], numbered=True)
        search_arg = pyip.inputEmail('Enter address to search by: ')
    elif search_category == 'Message Status':
        search_key = pyip.inputMenu(imap_search_keys['Message Status'], numbered=True)
        search_arg = None

    return search_key, search_arg


def search_email_messages(search_key, search_arg):
    """
    Search email messages using provided IMAP search key and argument.
    """
    msg_UIDs = imap_object.search(b'{search_key} {search_arg}')
    print(f'Messages found: {len(msg_UIDs)}')
    return msg_UIDs

uids = search_email_messages(search_key, search_arg)
raw_messages = imap_object.fetch(uids, ['BODY[]'])

def display_messages(uids):
    """
    Display email messages returned from search results.
    """
    for uid in uids:
        message = pyzmail.PyzMessage.factory(raw_messages[uid][b'BODY[]'])
        print(f'Subject: {message.get_subject()}, Sender: {message.get_address("from")}')

def delete_emails(uids):
    """
    Confirm and delete email messages.
    """
    confirm_delete = pyip.inputYesNo('Do you want to delete these messages? ')
    if confirm_delete == 'yes':
        imap_object.delete_messages(uids)
        print('Messages deleted successfully!')



# TODO: Include feature to permanently delete all emails in the bin folder.

imap_object.logout()
