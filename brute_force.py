from functools import cache

@cache
def is_solved(board):
    flat = [i for sub in board for i in sub]
    for i in range(0, len(flat) - 1):
        if str(flat[i]) != str(i + 1):
            return False
    return True

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

	if current[0] < len(board) - 1:
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

	if current[1] < len(board[0]) - 1:
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]
		solved = get_solutions([current[0], current[1]+1], board, path + ['r'], depth)
		if solved:
			print(path + ['r'])
		board[current[0]][current[1]], board[current[0]][current[1]+1] = board[current[0]][current[1]+1], board[current[0]][current[1]]

brd = [[7, 1, 0, 4], [13, 9, 3, 2], [14, 11, 12, 6], [10, 15, 8, 5]]
crnt = [0, 2]
get_solutions(tuple(crnt), tuple(brd), tuple([]), 60)