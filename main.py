from flask import Flask
from flask.json import jsonify
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

class File(Resource):
    def get(self):
        #Get path of file from ID
            #SQL 
        #Return file
        return '{"result":"result"}'

api.add_resource(File, '/file')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='8082')