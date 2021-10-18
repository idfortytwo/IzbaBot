from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.models import Base


engine = create_engine('sqlite:///izbabot//db/db.sqlite', echo=False)
Session = sessionmaker(bind=engine)


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