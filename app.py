from flask import Flask, render_template, request, redirect, session, send_file
from pymongo import MongoClient
from decouple import config
from pydub import AudioSegment
import zipfile, io

import Helper as Helper
import S3Client as Client
import soundfile as sf


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


def upload(files, folder="raw", formatFlag=False):
    for file in files:
        if formatFlag:
            data = file[0]
            filename = file[1]
            
            s3.upload(data, filename, folder)
        
        else:
            s3.upload(file, file.filename, folder)
            
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
        upload(files)
        converted_files = []
        original_files = s3.retrieveAudioFiles() 
        
        for file in original_files:
            original_filename, data = file 
            filename, filetype = Helper.separateFileName(original_filename)
            updated_filename = filename + ".wav"
            print(original_filename)
            #data = s3.getContents(original_filename)
            data = io.BytesIO(data)
            audio = AudioSegment.from_file(data, format='mp3')
            audio = audio.export("test.mp3", format="mp3")
            converted_files.append((audio, updated_filename))
            
        upload(converted_files, "converted", True)
        
    return redirect('/home')


if __name__ == "__main__":
	app.debug = True
	app.run()
