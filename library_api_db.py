from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        user='root',  
        password='password',  
        database='library_db'  
    )
    return conn

@app.route('/books', methods=['GET'])
def get_books():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify({'books': books})

@app.route('/books/<int:book_id>', methods=['GET'])
def get_specific_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    cursor.close()
    conn.close()
    if book:
        return jsonify({'book': book})
    else:
        return jsonify({'error': 'Book Not Found!'}), 404

@app.route('/books', methods=['POST'])
def add_books():
    new_books = request.get_json()
    if isinstance(new_books, list):  
        conn = get_db_connection()
        cursor = conn.cursor()
        for book in new_books:
            if 'title' not in book or 'author' not in book:
                return jsonify({'error': 'Each book must have a title and author'}), 400
            cursor.execute('INSERT INTO books (title, author) VALUES (%s, %s)', (book['title'], book['author']))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Books added successfully'}), 201
    else:
        return jsonify({'error': 'Expected a list of books!'}), 400

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book_data = request.get_json()
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('UPDATE books SET title = %s, author = %s WHERE id = %s',
                       (book_data['title'], book_data['author'], book_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book updated successfully'})
    else:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Book not found!'}), 404

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM books WHERE id = %s', (book_id,))
    book = cursor.fetchone()
    if book:
        cursor.execute('DELETE FROM books WHERE id = %s', (book_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        cursor.close()
        conn.close()
        return jsonify({'error': 'Book not found!'}), 404

if __name__ == '__main__':
    app.run(debug=True)
