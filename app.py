from flask import Flask, render_template, request, redirect, session
from pymongo import MongoClient
from gridfs import GridFS 
import Helper
import os, base64

conn = MongoClient(f"mongodb+srv://{os.environ['USER']}:{os.environ['PASSWORD']}@cluster0.dzuvr.mongodb.net/{os.environ['DB']}?retryWrites=true&w=majority")
db = conn[os.environ['DB']]
fs = GridFS(db, os.environ['FS_COLLECTION'])

app = Flask(__name__)
app.secret_key = "super secret key"

ROOT = os.path.abspath(os.curdir)
UPLOAD_PATH = ROOT + "/uploads"

app.config['UPLOAD_FOLDER'] = UPLOAD_PATH

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


@app.route('/audiofiles', methods=['GET'])
def get_audio_files():
	results = []

	for file in fs.find():
		results.append(file.file)

	print(results)

	curr_context = session.get('context')
	curr_context['audio_files'] = results
	session['context'] = curr_context

	return redirect('/home')


@app.route('/convert', methods=['POST'])
def convert():
	files = request.files.getlist("files")
	
	for file in files:
		tmp_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
		file.save(tmp_path)

		encode = ''
		with open(tmp_path, 'rb') as f:
			encode = base64.b64encode(f.read())

		filename, filetype = Helper.separateFileName(file.filename)

		fs.put(encode, filename=filename, filetype=filetype, file=file.filename)

	return redirect('/home')


if __name__ == "__main__":
	app.debug = True 
	app.run()