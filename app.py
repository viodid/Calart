from flask import Flask, render_template, request
from cs50 import SQL
from helpers import hash, check_password_hash

app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calart.db")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template(
                "apology.html", top=403, bottom="Debes añadir tu correo"
            )

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template(
                "apology.html", top=403, bottom="Debes añadir tu contraseña"
            )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE email = ?", request.form.get("email")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template(
                "apology.html", top=403, bottom="correo y/o contraseña inválidos"
            )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Provide a username in the session
        session["username"] = rows[0]["username"]

        # Redirect user to home page
        return redirect("/")

    return render_template("login.html")


@app.route("/social")
def social():
    return render_template("social.html")
