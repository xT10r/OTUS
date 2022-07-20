#!/usr/bin/env python3

# Фрагмент кода 2:

from flask_wtf import Form
# from wtforms import TextField
from wtforms import StringField

class LoginForm(Form):

    username = StringField('username')
    password = StringField('password')

form = Form()
asd = LoginForm(form)