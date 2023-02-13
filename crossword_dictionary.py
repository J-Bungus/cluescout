from bs4 import BeautifulSoup
import requests
import json
from tqdm import tqdm
import time
import os.path

import defs

def convert_size(size):
	for x in ['bytes', 'KB', 'MB']:
		if size < 1000.0:
			return "%3.1f %s" % (size, x)
		else:
			size /= 1000.0

def update_dictionary(arr, date, direction):
	# takes a list of two values and updates crossword_dictionary
	
	key = arr[1]
	value = arr[0]

	if key in defs.crossword_dictionary:
		answer_list = []
		for clue in defs.crossword_dictionary[key]:
			answer_list.append(clue["clue"])

		if (answer_list.count(value) == 0):
			defs.crossword_dictionary[key].append(
				{
					"clue": value,
					"date": date,
					"direction": direction
				})
	else:
		defs.crossword_dictionary.update(
			{
				key: [
					{
						"clue": value,
						"date": date,
						"direction": direction 
					}
				]
			})

def write():
	# takes crossword_dictionary and pretty prints it to a file called pretty_crossword_dictionary.txt
	#     and creates a json file with the dictionary data

	with open(defs.CROSSWORD_TXT_FILE, 'w') as file:
		for key in defs.crossword_dictionary:
			counter = 1
			file.write("-----\n")
			file.write(f"Answer: {key} \n")
			file.write("Clue: ")
			for clue in defs.crossword_dictionary[key]:
				if counter == 1:
					file.write(f"{counter}. {clue['clue']}\n")
				else:
					file.write(f"      {counter}. {clue['clue']}\n")
				counter += 1

	json_object = json.dumps(defs.crossword_dictionary, indent=4)

	with open(defs.CROSSWORD_JSON_FILE, 'a') as file:
		file.write(json_object)

def get_max_pages(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text, 'html.parser')

	max_page_number = soup.find_all('a', class_="page-numbers")[1].get_text()

	return int(max_page_number)

def get_links(url):
	url_list = []

	request = requests.get(url)
	soup = BeautifulSoup(request.text, "html.parser")

	element_list = soup.find_all('a', attrs={'rel': 'bookmark'})

	for element in element_list:
		url_list.append(element['href'])

	return url_list

def get_data(url):
	request = requests.get(url)
	soup = BeautifulSoup(request.text, "html.parser")
	data_element = soup.find("div", class_="nywrap")
	
	date = soup.find('h1', class_="entry-title").get_text()[-8:]

	if data_element:
		children = data_element.findChildren(recursive=False)
		hz_element_list = children[1].find_all('li')
		ve_element_list = children[len(children) - 1].find_all('li')

		try:
			for element in hz_element_list:
				clue = element.a.get_text()
				answer = element.span.get_text()

				update_dictionary([clue, answer], date, "Across")

			for element in ve_element_list:
				clue = element.a.get_text()
				answer = element.span.get_text()

				update_dictionary([clue,answer], date, "Down")
		except:
			print("WARNING: NO DATA FROM ", url)

def scrape():
	start = time.time()

	crossword_list = []
	crossword_dates = []
	url_list = [defs.BASE_URL]

	max_page_number = get_max_pages(defs.BASE_URL)

	print(f"Fetching source links from {max_page_number} pages...")


	# generate list of urls to pages on target website
	for i in range(max_page_number-1):
		url_list.append(defs.BASE_URL + "page/" + str(i+2) + "/")


	# scrape links to individual crosswords from each page
	for url in tqdm(url_list):
		crossword_list.extend(get_links(url))

	with open(defs.URL_LIST_FILE, "w") as file:
		# scrape clue answer pairs from each crossword
		for crossword in tqdm(crossword_list):
			get_data(crossword)
			file.write(f"{crossword}\n")

	time_taken = time.time() - start
	print("-------------------")
	print(f"| Scrape Complete |")
	print("-------------------")
	print(f"Time: {time_taken}")
	write()
	with open(defs.CROSSWORD_JSON_FILE, 'r') as file:
		json_object = json.load(file)
		print(f"File Size: ")
		print(f"    {defs.CROSSWORD_TXT_FILE}: {convert_size(os.path.getsize(defs.CROSSWORD_TXT_FILE))}")
		print(f"    {defs.CROSSWORD_JSON_FILE}: {convert_size(os.path.getsize(defs.CROSSWORD_JSON_FILE))}")
		print(f"Length: {len(json_object)}")

#scrape()