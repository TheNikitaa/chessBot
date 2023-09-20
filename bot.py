from config.cfg import load_config
import core.game

config = load_config()

bot_token = config.tg_bot.token
admin = config.tg_bot.admin_id

# print(bot_token)
# print(admin)
