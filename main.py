#! python3
# email_cleaner.py - Searches for and deletes emails based on specified criteria.

import os
import imaplib
import pyzmail
# need to install pyzmail39 using pip for python3.6 and up
from imapclient import IMAPClient
from dotenv import load_dotenv

load_dotenv()
imaplib._MAXLINE = 10000000

EMAIL_ADDRESS = os.environ.get('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
IMAP_SERVER = os.environ.get('IMAP_SERVER')

# Connect to email client
imap_object = IMAPClient(IMAP_SERVER, use_uid=True, ssl=True)
imap_object.login(EMAIL_ADDRESS, EMAIL_PASSWORD)

# TODO: Define or selec  criteria to search emails by.
before_date = ''
from_address = ''

imap_search_keys = {
    'all': 'ALL',
    'before': f'BEFORE {before_date}',
    'from': f'FROM {from_address}',
}

# Search emails
imap_object.select_folder('INBOX', readonly=True)
uids = imap_object.search(b'SINCE 01-Jul-2022')

raw_messages = imap_object.fetch(uids, ['BODY[]'])

for uid in uids:
    message = pyzmail.PyzMessage.factory(raw_messages[uid][b'BODY[]'])
    print(message.get_addresses('from'))

# TODO: List emails to be deleted by selected criteria

# TODO: confirm and delete

imap_object.logout()
