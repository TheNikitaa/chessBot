import asyncio
from core.game import Chess
from aiogram import Router, F
from aiogram.filters.command import Command, CommandObject
from aiogram import types
from keyboards.menu import *
from aiogram.enums import ParseMode
from config.cfg import load_config

config = load_config()
admin_id = config.tg_bot.admin_id

router = Router()
game = Chess()
game_flag = 0

@router.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        f"Добро пожаловать в шахматный мир, <b>{message.from_user.full_name}</b>\n- Хочешь со мной сразиться?", reply_markup=start_kb(), parse_mode=ParseMode.HTML
    )

@router.message(Command("settings"))
async def cmd_settings(message: types.Message, command: CommandObject):
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
            game = Chess(30, 12)
        else:
            await message.answer(f"Несуществющий уровень сложности!!")
            return
        await message.answer(f"Уровень сложности установлен на <b>{level[1]}</b>\n\t Приятной игры!", reply_markup=start_kb(), parse_mode=ParseMode.HTML)
    else:
        await message.answer("Вам нужно выбрать сложность. (пример Easy)")

@router.message(Command("game"))
async def cmd_game(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "Вы не выбрали цвет для игры - <b>White, Black</b>", reply_markup=game_kb(), parse_mode=ParseMode.HTML
        )
        return
    global game_flag
    if game_flag:
        game.board.reset_board()
        game_flag = 0
        await message.answer("Игра остановлена. Начинаю новую игру!")
    if not game_flag:
        game_flag = 1
    color = message.text.split()
    game.choose_color(color[1])
    if len(color) == 2:
        await message.answer(f"<b>Игра началась.</b> Вы играете за <b>{color[1]}</b>. Для хода используйте комманду /move 'ход'", parse_mode=ParseMode.HTML)
    else:
        await message.answer("Введите цвет корректно! (пример /game White)")


@router.message(F.text.lower() == "об авторах")
async def cmd_about(message: types.Message):
    await message.reply(f"Создать бота - <b>@nikakimvv</b>\nСоздатель сайт - <b>@Timofey78900</b>", reply_markup=start_kb(), parse_mode=ParseMode.HTML)

@router.message(Command("move"))
async def cmd_move(message: types.Message, command: CommandObject):
    if command.args is None:
        await message.answer(
            "- А куда ты ходить собрался, а? (пример /move Nc3)"
        )
        return
    move = message.text.split()
    if len(move) == 2:
        global game_flag
        a = game.move(move[1])
        if a:
            await message.reply("Неверный ход!")
            return
        elif game_flag:
            await message.answer(f"Вы сделали ход <b>{move[1]}</b>",
                                 parse_mode=ParseMode.HTML)
            if game.state():
                await message.answer("Объявлен мат! Вы победили!!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                game_flag = 0
                return
            elif game.state() == 2:
                await message.answer("Объявлен пат! Ничья!!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                game_flag = 0
                return
            stockfish_move = game.stockfish_move()
            if game.state():
                await message.answer("- Похоже я выйграл! Не плачь только!! xD")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                game_flag = 0
                return
            elif game.state() == 2:
                await message.answer("- Похоже я объявил пат.. Ничья?!")
                game.render_png()
                img = types.FSInputFile('board.png')
                await message.answer_photo(img)
                game_flag = 0
                return
            await message.answer(f"- Я пожалуй пойду на <b>{stockfish_move}</b>", 
                                 parse_mode=ParseMode.HTML)
            game.print_moves()
            game.render_png()
            img = types.FSInputFile('board.png')
            await message.answer_photo(img)
        else:
            await message.answer("Вы не начали игру!")
    else:
        await message.answer("Невозможный ход. (пример Nc3)")

@router.message(Command("rate"))
async def cmd_rate(message: types.Message):
    if str(message.from_user.id) == admin_id:
        rate = game.check_position()
        if rate[1]:
            await message.answer(f"Оценка позиции в пользу <b>белых:</b> {rate[0]}", 
                                parse_mode=ParseMode.HTML)
        else:
            await message.answer(f"Оценка позиции в пользу <b>черных:</b> {rate[0]}",
                                parse_mode=ParseMode.HTML)
    else:
        await message.reply(f"Что-то не так {message.from_user.id} {admin_id}")
