# main.py

from email_utils import fetch_unread_emails

emails = fetch_unread_emails()

for i, email in enumerate(emails):
    print(f"\n--- Email {i+1} ---")
    print("From:", email["from"])
    print("Subject:", email["subject"])
    print("Body:", email["body"][:200], "...")
