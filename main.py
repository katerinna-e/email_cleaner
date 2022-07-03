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

# TODO: Define or select criteria to search emails by.
before_date = ''
from_address = ''

# Dict of available search keys.
imap_search_keys = {
    'all': 'ALL',
    'before': f'BEFORE {before_date}',
    'from': f'FROM {from_address}',
}

def search_email_messages(search_key, search_arg):
    """Search email messages using provided IMAP search key and argument."""
    msg_UIDs = imap_object.search(b'{search_key} {search_arg}')
    print(f'Messages found: {len(uids)}')
    return msg_UIDs

imap_object.select_folder('INBOX', readonly=False)
uids = imap_object.search(b'FROM reply@rs.ca.nextdoor.com')

print(f'Messages found: {len(uids)}')

raw_messages = imap_object.fetch(uids, ['BODY[]'])

for uid in uids:
    message = pyzmail.PyzMessage.factory(raw_messages[uid][b'BODY[]'])
    print(message.get_subject())

# TODO: List emails to be deleted by selected criteria

# Confirm and delete email messages
confirm_delete = input('Do you want to delete these messages? (Y/N) ')

if confirm_delete == 'Y':
    imap_object.delete_messages(uids)
    print('Messages deleted successfully!')

# TODO: Include feature to permanently delete all emails in the bin folder.

imap_object.logout()