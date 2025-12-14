from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.exceptions import TelegramBadRequest

from app.database.requests import get_or_create_user
import app.keyboards as kb

user = Router()

WELCOME_TEXT = (
    "Добро пожаловать в бота для дизайнеров и креаторов\n\n"
    "Открой доступ к инструментам, которые ускоряют работу и вдохновляют:\n\n"
    "🔒 Закрытый канал с полезными материалами\n"
    "🎨 Midjourney, Nano Banana Pro, Stable\n"
    "📦 Премиум-ресурсы Freepik и Envato\n\n"
    "Всё, что нужно для креатива — в одном боте."
)

MAIN_MENU_TEXT = "Главное меню"
AI_MENU_TEXT = "Выберите модель ИИ:"


async def safe_edit_message(
    callback: CallbackQuery,
    text: str,
    reply_markup=None
):
    try:
        await callback.message.edit_text(text, reply_markup=reply_markup)
    except TelegramBadRequest:
        await callback.message.answer(text, reply_markup=reply_markup)


@user.message(CommandStart())
async def cmd_start(message: Message):
    await get_or_create_user(
        tg_id=message.from_user.id,
        username=message.from_user.username,
    )
    
    await message.answer(WELCOME_TEXT, reply_markup=kb.start_menu_kb())


@user.callback_query(F.data == "main_menu")
async def main_menu_handler(callback: CallbackQuery):
    await callback.answer()
    await safe_edit_message(
        callback,
        MAIN_MENU_TEXT,
        reply_markup=kb.main_menu_kb()
    )


@user.callback_query(F.data == "profile")
async def profile_handler(callback: CallbackQuery):
    await callback.answer()
    
    user = await get_or_create_user(
        tg_id=callback.from_user.id,
        username=callback.from_user.username,
    )

    text = (
        f"Статус: {user.status}\n"
        f"Истекает: {user.expires_at or '—'}\n"
    )
    
    await safe_edit_message(
        callback,
        text,
        reply_markup=kb.profile_kb()
    )


@user.callback_query(F.data == "profile:extend")
async def profile_extend(callback: CallbackQuery):
    await callback.answer()
    
    text = (
        "💳 Продление подписки\n\n"
    )
    
    await safe_edit_message(
        callback,
        text,
        reply_markup=kb.back_to_profile_kb()
    )


@user.callback_query(F.data == "ai")
async def ai_menu(callback: CallbackQuery):
    await callback.answer()
    await safe_edit_message(
        callback,
        AI_MENU_TEXT,
        reply_markup=kb.ai_choices_kb()
    )


@user.callback_query(F.data.startswith("ai:"))
async def ai_choice_handler(callback: CallbackQuery):
    model = callback.data.split(":", 1)[1]
    await callback.answer()
    
    model_names = {
        "midjourney": "Midjourney",
        "nano_banana": "Nano Banana Pro",
        "stable": "Stable Diffusion"
    }
    
    model_name = model_names.get(model, model)
    
    text = (
        f"🎨 {model_name}\n\n"
        f"Отправьте текстовый промпт для генерации изображения."
    )
    
    await safe_edit_message(
        callback,
        text,
        reply_markup=kb.back_to_ai_menu_kb()
    )


@user.callback_query(F.data == "resources")
async def resources_handler(callback: CallbackQuery):
    await callback.answer()
    
    text = (
        "Отправьте ссылку на нужный ресурс."
    )
    
    await safe_edit_message(
        callback,
        text,
        reply_markup=kb.back_to_main_kb()
    )


@user.callback_query(F.data == "channel")
async def channel_handler(callback: CallbackQuery):
    await callback.answer()
    
    text = (
        "🔒 Закрытый канал\n\n"
    )
    
    await safe_edit_message(
        callback,
        text,
        reply_markup=kb.back_to_main_kb()
    )


@user.callback_query(F.data == "back:main")
async def back_to_main(callback: CallbackQuery):
    await main_menu_handler(callback)


@user.callback_query(F.data == "back:profile")
async def back_to_profile(callback: CallbackQuery):
    await profile_handler(callback)


@user.callback_query(F.data == "back:ai")
async def back_to_ai(callback: CallbackQuery):
    await ai_menu(callback)