import json
from flask_cors import CORS
from flask import Flask, request, render_template, send_from_directory, make_response
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
            f.save(f'./static/images/upload/{f.filename}')
    return 'upload success'

@app.route("/nextPicture")
def next_picture():
    args = request.args
    db = DBHelper()
    fetch_status = 0
    if args:
        # save value
        value = args.get('value')
        filename = args.get('filename')
        status = args.get('status')
        fetch_status = args.get('fetch_status')
        db.update(filename, value, status)
    data = db.select_by_status(fetch_status)
    if data:
        data = data[0]
    else:
        data = {}
    db.close()
    return json.dumps(data)

@app.route("/delete")
def delete():
    args = request.args
    db = DBHelper()
    if args:
        # save value
        filename = args.get('filename')
        db.delete(filename)
        data = {
            'message': 'OK'
        }
    else:
        data = {
            'message': 'No data'
        }
    db.close()
    return json.dumps(data)

@app.route("/dashboard")
def dashboard():
    db = DBHelper()
    data = {
        'todo': 0,
        'checked': 0,
        'pending': 0
    }
    for row in db.select():
        if row['status'] == 0:
            data['todo'] += 1
        elif row['status'] == 1:
            data['checked'] += 1
        elif row['status'] == 2:
            data['pending'] += 1
    db.close()
    return json.dumps(data)

@app.route("/download")
def download():
    db = DBHelper()
    db.export()
    db.close()
    filename = 'label.zip'
    response = make_response(
        send_from_directory('static/', filename.encode('utf-8').decode('utf-8'), as_attachment=True))
    response.headers["Content-Disposition"] = "attachment; filename={}".format(filename.encode().decode('latin-1'))
    return response

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == '__main__':
    # TODO upload file to backend call paddleOCR
    # TODO design table and process image then save result to table
    #  show parent picture
    #  adjust picture size (mouse)
    #  p pending / 20 min
    # ---- next & previous / 30 min
    #  specific status (user can choice what status he want to show) / 1 hours
    #  status color / 20 min
    # TODO line number
    app.run(host="0.0.0.0", port=8080, debug=True)
