from flask import Flask, jsonify
import bookfinder
app = Flask(__name__)

@app.route("/search/<string:bookName>")
def find(bookName):
    return jsonify(bookfinder.search(bookName))

@app.route("/getBook/<string:md5>")
def downBook(md5):
    return jsonify(bookfinder.getBook(md5))

if __name__ == '__main__':
    app.run(debug=True)