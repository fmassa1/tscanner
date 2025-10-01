from flask import Flask, request, jsonify, render_template, redirect
from sql.dbFunctions import *


app = Flask(__name__, template_folder="../frontend/pages", static_folder="../frontend/static",)


@app.route('/', methods=['GET']) 
def index():
    users = getAllUsers()
    return render_template("home.html", users=users)


@app.route("/user/<username>")
def user_page(username):
    posts = getUsersPosts(username)
    comments = getUsersComments(username)
    return render_template("user.html", username=username, posts=posts, comments=comments)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
    #app.run(debug=True)