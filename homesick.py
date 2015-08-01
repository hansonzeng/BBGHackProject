from flask import Flask, redirect, url_for, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '145224459145814',
        'secret': 'a7bfc0602ae655274952f7d33af7f8dc'
    },
    'twitter': {
        'id': '3RzWQclolxWZIMq5LJqzRZPTl',
        'secret': 'm9TEd58DSEtRrZHpz2EjrV9AhsBRxKMo8m3kuIZj3zLwzwIimt'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'api'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('loagout.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('indexi1'))


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('api'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous():
        return redirect(url_for('api'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('api'))

@app.route('/api')
def api():

    if current_user.is_authenticated():
        return render_template("page.html")
    else:
        return "bastard, you aren't logged int"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
