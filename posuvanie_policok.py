import tkinter
import time
import random
import collections


width = height = 500
a = 100
pad = 50
canvas = tkinter.Canvas(width=width, height=height)
canvas.pack()

cisla = [[7, 1, 0, 4],
		 [13, 9, 3, 2],
		 [14, 11, 12, 6],
		 [10, 15, 8, 5]]
zlte = [1, 3, 6, 8, 9, 11, 14, 0]

prd = [[1,2,3,4],
		 [5,6,7,8],
		 [9,10,11,12],
		 [13,14,15,0]]

jeff = [[1,2,3],
		[4,5,6],
		[7,8,0]]

solutions = []

class Puzzle:
	def __init__(self, board, canvas):
		self.board = board
		self.width = len(board)
		self.tahy = 0
		self.canvas = canvas
		self.current = self.get_current()

	def kresli(self):
		self.canvas.delete('vsetko')
		self.canvas.create_text(a+13, pad//2, text="Počet ťahov: " + str(self.tahy), font='Arial 15', tags='vsetko')
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j] in zlte:
					self.canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='orange', tags='vsetko')
				else:
					self.canvas.create_rectangle(pad+a*j, pad+i*a+a, pad+a*j+a, pad+i*a, fill='grey', tags='vsetko')

				if self.board[i][j] == 0:
					self.canvas.create_text((pad+a*j+pad+a*j+a)//2, (pad+i*a+a+pad+i*a)//2, text='', font='Arial 15', tags='vsetko')
				else:
					self.canvas.create_text((pad+a*j+pad+a*j+a)//2, (pad+i*a+a+pad+i*a)//2, text=self.board[i][j], font='Arial 15', tags='vsetko')

		self.current = self.get_current()

	def get_solution(self, e='<KeyRelease-space>'):
		canvas.create_text(width//2, height-pad, text='Hľadá sa riešenie, môže to trvať až minútu.', font='Arial 15', tags='hladam')
		puzzle = Puzzle(self.board, self.canvas)
		ratios = [1, 2, 6, 7, 8, 9]
		for ratio in ratios:
			s = Solver(puzzle, ratio, 10)
			p = s.solve()
			presnost = ratio
			if p is not None:
				break
			print(ratio)
		else:
			self.canvas.delete('hladam')
			canvas.create_text(width//2, height-pad, text='Riešenie nenájdené', font='Arial 15', tags='hladam')

		result = []
		for node in p:
			if node.action is not None:
				result.append(node.action)

		print(result)
		self.solve_graphically(result, presnost)

	def solve_graphically(self, moves, presnost):
		self.tahy = 0
		steps = len(moves)
		self.canvas.delete('hladam')
		if presnost == 1:
			canvas.create_text(width//2, height-pad, text='Nájdené optimálne riešenie.', font='Arial 15', tags='hladam')
		else:
			if steps <= self.width**2:
				canvas.create_text(width//2, height-pad, text='Nájdené riešenie nemusí byť optimálne.', font='Arial 15', tags='hladam')
			else:
				canvas.create_text(width//2, height-pad, text='Nájdené neoptimálne riešenie.', font='Arial 15', tags='hladam')

		for move in moves:
			if move == 'D':
				self.down()
			elif move == 'U':
				self.up()
			elif move == 'L':
				self.left()
			elif move == 'R':
				self.right()
			self.canvas.update()
			time.sleep(0.5)

		
	def down(self, e='<KeyRelease-Down>'):
		if self.current[0] < self.width - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]+1][self.current[1]] = self.board[self.current[0]+1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def up(self, e='<KeyRelease-Up>'):
		if self.current[0] > 0:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]-1][self.current[1]] = self.board[self.current[0]-1][self.current[1]], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def right(self, e='<KeyRelease-Right>'):
		if self.current[1] < self.width - 1:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1]+1] = self.board[self.current[0]][self.current[1]+1], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	def left(self, e='<KeyRelease-Left>'):
		if self.current[1] > 0:
			self.board[self.current[0]][self.current[1]], self.board[self.current[0]][self.current[1]-1] = self.board[self.current[0]][self.current[1]-1], self.board[self.current[0]][self.current[1]]
			self.tahy += 1
			self.kresli()

	@property
	def solved(self):
		flat = [i for sub in self.board for i in sub]
		for i in range(0, len(flat)-1):
			if str(flat[i]) != str(i+1):
				return False
		return True

	def get_current(self):
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j] == 0:
					current = [i, j]
					return current

	@property
	def actions(self):
		def create_move(at, to):
			return lambda: self.move(at, to)

		moves = []
		for i in range(self.width):
			for j in range(self.width):
				dirs = {'R':(i, j-1),
					  'L':(i, j+1),
					  'D':(i-1, j),
					  'U':(i+1, j)}

				for action, (r, c) in dirs.items():
					if r >= 0 and c >= 0 and r < self.width and c < self.width and self.board[r][c] == 0:
						move = create_move((i,j), (r,c)), action
						moves.append(move)
		return moves

	@property
	def manhattan(self):
		distance = 0
		for i in range(self.width):
			for j in range(self.width):
				if self.board[i][j] != 0:
					x, y = divmod(self.board[i][j]-1, self.width)
					distance += abs(x - i) + abs(y - j)
		return distance

	def shuffle(self):
		puzzle = self
		for _ in range(70):
			puzzle = random.choice(puzzle.actions)[0]()
		return puzzle

	def copy(self):
		board = []
		for row in self.board:
			board.append([x for x in row])
		return Puzzle(board, canvas)

	def move(self, at, to):
		copy = self.copy()
		i, j = at
		r, c = to
		copy.board[i][j], copy.board[r][c] = copy.board[r][c], copy.board[i][j]
		return copy

	def __str__(self):
		return ''.join(map(str, self))

	def __iter__(self):
		for row in self.board:
			yield from row


class Node:
	def __init__(self, puzzle, parent=None, action=None, ratio=1):
		self.puzzle = puzzle
		self.parent = parent
		self.action = action
		self.ratio = ratio
		if (self.parent != None):
			self.g = parent.g + 1
		else:
			self.g = 0

	@property
	def score(self):
		return (self.g + self.h)

	@property
	def state(self):
		return str(self)

	@property
	def path(self):
		node, p = self, []
		while node:
			p.append(node)
			node = node.parent
		yield from reversed(p)

	@property
	def solved(self):
		return self.puzzle.solved

	@property
	def actions(self):
		return self.puzzle.actions

	@property
	def h(self):
		return self.puzzle.manhattan * self.ratio

	@property
	def f(self):
		return self.h + self.g

	def __str__(self):
		return str(self.puzzle)


class Solver:
	def __init__(self, start, ratio=1, timeout=float('inf')):
		self.start = start
		self.ratio = ratio
		self.timeout = timeout

	def solve(self):
		start = time.time()
		queue = collections.deque([Node(self.start)])
		seen = set()
		seen.add(queue[0].state)
		while queue:
			if time.time() - start > self.timeout:
				break
			queue = collections.deque(sorted(list(queue), key=lambda node: node.f))
			node = queue.popleft()
			if node.solved:
				return node.path

			for move, action in node.actions:
				child = Node(move(), node, action, self.ratio)

				if child.state not in seen:
					queue.appendleft(child)
					seen.add(child.state)


#board = [[7, 1, 0, 4], [13, 9, 3, 2], [14, 11, 12, 6], [10, 15, 8, 5]] #jano

# board = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,0]] #spravna

#board = [[5,1,7,3],[9,2,11,4],[13,6,15,8],[0,10,14,12]] #test case 1

#board = [[2,5,13,12],[1,0,3,15],[9,7,14,6],[10,11,8,4]] #test case 2

#board = [[5,2,4,8],[10,0,3,14],[13,6,11,12],[1,15,9,7]] #test case 3

#board = [[11,4,12,2],[5,10,3,15],[14,1,6,7],[0,9,8,13]] #test case 4

#board = [[5,8,7,11],[1,6,12,2],[9,0,13,10],[14,3,4,15]] #test case 5

board = [[1,2,3],[4,5,0],[6,7,8]] #3x3

puzzle = Puzzle(board, canvas)
#puzzle = puzzle.shuffle()
puzzle.kresli()

canvas.bind_all('<KeyRelease-Down>', puzzle.down)
canvas.bind_all('<KeyRelease-Up>', puzzle.up)
canvas.bind_all('<KeyRelease-Right>', puzzle.right)
canvas.bind_all('<KeyRelease-Left>', puzzle.left)
canvas.bind_all('<KeyRelease-space>', puzzle.get_solution)
puzzle.canvas.mainloop()
