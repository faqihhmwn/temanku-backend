import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


load_dotenv()


DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")

INSTANCE_CONNECTION_NAME = os.getenv("INSTANCE_CONNECTION_NAME")

print("===== DATABASE CONFIG DEBUG =====")
print("DB_USER:", DB_USER)
print("DB_NAME:", DB_NAME)
print("DB_HOST:", DB_HOST)
print("DB_PORT:", DB_PORT)
print("INSTANCE_CONNECTION_NAME:", INSTANCE_CONNECTION_NAME)
print("USING_CLOUD_SQL_SOCKET:", bool(INSTANCE_CONNECTION_NAME))
print("=================================")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


if INSTANCE_CONNECTION_NAME:
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@/{DB_NAME}"
        f"?unix_socket=/cloudsql/{INSTANCE_CONNECTION_NAME}"
    )
else:
    DATABASE_URL = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )


engine = create_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()