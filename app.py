from flask import Flask, render_template, request, redirect, session
from cs50 import SQL
from helpers import hash, checkPasswordhash, loginRequired

from flask_mail import Mail, Message


app = Flask(__name__)

mail = Mail(app)


app.config.from_pyfile("config.py")

mail = Mail(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///calart.db")


@app.route("/")
def index():
    print(mail.MAIL_USERNAME)
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
        return redirect("/profile")

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

        # send confirmation email
        subject = "Bienvenido a Calat33🌱 🌎"
        message = f"""\
        ¡Bienvenid@ a bordo {username}!<br><br>
        Gracias por registrarte en nuestra página web! De ahora en adelante irás recibiendo noticias sobre nuestras andadurías.<br>
        Si no deseas recibir más correos, simplemente responde a cualquier email con la palabra baja.<br><br>
        Nos emociona que quieras ser parte del cambio,<br><br>
        El equipo de Calat33."""
        sendmail(message, subject, [email])

        # Redirect user to home page
        return redirect("/profile")

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
        password_input = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Query database for username
        password = db.execute(
            "SELECT hash FROM users WHERE username = ?", session["username"]
        )

        if not last_password or not password_input or not confirmation:
            return render_template(
                "apology.html", top=400, bottom="Al_menos_un_campo_sin_rellenar"
            )

        if not checkPasswordhash(password[0]["hash"], last_password):

            return render_template(
                "apology.html", top=400, bottom="contraseña_incorrecta"
            )
        elif password_input != confirmation:
            return render_template(
                "apology.html", top=400, bottom="Las_contraseñas_no_coinciden_:("
            )
        # update username's password into the db
        db.execute(
            "UPDATE users SET hash = ? WHERE username = ?",
            hash(password_input),
            session["username"],
        )
        # Redirect user to login
        return redirect("/login")

    return render_template("change.html")


@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        email = request.form.get("email")
        message = request.form.get("message")

        if not name or not email:
            return render_template(
                "apology.html", top=400, bottom="Campos_requeridos_sin_rellenar"
            )
        elif not message:
            return render_template(
                "apology.html", top=400, bottom="Mensaje_sin_escribir"
            )

        message = f"""\
        {request.form.get("message")}<br><br>
        <b>From:</b> {name} {surname}<br>{email}
        """

        subject = "Form Contact Page"

        sendmail(message, subject, ["calat33@gmail.com"])

        return render_template("apology.html", top=200, bottom="Mensaje_Enviado!")

    return render_template("contact.html")


@app.route("/social")
def social():
    return render_template("social.html")


@app.route("/artist")
def artist():
    return render_template("artist.html")


def sendmail(message_client, subject, recipients):
    msg = Message(subject, recipients=recipients)
    message = f"""\
        <html>
            <body style="padding:1.5rem; background: transparent; font-size:1.1rem; font">
                <div style="display:flex; justify-content:center; align-items:center; margin-bottom:2rem;">
                    <img src="https://i.ibb.co/xmtSkh6/calat-email.png" style="max-width:300px">
                </div>
                <p>{message_client}</p>
                <div>
                    <a href="https://www.facebook.com/CALAT-33-169199418110806" style='margin-right: 0.5rem;'>
                        Facebook
                    </a>
                    <a href="https://www.instagram.com/calat33/" style='margin-right: 0.5rem;'>
                        Instagram
                    </a>
                    <a href="https://twitter.com/hashtag/calat33">
                        Twitter
                    </a>
                </div>
            </body>
        </html>
        """
    msg.html = message
    mail.send(msg)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
