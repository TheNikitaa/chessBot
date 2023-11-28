from aiogram import types

def start_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="/settings"),
            types.KeyboardButton(text="/game"),
            types.KeyboardButton(text="Об авторе")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def settings_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="/settings Easy"),
            types.KeyboardButton(text="/settings Medium"),
            types.KeyboardButton(text="/settings Hard")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard

def game_kb() -> types.ReplyKeyboardMarkup:
    kb = [
        [
            types.KeyboardButton(text="/game White"),
            types.KeyboardButton(text="/game Black")
        ]
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    return keyboard
