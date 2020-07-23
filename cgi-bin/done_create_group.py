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
        <title>Done create group | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/done_create_group.css">
    </head>
    <body>
        <div id=doneCreateGroup>
            <div class="mainImage"><!--login_img/IN_06.pngをCSSで指定--></div>

            <div class="moveButton">
                <button type="submit" class="create" onclic="location.href=''">Look at a Group &gt;</button>
                <!--hrefはカレンダー画面に遷移-->
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
        self.table = "group_table"


    # DB に書き込み
    def write_db(self, group_name, key_number):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        # (テーブルがなければ)テーブルの作成
        create_table = "CREATE TABLE IF NOT EXISTS %s\
                (id INTEGER PRIMARY KEY AUTOINCREMENT,\
                group_name TEXT,\
                key_number TEXT,\
                registered_at TEXT)" % self.table
        cur.execute(create_table)

        registered_at = datetime.datetime.now()
        insert_data = ( group_name, key_number, registered_at )
        # DB に書き込み
        insert_table = "INSERT INTO %s(group_name, key_number, registered_at) VALUES(?, ?, ?)" % self.table
        cur.execute(insert_table, insert_data)

        conn.commit()
        conn.close()


    # DB の全データを読み込んで返す
    def read_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()

        ret = []
        try:
            select_from = "SELECT * FROM %s" % self.table
            for row in cur.execute(select_from):
                ret.append(row)
        except:
            pass

        conn.close()
        return ret


if __name__ == "__main__":
    form = cgi.FieldStorage()
    group_name = form.getvalue("groupName", "")
    key_number = form.getvalue("keyNumber", "")

    html_response = HtmlResponse()
    data_base = DataBase()
    if group_name != "" and key_number != "":
        data_base.write_db(group_name, key_number)

    print(html_response.build_response())

