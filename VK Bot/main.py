import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from tk import fmain_token
import time 
import log
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import json
from datetime import datetime
import threading
import sys
import sqlite3 as sq

def DataBase():
	with sq.connect("test.db") as con:
		cur = con.cursor()
		cur.execute("""CREATE TABLE IF NOT EXISTS users(
			name TEXT NOT NULL,
			vk_id TEXT NOT NULL,
			time TEXT NOT NULL
		)""")


#Автоматический ввод текста рассылки при запуске
def start():
	print("Bot Start")
	print("Введите сcылку с инфо о последних проекта(для .update) : ")
	uupdate = input()
	print("Введите сообщение для начала рассылки : ")
	ssend = input()



def bot():
	keyboard = VkKeyboard(one_time=True) # cоздаю клавиатуру (one_time - многоразовасть клавиатуры)
	keyboard.add_button(".help - список команд")
	keyboard.add_line()
	keyboard.add_button('.update - новости сервера', color=VkKeyboardColor.POSITIVE)


	vk_session = vk_api.VkApi(token = fmain_token)
	session_api = vk_session.get_api()
	longpoll = VkLongPoll(vk_session)
	vk = vk_session.get_api()



	def sender(id, text):
		vk_session.method('messages.send', {'user_id' :id, 'message' :text, 'random_id' :0, 'keyboard' :keyboard.get_keyboard()})
	def send_post(id, url):
		vk_session.method('messages.send', {'user_id' :id, 'attachment' :url, 'random_id' :0})


	print("Bot On")


	for event in longpoll.listen():
		if event.type == VkEventType.MESSAGE_NEW:
			if event.to_me:
				msg = event.text.lower()
				id = event.user_id
				if msg == "начать":
					sender(id, 'Здравствуйте.Меня зовут Рон и я ваш бот-помошник.')
				if msg == "quitbr":
					sender(id, 'Начинаю процесс')
					sender(id, 'Успешно!...')
					sys.exit()

				if msg == ".update":
					send_post(id, uupdate)
					sender(id, 'Сверху ссылка на пост о последнем обновлении')
				if msg == '.update - новости сервера':
					send_post(id, uupdate)
					sender(id, 'Сверху ссылка на пост о последнем обновлении')

				if msg == "++":
					sender(id, 'Рассылка on')
				if msg == ".help - список команд":
					sender(id, '.report - подать жалобу на игрока')
					sender(id, '.ban - Обжаловать неверно назначенное наказание')
					sender(id, '.other - связаться с администрацией')
					sender(id, '.update - узнать о последнем обновлении')
					sender(id, '.help - список команд(ты уже знаешь xd)')
				if msg == ".report":
					sender(id, 'Напишите свой ник, ник игрока ,который,по вашему мнению,нарушил правила и изложите суть жалобы, а также предоставте доказательства(скриншот,видеоролик и т.д)  - если имеются.')
					sender(id, 'Ваша жалоба будет рассмотрена администрацией после того, как вы отправите необходимые данные.')
				if msg == ".other":
					sender(id, 'Ваше сообщение будет отправленно администрации. Ожидайте ответа')
				if msg == ".ban":
					sender(id, 'Напишите свой ник и изложите суть жалобы')
					sender(id, 'Администрация ответит в скором времени. Удачи')
				if msg == ".help":
					sender(id, '.report - подать жалобу на игрока')
					sender(id, '.ban - Обжаловать неверно назначенное наказание')
					sender(id, '.other - связаться с администрацией')
					sender(id, '.update - узнать о последнем обновлении')
					sender(id, '.help - список команд(ты уже знаешь xd)')
				else:
					sender(id, 'Напишите команду .help ,чтобы увидеть список доступных команд.')

def main():
	start()
	DataBase()
	bot()

if __name__ == "__main__":
	main()