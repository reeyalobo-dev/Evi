from flask import Flask
from flask_cors import CORS
from flask_restx import Api
from flask_jwt_extended import JWTManager
from flask_socketio import SocketIO

from app.config import Config
from app.api import register_namespaces


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    JWTManager(app)
    SocketIO(app, cors_allowed_origins="*")

    api = Api(app, title="EviRank-X API", version="1.0", doc="/swagger")
    register_namespaces(api)

    @app.get("/health")
    def health():
        return {"status": "ok"}

    return app
