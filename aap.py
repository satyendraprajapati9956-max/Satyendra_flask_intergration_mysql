from flask import Flask, render_template, request, redirect
import mysql.connector
from datetime import datetime

app = Flask(__name__)

def get_db_connection():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="4022",
        database="todo_db"
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM tasks ORDER BY due_date ASC")
    tasks = cursor.fetchall()
    conn.close()

    # Divide tasks into categories
    categories = {"morning": [], "afternoon": [], "evening": [], "night": []}
    for task in tasks:
        categories[task["category"]].append(task)

    return render_template("index.html", categories=categories)

@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    due_date = request.form.get('due_date')
    category = request.form.get('category')
    note = request.form.get('note')

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, due_date, category, note) VALUES (%s,%s,%s,%s)",
        (title, due_date, category, note)
    )
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/complete/<int:task_id>')
def complete(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/delete/<int:task_id>')
def delete(task_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)
