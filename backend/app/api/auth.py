from flask_restx import Namespace, Resource, fields

auth_ns = Namespace("auth", description="Authentication operations")

login_model = auth_ns.model("Login", {
    "email": fields.String(required=True),
    "password": fields.String(required=True),
})


@auth_ns.route("/login")
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        return {"access_token": "demo-token", "user": {"email": "recruiter@evirank-x.com", "role": "recruiter"}}


@auth_ns.route("/register")
class Register(Resource):
    def post(self):
        return {"message": "registered"}


@auth_ns.route("/refresh")
class Refresh(Resource):
    def post(self):
        return {"access_token": "demo-token"}


@auth_ns.route("/logout")
class Logout(Resource):
    def post(self):
        return {"message": "logged out"}
