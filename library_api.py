from flask import Flask, jsonify, request
from flask_mysqldb import MySQL

app = Flask(__name__)

books = [
    {'id': 1, 'title': 'The lord of rings', 'author': 'J.R.R'},
    {'id': 2, 'title': 'Harry potter and the Sorcerer\'s Stone', 'author': 'J.K'}
]

app.config['MYSQL_HOST'] = 'localhost' 
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345678'
app.config['MYSQL_DB'] = 'Library'

mysql = MySQL(app)

def find_book(book_id):
    for book in books:
        if book['id'] == book_id:
            return book
    return None

def get_next_book_id():
    if books:
        return max(book['id'] for book in books) + 1  
    else:
        return 1  

@app.route('/books', methods=['GET'])
def get_books():
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    cursor.close()
    return jsonify({'books': books})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_specific_book(book_id):
    cursor = mysql.connection.cursor()
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    cursor.close()
    book = find_book(book_id)
    if book:
        return jsonify({'book': book})
    else:
        return jsonify({'error': 'Book Not Found!'}), 404

@app.route('/books', methods=['POST'])
def add_books():
    new_books = request.get_json()
    cursor = mysql.connection.cursor()
    if isinstance(new_books, list):
        for book in new_books:
            if 'title' not in book or 'author' not in book:
                return jsonify({'error': 'Each book must have a title and author'}), 400
            cursor.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (book['title'], book['author']))
        mysql.connection.commit()
        return jsonify({'message': 'Books added successfully'}), 201
    else:
        return jsonify({'error': 'Expected a list of books!'}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE books SET title = %s, author = %s WHERE id = %s', (data['title'], data['author'], book_id))
    mysql.connection.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
    mysql.connection.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
