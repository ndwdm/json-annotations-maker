import sys
from os import walk
import os
import imghdr
import csv
import argparse

from flask import Flask, redirect, url_for, request
from flask import render_template
from flask import send_file


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route('/tagger')
def tagger():
    #with open(app.config["OUT"],'a') as f:
        #if os.path.getsize(app.config["OUT"]) == 0:
            #f.write('[')
    if (app.config["HEAD"] == len(app.config["FILES"])):
        with open(app.config["OUT"],'a') as f:
            f.seek(0, 2)
            size = f.tell()
            f.truncate(size - 1)
            f.write(']')
        return redirect(url_for('bye'))
    directory = app.config['IMAGES']
    image = app.config["FILES"][app.config["HEAD"]]
    labels = app.config["LABELS"]
    not_end = not(app.config["HEAD"] == len(app.config["FILES"]) - 1)
    print(not_end)
    return render_template('tagger.html', not_end=not_end, directory=directory, image=image, labels=labels, head=app.config["HEAD"] + 1, len=len(app.config["FILES"]))

@app.route('/next')
def next():
    image = app.config["FILES"][app.config["HEAD"]]
    app.config["HEAD"] = app.config["HEAD"] + 1
    with open(app.config["OUT"],'a') as f:
        if image != '' and image != '.DS_Store':
            f.write('{"image":"' + image + '",')
            f.write('"annotations":[')
            for label in app.config["LABELS"]:
                f.write('{"label":"' + label["name"] + '",')
                f.write('"coordinates":{"x":' + str(round((float(label["xMin"]) + float(label["xMax"]))/2)) + ',' +
                    '"y":' + str(round((float(label["yMin"]) + float(label["yMax"])) / 2)) + ',' +
                    '"width":' + str(round((float(label["xMax"]) - float(label["xMin"])))) + ',' +
                    '"height":' + str(round((float(label["yMax"]) - float(label["yMin"])))))
                f.write('}},')
            f.seek(0, 2)
            size = f.tell()
            f.truncate(size - 1)
            f.write(']},')
    app.config["LABELS"] = []
    return redirect(url_for('tagger'))

@app.route("/bye")
def bye():
    return send_file("taf.gif", mimetype='image/gif')

@app.route('/add/<id>')
def add(id):
    xMin = request.args.get("xMin")
    xMax = request.args.get("xMax")
    yMin = request.args.get("yMin")
    yMax = request.args.get("yMax")
    width = request.args.get("width")
    height = request.args.get("height")
    app.config["LABELS"].append({"id":id, "name":"", "xMin":xMin, "xMax":xMax, "yMin":yMin, "yMax":yMax, "width":width, "height":height})
    return redirect(url_for('tagger'))

@app.route('/remove/<id>')
def remove(id):
    index = int(id) - 1
    del app.config["LABELS"][index]
    for label in app.config["LABELS"][index:]:
        label["id"] = str(int(label["id"]) - 1)
    return redirect(url_for('tagger'))

@app.route('/label/<id>')
def label(id):
    name = request.args.get("name")
    app.config["LABELS"][int(id) - 1]["name"] = name
    return redirect(url_for('tagger'))

# @app.route('/prev')
# def prev():
#     app.config["HEAD"] = app.config["HEAD"] - 1
#     return redirect(url_for('tagger'))

@app.route('/image/<f>')
def images(f):
    images = app.config['IMAGES']
    return send_file(images + f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('dir', type=str, help='specify the images directory')
    parser.add_argument("--out")
    args = parser.parse_args()
    directory = args.dir
    if directory[len(directory) - 1] != "/":
         directory += "/"
    app.config["IMAGES"] = directory
    app.config["LABELS"] = []
    files = None
    for (dirpath, dirnames, filenames) in walk(app.config["IMAGES"]):
        files = filenames
        break
    if files == None:
        print("No files")
        exit()
    app.config["FILES"] = files
    app.config["HEAD"] = 0
    if args.out == None:
        app.config["OUT"] = "out.json"
    else:
        app.config["OUT"] = args.out
    print(files)
    with open(app.config["OUT"],'w') as f:
        if os.path.getsize(app.config["OUT"]) == 0:
            f.write('[')
    app.run(debug="True")
