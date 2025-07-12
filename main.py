# main.py

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from datetime import datetime
from data import data

BOT_TOKEN = "8042590087:AAHIDTXBOSgF8p6tJbQ478Ux0NRWXZyBF7E"
GROUP_ID = -1002408634590  # Your group ID
START_HOUR = 7
END_HOUR = 22

bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.MARKDOWN)
dp = Dispatcher()

def is_time_allowed():
    current_hour = datetime.now().hour
    return START_HOUR <= current_hour < END_HOUR

async def is_member(user_id: int) -> bool:
    try:
        member = await bot.get_chat_member(chat_id=GROUP_ID, user_id=user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

@dp.message(CommandStart())
async def start_handler(message: types.Message):
    if not is_time_allowed():
        return await message.answer("🕒 Bot is available from 7 AM to 10 PM only.")

    if not await is_member(message.from_user.id):
        join_btn = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🔗 Join Group", url="https://t.me/agri_master_mind")]]
        )
        return await message.answer("🚫 Please join our group to access the notes.", reply_markup=join_btn)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📘 B.Sc. Agriculture", callback_data="B.Sc. Agriculture")],
            [InlineKeyboardButton(text="📗 RPSC AAO", callback_data="RPSC AAO")],
            [InlineKeyboardButton(text="📕 Agriculture Supervisor", callback_data="Agriculture Supervisor")],
            [InlineKeyboardButton(text="📖 Agri Master Mind Blog", url="https://www.agrimastermind.in")]
        ]
    )
    await message.answer("👋 Welcome to Agri Master Mind Bot!\nChoose an option below:", reply_markup=kb)

@dp.callback_query()
async def handle_callback(call: types.CallbackQuery):
    path = call.data.split(" → ")
    node = data
    for key in path:
        node = node.get(key, {})

    if isinstance(node, dict):
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text=key, callback_data=f"{call.data} → {key}")]
                for key in node
            ]
        )
        await call.message.edit_text(f"📂 *{path[-1]}*:", reply_markup=kb)
    elif isinstance(node, str):
        await call.message.answer(node)
    else:
        await call.message.edit_text("📄 Available Notes:")
        for title, links in node.items():
            view = links.get("view", "#")
            download = links.get("download", "#")
            await call.message.answer(f"*{title}*\n🔗 [View]({view}) | ⬇️ [Download]({download})")

if __name__ == "__main__":
    asyncio.run(dp.start_polling(bot))
