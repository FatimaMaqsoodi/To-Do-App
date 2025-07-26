from flask import Flask, render_template, request, redirect, url_for, send_file
from flask_mysqldb import MySQL
import json
import os
from datetime import datetime, date

app = Flask(__name__)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'tododb'

mysql = MySQL(app)

BACKUP_FILE = 'tasks_backup.json'


# Load tasks from file into DB once
def load_tasks_from_file():
    if os.path.exists(BACKUP_FILE):
        try:
            with open(BACKUP_FILE, 'r', encoding='utf-8') as f:
                tasks = json.load(f)
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(" Error loading JSON file:", e)
            return

        cur = mysql.connection.cursor()
        for task in tasks:
            due_date = task.get('due_date')
            if due_date:
                try:
                    due_date = datetime.strptime(due_date, '%Y-%m-%d').date()
                except ValueError:
                    due_date = None

            cur.execute("""
                INSERT IGNORE INTO tasks (id, task, category, completed, due_date, priority)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (
                task['id'], task['task'], task['category'], task['completed'], due_date, task.get('priority')
            ))
        mysql.connection.commit()
        cur.close()


# Save tasks to JSON file
def save_tasks_to_file():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, task, category, completed, due_date, priority FROM tasks")
    tasks = cur.fetchall()
    cur.close()

    tasks_data = []
    for t in tasks:
        due_date_str = t[4].strftime('%Y-%m-%d') if isinstance(t[4], (datetime, date)) else None
        tasks_data.append({
            'id': t[0],
            'task': t[1],
            'category': t[2],
            'completed': bool(t[3]),
            'due_date': due_date_str,
            'priority': t[5]
        })

    try:
        with open(BACKUP_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks_data, f, indent=4, ensure_ascii=False)
        print(" Tasks saved to JSON.")
    except Exception as e:
        print(" Failed to save JSON:", e)


# Run once before first request
@app.before_request
def init():
    if not hasattr(app, '_init_done'):
        load_tasks_from_file()
        app._init_done = True


@app.route("/")
def index():
    category = request.args.get('category', 'All')
    show_completed = request.args.get('completed', 'false') == 'true'

    cur = mysql.connection.cursor()
    if category == 'All':
        if show_completed:
            cur.execute("SELECT * FROM tasks WHERE completed = TRUE")
        else:
            cur.execute("SELECT * FROM tasks WHERE completed = FALSE")
    else:
        if show_completed:
            cur.execute("SELECT * FROM tasks WHERE category = %s AND completed = TRUE", (category,))
        else:
            cur.execute("SELECT * FROM tasks WHERE category = %s AND completed = FALSE", (category,))

    tasks = cur.fetchall()
    cur.execute("SELECT DISTINCT category FROM tasks")
    categories = [row[0] for row in cur.fetchall()]
    cur.close()

    return render_template("index.html", tasks=tasks, category=category, categories=categories, show_completed=show_completed)


@app.route("/add", methods=["POST"])
def add():
    task = request.form['task']
    category = request.form['category']
    due_date = request.form.get('due_date')
    priority = request.form.get('priority')

    if due_date == '':
        due_date = None

    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO tasks (task, category, due_date, priority) VALUES (%s, %s, %s, %s)",
                (task, category, due_date, priority))
    mysql.connection.commit()
    cur.close()
    save_tasks_to_file()
    return redirect(url_for('index'))


@app.route("/complete/<int:task_id>")
def complete(task_id):
    cur = mysql.connection.cursor()
    cur.execute("UPDATE tasks SET completed = TRUE WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    save_tasks_to_file()
    return redirect(url_for('index'))


@app.route("/delete/<int:task_id>")
def delete(task_id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
    mysql.connection.commit()
    cur.close()
    save_tasks_to_file()
    return redirect(url_for('index'))


@app.route("/clear_history", methods=["POST"])
def clear_history():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM tasks WHERE completed = TRUE")
    mysql.connection.commit()
    cur.close()
    save_tasks_to_file()
    return redirect(url_for('index'))


@app.route("/export")
def export():
    save_tasks_to_file()
    return send_file(BACKUP_FILE, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
