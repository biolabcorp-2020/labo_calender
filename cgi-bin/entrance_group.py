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
<html lang='ja'>
    <head>
        <meta charset="utf-8">
        <title>entrance group | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/entrance_group.css">
    </head>

    <body>
        <div id="JoinGroup">
            <div class = "mainImage">
                <!--CSSで画像img/login_img/IN_03.pngを挿入-->
            </div>

            <form action="entrance_group.py" method="POST">
                <div class="textInput">
                    <input class="groupName" type="text" placeholder="Group name" name="groupName">  <!--グループ名(groupName)を格納する-->
                </div>
                <div class="textInput">
                    <input class="roomKeyNumber" type="password" placeholder="Room key number" name="keyNumber"> <!--キーナンバー(roomKeyNumber)を格納する-->
                </div>

                <div class="moveButton">
                    <button type="submit" class="back" onclick="location.href='../html/select_menu.html'">&lt; Back</button>   <!--リンクを追加-->
                    <button type="submit" class="join">Join</button>
                </div>
            </form>
        </div>
    </body>

</html>"""
        return html_text


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
            for row in cur.execute("SELECT * FROM group_table"):
                ret.append(row)
        except:
            pass

        conn.close()
        return ret


def check_group(group_name, key_number):
    if group_name == "" or key_number == "":
        return False

    data_base = DataBase()
    for row in data_base.read_db():
        if row[1] == group_name and row[2] == key_number:
            return True

    return False


if __name__ == "__main__":
    form = cgi.FieldStorage()

    html_response = HtmlResponse()

    group_name = form.getvalue("groupName", "")
    key_number = form.getvalue("keyNumber", "")
    if check_group(group_name, key_number):
        html_text = """Content-type: text/html


        <!DOCTYPE html>
        <html>
            <head>
                <meta http-equiv="refresh" content="0; url=login.py">
            </head>
        </html>"""
        print(html_text)
    else:
        print(html_response.build_response())


