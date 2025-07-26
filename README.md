###To-do List App Project:

---

````markdown
# 📝 Flask To-Do List App with MySQL

A simple, categorized to-do list web application built using **Flask** and **MySQL**. Users can add, view, filter, complete, and delete tasks. All data is stored persistently in a MySQL database.

---

## 📁 Project Folder: `Arch_Internship_Projects/`

### 📦 Features
- ✅ Add tasks with categories (Work, Personal, Other)
- 🎯 Mark tasks as completed
- 🗑️ Delete completed tasks
- 📂 Filter tasks by category
- 💾 Data persists via MySQL database
- 🎨 Responsive, styled HTML/CSS frontend

---

## 🚀 Getting Started

### 🔧 Prerequisites
Make sure the following are installed:
- Python 3.x
- MySQL Server
- `pip` package manager

### 📦 Install Dependencies
```bash
pip install flask flask-mysqldb
````

---

## 🗃️ MySQL Setup

Create the database and table using the following SQL:

```sql
CREATE DATABASE tododb;

USE tododb;

CREATE TABLE tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    task TEXT NOT NULL,
    category VARCHAR(50),
    completed BOOLEAN DEFAULT FALSE
);
```

---

## 🧾 File Structure

```
Arch_Internship_Projects/
├── app.py                  # Main Flask app
├── templates/
│   └── index.html          # HTML frontend
├── static/
│   └── style.css           # Styling file
└── README.md               # Project documentation
```

---

## ⚙️ Configuration

Update MySQL credentials in `app.py`:

```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Your MySQL password
app.config['MYSQL_DB'] = 'tododb'
```

---

## ▶️ Run the App

```bash
python app.py
```

Then open in browser:
[http://127.0.0.1:5000](http://127.0.0.1:5000)

---
## 📌 Features

* This app is for educational/demo purposes only.
* You can enhance it by adding:

  * Deadlines
  * Priorities
  * Authentication system
  * Dark mode!

---

## 🙌 Contributions

Contributions are welcome!
Open issues or submit pull requests to improve this project.

---

## 📄 License
```
This project is open source and free for learning and personal use.
```
