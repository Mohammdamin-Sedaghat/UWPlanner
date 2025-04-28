from flask import Flask
from flask_cors import CORS
def create_app():
    app = Flask(__name__)
    CORS(app)

    from .auth import auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
