import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import tensorflow as tf
import numpy as np
import cv2

UPLOAD_FOLDER = '/tmp'
MAX_CONTENT_PATH = 1024 * 1024 * 2
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_PATH'] = MAX_CONTENT_PATH

if not os.listdir("model"):
    m = tf.keras.applications.ResNet152V2(
        include_top=True, weights='imagenet', input_tensor=None, input_shape=None,
        pooling=None, classes=1000, classifier_activation='softmax'
    )
    m.save("model")
else:
    m = tf.keras.models.load_model("model")

def resize(f):
    im = cv2.resize(cv2.imread(f), (224, 224)) / 255
    return np.expand_dims(im, axis = 0)

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/resnet/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        f = request.files['file']
        if f.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if f and allowed_file(f.filename):
            fname = secure_filename(f.filename)
            fname = os.path.join(app.config['UPLOAD_FOLDER'], fname)
            f.save(fname)
            im = resize(fname)
            os.remove(fname)
            pred = m.predict(im)
            res = tf.keras.applications.resnet.decode_predictions(
              pred, top=5
            )
            res = '[' + ','.join([f'["{x[0]}","{x[1]}",{x[2]}]' for x in res[0]]) + ']' 
            return res, 200, {'Content-Type': 'application/json; charset=utf-8'}
    return '''
    <!doctype html>
    <html><body>
    <p>Upload an image...</p>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit>
    </form>
    </body></html>
    '''

if __name__ == '__main__':
   app.run(debug = True, host = "0.0.0.0")