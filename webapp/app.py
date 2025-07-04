import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'uploads')
app.config['SECRET_KEY'] = 'changeme'
DATABASE = os.path.join(app.root_path, 'orders.db')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                quote_file TEXT,
                purchase_file TEXT,
                delivered_file TEXT
            )"""
    )
    conn.commit()
    conn.close()


@app.route('/')
def index():
    conn = get_db()
    orders = conn.execute('SELECT * FROM orders').fetchall()
    conn.close()
    return render_template('index.html', orders=orders)


@app.route('/order/new', methods=['GET', 'POST'])
def new_order():
    if request.method == 'POST':
        name = request.form['name']
        conn = get_db()
        conn.execute('INSERT INTO orders (name) VALUES (?)', (name,))
        conn.commit()
        conn.close()
        flash('Order created')
        return redirect(url_for('index'))
    return render_template('new_order.html')


@app.route('/order/<int:order_id>/upload/<file_type>', methods=['POST'])
def upload_file(order_id, file_type):
    if file_type not in ['quote', 'purchase', 'delivered']:
        flash('Invalid file type')
        return redirect(url_for('index'))
    file = request.files.get('file')
    if not file:
        flash('No file selected')
        return redirect(url_for('index'))
    filename = f"{order_id}_{file_type}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)

    column = f"{file_type}_file"
    conn = get_db()
    conn.execute(f'UPDATE orders SET {column} = ? WHERE id = ?', (filename, order_id))
    conn.commit()
    conn.close()
    flash(f'{file_type.capitalize()} file uploaded')
    return redirect(url_for('index'))


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')
