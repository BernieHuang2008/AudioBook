from flask import Flask, send_from_directory, render_template, request, jsonify
import json

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
    return send_from_directory("books/{}/audio".format(book), path)


@app.route('/<book>/data/<path>')
def book_req_data(book, path):
    return send_from_directory("books/{}/data".format(book), path)

@app.route('/<book>/edit', methods=['POST'])
def book_edit(book):
    data = request.json
    
    # START edit of datajson
    with open("books/{}/data/{}.json".format(book, data['meta']['day']), "r") as f:
        datajson = json.load(f)
    
    # edit: playTime
    if 'playTime' in data:
        datajson['article_info']['audio_info']['audio_info_by_speed']['normal']['time_list'] = data['playTime']

    
    # END edit of datajson
    with open("books/{}/data/{}.json".format(book, data['meta']['day']), "w") as f:
        json.dump(datajson, f)
    
    return jsonify({"status": "ok"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
