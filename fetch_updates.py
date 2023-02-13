from bs4 import BeautifulSoup
import requests
from datetime import date, datetime, timedelta
from tqdm import tqdm
import json

from crossword_dictionary import *
import defs

# updates_dict() checks if the newest crossword data on the website is different from the data stored
#    on the local machine, if it is different, then it scrapes the website for the updated data
def update_dict():
	day_list = []
	url_list = []

	file_opened = True

	try:
		file = open(defs.CROSSWORD_JSON_FILE, "r")
		defs.crossword_dictionary = json.load(file)

	except:
		print("Something went wrong when opening ", defs.CROSSWORD_JSON_FILE)
		print("OVERWRITING...")
		scrape()

		file_opened = False

	if file_opened:
		r = requests.get(defs.BASE_URL)
		soup = BeautifulSoup(r.text, 'html.parser')
		present_date = datetime.strptime(soup.find('h2', class_="entry-title").get_text()[-8:], "%m/%d/%y")
		data_date = ""

		with open(defs.URL_LIST_FILE, "r") as file:
			file.seek(0, 0)
			date = file.readline()[-10:-2]
			data_date = datetime.strptime(date, "%m-%d-%y")

		date_diff = int((present_date - data_date).days)
		
		if (date_diff > 0):
			for i in range(date_diff):
				day_list.append(data_date + timedelta(i+1))

			for day in day_list:
				url_list.append("https://nytcrosswordanswers.org/nyt-crossword-answers-" + datetime.strftime(day, "%m-%d-%y"))

			with open(defs.URL_LIST_FILE, "a") as file:
				for url in tqdm(url_list):
					file.seek(0, 0)
					get_data(url)
					file.write(f"{url}\n")

			write()
