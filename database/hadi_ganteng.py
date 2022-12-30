# Credits by @hdiiofficial
from sqlalchemy import Column, BigInteger, Numeric
from database import BASE, SESSION


class Users(BASE):
    __tablename__ = "users"
    __table_args__ = {'extend_existing': True}
    user_id = Column(Numeric, primary_key=True)

    def __init__(self, user_id, channels=None):
        self.user_id = user_id
        self.channels = channels

Users.__table__.create(checkfirst=True)


async def num_users():
    try:
        return SESSION.query(Users).count()
    finally:
        SESSION.close()

async def broad_cast():
    try:
        return SESSION.query(Users.user_id).order_by(Users.user_id)
    finally:
        SESSION.close()
