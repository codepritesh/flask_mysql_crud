from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app,origins=["http://www.domain1.com", "http://www.domain2.com","http://localhost:5173"])
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@localhost:3308/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

    def __init__(self, title, author):
        self.title = title
        self.author = author

class Employee(db.Model):
    code = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    age = db.Column(db.Integer,nullable=False)
    experience = db.Column(db.Integer,nullable=False)
    salary = db.Column(db.Integer,nullable=False)

    def __init__(self, name, age, experience, salary):
        self.name = name
        self.age = age
        self.experience = experience
        self.salary = salary

# read all data
        
@app.route('/employee', methods=['GET'])
def get_employee_all():
    employees = Employee.query.all()
    emp_list =[]
    for employee in employees:
        emp_list.append({ code: "001", name: "pritesh", age: 30, experience: 5, salary: 550000 })


@app.route('/books', methods=['GET'])
def get_books_all():
    books = Book.query.all()
    book_list = []
    for book in books:
        book_list.append({'id': book.id, 'title': book.title, 'author': book.author})
    return jsonify(book_list)

@app.route('/paginatebooks', methods=['GET'])
def get_books_pagination():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    books = Book.query.paginate(page, per_page, error_out=False)
    
    book_list = []
    for book in books.items:
        book_list.append({'id': book.id, 'title': book.title, 'author': book.author})
    
    return jsonify({
        'books': book_list,
        'total_pages': books.pages,
        'current_page': books.page,
        'total_books': books.total
    })

# read single data
@app.route('/books/<int:book_id>', methods=['GET'])
def get_book_single(book_id):
    book = Book.query.get_or_404(book_id)
    return jsonify({'id': book.id, 'title': book.title, 'author': book.author})

@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'}), 201

@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = Book.query.get_or_404(book_id)
    data = request.get_json()
    book.title = data['title']
    book.author = data['author']
    db.session.commit()
    return jsonify({'message': 'Book updated successfully'})

@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()
    return jsonify({'message': 'Book deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True, host="localhost", port="5000")
