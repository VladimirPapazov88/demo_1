from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

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
    return jsonify({"phone": params["phone"], "password": params["password"]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
