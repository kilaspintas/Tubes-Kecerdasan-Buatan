from flask import Flask, render_template, Response
import cv2
import numpy as np
import os

app = Flask(__name__)
camera = cv2.VideoCapture(0)

def sumberVideo():
    while True:
        success, img = camera.read()
        if img is not None:
            img = cv2.flip(img, 1)
            ret, buffer = cv2.imencode('.jpg', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result

        else:
            print('Kamera tidak terdeteksi')
            break

@app.route('/')
def index():
    return render_template('index.html')
@app.route('/video_feed')
def video_feed():
    return Response(sumberVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/teks')
def teks():
    return 'Watermark'

if __name__ == "__main__":
    app.run(debug=True)