import logging

from app.database.models import Base

from sqlalchemy.ext.asyncio import (
    AsyncSession, 
    AsyncEngine, 
    create_async_engine, 
    async_sessionmaker,
)


log = logging.getLogger('database.engine')

async def create_tables(engine: AsyncEngine, debug: bool=False) -> None:

    async with engine.begin() as conn:

        if debug:

            await conn.run_sync(Base.metadata.drop_all)
            
        await conn.run_sync(Base.metadata.create_all)


async def create_sessionmaker(database_url: str, debug: bool=False) -> async_sessionmaker:
    """
    Create an async sessionmaker for the database and create tables if they don't exist.

    :param str database_url: SQLAlchemy database URL
    :param bool debug: Debug mode, defaults to False
    :return async_sessionmaker: Async sessionmaker (sessionmaker with AsyncSession class)
    """

    if 'sqlite' in database_url:

        log.warning(
            "Using SQLite database in production is not recommended"
        )

    engine = create_async_engine(
        database_url, future=True,
    )
    await create_tables(engine, debug)

    return async_sessionmaker(engine, expire_on_commit=False)
