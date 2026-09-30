from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from db.models import User

async def add_or_update_user(session: AsyncSession, telegram_id: int, full_name: str, username: str | None):
    stmt = insert(User).values(
        telegram_id=telegram_id,
        full_name=full_name,
        username=username
    )
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=['telegram_id'],
        set_ = {
            "username": stmt.excluded.username,
            "full_name": stmt.excluded.full_name
        }
    )
    await session.execute(do_update_stmt)
    await session.commit()
    print("Done: Added")