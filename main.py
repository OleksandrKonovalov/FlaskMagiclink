import os
import random
import string
import smtplib
import sys
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, redirect
app = Flask(__name__)

emails = ["test@email.com"]
tokens = {}


class User:
    def __init__(self, email):
        self.email = email
        self.visits = 0


def send_link(email, token):
    port_number = 1234
    msg = MIMEMultipart()
    msg['From'] = 'magiclinksender@email.com'
    msg['To'] = email
    msg['Subject'] = 'Magic Link'
    message = 'Your magic link is: http://flask-magiclink.herokuapp.com/login?token=%s' % token
    msg.attach(MIMEText(message))
    mailserver = smtplib.SMTP('localhost', port_number)
    mailserver.login("magiclinksender@email.com", "password")
    mailserver.sendmail('magiclinksender@email.com', email, msg.as_string())
    mailserver.quit()


def generate_tokens():
    for email in emails:
        token = ''.join(random.choices(string.ascii_lowercase + string.digits, k=64))
        tokens[token] = User(email)
        # send_link(email, token)
        print(token)
        sys.stdout.flush()


@app.route('/')
def home():
    return "http://flask-magiclink.herokuapp.com/login?token=%s" % list(tokens.keys())[0]


@app.route('/login')
def login():
    token = request.args.get('token')
    if token and token in tokens:
        tokens[token].visits += 1
        return "Welcome, %s. This is your %d visit." % (tokens[token].email, tokens[token].visits)
    else:
        return redirect('/')


if __name__ == "__main__":
    generate_tokens()
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
