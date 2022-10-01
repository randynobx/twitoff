"""Flask app"""
import os
from flask import Flask, redirect, render_template, request
from twitoff.predict import predict_user

from twitoff.twitter import add_or_update_user
from .models import DB, User


def create_app():
    
    # Initialize app
    app = Flask(__name__)
    
    database_uri = os.getenv('DATABASE_URI')

    # Database configuration
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri

    DB.init_app(app)

    app_title = "Twitoff"
    
    @app.route('/')
    def index():
        users = User.query.all()
        return render_template('base.html', title='Home', users=users)

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
        """

    @app.route('/user/<username>')
    def show_user(username=None):
        db_user = User.query.filter_by(username=username).first_or_404()
        return render_template('user.html',
                               title=db_user.username,
                               message='',
                               tweets=db_user.tweets
                               )

    @app.route('/user', methods=['POST'])
    def add_user():
        username = request.values['user_name']
        add_or_update_user(username)
        return redirect(f'/user/{username}')

    @app.route('/compare', methods=['POST'])
    def compare():
        username0 = request.values['user0']
        username1 = request.values['user1']
        hypo_tweet_text = request.values['tweet_text']
        
        if username0 == username1:
            message = 'Cannot compare users to themselves!'
        else:
            prediction = predict_user(username0,
                                      username1,
                                      hypo_tweet_text)
            if prediction:
                predicted_user = username1
            else:
                predicted_user = username0
            message = f'This tweet was more likely written by {predicted_user}'
        
        return render_template('predict.html',
                               title='Prediction',
                               message=message
                               )

    return app
