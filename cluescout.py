from datetime import datetime
import pyfiglet
import json

import defs
from cli_functions import *
from crossword_dictionary import *
from fetch_updates import *
from data_functions import *

def main():
	print("\n\n\n")
	result = pyfiglet.figlet_format("Clue Scout", font="roman")
	print(result, end="")

	try:
		file = open(defs.CROSSWORD_JSON_FILE, 'x+')
		scrape()

	except FileExistsError:
		update_dict()

	option = menu().lower(); # program is not case-sensitive so input is changed to lower case

	# continuously re-prompt the user until valid input is entered
	while (option != "a" and option != "b" and option != "c" and option != "x"):
		option = menu(True).lower()

	# continously prompt the user until they want to exit
	while (option != "x"):
		if (option == "a"):
			option = search_clues().lower()
		elif (option == "b"):
			option = search_answers().lower()
		elif (option == "c"):
			option = search_crosswords().lower()
		elif (option == "q"):
			option = menu()
			while (option != "a" and option != "b" and option != "c" and option != "x"):
				option = menu(True).lower()

main()