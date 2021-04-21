from flask import Flask, render_template, request, redirect, session, send_file
from pymongo import MongoClient
from decouple import config
import zipfile, io

import Helper as Helper
import S3Client as Client


USER = config('USER')
PASSWORD = config('PASSWORD')
DB = config('DB')

conn = MongoClient(f"mongodb+srv://{USER}:{PASSWORD}@cluster0.dzuvr.mongodb.net/{PASSWORD}?retryWrites=true&w=majority")
db = conn[DB]

app = Flask(__name__)
app.secret_key = "super secret key"

s3 = Client.S3Client()


@app.route('/')
def firstpage():
	if 'context' in session:
		session.pop('context')

	session['context'] = {}

	return render_template('index.html', context=session.get('context'))


@app.route('/home')
def home():
	context = session.get('context')
	if len(context) > 0:
		print(context)
	return render_template('index.html', context=context)


def upload(files):
	for file in files:
		filename = file.filename
		s3.upload(file, filename)


@app.route('/download', methods=['GET'])
def download():
    audio_files = s3.retrieveAudioFiles()
    
    memory_file = io.BytesIO() 
    
    with zipfile.ZipFile(memory_file, "w") as zf:
        for file in audio_files:
            filename = file[0]
            data = file[1]
            zf.writestr(filename, data)
            
    memory_file.seek(0)
    
    return send_file(memory_file, attachment_filename="converted_audio_files.zip", as_attachment=True)

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist("files") 
    target_filetype = request.form.get("audio_file_types")
    
    if files:
        for file in files:
            filename, filetype = Helper.separateFileName(file.filename)
            print(filename, end=" ")
            print(filetype)
            
        #upload(files)
        
    return redirect('/home')


if __name__ == "__main__":
	app.debug = True
	app.run()
