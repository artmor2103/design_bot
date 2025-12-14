from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder


def start_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Профиль", callback_data="profile")
    kb.button(text="Бесплатная 3-х дневная пробная версия", callback_data="trial")
    kb.button(text="Главное меню", callback_data="main_menu")
    kb.adjust(3)
    return kb.as_markup()


def main_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Профиль", callback_data="profile")
    kb.button(text="Скачать с freepik/envanto", callback_data="resources")
    kb.button(text="ИИ", callback_data="ai")
    kb.button(text="Канал", callback_data="channel")
    kb.adjust(3)
    return kb.as_markup()


def ai_choices_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Nano banana pro", callback_data="ai:nano_banana")
    kb.button(text="Midjourney", callback_data="ai:midjourney")
    kb.button(text="Stable", callback_data="ai:stable")
    kb.button(text="Главное меню", callback_data="back:main")
    kb.adjust(4)
    return kb.as_markup()


def profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Продлить подписку", callback_data="profile:extend")
    kb.button(text="Главное меню", callback_data="back:main")
    kb.adjust(2)
    return kb.as_markup()


def back_to_profile_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад в профиль", callback_data="back:profile")
    kb.button(text="Главное меню", callback_data="back:main")
    kb.adjust(2)
    return kb.as_markup()


def back_to_ai_menu_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Назад в ИИ", callback_data="back:ai")
    kb.button(text="Главное меню", callback_data="back:main")
    kb.adjust(2)
    return kb.as_markup()


def back_to_main_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardBuilder()
    kb.button(text="Главное меню", callback_data="back:main")
    return kb.as_markup()