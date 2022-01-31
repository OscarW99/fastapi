# every model represents a table in our database
# Here we can create new tables

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, Time
from sqlalchemy.orm import relationship
from .database import Base


# This class is an extension of Base from sqlalchemy
class Post(Base):
    __tablename__ = "posts"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # cascade means when a parent object is deleted (eg user), all the children of that object are deleted (eg posts of that user)
    owner = relationship("User") # I assume this relationship function requires there to be a foreign key linked to the users table


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))




class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)



# if we add new columns to our tables here, it will not automatically update the pgadmin tables. To update tables with new columns, you must first delete the table in pgadmin.
# ... this can be solved with a database migration tool such as alembic (will cover later). 