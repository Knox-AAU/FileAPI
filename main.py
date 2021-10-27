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
    """ Used to get a file located on Node04.

    :param id: the id of the file needs to be found and returned.
    :return: returns the file corresponding to the input id.
    """
    filePath = GetPath(id)
    modifiedFilePath = modifyFilePath(filePath)
    if(not os.path.isfile(modifiedFilePath)):
        abort(404, description="A file cannot be found for the given ID") 
        
    # Return file
    return send_file(modifyFilePath(filePath))


def getRootDir():
    """ Gets the root directory of the system running the program.

    :return: Returns the root dir for the operation system in use.
    """
    if(platform.system() == 'Windows'):
        return 'C:/'
    return '/'


def modifyFilePath(filePath):
    """ Modifies the path of a file located on Node01 and modifies it to fit the corresponding location of the file on Node04

    :param filepath: the filepath from the database that needs to be modified to remove unnecessary parts and add root directory.
    :return: the modified filepath including the system specific root dir.
    """

    if(filePath is None):
        return "" #If filePath is None, the program will crash during the string manipulation
    
    strippedPath = filePath.strip()
    skipablePartRemoved = strippedPath.replace(config.get('main', 'skipPath'), '')
    pathWithoutFirstSlash = skipablePartRemoved[1:]

    return getRootDir() + pathWithoutFirstSlash

def GetPath(fileId):
    """ Get the path of a file located on the Node04 Databased by querying a file on Node01 and getting its filepath.

    :param int fileId: The id of a file located on the Node01 Database.
    :return: Returns the path of a file on the Node04 Database. 
    """
    response = requests.get(f'http://knox-master01.srv.aau.dk/wordCountAPI/wordCount/FileList/{fileId}')

    if (response.status_code not in range(200, 299)):
        abort(404, description=f"A file with a given id was not found status code {response.status_code}") 

    return response.json()["filePath"]

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config.get('main', 'port'))