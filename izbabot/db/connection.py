import os

from dotenv import load_dotenv
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base


load_dotenv()
conn_url = os.environ.get('conn_url')
engine = create_engine(conn_url, echo=False)
Session = sessionmaker(bind=engine)


def create_schema():
    Base.metadata.create_all(engine)


@contextmanager
def session_scope():
    """Provide a transactional scope around a series of operations."""
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


if __name__ == '__main__':
    engine = create_engine('sqlite:///db.sqlite', echo=False)
    Base.metadata.create_all(engine)