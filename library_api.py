from flask import Flask, jsonify, request

app = Flask(__name__)

books = [
    {'id': 1, 'title': 'The lord of rings', 'author': 'J.R.R'},
    {'id': 2, 'title': 'Harry potter and the Sorcerer\'s Stone', 'author': 'J.K'}
]

def find_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return book
    return None

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_specific_book(book_id):
    book = find_book(book_id)
    if book:
        return jsonify({'book': book})
    else:
        return jsonify({'error': 'Book Not Found'}), 404

@app.route('/books', methods=['POST'])
def add_books():
    new_books = request.get_json()
    if isinstance(new_books, list):  
        for book in new_books:
            if 'id' not in book or 'title' not in book or 'author' not in book:
                return jsonify({'error': 'Each book must have an id, title, and author'}), 400
            books.append(book)
        return jsonify({'message': 'Books added successfully'}), 201
    else:
        return jsonify({'error': 'Expected a list of books'}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = find_book(book_id)
    if book:
        book.update(request.get_json())
        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'error': 'Book not found'}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = find_book(book_id)
    if book:
        books.remove(book)
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'error': 'Book not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
