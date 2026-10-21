
from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def connect():
    return sqlite3.connect("attendance.db")

def create_table():
    con = connect()
    con.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            total INTEGER DEFAULT 0,
            present INTEGER DEFAULT 0
        )
    """)
    con.commit()
    con.close()

@app.route("/", methods=["GET", "POST"])
def home():
    con = connect()

    if request.method == "POST":
        name = request.form["name"]
        con.execute("INSERT INTO students (name) VALUES (?)", (name,))
        con.commit()

    students = con.execute("SELECT * FROM students").fetchall()
    con.close()
    return render_template("index.html", students=students)

@app.route("/mark/<int:id>/<status>")
def mark(id, status):
    con = connect()
    con.execute(
        "UPDATE students SET total = total + 1, "
        "present = present + ? WHERE id = ?",
        (1 if status == "Present" else 0, id)
    )
    con.commit()
    con.close()
    return redirect("/")

create_table()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
