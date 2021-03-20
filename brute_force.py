def get_solutions(current, board, path, depth):
	if len(path) > depth:
		return False

	if len(path) > 1:
		if path[-1] == 'r' and path[-2] == 'l':
			return False
		if path[-1] == 'l' and path[-2] == 'r':
			return False
		if path[-1] == 'h' and path[-2] == 'd':
			return False
		if path[-1] == 'd' and path[-2] == 'h':
			return False

	if is_solved(board):
		solutions.append(path)
		return True

	if current[0] < len(cisla) - 1:
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]+1, current[1]], board, path + ['d'], depth)
		if solved:
			print(path + ['d'])
		board[current[0]][current[1]], board[current[0]+1][current[1]] = board[current[0]+1][current[1]], board[current[0]][current[1]]

	if current[1] > 0:
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]-1], board, path + ['l'], depth)
		if solved:
			print(path + ['l'])
		board[current[0]][current[1]], board[current[0]][current[1]-1] = board[current[0]][current[1]-1], board[current[0]][current[1]]

	if current[0] > 0:
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]
		solved = get_solutions([current[0]-1, current[1]], board, path + ['h'], depth)
		if solved:
			print(path + ['h'])
		board[current[0]][current[1]], board[current[0]-1][current[1]] = board[current[0]-1][current[1]], board[current[0]][current[1]]

	if current[1] < len(cisla[0]) - 1:
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]+1], board, path + ['r'], depth)
		if solved:
			print(path + ['r'])
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]