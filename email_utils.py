# email_utils.py

import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

def fetch_unread_emails():
    load_dotenv()
    EMAIL = os.getenv("EMAIL_ADDRESS")
    PASSWORD = os.getenv("EMAIL_PASSWORD")

    # Connect to Gmail
    imap = imaplib.IMAP4_SSL("imap.gmail.com")
    imap.login(EMAIL, PASSWORD)

    # Select inbox
    imap.select("inbox")

    # Search for unread emails
    status, messages = imap.search(None, 'UNSEEN')

    emails = []
    for num in messages[0].split():
        status, data = imap.fetch(num, '(RFC822)')
        raw_msg = data[0][1]
        msg = email.message_from_bytes(raw_msg)

        # Decode subject
        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding if encoding else "utf-8")

        # Get sender
        from_ = msg.get("From")

        # Get body
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()

        emails.append({
            "subject": subject,
            "from": from_,
            "body": body.strip()
        })

    imap.logout()
    return emails
