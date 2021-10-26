from flask import Flask, send_file,abort
import os
from configparser import ConfigParser
import platform
import requests

api = Flask(__name__)
config = ConfigParser()
config.read('config.ini')

@api.route("/file/<id>")
def file(id):
    filePath = GetPath(id)
    modifiedFilePath = modifyFilePath(filePath)
    if(not os.path.isfile(modifiedFilePath)):
        abort(404, description="A file cannot be found for the given ID") 
        
    # Return file
    return send_file(modifyFilePath(filePath))

def getRootDir():
    if(platform.system() == 'Windows'):
        return 'C:/'
    return '/'

def modifyFilePath(filePath):

    if(filePath is None):
        return "" #If filePath is None, the program will crash during the string manipulation
    
    strippedPath = filePath.strip()
    skipablePartRemoved = strippedPath.replace(config.get('main', 'skipPath'), '')
    pathWithoutFirstSlash = skipablePartRemoved[1:]

    return getRootDir() + pathWithoutFirstSlash

def GetPath(fileId):
    response = requests.get(f'http://knox-master01.srv.aau.dk/wordCountAPI/FileList?id={fileId}')

    if (response.status_code not in range(200, 299)):
        abort(404, description="A file with a given id was not found") 

    return response.json().filePath

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config.get('main', 'port'))