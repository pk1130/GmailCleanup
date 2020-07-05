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
    senders = []
    for i in data[0].split():
        # fetch the email message by ID
        res, msg = obj.fetch(i, "(RFC822)")
        for response in msg:
            if isinstance(response, tuple):
                # parse a bytes email into a message object
                msg = email.message_from_string(response[1].decode("utf-8"))
                # add name of email sender to sender list
                senders.append(msg.get("From"))
    print(senders)
            
    before = (dt.date.today() - dt.timedelta(days)).strftime("%d-%b-%Y")
    status, data = obj.search(None, f"(UNSEEN FROM Facebook BEFORE {before})")
    print(len([int(s) for s in data[0].split() if s.isdigit()]))

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
    trash_emails_before_date_from_sender(gmail, 365, '"INBOX"')
    disconnect(gmail)