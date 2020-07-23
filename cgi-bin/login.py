#!/usr/bin/env python 

import cgi
import sqlite3
import datetime

class HtmlResponse:


    def __init__(self):
        pass


    def build_response(self):
        html_text = """Content-type: text/html


        <!DOCTYPE html>
        <html>
            <head>
                <meta http-equiv="refresh" content="0; url=../html/select_menu.html">
            </head>
        </html>"""
        return html_text


    def build_response_error(self, insert_data):
        html_text = """Content-type: text/html


        <!DOCTYPE html>
<html lang='ja'>
    <head>
        <meta charset="utf-8">
        <title>Login | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/login.css">
        <link rel="stylesheet" href="../html/css/%s.css">
    </head>

    <body>
        <div id="Log_in">
            <div class = "mainImage">
                <!--CSSで画像を挿入-->
            </div>

            <form action="login.py" method="POST">
                    <div class="textInput">
                            <input class="UserName" type="text" placeholder="User Name" name="UserName">  <!--グループ名(UserName)を格納する-->
                    </div>
                    <div class="textInput">
                            <input class="password" type="password" placeholder="passward" name="password"> <!--キーナンバー(passward)を格納する-->
                    </div>

                    %s

                    <div class="LogInButton">
                            <button type="submit" class="LogIn">Log in</button>   <!--リンクを追加-->
                    </div>

                    <div class = "registration">
                            Not registered?
                            <a href="../html/create_account.html">Registration your account</a>
                    </div>
                    <div class = "forget_pass">
                            <a href="xx.html">Forget password?</a>
                    </div>
            </form>
        </div>
    </body>
</html>"""
        return html_text % insert_data


class DataBase:


    def __init__(self):
        # フルパスじゃないと上手くいかない...?
        # self.db_path = "/home/hal/Biolabcorp/Test/cgi-bin/db/test_db.sqlite"
        self.db_path = "./cgi-bin/db/test_db.sqlite"


    # DB の全データを読み込んで返す
    def read_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        ret = []
        try:
            for row in cur.execute("SELECT * FROM account_table"):
                ret.append(row)
        except:
            pass

        conn.close()
        return ret


def check_account(user_name, password):
    if user_name == "" or password == "":
        return -1

    data_base = DataBase()
    for row in data_base.read_db():
        if row[1] == user_name and row[3] == password:
            return 0

    return 1


if __name__ == "__main__":
    form = cgi.FieldStorage()

    html_response = HtmlResponse()

    user_name = form.getvalue("UserName", "")
    password = form.getvalue("password", "")

    error_code = check_account(user_name, password)
    # 0: エラーなし / 1: 入力ミス / -1: 入力なし
    if error_code == -1:
        insert_data = ("login", "")
        print(html_response.build_response_error(insert_data))

    if error_code == 0:
        print(html_response.build_response())

    if error_code == 1:
        insert_data = ("login_error", "<div class=\"errorMessage\">UserName または password が間違っています。</div>")
        print(html_response.build_response_error(insert_data))

