from pymongo import MongoClient
import gridfs
import os, sys
import base64

ROOT = os.path.abspath(os.curdir)
PATH = ROOT + "/test.mp3"
PATH2 = ROOT + "/test2.mp3"

print(PATH)

conn = MongoClient("mongodb://localhost:27017/")

db = conn['AudioConverter']

collection = db['AudioFiles']

fs = gridfs.GridFS(db, 'AudioFiles')


for i in collection.find():
	print(i)


encode = ''
with open(PATH, 'rb') as f:
	encode = base64.b64encode(f.read())


fs.put(encode, filename='test', filetype="mp3")


for file in fs.find({'filetype': 'mp3'}, no_cursor_timeout=True):
	print(file.filename)
	data = file.read()

	with open(PATH2, 'wb') as fout:
		fout.write(base64.decodestring(data))
	
	fs.delete(file._id)


