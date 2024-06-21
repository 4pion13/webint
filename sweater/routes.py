import flask
from flask import Flask, render_template, request, redirect, session, url_for, jsonify, json
import json
import os
import urllib.request
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from ultralytics import YOLO
import uuid
from celery import Celery

model = YOLO('/Users/romannovikov/Documents/Проекты/intensive/best (4).pt')

app = Flask(__name__)
celery = Celery(app.name, broker='amqp://guest@localhost//')
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'zip'}
UPLOAD_FOLDER = '/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

@app.route('/', methods=['POST','GET'])
def take_photo():
    return render_template('take_file.html')


@app.route('/photo', methods=['POST','GET'])
def photo():
    status = False
    if request.method == "POST":
        x = 9999
        status = True
        status = True
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            print(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            print(filename)
            file_name = filename
            ui = uuid.uuid4()
            results = model.predict(model='/Users/romannovikov/Documents/Проекты/intensive/best (4).pt', 
                source= f'{UPLOAD_FOLDER}/{file_name}', 
                imgsz=640,  
                save=True,
                #conf=0.3,
                name = str(ui),
                project="/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/uploads/res",
                show_labels = True,
                show_conf = True,
                show_boxes = True,
                save_dir='/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/uploads/res')
            return redirect(url_for('show_file', photo_name = file_name, ui = ui))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
            
    return render_template('photo.html', methods=['POST','GET'], status = status)


@app.route('/show/<photo_name>/<ui>', methods=['POST','GET'])
def show_file(photo_name, ui):
    photo_name = f'uploads/res/{ui}/{photo_name}'
    return render_template('show_file.html', filename = photo_name)



@app.route('/video', methods=['POST','GET'])
def video():
    status = False
    if request.method == "POST":
        x = 9999
        status = True
        status = True
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file:
            status = True
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            file_name = filename
            ui = uuid.uuid4()
            return redirect(url_for('loading', photo_name = file_name, ui = ui))
        else:
            flash('Allowed image types are -> png, jpg, jpeg, gif')
            return redirect(request.url)
    return render_template('video.html', status = status)


@app.route('/show_video/<photo_name>/<ui>', methods=['POST','GET'])
def show_video(photo_name, ui):
    photo_name = f'uploads/res/{ui}/{photo_name}'
    return render_template('show_video.html', filename = photo_name)

@app.route('/<photo_name>/<ui>', methods=['POST','GET'])
def loading(photo_name, ui):

    return render_template('loading.html')



@app.route('/process', methods=['POST', 'GET'])
def load():
    if request.method == 'POST':
        print('Сработало')
        #photo_name = request.json['data']
        photo_name = request.form['data']
        dir_name = request.form['data_two']
        print(photo_name, request.form['data_two'])
        results = model.predict(model='/Users/romannovikov/Documents/Проекты/intensive/best (4).pt', 
                    source= f'{UPLOAD_FOLDER}/{photo_name}', 
                    imgsz=640,  
                    save=True,
                    #conf=0.5,
                    name = str(dir_name),
                    project="/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/uploads/res",
                        show_labels = True,
                        show_conf = True,
                        show_boxes = True,
                    save_dir='/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/uploads/res')
        #return redirect(url_for('show_video', photo_name = photo_name, ui = dir_name))
        photo_name = f'uploads/res/{dir_name}/{photo_name}'
        print(photo_name)
    return photo_name

    


@app.route("/res/model")
def res():
    folder = '/Users/romannovikov/Documents/Проекты/intensive/.venv/sweater/static/img/model_res'
    list = []
    for filename in os.listdir(folder):
        filename = f'img/model_res/{filename}'
        list.append(filename)
    return render_template('res.html', list = list)

if __name__ == "__main__":
    app.run(host="localhost",port="3232", debug=True)