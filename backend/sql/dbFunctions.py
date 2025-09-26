from mysql_connector import get_connection

def addUserToDB(post):
    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()

def addPostToDB(post):
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO post (url, title, author, comments, ups)
        VALUES (%s, %s, %s, %s, %s)
    """
    values = (
        post.get("permalink"),
        post.get("title"),
        post.get("author"),
        post.get("num_comments"),
        post.get("ups")
    )
    cursor.execute(sql, values)
    conn.commit()

    cursor.close()
    conn.close()

def addCommentToDB(post):
    conn = get_connection()
    cursor = conn.cursor()

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

    cursor.close()
    conn.close()