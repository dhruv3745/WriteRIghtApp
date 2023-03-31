import subprocess
import sys
#from ARtest import findrect

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install("Flask")
install("pybase64")
install("opencv-python")
install("flask-cors")
#install("time")

from flask import Flask, jsonify, Response;
from flask_cors import CORS
from flask import g
from flask import request
import cv2
import numpy as np
import base64
import time
import os

os.path.expanduser("~")
print(os.getcwd())
vid = cv2.VideoCapture(0)


app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/', methods = ['GET'])
def get_articles():
    return jsonify({"hello": "Word"})
def get_n():
    for n in range(0,999999999999,1):
        yield n
#@app.route('/capture', methods = ['GET'])
def get_frame():
    #g.n = g.n + 1
    n = next(get_n())
    _ , frame = vid.read()
    filename = "/Users/paxysnowman/WriteAid/WriteAidReact/navigation/screens/" + str(n) + ".jpg"
    delete_filename = str(n-20) + ".jpg"
    cv2.imwrite(filename, frame)
    if (n > 22):
        os.remove(delete_filename)
    yield n
        
    #(flag, img_encode) = cv2.imencode(".jpg", frame)
    #data_encode = np.array(img_encode)
    #byte_encode = img_encode.tobytes()
    #yield(byte_encode)
    
    #yield (b'--frame\r\n'
               #b'Content-Type: image/jpeg\r\n\r\n' + byte_encode + b'\r\n')

@app.route('/video')
def video():
    #return {"TEST": str(time.localtime())}
    return {"TEST": str(next(get_frame()))}

@app.route('/process_frame', methods = ["POST"] )
def call_process_frame():
    data = request.get_json()
    img_path = data['img_path']
    coord_tuple = data['coord_tuple']
    stencil_path = data['stencil_path']
    #print(img_path, file=sys.stderr)
    #print(coord_tuple, file=sys.stderr)
    #print(stencil_path, file=sys.stderr)
    return {"efe": img_path + coord_tuple + stencil_path}
    
    #process.process_frame(img_path, coord_tuple, stencil_path)

if __name__ == "__main__":
    get_n()
    app.run(debug=True)
