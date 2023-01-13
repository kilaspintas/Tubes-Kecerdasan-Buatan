from flask import *
from keras.models import load_model
from time import sleep
from keras.utils import img_to_array
import cv2
import numpy as np
from PIL import Image
app = Flask(__name__)

hasil = {
    'ekspresi' : 'ada',
    'rating' : 'ada'
    }
face_classifier = cv2.CascadeClassifier(r'haarcascade_frontalface_default.xml')
classifier =load_model(r'100.h5')
emotion_labels = ['jijik','marah','netral','sedih','senang', 'takut', 'terkejut']

camera = cv2.VideoCapture(0)

def sumberVideo():
   while True:
    _, frame = camera.read()
    gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray)

    for (x,y,w,h) in faces:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
        roi_gray = gray[y:y+h,x:x+w]
        roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)

        if np.sum([roi_gray])!=0:
            roi = roi_gray.astype('float')/255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi,axis=0)

            prediction = classifier.predict(roi)[0]
            label=emotion_labels[prediction.argmax()]
            label_position = (x,y)
            cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        else:
            cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
    cv2.imshow('Emotion Detector',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()

def deteksiGambar():
    frame = cv2.imread('aset.jpg')

    while True:
        gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        faces = face_classifier.detectMultiScale(gray)

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
            roi_gray = gray[y:y+h,x:x+w]
            roi_gray = cv2.resize(roi_gray,(48,48),interpolation=cv2.INTER_AREA)
            if np.sum([roi_gray])!=0:
                roi = roi_gray.astype('float')/255.0
                roi = img_to_array(roi)
                roi = np.expand_dims(roi,axis=0)

                prediction = classifier.predict(roi)[0]
                label=emotion_labels[prediction.argmax()]
                if(label == 'sedih'):
                    hasil['rating'] = 'buruk'
                elif(label == 'senang'):
                    hasil['rating'] = 'bagus'

                hasil['ekspresi'] = label
                label_position = (x,y)
                cv2.putText(frame,label,label_position,cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
            else:
                cv2.putText(frame,'No Faces',(30,80),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,0),2)
        cv2.imwrite("hasil.jpg",frame)
        break


@app.route('/', methods=['GET', 'POST'])
def index():
    if(request.method == "POST"):
        data = request.files.get('file')
        data = np.array(Image.open(data))
        data = cv2.cvtColor(data,cv2.COLOR_BGR2GRAY)
        cv2.imwrite('aset.jpg',data)
        deteksiGambar()
    return render_template('program.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    return jsonify(hasil)

@app.route('/kamera', methods=['GET', 'POST'])
def kamera():
    return Response(sumberVideo(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/oncam', methods=['GET', 'POST'])
def onCam():
    return render_template('kamera.html')
if __name__ == "__main__":
    app.run(debug=True)
