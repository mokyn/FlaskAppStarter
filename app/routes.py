# Authors: CS-World Domination Summer19 - JG
try:
    from flask import render_template, redirect, url_for, request, send_from_directory, flash
except:
    print("Make sure to pip install Flask twilio")
from app import app
import os

from werkzeug.utils import secure_filename
from werkzeug.datastructures import  FileStorage

from app import plantsearch

try:
    from PIL import Image
    import PIL.ImageOps
except:
    print("Make sure to pip install Pillow")

import base64
import requests
your_api_key = "GbOWe16RYiNsCsotfeAhO0l5zBx8bTEOdK74LXF8IrdHTywmxC"

# Home page, renders the index.html template
@app.route('/index',methods=['GET','POST'])
@app.route('/',methods=['GET','POST'])
def index():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        # if the image is valid, do the following
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # Create a path to the image in the upload folder, save the upload
            # file to this path
            save_old=(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            remember = filename
            file.save(save_old)
            with open(save_old, "rb") as file:
                images = [base64.b64encode(file.read()).decode("ascii")]
            json_data = {
            "images": images,
            "modifiers": ["similar_images"],
            "plant_details": ["common_names", "url", "wiki_description", "taxonomy"]
}
            response = requests.post(
                "https://api.plant.id/v2/identify",
                json=json_data,
                headers={
                    "Content-Type": "application/json",
                    "Api-Key": your_api_key
                }).json()
            rt = render_template('apiResults.html', data=response["suggestions"], filename=remember)
            return rt
    return render_template('index.html', title='Home')

@app.route('/plantsearch',methods=['GET','POST'])
def search():
    if request.method == 'POST':
        old_text = request.form['text']
        plants=plantsearch.initdatabase()
        result = plantsearch.search(old_text,plants)
        #print(result)
        #print("\n".join([param+": "+result[param] for param in result]))
        new_text = ", ".join([str(param)+"is "+str(result[param]) for param in result])
        return render_template('textResults.html', old_text=old_text, new_text=new_text)
    return render_template('search.html', title='Home')


# Used for uploading pictures
@app.route('/<filename>')
def get_file(filename):
    return send_from_directory('static',filename)

# allowed image types 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])
app.config['ALLOWED_EXTENSIONS']=ALLOWED_EXTENSIONS

# is file allowed to be uploaded?
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']