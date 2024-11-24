from flask import Flask, send_from_directory, render_template, request, jsonify
import json

import xr_config
CONFIG = xr_config.read()

app = Flask(__name__)

@app.route('/')
def reader_index():
    return render_template("index.html")


@app.route('/<path>')
def reader_ui(path):
    if '.' in path:
        return send_from_directory("ui", path)
    else:
        return render_template("new.html", bookname=path.strip())


@app.route('/<book>/audio/<path>')
def book_req_audio(book, path):
    return send_from_directory("{}/{}/audio".format(CONFIG['data/dir'], book), path)


@app.route('/<book>/data/<path>')
def book_req_data(book, path):
    return send_from_directory("{}/{}/data".format(CONFIG['data/dir'], book), path)

@app.route('/<book>/edit', methods=['POST'])
def book_edit(book):
    data = request.json
    
    # START edit of datajson
    with open("{}/{}/data/{}.json".format(CONFIG['data/dir'], book, data['meta']['day']), "r") as f:
        datajson = json.load(f)
    
    # edit: playTime
    if 'playTime' in data:
        datajson['article_info']['audio_info']['audio_info_by_speed']['normal']['time_list'] = data['playTime']

    
    # END edit of datajson
    with open("{}/{}/data/{}.json".format(CONFIG['data/dir'], book, data['meta']['day']), "w") as f:
        json.dump(datajson, f)
    
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host=CONFIG['server/host'], port=CONFIG['server/port'], debug=CONFIG['server/debug'])
