#!/usr/bin/env python 

import cgi
import sqlite3
import datetime

class HtmlResponse:


    def __init__(self):
        pass


    def build_response(self, insert_data):
        html_text = """Content-type: text/html


        """
        return html_text % insert_data


class DataBase:


    def __init__(self, table):
        # フルパスじゃないと上手くいかない...?
        self.db_path = ""
        self.table = table


    # DB に書き込み
    def write_db(userName, eMail, passWord):
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
    def read_db():
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        ret = []
        try:
            for row in cur.execute("SELECT * FROM sample_table"):
                ret.append(row)
        except:
            pass

        conn.close()
        return ret


if __name__ == "__main__":
    form = cgi.FieldStorage()

    html_response = HtmlResponse()
    data_base = DataBase()

"""
    userName = form.getvalue("user_name", "")
    eMail = form.getvalue("email", "")
    passWord = form.getvalue("pass", "")
    
    if userName == "" or eMail == "" or passWord == "":
        # 不正な入力時の処理
        response_html_invalid()
    else:
        write_db(userName, eMail, passWord)
        response_html_valid(userName, eMail, passWord, read_db())
"""
