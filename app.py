from flask import Flask
from controller.PersonController import PersonBp
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  
app.register_blueprint(PersonBp)


@app.route("/")
def index():
    return "Aplicacion funcionado!!!", 200


@app.route("/health")
def health():
    return "Verificacion aplicacion exitosa.", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)