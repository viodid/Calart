from flask import Flask, render_template, request, redirect, session
from flask_mobility import Mobility

from cs50 import SQL
from helpers import hash, checkPasswordhash, loginRequired
import os

app = Flask(__name__)
Mobility(app)

# REMEMBER UNCOMMENT FOR DEPLOYMENT
# app.config.from_pyfile("config.py")
app.config.from_pyfile("dev_config.py")


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calart.db")

mobile_devices = ["android", "iphone", "windows phone"]
user_agent = ""


@app.route("/")
def index():
    # print(request.user_agent.platform)
    # load diferent pages as diferent devices
    user_agent = request.user_agent.platform
    if user_agent not in mobile_devices:
        return render_template("desktop/index.html")
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("email/username"):
            return render_template(
                "apology.html", top=400, bottom="Debes_añadir_tu_correo"
            )

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template(
                "apology.html", top=400, bottom="Debes_añadir_tu_contraseña"
            )

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE email = ? OR username = ?",
            request.form.get("email/username"),
            request.form.get("email/username"),
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not checkPasswordhash(
            rows[0]["hash"], request.form.get("password")
        ):
            return render_template(
                "apology.html", top=400, bottom="correo_y~so_contraseña_inválidos"
            )

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]
        # Provide a username in the session
        session["username"] = rows[0]["username"]
        # Select default theme from db
        session["theme"] = rows[0]["theme"]

        # Redirect user to home page
        return index()

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Ensure emai was submitted
        if not email:
            return render_template(
                "apology.html", top=400, bottom="Debes_añadir_tu_email"
            )

        # Ensure username was submitted
        elif not username:
            return render_template(
                "apology.html", top=400, bottom="Debes_añadir_tu_usuario"
            )

        # Ensure password was submitted
        elif not password:
            return render_template(
                "apology.html", top=400, bottom="Debes_añadir_tu_contraseña"
            )

        # Query database for email
        email_db = db.execute("SELECT email FROM users WHERE email = ?", email)

        # Ensure email do not exists
        if len(email_db) != 0:
            return render_template(
                "apology.html", top=400, bottom="Este email ya está registrado"
            )

        # Query database for username
        username_db = db.execute(
            "SELECT username FROM users WHERE username = ?", username
        )

        # Ensure username do not exists
        if len(username_db) != 0:
            return render_template(
                "apology.html", top=400, bottom="Este usuario ya está registrado"
            )

        db.execute(
            "INSERT INTO users(email, hash, username) VALUES(?, ?, ?)",
            email,
            hash(password),
            username,
        )
        rows = db.execute("SELECT * FROM users WHERE email = ?", email)
        session["user_id"] = rows[0]["id"]
        session["username"] = rows[0]["username"]
        # Redirect user to home page
        return redirect("/")

    return render_template("register.html")


@app.route("/profile", methods=["GET", "POST"])
@loginRequired
def profile():
    if request.method == "POST":
        theme = request.form.get("theme")
        session["theme"] = theme
        db.execute(
            "UPDATE users SET theme = ? WHERE username = ?", theme, session["username"]
        )

    return render_template("profile.html")


@app.route("/change", methods=["GET", "POST"])
@loginRequired
def change():
    if request.method == "POST":
        last_password = request.form.get("last_password")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not last_password or not password or not password:
            return render_template(
                "apology.html", top=400, bottom="Al_menos_un_campo_sin_rellenar"
            )
        elif password != confirmation:
            return render_template(
                "apology.html", top=400, bottom="Las_contraseñas_no_coinciden_:("
            )
        # update username's password into the db
        db.execute(
            "UPDATE users SET hash = ? WHERE username = ?",
            hash(password),
            session["username"],
        )
        # Redirect user to login
        return redirect("/login")

    return render_template("change.html")


@app.route("/social")
def social():
    return render_template("social.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
