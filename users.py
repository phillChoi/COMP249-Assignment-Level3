'''
Created on Mar 26, 2012

@author: steve
'''

import bottle, uuid

# this variable MUST be used as the name for the cookie used by this application
COOKIE_NAME = 'sessionid'

def check_login(db, usernick, password):
    """returns True if password matches stored"""
    cur = db.cursor()
    sql = "SELECT nick,password FROM users"
    cur.execute(sql)
    p = db.crypt(password)
    for row in cur:
        if row[0] == usernick:
            if row[1] == db.crypt(password):
                return True
            else:
                return False

def generate_session(db, usernick):
    """create a new session and add a cookie to the response object (bottle.response)
    user must be a valid user in the database, if not, return None
    There should only be one session per user at any time, if there
    is already a session active, use the existing sessionid in the cookie
    """
    cur = db.cursor()
    cur.execute("SELECT nick FROM users WHERE nick = ?", (usernick,))
    user = cur.fetchone()
    if user is None:
        return None
    else:
        key = str(uuid.uuid4())
        cur.execute("SELECT sessionid FROM sessions WHERE usernick = ?", (usernick,))
        result = cur.fetchone()
        if result == None:
            cur.execute("INSERT INTO sessions VALUES (?,?)", (key, usernick))
            db.commit()
            bottle.response.set_cookie(COOKIE_NAME, key)
        else:
            bottle.response.set_cookie(COOKIE_NAME, result[0])


def delete_session(db, usernick):
    """remove all session table entries for this user"""
    cur = db.cursor()
    cur.execute("DELETE FROM sessions WHERE usernick = ?", (usernick,))
    db.commit()


def session_user(db):
    """try to
    retrieve the user from the sessions table
    return usernick or None if no valid session is present"""
    key = bottle.request.get_cookie(COOKIE_NAME)
    cur=db.cursor()
    row = cur.execute("SELECT usernick FROM sessions WHERE sessionid = ?",(key,)).fetchone()
    if row:
        return row[0]
    else:
        return None




