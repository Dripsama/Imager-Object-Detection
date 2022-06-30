import os
from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.utils import secure_filename
from processing import new_method

ALLOWED_EXTENSIONS = set(['jpg', 'jpeg', 'gif', 'png'])

UPLOAD_FOLDER = 'F:/CODES/Python/Flask/image-upload-flask/uploads'

app = Flask(__name__)
CORS(app)

app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		print(file);
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
		output = new_method(path)
		# print(output)
		# resp = jsonify({'message' : 'File uploaded succesfully'})
		resp = jsonify(output)
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file types are jpg, jpeg, gif, png'})
		resp.status_code = 400
		return resp

if __name__ == "__main__":
    app.run(port = 4000)