# main.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from datetime import datetime
from data import data

BOT_TOKEN = "8042590087:AAHIDTXBOSgF8p6tJbQ478Ux0NRWXZyBF7E"
GROUP_ID = -1002408634590
START_HOUR = 7
END_HOUR = 22

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

def is_time_allowed():
    hour = datetime.now().hour
    return START_HOUR <= hour < END_HOUR

async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(GROUP_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(CommandStart())
async def start(message: types.Message):
    if not is_time_allowed():
        return await message.answer("🕒 Bot is available from 7 AM to 10 PM only.")

    if not await is_member(message.from_user.id):
        btn = InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔗 Join Group", url="https://t.me/agri_master_mind")
        ]])
        return await message.answer("🔒 Please join our group to access this bot.", reply_markup=btn)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📘 B.Sc. Agriculture", callback_data="B.Sc. Agriculture")],
        [InlineKeyboardButton(text="📗 RPSC AAO", callback_data="RPSC AAO")],
        [InlineKeyboardButton(text="📕 Agriculture Supervisor", callback_data="Agriculture Supervisor")],
        [InlineKeyboardButton(text="📖 Visit Blog", url="https://www.agrimastermind.in")]
    ])
    await message.answer("👋 Welcome to *Agri Master Mind Bot*!\nChoose an option:", reply_markup=keyboard)

@dp.callback_query()
async def callback(call: types.CallbackQuery):
    path = call.data.split(" → ")
    node = data
    for key in path:
        node = node.get(key, {})

    if isinstance(node, dict):
        btns = [[InlineKeyboardButton(text=k, callback_data=f"{call.data} → {k}")] for k in node]
        await call.message.edit_text(f"📂 *{path[-1]}*:", reply_markup=InlineKeyboardMarkup(inline_keyboard=btns))
    else:
        for title, links in node.items():
            await call.message.answer(
                f"*{title}*\n🔗 [View]({links['view']}) | ⬇️ [Download]({links['download']})"
            )

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
