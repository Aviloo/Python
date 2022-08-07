
import settings

import requests
from bs4 import BeautifulSoup
import datetime
import time
import smtplib

link = settings.link

def file_creation(text):
	CurrentTime = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
	path = f'results\{CurrentTime}' + '.json'
	file = open(path, "w+")
	file.write(text)
	file.close()

def email_send():
	send_address = settings.email_address
	address = settings.your_address
	password = settings.your_password
	CurrentTime = datetime.datetime.now().strftime('%Y_%m_%d %H hours %M minutes %S seconds')
	message = f"The user was online at {CurrentTime}"

	server = smtplib.SMTP("smtp.gmail.com", 587)
	server.starttls()

	try:
		server.login(address, password)
		server.sendmail(address,send_address,message)

		print("Message was sent")
		return
	except Exception as _ex:
		print(f"{_ex}\nCheck your login or password")

def content(html):
	soup = BeautifulSoup(html, 'html.parser')
	names = soup.find_all('div', class_=settings.online_class)

	paragraphs = [p.get_text() for p in soup.find_all('div')]
	spited = str(paragraphs[31:])
	var = spited[spited.find("n") + 1:]
	final_string = var.split('n')[0]
	print(final_string)
	if final_string == "O":
		Time = datetime.datetime.now()
		file_creation(f'At that time ({Time}) the user was online')
		if settings.email_distribution == "False":
			pass
		if settings.email_distribution == "True":
			email_send()
	else:
		pass
	return final_string


def get_html(url):
	result = requests.get(url)
	return result

def listen():
	html = get_html(link)
	if html.status_code == 200:
		content(html.content)
	else:
		print("Error. Check your link")


def main():
	listen()

if __name__ == '__main__':
	StartTime = time.time()
	while True:
		time.sleep(settings.Cooldown - ((time.time() - StartTime) % settings.Cooldown))
		main()







