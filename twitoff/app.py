"""Flask app"""

from flask import Flask, redirect, render_template

from twitoff.twitter import add_or_update_user
from .models import DB, User, Tweet

def create_app():
    
    # Initialize app
    app = Flask(__name__)

    # Database configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"

    DB.init_app(app)

    app_title = "Twitoff"
    
    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('index.html', title='Home', users = users)


    @app.route('/update')
    def update():
        users = User.query.all()
        for user in users:
            add_or_update_user(user.username)
        return redirect('/')


    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return """Reset Database!
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>
        <a href='/users'>Go to users</a>
        """

    @app.route('/populate')
    def populate():
        # user1 = User(id=1, username='joe_schmoe')
        # tweet1 = Tweet(id=1, text='yo this is a tweet', user=user1)
        # DB.session.add(user1)
        # DB.session.add(tweet1)
        # DB.session.commit()
        return """Created some users/tweets
        <a href='/'>Go to Home</a>
        <a href='/reset'>Go to reset</a>
        <a href='/populate'>Go to populate</a>
        <a href='/users'>Go to users</a>
        """

    @app.route('/users')
    def show_all_users():
        users = User.query.all()
        return render_template('users.html', title='Users', users=users)
    
    @app.route('/user/')
    def show_user():
        user = User.query.filter()
        return render_template('user.html'
                               , title=f'Twitoff | {user.username}'
                               , user=user
                               )
    
    return app
