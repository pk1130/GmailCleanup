import imaplib 
import datetime as dt
from imapclient import IMAPClient, imap_utf7
import email


def connect_to_gmail():
    """Function to connect to Gmail using IMAP client.

    Returns:
        IMAP4_SSL: Open IMAP connection
    """
    try: 
        conn = imaplib.IMAP4_SSL('imap.gmail.com', 993)
        print(f"[CONNECTION] {dt.datetime.today()} Connecting to Gmail using Imap")
        conn.login("login@gmail.com","pwd")
        print(f"[SUCCESS] Logged in at {dt.datetime.today()}")
        return conn
    except Exception as e:
        print(f"[EXCEPTION] Failed to connect to server : {e}")

def trash_emails_before_date_from_sender(obj, days, folder):
    """Function to remove emails from spam senders and unnecessary subscriptions

    Args:
        obj (IMAP object): IMAP object to interact with mail service
        date (int): Number of days before which 
        folder (String): word to describe Gmail folder label
    """
    # print (obj.select('"INBOX"'))
    status, msgs = obj.select(folder)
    msgs = int(msgs[0])
    print(f"- Found a total of {msgs} messages in {folder}.")
    typ, data = obj.search(None, 'ALL')
    sender = "insert sender here"
    before = (dt.date.today() - dt.timedelta(days)).strftime("%d-%b-%Y")
    status, data = obj.search(None, f"(UNSEEN FROM {sender} BEFORE {before})")
    total = len([int(s) for s in data[0].split() if s.isdigit()])
    emails = data[0].split()
    if len(emails) == 0:
        print("No emails found! Done!")
    else:
        print(f"[FOUND] {total} emails found from {sender} before {before}, deleting ...")
        obj.store("1:{0}".format(int(emails[-1])), '+X-GM-LABELS', '\\Trash') #move to trash
        print(f"[DELETED] Deleted {total} mails from {sender}.")
    print("Emptying Trash & Expunge...")
    obj.select('[Gmail]/Trash')  # select all trash
    obj.store("1:*", '+FLAGS', '\\Deleted')  #Flag all Trash as Deleted
    obj.expunge()  # not need if auto-expunge enabled

def disconnect(conn):
    """Function to disconnect from Gmail and close IMAP client.

    Args:
        conn (IMAP object): IMAP object to interact with mail service
    """
    print("[DISCONNECTING] Disconnecting from Gmail ...")
    try:
        conn.close()
        conn.logout()
        print(f"[DISCONNECTED] Disconnected at {dt.datetime}") 
    except Exception as e:
        print(f"[EXCEPTION] Failed to disconnect : {e}")

if __name__ == '__main__':
    gmail = connect_to_gmail()
    trash_emails_before_date_from_sender(gmail, 365, '"INBOX"') #example - 365 days/1 year
    disconnect(gmail)