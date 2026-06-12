from sqlalchemy.orm import Session
from config import get_db
import datetime
from oauth2 import get_current_admin
from tables.quiz import QuizQuestion
from tables.quiz_package import QuizPackage
from tables.users import Users
from fastapi import APIRouter, Depends, UploadFile, File, Form
from utils.storage import upload_image, delete_image


router = APIRouter(
    prefix="/quiz",
    tags=["Quiz"]
)


def quiz_admin_response(question: QuizQuestion):
    return {
        "id": question.id,
        "question_text": question.question_text,
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
        "image_url": question.image_url,
        "options": [
            question.option_a,
            question.option_b,
            question.option_c,
            question.option_d
        ]
    }


@router.post("/packages/{package_id}/questions")
async def create_quiz_question(
    package_id: int,

    question_text: str = Form(...),
    answer: str = Form(...),

    option_a: str | None = Form(None),
    option_b: str | None = Form(None),
    option_c: str | None = Form(None),
    option_d: str | None = Form(None),

    file: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):
    
    package = db.query(QuizPackage).filter(
    QuizPackage.id == package_id
    ).first()

    if not package:
        return {
            "success": False,
            "message": "Quiz package tidak ditemukan"
        }
    
    image_url = None

    if file:

        if not file.content_type.startswith("image/"):
            return {
                "success": False,
                "message": "File harus berupa gambar"
            }

        image_url = upload_image(file)

    new_question = QuizQuestion(
        package_id=package_id,
        question_text=question_text,
        image_url=image_url,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        answer=answer
    )

    db.add(new_question)
    db.commit()
    db.refresh(new_question)

    return {
        "success": True,
        "message": "Soal quiz berhasil dibuat",
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


@router.get("/packages/{package_id}/questions")
def get_questions_by_package(
    package_id: int,
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    package = db.query(QuizPackage).filter(
        QuizPackage.id == package_id
    ).first()

    if not package:
        return {
            "success": False,
            "message": "Quiz package tidak ditemukan"
        }

    questions = db.query(QuizQuestion).filter(
        QuizQuestion.package_id == package_id
    ).all()

    return {
        "success": True,
        "data": [
            quiz_admin_response(q)
            for q in questions
        ]
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
            "message": "Soal quiz tidak ditemukan"
        }

    return {
        "success": True,
        "data": quiz_admin_response(question)
    }


@router.put("/questions/{question_id}")
async def update_quiz_question(
    question_id: int,

    question_text: str = Form(...),
    answer: str = Form(...),

    option_a: str | None = Form(None),
    option_b: str | None = Form(None),
    option_c: str | None = Form(None),
    option_d: str | None = Form(None),

    file: UploadFile | None = File(None),

    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    question = db.query(QuizQuestion).filter(
        QuizQuestion.id == question_id
    ).first()

    if not question:
        return {
            "success": False,
            "message": "Soal quiz tidak ditemukan"
        }

    question.question_text = question_text
    question.answer = answer

    question.option_a = option_a
    question.option_b = option_b
    question.option_c = option_c
    question.option_d = option_d

    if file:

        if not file.content_type.startswith("image/"):
            return {
                "success": False,
                "message": "File harus berupa gambar"
            }

        if question.image_url:
            try:
                delete_image(question.image_url)
            except Exception:
                pass

        question.image_url = upload_image(file)

    question.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(question)

    return {
        "success": True,
        "message": "Soal quiz diperbarui",
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
            "message": "Soal tidak ditemukan"
        }

    if question.image_url:
        try:
            delete_image(question.image_url)
        except Exception:
            pass

    db.delete(question)
    db.commit()

    return {
        "success": True,
        "message": "Soal berhasil dihapus"
    }
