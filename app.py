from flask import Flask, render_template, request, redirect
from datetime import datetime
import sqlite3

app = Flask(__name__)

# --- Database ---
def init_db():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS transactions
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  type TEXT,
                  amount INTEGER,
                  note TEXT,
                  date TEXT)''')
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("SELECT id, type, amount, note, date FROM transactions ORDER BY id DESC")
    rows = c.fetchall()
    conn.close()
    return rows

def add_transaction(t_type, amount, note, date):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("INSERT INTO transactions (type, amount, note, date) VALUES (?, ?, ?, ?)",
              (t_type, amount, note, date))
    conn.commit()
    conn.close()

def delete_transaction(tid):
    conn = sqlite3.connect("data.db")
    c = conn.cursor()
    c.execute("DELETE FROM transactions WHERE id=?", (tid,))
    conn.commit()
    conn.close()

# --- Routes ---
@app.route("/")
def index():
    transactions = get_transactions()
    total_income = sum(t[2] for t in transactions if t[1] == "income")
    total_expense = sum(t[2] for t in transactions if t[1] == "expense")
    balance = total_income - total_expense

    return render_template("index.html",
                           transactions=transactions,
                           total_income=total_income,
                           total_expense=total_expense,
                           balance=balance)

@app.route("/add", methods=["POST"])
def add():
    t_type = request.form.get("type")
    amount = int(request.form.get("amount"))
    note = request.form.get("note")
    date = datetime.now().strftime("%d-%m-%Y %H:%M")

    add_transaction(t_type, amount, note, date)
    return redirect("/")

@app.route("/delete/<int:tid>")
def delete(tid):
    delete_transaction(tid)
    return redirect("/")

if __name__ == "__main__":
    init_db()
    app.run(debug=True)