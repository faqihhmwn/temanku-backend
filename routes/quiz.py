from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from config import get_db
import datetime
from oauth2 import get_current_user, get_current_admin
from tables.quiz import QuizQuestion
from models.quiz import CreateQuizQuestion, UpdateQuizQuestion
from tables.users import Users


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


def quiz_admin_response(question: QuizQuestion):
    return {
        "id": question.id,
        "question_text": question.question_text,
        "question_type": question.question_type,
        "category": question.category,
        "image_url": question.image_url,
        "option_a": question.option_a,
        "option_b": question.option_b,
        "option_c": question.option_c,
        "option_d": question.option_d,
        "answer": question.answer,
        "created_at": question.created_at,
        "updated_at": question.updated_at
    }


def public_quiz_response(question: QuizQuestion):
    return {
        "id": question.id,
        "question_text": question.question_text,
        "question_type": question.question_type,
        "category": question.category,
        "image_url": question.image_url,
        "options": [
            question.option_a,
            question.option_b,
            question.option_c,
            question.option_d
        ]
    }


@router.post("/questions")
def create_quiz_question(
    request: CreateQuizQuestion,
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    new_question = QuizQuestion(
        question_text=request.question_text,
        question_type=request.question_type,
        category=request.category,
        image_url=request.image_url,
        option_a=request.option_a,
        option_b=request.option_b,
        option_c=request.option_c,
        option_d=request.option_d,
        answer=request.answer
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "success": True,
        "message": "Quiz question created",
        "data": quiz_admin_response(new_question)
    }


@router.get("/questions")
def get_quiz_questions(
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    questions = db.query(QuizQuestion).all()

    return {
        "success": True,
        "data": [quiz_admin_response(q) for q in questions]
    }


# PUBLIC ENDPOINT UNTUK USER
# Taruh sebelum /questions/{question_id}
@router.get("/questions/public")
def get_public_quiz_questions(
    db: Session = Depends(get_db)
):

    questions = db.query(QuizQuestion).all()

    return {
        "success": True,
        "data": [public_quiz_response(q) for q in questions]
    }


@router.get("/questions/public/{question_id}")
def get_public_quiz_question_detail(
    question_id: int,
    db: Session = Depends(get_db)
):

    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == question_id
    ).first()

    if not question:
        return {
            "success": False,
            "message": "Quiz question not found"
        }

    return {
        "success": True,
        "data": public_quiz_response(question)
    }


@router.get("/questions/{question_id}")
def get_quiz_question_detail(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == question_id
    ).first()

    if not question:
        return {
            "success": False,
            "message": "Quiz question not found"
        }

    return {
        "success": True,
        "data": quiz_admin_response(question)
    }


@router.put("/questions/{question_id}")
def update_quiz_question(
    question_id: int,
    request: UpdateQuizQuestion,
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == question_id
    ).first()

    if not question:
        return {
            "success": False,
            "message": "Quiz question not found"
        }

    update_data = request.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(question, key, value)

    question.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(question)

    return {
        "success": True,
        "message": "Quiz question updated",
        "data": quiz_admin_response(question)
    }


@router.delete("/questions/{question_id}")
def delete_quiz_question(
    question_id: int,
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == question_id
    ).first()

    if not question:
        return {
            "success": False,
            "message": "Quiz question not found"
        }

    db.delete(question)
    db.commit()

    return {
        "success": True,
        "message": "Quiz question deleted"
    }