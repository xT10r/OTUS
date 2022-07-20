#!/usr/bin/env python3

# Фрагмент кода 1:

from flask import Flask
from mod_api import mod_api

app = Flask('vuln_app')
app.config['SECRET_KEY'] = 'F0cUzh8BgYJSLXAU8qDmClM0dE8GJTpsiyVEl3BCqQMCABp1U$f%'
app.register_blueprint(mod_api, url_prefix='/api')

