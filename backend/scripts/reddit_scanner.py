import requests

reddit_urls = [   "https://www.reddit.com/r/uichicago/.json",
               ]
headers = {"User-Agent": "MyRedditApp/0.1"}

reddit_data = []
posts_data = []

for url in reddit_urls:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        children = data["data"]["children"]

        for child in children:
            post = child["data"]
            posts_data.append({
                "title": post.get("title"),
                #"selftext": post.get("selftext"),
                "author": post.get("author"),
                "author_fullname": post.get("author_fullname"),
                "num_comments": post.get("num_comments"),
                "ups": post.get("ups"),
            })
    else:
        print(f"Failed to fetch {url}: {response.status_code}")

print(len(posts_data))
for p in posts_data:
    print(p)