import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin


class User(SqlAlchemyBase, UserMixin, SerializerMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    username = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    nickname = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    telegram = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    xp = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    inventory = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    hands = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    body = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    legs = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    head = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    used_promocodes = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    icon_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guild_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("guilds.id"))
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    guilds = orm.relationship('Guild')
    user = orm.relationship("Users", back_populates='user')

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)
