from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from helpers import hash, check_password_hash

app = Flask(__name__)
app.config.from_pyfile("configuration.py")

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calart.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email/username"):
            return render_template(
                "apology.html", top=403, bottom="Debes_añadir_tu_correo"
            )

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template(
                "apology.html", top=403, bottom="Debes_añadir_tu_contraseña"
            )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?",
            request.form.get("email/username"),
            request.form.get("email/username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template(
                "apology.html", top=403, bottom="correo_y~so_contraseña_inválidos"
            )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Provide a username in the session
        session["username"] = rows[0]["username"]

        print(session)

        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")


@app.route("/social")
def social():
    return render_template("social.html")
