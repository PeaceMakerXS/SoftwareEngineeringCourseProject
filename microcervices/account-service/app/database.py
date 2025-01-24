from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, declared_attr

from .settings import get_db_url

DATABASE_URL = get_db_url()

class DatabaseConnectionPool:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_pool()
        return cls._instance

    def _initialize_pool(self):
        print('Initializing database connection pool...')
        self._engine = create_async_engine(DATABASE_URL)
        self._session_factory = async_sessionmaker(self._engine, expire_on_commit=False)

    def get_session_factory(self):
        return self._session_factory

class Base(AsyncAttrs, DeclarativeBase):
    __abstract__ = True

    @classmethod
    @declared_attr.directive
    def __tablename__(cls) -> str:
        return f'{cls.__name__.lower()}'
