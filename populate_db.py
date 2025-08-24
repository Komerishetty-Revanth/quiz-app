from app import app, db
from models import Quiz, Question, Answer

with app.app_context():
    db.create_all()
    # Create quiz
    quiz = Quiz(title="General Knowledge")
    db.session.add(quiz)
    db.session.commit()

    # Add questions
    q1 = Question(text="What is the capital of France?", quiz=quiz)
    q2 = Question(text="Which planet is known as the Red Planet?", quiz=quiz)
    db.session.add_all([q1, q2])
    db.session.commit()

    # Add answers
    a1 = Answer(text="Paris", is_correct=True, question=q1)
    a2 = Answer(text="London", is_correct=False, question=q1)
    a3 = Answer(text="Mars", is_correct=True, question=q2)
    a4 = Answer(text="Jupiter", is_correct=False, question=q2)
    db.session.add_all([a1, a2, a3, a4])
    db.session.commit()
    print("Sample quiz data added!")
