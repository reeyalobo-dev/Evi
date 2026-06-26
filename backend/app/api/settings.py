from flask_restx import Namespace, Resource

settings_ns = Namespace("settings", description="Application settings and model configuration")


@settings_ns.route("")
class Settings(Resource):
    def get(self):
        return {"theme": "dark", "model": "lambda-mart", "calibration": "platt"}
