# ChordTap - An application to bring chord-typing to the masses. Type at the speed of speech.

from pynput import keyboard
import json
from sys import argv
import time

controller = keyboard.Controller()

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

def on_press(key):
	global current_word, last_key_time

	if key == keyboard.Key.esc:
		exit() # ctrl-c
	
	elif (key == keyboard.Key.space or key == keyboard.Key.enter or key == keyboard.Key.tab) or (key in (":", ";", ",", ".", "?", "!", "\"", "'", "(", ")", "-", "{", "}", "[", "]", "|", "\\", "/", "`", "~", "1", "2", "3", "4", "5", "6", "7", "8", "9", "0")):
		for word in words:
			if match_word(word):
				print("Match:", word)

				word_length = len(''.join(current_word)) + 1 # +1 for the space
				print("Backspace", word_length, "times")
				for i in range(word_length):
					controller.press(keyboard.Key.backspace) # backspace
					controller.release(keyboard.Key.backspace)

				controller.type(word)
				
				if key == keyboard.Key.enter:
					controller.press(keyboard.Key.enter)
					controller.release(keyboard.Key.enter)
				elif key == keyboard.Key.space:
					controller.press(keyboard.Key.space)
					controller.release(keyboard.Key.space)
				elif key == keyboard.Key.tab:
					controller.press(keyboard.Key.tab)
					controller.release(keyboard.Key.tab)
				else:
					controller.press(key)
					controller.release(key)
				
				word_history.append(word)

				break
		current_word = []
	
	elif key == keyboard.Key.shift_r:
		if len(current_word) > 0:
			print("Backspace", len(current_word[-1]), "times")
			for i in range(len(current_word[-1])):
				controller.press(keyboard.Key.backspace) # backspace
				controller.release(keyboard.Key.backspace)
			current_word.pop() # remove last chord
			print('Word:', ' '.join(current_word))
		
		elif len(word_history) > 0:
			print("Backspace", len(word_history[-1]) + 1, "times")
			for i in range(len(word_history[-1]) + 1):
				controller.press(keyboard.Key.backspace) # backspace
				controller.release(keyboard.Key.backspace)
			word_history.pop() # remove last word
			print('History:', ' '.join(word_history))
	
	else:
		try:
			if time.time() - last_key_time > 0.1: # if the key was pressed more than 0.1 seconds ago
				# make a new chord
				current_word.append(key.char)
			else:
				# add to the last chord
				current_word[-1] += key.char
			
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
	print("Press right shift to delete last chord/word")
	print("Press esc to exit")

	with keyboard.Listener(on_press=on_press) as listener:
		listener.join()