from flask import Flask, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash, check_password_hash
from forms import RegistrationForm, LoginForm
from config import Config
from extensions import db, login_manager
from models import User, Quiz, Question, Answer
from flask_login import login_user, logout_user, current_user, login_required

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    quizzes = Quiz.query.all()
    return render_template('index.html', quizzes=quizzes)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            flash('Login successful!', 'success')
            return redirect(url_for('index'))
        flash('Invalid email or password.', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/quiz/<int:quiz_id>', methods=['GET', 'POST'])
@login_required
def quiz(quiz_id):
    quiz = Quiz.query.get_or_404(quiz_id)
    questions = quiz.questions
    if request.method == 'POST':
        score = 0
        total = len(questions)
        for question in questions:
            selected = request.form.get(str(question.id))
            if selected:
                answer = Answer.query.filter_by(id=int(selected), question_id=question.id).first()
                if answer and answer.is_correct:
                    score += 1
        return render_template('result.html', score=score, total=total)
    return render_template('quiz.html', quiz=quiz, questions=questions)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
