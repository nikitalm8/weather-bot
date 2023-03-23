import logging

from app.database.models import Base

from sqlalchemy.orm import sessionmaker  
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession


class Database:

    def __init__(self, database_url: str, debug: bool=False):

        logger = logging.getLogger('database.engine')
        
        if 'sqlite' in database_url:

            logger.warning(
                "Using SQLite database in production is not recommended"
            )

        self.engine = create_async_engine(
            database_url, future=True, pool_pre_ping=True
        )
        self.sessionmaker = sessionmaker(
            self.engine, expire_on_commit=False, class_=AsyncSession
        )
        self.debug = debug

    async def create_tables(self):

        async with self.engine.begin() as conn:

            if self.debug:

                await conn.run_sync(Base.metadata.drop_all)
                
            await conn.run_sync(Base.metadata.create_all)

    @classmethod
    async def init(cls, database_url: str, debug: bool=False) -> "Database":

        instance = cls(database_url, debug)
        await instance.create_tables()

        return instance


async def create_sessionmaker(database_url: str, debug: bool=False) -> sessionmaker:

    database = await Database.init(database_url, debug)

    return database.sessionmaker
