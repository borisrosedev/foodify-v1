from sqlalchemy import Integer, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from werkzeug.security import generate_password_hash, check_password_hash
from ...db import db
import enum

class UserRole(enum.Enum):
    user="user"
    premium="premium"
    admin="admin"


class User(db.Model):
    __tablename__="users"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    password_hash: Mapped[str]= mapped_column(String(200), nullable=False)
    firstname:Mapped[str]= mapped_column(String(50), nullable=False)
    lastname:Mapped[str]= mapped_column(String(50), nullable=False)
    photo_url:Mapped[str] = mapped_column(String(50), nullable=False)
    role:Mapped[UserRole]= mapped_column(Enum(UserRole), default=UserRole.user, nullable=False)

    def get_fullname(self):
        return f'{self.firstname.capitalize()} {self.lastname.capitalize()}'

    @property 
    def password(self):
        raise Exception('password is write-only')

    @password.setter
    def password(self, plain_password):
        self.password_hash = generate_password_hash(password=plain_password)

    def check_password(self, raw_password):
        return check_password_hash(self.password_hash, raw_password)

