from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

from sqlalchemy import String, func, literal_column
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from db.models import Activity, User


async def add_or_update_user(
    session: AsyncSession, telegram_id: int, full_name: str, username: str | None
):
    stmt = insert(User).values(
        telegram_id=telegram_id, full_name=full_name, username=username
    )
    do_update_stmt = stmt.on_conflict_do_update(
        index_elements=["telegram_id"],
        set_={"username": stmt.excluded.username, "full_name": stmt.excluded.full_name},
    )
    await session.execute(do_update_stmt)
    await session.commit()


async def add_or_update_activity(session: AsyncSession, telegram_id: int, minutes: int):
    stmt = insert(Activity).values(
        telegram_id=telegram_id,
        record_date=datetime.now(tz=timezone.utc) + timedelta(hours=5),
        duration_minutes=minutes,
    )

    do_update_stmt = stmt.on_conflict_do_update(
        constraint="uq_user_record_date",
        set_={
            Activity.duration_minutes: Activity.duration_minutes
            + stmt.excluded.duration_minutes
        },
    )

    returning_stmt = do_update_stmt.returning(
        Activity.duration_minutes,
        literal_column("xmax = 0").label("is_inserted"),
    )

    res = (await session.execute(returning_stmt)).fetchone()
    await session.commit()

    if res is None:
        raise RuntimeError("Activity yozib bo'lmadi.")

    return {"is_updated": not res.is_inserted, "duration_minutes": res.duration_minutes}
