import os
from flask import Flask, request, redirect, url_for, flash, render_template
from werkzeug.utils import secure_filename

##
import prototype

# bootstrap application
UPLOAD_FOLDER = './static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
app.secret_key = "super secret secret key 123"

# configure routes
@app.route('/tt', methods=['GET', 'POST'])
def index():
    # Handling post method
    if request.method == 'POST':
        if 'upload_img' not in request.files:
            flash('No file part')
            return redirect(request.url)
        img = request.files['upload_img']
        if img.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if allowed_file(img.filename) is False:
            flash('This type of file is not allowed.')
            return redirect(request.url)
        # storing the file
        if img:
            filename = secure_filename(img.filename)
            img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            detected_objects = prototype.object_detection_for_upload(filename)
            return render_template('img_posted.html', filename=filename, detected_objects=detected_objects)
    # Handling get method and every other method
    return render_template('index.html')

##
@app.route('/')
def start():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/impressum')
def impressum():
    return "Impressum"

# helper methods
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == '__main__':
    app.run(debug=True)
