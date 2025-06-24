from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql://todoapp_user:X67VRD9VeNixsc2uuNEZNLoprNkb6gao@dpg-d1d83kndiees73ckipg0-a/todoapp_zluj"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

# SQLALCHEMY_DATABASE_URL = \
#     'postgresql://postgres:admin123@localhost/todosapp'
#
# engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                           bind=engine)

Base = declarative_base()


