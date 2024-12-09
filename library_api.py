from flask import Flask,jsonify,request

app=Flask(__name__)

books=[
    {'id':1,'title':'The lord of rings','author':'J.R.R'},
    {'id':2,'title':'Harry potter and the Socrer\'s Stone','author':'J.K'}
]

def find_book(book_id):
    for book in books:
        if book['id']==book_id:
            return book
    return None

@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})

@app.route('/books/<int:book_id>',methods=['GET'])
def get_spef_book(book_id):
    book=find_book(book_id)
    if book:
        return jsonify({'book':book})
    else:
        return jsonify ({'error':'Book Not Found'})
    
@app.route('/books', methods=['POST'])
def add_book():
    book = request.get_json()
    books.append(book)
    return jsonify({'message': 'Book added successfully'}), 201

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