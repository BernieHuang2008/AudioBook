from flask import Flask, send_from_directory, render_template

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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
