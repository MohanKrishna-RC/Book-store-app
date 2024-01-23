from flask import Flask, jsonify, request
from urllib.parse import quote as url_quote
from gevent.pywsgi import WSGIServer

app = Flask(__name__)

# Sample data (in-memory database)
books = [
    {"id": 1, "title": "Python Crash Course", "author": "Eric Matthes"},
    {"id": 2, "title": "Fluent Python", "author": "Luciano Ramalho"},
]

# Get all books
@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

# Get a specific book
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((item for item in books if item["id"] == book_id), None)
    if book:
        return jsonify({'book': book})
    else:
        return jsonify({'message': 'Book not found'}), 404

# Create a new book
@app.route('/books', methods=['POST'])
def create_book():
    new_book = {
        'id': len(books) + 1,
        'title': request.json['title'],
        'author': request.json['author']
    }
    books.append(new_book)
    return jsonify({'book': new_book}), 201

# Update a book
@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((item for item in books if item["id"] == book_id), None)
    if book:
        book['title'] = request.json['title']
        book['author'] = request.json['author']
        return jsonify({'book': book})
    else:
        return jsonify({'message': 'Book not found'}), 404

# Delete a book
@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [item for item in books if item['id'] != book_id]
    return jsonify({'message': 'Book deleted'})

if __name__ == '__main__':
    app.run(debug=True)
#     http_server = WSGIServer(('0.0.0.0', 5000), app)
#     http_server.serve_forever()