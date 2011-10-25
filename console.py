import re
from core import GameManager
from pieces import *

class ConsoleUserInterface:
	
	def __init__(self):
		self.game = GameManager() 
		self.input_exp = re.compile(r'\((?P<x>\d),(?P<y>\d)\)')

	def draw(self):
		"""
		This is responcible for displaying the game in a textual manner to
		the user.
		"""

		#print some game info
		player_index = self.game.players.index(self.game.current_player)
		print "Player: " + str(self.game.players[player_index].name)
		print "Turn#: " + str(self.game.turn)

		#TODO: see if there is a better way using map() or something
		#print the board in a grid 
		for y in range(8):
			row = ""
			for x in range(8):
				state = self.game.board[(x,y)].value
				if state == SpaceState.Empty:
					square = "0"
				elif state == SpaceState.Black:
					square = "B"
				elif state == SpaceState.White:
					square = "W"
				else:
					square = "0"

				row = row + " " + square

			print row

	def update(self):
		#requiring correct input
		while True:
			input = raw_input("Enter placement (x,y) or 'pass': ")
			if input.lower() == 'pass':
				self.game.pass_player()
				return True
			elif input.lower() == 'exit':
				return False
			else:
				#this is suppose to be a coordinate for the placement
				match = self.input_exp.match(input)
				if not match: continue

				location = (int(match.groupdict()['x']), 
								int(match.groupdict()['y']))
				
				self.game.make_placement(location)
				return True

if __name__ == '__main__':
	game = ConsoleUserInterface()

	while True:
		game.draw()
		if not game.update():
			print 'Thanks for playing.'
			break
