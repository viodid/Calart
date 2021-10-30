from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from helpers import hash, checkPasswordhash, loginRequired

app = Flask(__name__)
app.config.from_pyfile("config.py")


# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calart.db")


@app.route("/")
def index():
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

        # Redirect user to home page
        return redirect("/")

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
        pass

    return render_template("profile.html")


@app.route("/social")
def social():
    return render_template("social.html")


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
