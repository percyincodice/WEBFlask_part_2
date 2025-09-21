from controller.UserController import UserBp
from flask import Flask
from controller.PersonController import PersonBp
from controller.AuthController import AuthBp
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  
app.register_blueprint(PersonBp)
app.register_blueprint(AuthBp)
app.register_blueprint(UserBp)


@app.route("/")
def index():
    return "Aplicacion funcionado!!!", 200


@app.route("/health")
def health():
    return "Verificacion aplicacion exitosa.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)