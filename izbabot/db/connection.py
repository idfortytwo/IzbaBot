import os

from typing import ContextManager
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Base


load_dotenv()
conn_url = os.environ.get('conn_url')
engine = create_async_engine(conn_url, echo=False)
Session = AsyncSession(bind=engine)


async def create_schema():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def session_scope() -> ContextManager[AsyncSession]:
    """Provide a transactional scope around a series of operations."""
    session = AsyncSession(bind=engine)
    try:
        yield session
        await session.commit()
    except:
        await session.rollback()
        raise
    finally:
        await session.close()
