import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    
install("Flask")
install("pybase64")
install("opencv-python")
from flask import Flask, jsonify;
import cv2
import numpy as np
import base64

vid = cv2.VideoCapture(0)

app = Flask(__name__)

@app.route('/', methods = ['GET'])
def get_articles():
    return jsonify({"hello": "Word"})

@app.route('/capture', methods = ['GET'])
def get_article():
    ret, frame = vid.read()
        
    (flag, img_encode) = cv2.imencode(".jpg", frame)
    data_encode = np.array(img_encode)
    byte_encode = data_encode.tobytes()
    print("the world")
    print(byte_encode)
    g = "send"
    #jpg_original = base64.b64decode(byte_encode)
    #jpg_as_np = np.frombuffer(jpg_original, dtype=np.uint8)
    #img = cv2.imdecode(jpg_as_np, flags=1)
    #cv2.imwrite('00.jpg', img)
    with open('readme.txt', 'w') as f:
        f.write(str(byte_encode))
    return jsonify({g : str(byte_encode)})

if __name__ == "__main__":
    app.run(debug=True)
