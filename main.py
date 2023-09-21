from flask import Flask, render_template, request
import requests
import smtplib
from email.mime.text import MIMEText

OWN_EMAIL = "OWN_EMAIL"
OWN_PASSWORD = "OWN_EMAIL"  # security application password, not account password

BLOG_API_URL = "https://api.npoint.io/eb6cd8a5d783f501ee7d"
posts = requests.get(BLOG_API_URL).json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


# @app.route("/contact")
# def contact():
#     return render_template("contact.html")
#
# @app.route("/form-entry", methods=["POST"])
# def receive_data():
#     data = request.form
#     print(data["name"])
#     print(data["email"])
#     print(data["phone"])
#     print(data["message"])
#     return "<h1>Successfully sent your message</h1>"

@app.route("/contact", methods=["GET","POST"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data["name"])
        print(data["email"])
        print(data["phone"])
        print(data["message"])
        # return "<h1>Successfully sent your message</h1>"
        return render_template("contact.html", message_sent=True)
    return render_template("contact.html", message_sent=False)

def send_email(name, email, phone, message):
    email_message = f"Subject:New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nMessage:{message}"
    body = MIMEText(email_message)
    with smtplib.SMTP_SSL("smtp.gmail.com", 456) as connection:
        connection.starttls()
        connection.login(OWN_EMAIL, OWN_PASSWORD)
        connection.sendmail(OWN_EMAIL, OWN_EMAIL, body)
    print('message sent!')

@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
