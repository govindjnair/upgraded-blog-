from flask import Flask, render_template, request
import requests

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
    return render_template("post.html", data = post)

@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        data = request.form
        print(data)
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)

if __name__ == "__main__":
    app.run(debug=True)