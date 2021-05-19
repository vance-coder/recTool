import json
from flask_cors import CORS
from flask import Flask, request, render_template

from dbHelper import DBHelper

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        if not files:
            print('It is None')
        for f in files:
            f.save(f'static/images/upload/{f.filename}')
    return 'upload success'


@app.route("/nextPicture")
def next_picture():
    db = DBHelper()
    data = db.select(limit=1)[0]
    return json.dumps(data)


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == '__main__':
    # TODO upload file to backend call paddleOCR
    # TODO design table and process image then save result to table
    app.run(host="0.0.0.0", port=8080, debug=True)
