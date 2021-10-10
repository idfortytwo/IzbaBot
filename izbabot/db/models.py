from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

from utils import get_beer_word


Base = declarative_base()


class OwnedBeer(Base):
    __tablename__ = 'owned_beers'

    def __init__(self, beer_from_id, beer_to_id, count):
        self.beer_from_id = int(beer_from_id)
        self.beer_to_id = int(beer_to_id)
        self.count = count

    beer_from_id = Column(Integer, primary_key=True)
    beer_to_id = Column(Integer, primary_key=True)
    count = Column(Integer, nullable=False)

    def __str__(self):
        return f'{self.beer_from_id} stoi {self.beer_to_id} {self.count} {get_beer_word(self.count)}'

    def __repr__(self):
        return f'OwnedBeer(beer_from_id={self.beer_from_id}, beer_to_id={self.beer_to_id}, count={self.count})'