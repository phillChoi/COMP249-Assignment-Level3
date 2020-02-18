__author__ = 'Steve Cassidy'

from bottle import Bottle, template, static_file, debug, redirect, request
import interface, users
from database import COMP249Db

COOKIE_NAME = 'sessionid'

application = Bottle()
# turn on debugging for bottle during testing
debug()

@application.route('/')
def index():
    """Generate the main page of the app 
    with a list of the most recent posts"""

    db = COMP249Db()
    session_user = users.session_user(db)
    info = {
        'title': "¡Welcome to Psst!",
        'posts': interface.post_list(db)
    }

    return template('index', info, session_user=session_user)


@application.route('/mentions/<who>')
def mentions(who):
    """Generate a page that lists the mentions of a 
    given user"""
    db = COMP249Db()

    info = dict()
    info['title'] = "Mentions of " + who

    info['posts'] = interface.post_list_mentions(db, usernick=who)

    # re-use the index template since this is just a list of posts
    return template('index', info)


@application.route('/users/<who>')
def userpage(who):
    """Generate a page with just the posts for a given user"""

    db = COMP249Db()

    info = {
        'title': "User page for " + who,
        'posts': interface.post_list(db, usernick=who),
    }

    # re-use the index template since this is just a list of posts
    return template("index", info)


@application.route('/about')
def about():
    """Generate the about page"""

    return template('about', title="About updatio.")


@application.route('/static/<filename:path>')
def static(filename):
    """Serve static files from the static folder"""

    return static_file(filename=filename, root='static')

@application.route('/login', method='POST')
def loginform():
    """"""
    db = COMP249Db()
    nick = request.forms.get('nick')
    password = request.forms.get('password')
    session_user = users.session_user(db)
    if users.check_login(db, nick, password) == True:
        users.generate_session(db, nick)
        return redirect('/', code=302)
    else:
        info = {
            'title': "Failed Login"
        }

        return template('failed',info,session_user=session_user)

@application.route('/logout', method='POST')
def logout():
    db = COMP249Db()
    usernick = users.session_user(db)
    users.delete_session(db,usernick)
    return redirect('/', code=302)


@application.route('/post', method='POST')
def post():
    db = COMP249Db()
    usernick = users.session_user(db)
    message = request.forms.get('post')
    interface.post_add(db, usernick, message)
    return redirect('/')

if __name__ == '__main__':
    application.run(debug=True, port=8010)
