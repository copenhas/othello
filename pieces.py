import enum

SpaceState = enum.Enumeration("SpaceState", ["Empty", "Black", "White"])
PlayerColor = enum.Enumeration("PlayerColor", ["Black", "White"])

def get_opposite_color(color):
	if color == PlayerColor.Black:
		return PlayerColor.White
	elif color == PlayerColor.White:
		return PlayerColor.Black
	else:
		return None

def get_opposite_state(state):
	if state == SpaceState.Empty:
		return SpaceState.Empty
	elif state == SpaceState.Black:
		return SpaceState.White
	elif state == SpaceState.White:
		return SpaceState.Black
	else:
		return None 

def state_to_color(state):
	if state == SpaceState.Black:
		return PlayerColor.Black
	elif state == SpaceState.White:
		return PlayerColor.White
	else:
		return None

def color_to_state(color):
	if color == PlayerColor.Black:
		return SpaceState.Black
	elif color == PlayerColor.White:
		return SpaceState.White
	else:
		return None

