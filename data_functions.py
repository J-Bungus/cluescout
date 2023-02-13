from datetime import date
import json
import re
from tabulate import tabulate
from textwrap import TextWrapper

import defs

# Opens crossword_dict.json and returns it as a python dictionary
def open_json():
	crossword_dict = {}

	with open(defs.CROSSWORD_JSON_FILE) as file:
		crossword_dict = json.load(file)

	return crossword_dict

# fix_string(string) takes in a string and returns a string with ",", and ' replaced
#    by its corresponding unicode characters
# requires: string has proper pairing of double quotes, and single quotes are apostrophes
def fix_string(string):
	# determine the number of occurences for quotes
	quote_count = string.count('"')

	# replace the quotes with unicode
	for i in range(quote_count):
		if not(i % 2):
			# replace the first quote with corresponding unicode
			string = string.replace('"', "\u201c", 1) 
		else:
			# replace the second quote with corresponding unicode
			string = string.replace('"', "\u201d", 1)

	# replace all apostrophes with corresponding unicode
	string = string.replace("'", "\u2019")

	return string


# find_answer(clue_in) takes in a clue and outputs the associated answers
def find_answer(clue_in):

	crossword_dict = open_json() # open dicitonary file

	# create regex to search for partial clue matches
	target = ".*" + fix_string(clue_in) + ".*"
	counter = 1 # initialize a counter to keep track of how many answers have been printed
	has_answers = False # initialize bool variable to false, we assume thhere are no matches

	print("Possible Answer(s): ")

	# search for matching answers that are associated with clue_in
	for key in crossword_dict:
		for clue in crossword_dict[key]:

			# if the clues match then we know the answer must be associated with the clue
			if (fix_string(clue_in.lower()) == clue["clue"].lower()):
				print(f"   {counter}. {key} | Crossword: {clue['date']}")
				counter += 1

				# remove from list because we don't want to double count this value 
				crossword_dict[key].remove(clue)

				has_answers = True # set the bool variable to true because there are matches

	# if the counter is still at 1 that means there was no data			
	if (counter == 1):
		print("None")

	print("Partial Clue Match(es): ")
	counter = 1 # reset counter to 1 to keep track of the partial matches that are found

	# search for partial matches of the clue in the dictionary
	for key in crossword_dict:
		for clue in crossword_dict[key]:
			if re.fullmatch(target, clue["clue"], re.I,):
				print(f"   {counter}. {key} | Crossword: {clue['date']}")
				counter += 1
				has_answers = True

	# if the counter is still at 1 that means there was no data
	if (counter == 1):
		print("None")

	# if the the bool variable is still false, then there was no data at all
	if not(has_answers):
		print(f'Sorry, no matches for "{clue_in}"')

# find_clue(answer) takes in an answer and outputs the associated clues 
def find_clue(answer):
	crossword_dict = open_json() # open dictionary file
	target = fix_string(answer) # make sure the string has the correct uni-code substitutions
	counter = 1 # initiate a counter to keep track of how many clues have been printed

	print("Associated Clue(s): ")

	# search dictionary for clues that match the answer given
	for key in crossword_dict.keys():
		if re.fullmatch(target, key, re.I):
			for clue in crossword_dict[key]:
				print(f"   {counter}. {clue['clue']} | Crossword: {clue['date']}")
				counter += 1

	# if the counter is 1, then that means no data was found
	if counter == 1:
		print(f'Sorry, no matches for "{answer}"')

# find_crossword(date) takes in a date that identifies a crossword and outputs all 
#    the clue answer pairs associated with the crossword in a beautiful table
def find_crossword(date):
	crossword_dict = open_json() # open dictionary file
	vertical_list = []
	across_list = []
	wrap = TextWrapper(width=40) # set maximum text-length per line to be 40 characters

	# search dictionary for entries that match the date
	for key in crossword_dict:
		for entry in crossword_dict[key]:

			# sort the entries by across or down
			if entry["date"] == date and entry["direction"] == "Across":
				across_list.append([wrap.fill(entry['clue']), key])
			elif entry["date"] == date:
				vertical_list.append([wrap.fill(entry['clue']), key])

	# print if the date matches a crossword otherwise state that there isn't a match
	if (len(vertical_list) > 0 and len(across_list) > 0):

		print("\n| Across:  \n")
		print(tabulate(across_list, headers=["Clue", "Answer"], tablefmt="fancy_grid"))

		print("\n| Down: \n")
		print(tabulate(vertical_list, headers=["Clue", "Answer"], tablefmt="fancy_grid"))
	else:
		print(f"Sorry, no crossword found for the date: {date}")

def play_game():
	return 0