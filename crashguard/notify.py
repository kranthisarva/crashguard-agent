import os, requests, smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def _pushover(title, body):
    token = os.getenv("PUSHOVER_TOKEN"); user = os.getenv("PUSHOVER_USER")
    if not token or not user: return False
    requests.post("https://api.pushover.net/1/messages.json", data={"token":token,"user":user,"title":title,"message":body})
    return True

def _email(title, body):
    host=os.getenv("SMTP_HOST"); user=os.getenv("SMTP_USER"); pwd=os.getenv("SMTP_PASS"); to=os.getenv("EMAIL_TO"); port=int(os.getenv("SMTP_PORT","587"))
    if not (host and user and pwd and to): return False
    msg = MIMEMultipart(); msg["Subject"]=title; msg["From"]=user; msg["To"]=to; msg.attach(MIMEText(body,"plain"))
    ctx = ssl.create_default_context()
    with smtplib.SMTP(host, port) as s:
        s.starttls(context=ctx); s.login(user, pwd); s.sendmail(user, [to], msg.as_string())
    return True

def notify(title, body):
    try:
        if not _pushover(title, body):
            _email(title, body)
    except Exception as e:
        # Log and continue so the workflow doesn't fail on notification issues
        print(f"[WARN] Notification failed: {e}")
        return False
    return True

