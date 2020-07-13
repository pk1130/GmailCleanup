# GmailCleanup

A simple Python script that requires a one-time run to delete emails from a 
particular sender before a particular date. It uses the Python IMAP client
(imaplib) to connect to the mailbox and get the emails.

### Tech-Stack:
- Python
- Python IMAP client

### To-do/Future Dev:
- Could implement spam classification algorithm using machine learning that studies a mailbox's senders and classifies certain senders as spam
- Use Python web drivers like Selenium to log into email and set auto-filters