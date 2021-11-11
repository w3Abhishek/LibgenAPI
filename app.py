from flask import Flask, request, jsonify
import bookfinder

app = Flask(__name__)

@app.route('/search?q=<string:bookQuery>')
def query(bookQuery):
    book = bookfinder.search(bookQuery)
    return jsonify(book)

if __name__ == '__main__':
    app.run(debug=True)
