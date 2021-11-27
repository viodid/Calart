from functools import wraps
from flask import redirect, session
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def hash(password):
    # discard repeated values
    password = set(password)
    # initialize variable to store all ord() chracters
    int_pool = 1
    # initialize list to append the final hash char
    hash_plain = []

    for i in password:
        int_pool *= ord(i)

    int_pool **= 100
    pool_str = str(int_pool)

    for i in range(4, 81):
        if i % 4 == 0:
            number = int(pool_str[:i])
            number_table = number % 127

            if number_table < 32:
                number_table += 32

            char_number = chr(number_table)
            hash_plain.append(char_number)

    return "".join(hash_plain)


def checkPasswordhash(hash_db, password):
    if hash(password) == hash_db:
        return True
    return False


def loginRequired(f):
    @wraps(f)
    def wrapper(*args, **kwds):
        if session.get("username") is None:
            return redirect("/login")
        return f(*args, **kwds)

    return wrapper


def sendmail(receiver, message_client, subject, sender, password):

    port = 465  # For SSL
    smtp_server = "smtp.gmail.com"
    context = ssl.create_default_context()

    message = MIMEMultipart("alternative")
    message["Subject"] = subject
    message["From"] = sender
    message["To"] = receiver

    text = message_client

    html = f"""\
        <html>
            <body style="padding:1.5rem; background: transparent; font-size:1.1rem; font">
                <div style="display:flex; justify-content:center; align-items:center; margin-bottom:2rem;">
                    <img src="https://i.ibb.co/xmtSkh6/calat-email.png" style="max-width:300px">
                </div>
                <p>{message_client}</p>
                <div>
                    <a href="https://www.facebook.com/CALAT-33-169199418110806" style='margin-right: 0.5rem;'>
                        Facebook
                    </a>
                    <a href="https://www.instagram.com/calat33/" style='margin-right: 0.5rem;'>
                        Instagram
                    </a>
                    <a href="https://twitter.com/hashtag/calat33">
                        Twitter
                    </a>
                </div>
            </body>
        </html>
        """

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")
    message.attach(part1)
    message.attach(part2)

    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message.as_string())
