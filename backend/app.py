from flask import Flask, render_template, request
from flask_cors import CORS

from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

CORS(app)

# normal flask route
@app.route('/')
def index():
    if request.method == "GET":
        return {"message": "bye user!"}  #JSON object

# flask-restful
class HelloWorld(Resource):
    def get(self):
        return {"message": "bye user!"}
    
api.add_resource(HelloWorld, '/flaskrestful')


if __name__ == "__main__":
    app.run(debug=True)