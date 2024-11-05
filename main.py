from flask import Flask, render_template, request
import requests
import smtplib
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
blog_data = requests.get("https://api.npoint.io/eeb9fbe29eeb0417386b").json()


@app.route('/')
def index():
    return render_template("index.html", data=blog_data)


@app.route('/about')
def about():
    return render_template("about.html")


@app.route('/post/<int:pid>')
def post_preview(pid):
    post = None
    for item in blog_data:
        if item["id"] == pid:
            post = item
    return render_template("post.html", data=post)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        send_mail(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


def send_mail(name, email, phone, message):
    mail_content = f"Subject: New Message\n\nName: {name}\nEmail: {email}\nPhone: {phone}\nmessage: {message}"

    with smtplib.SMTP(os.getenv("host"), 2525) as connection:
        connection.starttls()
        connection.login(user=os.getenv("uname"), password=os.getenv("password"))
        connection.sendmail(from_addr=os.getenv("from"),
                            to_addrs=os.getenv("to"),
                            msg=mail_content)
        print("Mail Sent")


if __name__ == "__main__":
    app.run(debug=True)
