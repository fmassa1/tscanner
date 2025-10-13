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


@app.route("/subreddit_stats")
def subreddit_stats():
    data = get_subreddit_risk_data()

    subreddits = [row['subreddit'] for row in data]
    avg_risk = [row['avg_risk'] for row in data]
    post_counts = [row['post_count'] for row in data]

    return render_template("subreddits.html", subreddits=subreddits, avg_risk=avg_risk, post_counts=post_counts)

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=5000, debug=True)
    #app.run(debug=True)