from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

# -------- DATABASE --------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS patients (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age TEXT, disease TEXT)")

    conn.commit()
    conn.close()

init_db()

# -------- LOGIN --------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = c.fetchone()
        conn.close()

        if user:
            session["user"] = username
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid login")

    return render_template("login.html")


# -------- REGISTER --------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        conn.close()

        return redirect("/")

    return render_template("register.html")


# -------- DASHBOARD --------
@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    return render_template("dashboard.html")


# -------- ADD PATIENT --------
@app.route("/add", methods=["GET", "POST"])
def add():
    if "user" not in session:
        return redirect("/")

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        disease = request.form.get("disease")

        conn = sqlite3.connect("database.db")
        c = conn.cursor()
        c.execute("INSERT INTO patients (name, age, disease) VALUES (?, ?, ?)", (name, age, disease))
        conn.commit()
        conn.close()

        return redirect("/view")

    return render_template("add.html")


# -------- VIEW PATIENTS --------
@app.route("/view")
def view():
    if "user" not in session:
        return redirect("/")

    conn = sqlite3.connect("database.db")
    c = conn.cursor()
    c.execute("SELECT * FROM patients")
    data = c.fetchall()
    conn.close()

    patients = []
    for row in data:
        patients.append({
            "id": row[0],
            "name": row[1],
            "age": row[2],
            "disease": row[3]
        })

    return render_template("view.html", patients=patients)


# -------- LOGOUT --------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# -------- RUN --------
if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    