from sqlalchemy import select
from app.database.models import async_session, User


async def get_or_create_user(
    tg_id: int,
    username: str | None = None,
) -> User:
    async with async_session() as session:
        user = await session.scalar(
            select(User).where(User.telegram_id == tg_id)
        )

        if user:
            return user

        user = User(
            telegram_id=tg_id,
            username=username,
        )
        session.add(user)
        await session.commit()
        return user
