from sql.mysql_connector import get_connection

def addUserToDB(post):
    conn = get_connection()
    cursor = conn.cursor()
    check = """
            SELECT 1 
            FROM users 
            WHERE username = %s
            """
    check_value = (post.get("author"),)
    cursor.execute(check, check_value)

    if cursor.fetchone() is None:
        sql = """
            INSERT INTO users (url, username, id)
            VALUES (%s, %s, %s)
        """
        values = (
            f"https://www.reddit.com/user/{post.get('author')}",
            post.get("author"),
            post.get("author_fullname"),
        )
        cursor.execute(sql, values)
        conn.commit()

    else:
        print(f"User already exists in DB: {post.get('username')}")

    cursor.close()
    conn.close()

def addPostToDB(post):
    conn = get_connection()
    cursor = conn.cursor()

    check = """
            SELECT 1 
            FROM posts 
            WHERE url = %s
            """
    check_value = (post.get("permalink"),)
    cursor.execute(check, check_value)

    if cursor.fetchone() is None:
        sql = """
              INSERT INTO posts (post_id, url, title, author, body, comments, ups, created_on, subreddit)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
              """
        values = (
            post.get("id"),
            post.get("permalink"),
            post.get("title"),
            post.get("author"),
            post.get("selftext"),
            post.get("num_comments"),
            post.get("ups"),
            post.get("created_on"),
            post.get("subreddit"),
        )
        cursor.execute(sql, values)
        conn.commit()
    else:
        print(f"Post already exists in DB: {post.get('title')}")

    cursor.close()
    conn.close()

def addCommentToDB(post):
    conn = get_connection()
    cursor = conn.cursor()
    check = """
            SELECT 1 
            FROM comments 
            WHERE url = %s
            """
    check_value = (post.get("url"),)
    cursor.execute(check, check_value)

    if cursor.fetchone() is None:
        sql = """
            INSERT INTO comments (post_id, parent_id, author, body, url, ups, created_on, subreddit)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
        values = (
            post.get("id"),
            post.get("parent_id"),
            post.get("author"),
            post.get("body"),
            post.get("url"),
            post.get("ups"),
            post.get("created_on"),
            post.get("subreddit"),

        )
        cursor.execute(sql, values)
        conn.commit()
    
    else:
        print(f"Comment already exists in DB: {post.get('id')}")

    cursor.close()
    conn.close()


def getAllUsers():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM users"
    cursor.execute(sql)
    users = cursor.fetchall()

    cursor.close()
    conn.close()
    return users

def getAllPosts():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM posts"
    cursor.execute(sql)
    posts = cursor.fetchall()

    cursor.close()
    conn.close()
    return posts

def getUsersPosts(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM posts WHERE author = %s"
    cursor.execute(sql, (username,))
    projects = cursor.fetchall()

    cursor.close()
    conn.close()
    return projects

def getUsersComments(username):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    sql = "SELECT * FROM comments WHERE author = %s"
    cursor.execute(sql, (username,))
    comments = cursor.fetchall()

    cursor.close()
    conn.close()
    return comments