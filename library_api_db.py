from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:12345678@localhost/Library'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  
db = SQLAlchemy(app)

class Book(db.Model):
    __tablename__ = 'books'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=False)

    def __init__(self, title, author):
        self.title = title
        self.author = author

    def to_dict(self):
        return {"id": self.id, "title": self.title, "author": self.author}

@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()  
    return jsonify({'books': [book.to_dict() for book in books]})

# Route to get a specific book by id
@app.route('/books/<int:book_id>', methods=['GET'])
def get_specific_book(book_id):
    book = Book.query.get(book_id)  
    if book:
        return jsonify({'book': book.to_dict()})
    else:
        return jsonify({'error': 'Book Not Found!'}), 404

@app.route('/books', methods=['POST'])
def add_books():
    new_books = request.get_json()
    if isinstance(new_books, list):
        for book_data in new_books:
            if 'title' not in book_data or 'author' not in book_data:
                return jsonify({'error': 'Each book must have a title and author'}), 400
            new_book = Book(title=book_data['title'], author=book_data['author'])
            db.session.add(new_book)
        db.session.commit()
        return jsonify({'message': 'Books added successfully'}), 201
    else:
        return jsonify({'error': 'Expected a list of books!'}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    book = Book.query.get(book_id)
    if book:
        book.title = book_data.get('title', book.title)
        book.author = book_data.get('author', book.author)
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    else:
        return jsonify({'error': 'Book not found!'}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get(book_id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'error': 'Book not found!'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
