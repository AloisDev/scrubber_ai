from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# from dependencies import Base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String(255), index=True)
    lastName = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password = Column(String(255))
