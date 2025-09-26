import requests

reddit_urls = ["https://www.reddit.com/r/uichicago/.json"]
headers = {"User-Agent": "MyRedditApp/0.1"}

posts_data = []

def get_posts():
    for url in reddit_urls:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            children = data["data"]["children"]

            for child in children:
                post = child["data"]
                posts_data.append({
                    "title": post.get("title"),
                    "selftext": post.get("selftext"),
                    "author": post.get("author"),
                    "author_fullname": post.get("author_fullname"),
                    "num_comments": post.get("num_comments"),
                    "ups": post.get("ups"),
                    "url": post.get("url"),
                    "permalink": f"https://www.reddit.com{post.get('permalink')}",
                    "comments": []
                })
        else:
            print(f"Failed to fetch {url}: {response.status_code}")


def check_posts():
    for post in posts_data:
        api_url = post["permalink"] + ".json"
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            data = response.json()
            comments_data = data[1]["data"]["children"]
            comments = []

            for c in comments_data:
                if c["kind"] == "t1":
                    comment = c["data"]
                    comments.append({
                        "name": comment.get("author"),
                        "author": comment.get("author"),
                        "body": comment.get("body"),
                        "ups": comment.get("ups"),
                        "id": comment.get("id"),
                        "parent_id": comment.get("parent_id"),
                    })
            
            post["comments"] = comments

get_posts()
check_posts()
print(len(posts_data[:5]))
for p in posts_data:
    print(p)