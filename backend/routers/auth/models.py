from sqlmodel import SQLModel, Field, Column
import uuid
from datetime import datetime
import sqlalchemy.dialects.postgresql as pg
class User(SQLModel, table=True):
    __tablename__ = "User"

    uid: uuid.UUID = Field(sa_column=Column(
        default = uuid.uuid4,
        nullable= False,
        primary_key= True,
        unique= True
    ))
    email: str
    username: str
    hash_pwd : str = Field(exclude=True)
    is_verified : str = Field(default=False)
    created_on: datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
            nullable=False
        )
        )
    updated_on : datetime = Field(
        sa_column=Column(
            pg.TIMESTAMP,
            default=datetime.now,
            onupdate= datetime.now,
            nullable=False
        )
        )