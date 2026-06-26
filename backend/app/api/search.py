from flask_restx import Namespace, Resource

search_ns = Namespace("search", description="Search and comparison endpoints")


@search_ns.route("")
class Search(Resource):
    def get(self):
        return [{"id": 1, "title": "Python backend engineer"}]
