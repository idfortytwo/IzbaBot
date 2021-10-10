from sqlalchemy import Column, Integer
from sqlalchemy.orm import declarative_base

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
        if self.count == 1:
            beer_word = 'piwo'
        elif self.count in [2, 3, 4]:
            beer_word = 'piwa'
        else:
            beer_word = 'piw'

        return f'{self.beer_from_id} stoi {self.beer_to_id} {self.count} {beer_word}'

    def __repr__(self):
        return f'OwnedBeer(beer_from_id={self.beer_from_id}, beer_to_id={self.beer_to_id}, count={self.count})'