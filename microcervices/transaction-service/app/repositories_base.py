from sqlalchemy import select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

class BaseRepository:
	_model = None

	@classmethod
	async def find_all(cls, session: AsyncSession,  **filter_by):
		query = select(cls._model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalars().all()

	@classmethod
	async def get_by(cls, session: AsyncSession, **filter_by):
		query = select(cls._model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalars().first()

	@classmethod
	async def count(cls, session: AsyncSession, **filter_by):
		query = select(func.count()).select_from(cls._model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalar()

	@classmethod
	async def exists(cls, session: AsyncSession, **filter_by):
		query = select(func.count()).select_from(cls._model).filter_by(**filter_by)
		result = await session.execute(query)
		return result.scalar() > 0

	@classmethod
	async def insert(cls, session: AsyncSession, obj: _model):
		session.add(obj)
		await session.flush()

	@classmethod
	async def update(cls, session: AsyncSession, obj: _model):
		await session.merge(obj)
		await session.flush()

	@classmethod
	async def delete_object(cls, session: AsyncSession, obj: _model):
		await session.delete(obj)
		await session.flush()

	@classmethod
	async def delete_by(cls, session: AsyncSession, **filter_by):
		query = delete(cls._model).where(
			*[getattr(cls._model, key) == value for key, value in filter_by.items()]
		)
		await session.execute(query)
		await session.flush()
