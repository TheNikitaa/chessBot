import asyncio
from core.game import Chess
from aiogram import Router, F
from aiogram.filters.command import Command, CommandObject
from aiogram import types
from keyboards.menu import *
from aiogram.enums import ParseMode

router = Router()
game = Chess()

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Добро пожаловать в шахматный мир, <b>{message.from_user.full_name}</b>\n- Хочешь со мной сразиться?", reply_markup=start_kb(), parse_mode=ParseMode.HTML
    )

@router.message(Command("settings"))
async def cmd_setting(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Выберите уровень сложности - <b>Easy, Medium, Hard</b>", reply_markup=settings_kb(),parse_mode=ParseMode.HTML
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
            await message.answer(f"Несуществющий уровень сложности!!")
            return
        await message.answer(f"Уровень сложности установлен на <b>{level[1]}</b>\n\t Приятной игры!",parse_mode=ParseMode.HTML)
    else:
        await message.answer("Вам нужно выбрать сложность. (пример Easy)")

@router.message(Command("game"))
async def cmd_game(message: types.Message):
    pass

@router.message(F.text.lower() == "об авторах")
async def about(message: types.Message):
    pass

@router.message(Command("move"))
async def cmd_move(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "- А куда ты ходить собрался, а? (пример /move Nc3)"
        )
        return
    move = message.text.split()
    if len(move) == 2:
        a = game.move(move[1])
        if a:
            await message.reply("Неверный ход!")
            return
        else:
            await message.answer(f"Вы сделали ход <b>{move[1]}</b>",
                                 parse_mode=ParseMode.HTML)
            game.move(move[1])
            if game.state():
                game.save_pgn()
                await message.answer("Объявлен мат! Вы победили!!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                return
            elif game.state() == 2:
                game.save_pgn()
                await message.answer("Объявлен пат! Ничья!!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                return
            stockfish_move = game.stockfish_move()
            if game.state():
                game.save_pgn()
                await message.answer("- Похоже я выйграл! Не плачь только!! xD")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                return
            elif game.state() == 2:
                game.save_pgn()
                await message.answer("- Похоже я объявил пат.. Ничья?!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                return
            await asyncio.sleep(1.5)
            await message.answer(f"- Я пожалуй пойду на <b>{stockfish_move}</b>", 
                                 parse_mode=ParseMode.HTML)
            await asyncio.sleep(1.5)
            game.render_png()
            img = types.FSInputFile('board.png')
            await message.answer_photo(img)
    else:
        await message.answer("Невозможный ход. (пример Nc3)")

@router.message(Command("rate"))
async def cmd_rate(message: types.Message):
    rate = game.check_position()
    if rate[1]:
        await message.answer(f"Оценка позиции в пользу <b>белых:</b> {rate[0]}", 
                             parse_mode=ParseMode.HTML)
    else:
        await message.answer(f"Оценка позиции в пользу <b>черных:</b> {rate[0]}",
                             parse_mode=ParseMode.HTML)
