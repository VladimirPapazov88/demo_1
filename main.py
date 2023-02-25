from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
from dateutil.relativedelta import relativedelta
import pymysql
import datetime
import hashlib
import os

host = ""
port = ""
try:
    host = os.environ["HOST"]
    port = os.environ["PORT"]
except:
    host = "localhost"
    port = "8006"

mysqlpass = ""
with open('secrets/mysql_pass.txt', 'r') as f:
    mysqlpass = f.read()

db = pymysql.connect(host=host, port=int(port), user='root',
                     password=mysqlpass, database='db')

cursor = db.cursor()

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'api_docs',
            "route": '/api_docs',
        }
    ],
    "specs_route": "/api/",
    "static_url_path": "/flasgger_static",
    "swagger_ui": True
}

app = Flask(__name__)
swagger = Swagger(app, swagger_config)


@app.route("/auth/v.1.0", methods=["POST"])
@swag_from("Auth.yaml", methods=["POST"])
def index():
    params = request.get_json()
    phone = params["phone"]
    passhash = hashlib.md5(params["password"].encode("utf-8")).hexdigest()

    allphonesSQL = "SELECT EXISTS(SELECT `phone` FROM `users` WHERE phone=%s)"
    cursor.execute(allphonesSQL, (phone,))
    exist = cursor.fetchone()

    print(exist)

    error = "Номер телефона некорректен"
    try:
        if (phone[0:3] == "+7(") and (phone[6] == ")") and (phone[7:10].isdigit()) and (phone[10] == "-") and (phone[11:13].isdigit()) and (phone[13] == "-") and (phone[14:16].isdigit()) and (len(phone) == 16):
            if (exist[0] == 1):
                error = "Такой аккаунт уже есть"
            else:
                error = ""
    except IndexError:
        pass

    if (error == ""):
        sql = "INSERT INTO `users` (`date_insert`, `date_update`, `phone`, `password_hash`) VALUES (%s, %s, %s, %s)"
        sql2 = "INSERT INTO `users_tokens` (`date_insert`, `date_update`, `user_id`, `token`, `expires`) VALUES (%s, %s, (SELECT `id` FROM `users` WHERE (`password_hash` = %s)), UUID(), %s)"
        cursor.execute(sql, (str(datetime.datetime.now()), str(
            datetime.datetime.now()), phone, passhash))
        cursor.execute(sql2, (str(datetime.datetime.now()), str(datetime.datetime.now(
        )), passhash, str(datetime.datetime.now()+relativedelta(months=2))))
        db.commit()
        sql3 = "SELECT `token` FROM `users_tokens` WHERE (`user_id` = (SELECT `id` FROM `users` WHERE (`password_hash` = %s)))"
        cursor.execute(sql3, (passhash,))
        token = cursor.fetchone()
        sql4 = "SELECT `expires` FROM `users_tokens` WHERE (`user_id` = (SELECT `id` FROM `users` WHERE (`password_hash` = %s)))"
        cursor.execute(sql4, (passhash,))
        expires = cursor.fetchone()
        return jsonify({"success": True, "error": "", "data": {"token": token[0], "expires": expires[0]}})
    return jsonify({"success": False, "error": error, "data": {}})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
