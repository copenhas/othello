import graph
from pieces import *

class Player:
	"""
	Represents a player for the game. 'name' is text to represent the player
	and 'color' is a value from 'PlayerColor' for which piece that are using.
	"""
	
	def __init__(self, name, color):
		self.name = name
		self.color = color

class IllegalPlacementError(Exception):
	pass	

class GameManager:
	"""
	GameManager keeps track of the game's state and provides method that
	represent the rules of placement and turns.	
	"""

	def __init__(self, players=[]):
		self.board = self.__create_board()
		self.pieces_left = 60
		self.turn = 1 

		if len(players) == 0:
			self.players = [Player('Black', PlayerColor.Black), 
							Player('White', PlayerColor.White)]
		else:
			self.players = players

		self.current_player = self.players[0]

	def pass_player(self):
		self.__update_turn()


	#TODO: split this up into severl methods for easier testing
	def make_placement(self, location):
		"""
		'location' is a 2 element tuple representing the coordinates of where
		the current player wants to place a piece. This method checks to 
		see if the move is legal (raises IllegalPlacementError if not) and
		changes the state of any square that are captured fromt he placement.
		"""

		#determine if placement is leagl
		if not self.is_legal_placement(self.current_player, location): 
			raise IllegalPlacementError()

		#figure out captures and flip them
		captures = self.captures_for_placement(self.current_player, location)

		#place piece on location to the color of the current player
		state = color_to_state(self.current_player.color)

		#claim captures
		self.board[location].value = state
		for square in captures:
			square.value = state
		
		#update turn and player
		self.__update_turn()
		
	def is_legal_placement(self, player, location):
		"""
		Checks to make sure the hypothical placement of the player's peice at
		the location given. 'location' is a 2 element tuple representing the
		coordinates of where to play the player's piece.
		"""

		#can't play on top of another piece
		if self.board[location].value != SpaceState.Empty: return False
	
		#check adjacent for a peice of opposite color
		possibles, vectors = self.__get_opposite_adjacents(player, location)

		state = color_to_state(self.current_player.color)
		#now follow the nodes until one of the player's color (success)
		#or an empty space (failure)
		while len(possibles) > 0:
			current = possibles.pop()
			vector = vectors.pop()

			try:
				if len(self.__get_until(current, vector, state)) > 0:
					return True
			except:
				pass #not found so not valid

		return False 

	def captures_for_placement(self, player, location):
		"""
		Returns a list of squares that will be captured by the hypothical
		placement of a player's piece at the location. 'location' is a
		2 element tuple representing the coordinates of where the placement is.

		This makes no check to see if the placement is legal, use
		'is_legal_placement' for that.
		"""

		#look in each direction for a piece of the opposite color
		of_interest, vectors = self.__get_opposite_adjacents(player, location)

		state = color_to_state(self.current_player.color)
		#follow that until it hits an empty space or a piece of the player's
		#anything between this placement and a piece of the player's
		#is considered a capture and should be returned
		captures = []
		while len(of_interest) > 0:
			current = of_interest.pop()
			vector = vectors.pop()

			try:
				possible =  self.__get_until(current, vector, state)
				captures = captures + possible
			except:
				pass #not found

		return captures 

	class NotFoundError(Exception):
		pass

	def __update_turn(self):
		self.turn = self.turn + 1
		
		#might as well genericify this
		player_index = self.players.index(self.current_player)
		if player_index == (len(self.players) - 1):
			#start back at the beginning when we reach the last player
			self.current_player = self.players[0]
		else:
			#otherwise just go to the next
			self.current_player = self.players[player_index + 1]

	def __get_opposite_adjacents(self, player, location):
		if not self.board.has_key(location): return []

		node_of_interest = self.board[location]

		opposite_state = get_opposite_state(color_to_state(player.color))
		opposite_node = lambda node: node.value == opposite_state

		nodes = filter(opposite_node, 
							self.board[location].adjacents.itervalues())

		direction = lambda node: (node.id[0] - location[0], 
									node.id[1] - location[1])

		vectors = map(direction, nodes)

		return nodes, vectors

	def __get_until(self, node, vector, state):
		if node.value == SpaceState.Empty: raise NotFoundError()
		if node.value == state: return []

		next_id = (node.id[0] + vector[0], node.id[1] + vector[1])
		if not node.adjacents.has_key(next_id): return [] 

		next_node = node.adjacents[next_id]

		return [node] + self.__get_until(next_node, vector, state)

	def __create_board(self):
		board = graph.Graph()

		#create the board
		for x in range(8):
			for y in range(8):
				board[(x,y)] = graph.NDNode((x,y), SpaceState.Empty)

		#create vertices
		delta_adjacents = [(-1, -1), (0, -1), (1, -1),
							(-1, 0), (1, 0),
						(-1, 1), (0, 1), (1, 1)]
		for square in board:
			for delta in delta_adjacents:
				adjacent = (square.id[0] - delta[0], square.id[1] - delta[1])

				if board.has_key(adjacent):
					square.adjacents[adjacent] = board[adjacent]

		#setup board
		board[(3,3)].value = SpaceState.White
		board[(3,4)].value = SpaceState.Black
		board[(4,3)].value = SpaceState.Black
		board[(4,4)].value = SpaceState.White

		return board

