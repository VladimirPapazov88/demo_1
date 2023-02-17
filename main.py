from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from
import pymysql, datetime
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

print(mysqlpass)

db = pymysql.connect(host=host, port=int(port), user='root', password=mysqlpass, database='db')

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
    sql = "INSERT INTO `users` (`date_insert`, `date_update`, `phone`, `password_hash`) VALUES (%s, %s, %s, %s)"
    cursor.execute(sql, (str(datetime.datetime.now()), str(datetime.datetime.now()), phone, passhash))
    db.commit()
    return jsonify({"phone": params["phone"], "password": params["password"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
