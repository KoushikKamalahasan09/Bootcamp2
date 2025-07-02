from flask import Flask, request
from flask_cors import CORS

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

CORS(app)


# flask-restful
class HelloWorld(Resource):
    def get(self):
        return {"messagehi": "Hi user!"} #JSON Object
    
class ByeWorld(Resource):
    def get(self):
        return {"messagebye":"Bye user!"} #JSON Object
    
class data(Resource):
    def get(self):
        return {
            "name": "test",
            "project": "Flask + JS API Test",
            "status": "In Progress",
            "version": 1.0
        }
    

    
api.add_resource(HelloWorld, '/flaskrestful/Hi')
api.add_resource(ByeWorld, '/flaskrestful/Bye')
api.add_resource(data, '/data')

if __name__ == "__main__":
    app.run(debug=True)