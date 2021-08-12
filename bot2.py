from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

logging.basicConfig(filename='bot2.log', level=logging.INFO)

PROXY = {'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {'username': settings.PROXY_USERNAME, 'password': settings.PROXY_PASSWORD}}

def on_start(update, context):
	chat = update.effective_chat
	context.bot.send_message(chat_id=chat.id, text="Привет, я Валютный бот!")


def on_message(update, context):
	chat = update.effective_chat
	text = update.message.text
	try:
		number = float(text)
		rate = 86.89
		soms = number * rate
		message = "$%.2f = %.2f р." % (number, soms)
		context.bot.send_message(chat_id=chat.id, text=message)
	except:
		context.bot.send_message(chat_id=chat.id, text="Напишите число для перевода")


def main():
    updater = Updater(settings.API_KEY, use_context=True, request_kwargs=PROXY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", on_start))
    dispatcher.add_handler(MessageHandler(Filters.all, on_message))
    print("Бот запущен. Нажмите Ctrl+C для завершения")
    logging.info("Бот Стартовал")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
