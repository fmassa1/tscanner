from sql.mysql_connector import get_connection

def addUserToDB(post):
    conn = get_connection()
    cursor = conn.cursor()
    print(post)
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
              INSERT INTO posts (url, title, author, comments, ups)
              VALUES (%s, %s, %s, %s, %s)
              """
        values = (
            post.get("permalink"),
            post.get("title"),
            post.get("author"),
            post.get("num_comments"),
            post.get("ups"),
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
            INSERT INTO comments (post_id, parent_id, author, body, url, ups)
            VALUES (%s, %s, %s, %s, %s, %s)
            """
        values = (
            post.get("id"),
            post.get("parent_id"),
            post.get("author"),
            post.get("body"),
            post.get("url"),
            post.get("ups"),
        )
        cursor.execute(sql, values)
        conn.commit()
    
    else:
        print(f"Comment already exists in DB: {post.get('id')}")

    cursor.close()
    conn.close()