from flask import Flask, send_file,abort
import psycopg2 #Postgres for Python
import os
from dotenv import load_dotenv
from configparser import ConfigParser


api = Flask(__name__)
config = ConfigParser()
config.read('config.ini')

@api.route("/file/<id>")
def file(id):
    filePath = GetPath(id)
    if(not os.path.isfile(modifyFilePath(filePath))):
        abort(404) 
        
    #Return file
    return send_file(modifyFilePath(filePath))

def modifyFilePath(filePath):
    if(filePath is None):
        return ""
    
    strippedPath = filePath.strip()
    skipablePartRemoved = strippedPath.replace(config.get('main', 'skipPath'), '')
    pathWithoutFirstSlash = skipablePartRemoved[1:]
    return config.get('main', 'rootDir') + pathWithoutFirstSlash

def GetPath(id):
    row = None
    load_dotenv()
    try:
        conn = psycopg2.connect(
            host     = os.getenv("DB_HOST"),
            database = os.getenv("DATABASE"),
            user     = os.getenv("DB_USER"),
            password = os.getenv("DB_PASSWORD"))
        cur = conn.cursor()
        cur.execute("SELECT filepath FROM filelist WHERE id =" + id )
        row = cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if 'conn' in locals() and conn is not None:
            conn.close()
            print('Database connection closed.')
   
    return row

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config.get('main', 'port'))