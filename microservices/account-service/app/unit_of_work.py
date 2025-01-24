from contextlib import asynccontextmanager

from app.database import DatabaseConnectionPool

class UnitOfWork:
    def __init__(self, session_factory):
        self._session_factory = session_factory
        self._session = None

    @asynccontextmanager
    async def start(self, do_commit=True):
        self._session = self._session_factory()
        async with self._session.begin():
            try:
                yield self
                if do_commit:
                    await self._session.commit()
            except Exception as e:
                await self._session.rollback()
                raise e

    @property
    def session(self):
        return self._session


db_connection = DatabaseConnectionPool()
uow = UnitOfWork(db_connection.get_session_factory())
