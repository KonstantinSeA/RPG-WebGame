import sqlalchemy
import datetime
from sqlalchemy import orm
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin


class Guild(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'guilds'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    guild_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guildmaster_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    guild_members_id = sqlalchemy.Column(sqlalchemy.String, nullable=True)
