from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def get_db():
    return sqlite3.connect("database.db")

# ---------------- LOGIN SYSTEM ----------------

@app.route("/register", methods=["GET","POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]
        role = "viewer"  # Default role

        conn = get_db()

        # Check if username already exists
        existing_user = conn.execute(
        "SELECT * FROM users WHERE username=?",
        (username,)
        ).fetchone()

        if existing_user:
            return render_template("register.html", error="Username already exists!")

        conn.execute(
        "INSERT INTO users(username,password,role) VALUES (?,?,?)",
        (username,password,role)
        )

        conn.commit()

        return redirect("/login")

    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()

        user = conn.execute(
        "SELECT * FROM users WHERE username=? AND password=?",
        (username,password)
        ).fetchone()

        if user:

            session["user"] = username
            session["role"] = user[3]

            return redirect("/")

        else:
            return "Invalid login"

    return render_template("login.html")


@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")

# ---------------- HOME ----------------

@app.route("/")
def home():

    if "user" not in session:
        return redirect("/login")

    return render_template(
        "index.html",
        role=session["role"],
        user=session["user"]
    )

# ---------------- ADD TRANSACTION ----------------

@app.route("/add", methods=["GET","POST"])
def add():

    if "user" not in session:
        return redirect("/login")

    # only admin can add
    if session["role"] != "admin":
        return "Access denied"

    if request.method == "POST":

        amount = request.form["amount"]
        ttype = request.form["type"]
        category = request.form["category"]
        date = request.form["date"]
        note = request.form["note"]

        conn = get_db()

        conn.execute(
        "INSERT INTO transactions(amount,type,category,date,note) VALUES (?,?,?,?,?)",
        (amount,ttype,category,date,note)
        )

        conn.commit()

        return redirect("/transactions")

    return render_template("add.html")

# ---------------- VIEW TRANSACTIONS ----------------

@app.route("/transactions")
def transactions():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    # Get filter parameters
    filter_type = request.args.get("type", "")
    filter_category = request.args.get("category", "")
    filter_date = request.args.get("date", "")

    # Build query based on filters
    query = "SELECT * FROM transactions WHERE 1=1"
    params = []

    if filter_type:
        query += " AND type=?"
        params.append(filter_type)

    if filter_category:
        query += " AND category=?"
        params.append(filter_category)

    if filter_date:
        query += " AND date=?"
        params.append(filter_date)

    data = conn.execute(query, params).fetchall()

    # Get unique categories for filter dropdown
    categories = conn.execute(
    "SELECT DISTINCT category FROM transactions ORDER BY category"
    ).fetchall()
    
    categories = [cat[0] for cat in categories if cat[0]]

    return render_template(
        "transactions.html",
        data=data,
        role=session["role"],
        categories=categories,
        filter_type=filter_type,
        filter_category=filter_category,
        filter_date=filter_date
    )

# ---------------- DELETE ----------------

@app.route("/delete/<int:id>")
def delete(id):

    if "user" not in session:
        return redirect("/login")

    # only admin can delete
    if session["role"] != "admin":
        return "Access denied"

    conn = get_db()

    conn.execute(
    "DELETE FROM transactions WHERE id=?",
    (id,)
    )

    conn.commit()

    return redirect("/transactions")

# ---------------- SUMMARY ----------------

@app.route("/summary")
def summary():

    if "user" not in session:
        return redirect("/login")

    conn = get_db()

    income = conn.execute(
    "SELECT SUM(amount) FROM transactions WHERE type='income'"
    ).fetchone()[0] or 0

    expense = conn.execute(
    "SELECT SUM(amount) FROM transactions WHERE type='expense'"
    ).fetchone()[0] or 0

    balance = income - expense

    return render_template(
        "summary.html",
        income=income,
        expense=expense,
        balance=balance
    )

# ---------------- ANALYST INSIGHTS ----------------

@app.route("/insights")
def insights():

    if "user" not in session:
        return redirect("/login")

    # Only admin and analyst can access insights
    if session["role"] not in ["admin", "analyst"]:
        return "Access denied"

    conn = get_db()

    # Get detailed analytics
    income = conn.execute(
    "SELECT SUM(amount) FROM transactions WHERE type='income'"
    ).fetchone()[0] or 0

    expense = conn.execute(
    "SELECT SUM(amount) FROM transactions WHERE type='expense'"
    ).fetchone()[0] or 0

    balance = income - expense

    # Category breakdown
    category_data = conn.execute(
    "SELECT category, type, SUM(amount) as total FROM transactions GROUP BY category, type ORDER BY total DESC"
    ).fetchall()

    # Monthly breakdown
    monthly_data = conn.execute(
    "SELECT DATE(date) as month, type, SUM(amount) as total FROM transactions GROUP BY DATE(date), type ORDER BY DATE(date) DESC"
    ).fetchall()

    # Transaction count
    total_transactions = conn.execute(
    "SELECT COUNT(*) FROM transactions"
    ).fetchone()[0]

    return render_template(
        "insights.html",
        income=income,
        expense=expense,
        balance=balance,
        category_data=category_data,
        monthly_data=monthly_data,
        total_transactions=total_transactions,
        role=session["role"]
    )

import os

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
