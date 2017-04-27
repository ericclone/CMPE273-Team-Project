from flask import Flask, render_template
from flask_mail import Mail,  Message
from flask import request

app = Flask(__name__)

app.config.update(
    MAIL_SERVER = 'smtp.gmail.com',
    MAIL_PORT = 465,
    MAIL_USE_SSL = True,
    MAIL_USERNAME = 'sjsu.cmpe273.test@gmail.com',
    MAIL_PASSWORD = 'sjsu1234'
)
mail = Mail(app)

@app.route("/send_mail", methods=['GET', 'POST'])
def send_mail():
    email = request.form.get('email')
    msg = mail.send_message(
        'Hello',
        sender='sjsu.cmpe273.test@gmail.com',
        recipients=[email],
        body="Testing"
    )
    return email


@app.route("/index", methods=['GET', 'POST'])
def index():
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')