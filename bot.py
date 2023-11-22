import asyncio
import logging
import core.game 
from core.game import Chess
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command, CommandObject
from aiogram.utils.formatting import Text, Bold
from aiogram.enums import ParseMode
from config.cfg import load_config

logging.basicConfig(level=logging.INFO)
config = load_config()

bot_token = config.tg_bot.token
admin = config.tg_bot.admin_id

game = Chess()
bot = Bot(token=bot_token)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    context = Text(
        Bold(f"Добро пожаловать в шахматный мир, {message.from_user.full_name}\n"),
        "- Хочешь со мной сразиться?"
    )
    await message.answer(
        **context.as_kwargs()
    )

@dp.message(Command("settings"))
async def cmd_setting(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Вы не выбрали уровень сложности!"
        )
        return
    level = message.text.split()
    if len(level) == 2:
        global game
        if level[1] == "Easy":
            game = Chess(5, 2)
        elif level[1] == "Medium":
            game = Chess(10, 4)
        elif level[1] == "Hard":
            game = Chess(15, 6)
        else:
            await message.answer(f"Вы не выбрали нужный уровень!!")
            return
        await message.answer(f"Уровень сложности установлен на <b>{level[1]}</b>\n\t Приятной игры!",
                             parse_mode=ParseMode.HTML)
    else:
        await message.answer("Вам нужно выбрать сложность. (пример Easy)")
    

@dp.message(Command("move"))
async def cmd_move(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "- А куда ты ходить собрался, а? (пример Nc3)"
        )
        return
    move = message.text.split()
    if len(move) == 2:
        a = game.move(move[1])
        if a == 1:
            await message.reply("Неверный ход!")
            return
        else:
            await message.answer(f"Вы сделали ход {move[1]}!")
            game.move(move[1])
            stockfish_move = game.stockfish_move()
            await asyncio.sleep(2)
            await message.answer(f"- Я пожалуй пойду на {stockfish_move}")
            await asyncio.sleep(2)
            game.render_png()
            img = types.FSInputFile('board.png')
            await message.answer_photo(img)
    else:
        await message.answer("Невозможный ход. (пример Nc3)")    

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())