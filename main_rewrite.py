# ChordTap - An application to bring chord-typing to the masses. Type at the speed of speech.

import keyboard
import json
from sys import argv
import time

words = {}

current_word = [] # list of chords that have been typed
word_history = []

last_key_time = time.time() # time of last keypress

def match_word(word):
	# for each chord in the word, check if it matches the current chord
	# matching is as follows:
	# all characters in the defined chord are present in the input chord

	chords = words[word]

	if len(chords) != len(current_word):
		return False # cannot be present

	for chord_index in range(len(chords)):
		chord = chords[chord_index]
		
		if len(chord) != len(current_word[chord_index]):
			# if the chord is not the same length as the input chord, it cannot be present
			return False

		# check for match
		for char in chord:
			if char not in current_word[chord_index]:
				return False
	
	return True

def backspace_n(number):
	string = ", ".join(["backspace" for i in range(number)])
	keyboard.send(string)

def on_press(key: keyboard.KeyboardEvent):
	global current_word, last_key_time

	if key.name == 'esc':
		exit() # ctrl-c
	
	elif (key.name == 'space' or key.name == 'enter' or key.name == 'tab') or (key.name in (":", ";", ",", ".", "?", "!", "\"", "'", "(", ")", "-", "{", "}", "[", "]", "|", "\\", "/", "`", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0")):
		for word in words:
			if match_word(word):
				print("Match:", word)

				word_length = len(''.join(current_word)) + 1 # +1 for the space
				print("Backspace", word_length, "times")
				backspace_n(word_length)

				keyboard.write(word)
				
				if key.name == 'enter':
					keyboard.send('enter')
				elif key.name == 'space':
					keyboard.send('space')
				elif key.name == 'tab':
					keyboard.send('tab')
				else:
					keyboard.send(key.name)
				
				word_history.append(word)

				break
		current_word = []
	
	elif key.name == 'backspace':
		if len(current_word) > 0:
			print("Backspace", len(current_word[-1])-1, "times")
			backspace_n(len(current_word[-1])-1)
			current_word.pop() # remove last chord
			print('Word:', ' '.join(current_word))
		
		elif len(word_history) > 0:
			print("Backspace", len(word_history[-1]), "times")
			backspace_n(len(word_history[-1]))
			word_history.pop() # remove last word
			print('History:', ' '.join(word_history))
	
	else:
		try:
			if time.time() - last_key_time > 0.1: # if the key was pressed more than 0.1 seconds ago
				# make a new chord
				current_word.append(key.name)
			else:
				# add to the last chord
				current_word[-1] += key.name
			
			print()
			print('Word:', ' '.join(current_word))
			try:
				print('Chord:', ''.join(current_word[-1]))
			except:
				print('No chord')
			print('History:', ' '.join(word_history))
		except: pass
	
	last_key_time = time.time()

if __name__ == '__main__':
	if len(argv) != 2:
		print("Usage: python main.py <dict file>")
		exit()

	try:
		with open(f'dictionaries/{argv[1]}.json', encoding="utf8") as f:
			words = json.load(f)
	except FileNotFoundError:
		print("Dictionary file not found")
		exit()

	print("Press keys to type words")
	print("Press space or enter to submit")
	print("Press backspace to delete last chord")
	print("Press esc to exit")

	keyboard.on_press(on_press)

	while True: pass