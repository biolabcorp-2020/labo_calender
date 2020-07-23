#!/usr/bin/env python 

import cgi
import sqlite3

class HtmlResponse:


    def __init__(self):
        pass


    def build_response(self, insert_data):
        html_text = """Content-type: text/html


<!DOCTYPE html>
<HTML>
    <head>
        <meta charset="utf-8">
        <title>Check create group | BioLabCorp</title>
        <link rel="stylesheet" href="../html/css/check_create_group.css">
    </head>
    <body>
        <div id=checkCreateGroup>
            <div class="mainImage"><!--login_img/IN_0405.pngをCSSで指定--></div>

            <form action="done_create_group.py" method="POST">
                <div class="textOutput">
                    <!--グループ名を表示(check_create_group.htmlで受け取った値はvalue)-->
                    <input type="text" class="groupName" name="groupName" value="%s" readonly>
                </div>

                <div class="textOutput">
                    <!--キーナンバーを表示(check_create_group.htmlで受け取った値はvalue)-->
                    <input type="password" class="roomKeyNumber" name="keyNumber" value="%s" readonly>
                </div>

                <div class="moveButton">
                    <button type="submit" class="back" onclick="location.href='../html/create_group.html'">&lt; Back</button>
                    <button type="submit" class="create" onclick="location.href='done_create_group.py'">Create</button>
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


    # 既に登録されていないか確認
    def check_group(self, group_name):
        if group_name == "":
            return -1
        
        num_group = 0
        for row in self.read_db():
            if row[1] == group_name:
                num_group = 1

        return num_group


if __name__ == "__main__":
    form = cgi.FieldStorage()
    group_name = form.getvalue("groupName", "")
    key_number = form.getvalue("keyNumber", "")

    html_response = HtmlResponse()
    data_base = DataBase()

    error_code = data_base.check_group(group_name)
    # 0: エラーなし / 1: group_name 重複 / -1:入力なし
    if error_code == -1:
        print(html_response.build_response_error("create_group"))

    if error_code == 0:
        print(html_response.build_response((group_name, key_number)))

    if error_code == 1:
        print(html_response.build_response_error("create_group_error"))

