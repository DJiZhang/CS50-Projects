from flask import Flask, render_template, request, jsonify, send_file
import json
from helper import convert,validate_file
import io
# Configure application
app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/filemode")
def file_mode():
    return render_template("file.html")

@app.post("/api/convert")
def api_convert():

    data = request.get_json()
    content = data.get("content","")
    delims = data.get("delimeters", {"inline": None, "display": None})

    result = convert(content, delims)
    return jsonify({"result": result})

@app.post("/api/file_upload")
def api_file_upload():
    f = request.files.get("file")
    try:
        name = validate_file(f.filename)
    except ValueError as e:
        print(e)
        return {"error": "error opening file"}, 400
    content = f.read().decode("utf-8")
    delims_raw = request.form.get("delimeters",'{"inline": None, "display": None}')
    delimeters = json.loads(delims_raw)
    converted = convert(content, delimeters)
    buffer = io.BytesIO(converted.encode("utf-8"))
    return send_file(buffer,
                     mimetype="text/plain",
                     as_attachment=True,
                     download_name= f"converted_{name}"
                     )


