from sqlalchemy import Column, Integer, BigInteger, String, ForeignKey
from sqlalchemy.orm import declarative_base

from utils import get_beer_word


Base = declarative_base()


class Member(Base):
    __tablename__ = 'members'

    def __init__(self, member_id, name):
        self.member_id = member_id
        self.name = name

    member_id = Column(BigInteger, primary_key=True)
    name = Column(String, nullable=False)

    def __repr__(self):
        return f'Member(member_id={self.member_id}, name={self.name})'


class OwedBeer(Base):
    __tablename__ = 'owed_beers'

    def __init__(self, beer_from_id, beer_to_id, count):
        self.beer_from_id = int(beer_from_id)
        self.beer_to_id = int(beer_to_id)
        self.count = count

    beer_from_id = Column(BigInteger, ForeignKey('members.member_id'), primary_key=True)
    beer_to_id = Column(BigInteger, ForeignKey('members.member_id'), primary_key=True)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.beer_from_id} stoi {self.beer_to_id} {self.count} {get_beer_word(self.count)}'

    def __repr__(self):
        return f'OwedBeer(beer_from_id={self.beer_from_id}, beer_to_id={self.beer_to_id}, count={self.count})'