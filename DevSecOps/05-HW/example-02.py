#!/usr/bin/env python3

# Фрагмент кода 2:

from flask_wtf import Form
from wtforms import TextField

class LoginForm(Form):

    username = TextField('username')
    password = TextField('password')