from flask import Flask, request
from flask_cors import CORS

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

CORS(app)


# flask-restful
class HelloWorld(Resource):
    def get(self):
        return {"message": "bye user!"} #JSON Object
    
api.add_resource(HelloWorld, '/flaskrestful')


if __name__ == "__main__":
    app.run(debug=True)