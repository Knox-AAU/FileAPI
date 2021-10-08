from flask import Flask, send_file
import psycopg2
import os
from configparser import ConfigParser


api = Flask(__name__)
config = ConfigParser()
config.read('config.ini')

@api.route("/file/<id>")
def file(id):
    filePath = GetPath(id)
    strippedPath = filePath.strip()
    skipablePartRemoved = strippedPath.replace(config.get('main', 'skipPath'), '')
    pathWithoutFirstSlash = skipablePartRemoved [1:]

    #Return file
    return send_file(config.get('main', 'rootDir') + pathWithoutFirstSlash)


def GetPath(id):
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="wordcount",
            user="postgres",
            password="1234")
        cur = conn.cursor()
        cur.execute("SELECT filepath FROM filelist WHERE id =" + id )
        row = cur.fetchone()[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
   
   
    return row

if __name__ == '__main__':
    api.run(host='0.0.0.0', port=config.get('main', 'port'))