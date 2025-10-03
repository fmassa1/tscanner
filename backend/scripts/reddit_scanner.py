import requests
import datetime
import time
from sql.dbFunctions import addUserToDB, addPostToDB, addCommentToDB, getAllUsers
from scripts.hate_scanner import calculate_risk_score

reddit_urls = [   #"https://www.reddit.com/r/uichicago/.json?limit=100",
               "https://www.reddit.com/r/greentext/.json?limit=100", 
               "https://www.reddit.com/r/4chan/.json?limit=100", 
               "https://www.reddit.com/r/PoliticalCompassMemes/.json",
            #    "https://www.reddit.com/r/SocialJusticeInAction/.json", BANNED
               "https://www.reddit.com/r/LoveForLandlords/.json?limit=100", 
            #    "https://www.reddit.com/r/AntiHateCommunites/.json" GONE
               ]
headers = {"User-Agent": "MyRedditApp/0.1"}

posts_data = []



def make_request(url):
    time.sleep(1)
    return requests.get(url, headers=headers)

def get_post_data(post):
    post_data = {
        "id": post.get("id"),
        "title": post.get("title"),
        "selftext": post.get("selftext"),
        "author": post.get("author"),
        "author_fullname": post.get("author_fullname"),
        "num_comments": post.get("num_comments"),
        "ups": post.get("ups"),
        "url": post.get("url"),
        "subreddit": post.get("subreddit"),
        "permalink": f"https://www.reddit.com{post.get('permalink')}",
        "created_on": datetime.datetime.fromtimestamp(post.get("created_utc"), tz=datetime.timezone.utc),
        "comments": []
    }

    if post_data.get("author") == "[deleted]":
        post_data["author_fullname"] = "[deleted]"

    return post_data

def get_comment_data(comment):
    new_comment = {
        "author": comment.get("author"),
        "author_fullname": comment.get("author_fullname"),
        "body": comment.get("body"),
        "ups": comment.get("ups"),
        "id": comment.get("id"),
        "parent_id": comment.get("parent_id"),
        "subreddit": comment.get("subreddit"),
        "url": f"https://www.reddit.com{comment.get('permalink')}",
        "created_on": datetime.datetime.fromtimestamp(comment.get("created_utc"), tz=datetime.timezone.utc),

    }
    if new_comment.get("author") == "[deleted]":
        new_comment["author_fullname"] = "[deleted]"
    
    return new_comment

def get_posts():
    for url in reddit_urls:
        response = make_request(url)
        if response.status_code == 200:
            data = response.json()
            children = data["data"]["children"]

            for child in children:
                post = child["data"]
                post_data = get_post_data(post)

                posts_data.append(post_data)
                addUserToDB(post_data)
                addPostToDB(post_data)
        else:
            print(f"Failed to fetch {url}: {response.status_code}")


def check_posts():
    for post in posts_data:
        api_url = post["permalink"] + ".json"
        response = make_request(api_url)
        if response.status_code == 200:
            data = response.json()
            comments_data = data[1]["data"]["children"]
            comments = []

            for c in comments_data:
                if c["kind"] == "t1":
                    comment = c["data"]
                    new_comment = get_comment_data(comment)

                    comments.append(new_comment)
                    addUserToDB(new_comment)
                    addCommentToDB(new_comment)
                    
            
            post["comments"] = comments

def check_profile(profile):
    api_url = profile["url"] + ".json"
    response = make_request(api_url)
    if response.status_code == 200:
        data = response.json()
        user_post = data["data"]["children"]
        comments = []

        for p in user_post:
            if p["kind"] == "t1":
                comment = p["data"]
                new_comment = get_comment_data(comment)
                comments.append(new_comment)
                addCommentToDB(new_comment)
            if p["kind"] == "t3":
                post = p["data"]
                post_data = get_post_data(post)
                posts_data.append(post_data)
                addPostToDB(post_data)



print(calculate_risk_score("I hate you"))
# get_posts()
# check_posts()
# users = getAllUsers()
# for u in users:
#     check_profile(u)
# print(len(posts_data[:5]))
# for p in posts_data:
#     print(p)