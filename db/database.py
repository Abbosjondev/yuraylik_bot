from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from core.config import DATABASE_ECHO, DATABASE_URL

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found!")

engine = create_async_engine(DATABASE_URL, echo=DATABASE_ECHO)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)