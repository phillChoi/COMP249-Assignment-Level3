"""
Created on Feb 20, 2015

@author: steve cassidy
"""

import re


def post_to_html(content):
    """Convert a post to safe HTML, quote any HTML code, convert
    URLs to live links and spot any @mentions or #tags and turn
    them into links.  Return the HTML string"""

    # replace key HTML special characters with entities
    content = content.replace('&', '&amp;')
    content = content.replace('<', '&lt;')
    content = content.replace('>', '&gt;')

    # regular expression to replace links with anchor tags
    linkpat = r"(https?\://[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,3}(/\S*)?)"
    repl =    r"<a href='\1'>\1</a>"
    (content, n) = re.subn(linkpat, repl, content)

    # re to make links from @mentions
    mentionpat = r"@([a-zA-Z0-9.]+[a-zA-Z0-9]+)"
    repl =       r"<a href='/users/\1'>@\1</a>"
    (content, n) = re.subn(mentionpat, repl, content)

    # re to wrap hashtags with a strong tag
    hashpat = r"(#[a-zA-Z0-9]+)"
    repl    = r"<strong class='hashtag'>\1</strong>"
    (content, n) = re.subn(hashpat, repl, content)

    return content


def post_list(db, usernick=None, limit=50):
    """Return a list of posts ordered by date
    db is a database connection (as returned by COMP249Db())
    if usernick is not None, return only posts by this user
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """

    cursor = db.cursor()

    if usernick is not None:
        sql = """SELECT id, timestamp, usernick, avatar, content
        FROM posts, users
        WHERE posts.usernick=users.nick AND usernick=?
        ORDER BY timestamp DESC
        LIMIT ?"""

        cursor.execute(sql, [usernick, limit])
    else:
        sql = """SELECT id, timestamp, usernick, avatar, content
        FROM posts, users
        WHERE posts.usernick=users.nick
        ORDER BY timestamp DESC
        LIMIT ?"""

        cursor.execute(sql, [limit])

    return cursor.fetchall()


def post_list_followed(db, usernick, limit=50):
    """Return a list of posts by user usernick and any users
    followed by them, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """

    cursor = db.cursor()

    sql = """SELECT DISTINCT id, timestamp, usernick, avatar, content
        FROM posts
        INNER JOIN (
           users INNER JOIN follows ON users.nick = follows.followed
        )
        ON posts.usernick = nick
        WHERE follower = ?
        ORDER BY timestamp DESC
        LIMIT ?"""

    cursor.execute(sql, [usernick, limit])

    return cursor.fetchall()


def post_list_mentions(db, usernick, limit=50):
    """Return a list of posts that mention usernick, ordered by date
    db is a database connection (as returned by COMP249Db())
    return at most limit posts (default 50)

    Returns a list of tuples (id, timestamp, usernick, avatar,  content)
    """

    cursor = db.cursor()

    sql = """SELECT DISTINCT id, timestamp, usernick, avatar, content
        FROM posts, users
        WHERE posts.usernick=users.nick AND content LIKE ?
        ORDER BY timestamp DESC
        LIMIT ?"""

    cursor.execute(sql, ['%@' + usernick + '%', limit])

    return cursor.fetchall()


def post_add(db, usernick, message):
    """Add a new post to the database.
    The date of the post will be the current time and date.

    Return a the id of the newly created post or None if there was a problem"""

    # reject long messages
    if len(message) > 150:
        return None

    cursor = db.cursor()

    sql = "INSERT INTO posts (usernick, content) VALUES (?, ?)"

    cursor.execute(sql, (usernick, message))

    db.commit()

    # get the inserted post via the lastrowid
    return cursor.lastrowid
