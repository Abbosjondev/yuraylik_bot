from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Assalomu alaykum, botga xush kelibsiz.')