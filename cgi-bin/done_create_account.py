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
<HTML>
    <head>
        <meta charset="utf-8">
        <title>Done Create Account | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/done_create_account.css">
    </head>
    <body>
        <div id=checkCreateaccount>
            <div class="mainImage"><!--login_img/IN_06.pngをCSSで指定--></div>

            <div class="moveButton">
                <button type="submit" class="create" onclick="location.href='../html/select_menu.html'">Log in &gt;</button>
            </div>
        </div>
    </body>
    <footer>

    </footer>
</HTML>"""
        
        return html_text


class DataBase:


    def __init__(self):
        # フルパスじゃないと上手くいかない...?
        # self.db_path = "/home/hal/Biolabcorp/Test/cgi-bin/db/test_db.sqlite"
        self.db_path = "./cgi-bin/db/test_db.sqlite"


    # DB に書き込み
    def write_db(self, user_name, email, password):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # (テーブルがなければ)テーブルの作成
        cur.execute("CREATE TABLE IF NOT EXISTS account_table\
                (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                user_name TEXT,\
                email TEXT,\
                password TEXT,\
                registered_at TEXT)")

        registered_at = datetime.datetime.now()
        insert_data = ( user_name, email, password, registered_at )
        # DB に書き込み
        cur.execute("INSERT INTO account_table(user_name, email, password, registered_at) VALUES(?, ?, ?, ?)", insert_data)

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


if __name__ == "__main__":
    form = cgi.FieldStorage()

    html_response = HtmlResponse()
    data_base = DataBase()

    user_name = form.getvalue("UserName", "")
    email = form.getvalue("EMail", "")
    password = form.getvalue("PassWord", "")

    if user_name != "" and email != "" and password != "":
        data_base.write_db(user_name, email, password)

    print(html_response.build_response())

