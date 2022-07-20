#!/usr/bin/env python3

# Фрагмент кода 3:

def post(self):
    username = self.get_argument('username')
    password = self.get_argument('password').encode('utf-8')
    email = self.get_argument('mail')
    try:
        username = username.lower()
        email = email.strip().lower()
        user = User({'username': username, 'password': password, 'email': email, 'date_joined': curtime()})
        user.validate()
        save_user(self.db_conn, user)

    except Exception:

        return self.render_template("success_create.html")

