
import json
import smtplib

from validate_email import validate_email
from DataBaseManager import DataBaseManager
from MenuManager import MenuManager
#import DNS

from flask import Flask, flash, redirect, render_template, request, session, abort, make_response
import os
from bcrypt import hashpw, gensalt
import requests
import unicodedata
from Crypto.Cipher import AES
import base64
from hashlib import md5

BLOCK_SIZE = 16

KEY = "some password".encode()

def pad(data):
    length = BLOCK_SIZE - (len(data) % BLOCK_SIZE)
    return data + (chr(length)*length).encode()

def unpad(data):
    return data[:-(data[-1] if type(data[-1]) == int else ord(data[-1]))]

def bytes_to_key(data, salt, output=48):
    # extended from https://gist.github.com/gsakkis/4546068
    assert len(salt) == 8, len(salt)
    data += salt
    key = md5(data).digest()
    final_key = key
    while len(final_key) < output:
        key = md5(key + data).digest()
        final_key += key
    return final_key[:output]

def decrypt(encrypted, passphrase):
    encrypted = base64.b64decode(encrypted)
    assert encrypted[0:8] == b"Salted__"
    salt = encrypted[8:16]
    key_iv = bytes_to_key(passphrase, salt, 32+16)
    key = key_iv[:32]
    iv = key_iv[32:]
    aes = AES.new(key, AES.MODE_CBC, iv)
    return unpad(aes.decrypt(encrypted[16:]))

class LoginManager():
    def __init__(self):
        self.database = DataBaseManager()
        self.app = Flask(__name__)
        self.app.secret_key = os.urandom(24)
        self.app.jinja_env.auto_reload = True
        self.app.config['TEMPLATES_AUTO_RELOAD'] = True
        self.app.add_url_rule('/', 'home', self.show_home_page)
        self.app.add_url_rule('/login', 'login', self.show_login_page)
        self.app.add_url_rule('/handle_login', 'handle_login', self.login, methods=['POST'])
        self.app.add_url_rule('/handle_signup', 'handle_signup', self.signup, methods=['POST'])
        self.app.add_url_rule('/handle_forgot_password', 'handle_forgot_password', self.forgot_password, methods=['POST'])
        self.app.add_url_rule('/logout','handle_logout', self.logout, methods=['POST'])

        self.app.add_url_rule('/contact_us','contact_us',self.contact_us,methods=['GET'])
        self.app.add_url_rule('/about','about',self.about,methods=['GET'])

        self.app.add_url_rule('/turn_on_or_off', 'turn_on_or_off', MenuManager.turn_on_or_off,methods=['POST'])
        self.app.add_url_rule('/change_password','change_password',self.change_password, methods=['POST'])
        self.app.add_url_rule("/input_speech_to_text_request","input_speech_to_text_request",MenuManager.input_speech_to_text_request,methods=['POST'])
        self.app.add_url_rule('/add_device', 'add_device', MenuManager.add_device ,methods=['POST'])
        self.app.add_url_rule("/remove_device", "remove_device", MenuManager.remove_device, methods=["POST"])

        self.app.run(debug=True, host='0.0.0.0', port=80)

    def about(self):
        return render_template("About.html")
    def contact_us(self):
        return render_template("Contact_us.html")
    def change_password(self):
        email = session["email"]
        new_password = request.form['new_password']
        self.database.change_password(hashpw(new_password.encode('utf-8'), gensalt()),email)
        return "<script>alert('password changed')</script>"

    def is_human(self,captcha_response):
        secret = "6LewXo8UAAAAAKBHNoISSx5WD2PRmnU1SbFNSbbt"
        payload = {'response':captcha_response, 'secret':secret}
        response = requests.post("https://www.google.com/recaptcha/api/siteverify", payload)
        response_text = json.loads(response.text)
        return response_text['success']

    def show_home_page(self):
        return render_template('index.html')

    def show_login_page(self):
        if('email' in session):
            return render_template('Menu.html',result = self.database.get_devices_by_type(session["email"],"light"))

        return render_template("LOG_SIGN_IN.html")

    def login(self):
        email = request.form['email']
        email = decrypt(email,KEY)
        password = request.form['password']
        password = decrypt(password,KEY)
        captcha_response = request.form['g-recaptcha-response']
        if(self.database.user_is_registered(email,password) and self.is_human(captcha_response)):
            #result = "<script>alert('202:success login')</script>"
            response = make_response(render_template('Menu.html',result = self.database.get_devices_by_type(email,"light")))
            response.set_cookie("username",self.database.get_username_by_email(email))
            session['email'] = email
            return response

        return render_template("LOG_SIGN_IN.html")

    def signup(self):
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        email = decrypt(email,KEY)
        username = decrypt(username,KEY)
        password = decrypt(password,KEY)
        #DNS.defaults['server']=['8.8.8.8', '8.8.4.4']#set your DNS server to Google's public DNS server
        captcha_response = request.form['g-recaptcha-response']
        if(self.database.add_user(username,password,email) and self.is_human(captcha_response)):
            #result = "<script>alert('202:success signup')</script>"
            response = make_response(render_template('Menu.html',result = self.database.get_devices_by_type(email,"light")))
            response.set_cookie('username',request.form['username'])
            session['email'] = email
            return response

        #result = "<script>alert('404:user is already exist or email is not exist')</script>"
        return render_template("LOG_SIGN_IN.html")

    def logout(self):
        if('email' in session):
            #result = "<script>alert('202:success logout')</script>"
            session.pop('email', None)
            return render_template('index.html')
        else:
            result = "<script>alert('404:user doesnt exist')</script>"
        return result

    def forgot_password(self):
        email = request.form["forgot_email"]
        email = decrypt(email,KEY)
        if(not self.database.is_user_exist(email)):
            return "<script>alert('404:user doesnt exist')</script>"

        gmail_user = 'smarthomeprojetmail@gmail.com'
        gmail_password = 'smartinon555'#need to earse this every time and do not to push the password to git

        sent_from = gmail_user
        to = [str(email, 'utf-8')]
        subject = 'Forgot password'
        body = "your new password is: " + self.database.get_user_password(email)

        email_text = """\
        From: %s
        To: %s
        Subject: %s

        %s
        """ % (sent_from, ", ".join(to), subject, body)

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        return ('<script>alert("202:the password sent to your email")</script>')
