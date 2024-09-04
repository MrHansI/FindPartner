from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from models import db, User
from config import Config
import os
from werkzeug.utils import secure_filename
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'

app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config.from_object(Config)
migrate = Migrate(app, db)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/')
@login_required
def home():
    return render_template('home.html', username=current_user.username)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid username or password.')

    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        middle_name = request.form.get('middle_name')
        display_name = request.form['display_name']
        password = request.form['password']
        relationship_status = request.form['relationship_status']
        partner_nick = request.form.get('partner_nick')
        profile_picture = request.files['profile_picture']

        if profile_picture:
            filename = os.path.join(app.config['UPLOAD_FOLDER'], profile_picture.filename)
            profile_picture.save(filename)
            picture_path = profile_picture.filename
        else:
            picture_path = None

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
 #           display_name=display_name,
            password=password,  # Здесь используется setter для хэширования пароля
            relationship_status=relationship_status,
            partner_nick=partner_nick,
            profile_picture=picture_path
        )

        db.session.add(new_user)
        db.session.commit()

        flash('Регистрация прошла успешно!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')



@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
