from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_mail import Mail, Message
from models import User, db
from app import app, login_manager
from authlib.integrations.flask_client import OAuth
from itsdangerous import URLSafeTimedSerializer as Serializer
from itsdangerous import SignatureExpired, BadSignature


oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=app.config['GOOGLE_CLIENT_ID'],
    client_secret=app.config['GOOGLE_CLIENT_SECRET'],
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
    client_kwargs={
        'scope': 'openid email profile'
    }
)

mail = Mail(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='scrypt')
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please login.')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Login successful!')
            return redirect(url_for('profile'))
        flash('Login failed. Check your email and/or password.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html', user=current_user)

@app.route('/login/google')
def login_google():
    redirect_uri = url_for('authorized_google', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/login/google/authorized')
def authorized_google():
    token = google.authorize_access_token()
    user_info = token['userinfo']
    user = User.query.filter_by(email=user_info['email']).first()
    print(user)
    users = User.query.all()
    print(users)
    if not user:
        user = User(username=user_info['name'], email=user_info['email'], password='')
        db.session.add(user)
        db.session.commit()

    login_user(user)
    return redirect(url_for('profile'))


@app.route('/restore_password', methods=['GET', 'POST'])
def restore_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = generate_password_reset_token(user.email)
            send_password_reset_email(user.email, token)
            flash('Check your email for instructions to reset your password.')
        else:
            flash('Email not found.')
    return render_template('restore_password.html')

def generate_password_reset_token(email, expiration=3600):
    s = Serializer(app.config['SECRET_KEY'])
    return s.dumps({'reset_password': email})

def send_password_reset_email(to, token):
    msg = Message('Password Reset Request', sender='noreply@example.com', recipients=[to])
    msg.body = f"Your password reset link: {url_for('reset_password', token=token, _external=True)}"
    mail.send(msg)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        email = s.loads(token, max_age=3600)['reset_password']
    except SignatureExpired:
        flash('The link is expired.')
        return redirect(url_for('restore_password'))
    except BadSignature:
        flash('The link is invalid.')
        return redirect(url_for('restore_password'))

    if request.method == 'POST':
        password = request.form['password']
        hashed_password = generate_password_hash(password, method='sha256')
        user = User.query.filter_by(email=email).first()
        if user:
            user.password = hashed_password
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('login'))

    return render_template('reset_password.html')