#!/usr/bin/env python 

import cgi
import sqlite3
import datetime

class HtmlResponse:


    def __init__(self):
        pass


    def build_response(self, insert_data):
        html_text = """Content-type: text/html


        <!DOCTYPE html>
<HTML>
    <head>
        <meta charset="utf-8">
        <title>Check Create Acount | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/check_create_account.css">
    </head>
    <body>
        <div id=checkCreateGroup>
            <div class="mainImage"><!--login_img/IN_0405.pngをCSSで指定--></div>

            <form action="done_create_account.py" method="POST">
                <div class="textOutput">
                    <!--ユーザーネームを表示(check_create_account.htmlで受け取った値はvalue)-->
                    <input type="text" class="UserName" name="UserName" value="%s" readonly>
                </div>

                <div class="textOutput">
                    <input type="email" class="email" name="EMail" value="%s" readonly> <!--メールアドレスを表示(check_create_account.htmlで受け取った値はvalue)-->

                <div class="textOutput">
                    <!--パスワードを表示(check_create_account.htmlで受け取った値はvalue)-->
                    <input type="password" class="password" name="PassWord" value="%s" readonly>
                </div>

                <div class="moveButton">
                    <button type="submit" class="back" onclick="location.href='create_account.html'">&lt; Back</button>
                    <button type="submit" class="create">Registration</button>
                </div>
            </form>
        </div>
    </body>
    <footer>

    </footer>
</HTML>"""
        return html_text % insert_data


    def build_response_error(self, insert_data):
        html_text = """Content type: text/html


        <!DOCTYPE html>
        <html>
            <head>
                <meta http-equiv="refresh" content="0; url=../html/%s.html">
            </head>
        </html>"""

        return html_text % insert_data


class DataBase:


    def __init__(self):
        # フルパスじゃないと上手くいかない...?
        # self.db_path = "/home/hal/Biolabcorp/Test/cgi-bin/db/test_db.sqlite"
        self.db_path = "./cgi-bin/db/test_db.sqlite"


    # DB に書き込み
    def write_db(self, userName, eMail, passWord):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # (テーブルがなければ)テーブルの作成
        cur.execute("CREATE TABLE IF NOT EXISTS sample_table\
                (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                user_name TEXT,\
                email TEXT,\
                pass TEXT,\
                registered_at TEXT)")

        registered_at = datetime.datetime.now()
        insert_data = ( userName, eMail, passWord, registered_at )
        # DB に書き込み
        cur.execute("INSERT INTO sample_table(user_name, email, pass, registered_at) VALUES(?, ?, ?, ?)", insert_data)

        conn.commit()
        conn.close()


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


    # 既に登録されていないか確認
    def check_account(self, user_name, email):
        if user_name == "" or email == "":
            return -1

        num_user = 0
        num_email = 0
        for row in self.read_db():
            if row[1] == user_name:
                num_user = 2

            if row[2] == email:
                num_email = 1

        return num_user + num_email


if __name__ == "__main__":
    form = cgi.FieldStorage()

    user_name = form.getvalue("UserName", "")
    email = form.getvalue("EMail", "")
    password = form.getvalue("PassWord", "")
   
    html_response = HtmlResponse()
    data_base = DataBase()

    error_code = data_base.check_account(user_name, email)
    # 0: エラーなし / 1: user_name 重複 / 2: email 重複 / 3: user_name+email 重複 / -1: 入力なし
    if error_code == -1:
        print(html_response.build_response_error("create_account"))

    if error_code == 0:
        print(html_response.build_response((user_name, email, password)))

    if error_code == 1:
        print(html_response.build_response_error("create_account_error_1"))

    if error_code == 2:
        print(html_response.build_response_error("create_account_error_2"))

    if error_code == 3:
        print(html_response.build_response_error("create_account_error_3"))


