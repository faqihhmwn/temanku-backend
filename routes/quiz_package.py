from fastapi import APIRouter, Depends, Form
from sqlalchemy.orm import Session
import datetime

from config import get_db
from oauth2 import get_current_admin

from tables.quiz_package import QuizPackage
from tables.quiz import QuizQuestion
from tables.users import Users

from utils.storage import delete_image

router = APIRouter(
    prefix="/quiz",
    tags=["Quiz Package"]
)


def quiz_package_response(package: QuizPackage):
    return {
        "id": package.id,
        "title": package.title,
        "description": package.description,
        "difficulty": package.difficulty,
        "created_at": package.created_at,
        "updated_at": package.updated_at
    }


@router.post("/packages")
def create_quiz_package(
    title: str = Form(...),
    description: str | None = Form(None),
    difficulty: str = Form(...),

    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    if difficulty not in ["easy", "medium", "hard"]:
        return {
            "success": False,
            "message": "Difficulty harus easy, medium, atau hard"
        }

    package = QuizPackage(
        title=title,
        description=description,
        difficulty=difficulty
    )

    db.add(package)
    db.commit()
    db.refresh(package)

    return {
        "success": True,
        "message": "Quiz package berhasil dibuat",
        "data": quiz_package_response(package)
    }


@router.get("/packages")
def get_quiz_packages(
    db: Session = Depends(get_db),
    current_admin: Users = Depends(get_current_admin)
):

    packages = db.query(QuizPackage).all()

    return {
        "success": True,
        "data": [
            quiz_package_response(package)
            for package in packages
        ]
    }


@router.put("/packages/{package_id}")
def update_quiz_package(
    package_id: int,

    title: str = Form(...),
    description: str | None = Form(None),
    difficulty: str = Form(...),

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

    if difficulty not in ["easy", "medium", "hard"]:
        return {
            "success": False,
            "message": "Difficulty harus easy, medium, atau hard"
        }

    package.title = title
    package.description = description
    package.difficulty = difficulty
    package.updated_at = datetime.datetime.now()

    db.commit()
    db.refresh(package)

    return {
        "success": True,
        "message": "Quiz package berhasil diperbarui",
        "data": quiz_package_response(package)
    }


@router.delete("/packages/{package_id}")
def delete_quiz_package(
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

    for question in questions:

        if question.image_url:
            try:
                delete_image(question.image_url)
            except Exception:
                pass

    db.delete(package)
    db.commit()

    return {
        "success": True,
        "message": "Quiz package berhasil dihapus"
    }


@router.get("/public")
def get_public_quiz_packages(
    db: Session = Depends(get_db)
):

    packages = db.query(QuizPackage).all()

    result = []

    for package in packages:

        total_questions = db.query(
            QuizQuestion
        ).filter(
            QuizQuestion.package_id == package.id
        ).count()

        result.append({
            "id": package.id,
            "title": package.title,
            "description": package.description,
            "difficulty": package.difficulty,
            "total_questions": total_questions
        })

    return {
        "success": True,
        "data": result
    }


@router.get("/public/{package_id}")
def get_public_quiz_package_detail(
    package_id: int,
    db: Session = Depends(get_db)
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
        "data": {
            "id": package.id,
            "title": package.title,
            "description": package.description,
            "difficulty": package.difficulty,
            "questions": [
                {
                    "id": q.id,
                    "question_text": q.question_text,
                    "image_url": q.image_url,
                    "options": [
                        q.option_a,
                        q.option_b,
                        q.option_c,
                        q.option_d
                    ]
                }
                for q in questions
            ]
        }
    }