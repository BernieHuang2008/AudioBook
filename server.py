from flask import Flask, send_from_directory, render_template, request, jsonify
import json
import os
from urllib.parse import quote
import requests

import xr_config

CONFIG = xr_config.read()

app = Flask(__name__)


@app.route("/")
def reader_index():
    return send_from_directory("h5app", "index.html")


@app.route("/<path>")
def reader_static(path):
    return send_from_directory("h5app", path)


@app.route("/api/wenyan_qword")
def wenyan_qword():
    word = request.args.get("word")[:4]
    if not word:
        return jsonify({"error": "Missing 'word' parameter"}), 400

    url = "http://www.dushan.net/guhanyu/show.asp?q="+quote(word, encoding="gbk")
    resp = requests.get(url)
    x = resp.text
    if "没有找到您要查找的汉字！" in x:
        return jsonify({"error": "Word not found"}), 404

    x=x[x.index('<div class="hr"></div>\r\n\t\t\t\t\t<p class="mt10">')+45:]
    x=x[:x.index('\r\n\t\t\t\t\t<div class="hr"></div>')]

    
    response_data = {
        "raw": x
    }

    return jsonify(response_data)


@app.route("/js/<path>")
def reader_js(path):
    return send_from_directory("h5app/js", path)


@app.route("/css/<path>")
def reader_css(path):
    return send_from_directory("h5app/css", path)


@app.route("/resources/booklist")
def booklist():
    return jsonify({"booklist": os.listdir(CONFIG["data/dir"])})


@app.route("/resources/books/<book>/audio/<path>")
def book_req_audio(book, path):
    return send_from_directory("{}/{}/audio".format(CONFIG["data/dir"], book), path)


@app.route("/resources/books/<book>/data/<path>")
def book_req_data(book, path):
    return send_from_directory("{}/{}/data".format(CONFIG["data/dir"], book), path)


@app.route("/<book>/edit", methods=["POST"])
def book_edit(book):
    data = request.json

    # START edit of datajson
    with open(
        "{}/{}/data/{}.json".format(CONFIG["data/dir"], book, data["meta"]["day"]), "r"
    ) as f:
        datajson = json.load(f)

    # edit: playTime
    if "playTime" in data:
        datajson["article_info"]["audio_info"]["audio_info_by_speed"]["normal"][
            "time_list"
        ] = data["playTime"]

    # END edit of datajson
    with open(
        "{}/{}/data/{}.json".format(CONFIG["data/dir"], book, data["meta"]["day"]), "w"
    ) as f:
        json.dump(datajson, f)

    return jsonify({"status": "ok"})


if __name__ == "__main__":
    app.run(
        host=CONFIG["server/host"],
        port=CONFIG["server/port"],
        debug=CONFIG["server/debug"],
    )
