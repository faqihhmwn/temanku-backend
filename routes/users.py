from fastapi import APIRouter, Depends
from models.users import ResponseSchema, tokenResponse, Register, Login
from sqlalchemy.orm import Session
from config import get_db
from passlib.context import CryptContext
from repository.users import UsersRepo, JWTRepo
from tables.users import Users

router = APIRouter(
    tags={"Authentication"}
)

pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")
# pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

# register
@router.post('/signup')
async def signup(request: Register, db: Session = Depends(get_db)):
    try:

        existing_username = UsersRepo.find_by_username(
            db,
            Users,
            request.username
        )

        if existing_username:
            return ResponseSchema(
                code="400",
                status="Bad Request",
                message="Username already exists"
            ).dict(exclude_none=True)

        existing_email = UsersRepo.find_by_email(
            db,
            Users,
            request.email
        )

        if existing_email:
            return ResponseSchema(
                code="400",
                status="Bad Request",
                message="Email already exists"
            ).dict(exclude_none=True)

        _user = Users(
            username=request.username,
            password=pwd_context.hash(request.password),
            email=request.email,
            phone_number=request.phone_number,
            first_name=request.first_name,
            last_name=request.last_name
        )

        UsersRepo.insert(db, _user)

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Register Success"
        ).dict(exclude_none=True)

    except Exception as error:
        print(error)

        return ResponseSchema(
            code="500",
            status="Error",
            message="Internal Server Error"
        ).dict(exclude_none=True)


# Login

@router.post('/login')
async def login(request: Login, db: Session = Depends(get_db)):
    try:

        _user = UsersRepo.find_by_username(
            db,
            Users,
            request.username
        )

        if not _user:
            return ResponseSchema(
                code="404",
                status="Not Found",
                message="Username not found"
            ).dict(exclude_none=True)

        if not pwd_context.verify(request.password, _user.password):
            return ResponseSchema(
                code="400",
                status="Bad Request",
                message="Invalid Password"
            ).dict(exclude_none=True)

        token = JWTRepo.generate_token({
            'user_id': _user.id
        })

        return ResponseSchema(
            code="200",
            status="Ok",
            message="Login Success",
            result=tokenResponse(
                access_token=token,
                token_type="bearer"
            ).dict(exclude_none=True)
        ).dict(exclude_none=True)

    except Exception as error:
        print(error)

        return ResponseSchema(
            code="500",
            status="Error",
            message="Internal Server Error"
        ).dict(exclude_none=True)